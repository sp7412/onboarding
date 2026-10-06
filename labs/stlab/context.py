"""Shared context ledger for coordinated agents (teaching model, labs 09–12).

Agents never share raw transcripts or edit each other's notes. They write typed *facts*
with provenance to an append-only ledger, and read a "current view" filtered by trust
level. Status is the guardrail:

    proposed  -> written by an agent; not yet trusted
    verified  -> promoted by the control plane with evidence (caller confirmed, record match)
    committed -> the system of record changed (e.g. a job was booked)
    retracted -> withdrawn (wrong, superseded by the caller, or expired)

This is a generic pattern for multi-agent systems, not any company's internal design.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

STATUSES = ("proposed", "verified", "committed", "retracted")
RANK = {"retracted": -1, "proposed": 0, "verified": 1, "committed": 2}

# Which agent may propose which keys. The control plane may write anything.
DEFAULT_PERMISSIONS: dict[str, set[str]] = {
    "voice_agent": {"intent", "job_type", "urgency", "constraint", "caller_sentiment",
                    "callback_window", "equipment"},
    "text_agent": {"intent", "job_type", "urgency", "constraint", "callback_window"},
    "lead_scoring": {"est_value"},
    "demand_forecast": {"forecast_gap"},
    "dispatch": {"assigned_tech", "scheduled_slot"},
}
CONTROL_PLANE = "control_plane"


class ContextError(Exception):
    """A rejected ledger operation. `code` is stable and machine-readable."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True)
class Fact:
    job_id: str
    key: str
    value: Any
    status: str
    confidence: float
    source: str
    evidence: str | None
    version: int
    at: int                      # logical clock tick (deterministic for labs)
    expires_at: int | None = None


@dataclass
class ContextLedger:
    permissions: dict[str, set[str]] = field(default_factory=lambda: {k: set(v) for k, v in DEFAULT_PERMISSIONS.items()})
    _log: list[Fact] = field(default_factory=list)
    _subs: dict[str, list[Callable[[Fact], None]]] = field(default_factory=lambda: defaultdict(list))
    clock: int = 0

    # ---- internals -------------------------------------------------------------------
    def tick(self, n: int = 1) -> int:
        self.clock += n
        return self.clock

    def _latest(self, job_id: str, key: str) -> Fact | None:
        for f in reversed(self._log):
            if f.job_id == job_id and f.key == key:
                return f
        return None

    def version(self, job_id: str, key: str) -> int:
        f = self._latest(job_id, key)
        return f.version if f else 0

    def _append(self, fact: Fact) -> Fact:
        self._log.append(fact)
        for cb in list(self._subs.get(fact.key, [])) + list(self._subs.get("*", [])):
            cb(fact)
        return fact

    # ---- writes ------------------------------------------------------------------------
    def propose(self, agent: str, job_id: str, key: str, value: Any, confidence: float,
                evidence: str | None = None, expected_version: int | None = None,
                ttl: int | None = None) -> Fact:
        """Write a *proposed* fact. Agents can only propose keys they're allowed to."""
        if agent != CONTROL_PLANE and key not in self.permissions.get(agent, set()):
            raise ContextError("not_permitted", f"{agent} may not write {key!r}")
        if not 0.0 <= confidence <= 1.0:
            raise ContextError("bad_confidence", "confidence must be between 0 and 1")
        current = self.version(job_id, key)
        if expected_version is not None and expected_version != current:
            raise ContextError("version_conflict",
                               f"{job_id}/{key} is at version {current}, not {expected_version}")
        now = self.tick()
        return self._append(Fact(job_id, key, value, "proposed", confidence, agent, evidence,
                                 current + 1, now, now + ttl if ttl else None))

    def _promote(self, job_id: str, key: str, status: str, by: str, evidence: str | None) -> Fact:
        if by != CONTROL_PLANE:
            raise ContextError("not_permitted", f"only the control plane can mark facts {status}")
        latest = self._latest(job_id, key)
        if latest is None or latest.status == "retracted":
            raise ContextError("no_fact", f"nothing to {status} for {job_id}/{key}")
        if status == "verified" and not evidence:
            raise ContextError("no_evidence", "verification needs evidence")
        now = self.tick()
        return self._append(Fact(job_id, key, latest.value, status, latest.confidence,
                                 latest.source, evidence or latest.evidence, latest.version + 1,
                                 now, latest.expires_at))

    def verify(self, job_id: str, key: str, evidence: str, by: str = CONTROL_PLANE) -> Fact:
        return self._promote(job_id, key, "verified", by, evidence)

    def commit(self, job_id: str, key: str, by: str = CONTROL_PLANE, evidence: str | None = None) -> Fact:
        return self._promote(job_id, key, "committed", by, evidence)

    def retract(self, job_id: str, key: str, reason: str, by: str = CONTROL_PLANE) -> Fact:
        if by != CONTROL_PLANE:
            raise ContextError("not_permitted", "only the control plane can retract facts")
        latest = self._latest(job_id, key)
        if latest is None:
            raise ContextError("no_fact", f"nothing to retract for {job_id}/{key}")
        now = self.tick()
        return self._append(Fact(job_id, key, latest.value, "retracted", 0.0, by, reason,
                                 latest.version + 1, now))

    # ---- reads -------------------------------------------------------------------------
    def get(self, job_id: str, key: str, min_status: str = "verified",
            min_confidence: float = 0.0, as_of: int | None = None) -> Fact | None:
        """Latest fact for (job_id, key) at or above a trust level, ignoring expired facts.

        A retraction hides everything before it. `as_of` reads the ledger as it was at a
        past tick (used by the learning loop to avoid hindsight leakage).
        """
        now = self.clock if as_of is None else as_of
        for f in reversed(self._log):
            if f.job_id != job_id or f.key != key or f.at > now:
                continue
            if f.status == "retracted":
                return None
            if RANK[f.status] >= RANK[min_status] and f.confidence >= min_confidence:
                if f.expires_at is not None and f.expires_at <= now:
                    return None
                return f
        return None

    def view(self, job_id: str, min_status: str = "verified", min_confidence: float = 0.0,
             as_of: int | None = None) -> dict[str, Any]:
        keys = {f.key for f in self._log if f.job_id == job_id}
        out = {}
        for k in sorted(keys):
            f = self.get(job_id, k, min_status, min_confidence, as_of)
            if f is not None:
                out[k] = f.value
        return out

    def history(self, job_id: str, key: str | None = None) -> list[Fact]:
        return [f for f in self._log if f.job_id == job_id and (key is None or f.key == key)]

    def subscribe(self, key: str, callback: Callable[[Fact], None]) -> None:
        """Call `callback(fact)` whenever a fact with this key is written ('*' = all keys)."""
        self._subs[key].append(callback)


def context_tools(ledger: ContextLedger, agent: str) -> dict[str, Callable]:
    """The only way an agent touches shared context: two narrow tools bound to its identity."""
    def get_context(job_id: str, keys: list[str] | None = None, min_status: str = "verified") -> dict:
        v = ledger.view(job_id, min_status=min_status)
        return {k: v[k] for k in (keys or v) if k in v}

    def propose_fact(job_id: str, key: str, value: Any, confidence: float,
                     evidence: str | None = None) -> dict:
        try:
            f = ledger.propose(agent, job_id, key, value, confidence, evidence)
            return {"ok": True, "version": f.version}
        except ContextError as e:
            return {"ok": False, "error": e.code, "message": str(e)}

    return {"get_context": get_context, "propose_fact": propose_fact}
