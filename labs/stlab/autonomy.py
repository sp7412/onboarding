"""Statistical policy for earning autonomy in a deterministic teaching environment."""
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
LEVEL_TARGETS = (0.20, 0.10, 0.05, 0.02, 0.01)

@dataclass(frozen=True)
class PromotionDecision:
    level: int
    decision: str
    upper_bound: float
    n: int
    reason: str

def wilson_upper(errors: int, n: int, z: float = 1.96) -> float:
    if n <= 0:
        return 1.0
    p = errors / n
    denom = 1 + z*z/n
    center = p + z*z/(2*n)
    spread = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return (center + spread) / denom

def wilson_interval(errors: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return 0.0, 1.0
    p = errors/n; denom=1+z*z/n
    center=p+z*z/(2*n); spread=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (center-spread)/denom, (center+spread)/denom

def promotion_policy(errors: int, n: int, current_level: int,
                     min_samples: int = 200) -> PromotionDecision:
    target = LEVEL_TARGETS[min(current_level, len(LEVEL_TARGETS)-1)]
    upper = wilson_upper(errors, n)
    if n < min_samples:
        return PromotionDecision(current_level, "hold", upper, n, "minimum sample size not reached")
    if upper < target and current_level < len(AUTONOMY_LEVELS)-1:
        return PromotionDecision(current_level+1, "promote", upper, n,
                                  f"Wilson upper bound {upper:.3f} < target {target:.3f}")
    if upper >= target * 1.5 and current_level > 0:
        return PromotionDecision(current_level-1, "demote", upper, n,
                                  f"error bound materially exceeds target {target:.3f}")
    return PromotionDecision(current_level, "hold", upper, n, f"upper bound {upper:.3f} does not clear target")

def sprt(errors: int, n: int, p0: float = 0.02, p1: float = 0.05,
         alpha: float = 0.05, beta: float = 0.10) -> str:
    """Sequential test of acceptable error p0 against unacceptable p1."""
    if n <= 0: return "continue"
    llr = errors*math.log(p1/p0) + (n-errors)*math.log((1-p1)/(1-p0))
    upper = math.log((1-beta)/alpha)
    lower = math.log(beta/(1-alpha))
    if llr >= upper: return "demote"
    if llr <= lower: return "promote"
    return "continue"

def cost_threshold(wrong_book_cost: float, missed_book_cost: float) -> float:
    """Minimum P(bookable) for taking the booking action."""
    if wrong_book_cost < 0 or missed_book_cost < 0 or wrong_book_cost + missed_book_cost == 0:
        raise ValueError("costs must be non-negative and not both zero")
    return wrong_book_cost / (wrong_book_cost + missed_book_cost)

def expected_cost(p_bookable: float, wrong_book_cost: float, missed_book_cost: float) -> tuple[float,float]:
    return ((1-p_bookable)*wrong_book_cost, p_bookable*missed_book_cost)

def calibration(probs: list[float], outcomes: list[int], bins: int = 10) -> tuple[list[tuple[float,float,int]], float]:
    if len(probs) != len(outcomes) or not probs: raise ValueError("probabilities and outcomes must match")
    edges=np.linspace(0,1,bins+1); rows=[]; total=len(probs); ece=0.0
    for lo,hi in zip(edges[:-1],edges[1:]):
        idx=[i for i,p in enumerate(probs) if lo <= p < hi or (hi == 1 and p <= hi)]
        if not idx: continue
        avg=sum(probs[i] for i in idx)/len(idx); rate=sum(outcomes[i] for i in idx)/len(idx)
        rows.append((avg,rate,len(idx))); ece += len(idx)/total*abs(avg-rate)
    return rows,ece

def psi(expected: list[float], actual: list[float], eps: float = 1e-6) -> float:
    e=np.asarray(expected,dtype=float); a=np.asarray(actual,dtype=float)
    e=np.clip(e,eps,None); a=np.clip(a,eps,None)
    return float(np.sum((a-e)*np.log(a/e)))

def mahalanobis_scores(train: np.ndarray, points: np.ndarray) -> np.ndarray:
    mean=train.mean(axis=0); cov=np.cov(train,rowvar=False)
    inv=np.linalg.pinv(cov + np.eye(cov.shape[0])*1e-6)
    d=points-mean
    return np.sqrt(np.einsum("ij,jk,ik->i",d,inv,d))

def drift_guard(expected_mix: list[float], observed_mix: list[float],
                features_train: np.ndarray, features_current: np.ndarray,
                psi_limit: float = 0.25, mahalanobis_limit: float = 3.5) -> dict:
    p=psi(expected_mix, observed_mix)
    scores=mahalanobis_scores(features_train, features_current)
    ood=bool(np.max(scores, initial=0.0) > mahalanobis_limit)
    return {"psi":p,"max_mahalanobis":float(np.max(scores,initial=0.0)),
            "pause":p > psi_limit or ood,"reason":"distribution shift" if p > psi_limit or ood else "stable"}

def segment_levels(segment_results: dict[str, tuple[int,int]], levels: dict[str,int] | None = None) -> dict[str, PromotionDecision]:
    levels = {} if levels is None else levels
    return {name: promotion_policy(errors,n,levels.get(name,0)) for name,(errors,n) in segment_results.items()}

def simpsons_paradox() -> dict[str, dict[str,float]]:
    """A small constructed example: aggregate accuracy rises while a key segment falls."""
    return {
        "old": {"easy": 0.99, "hard": 0.80, "aggregate": 0.95},
        "new": {"easy": 0.995, "hard": 0.75, "aggregate": 0.965},
    }
