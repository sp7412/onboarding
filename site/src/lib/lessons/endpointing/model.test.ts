import { describe, expect, it } from "vitest";
import { endpoint, timerProgress } from "./model";

describe("endpointing model", () => {
  it("waits before the minimum silence timer", () => {
    expect(endpoint({ silenceMs: 300, minSilenceMs: 500, maxSilenceMs: 2000, context: "complete" })).toEqual({
      action: "wait", waitMs: 300, reason: "listening",
    });
  });

  it("commits a complete thought after the minimum timer", () => {
    expect(endpoint({ silenceMs: 700, minSilenceMs: 500, maxSilenceMs: 2000, context: "complete" }).action).toBe("commit");
  });

  it("keeps an unfinished thought open until the maximum timer", () => {
    expect(endpoint({ silenceMs: 700, minSilenceMs: 500, maxSilenceMs: 2000, context: "unfinished" })).toEqual({
      action: "wait", waitMs: 700, reason: "context",
    });
    expect(endpoint({ silenceMs: 2000, minSilenceMs: 500, maxSilenceMs: 2000, context: "unfinished" }).reason).toBe("maximum-silence");
  });

  it("clamps the timer visualization", () => {
    expect(timerProgress(750, 1500)).toBe(0.5);
    expect(timerProgress(2000, 1500)).toBe(1);
  });
});
