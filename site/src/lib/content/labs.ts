import { expectCondition } from "./errors";

export interface Lab {
  number: string; // "00" … "08"
  slug: string;
  title: string;
  /** One-paragraph goal (first markdown paragraph after the H1). */
  goal: string;
  /** "none" | "optional OpenAI" | "OpenAI + LiveKit to run live" … */
  keys: string;
  /** Time estimate parsed from labs/README.md ("30–60 minutes", "60–90 minutes"). */
  time: string;
  /** Check-your-understanding questions (markdown cells). */
  questions: string[];
  /** Graded exercise text (markdown). */
  exercise: string;
  /** Sections of the notebook, for the launcher page. */
  sections: string[];
}

/** labs/README.md table rows: `| 00 | setup_and_mental_model | architecture + mock backend | none |` */
export function parseLabsReadme(markdown: string, file: string): { number: string; slug: string; layer: string; keys: string }[] {
  const rows = [...markdown.matchAll(/^\| (\d{2}) \| ([a-z0-9_]+) \| (.+?) \| (.+?) \|$/gm)].map(
    (m) => ({ number: m[1], slug: m[2], layer: m[3], keys: m[4] }),
  );
  // Row-shape validation only; the full-table expectation (9 labs) is checked in
  // the repo integration tests where the real README is parsed.
  return rows;
}

/** Parse a `# %%`-delimited notebook source into markdown cells and code cells. */
export function splitCells(source: string): { markdown: string[]; code: string[] } {
  const markdown: string[] = [];
  const code: string[] = [];
  let current: string[] | undefined;
  let mode: "markdown" | "code" | undefined;
  for (const raw of source.split("\n")) {
    const md = raw.match(/^# %% \[markdown\]/);
    const plain = /^# %%/.test(raw);
    if (md || plain) {
      if (current && mode === "markdown") markdown.push(current.join("\n"));
      if (current && mode === "code") code.push(current.join("\n"));
      current = [];
      mode = md ? "markdown" : "code";
      continue;
    }
    if (current && mode === "markdown") {
      // markdown lines are prefixed with `# ` (jupytext percent format)
      current.push(raw.replace(/^# ?/, ""));
    } else if (current && mode === "code") {
      current.push(raw);
    }
  }
  if (current && mode === "markdown") markdown.push(current.join("\n"));
  if (current && mode === "code") code.push(current.join("\n"));
  return { markdown, code };
}

export function parseLabSource(filename: string, source: string, readme: { keys: string; time: string }): Lab {
  const file = `labs/src/${filename}`;
  const number = filename.slice(0, 2);
  const { markdown } = splitCells(source);

  expectCondition(file, "at least one markdown cell", markdown.length > 0);
  const first = markdown[0];
  const titleMatch = first.match(/^# (\d{2}) · (.+)$/m);
  expectCondition(file, "an `# NN · Title` heading in the first markdown cell", Boolean(titleMatch));
  const title = titleMatch![2].trim();

  const goalParagraph = first
    .split("\n\n")
    .map((p) => p.replace(/\*\*/g, "").replace(/^#+\s.*$/, "").trim())
    .filter((p) => p && !p.startsWith("**Goal") && p.length > 60)[0];

  const sections = markdown
    .flatMap((cell) => cell.split("\n"))
    .filter((l) => /^## /.test(l))
    .map((l) => l.replace(/^## /, "").trim());

  // Check your understanding block: numbered questions after the heading.
  const qStart = markdown.findIndex((c) => /^## Check your understanding/m.test(c));
  expectCondition(file, "a `## Check your understanding` section", qStart !== -1);
  const questions: string[] = [];
  let exercise = "";
  for (const cell of markdown.slice(qStart)) {
    for (const line of cell.split("\n")) {
      const q = line.match(/^\d+\.\s+(.+)$/);
      if (q) questions.push(q[1].trim());
      const ex = line.match(/^\*\*Graded exercise:\*\* (.+)$/);
      if (ex) exercise = ex[1].trim();
    }
  }
  expectCondition(file, `lab ${number} to have at least two understanding questions`, questions.length >= 2);
  expectCondition(file, `lab ${number} to have a graded exercise`, Boolean(exercise));

  return {
    number,
    slug: filename.replace(/^(\d{2})_/, "").replace(/\.py$/, ""),
    title,
    goal: goalParagraph ?? first.replace(/^#+\s/m, "").trim().slice(0, 280),
    keys: readme.keys,
    time: readme.time,
    questions,
    exercise,
    sections,
  };
}
