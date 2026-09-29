import { contentId } from "./ids";
import { expectCondition } from "./errors";

export interface GlossaryTerm {
  id: string;
  term: string;
  meaning: string;
}

export function parseGlossary(markdown: string, file: string): GlossaryTerm[] {
  const terms: GlossaryTerm[] = [];
  let inTable = false;
  for (const raw of markdown.split("\n")) {
    const line = raw.trim();
    if (line.startsWith("| Term |")) {
      inTable = true;
      continue;
    }
    if (!inTable) continue;
    if (line.startsWith("|---")) continue;
    if (line.startsWith("|")) {
      const cells = line.split("|").slice(1, -1).map((c) => c.trim());
      expectCondition(file, "glossary row with exactly 2 cells", cells.length === 2, line);
      if (!cells[0] || !cells[1]) {
        expectCondition(file, "non-empty term and meaning", false, line);
      }
      terms.push({ id: contentId("glos", cells[0], cells.join(": ")), term: cells[0], meaning: cells[1] });
    }
  }
  // Row-shape validation only; corpus size expectations live in the repo
  // integration tests where the real glossary is parsed.
  return terms;
}
