import { describe, expect, it } from "vitest";
import { alarmRates, positivePredictiveValue, thresholdMetrics, weightedAlarmCost } from "./model";

describe("rare-alarms model", () => {
  it("counts the four outcomes without rounding away the base rate", () => {
    expect(alarmRates(0.01, 0.9, 0.95, 1000)).toMatchObject({
      truePositives: 9,
      falseNegatives: expect.closeTo(1),
      falsePositives: expect.closeTo(49.5),
      trueNegatives: expect.closeTo(940.5),
    });
  });

  it("computes the chance that a positive alarm is real", () => {
    expect(positivePredictiveValue(0.01, 0.9, 0.95)).toBeCloseTo(9 / 58.5);
  });

  it("moves sensitivity down and specificity up as the threshold rises", () => {
    expect(thresholdMetrics(0)).toEqual({ sensitivity: 1, specificity: 0.5 });
    expect(thresholdMetrics(1)).toEqual({ sensitivity: 0.55, specificity: 0.99 });
  });

  it("makes false alarms and missed events carry different costs", () => {
    expect(weightedAlarmCost(0.01, 0.9, 0.95, 2, 20)).toBeCloseTo(119);
  });
});
