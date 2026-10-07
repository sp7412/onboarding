"""Lab 14: statistical policy for earning (and losing) autonomy, one segment at a time.

Teaching code. The five level names are original labels inspired by public Pantheon 2026
descriptions of graduated AI maturity; they are not ServiceTitan's internal names or policy.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

AUTONOMY_LEVELS = (
    "suggest only",
    "act with human approval",
    "act and notify",
    "act autonomously within limits",
    "fully autonomous",
)
# LEVEL_TARGETS[i] is the error rate an agent must beat (with confidence) to move from level i
# to level i+1, and the rate it must keep beating to stay at level i+1.
LEVEL_TARGETS = (0.20, 0.10, 0.05, 0.02, 0.01)


@dataclass(frozen=True)
class PromotionDecision:
    level: int
    decision: str          # promote | hold | demote
    lower_bound: float
    upper_bound: float
    n: int
    reason: str


def wilson_interval(errors: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial error rate (95% by default)."""
    if n <= 0:
        return 0.0, 1.0
    p = errors / n
    denom = 1 + z * z / n
    center = p + z * z / (2 * n)
    spread = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (center - spread) / denom), min(1.0, (center + spread) / denom)


def wilson_upper(errors: int, n: int, z: float = 1.96) -> float:
    return wilson_interval(errors, n, z)[1]


def promotion_policy(errors: int, n: int, current_level: int,
                     min_samples: int = 200) -> PromotionDecision:
    """Promote, hold or demote one level, from evidence gathered *at the current level*.

    - Promote when the upper bound on the error rate is below the next level's target.
    - Demote when the lower bound is above the target this level was earned against, i.e.
      when there is evidence the agent is worse than required, not merely too little data.
    - Otherwise hold and keep collecting evidence.
    """
    lo, hi = wilson_interval(errors, n)
    top = len(AUTONOMY_LEVELS) - 1
    if current_level > 0 and n > 0 and lo > LEVEL_TARGETS[current_level - 1]:
        return PromotionDecision(current_level - 1, "demote", lo, hi, n,
                                 f"lower bound {lo:.3f} > {LEVEL_TARGETS[current_level - 1]:.3f} "
                                 "required at this level")
    if n < min_samples:
        return PromotionDecision(current_level, "hold", lo, hi, n,
                                 f"{n} of {min_samples} required samples")
    if current_level < top and hi < LEVEL_TARGETS[current_level]:
        return PromotionDecision(current_level + 1, "promote", lo, hi, n,
                                 f"upper bound {hi:.3f} < target {LEVEL_TARGETS[current_level]:.3f}")
    return PromotionDecision(current_level, "hold", lo, hi, n,
                             f"bounds [{lo:.3f}, {hi:.3f}] don't settle it yet")


def sprt(errors: int, n: int, p0: float = 0.02, p1: float = 0.05,
         alpha: float = 0.05, beta: float = 0.10) -> str:
    """Wald's sequential probability ratio test of H0: rate = p0 (acceptable) vs H1: rate = p1.

    Returns "promote" (accept H0), "demote" (accept H1) or "continue". alpha is the chance of
    promoting an agent whose true rate is p1; beta the chance of demoting one at p0.
    """
    if n <= 0:
        return "continue"
    llr = errors * math.log(p1 / p0) + (n - errors) * math.log((1 - p1) / (1 - p0))
    if llr >= math.log((1 - beta) / alpha):
        return "demote"
    if llr <= math.log(beta / (1 - alpha)):
        return "promote"
    return "continue"


def sprt_stopping_n(stream: list[int], **kwargs: float) -> tuple[str, int]:
    """Run SPRT over a 0/1 error stream; return the decision and how many samples it took."""
    errors = 0
    for i, e in enumerate(stream, 1):
        errors += e
        decision = sprt(errors, i, **kwargs)
        if decision != "continue":
            return decision, i
    return "continue", len(stream)


def cost_threshold(wrong_book_cost: float, missed_book_cost: float) -> float:
    """Minimum P(bookable) at which booking has lower expected cost than not booking."""
    if wrong_book_cost < 0 or missed_book_cost < 0 or wrong_book_cost + missed_book_cost == 0:
        raise ValueError("costs must be non-negative and not both zero")
    return wrong_book_cost / (wrong_book_cost + missed_book_cost)


def expected_cost(p_bookable: float, wrong_book_cost: float,
                  missed_book_cost: float) -> tuple[float, float]:
    """(expected cost of booking, expected cost of not booking)."""
    return (1 - p_bookable) * wrong_book_cost, p_bookable * missed_book_cost


def calibration(probs: list[float], outcomes: list[int],
                bins: int = 10) -> tuple[list[tuple[float, float, int]], float]:
    """Reliability-diagram rows (mean confidence, observed rate, n) and expected calibration error."""
    if len(probs) != len(outcomes) or not probs:
        raise ValueError("probabilities and outcomes must be non-empty and the same length")
    p = np.clip(np.asarray(probs, dtype=float), 0.0, 1.0)
    y = np.asarray(outcomes, dtype=float)
    idx = np.minimum((p * bins).astype(int), bins - 1)       # p == 1.0 goes in the last bin
    rows, ece = [], 0.0
    for b in range(bins):
        mask = idx == b
        k = int(mask.sum())
        if k == 0:
            continue
        conf, rate = float(p[mask].mean()), float(y[mask].mean())
        rows.append((conf, rate, k))
        ece += k / len(p) * abs(conf - rate)
    return rows, ece


def psi(expected: list[float], actual: list[float], eps: float = 1e-6) -> float:
    """Population stability index between two category mixes (rule of thumb: >0.25 is a big shift)."""
    e = np.clip(np.asarray(expected, dtype=float), eps, None)
    a = np.clip(np.asarray(actual, dtype=float), eps, None)
    e, a = e / e.sum(), a / a.sum()
    return float(np.sum((a - e) * np.log(a / e)))


def mahalanobis_scores(train: np.ndarray, points: np.ndarray) -> np.ndarray:
    mean = train.mean(axis=0)
    cov = np.cov(train, rowvar=False)
    inv = np.linalg.pinv(cov + np.eye(cov.shape[0]) * 1e-6)
    d = points - mean
    return np.sqrt(np.einsum("ij,jk,ik->i", d, inv, d))


def drift_guard(expected_mix: list[float], observed_mix: list[float],
                features_train: np.ndarray, features_current: np.ndarray,
                psi_limit: float = 0.25, ood_quantile: float = 0.99,
                ood_rate_limit: float = 0.05) -> dict:
    """Pause autonomy when the traffic mix or the inputs move away from what was validated.

    The OOD check calibrates a distance threshold on the training data itself (its 99th
    percentile), then pauses only if clearly more current points exceed it than expected.
    A single extreme point never pauses the system; a shifted population does.
    """
    p = psi(expected_mix, observed_mix)
    threshold = float(np.quantile(mahalanobis_scores(features_train, features_train), ood_quantile))
    scores = mahalanobis_scores(features_train, features_current)
    ood_rate = float(np.mean(scores > threshold)) if len(scores) else 0.0
    shifted, ood = p > psi_limit, ood_rate > ood_rate_limit
    reason = "stable"
    if shifted or ood:
        reason = " and ".join(x for x, on in (("traffic mix shifted", shifted),
                                              ("inputs out of distribution", ood)) if on)
    return {"psi": round(p, 4), "ood_threshold": round(threshold, 3),
            "ood_rate": round(ood_rate, 3), "pause": shifted or ood, "reason": reason}


def segment_levels(segment_results: dict[str, tuple[int, int]],
                   levels: dict[str, int] | None = None,
                   min_samples: int = 200) -> dict[str, PromotionDecision]:
    levels = levels or {}
    return {name: promotion_policy(errors, n, levels.get(name, 0), min_samples)
            for name, (errors, n) in segment_results.items()}


def hidden_regression_example() -> dict[str, dict[str, float]]:
    """Aggregate accuracy rises while the hard segment gets worse, because the mix shifted
    toward easy calls. (Related to, but weaker than, Simpson's paradox, where *every* segment
    moves opposite to the aggregate.)"""
    old_mix, new_mix = {"easy": 0.75, "hard": 0.25}, {"easy": 0.90, "hard": 0.10}
    old = {"easy": 0.99, "hard": 0.83}
    new = {"easy": 0.99, "hard": 0.75}
    agg = lambda acc, mix: round(sum(acc[s] * mix[s] for s in mix), 4)   # noqa: E731
    return {"old": {**old, "share_hard": old_mix["hard"], "aggregate": agg(old, old_mix)},
            "new": {**new, "share_hard": new_mix["hard"], "aggregate": agg(new, new_mix)}}
