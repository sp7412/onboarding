import { describe, it, expect } from "vitest";
import { loadContent, repoLinkToRoute, DOC_PAGES } from "./repo";

const bundle = loadContent();

describe("real repo content", () => {
  it("parses every checklist stage with items", () => {
    const stages = bundle.checklist.stages.map((s) => s.stage);
    expect(stages).toEqual(["pre-start", "d30", "d60", "d90", "recurring"]);
    const pre = bundle.checklistItems.filter((i) => i.stage === "pre-start");
    expect(pre.length).toBeGreaterThanOrEqual(20);
    // Wrapped items joined: the primer/lifecycle item is a single item with two links.
    const primer = pre.find((i) => i.text.startsWith("Read the [domain primer]"));
    expect(primer?.links.length).toBe(2);
  });

  it("parses the full reading guide", () => {
    expect(bundle.reading.items.length).toBeGreaterThanOrEqual(20);
    const productPage = bundle.reading.items.find((i) => i.number === "1");
    expect(productPage?.url).toContain("servicetitan.com/features/pro/virtual-agent");
    expect(productPage?.lookFor).toHaveLength(4);
    // Doc-table rows parsed as tier-2 cards
    expect(bundle.reading.items.filter((i) => i.number === undefined).length).toBeGreaterThanOrEqual(10);
  });

  it("parses all 13 podcast episodes in listening order", () => {
    expect(bundle.podcasts.length).toBe(13);
    expect(bundle.podcasts.map((p) => p.episode)).toEqual([
      "1", "2", "10", "11", "3", "4", "12", "5", "13", "6", "7", "8", "9",
    ]);
    for (const p of bundle.podcasts) {
      expect(p.block).toContain("CUSTOMIZE PROMPT");
      expect(p.sources.length).toBeGreaterThan(0);
    }
  });

  it("parses the whitepaper in README order with essentials path", () => {
    expect(bundle.whitepaper.chapters[0].number).toBe("00");
    expect(bundle.whitepaper.chapters).toHaveLength(17);
    const essentials = bundle.whitepaper.chapters.filter((c) => c.essentials).map((c) => c.number);
    expect(essentials).toEqual(["00", "01", "02", "06", "07", "10", "11", "14"]);
  });

  it("parses the glossary", () => {
    expect(bundle.glossary.length).toBeGreaterThanOrEqual(50);
    expect(bundle.glossary.some((t) => t.term === "Barge-in")).toBe(true);
  });

  it("parses all nine labs with questions and exercises", () => {
    expect(bundle.labs.map((l) => l.number)).toEqual(["00", "01", "02", "03", "04", "05", "06", "07", "08"]);
    // labs/README.md table shape: 9 rows, numbers 00-08
    expect(bundle.labs.length).toBe(9);
    for (const lab of bundle.labs) {
      expect(lab.questions.length).toBeGreaterThanOrEqual(2);
      expect(lab.exercise).toBeTruthy();
    }
    expect(bundle.labs.find((l) => l.number === "03")?.title).toContain("Turn-taking");
  });

  it("parses doc pages and templates with titles", () => {
    expect(bundle.docs.length).toBe(DOC_PAGES.length);
    expect(bundle.docs.find((d) => d.slug === "voice-agent-architecture")?.title).toContain("Voice-Agent Architecture");
    expect(bundle.templates.length).toBe(6);
    expect(bundle.templates.every((t) => t.title.length > 3)).toBe(true);
  });

  it("produces unique stable ids across all checklist items", () => {
    const ids = bundle.checklistItems.map((i) => i.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe("repoLinkToRoute", () => {
  it("maps docs and whitepaper links to site routes", () => {
    expect(repoLinkToRoute("../docs/servicetitan-101.md")).toBe("/docs/servicetitan-101");
    expect(repoLinkToRoute("../docs/whitepaper/01-company.md")).toBeNull();
    expect(repoLinkToRoute("../docs/reading-guide.md")).toBeNull();
    expect(repoLinkToRoute("../docs/podcast-prompts.md")).toBeNull();
    expect(repoLinkToRoute("../notes/study-question.md")).toBeNull();
    expect(repoLinkToRoute("../notes/glossary.md")).toBeNull();
    expect(repoLinkToRoute("../templates/design-doc.md")).toBeNull();
  });

  it("returns null for unmapped or external targets", () => {
    expect(repoLinkToRoute("https://example.com")).toBeNull();
    expect(repoLinkToRoute("../unknown/place.md")).toBeNull();
  });
});
