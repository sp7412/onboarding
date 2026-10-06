import { describe, expect, it } from "vitest";
import { bookingRate, denominator, percent, rateSummary } from "./model";

const calls = { allCalls: 100, bookableCalls: 60, bookedCalls: 42 };

describe("denominator model", () => {
  it("uses all calls or bookable calls without changing the numerator", () => {
    expect(denominator(calls, "all-calls")).toBe(100);
    expect(denominator(calls, "bookable")).toBe(60);
    expect(percent(calls, "all-calls")).toBe(42);
    expect(percent(calls, "bookable")).toBe(70);
  });

  it("returns zero for an empty denominator", () => {
    expect(bookingRate({ allCalls: 0, bookableCalls: 0, bookedCalls: 0 }, "bookable")).toBe(0);
  });

  it("rejects impossible call counts", () => {
    expect(() => denominator({ allCalls: 4, bookableCalls: 5, bookedCalls: 1 }, "bookable")).toThrow();
    expect(() => denominator({ allCalls: 4, bookableCalls: 2, bookedCalls: 3 }, "bookable")).toThrow();
  });

  it("produces a plain-language summary", () => {
    expect(rateSummary(calls, "bookable")).toBe("42 booked / 60 bookable calls = 70.0%");
  });
});
