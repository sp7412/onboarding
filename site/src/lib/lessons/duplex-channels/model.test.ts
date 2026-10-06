import { describe, expect, it } from "vitest";
import { channelResult, challengeMessage, modeSummary } from "./model";

describe("duplex channel model", () => {
  it("distinguishes turn-taking from simultaneous listening and speaking", () => {
    expect(modeSummary("turn-based")).toContain("take turns");
    expect(modeSummary("full-duplex")).toContain("listen while speaking");
  });

  it("keeps thinking quiet", () => {
    expect(channelResult("thinking", false)).toMatchObject({ accepted: true, spoken: false });
  });

  it("only allows verified commentary to be spoken", () => {
    expect(channelResult("commentary", false)).toMatchObject({ accepted: false, spoken: false });
    expect(channelResult("commentary", true)).toMatchObject({ accepted: true, spoken: true });
  });

  it("produces a useful accessible challenge result", () => {
    expect(challengeMessage("commentary", false)).toMatch(/^Blocked:/);
    expect(challengeMessage("commentary", true)).toMatch(/^Safe to say aloud:/);
  });
});
