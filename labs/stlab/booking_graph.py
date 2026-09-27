"""The booking workflow from notebook 06 as an importable module (used by notebook 08).

A LangGraph StateGraph where the *process* is deterministic and only the
fuzzy parts (classifying the problem, parsing yes/no/which-slot) are
delegated to small functions you could swap for an LLM.
"""
from __future__ import annotations

import operator
import re
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from . import backend as be

JOB_WORDS = [("water heater", "water_heater"), ("hot water", "water_heater"), ("leak", "leak_repair"),
             ("tune", "hvac_tuneup"), ("maintenance", "hvac_tuneup"), ("furnace", "furnace_repair"),
             ("heat", "furnace_repair"), ("a/c", "ac_repair"), ("ac", "ac_repair"), ("air", "ac_repair"),
             ("cool", "ac_repair")]


class CallGraphState(TypedDict, total=False):
    caller_phone: str
    heard: Annotated[list[str], operator.add]     # every caller utterance, appended
    said: Annotated[list[str], operator.add]      # every agent prompt, appended
    customer: dict | None
    job_type: str | None
    triage_attempts: int
    emergency: bool
    slots: list[dict]
    chosen_slot: dict | None
    address_confirmed: bool
    job: dict | None
    outcome: str | None


def classify_problem(text: str) -> str | None:
    t = text.lower()
    return next((j for w, j in JOB_WORDS if re.search(rf"\b{re.escape(w)}", t)), None)


def parse_yes_no(text: str) -> bool | None:
    t = text.lower()
    if re.search(r"\b(no|nope|wrong|not)\b", t):
        return False
    if re.search(r"\b(yes|yeah|yep|correct|right|sure)\b", t):
        return True
    return None


def parse_choice(text: str, n: int) -> int | None:
    t = text.lower()
    for i, w in enumerate(["first", "second", "third"][:n]):
        if w in t:
            return i
    if parse_yes_no(t):
        return 0
    return None


def ask(prompt: str) -> str:
    """Pause the graph, surface `prompt` to the talker, and resume with the caller's words."""
    return interrupt({"say": prompt})


# ---------------------------------------------------------------- nodes
def identify(state: CallGraphState):
    cust = be.lookup_customer(state["caller_phone"])
    if cust:
        return {"customer": cust}
    heard = ask("I couldn't find your account from this number. What's the phone number on the account?")
    return {"heard": [heard], "customer": be.lookup_customer(heard)}


def triage(state: CallGraphState):
    name = state["customer"]["name"].split()[0] if state.get("customer") else "there"
    prompt = f"Thanks, {name}. What's going on with your system?"
    if state.get("triage_attempts"):
        prompt = "Sorry, is this about heating, cooling, a water heater, or a leak?"
    heard = ask(prompt)
    return {"heard": [heard], "said": [prompt], "job_type": classify_problem(heard),
            "emergency": be.detect_emergency(heard), "triage_attempts": state.get("triage_attempts", 0) + 1}


def route_after_triage(state: CallGraphState):
    if state.get("emergency"):
        return "escalate"
    if not state.get("customer"):
        return "escalate"
    if state.get("job_type"):
        return "find_slots"
    return "triage" if state["triage_attempts"] < 2 else "escalate"


def find_slots(state: CallGraphState):
    # Side effect lives in its OWN node, before any interrupt, so resuming doesn't repeat it.
    try:
        return {"slots": be.find_slots(state["job_type"], state["customer"]["zip"], limit=2)}
    except be.PolicyError as e:
        return {"slots": [], "outcome": f"policy:{e.code}"}


def choose_slot(state: CallGraphState):
    s = state["slots"]
    def fmt(x):
        hour = int(x["start"][:2])
        return f"{x['weekday']} at {hour % 12 or 12}{'am' if hour < 12 else 'pm'} with {x['tech']}"

    prompt = "I can do " + " or ".join(fmt(x) for x in s) + ". Which works?"
    heard = ask(prompt)
    idx = parse_choice(heard, len(s))
    return {"heard": [heard], "said": [prompt], "chosen_slot": s[idx] if idx is not None else None}


def confirm_address(state: CallGraphState):
    prompt = f"Great. Just to confirm, the service address is {state['customer']['address']}?"
    heard = ask(prompt)
    return {"heard": [heard], "said": [prompt], "address_confirmed": parse_yes_no(heard) is True}


def book(state: CallGraphState, config):
    key = f"{config['configurable']['thread_id']}:{state['chosen_slot']['id']}"
    c = state["chosen_slot"]
    try:
        job = be.create_job(state["customer"]["id"], c["id"], state["job_type"], state["heard"][-3][:80], key)
    except be.PolicyError as e:
        return {"outcome": f"policy:{e.code}"}
    msg = f"You're booked for {c['weekday']} {c['start']}–{c['end']} with {c['tech']}. Your job number is {job['id']}."
    return {"job": job, "outcome": "booked", "said": [msg]}


def escalate(state: CallGraphState):
    if state.get("emergency"):
        msg = "If you smell gas, leave the home now and call 911 from outside. Connecting you to our emergency line."
        return {"outcome": "emergency_transfer", "said": [msg]}
    return {"outcome": state.get("outcome") or "transfer", "said": ["Let me connect you with a team member."]}


def build(checkpointer=None):
    g = StateGraph(CallGraphState)
    for name, fn in [("identify", identify), ("triage", triage), ("find_slots", find_slots),
                     ("choose_slot", choose_slot), ("confirm_address", confirm_address), ("book", book),
                     ("escalate", escalate)]:
        g.add_node(name, fn)
    g.add_edge(START, "identify")
    g.add_edge("identify", "triage")
    g.add_conditional_edges("triage", route_after_triage, ["escalate", "find_slots", "triage"])
    g.add_conditional_edges("find_slots", lambda s: "choose_slot" if s.get("slots") else "escalate",
                            ["choose_slot", "escalate"])
    g.add_conditional_edges("choose_slot", lambda s: "confirm_address" if s.get("chosen_slot") else "escalate",
                            ["confirm_address", "escalate"])
    g.add_conditional_edges("confirm_address", lambda s: "book" if s.get("address_confirmed") else "escalate",
                            ["book", "escalate"])
    g.add_edge("book", END)
    g.add_edge("escalate", END)
    return g.compile(checkpointer=checkpointer or InMemorySaver())


def advance(graph, call_id: str, caller_phone: str | None = None, caller_said: str | None = None) -> dict:
    """One step of the workflow, shaped like a tool result for a realtime talker.

    Start with caller_phone; then call with caller_said each time the caller answers.
    Returns {"say": str, "done": bool, "outcome": str|None}.
    """
    cfg = {"configurable": {"thread_id": call_id}}
    inp = {"caller_phone": caller_phone} if caller_phone else Command(resume=caller_said)
    out = graph.invoke(inp, cfg)
    if "__interrupt__" in out:
        return {"say": out["__interrupt__"][0].value["say"], "done": False, "outcome": None}
    return {"say": (out.get("said") or [""])[-1], "done": True, "outcome": out.get("outcome"),
            "job": out.get("job")}
