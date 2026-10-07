"""Lab 13 sandbox: one call becomes facts, then coordinated business decisions."""
from __future__ import annotations
import copy
from dataclasses import dataclass, field
from typing import Any
from .calls import SCHEMA_VERSION
from .context import ContextLedger, context_tools
from .coordination import Board, Job, assign_tech, lead_score
from . import backend as be
from .tools import CallState, execute_tool

ALLOWED = {
    "intent": {"book_service","price_quote","reschedule","cancel","out_of_area","emergency","unknown","spam"},
    "job_type": {"ac_repair","furnace_repair","hvac_tuneup","plumbing_leak","electrical_issue","none"},
    "urgency": {"emergency","same_day","soon","routine","none"},
    "caller_sentiment": {"positive","neutral","frustrated","angry"},
}
FIELD_NAMES = ("intent","job_type","urgency","emergency","bookable","caller_sentiment",
               "replacement_interest","membership","price_shopper","injection_attempt")

@dataclass(frozen=True)
class Evidence:
    value: Any
    confidence: float
    evidence: tuple[dict[str, str], ...]

@dataclass
class CallFacts:
    schema_version: str
    call_id: str
    fields: dict[str, Evidence] = field(default_factory=dict)

    def values(self) -> dict[str, Any]:
        return {k: v.value for k, v in self.fields.items()}

    def as_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "call_id": self.call_id,
                "fields": {k: {"value": v.value, "confidence": v.confidence,
                               "evidence": list(v.evidence)} for k, v in self.fields.items()}}

def _evidence(record: dict, needle: str) -> tuple[dict[str, str], ...]:
    rows = []
    for turn in record["transcript"]:
        if turn["speaker"] == "caller" and (not needle or needle.lower() in turn["text"].lower()):
            rows.append({"speaker": "caller", "quote": turn["text"]})
    if not rows:
        rows = [{"speaker": "caller", "quote": record["transcript"][0]["text"]}]
    return tuple(rows[:2])

def extract_call_facts(record: dict, confidence: float = 0.96) -> CallFacts:
    """Teaching extractor: gold labels stand in for a deterministic scripted voice model."""
    vals = {k: record[k] for k in FIELD_NAMES}
    facts = {}
    for key, value in vals.items():
        needle = str(value).replace("_", " ")
        facts[key] = Evidence(value, confidence, _evidence(record, needle))
    return CallFacts("call-facts-v1", record["call_id"], facts)

def validate_call_facts(facts: CallFacts, confidence_floor: float = 0.85) -> tuple[bool, list[str]]:
    errors = []
    if facts.schema_version != "call-facts-v1":
        errors.append("schema_version")
    missing = set(FIELD_NAMES) - set(facts.fields)
    errors.extend(f"missing:{x}" for x in sorted(missing))
    for key, fact in facts.fields.items():
        if fact.confidence < confidence_floor:
            errors.append(f"low_confidence:{key}")
        if not fact.evidence:
            errors.append(f"missing_evidence:{key}")
        if key in ALLOWED and fact.value not in ALLOWED[key]:
            errors.append(f"invalid_value:{key}")
    if facts.fields.get("emergency", Evidence(False, 1, ())).value and facts.fields.get("bookable", Evidence(False, 1, ())).value:
        errors.append("emergency_bookable_conflict")
    return not errors, errors

def facts_to_ledger(facts: CallFacts, confidence_floor: float = 0.85) -> ContextLedger:
    ok, errors = validate_call_facts(facts, confidence_floor)
    if not ok:
        raise ValueError("; ".join(errors))
    ledger = ContextLedger()
    voice = context_tools(ledger, "voice_agent")
    for key, fact in facts.fields.items():
        if key in voice_keys():
            result = voice["propose_fact"](facts.call_id, key, fact.value, fact.confidence,
                                           fact.evidence[0]["quote"])
            if not result["ok"]:
                raise ValueError(result)
            ledger.verify(facts.call_id, key, evidence=fact.evidence[0]["quote"])
    return ledger

def voice_keys() -> set[str]:
    return {"intent","job_type","urgency","caller_sentiment","callback_window",
            "equipment","constraint","replacement_interest","membership",
            "price_shopper","injection_attempt","emergency","bookable"}

@dataclass(frozen=True)
class BookabilityDecision:
    action: str
    reason: str
    confidence: float

def decide_bookability(facts: CallFacts, confidence_floor: float = 0.85) -> BookabilityDecision:
    ok, errors = validate_call_facts(facts, confidence_floor)
    if not ok:
        return BookabilityDecision("callback", "facts rejected: " + ", ".join(errors), 0.0)
    v = facts.values()
    if v["emergency"]:
        return BookabilityDecision("transfer", "emergency requires human handling", 0.99)
    if v["injection_attempt"]:
        return BookabilityDecision("transfer", "prompt-injection attempt is not an authorization signal", 0.99)
    if v["intent"] == "out_of_area":
        return BookabilityDecision("decline", "outside the teaching service area", 0.98)
    if v["intent"] in {"reschedule", "cancel"}:
        return BookabilityDecision("callback", "use the dedicated appointment workflow", 0.98)
    if not v["bookable"]:
        return BookabilityDecision("decline", "gold call is not a bookable opportunity", 0.95)
    return BookabilityDecision("book", "bookable facts passed the contract", 0.97)

def lead_score_from_facts(facts: CallFacts) -> float:
    v = facts.values()
    signals = []
    if v["replacement_interest"]: signals.append("replacement_interest")
    if v["urgency"] == "same_day": signals.append("same_day_needed")
    if v["urgency"] == "emergency": signals.append("system_down")
    return lead_score(v["job_type"], signals)

def dispatch_for_facts(facts: CallFacts) -> tuple[str | None, float]:
    v = facts.values()
    value = lead_score_from_facts(facts)
    board = Board(
        slots={"S1": None, "S2": None, "S3": None},
        techs={"S1": "Kara", "S2": "Luis", "S3": "Mo"},
        tech_level={"Kara": "senior", "Luis": "junior", "Mo": "junior"},
    )
    job = Job(facts.call_id, "Synthetic Caller", v["job_type"], value,
              signals=["same_day_needed"] if v["urgency"] == "same_day" else [])
    slot = board.open_slots()[0]
    tech = assign_tech(board, slot, job)
    return tech, value

def claim_guard(claim: str, *, committed: bool, transferred: bool = False,
                emergency: bool = False) -> bool:
    """True means the proposed spoken claim is grounded in committed application state."""
    text = claim.lower()
    if "booked" in text or "scheduled" in text:
        return committed and not transferred and not emergency
    if "transferring" in text or "human" in text:
        return transferred
    return True

def run_call(record: dict, confidence_floor: float = 0.85) -> dict[str, Any]:
    facts = extract_call_facts(record)
    decision = decide_bookability(facts, confidence_floor)
    tech, est_value = dispatch_for_facts(facts)
    trace = [{"stage":"extract", "schema_version":facts.schema_version,
              "valid":validate_call_facts(facts, confidence_floor)[0]},
             {"stage":"bookability", "action":decision.action, "reason":decision.reason},
             {"stage":"lead_score", "est_value":est_value, "assigned_tech":tech}]
    committed = False
    job_id = None
    retry_same = False
    be.reset()
    be.LATENCY_MS.update({k: 0 for k in be.LATENCY_MS})
    if decision.action == "book":
        state = CallState(call_id=record["call_id"])
        customer = be.lookup_customer("+18175550101")
        state.customer = customer
        slots = be.find_slots(record["job_type"] if record["job_type"] in be.JOB_TYPES else "ac_repair", customer["zip"])
        if slots:
            state.offered_slot_ids = [s["id"] for s in slots]
            state.address_confirmed = True
            state.slot_confirmed = True
            state.chosen_slot_id = slots[0]["id"]
            result = execute_tool("create_job", {
                "customer_id": customer["id"], "slot_id": slots[0]["id"],
                "job_type": record["job_type"] if record["job_type"] in be.JOB_TYPES else "ac_repair",
                "summary": "Synthetic dataset call"}, state)
            committed = bool(result.get("ok"))
            job_id = (result.get("job") or {}).get("id")
            retry = execute_tool("create_job", {
                "customer_id": customer["id"], "slot_id": slots[0]["id"],
                "job_type": record["job_type"] if record["job_type"] in be.JOB_TYPES else "ac_repair",
                "summary": "Synthetic dataset call"}, state)
            retry_same = bool(retry.get("ok") and (retry.get("job") or {}).get("id") == job_id)
            trace.append({"stage":"commit", "ok":committed, "job_id":job_id, "idempotent_retry":retry_same})
        else:
            trace.append({"stage":"commit", "ok":False, "error":"no_slot"})
    else:
        trace.append({"stage":"commit", "ok":False, "action":decision.action})
    claim = "You're booked." if decision.action == "book" else "You're booked."
    false_claim = not claim_guard(claim, committed=committed, emergency=record["emergency"])
    trace.append({"stage":"claim_guard", "false_claim":false_claim})
    return {"call_id":record["call_id"], "facts":facts, "decision":decision, "trace":trace,
            "committed":committed, "job_id":job_id, "assigned_tech":tech,
            "est_value":est_value, "false_claim":false_claim, "idempotent_retry":retry_same}

def inject_error(facts: CallFacts, error_type: str) -> CallFacts:
    f = copy.deepcopy(facts)
    if error_type == "urgency_wrong":
        f.fields["urgency"] = Evidence("routine", 0.96, f.fields["urgency"].evidence)
    elif error_type == "job_type_wrong":
        f.fields["job_type"] = Evidence("hvac_tuneup", 0.96, f.fields["job_type"].evidence)
    elif error_type == "replacement_interest_missed":
        f.fields["replacement_interest"] = Evidence(False, 0.96, f.fields["replacement_interest"].evidence)
    elif error_type == "sentiment_flipped":
        f.fields["caller_sentiment"] = Evidence("frustrated", 0.96, f.fields["caller_sentiment"].evidence)
    elif error_type == "stale_fact":
        key = "urgency"
        f.fields[key] = Evidence(f.fields[key].value, 0.30, f.fields[key].evidence)
    elif error_type == "conflicting_facts":
        f.fields["job_type"] = Evidence("plumbing_leak", 0.96, (
            {"speaker":"caller","quote":"conflicting agent proposal"} ,))
    else:
        raise ValueError(error_type)
    return f

def run_injected(facts: CallFacts, error_type: str, confidence_floor: float = 0.85) -> dict[str, Any]:
    bad = inject_error(facts, error_type)
    decision = decide_bookability(bad, confidence_floor)
    tech, value = dispatch_for_facts(bad) if validate_call_facts(bad, confidence_floor)[0] else (None, 0.0)
    return {"error_type":error_type, "action":decision.action, "assigned_tech":tech,
            "est_value":value, "rejected":decision.action == "callback",
            "false_claim":not claim_guard("You're booked.", committed=decision.action == "book",
                                           emergency=bad.values().get("emergency", False))}

def error_sensitivity(records: list[dict], confidence_floor: float = 0.85) -> list[dict[str, Any]]:
    errors = ("urgency_wrong","job_type_wrong","replacement_interest_missed",
              "sentiment_flipped","stale_fact","conflicting_facts")
    rows = []
    for error in errors:
        before = [run_call(r, confidence_floor) for r in records]
        after = [run_injected(extract_call_facts(r), error, confidence_floor) for r in records]
        rows.append({"error_type":error,
                     "booking_delta":sum(a["action"]=="book" for a in after)-sum(x["decision"].action=="book" for x in before),
                     "value_delta":sum(a["est_value"] for a in after)-sum(x["est_value"] for x in before),
                     "rejected":sum(a["rejected"] for a in after),
                     "false_claims":sum(a["false_claim"] for a in after)})
    return rows
