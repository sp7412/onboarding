import { describe, expect, it } from "vitest";
import { componentsWithinTailBudget, serialLatency, tailHitProbability } from "./model";

describe("latency-tail model", () => {
  it("computes the chance that one of eight components is slow", () => {
    expect(tailHitProbability(8, 0.05)).toBeCloseTo(0.3366, 4);
  });

  it("handles zero components and zero tail rate", () => {
    expect(tailHitProbability(0, 0.05)).toBe(0);
    expect(tailHitProbability(20, 0)).toBe(0);
  });

  it("adds normal serial work and a slow-path penalty", () => {
    expect(serialLatency(4, 35, 180)).toBe(320);
    expect(serialLatency(4, 35, 180, 2)).toBe(500);
  });

  it("finds the largest safe component count", () => {
    expect(componentsWithinTailBudget(0.05, 0.2)).toBe(4);
    expect(componentsWithinTailBudget(0, 0.2)).toBe(Infinity);
    expect(componentsWithinTailBudget(1, 0.2)).toBe(0);
  });

  it("rejects invalid inputs", () => {
    expect(() => tailHitProbability(-1, 0.05)).toThrow();
    expect(() => tailHitProbability(2, 1.1)).toThrow();
    expect(() => serialLatency(2.5, 20, 100)).toThrow();
  });
});
