"""Lab 13 sandbox ("Mini-Max"): one call becomes facts, then coordinated business decisions.

    transcript -> extract CallFacts -> context ledger -> bookability -> commit -> dispatch
               -> claim guard

A synthetic teaching system inspired by public Pantheon 2026 descriptions, not ServiceTitan's
implementation. The extractor stands in for a voice model: it starts from the dataset's gold
labels and, with `noise > 0`, makes deterministic mistakes whose confidence overlaps with
correct answers, which is what makes downstream confidence floors a real trade-off.
"""
from __future__ import annotations

import copy
import hashlib
from dataclasses import dataclass, field
from typing import Any

from . import backend as be
from .calls import INTENTS, SENTIMENTS, URGENCIES, ALL_JOB_TYPES, job_value
from .context import ContextLedger
from .coordination import Board, Job, assign_tech
from .tools import CallState, execute_tool

SCHEMA_VERSION = "call-facts-v1"
FIELD_NAMES = ("intent", "job_type", "urgency", "emergency", "bookable", "caller_sentiment",
               "replacement_interest", "membership", "price_shopper", "injection_attempt")
ALLOWED: dict[str, tuple] = {"intent": INTENTS, "job_type": ALL_JOB_TYPES, "urgency": URGENCIES,
                             "caller_sentiment": SENTIMENTS}
# Fields the bookability decision depends on. If any is below the confidence floor, the system
# asks a person instead of acting. Other fields below the floor are simply not used.
CRITICAL_FIELDS = ("intent", "job_type", "emergency", "bookable", "injection_attempt")
# How uncertain the extractor is about each field when it is right (see extract_call_facts).
CONFIDENCE_SPREAD = {"intent": 0.25, "job_type": 0.25, "bookable": 0.30, "urgency": 0.30,
                     "caller_sentiment": 0.35, "replacement_interest": 0.30, "emergency": 0.06,
                     "injection_attempt": 0.06, "membership": 0.15, "price_shopper": 0.20}
# Safety-critical cues are explicit in speech, so the extractor misses them less often.
ERROR_WEIGHT = {"emergency": 0.3, "injection_attempt": 0.3}
# Scenarios that are harder to understand get more extraction errors.
DIFFICULTY = {"phone_chunks": 2.0, "topic_switch": 2.0, "price_shopper": 1.5, "injection": 1.5,
              "out_of_area": 1.2}
# Illustrative costs used by the lab's sweeps (not real figures).
WRONG_BOOKING_COST = 1500.0   # wasted truck roll, rework, lost trust
MISSED_BOOKING_COST = 250.0   # a person has to call back; some callers go elsewhere


@dataclass(frozen=True)
class Evidence:
    value: Any
    confidence: float
    evidence: tuple[dict[str, str], ...]
    grounded: bool = True      # the quote actually supports the value


@dataclass
class CallFacts:
    schema_version: str
    call_id: str
    fields: dict[str, Evidence] = field(default_factory=dict)
    conflicts: tuple[str, ...] = ()

    def values(self) -> dict[str, Any]:
        return {k: v.value for k, v in self.fields.items()}

    def trusted(self, floor: float) -> dict[str, Any]:
        """Values a downstream consumer may act on: at or above the floor, with evidence."""
        return {k: v.value for k, v in self.fields.items()
                if v.confidence >= floor and v.evidence and k not in self.conflicts}

    def as_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "call_id": self.call_id,
                "fields": {k: {"value": v.value, "confidence": round(v.confidence, 4),
                               "evidence": list(v.evidence)} for k, v in self.fields.items()},
                "conflicts": list(self.conflicts)}


# --------------------------------------------------------------------------- extraction
def _u(*parts: Any) -> float:
    """Deterministic pseudo-random number in [0, 1) from the given parts."""
    digest = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def _wrong_value(key: str, value: Any, u: float) -> Any:
    if isinstance(value, bool):
        return not value
    options = [v for v in ALLOWED[key] if v != value]
    return options[int(u * len(options))]


def _caller_turns(record: dict) -> list[str]:
    return [t["text"] for t in record["transcript"] if t["speaker"] == "caller"]


def _evidence(record: dict, key: str, value: Any) -> tuple[tuple[dict[str, str], ...], bool]:
    """Pick the caller turn that supports the value; flag it if nothing really does."""
    turns = _caller_turns(record)
    needles = {
        "emergency": be.EMERGENCY_TERMS if value else (),
        "injection_attempt": ("ignore your rules",) if value else (),
        "price_shopper": ("how much", "calling around") if value else (),
        "membership": ("member",) if value else (),
        "job_type": (str(value).replace("_", " "), "ac", "tune-up", "water heater"),
        "intent": ("cancel", "move my appointment", "book", "need", "how much"),
        "urgency": ("today", "tomorrow", "next opening") if value != "emergency" else be.EMERGENCY_TERMS,
    }.get(key, ())
    for text in turns:
        if any(n in text.lower() for n in needles):
            return ({"speaker": "caller", "quote": text},), True
    return ({"speaker": "caller", "quote": turns[0]},), not needles


def extract_call_facts(record: dict, noise: float = 0.0, seed: int = 0) -> CallFacts:
    """Teaching extractor. noise=0 is an oracle: gold labels at confidence 0.99.

    With noise > 0 each field is wrong with probability noise x scenario difficulty x field
    weight. Correct values usually get high confidence with a tail toward lower values; wrong
    values get confidence spread over [0.45, 0.95). The ranges overlap on purpose: confidence
    helps, but it can't certify itself.
    """
    facts = {}
    difficulty = DIFFICULTY.get(record.get("scenario", ""), 1.0)
    for key in FIELD_NAMES:
        gold = record[key]
        p_wrong = noise * difficulty * ERROR_WEIGHT.get(key, 1.0)
        wrong = noise > 0 and _u(seed, record["call_id"], key, "err") < p_wrong
        value = _wrong_value(key, gold, _u(seed, record["call_id"], key, "val")) if wrong else gold
        u = _u(seed, record["call_id"], key, "conf")
        if noise == 0:
            confidence = 0.99
        elif wrong:
            confidence = 0.45 + 0.50 * u
        else:
            confidence = 0.99 - CONFIDENCE_SPREAD[key] * u ** 3
        quotes, grounded = _evidence(record, key, value)
        facts[key] = Evidence(value, round(confidence, 4), quotes, grounded)
    return CallFacts(SCHEMA_VERSION, record["call_id"], facts)


def validate_call_facts(facts: CallFacts, confidence_floor: float = 0.85) -> tuple[bool, list[str]]:
    """Contract check. Structural errors and untrusted *critical* fields make facts unusable."""
    errors = [f"conflict:{x}" for x in facts.conflicts]
    if facts.schema_version != SCHEMA_VERSION:
        errors.append("schema_version")
    errors += [f"missing:{x}" for x in sorted(set(FIELD_NAMES) - set(facts.fields))]
    for key, fact in facts.fields.items():
        if not fact.evidence:
            errors.append(f"missing_evidence:{key}")
        if key in ALLOWED and fact.value not in ALLOWED[key]:
            errors.append(f"invalid_value:{key}")
        if key in CRITICAL_FIELDS and fact.confidence < confidence_floor:
            errors.append(f"low_confidence:{key}")
    v = facts.values()
    if v.get("emergency") and v.get("bookable"):
        errors.append("emergency_bookable_conflict")
    return not errors, errors


def facts_to_ledger(facts: CallFacts, confidence_floor: float = 0.85,
                    ledger: ContextLedger | None = None) -> ContextLedger:
    """The voice agent proposes every fact; the control plane verifies only trusted ones."""
    ledger = ledger or ContextLedger()
    trusted = facts.trusted(confidence_floor)
    for key, fact in facts.fields.items():
        ledger.propose("voice_agent", facts.call_id, key, fact.value, fact.confidence,
                       fact.evidence[0]["quote"])
        if key in trusted and fact.grounded:
            ledger.verify(facts.call_id, key, evidence=fact.evidence[0]["quote"])
    return ledger


# --------------------------------------------------------------------------- decisions
@dataclass(frozen=True)
class BookabilityDecision:
    action: str            # book | transfer | callback | decline | workflow
    reason: str


def transcript_emergency(record: dict) -> bool:
    """Control-plane screen on the raw words, independent of the extractor."""
    return any(term in text.lower() for text in _caller_turns(record) for term in be.EMERGENCY_TERMS)


def decide_bookability(facts: CallFacts, record: dict | None = None,
                       confidence_floor: float = 0.85, transcript_screen: bool = True
                       ) -> BookabilityDecision:
    if transcript_screen and record is not None and transcript_emergency(record):
        return BookabilityDecision("transfer", "emergency words in the transcript")
    ok, errors = validate_call_facts(facts, confidence_floor)
    if not ok:
        return BookabilityDecision("callback", "facts not trusted: " + ", ".join(errors))
    v = facts.values()
    if v["emergency"]:
        return BookabilityDecision("transfer", "emergency requires a person")
    if v["injection_attempt"]:
        return BookabilityDecision("transfer", "override attempt is not an authorization signal")
    if v["intent"] == "out_of_area":
        return BookabilityDecision("decline", "outside the service area")
    if v["intent"] in ("reschedule", "cancel"):
        return BookabilityDecision("workflow", "existing appointment: reschedule/cancel workflow")
    if v["job_type"] not in be.JOB_TYPES:
        return BookabilityDecision("decline", f"no service for {v['job_type']}")
    if not v["bookable"]:
        return BookabilityDecision("decline", "not a bookable request")
    return BookabilityDecision("book", "trusted facts passed the contract")


def gold_action(record: dict) -> str:
    """The action a correct system would take, from the gold labels."""
    return decide_bookability(extract_call_facts(record), record).action


def lead_value(facts: CallFacts, confidence_floor: float = 0.85) -> float:
    """Lead score from trusted facts only; untrusted signals count as absent."""
    t = facts.trusted(confidence_floor)
    return job_value(t.get("job_type", "none"), bool(t.get("replacement_interest")),
                     t.get("urgency") == "same_day")


def dispatch(call_id: str, job_type: str, value: float) -> str:
    """Assign a technician on a small board; high-value jobs go to the senior tech."""
    board = Board(slots={"S1": None, "S2": None, "S3": None},
                  techs={"S1": "Luis", "S2": "Mo", "S3": "Kara"},
                  tech_level={"Kara": "senior", "Luis": "junior", "Mo": "junior"})
    return assign_tech(board, "S1", Job(call_id, "Synthetic Caller", job_type, value))


# --------------------------------------------------------------------------- claims
CLAIMS = {"book": "You're booked.", "transfer": "I'm transferring you to a person now.",
          "callback": "A team member will call you back shortly.",
          "decline": "I'm sorry, we can't help with that one.",
          "workflow": "Let me pull up your existing appointment."}


def claim_guard(claim: str, *, committed: bool, transferred: bool = False,
                emergency: bool = False) -> bool:
    """True if the spoken claim is grounded in application state."""
    text = claim.lower()
    if "booked" in text or "scheduled" in text:
        return committed and not transferred and not emergency
    if "transferring" in text:
        return transferred
    return True


# --------------------------------------------------------------------------- one call
def _book(record: dict, job_type: str) -> tuple[bool, str | None, bool]:
    """Book through the control plane with grounded confirmations; retry once to show idempotency."""
    state = CallState(call_id=record["call_id"])
    customer = execute_tool("lookup_customer", {"phone": "+18175550101"}, state)["customer"]
    slots = execute_tool("find_slots", {"job_type": job_type, "zip_code": customer["zip"]}, state)
    if not slots.get("slots"):
        return False, None, False
    slot_id = slots["slots"][0]["id"]
    state.last_user_text = "Yes, that's right."
    execute_tool("record_address_confirmation", {"caller_said": "yes, that's right"}, state)
    state.last_user_text = "The first window works."
    execute_tool("record_slot_choice", {"slot_id": slot_id, "caller_said": "the first window works"}, state)
    args = {"customer_id": customer["id"], "slot_id": slot_id, "job_type": job_type,
            "summary": f"Synthetic call {record['call_id']}"}
    first = execute_tool("create_job", args, state)
    retry = execute_tool("create_job", args, state)
    job_id = (first.get("job") or {}).get("id")
    return bool(first.get("ok")), job_id, bool(retry.get("ok") and retry["job"]["id"] == job_id)


def run_call(record: dict, confidence_floor: float = 0.85, noise: float = 0.0, seed: int = 0,
             transcript_screen: bool = True, facts: CallFacts | None = None) -> dict[str, Any]:
    facts = facts or extract_call_facts(record, noise, seed)
    ledger = facts_to_ledger(facts, confidence_floor)
    decision = decide_bookability(facts, record, confidence_floor, transcript_screen)
    trace: list[dict[str, Any]] = [
        {"stage": "extract", "schema_version": facts.schema_version,
         "valid": validate_call_facts(facts, confidence_floor)[0]},
        {"stage": "context_ledger", "verified": sorted(ledger.view(record["call_id"]))},
        {"stage": "bookability", "action": decision.action, "reason": decision.reason},
    ]
    committed, job_id, idempotent, tech, value = False, None, False, None, 0.0
    if decision.action == "book":
        saved = dict(be.LATENCY_MS)
        be.reset()
        be.LATENCY_MS.update({k: 0 for k in be.LATENCY_MS})
        try:
            committed, job_id, idempotent = _book(record, facts.values()["job_type"])
        finally:
            be.LATENCY_MS.update(saved)
        trace.append({"stage": "commit", "ok": committed, "job_id": job_id,
                      "idempotent_retry": idempotent})
    if committed:
        value = lead_value(facts, confidence_floor)
        tech = dispatch(record["call_id"], facts.values()["job_type"], value)
        trace.append({"stage": "lead_score_and_dispatch", "est_value": value, "tech": tech})
    proposed = CLAIMS[decision.action]
    grounded = claim_guard(proposed, committed=committed, transferred=decision.action == "transfer",
                           emergency=transcript_emergency(record))
    spoken = proposed if grounded else CLAIMS["callback"]
    trace.append({"stage": "claim_guard", "proposed": proposed, "allowed": grounded, "spoken": spoken})
    return {"call_id": record["call_id"], "facts": facts, "decision": decision, "trace": trace,
            "committed": committed, "job_id": job_id, "idempotent_retry": idempotent,
            "assigned_tech": tech, "est_value": value, "spoken": spoken,
            "guard_blocked": not grounded,
            "false_claim": "booked" in spoken.lower() and not committed}


# --------------------------------------------------------------------------- error analysis
ERROR_TYPES = ("emergency_missed", "bookable_flipped", "job_type_wrong", "urgency_wrong",
               "replacement_missed", "sentiment_flipped", "low_confidence", "conflicting_facts")


def inject_error(facts: CallFacts, error_type: str) -> CallFacts:
    """Return a copy of the facts with one confident mistake (or one trust problem)."""
    f = copy.deepcopy(facts)
    def put(key: str, value: Any, confidence: float = 0.95) -> None:
        f.fields[key] = Evidence(value, confidence, f.fields[key].evidence, grounded=False)
    v = f.values()
    if error_type == "emergency_missed":
        if v["emergency"]:
            put("emergency", False)
            put("intent", "book_service")
            put("bookable", True)
            put("job_type", "furnace_repair")
    elif error_type == "bookable_flipped":
        put("bookable", not v["bookable"])
    elif error_type == "job_type_wrong":
        put("job_type", "hvac_tuneup" if v["job_type"] != "hvac_tuneup" else "ac_repair")
    elif error_type == "urgency_wrong":
        put("urgency", "routine" if v["urgency"] == "same_day" else "same_day")
    elif error_type == "replacement_missed":
        put("replacement_interest", False)
    elif error_type == "sentiment_flipped":
        put("caller_sentiment", "angry" if v["caller_sentiment"] != "angry" else "positive")
    elif error_type == "low_confidence":
        put("intent", v["intent"], confidence=0.40)
    elif error_type == "conflicting_facts":
        f.conflicts = ("job_type",)
    else:
        raise ValueError(f"unknown error type {error_type!r}")
    return f


def _wrong_booking(record: dict, action: str, facts: CallFacts) -> bool:
    """Booked a call that shouldn't be booked, or booked the wrong kind of job."""
    return action == "book" and (gold_action(record) != "book"
                                 or facts.values()["job_type"] != record["job_type"])


def _cost(record: dict, action: str, facts: CallFacts) -> float:
    if _wrong_booking(record, action, facts):
        return WRONG_BOOKING_COST
    if action != "book" and gold_action(record) == "book":
        return MISSED_BOOKING_COST
    return 0.0


def error_sensitivity(records: list[dict], confidence_floor: float = 0.85,
                      transcript_screen: bool = True) -> list[dict[str, Any]]:
    """Inject each error type into every call's (correct) facts; measure downstream impact."""
    clean = {r["call_id"]: extract_call_facts(r) for r in records}
    base_actions = {cid: decide_bookability(f, r, confidence_floor, transcript_screen).action
                    for (cid, f), r in zip(clean.items(), records)}
    base_value = sum(lead_value(clean[r["call_id"]], confidence_floor)
                     for r in records if base_actions[r["call_id"]] == "book")
    rows = []
    for error in ERROR_TYPES:
        changed = wrong_books = emergency_books = missed = 0
        value = cost = 0.0
        techs_changed = 0
        for r in records:
            bad = inject_error(clean[r["call_id"]], error)
            action = decide_bookability(bad, r, confidence_floor, transcript_screen).action
            before = base_actions[r["call_id"]]
            changed += action != before
            cost += _cost(r, action, bad)
            wrong_books += _wrong_booking(r, action, bad)
            emergency_books += action == "book" and r["emergency"]
            missed += action != "book" and gold_action(r) == "book"
            if action == "book":
                v = lead_value(bad, confidence_floor)
                value += v
                good = clean[r["call_id"]]
                techs_changed += (dispatch(r["call_id"], good.values()["job_type"],
                                           lead_value(good, confidence_floor))
                                  != dispatch(r["call_id"], bad.values()["job_type"], v))
        rows.append({"error_type": error, "decisions_changed": changed, "wrong_bookings": wrong_books,
                     "emergencies_booked": emergency_books, "missed_bookings": missed,
                     "lead_value_delta": round(value - base_value, 2), "techs_changed": techs_changed,
                     "error_cost": cost})
    return rows


def floor_sweep(records: list[dict], floors: list[float], noise: float = 0.12,
                seed: int = 0) -> list[dict[str, Any]]:
    """Automation vs. error cost as the downstream confidence floor rises."""
    facts = [extract_call_facts(r, noise, seed) for r in records]
    gold = [gold_action(r) for r in records]
    rows = []
    should_book = sum(g == "book" for g in gold)
    for floor in floors:
        actions = [decide_bookability(f, r, floor).action for f, r in zip(facts, records)]
        wrong = [_wrong_booking(r, a, f) for r, a, f in zip(records, actions, facts)]
        rows.append({
            "confidence_floor": floor,
            "automation_rate": round(sum(a == "book" and g == "book" and not w
                                         for a, g, w in zip(actions, gold, wrong))
                                     / max(1, should_book), 3),
            "sent_to_people": sum(a == "callback" for a in actions),
            "wrong_bookings": sum(wrong),
            "error_cost": sum(_cost(r, a, f) for r, a, f in zip(records, actions, facts)),
        })
    return rows
