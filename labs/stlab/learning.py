"""Closing the loop: decisions, outcomes and recalibration (teaching model, lab 11).

Every decision is logged with the inputs the agent *actually had at the time* (a ledger
snapshot), the prediction it made and the action it took. When the job closes, the outcome
is attached. Assumptions (like how much a signal adds to a job's value) are then updated
from evidence, with shrinkage so a handful of jobs can't swing them wildly.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from statistics import mean


@dataclass
class DecisionRecord:
    decision_id: str
    job_id: str
    at: int
    inputs: dict
    prediction: float
    action: str
    outcome: float | None = None


@dataclass
class DecisionLog:
    records: dict[str, DecisionRecord] = field(default_factory=dict)

    def record(self, rec: DecisionRecord) -> None:
        if rec.decision_id in self.records:
            raise ValueError(f"duplicate decision id {rec.decision_id}")
        self.records[rec.decision_id] = rec

    def attach_outcome(self, job_id: str, actual_value: float) -> int:
        n = 0
        for r in self.records.values():
            if r.job_id == job_id:
                r.outcome = actual_value
                n += 1
        return n

    def closed(self) -> list[DecisionRecord]:
        return [r for r in self.records.values() if r.outcome is not None]


def mean_abs_error(records: list[DecisionRecord]) -> float:
    return mean(abs(r.prediction - r.outcome) for r in records) if records else 0.0


def fit_uplifts(records: list[DecisionRecord], signals: list[str]) -> dict[str, tuple[float, int]]:
    """Least-squares estimate of each signal's value, controlling for job type and the other signals.

    Comparing averages "with vs. without" a signal is biased when signals co-occur (a call with
    `system_down` may also mention a replacement). Fitting all effects together separates them.
    Returns {signal: (estimated uplift, number of records with the signal)}.
    """
    import numpy as np
    types = sorted({r.inputs.get("job_type", "?") for r in records})
    X, y = [], []
    for r in records:
        row = [1.0 if r.inputs.get("job_type", "?") == t else 0.0 for t in types]
        row += [1.0 if s in r.inputs.get("signals", []) else 0.0 for s in signals]
        X.append(row)
        y.append(r.outcome)
    coef, *_ = np.linalg.lstsq(np.array(X), np.array(y), rcond=None)
    return {s: (float(coef[len(types) + i]), sum(1 for r in records if s in r.inputs.get("signals", [])))
            for i, s in enumerate(signals)}


def observed_uplift(records: list[DecisionRecord], signal: str, signals: list[str] | None = None) -> tuple[float, int]:
    """Estimated value of one signal (see `fit_uplifts`)."""
    signals = signals or sorted({s for r in records for s in r.inputs.get("signals", [])} | {signal})
    return fit_uplifts(records, signals)[signal]


def shrink(prior: float, observed: float, n: int, k: float = 20.0) -> float:
    """Blend prior and evidence: with n observations the evidence gets weight n/(n+k)."""
    return (k * prior + n * observed) / (k + n)


def calibration_table(pairs: list[tuple[float, bool]], edges=(0.5, 0.7, 0.8, 0.9, 1.01)) -> list[dict]:
    """Reliability buckets: for facts the agent rated at confidence c, how often were they right?"""
    rows, lo = [], 0.0
    for hi in edges:
        bucket = [ok for c, ok in pairs if lo <= c < hi]
        if bucket:
            rows.append({"confidence": f"{lo:.1f}–{min(hi, 1.0):.1f}", "n": len(bucket),
                         "accuracy": round(sum(bucket) / len(bucket), 2)})
        lo = hi
    return rows


def synthetic_jobs(n: int = 400, seed: int = 11, true_uplift: dict[str, float] | None = None) -> list[dict]:
    """Deterministic fictional jobs. Signals have *true* effects that differ from the priors."""
    true_uplift = true_uplift or {"system_down": 120, "replacement_interest": 2600, "same_day_needed": 40}
    rng = random.Random(seed)
    base = {"ac_repair": 450, "no_cool_diagnostic": 400, "tune_up": 150}
    jobs = []
    for i in range(n):
        jt = rng.choice(list(base))
        sig = [s for s, p in (("system_down", 0.35), ("replacement_interest", 0.12), ("same_day_needed", 0.4))
               if rng.random() < p]
        actual = base[jt] + sum(true_uplift[s] for s in sig) + rng.gauss(0, 120)
        # the voice agent's extracted job type is right ~80% of the time; its confidence is optimistic
        conf = round(min(0.99, max(0.5, rng.gauss(0.88, 0.06))), 2)
        correct = rng.random() < (0.95 if conf >= 0.9 else 0.74 if conf >= 0.8 else 0.55)
        heard = jt if correct else rng.choice([t for t in base if t != jt])
        jobs.append({"job_id": f"J-{i:04d}", "job_type": jt, "heard_job_type": heard,
                     "confidence": conf, "signals": sig, "actual_value": max(0.0, round(actual, 2))})
    return jobs
