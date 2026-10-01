import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { parseVideos, topicOf, minutesOf } from "./videos";

const guide = readFileSync(resolve(__dirname, "../../../../docs/reading-guide.md"), "utf8");

describe("parseVideos", () => {
  const videos = parseVideos(guide, "docs/reading-guide.md");
  it("finds every YouTube link in the reading guide", () => {
    const expected = new Set(guide.match(/https:\/\/(?:www\.)?youtube\.com\/(?:watch\?v=[\w-]{11}|playlist\?list=[\w-]+)/g));
    expect(new Set(videos.map((v) => v.url))).toEqual(expected);
  });
  it("marks optional LangSmith videos as not must-watch and cleans their titles", () => {
    const studio = videos.find((v) => v.url.endsWith("NJXu-4nDo50"))!;
    expect(studio.mustWatch).toBe(false);
    expect(studio.title).toBe("Getting Started with LangSmith (3/8): Debugging with Studio");
    expect(videos.find((v) => v.url.endsWith("fA9b4D8IsPQ"))!.mustWatch).toBe(true);
  });
  it("assigns topics and parses minutes", () => {
    expect(topicOf("14A")).toBe("langsmith");
    expect(topicOf("27")).toBe("background");
    expect(minutesOf("9 min")).toBe(9);
    expect(minutesOf("2–4 h (sample first)")).toBeNull();
  });
});
