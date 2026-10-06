import { describe, expect, it } from "vitest";
import { erlangC } from "./model";

describe("Erlang C peak queue model", () => {
  it("matches the known c=5, offered-load=4 reference", () => {
    const result = erlangC(4, 60, 5);
    expect(result.utilization).toBeCloseTo(0.8, 10);
    expect(result.probabilityOfWaiting).toBeCloseTo(0.5541125541, 8);
    expect(result.expectedWaitMinutes).toBeCloseTo(33.24675325, 6);
  });

  it("shows that adding staff reduces waiting", () => {
    const four = erlangC(8, 30, 4);
    const five = erlangC(8, 30, 5);
    expect(five.probabilityOfWaiting).toBeLessThan(four.probabilityOfWaiting);
    expect(five.expectedWaitMinutes).toBeLessThan(four.expectedWaitMinutes);
  });

  it("marks an overloaded queue as unbounded", () => {
    expect(erlangC(10, 60, 5)).toEqual({
      utilization: 2,
      probabilityOfWaiting: 1,
      expectedWaitMinutes: Infinity,
    });
  });
});
