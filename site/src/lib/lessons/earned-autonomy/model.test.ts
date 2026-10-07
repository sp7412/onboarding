import { describe, expect, it } from "vitest";
import { errorFreeCallsNeeded, judge, wilsonInterval } from "./model";

describe("earned autonomy model", () => {
  it("matches the lab 14 Wilson values", () => {
    // Same numbers as senior-engineer/autonomy-promotion.md, computed with labs/stlab/autonomy.py.
    const [lo, hi] = wilsonInterval(30, 1200);
    expect(lo).toBeCloseTo(0.01757, 4);
    expect(hi).toBeCloseTo(0.03546, 4);
    expect(wilsonInterval(11, 140)[1]).toBeCloseTo(0.13522, 4);
    expect(wilsonInterval(0, 0)).toEqual([0, 1]);
  });

  it("promotes on the upper bound, holds on thin data, demotes on the lower bound", () => {
    expect(judge(30, 1200, 0.05, 0.10).decision).toBe("promote");
    expect(judge(9, 260, 0.05, 0.10).decision).toBe("hold");
    expect(judge(1, 90, 0.05, 0.10).reason).toContain("90 of 200");
    expect(judge(0, 48, 0.05, 0.10).decision).toBe("hold");
    expect(judge(40, 200, 0.05, 0.10).decision).toBe("demote");
    // Too little data is never a reason to demote.
    expect(judge(1, 5, 0.05, 0.10).decision).toBe("hold");
    // Interval wholly above the promotion target but not provably above the keep bar.
    const v = judge(100, 1000, 0.05, 0.10);
    expect(v.decision).toBe("hold");
    expect(v.reason).toContain("probably worse");
  });

  it("needs 73 clean calls before zero errors proves under 5%", () => {
    const n = errorFreeCallsNeeded(0.05);
    expect(wilsonInterval(0, n)[1]).toBeLessThan(0.05);
    expect(wilsonInterval(0, n - 1)[1]).toBeGreaterThanOrEqual(0.05);
    expect(n).toBe(73);
  });

  it("rejects impossible counts", () => {
    expect(() => wilsonInterval(5, 4)).toThrow();
    expect(() => wilsonInterval(-1, 4)).toThrow();
  });
});
