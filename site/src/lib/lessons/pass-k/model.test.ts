import { describe, expect, it } from "vitest";
import { repeatedSuccess, trialOutcome } from "./model";

describe("pass-k model", () => {
  it("compounds eight 90% trials to about 43%", () => {
    expect(repeatedSuccess(.9, 8)).toBeCloseTo(.43046721, 8);
  });
  it("shows a full trajectory, not an average", () => {
    expect(trialOutcome(.9, 3, [.1, .2, .95])).toBe(false);
    expect(trialOutcome(.9, 3, [.1, .2, .3])).toBe(true);
  });
});
