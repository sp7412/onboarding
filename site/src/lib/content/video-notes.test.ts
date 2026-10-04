import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { parseVideoNotes, videoId } from "./video-notes";
import { parseVideos } from "./videos";
import { ContentError } from "./errors";

const guide = readFileSync(resolve(__dirname, "../../../../docs/reading-guide.md"), "utf8");
const notes = readFileSync(resolve(__dirname, "../../../../docs/video-notes.md"), "utf8");
const videos = parseVideos(guide, "docs/reading-guide.md");

describe("parseVideoNotes", () => {
  const parsed = parseVideoNotes(notes, "docs/video-notes.md", videos);

  it("parses notes and matches every section to a Videos-page video", () => {
    expect(parsed.length).toBeGreaterThan(0);
    expect(parsed.every((note) => videos.some((video) => videoId(video.url) === note.id))).toBe(true);
  });

  it("limits takeaways and preserves the required metadata", () => {
    expect(parsed.every((note) => note.takeaways.length >= 3 && note.takeaways.length <= 5)).toBe(true);
    expect(parsed.every((note) => note.why.length > 0 && note.questions.length >= 1)).toBe(true);
  });

  it("extracts YouTube IDs", () => {
    expect(videoId("https://www.youtube.com/watch?v=XbrlOY4Z-Ow")).toBe("XbrlOY4Z-Ow");
    expect(videoId("https://www.youtube.com/playlist?list=abc")).toBeUndefined();
  });

  it("rejects unknown sections and malformed note metadata", () => {
    const base = notes.slice(0, notes.indexOf("\n## ", notes.indexOf("\n## ") + 1));
    expect(() => parseVideoNotes(`${base}\n## Unknown\n- Video: <https://www.youtube.com/watch?v=not-a-video> · 1 min · reading-guide item 5\n- **Takeaways:**\n  1. one\n- **Why it matters here:** Analysis: one\n- **Questions to discuss:**\n  1. one`, "fixture.md", videos)).toThrow(ContentError);
    expect(() => parseVideoNotes(base.replace("<https://www.youtube.com/watch?v=-OXiljTJxQU>", "missing"), "fixture.md", videos)).toThrow(/valid Video line/);
    const tooMany = base.replace("- **Why it matters here:**", "  5. five\n  6. six\n- **Why it matters here:**");
    expect(() => parseVideoNotes(tooMany, "fixture.md", videos)).toThrow(/no more than five takeaways/);
  });
});
