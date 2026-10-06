import { describe, expect, it } from "vitest";
import { calculateWorthIt, formatDollars } from "./model";

describe("worth-it model", () => {
  it("compares incremental job value with cost and expected error cost", () => {
    expect(calculateWorthIt({ costPerMinute: 0.2, callLengthMinutes: 5, bookingLift: 0.1, jobValue: 400, errorCost: 8 })).toEqual({
      callCost: 1,
      incrementalJobValue: 40,
      expectedErrorCost: 8,
      netValue: 31,
      isWorthIt: true,
    });
  });

  it("recognizes a negative unit economics case", () => {
    expect(calculateWorthIt({ costPerMinute: 1, callLengthMinutes: 10, bookingLift: 0.02, jobValue: 100, errorCost: 5 }).isWorthIt).toBe(false);
    expect(calculateWorthIt({ costPerMinute: 1, callLengthMinutes: 10, bookingLift: 0.02, jobValue: 100, errorCost: 5 }).netValue).toBe(-13);
  });

  it("formats illustrative dollar values", () => {
    expect(formatDollars(31)).toBe("$31.00");
  });

  it("rejects invalid inputs", () => {
    expect(() => calculateWorthIt({ costPerMinute: -1, callLengthMinutes: 5, bookingLift: 0.1, jobValue: 400, errorCost: 8 })).toThrow();
  });
});
