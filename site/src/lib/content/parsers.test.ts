import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { parseChecklist, flattenChecklist } from "./checklist";
import { parseReadingGuide } from "./reading-guide";
import { parsePodcastPrompts } from "./podcasts";
import { parseWhitepaperChapter, parseWhitepaperOrder } from "./whitepaper";
import { parseGlossary } from "./glossary";
import { parseLabSource, parseLabsReadme, splitCells } from "./labs";
import { ContentError } from "./errors";

const fx = (name: string) => readFileSync(join(__dirname, "__fixtures__", name), "utf8");

describe("parseChecklist", () => {
  const doc = parseChecklist(fx("checklist-mini.md"), "checklist-mini.md");

  it("finds all five stages in order", () => {
    expect(doc.stages.map((s) => s.stage)).toEqual(["pre-start", "d30", "d60", "d90", "recurring"]);
  });

  it("joins wrapped checkbox lines into one item", () => {
    const first = doc.stages[0].weeks[0].items[0];
    expect(first.text).toBe(
      "Read the [domain primer](../docs/servicetitan-101.md) and [contractor lifecycle](../docs/how-a-contractor-works.md).",
    );
    expect(first.links.map((l) => l.target)).toEqual(["../docs/servicetitan-101.md", "../docs/how-a-contractor-works.md"]);
  });

  it("captures Output lines as week outcomes", () => {
    expect(doc.stages[0].weeks[1].output).toContain("hypothesis about where the control plane begins");
  });

  it("marks exit criteria and gives them stable slugs", () => {
    const exit = flattenChecklist(doc).filter((i) => i.isExitCriterion);
    expect(exit.length).toBe(2);
    expect(exit.map((i) => i.weekSlug)).toEqual(["exit-d30", "exit-d90"]);
  });

  it("captures watch-outs", () => {
    expect(doc.watchouts.length).toBe(2);
  });

  it("builds stable IDs from stage, week slug and text hash", () => {
    const items = flattenChecklist(doc);
    for (const item of items) {
      expect(item.id).toMatch(/^chk-(pre-start|d30|d60|d90|recurring)-[a-z0-9-]+-[0-9a-f]{8}$/);
    }
    const again = parseChecklist(fx("checklist-mini.md"), "checklist-mini.md");
    expect(flattenChecklist(again).map((i) => i.id)).toEqual(items.map((i) => i.id));
  });

  it("fails loudly when a stage loses all its items", () => {
    // Remove every pre-start item so the stage-level strictness trips.
    const broken = fx("checklist-mini.md")
      .replace(/- \[ \] Read the \[domain primer\][\s\S]*?items 1–4\.\n/, "");
    expect(() => parseChecklist(broken, "broken.md")).toThrow(ContentError);
  });
});

describe("parseReadingGuide", () => {
  const doc = parseReadingGuide(fx("reading-guide-mini.md"), "reading-guide-mini.md");

  it("assigns tiers from headings", () => {
    expect(doc.items.map((i) => i.tier)).toEqual([1, 1, 2, 2, 2, 3, 4]);
  });

  it("extracts numbered items with url, kind and time", () => {
    const first = doc.items[0];
    expect(first.number).toBe("1");
    expect(first.url).toBe("https://example.com/features/virtual-agent");
    expect(first.kind).toBe("product page");
    expect(first.time).toBe("15 min");
  });

  it("extracts exactly four look-for prompts and joins wrapped why text", () => {
    const first = doc.items[0];
    expect(first.lookFor.length).toBe(4);
    expect(first.why).toContain("were promised.");
  });

  it("parses the official-docs table rows as tier-2 cards", () => {
    const tableItems = doc.items.filter((i) => i.number === undefined);
    expect(tableItems.length).toBe(2);
    expect(tableItems[0].title).toBe("Realtime overview");
    expect(tableItems[0].pairsWith).toBe("Lab 01");
  });

  it("records the doc-table note", () => {
    expect(doc.docTableNote).toContain("official pages");
  });

  it("fails when a tier-1 item loses a look-for prompt", () => {
    const broken = fx("reading-guide-mini.md").replace("  4. Customers review recordings and metrics, so there's a quality loop.\n", "");
    expect(() => parseReadingGuide(broken, "broken.md")).toThrow(/four "look for" prompts/);
  });
});

describe("parsePodcastPrompts", () => {
  const episodes = parsePodcastPrompts(fx("podcasts-mini.md"), "podcasts-mini.md");

  it("keeps file order as listening order and captures numbers", () => {
    expect(episodes.map((e) => e.episode)).toEqual(["1", "2", "6"]);
  });

  it("captures the verbatim block with sources and prompt", () => {
    const e1 = episodes[0];
    expect(e1.block).toContain("EPISODE 1: THE BUSINESS");
    expect(e1.block).toContain("CUSTOMIZE PROMPT");
    expect(e1.sources).toEqual(["https://example.com/features/virtual-agent", "https://example.com/blog/webinar-recap"]);
  });

  it("captures the When line", () => {
    expect(episodes[0].when).toContain("Week of Sept 28");
  });

  it("builds stable ids", () => {
    for (const e of episodes) expect(e.id).toMatch(/^pod-episode-\d+-[0-9a-f]{8}$/);
  });

  it("fails when an episode block is missing", () => {
    const broken = fx("podcasts-mini.md").replace(/```text[\s\S]*?```/, "");
    expect(() => parsePodcastPrompts(broken, "broken.md")).toThrow(ContentError);
  });
});

describe("whitepaper parsing", () => {
  const orderDoc = `# Background Whitepaper

## Reading Order

1. [00 - Introduction](00-introduction.md)
2. [01 - Company](01-company.md)
3. [02 - The Trades Industry](02-the-trades-industry.md)
4. [03 - How A Contractor Works](03-how-a-contractor-works.md)
5. [04 - The Contact Center](04-the-contact-center.md)
6. [05 - Pain Points](05-pain-points.md)
7. [06 - Product Landscape](06-product-landscape.md)
8. [07 - AI Voice Agents](07-ai-voice-agents.md)
9. [08 - Technology Landscape](08-technology-landscape.md)
10. [09 - Competitive Landscape](09-competitive-landscape.md)
11. [10 - Regulation And Compliance](10-regulation-and-compliance.md)
12. [11 - Economics And Metrics](11-economics-and-metrics.md)
13. [12 - Risks And Failure Modes](12-risks-and-failure-modes.md)
14. [13 - Future Directions](13-future-directions.md)
15. [14 - Implications And Open Questions](14-implications-and-open-questions.md)
16. [Appendix A - Timeline](appendix-a-timeline.md)
17. [Appendix B - Sources](appendix-b-sources.md)
`;

  it("parses the reading order", () => {
    expect(parseWhitepaperOrder(orderDoc, "README")[0]).toBe("00-introduction.md");
    expect(parseWhitepaperOrder(orderDoc, "README")).toHaveLength(17);
  });

  it("rejects gaps in chapter numbering and misplaced appendices", () => {
    expect(() => parseWhitepaperOrder(orderDoc.replace("(04-the-contact-center.md)", "(05-dupe.md)"), "README")).toThrow(/consecutively/);
    const swapped = orderDoc.replace("16. [Appendix A - Timeline](appendix-a-timeline.md)\n17. [Appendix B - Sources](appendix-b-sources.md)",
      "16. [Appendix B - Sources](appendix-b-sources.md)\n17. [Appendix A - Timeline](appendix-a-timeline.md)");
    expect(() => parseWhitepaperOrder(swapped, "README")).toThrow(/appendix A then appendix B/);
  });

  it("parses a chapter with reading time, takeaways and essentials flag", () => {
    const ch = parseWhitepaperChapter("07-ai-voice-agents.md", fx("whitepaper-chapter.md"));
    expect(ch.number).toBe("07");
    expect(ch.title).toBe("AI Voice Agents");
    expect(ch.readingTime).toBe("7 minutes");
    expect(ch.essentials).toBe(true);
    expect(ch.takeaways).toHaveLength(5);
    expect(ch.sections).toContain("What the product does");
  });

  it("marks non-essentials chapters", () => {
    const ch = parseWhitepaperChapter("04-the-contact-center.md", fx("whitepaper-chapter.md"));
    expect(ch.essentials).toBe(false);
  });

  it("fails when reading time is missing", () => {
    const broken = fx("whitepaper-chapter.md").replace("**Estimated reading time:** 7 minutes · **Facts as of:** September 27, 2026\n", "");
    expect(() => parseWhitepaperChapter("07-x.md", broken)).toThrow(ContentError);
  });
});

describe("parseGlossary", () => {
  const doc = `# Glossary

| Term | Meaning |
|---|---|
| CSR | Customer service representative who answers calls |
| Endpointing | Deciding a caller's spoken turn is complete |
| VAD | Voice activity detection |
`;

  it("parses rows into term/meaning pairs", () => {
    const terms = parseGlossary(doc, "glossary.md");
    expect(terms.length).toBe(3);
    expect(terms[0]).toMatchObject({ term: "CSR", meaning: "Customer service representative who answers calls" });
  });

  it("fails on a malformed row", () => {
    const broken = doc.replace("| VAD | Voice activity detection |", "| VAD | only | one | extra |");
    expect(() => parseGlossary(broken, "broken.md")).toThrow(ContentError);
  });
});

describe("lab parsing", () => {
  const readmeRow = parseLabsReadme(
    [
      "| # | Notebook | Layer | Keys needed | Time |",
      "|---|---|---|---|---|",
      ...Array.from({ length: 9 }, (_, i) => `| ${String(i).padStart(2, "0")} | lab_${i} | layer | none | 30–60 minutes |`),
    ].join("\n"),
    "labs/README.md",
  );

  it("parses the readme table row", () => {
    expect(readmeRow).toHaveLength(9);
    expect(readmeRow[3]).toEqual({ number: "03", slug: "lab_3", layer: "layer", keys: "none", time: "30–60 minutes" });
  });

  it("accepts an optional trailing column such as an Open in Colab badge", () => {
    const rows = parseLabsReadme(
      Array.from({ length: 9 }, (_, i) => `| ${String(i).padStart(2, "0")} | lab_${i} | layer | none | 30–60 minutes | [![Open In Colab](https://e.com/b.svg)](https://e.com/${i}) |`).join("\n"),
      "labs/README.md",
    );
    expect(rows).toHaveLength(9);
    expect(rows[2].time).toBe("30–60 minutes");
  });

  it("rejects duplicate or incomplete lab tables", () => {
    expect(() => parseLabsReadme(`| 00 | x | layer | none | 30–60 minutes |\n| 00 | y | layer | none | 30–60 minutes |`, "broken.md")).toThrow(ContentError);
  });

  it("splits percent cells and strips the leading hashes from markdown", () => {
    const { markdown, code } = splitCells(fx("lab-mini.py"));
    expect(markdown.length).toBe(4);
    expect(code.length).toBe(3);
    expect(markdown[0]).toContain("# 03 · Turn-taking");
  });

  it("parses title, questions and graded exercise", () => {
    const lab = parseLabSource("03_turn_taking_and_interruptions.py", fx("lab-mini.py"), { keys: "none", time: "30–60 minutes" });
    expect(lab.number).toBe("03");
    expect(lab.title).toBe("Turn-taking: VAD, endpointing, and barge-in");
    expect(lab.questions).toHaveLength(2);
    expect(lab.exercise).toContain("sweep endpointing delays");
    expect(lab.time).toBe("30–60 minutes");
  });

  it("fails when the understanding section is missing", () => {
    const broken = fx("lab-mini.py").replace("## Check your understanding", "## Something else");
    expect(() => parseLabSource("03_x.py", broken, { keys: "none", time: "30" })).toThrow(ContentError);
  });
});
