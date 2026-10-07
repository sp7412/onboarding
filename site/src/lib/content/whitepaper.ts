import { expectCondition } from "./errors";

export interface WhitepaperChapter {
  /** Chapter number, e.g. "00", "07", "A", "B". */
  number: string;
  slug: string;
  title: string;
  readingTime: string | undefined;
  /** True for the essentials path 00 → 01 → 02 → 06 → 07 → 10 → 11 → 14. */
  essentials: boolean;
  /** H2 "Five Takeaways" list items when present. */
  takeaways: string[];
  /** Section headings for in-page navigation. */
  sections: string[];
  body: string;
}

const ESSENTIALS = new Set(["00", "01", "02", "06", "07", "10", "11", "14"]);

export function parseWhitepaperChapter(filename: string, markdown: string): WhitepaperChapter {
  const file = `docs/whitepaper/${filename}`;
  const base = filename.replace(/\.md$/, "");
  const number = base.match(/^(\d{2}|appendix-[ab])/)?.[1]
    ?? base.match(/^(appendix-[ab])/)?.[1]
    ?? base.slice(0, 2);
  const slug = base.replace(/^(\d{2}-|appendix-[ab]-?)/, "");

  const lines = markdown.split("\n");
  const h1 = lines.find((l) => l.startsWith("# "));
  expectCondition(file, "an H1 title", Boolean(h1));
  const title = h1!.slice(2).replace(/^\d+\s*-\s*/, "").trim();

  const timeLine = lines.find((l) => /\*\*Estimated reading time:\*\*/.test(l));
  const readingTime = timeLine?.match(/\*\*Estimated reading time:\*\*\s*([^·]+)/)?.[1]?.trim();

  const takeaways: string[] = [];
  const sections: string[] = [];
  let inTakeaways = false;
  for (const line of lines) {
    if (line.startsWith("## ")) {
      const h2 = line.slice(3).trim();
      sections.push(h2);
      inTakeaways = /takeaway/i.test(h2);
      continue;
    }
    if (inTakeaways && /^[-\d]/.test(line.trim()) && line.trim() !== "") {
      takeaways.push(line.trim().replace(/^[-*]\s+|^\d+\.\s+/, ""));
    } else if (inTakeaways && line.trim() !== "") {
      // Any other non-empty line ends the list (blank lines inside it are fine).
      inTakeaways = false;
    }
  }

  const isAppendix = /^appendix-/.test(base);
  expectCondition(
    file,
    `chapter ${base} to declare an estimated reading time`,
    Boolean(readingTime) || isAppendix, // appendices are reference material without reading times
  );

  return {
    number,
    slug: base,
    title,
    readingTime,
    essentials: ESSENTIALS.has(number),
    takeaways,
    sections,
    body: markdown,
  };
}

export function parseWhitepaperOrder(readme: string, file: string): string[] {
  // Reading Order list: `1. [00 - Introduction](00-introduction.md)`
  const order = [...readme.matchAll(/^\d+\.\s+\[[^\]]+\]\(([^)]+\.md)\)/gm)].map((m) => m[1]);
  expectCondition(file, "unique whitepaper files", new Set(order).size === order.length);
  // Numbered chapters 00, 01, 02, … in order, followed by exactly appendix A then appendix B.
  const numbered = order.filter((f) => /^\d{2}-/.test(f));
  const expected = numbered.map((_, i) => String(i).padStart(2, "0"));
  expectCondition(file, "chapters numbered consecutively from 00 in reading order",
    numbered.length >= 15 && numbered.every((f, i) => f.startsWith(`${expected[i]}-`)), numbered.join(", "));
  expectCondition(file, "appendix A then appendix B after the chapters",
    order.slice(numbered.length).join(",") === "appendix-a-timeline.md,appendix-b-sources.md", order.slice(numbered.length).join(", "));
  return order;
}
