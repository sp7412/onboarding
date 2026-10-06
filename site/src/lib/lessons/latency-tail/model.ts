// Aha: Tail latency compounds across a serial request: eight components with a 5% slow-path rate give a 33.7% chance of at least one slow component (1 - 0.95^8).
function assertProbability(value: number): void {
  if (!Number.isFinite(value) || value < 0 || value > 1) throw new Error("probability must be between 0 and 1");
}

function assertCount(value: number): void {
  if (!Number.isInteger(value) || value < 0) throw new Error("component count must be a non-negative integer");
}

export function tailHitProbability(componentCount: number, perComponentTailRate: number): number {
  assertCount(componentCount);
  assertProbability(perComponentTailRate);
  return 1 - (1 - perComponentTailRate) ** componentCount;
}

export function serialLatency(componentCount: number, normalLatencyMs: number, tailPenaltyMs: number, slowComponents = 1): number {
  assertCount(componentCount);
  assertCount(slowComponents);
  if (!Number.isFinite(normalLatencyMs) || normalLatencyMs < 0 || !Number.isFinite(tailPenaltyMs) || tailPenaltyMs < 0) {
    throw new Error("latencies must be non-negative numbers");
  }
  return componentCount * normalLatencyMs + slowComponents * tailPenaltyMs;
}

export function componentsWithinTailBudget(perComponentTailRate: number, tailBudget: number): number {
  assertProbability(perComponentTailRate);
  assertProbability(tailBudget);
  if (perComponentTailRate === 0) return Number.POSITIVE_INFINITY;
  if (perComponentTailRate === 1) return 0;
  if (tailBudget === 0) return 0;
  return Math.floor(Math.log1p(-tailBudget) / Math.log1p(-perComponentTailRate));
}
