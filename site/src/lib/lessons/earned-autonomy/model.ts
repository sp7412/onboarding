/**
 * Earned autonomy: the Wilson score interval and lab 14's promote/hold/demote rule.
 * Mirrors labs/stlab/autonomy.py (wilson_interval and promotion_policy) so the lesson and
 * the lab give the same answers.
 */

export type Decision = "promote" | "hold" | "demote";

export interface Verdict {
  decision: Decision;
  lower: number;
  upper: number;
  reason: string;
}

/** 95% Wilson score interval for an error rate (errors out of n). */
export function wilsonInterval(errors: number, n: number, z = 1.96): [number, number] {
  if (!Number.isInteger(errors) || !Number.isInteger(n) || errors < 0 || n < 0 || errors > n) {
    throw new Error("errors and n must be integers with 0 <= errors <= n");
  }
  if (n === 0) return [0, 1];
  const p = errors / n;
  const denom = 1 + (z * z) / n;
  const centre = (p + (z * z) / (2 * n)) / denom;
  const half = (z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n))) / denom;
  return [Math.max(0, centre - half), Math.min(1, centre + half)];
}

/**
 * Lab 14's rule for one segment at one level:
 * demote when the lower bound is above the rate this level must keep beating;
 * hold below the minimum sample; promote when the upper bound is below the next target.
 *
 * The asymmetry is deliberate and matches labs/stlab/autonomy.py: the minimum sample gates
 * promotion, not demotion. Too little data never demotes (a wide interval keeps the lower
 * bound low), but clear evidence of harm demotes as soon as it appears, even in a small
 * sample. Losing autonomy should be faster than earning it. Parity with the Python policy is
 * tested against labs/data/autonomy-cases.json.
 */
export function judge(errors: number, n: number, promoteTarget: number, keepTarget: number,
                      minSamples = 200): Verdict {
  const [lower, upper] = wilsonInterval(errors, n);
  const pct = (x: number) => `${(x * 100).toFixed(1)}%`;
  if (n > 0 && lower > keepTarget) {
    return { decision: "demote", lower, upper, reason: `even the lower bound (${pct(lower)}) is worse than the ${pct(keepTarget)} this level requires` };
  }
  if (n < minSamples) {
    return { decision: "hold", lower, upper, reason: `${n} of ${minSamples} required calls` };
  }
  if (upper < promoteTarget) {
    return { decision: "promote", lower, upper, reason: `the upper bound (${pct(upper)}) is below the ${pct(promoteTarget)} target` };
  }
  if (lower >= promoteTarget) {
    return { decision: "hold", lower, upper, reason: `it is probably worse than the ${pct(promoteTarget)} target, but not provably worse than the ${pct(keepTarget)} this level requires` };
  }
  return { decision: "hold", lower, upper, reason: `the interval ${pct(lower)}–${pct(upper)} still straddles the ${pct(promoteTarget)} target` };
}

/** Smallest number of error-free calls whose upper bound falls below the target. */
export function errorFreeCallsNeeded(target: number, z = 1.96): number {
  if (!(target > 0 && target < 1)) throw new Error("target must be between 0 and 1");
  let n = 1;
  while (wilsonInterval(0, n, z)[1] >= target) n++;
  return n;
}
