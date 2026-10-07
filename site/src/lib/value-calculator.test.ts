import { describe, expect, it } from "vitest";
import { breakEvenFalseBookingRate, calculateValue, type ValueInputs } from "./value-calculator";

const base: ValueInputs = {
  monthlyCalls: 1000,
  afterHoursShare: 0.2,
  afterHoursAnswerRate: 0.75,
  agentBookingRate: 0.5,
  falseBookingRate: 0.02,
  completionRate: 0.8,
  averageTicket: 500,
  grossMargin: 0.5,
  wastedTruckRollCost: 300,
  agentCostPerCall: 2,
};

describe("calculateValue", () => {
  it("follows the funnel from missed calls to net value", () => {
    const r = calculateValue(base);
    expect(r.missedCalls).toBeCloseTo(50);          // 1000 × 0.2 × 0.25
    expect(r.agentBookings).toBeCloseTo(25);        // × 0.5
    expect(r.falseBookings).toBeCloseTo(0.5);       // × 0.02
    expect(r.completedJobs).toBeCloseTo(19.6);      // (25 − 0.5) × 0.8
    expect(r.addedRevenue).toBeCloseTo(9800);
    expect(r.addedGrossProfit).toBeCloseTo(4900);    // × 0.5 margin
    expect(r.wastedRollCost).toBeCloseTo(150);
    expect(r.agentCost).toBeCloseTo(100);
    expect(r.netValue).toBeCloseTo(4650);           // 4900 − 150 − 100
  });

  it("is zero when every after-hours call is already answered", () => {
    const r = calculateValue({ ...base, afterHoursAnswerRate: 1 });
    expect(r.missedCalls).toBe(0);
    expect(r.netValue).toBe(0);
  });

  it("clamps rates and ignores negative or non-numeric inputs", () => {
    const r = calculateValue({ ...base, monthlyCalls: -10, afterHoursShare: 2, averageTicket: Number.NaN });
    expect(r.missedCalls).toBe(0);
    expect(r.netValue).toBe(0);
    const clamped = calculateValue({ ...base, afterHoursShare: 2, afterHoursAnswerRate: -1 });
    expect(clamped.missedCalls).toBeCloseTo(1000);
  });

  it("loses money when false bookings exceed the break-even rate", () => {
    const be = breakEvenFalseBookingRate(base);   // 200 / (200 + 300)
    expect(be).toBeCloseTo(0.4);
    const noCost = { ...base, agentCostPerCall: 0 };
    expect(calculateValue({ ...noCost, falseBookingRate: be - 0.01 }).netValue).toBeGreaterThan(0);
    expect(calculateValue({ ...noCost, falseBookingRate: be + 0.01 }).netValue).toBeLessThan(0);
  });
});
