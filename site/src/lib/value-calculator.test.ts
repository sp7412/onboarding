import { describe, expect, it } from "vitest";
import { calculateValue } from "./value-calculator";

describe("calculateValue", () => {
  it("computes recovered after-hours jobs and net value", () => {
    const result = calculateValue({
      monthlyCalls: 1000,
      afterHoursShare: 0.2,
      currentAnswerRate: 0.75,
      agentBookingRate: 0.5,
      averageTicket: 500,
      closeRate: 0.8,
      falseBookingRate: 0.02,
      wastedTruckRollCost: 300,
    });
    expect(result.missedAfterHoursCalls).toBe(50);
    expect(result.addedBookedJobs).toBe(25);
    expect(result.addedRevenue).toBe(10000);
    expect(result.wastedRollCost).toBe(232.5);
    expect(result.netValue).toBe(9767.5);
  });

  it("clamps rates and prevents negative call inputs", () => {
    const result = calculateValue({
      monthlyCalls: -10,
      afterHoursShare: 2,
      currentAnswerRate: -1,
      agentBookingRate: 0.5,
      averageTicket: 500,
      closeRate: 1.5,
      falseBookingRate: 0.1,
      wastedTruckRollCost: 100,
    });
    expect(result.addedBookedJobs).toBe(0);
    expect(result.netValue).toBe(0);
  });
});
