import { describe, expect, it } from "vitest";
import { EXPLAINERS, validateExplainers } from "./explainers";

describe("explainer series", () => {
  it("contains four ordered, unique episodes with release assets", () => {
    expect(EXPLAINERS).toHaveLength(4);
    expect(new Set(EXPLAINERS.map((item) => item.id)).size).toBe(4);
    expect(EXPLAINERS.every((item) => item.videoUrl.includes("/releases/download/explainer-series/"))).toBe(true);
    expect(EXPLAINERS.every((item) => item.posterUrl.startsWith("/media/explainers/"))).toBe(true);
  });

  it("validates captions, posters, audio, and questions", () => {
    expect(() => validateExplainers()).not.toThrow();
    expect(EXPLAINERS.every((item) => item.questions.length === 2)).toBe(true);
  });
});
