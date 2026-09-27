"""A mock home-services backend: customers, technicians, schedule, jobs.

This is the "system of record" the agent talks to through tools. The point of
the tutorials is that *this layer* (plus the policy checks in `tools.py`)
enforces the rules, not the model's instructions.
"""
from __future__ import annotations

import copy
import datetime as dt
import time
import uuid

BASE_DATE = dt.date(2026, 10, 26)  # a Monday; keeps every run deterministic
SERVICE_ZIPS = {"76109", "76116", "76126", "76132", "76133"}
BUSINESS_HOURS = (8, 17)

JOB_TYPES = {
    "ac_repair":      {"skill": "hvac",     "hours": 2, "label": "AC repair"},
    "furnace_repair": {"skill": "hvac",     "hours": 2, "label": "Furnace repair"},
    "hvac_tuneup":    {"skill": "hvac",     "hours": 1, "label": "HVAC tune-up"},
    "water_heater":   {"skill": "plumbing", "hours": 2, "label": "Water heater service"},
    "leak_repair":    {"skill": "plumbing", "hours": 2, "label": "Leak repair"},
}

EMERGENCY_TERMS = ["gas smell", "smell gas", "smells like gas", "carbon monoxide", "co alarm",
                   "sparks", "smoke", "flooding", "burst pipe", "no heat and", "fire"]

_SEED_CUSTOMERS = {
    "+18175550101": {"id": "C-1001", "name": "Dana Whitfield", "zip": "76109",
                     "address": "4120 Bellaire Dr, Fort Worth, TX 76109",
                     "membership": "Comfort Club", "equipment": ["Heat pump, installed 2017"]},
    "+18175550142": {"id": "C-1002", "name": "Marcus Oyelaran", "zip": "76126",
                     "address": "9 Pecan Ridge Ct, Benbrook, TX 76126",
                     "membership": None, "equipment": ["Gas furnace, 2009", "50 gal water heater"]},
    "+18175550199": {"id": "C-1003", "name": "Priya Raman", "zip": "76244",
                     "address": "1200 Heritage Trace Pkwy, Keller, TX 76244",
                     "membership": None, "equipment": []},
}
_TECHS = [
    {"id": "T-01", "name": "Luis", "skills": {"hvac"}},
    {"id": "T-02", "name": "Kara", "skills": {"hvac", "plumbing"}},
    {"id": "T-03", "name": "Ben",  "skills": {"plumbing"}},
]
_WINDOWS = [(8, 10), (10, 12), (13, 15), (15, 17)]

# Simulated backend latency in milliseconds per operation (tweak in notebooks!)
LATENCY_MS = {"lookup_customer": 120, "find_slots": 450, "create_job": 300}

_state: dict = {}


def reset(seed_booked: bool = True) -> None:
    """Restore the backend to a known state."""
    slots = {}
    for d in range(5):
        day = BASE_DATE + dt.timedelta(days=d)
        for tech in _TECHS:
            for (a, b) in _WINDOWS:
                sid = f"S-{day:%m%d}-{tech['id']}-{a:02d}"
                slots[sid] = {"id": sid, "date": day.isoformat(), "weekday": day.strftime("%A"),
                              "start": f"{a:02d}:00", "end": f"{b:02d}:00", "tech_id": tech["id"],
                              "tech": tech["name"], "skills": sorted(tech["skills"]), "status": "open"}
    if seed_booked:  # make the schedule look lived-in
        for i, sid in enumerate(sorted(slots)):
            if i % 3 == 0:
                slots[sid]["status"] = "booked"
    _state.clear()
    _state.update(customers=copy.deepcopy(_SEED_CUSTOMERS), slots=slots, jobs={}, idem={}, log=[])


reset()


class PolicyError(Exception):
    """Raised when a request violates a business rule. `code` is machine-readable."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code, self.message = code, message

    def as_dict(self):
        return {"ok": False, "error": self.code, "message": self.message}


def _sleep(op: str):
    ms = LATENCY_MS.get(op, 0)
    if ms:
        time.sleep(ms / 1000)


def _audit(op, **kw):
    _state["log"].append({"ts": time.time(), "op": op, **kw})


# ---------------------------------------------------------------- operations
def lookup_customer(phone: str) -> dict | None:
    _sleep("lookup_customer")
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        digits = "1" + digits
    cust = _state["customers"].get("+" + digits)
    _audit("lookup_customer", phone=phone, found=bool(cust))
    return copy.deepcopy(cust) if cust else None


def in_service_area(zip_code: str) -> bool:
    return zip_code in SERVICE_ZIPS


def find_slots(job_type: str, zip_code: str, preferred_date: str | None = None, limit: int = 3) -> list[dict]:
    _sleep("find_slots")
    if job_type not in JOB_TYPES:
        raise PolicyError("unknown_job_type", f"Unknown job type '{job_type}'. Valid: {sorted(JOB_TYPES)}")
    if not in_service_area(zip_code):
        raise PolicyError("out_of_service_area", f"ZIP {zip_code} is outside the service area.")
    skill = JOB_TYPES[job_type]["skill"]
    out = [s for s in _state["slots"].values() if s["status"] == "open" and skill in s["skills"]]
    if preferred_date:
        pref = [s for s in out if s["date"] == preferred_date]
        out = pref or out
    out.sort(key=lambda s: (s["date"], s["start"]))
    _audit("find_slots", job_type=job_type, zip=zip_code, n=len(out))
    return [copy.deepcopy(s) for s in out[:limit]]


def create_job(customer_id: str, slot_id: str, job_type: str, summary: str,
               idempotency_key: str) -> dict:
    """Book a job. Idempotent on `idempotency_key` (retries return the same job)."""
    _sleep("create_job")
    if idempotency_key in _state["idem"]:
        job = _state["jobs"][_state["idem"][idempotency_key]]
        _audit("create_job", replay=True, job_id=job["id"])
        return {**copy.deepcopy(job), "replayed": True}
    slot = _state["slots"].get(slot_id)
    if slot is None:
        raise PolicyError("unknown_slot", f"No slot {slot_id}.")
    if slot["status"] != "open":
        raise PolicyError("slot_unavailable", f"Slot {slot_id} is no longer available.")
    if JOB_TYPES.get(job_type, {}).get("skill") not in slot["skills"]:
        raise PolicyError("skill_mismatch", f"{slot['tech']} can't do {job_type}.")
    slot["status"] = "booked"
    job = {"id": "J-" + uuid.uuid4().hex[:6].upper(), "customer_id": customer_id, "slot_id": slot_id,
           "job_type": job_type, "summary": summary, "date": slot["date"], "window": f"{slot['start']}-{slot['end']}",
           "tech": slot["tech"]}
    _state["jobs"][job["id"]] = job
    _state["idem"][idempotency_key] = job["id"]
    _audit("create_job", job_id=job["id"])
    return copy.deepcopy(job)


def detect_emergency(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in EMERGENCY_TERMS)


def jobs() -> list[dict]:
    return list(copy.deepcopy(_state["jobs"]).values())


def audit_log() -> list[dict]:
    return copy.deepcopy(_state["log"])
