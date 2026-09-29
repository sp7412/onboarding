import { contentId } from "./ids";
import { expectCondition, fail } from "./errors";

export type ReadingTier = 1 | 2 | 3 | 4;

export interface ReadingItem {
  id: string;
  /** Item number as printed (1, 2, … 11A, 26…), or undefined for table rows. */
  number: string | undefined;
  title: string;
  tier: ReadingTier;
  /** Primary link URL (first `- [ ] <url>` line). */
  url: string | undefined;
  /** Additional links (e.g. press release + keynote recap; doc-table rows). */
  extraLinks: { url: string; label?: string }[];
  kind: string; // product page / blog / talk / docs / paper / long-form guide …
  time: string; // "15 min", "45 min", "2–3 h (can be split)"
  why: string | undefined;
  /** The four "look for" reflection prompts. */
  lookFor: string[];
  pairsWith: string | undefined;
}

/** Draft shape while parsing an item; strictness is applied in flush(). */
type DraftItem = {
  -readonly [K in keyof ReadingItem]: ReadingItem[K] | (ReadingItem[K] extends string | undefined ? string : never);
};

export interface ReadingDoc {
  items: ReadingItem[];
  docTableNote: string | undefined;
}

const TIER_RE = /^## Tier (\d)/;

function splitMeta(meta: string): { kind: string; time: string } {
  // `· product page · 15 min` or `· talk · 20 min`
  const parts = meta.split("·").map((p) => p.trim()).filter(Boolean);
  const time = parts.length ? parts[parts.length - 1] : "";
  const kind = parts.slice(0, -1).join(" · ");
  return { kind, time };
}

export function parseReadingGuide(markdown: string, file: string): ReadingDoc {
  const lines = markdown.split("\n");
  const items: ReadingItem[] = [];
  let tier: ReadingTier | 0 = 0;
  let current: ReadingItem | undefined;
  let inLookFor = false;
  let inDocTable = false;
  let inDocTableNote = false;
  let docTableNote: string[] | undefined;

  const flush = () => {
    if (!current) return;
    const c = current;
    expectCondition(file, `item "${c.title}" to have a tier`, tier >= 1 && tier <= 4);
    expectCondition(file, `item "${c.title}" to have a time estimate`, Boolean(c.time));
    expectCondition(file, `item "${c.title}" to have at least one link`, Boolean(c.url || c.extraLinks.length));
    if (tier === 1 || tier === 2) {
      expectCondition(file, `tier ${tier} item "${c.title}" to have a "why"`, Boolean(c.why));
      expectCondition(
        file,
        `tier ${tier} item "${c.title}" to have four "look for" prompts (got ${c.lookFor.length})`,
        c.lookFor.length === 4,
      );
    }
    items.push({ ...c, tier: tier as ReadingTier });
    current = undefined;
    inLookFor = false;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    const tm = line.match(TIER_RE);
    if (tm) {
      flush();
      tier = Number(tm[1]) as ReadingTier;
      inDocTable = false;
      continue;
    }

    if (/^### Official documentation quick reference/.test(line)) {
      flush();
      inDocTable = true;
      docTableNote = [];
      inDocTableNote = true; // prose until the table starts is the note
      continue;
    }

    if (inDocTable && inDocTableNote) {
      if (line.trim() === "") continue;
      if (line.startsWith("|")) {
        inDocTableNote = false; // table begins; fall through to row handling next iteration
      } else {
        docTableNote!.push(line.trim());
        continue;
      }
    }

    if (inDocTable) {
      if (/^\| Read \|/.test(line)) continue; // header row
      if (/^\|---/.test(line)) continue; // separator
      if (line.startsWith("|")) {
        const cells = line.split("|").slice(1, -1).map((c) => c.trim());
        expectCondition(file, "doc-table row with 4 cells", cells.length === 4, line);
        const labelMatch = cells[0].match(/\[([^\]]+)\]\(([^)]+)\)/);
        expectCondition(file, `doc-table row to contain a link`, Boolean(labelMatch), line);
        items.push({
          id: contentId("read", labelMatch![1], cells.join(" ")),
          number: undefined,
          title: labelMatch![1],
          tier: tier === 0 ? 1 : tier,
          url: labelMatch![2],
          extraLinks: [],
          kind: "docs",
          time: cells[2],
          why: cells[1],
          lookFor: [],
          pairsWith: cells[3],
        });
      } else if (line.trim() === "" ) {
        // blank line inside table section: table might continue or end
      } else if (line.startsWith("### ")) {
        inDocTable = false;
        i--; // reprocess as a normal item heading
      } else if (!line.startsWith("|") && line.trim() !== "") {
        inDocTable = false;
        i--; // prose after table → normal item flow
      }
      continue;
    }
    if (line.startsWith("### ")) {
      // A non-official-docs item heading while scanning the table section ends it.
    }

    const hm = line.match(/^### (\d+([A-Z]?))\. (.+)$/);
    if (hm) {
      flush();
      current = {
        id: "",
        number: hm[1],
        title: hm[3].trim(),
        tier: tier === 0 ? 1 : tier,
        url: undefined,
        extraLinks: [],
        kind: "",
        time: "",
        why: undefined,
        lookFor: [],
        pairsWith: undefined,
      };
      continue;
    }

    if (!current) continue;

    const linkLine = line.match(/^- \[[ xX]\] <?(https?:\/\/[^>\s]+)>? · (.+)$/);
    if (linkLine) {
      if (!current.url) {
        current.url = linkLine[1];
      } else {
        current.extraLinks.push({ url: linkLine[1] });
      }
      const meta = splitMeta(linkLine[2]);
      current.kind = current.kind || meta.kind;
      current.time = current.time || meta.time;
      continue;
    }
    const bareLink = line.match(/^- \[[ xX]\] <?(https?:\/\/[^>\s]+)>?$/);
    if (bareLink) {
      if (!current.url) current.url = bareLink[1];
      else current.extraLinks.push({ url: bareLink[1] });
      continue;
    }
    const labeledLink = line.match(/^- \[[ xX]\] (.+?): <(https?:\/\/[^>\s]+)> · (.+)$/);
    if (labeledLink) {
      current.extraLinks.push({ url: labeledLink[2], label: labeledLink[1] });
      const meta = splitMeta(labeledLink[3]);
      current.kind = current.kind || meta.kind;
      current.time = current.time || meta.time;
      continue;
    }

    if (/^- \*\*Why:\*\*/.test(line)) {
      current.why = line.replace(/^- \*\*Why:\*\*\s*/, "");
      continue;
    }
    if (/^- \*\*Look for:\*\*/.test(line)) {
      inLookFor = true;
      continue;
    }
    if (inLookFor && /^\s*\d+\.\s/.test(line)) {
      current.lookFor.push(line.replace(/^\s*\d+\.\s/, "").trim());
      continue;
    }    if (/^- \*\*Pairs with:\*\*/.test(line)) {
      inLookFor = false;
      current.pairsWith = line.replace(/^- \*\*Pairs with:\*\*\s*/, "");
      continue;
    }
    // continuation of a wrapped Why/Pairs line
    if (!inLookFor && line.trim() !== "" && !line.startsWith("#") && !line.startsWith("- ")) {
      if (current.why !== undefined && !current.why.endsWith(".")) {
        // wrapped why-line continues
      }
      if (current.pairsWith && !current.lookFor.length) {
        current.pairsWith += " " + line.trim();
      } else if (current.why) {
        current.why += " " + line.trim();
      }
      continue;
    }
    // Blank lines between items carry no meaning; nothing to record.
  }
  flush();

  for (const t of [1, 2, 3, 4] as ReadingTier[]) {
    expectCondition(file, `tier ${t} to exist`, items.some((it) => it.tier === t));
  }
  expectCondition(file, "tier 1 to contain the product page item", items.some((it) => it.tier === 1 && /product page/.test(it.title)));

  return { items, docTableNote: docTableNote?.join(" ") };
}

/** Unused in production but handy in tests for grouping. */
export function itemsByTier(items: ReadingItem[]): Map<ReadingTier, ReadingItem[]> {
  const map = new Map<ReadingTier, ReadingItem[]>();
  for (const it of items) {
    const list = map.get(it.tier) ?? [];
    list.push(it);
    map.set(it.tier, list);
  }
  return map;
}

export { fail };
