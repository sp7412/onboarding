import { contentId } from "./ids";
import { expectCondition, fail } from "./errors";

export interface ChecklistItem {
  /** Stable ID: `chk-<stage>-<weekslug>-<hash8(text)>` */
  id: string;
  stage: "pre-start" | "d30" | "d60" | "d90" | "recurring";
  stageLabel: string;
  week: string;
  weekSlug: string;
  /** Raw item text with repo links preserved as markdown. */
  text: string;
  /** Repo-relative markdown links found in the item (display text + target). */
  links: { text: string; target: string }[];
  isExitCriterion: boolean;
}

export interface ChecklistWeek {
  week: string;
  weekSlug: string;
  items: ChecklistItem[];
  /** `**Output:** …` line under a week, if present. */
  output?: string;
}

export interface ChecklistStage {
  stage: ChecklistItem["stage"];
  stageLabel: string;
  weeks: ChecklistWeek[];
  itemCount: number;
}

export interface ChecklistDoc {
  title: string;
  intro: string[];
  stages: ChecklistStage[];
  watchouts: string[];
}

const STAGES: { heading: RegExp; stage: ChecklistItem["stage"]; label: string }[] = [
  { heading: /^## Pre-Start:/i, stage: "pre-start", label: "Pre-start (now–Oct 25)" },
  { heading: /^## Days 1–30:/i, stage: "d30", label: "Days 1–30: understand and earn trust" },
  { heading: /^## Days 31–60:/i, stage: "d60", label: "Days 31–60: align, design, and contribute" },
  { heading: /^## Days 61–90:/i, stage: "d90", label: "Days 61–90: own and multiply" },
  { heading: /^## Recurring Weekly Rhythm/i, stage: "recurring", label: "Recurring weekly rhythm" },
];

const REPO_LINK = /\[([^\]]+)\]\((\.\.?\/[^)]+)\)/g;

function parseLinks(text: string): { text: string; target: string }[] {
  return [...text.matchAll(REPO_LINK)].map((m) => ({ text: m[1], target: m[2] }));
}

function stageForHeading(line: string): (typeof STAGES)[number] | undefined {
  return STAGES.find((s) => s.heading.test(line));
}

/** Which stage owns the exit-criteria list `Day-N exit criteria` belongs to. */
function exitStage(heading: string): ChecklistItem["stage"] | undefined {
  if (/^### Day-30 exit criteria/i.test(heading)) return "d30";
  if (/^### Day-60 check/i.test(heading)) return "d60";
  if (/^### Day-90 exit criteria/i.test(heading)) return "d90";
  return undefined;
}

export function parseChecklist(markdown: string, file: string): ChecklistDoc {
  const lines = markdown.split("\n");
  const titleLine = lines.find((l) => l.startsWith("# "));
  expectCondition(file, "an H1 title", Boolean(titleLine));
  const title = titleLine!.slice(2).trim();

  // Intro = everything before the first `## ` heading that isn't the title.
  const firstHeading = lines.findIndex((l) => l.startsWith("## "));
  expectCondition(file, "at least one `## ` section", firstHeading !== -1);
  const intro = lines
    .slice(1, firstHeading)
    .filter((l) => !l.startsWith("#") && l.trim() !== "");

  const doc: ChecklistDoc = { title, intro, stages: [], watchouts: [] };

  let current: ChecklistStage | undefined;
  let week: ChecklistWeek | undefined;
  let inWatchouts = false;
  let pending: string[] = [];

  const flushPending = () => {
    if (!pending.length) return;
    if (!current) fail(file, "a checklist item inside a stage");
    // Items directly under a stage (no `### ` heading) land in an implicit "Ongoing" week.
    if (!week) {
      week = { week: "Ongoing", weekSlug: "ongoing", items: [] };
      current.weeks.push(week);
    }
    const text = pending.join(" ").trim();
    pending = [];
    week.items.push({
      id: contentId("chk", `${current.stage}-${week.weekSlug}`, text),
      stage: current.stage,
      stageLabel: current.stageLabel,
      week: week.week,
      weekSlug: week.weekSlug,
      text,
      links: parseLinks(text),
      isExitCriterion: false,
    });
  };

  for (const raw of lines) {
    const line = raw.trimEnd();

    const stageMatch = stageForHeading(line);
    if (stageMatch) {
      flushPending();
      week = undefined;
      inWatchouts = false;
      current = { stage: stageMatch.stage, stageLabel: stageMatch.label, weeks: [], itemCount: 0 };
      doc.stages.push(current);
      continue;
    }

    if (/^## Watch-outs/i.test(line)) {
      flushPending();
      inWatchouts = true;
      week = undefined;
      continue;
    }

    if (inWatchouts) {
      if (line.startsWith("- ")) doc.watchouts.push(line.slice(2).trim());
      continue;
    }

    if (!current) continue; // 90-day contract table etc.

    if (line.startsWith("### ")) {
      flushPending();
      const heading = line.slice(4).trim();
      const exit = exitStage(line);
      if (exit) {
        week = {
          week: heading,
          weekSlug: `exit-${exit}`,
          items: [],
        };
        current.weeks.push(week);
      } else {
        // `### Week of Sept 28 — Build the learning agenda` or `### Week 1 (…)`
        const em = heading.indexOf(" — ");
        const weekTitle = em !== -1 ? heading.slice(0, em) : heading;
        week = { week: heading, weekSlug: contentId("wk", weekTitle, heading).slice(3), items: [] };
        current.weeks.push(week);
      }
      continue;
    }

    if (line.startsWith("**Output:**")) {
      flushPending();
      if (week) week.output = line.slice("**Output:**".length).trim();
      continue;
    }

    if (/^- \[[ x]\] /i.test(line)) {
      flushPending();
      pending = [line.replace(/^- \[[ x]\] /i, "")];
      continue;
    }

    // Continuation lines of a wrapped checkbox item.
    if (pending.length && line.trim() !== "" && !line.startsWith("#")) {
      pending.push(line.trim());
      continue;
    }

    flushPending();
  }
  flushPending();

  for (const stage of doc.stages) {
    stage.itemCount = stage.weeks.reduce((n, w) => n + w.items.length, 0);
  }

  // Mark exit-criterion items by their weekSlug prefix.
  for (const stage of doc.stages) {
    for (const w of stage.weeks) {
      if (w.weekSlug.startsWith("exit-")) {
        for (const item of w.items) item.isExitCriterion = true;
      }
    }
  }

  // Strictness: every stage must have weeks with items.
  expectCondition(file, "the pre-start stage with at least one week and item", (() => {
    const pre = doc.stages.find((s) => s.stage === "pre-start");
    return Boolean(pre && pre.weeks.length > 0 && pre.weeks.every((w) => w.items.length > 0));
  })());
  for (const stage of doc.stages) {
    expectCondition(
      file,
      `stage "${stage.stageLabel}" to contain at least one item`,
      stage.itemCount > 0,
    );
  }

  return doc;
}

/** Flatten weeks into ordered items, keeping stage context. */
export function flattenChecklist(doc: ChecklistDoc): ChecklistItem[] {
  return doc.stages.flatMap((s) => s.weeks.flatMap((w) => w.items));
}
