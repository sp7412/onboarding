import { describe, expect, it } from "vitest";
import { playback, playbackSummary, truncateAtWord } from "./model";

describe("heard-vs-generated model", () => {
  it("truncates only at a word boundary", () => {
    expect(truncateAtWord("Please hold while I check that for you", 5)).toBe("Please hold while I check");
  });

  it("keeps generated and heard text equal without interruption", () => {
    expect(playback("  One   complete answer. ", null)).toEqual({
      generated: "One complete answer.",
      heard: "One complete answer.",
      interrupted: false,
    });
  });

  it("separates generated text from what the caller heard after a barge-in", () => {
    const result = playback("Please hold while I check that for you", 4);
    expect(result.heard).toBe("Please hold while I");
    expect(result.generated).not.toBe(result.heard);
    expect(playbackSummary(result)).toContain("heard 4");
  });
});
