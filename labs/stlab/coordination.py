"""Coordinating several agents on one dispatch board (teaching model, lab 10).

Independent agents each optimize their own metric. A coordinator adds four things:
shared judgment (one lead-scoring and one demand-forecast function everyone uses),
coordinated action (one agent can *request* another to act, under the receiver's rules),
arbitration (pick the proposal with the highest expected value net of cost) and hard
constraints the arbiter can never trade away (consent, emergencies, capacity).

All numbers are illustrative. This is a generic pattern, not any company's design.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

# ---------------------------------------------------------------- shared judgment
BASE_VALUE = {"tune_up": 150, "ac_repair": 450, "no_cool_diagnostic": 400, "replacement_estimate": 2500}
SIGNAL_UPLIFT = {"system_down": 300, "replacement_interest": 1800, "same_day_needed": 150}


def lead_score(job_type: str, signals: list[str], uplift: dict[str, float] | None = None) -> float:
    """Expected job value from job type plus signals. One function, used by every agent."""
    uplift = SIGNAL_UPLIFT if uplift is None else uplift
    return BASE_VALUE.get(job_type, 300) + sum(uplift.get(s, 0) for s in signals)


def demand_forecast(open_slots: int, expected_new_calls: int) -> int:
    """Positive = slots we expect to go unfilled; negative = more demand than capacity."""
    return open_slots - expected_new_calls


# ---------------------------------------------------------------- board
@dataclass
class Job:
    job_id: str
    customer: str
    job_type: str
    est_value: float
    signals: list[str] = field(default_factory=list)
    moved_count: int = 0


@dataclass
class Board:
    """Today's capacity: slot_id -> Job or None. Technicians have a skill level."""
    slots: dict[str, Job | None]
    techs: dict[str, str]                       # slot_id -> tech name
    tech_level: dict[str, str]                  # tech -> "senior" | "junior"
    tomorrow: list[Job] = field(default_factory=list)
    credits_issued: float = 0.0
    log: list[str] = field(default_factory=list)

    def open_slots(self) -> list[str]:
        return [s for s, j in self.slots.items() if j is None]

    def lowest_value_slot(self) -> str | None:
        booked = [(j.est_value, s) for s, j in self.slots.items() if j is not None]
        return min(booked)[1] if booked else None

    def booked_value(self) -> float:
        return sum(j.est_value for j in self.slots.values() if j is not None)


# ---------------------------------------------------------------- proposals and arbitration
@dataclass
class Proposal:
    agent: str
    action: str                     # "book_today", "move_job", "increase_ads", "book_tune_ups", "pull_forward"
    expected_value: float
    cost: float
    params: dict = field(default_factory=dict)
    needs_consent: bool = False
    reason: str = ""

    @property
    def net(self) -> float:
        return self.expected_value - self.cost


@dataclass
class Decision:
    proposal: Proposal
    accepted: bool
    reason: str


def arbitrate(proposals: list[Proposal], capacity: int,
              hard_rules: list[Callable[[Proposal], str | None]] | None = None) -> list[Decision]:
    """Accept proposals in order of net value until capacity is used.

    Hard rules run first and can veto a proposal outright (return a reason string); the
    arbiter never trades a hard rule for expected value. Proposals with net <= 0 are rejected.
    `capacity` counts slot-consuming proposals (params['slots'], default 1; 0 for spend-only).
    """
    decisions: list[Decision] = []
    remaining = capacity
    for p in sorted(proposals, key=lambda p: p.net, reverse=True):
        veto = next((r for r in (rule(p) for rule in (hard_rules or [])) if r), None)
        if veto:
            decisions.append(Decision(p, False, veto))
            continue
        if p.net <= 0:
            decisions.append(Decision(p, False, "net value not positive"))
            continue
        need = p.params.get("slots", 1)
        if need > remaining:
            decisions.append(Decision(p, False, "no capacity left"))
            continue
        remaining -= need
        decisions.append(Decision(p, True, f"net {p.net:.0f} within capacity"))
    return decisions


# ---------------------------------------------------------------- coordinated action
def request_move(board: Board, slot_id: str, consent: Callable[[Job, str], bool],
                 credit: float = 25.0, max_moves: int = 1) -> tuple[bool, str]:
    """Dispatch's rule for moving a booked job to tomorrow when another agent asks.

    The requester can't move jobs itself. Dispatch checks its own constraints: the customer
    must consent, nobody gets moved more than `max_moves` times, and a credit is issued.
    """
    job = board.slots.get(slot_id)
    if job is None:
        return False, "slot already free"
    if job.moved_count >= max_moves:
        return False, f"{job.customer} has already been moved"
    if not consent(job, f"Could we move your {job.job_type} to tomorrow with a ${credit:.0f} credit?"):
        return False, f"{job.customer} declined"
    job.moved_count += 1
    board.slots[slot_id] = None
    board.tomorrow.append(job)
    board.credits_issued += credit
    board.log.append(f"moved {job.job_id} ({job.customer}) to tomorrow with ${credit:.0f} credit")
    return True, "moved with consent"


def assign_tech(board: Board, slot_id: str, job: Job, senior_threshold: float = 1000) -> str:
    """Put the job in the slot; prefer a senior tech for high-value work by swapping slots."""
    board.slots[slot_id] = job
    tech = board.techs[slot_id]
    if job.est_value >= senior_threshold and board.tech_level[tech] != "senior":
        for other, t in board.techs.items():
            if board.tech_level[t] == "senior" and other != slot_id:
                board.slots[slot_id], board.slots[other] = board.slots[other], board.slots[slot_id]
                board.log.append(f"swapped {slot_id} and {other} so a senior tech takes {job.job_id}")
                return t
    return tech
