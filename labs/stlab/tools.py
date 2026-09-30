"""The control-plane boundary: tool schemas + a guarded dispatcher.

The model *proposes* a tool call (name + JSON args). `execute_tool` decides
whether it is allowed, validates it, runs it, and returns a JSON-serialisable
result the model can talk about. This is where hard guardrails live.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from . import backend as be

TOOL_SCHEMAS = [
    {
        "type": "function", "name": "lookup_customer",
        "description": "Look up a customer by phone number. Returns name, address, membership, equipment.",
        "parameters": {"type": "object", "properties": {"phone": {"type": "string"}}, "required": ["phone"]},
    },
    {
        "type": "function", "name": "find_slots",
        "description": "Find open appointment windows for a job type in a ZIP code.",
        "parameters": {"type": "object", "properties": {
            "job_type": {"type": "string", "enum": sorted(be.JOB_TYPES)},
            "zip_code": {"type": "string"},
            "preferred_date": {"type": "string", "description": "YYYY-MM-DD, optional"}},
            "required": ["job_type", "zip_code"]},
    },
    {
        "type": "function", "name": "create_job",
        "description": "Book the job in a specific slot. Only call after the caller has confirmed the address and the slot out loud.",
        "parameters": {"type": "object", "properties": {
            "customer_id": {"type": "string"}, "slot_id": {"type": "string"},
            "job_type": {"type": "string", "enum": sorted(be.JOB_TYPES)},
            "summary": {"type": "string", "description": "One-line description of the problem"}},
            "required": ["customer_id", "slot_id", "job_type", "summary"]},
    },
    {
        "type": "function", "name": "record_slot_choice",
        "description": "Call when the caller picks one of the windows you offered. Pass that slot_id and quote their exact words.",
        "parameters": {"type": "object", "properties": {
            "slot_id": {"type": "string"}, "caller_said": {"type": "string"}},
            "required": ["slot_id", "caller_said"]},
    },
    {
        "type": "function", "name": "record_address_confirmation",
        "description": "Call when the caller explicitly confirms the service address you read back. Quote their exact words.",
        "parameters": {"type": "object", "properties": {"caller_said": {"type": "string"}}, "required": ["caller_said"]},
    },
    {
        "type": "function", "name": "get_appointments",
        "description": "List the verified caller's upcoming appointments. Call before rescheduling or cancelling.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function", "name": "reschedule_appointment",
        "description": "Move one of the caller's appointments to a slot you offered from find_slots.",
        "parameters": {"type": "object", "properties": {
            "appointment_id": {"type": "string"}, "new_slot_id": {"type": "string"}},
            "required": ["appointment_id", "new_slot_id"]},
    },
    {
        "type": "function", "name": "confirm_cancellation",
        "description": "Call when the caller explicitly confirms they want to cancel. Quote their exact words.",
        "parameters": {"type": "object", "properties": {"caller_said": {"type": "string"}}, "required": ["caller_said"]},
    },
    {
        "type": "function", "name": "cancel_appointment",
        "description": "Cancel one of the caller's appointments. Only after confirm_cancellation succeeded.",
        "parameters": {"type": "object", "properties": {
            "appointment_id": {"type": "string"}, "reason": {"type": "string"}},
            "required": ["appointment_id", "reason"]},
    },
    {
        "type": "function", "name": "transfer_to_human",
        "description": "Transfer the caller to a human customer service rep.",
        "parameters": {"type": "object", "properties": {"reason": {"type": "string"}}, "required": ["reason"]},
    },
]


@dataclass
class CallState:
    """State the *application* owns for one call (not the model!)."""
    call_id: str = "call-001"
    phase: str = "identify"            # identify -> diagnose -> schedule -> confirm -> done
    customer: dict | None = None
    offered_slot_ids: list[str] = field(default_factory=list)
    address_confirmed: bool = False
    slot_confirmed: bool = False
    chosen_slot_id: str | None = None  # the offered slot the caller actually picked
    emergency: bool = False
    transferred: bool = False
    booked_job: dict | None = None
    last_user_text: str = ""           # the app records what the caller actually said
    appointment_ids: list[str] = field(default_factory=list)   # appointments shown to THIS caller
    cancel_confirmed: bool = False
    changes: list[dict] = field(default_factory=list)          # every state change the backend confirmed
    tool_calls: list[dict] = field(default_factory=list)


def execute_tool(name: str, args: dict | str, state: CallState, *, enforce: bool = True) -> dict:
    """Run a tool call through the policy layer. Always returns a dict (never raises)."""
    if isinstance(args, str):
        try:
            args = json.loads(args or "{}")
        except json.JSONDecodeError:
            return {"ok": False, "error": "bad_arguments", "message": "Arguments were not valid JSON."}
    record = {"name": name, "args": args}
    state.tool_calls.append(record)
    try:
        result = _dispatch(name, args, state, enforce)
    except be.PolicyError as e:
        result = e.as_dict()
    except TypeError as e:  # missing/extra args
        result = {"ok": False, "error": "bad_arguments", "message": str(e)}
    record["result"] = result
    return result


def _dispatch(name, args, st: CallState, enforce: bool) -> dict:
    if st.emergency and enforce and name not in ("transfer_to_human",):
        raise be.PolicyError("emergency_escalation_required",
                             "Possible emergency: give safety instructions and transfer to a human now.")
    if name == "lookup_customer":
        cust = be.lookup_customer(**args)
        if cust:
            st.customer, st.phase = cust, "diagnose"
            return {"ok": True, "customer": cust}
        return {"ok": True, "customer": None, "message": "No customer on file for that number."}
    if name == "find_slots":
        if enforce and st.customer and args.get("zip_code") != st.customer["zip"]:
            # the model may hallucinate a ZIP; the record wins
            args = {**args, "zip_code": st.customer["zip"]}
        slots = be.find_slots(**args)
        st.offered_slot_ids = [s["id"] for s in slots]
        st.phase = "schedule"
        return {"ok": True, "slots": slots}
    if name == "create_job":
        if enforce:
            if not st.customer or args.get("customer_id") != st.customer["id"]:
                raise be.PolicyError("customer_not_verified", "Look up and verify the customer first.")
            if not st.address_confirmed:
                raise be.PolicyError("address_not_confirmed", "Read the service address back and get a yes first.")
            if args.get("slot_id") not in st.offered_slot_ids:
                raise be.PolicyError("slot_not_offered", "Only book a slot that was offered to the caller.")
            if not st.slot_confirmed or args.get("slot_id") != st.chosen_slot_id:
                raise be.PolicyError("slot_not_confirmed",
                                     "Record which offered window the caller chose before booking it.")
        key = f"{st.call_id}:{args.get('slot_id')}"  # idempotency key owned by the app
        job = be.create_job(idempotency_key=key, **args)
        st.booked_job, st.phase = job, "done"
        st.changes.append({"action": "booked", "id": job["id"]})
        return {"ok": True, "job": job}
    if name == "get_appointments":
        if not st.customer:
            raise be.PolicyError("customer_not_verified", "Look up and verify the customer first.")
        appts = be.get_appointments(st.customer["id"])   # identity from state, never from the model
        st.appointment_ids = [a["id"] for a in appts]
        return {"ok": True, "appointments": appts}
    if name == "reschedule_appointment":
        appt_id = args.get("appointment_id")
        if enforce:
            if appt_id not in st.appointment_ids:
                raise be.PolicyError("appointment_not_owned", "Only change appointments listed for this caller.")
            if args.get("new_slot_id") not in st.offered_slot_ids:
                raise be.PolicyError("slot_not_offered", "Only move to a slot that was offered to the caller.")
        key = f"{st.call_id}:reschedule:{appt_id}:{args.get('new_slot_id')}"
        appt = be.reschedule_appointment(appt_id, args.get("new_slot_id"), idempotency_key=key,
                                          customer_id=st.customer["id"])
        st.changes.append({"action": "rescheduled", "id": appt["id"]})
        st.phase = "done"
        return {"ok": True, "appointment": appt}
    if name == "confirm_cancellation":
        quote = (args.get("caller_said") or "").strip().lower()
        heard = st.last_user_text.lower()
        affirm = any(w in heard for w in ("yes", "yeah", "yep", "correct", "please cancel", "go ahead"))
        if enforce and (not quote or quote not in heard or not affirm):
            raise be.PolicyError("confirmation_not_grounded",
                                 "The caller's last utterance doesn't contain that confirmation.")
        st.cancel_confirmed = True
        return {"ok": True, "cancel_confirmed": True}
    if name == "cancel_appointment":
        appt_id = args.get("appointment_id")
        if enforce:
            if appt_id not in st.appointment_ids:
                raise be.PolicyError("appointment_not_owned", "Only cancel appointments listed for this caller.")
            if not st.cancel_confirmed:
                raise be.PolicyError("cancel_not_confirmed", "Get an explicit yes before cancelling.")
        key = f"{st.call_id}:cancel:{appt_id}"
        appt = be.cancel_appointment(appt_id, args.get("reason", ""), idempotency_key=key,
                                      customer_id=st.customer["id"])
        st.changes.append({"action": "cancelled", "id": appt["id"]})
        st.phase = "done"
        return {"ok": True, "appointment": appt}
    if name == "record_slot_choice":
        slot_id = args.get("slot_id")
        quote = (args.get("caller_said") or "").strip().lower()
        heard = st.last_user_text.lower()
        if enforce:
            if slot_id not in st.offered_slot_ids:
                raise be.PolicyError("slot_not_offered", "Only record a choice among the offered windows.")
            if not quote or quote not in heard:
                raise be.PolicyError("confirmation_not_grounded",
                                     "The caller's last utterance doesn't contain that choice.")
        st.slot_confirmed, st.chosen_slot_id = True, slot_id
        return {"ok": True, "slot_id": slot_id}
    if name == "record_address_confirmation":
        quote = (args.get("caller_said") or "").strip().lower()
        heard = st.last_user_text.lower()
        affirm = any(w in heard for w in ("yes", "yeah", "yep", "correct", "that's right", "right", "sure"))
        if enforce and (not quote or quote not in heard or not affirm):
            raise be.PolicyError("confirmation_not_grounded",
                                 "The caller's last utterance doesn't contain that confirmation.")
        st.address_confirmed = True
        return {"ok": True, "address_confirmed": True}
    if name == "transfer_to_human":
        st.transferred, st.phase = True, "done"
        return {"ok": True, "message": "Transferring to a CSR.", "reason": args.get("reason")}
    return {"ok": False, "error": "unknown_tool", "message": f"No tool named {name}."}
