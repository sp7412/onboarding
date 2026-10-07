import fs from "node:fs";
import path from "node:path";
import { parseChecklist, flattenChecklist, type ChecklistDoc, type ChecklistItem } from "./checklist";
import { parseReadingGuide, type ReadingDoc } from "./reading-guide";
import { parsePodcastPrompts, type PodcastEpisode } from "./podcasts";
import { parseWhitepaperChapter, parseWhitepaperOrder, type WhitepaperChapter } from "./whitepaper";
import { parseGlossary, type GlossaryTerm } from "./glossary";
import { parseLabSource, parseLabsReadme, type Lab } from "./labs";
import { expectCondition } from "./errors";
import { parseVideoNotes, type VideoNote } from "./video-notes";
import { parseVideos, type Video } from "./videos";

export interface RepoDoc {
  /** Repo-relative path like "docs/servicetitan-101.md". */
  repoPath: string;
  slug: string;
  title: string;
  body: string;
}

export interface ContentBundle {
  checklist: ChecklistDoc;
  checklistItems: ChecklistItem[];
  reading: ReadingDoc;
  podcasts: PodcastEpisode[];
  whitepaper: { order: string[]; chapters: WhitepaperChapter[] };
  glossary: GlossaryTerm[];
  labs: Lab[];
  videos: Video[];
  videoNotes: VideoNote[];
  docs: RepoDoc[];
  templates: RepoDoc[];
}

// Repo root = the directory containing plan/30-60-90-checklist.md. Works under
// vitest (cwd = site/), in Astro dev, and in the built server bundle (where
// __dirname is unavailable but import.meta.url survives bundling).
function repoRoot(): string {
  const moduleDir = (() => {
    try {
      // eslint-disable-next-line @typescript-eslint/no-implied-eval
      return path.dirname(new URL(import.meta.url).pathname);
    } catch {
      return process.cwd();
    }
  })();
  const candidates = [
    path.resolve(process.cwd(), ".."),   // cwd = site/
    path.resolve(process.cwd()),         // cwd = repo root
    path.resolve(moduleDir, "..", "..", ".."), // module dir = site/src/lib/content
    path.resolve(moduleDir, "..", "..", "..", "..", ".."), // bundled: dist/chunks -> repo
  ];
  for (const dir of candidates) {
    if (fs.existsSync(path.join(dir, "plan", "30-60-90-checklist.md"))) return dir;
  }
  return candidates[0];
}

const REPO_ROOT = repoRoot();

function read(repoRelative: string): string {
  const p = path.join(REPO_ROOT, repoRelative);
  if (!fs.existsSync(p)) {
    throw new Error(`content source missing: ${repoRelative} (looked in ${REPO_ROOT})`);
  }
  return fs.readFileSync(p, "utf8");
}

export function readRepoFile(repoRelative: string): string {
  return read(repoRelative);
}

function parseDoc(repoRelative: string, slugOverride?: string): RepoDoc {
  const body = read(repoRelative);
  const lines = body.split("\n");
  const h1 = lines.find((l) => l.startsWith("# "));
  expectCondition(repoRelative, "an H1 title", Boolean(h1));
  const slug = slugOverride ?? path.basename(repoRelative, ".md");
  return { repoPath: repoRelative, slug, title: h1!.slice(2).trim(), body };
}

export interface DocPage {
  repoPath: string;
  icon: string;
  /** Route slug; defaults to the file's basename. */
  slug?: string;
  /** Pages that belong to a track are listed on the track's index page, not as home cards. */
  track?: string;
}

export const DOC_PAGES: DocPage[] = [
  { repoPath: "docs/servicetitan-101.md", icon: "reading" },
  { repoPath: "docs/how-a-contractor-works.md", icon: "reading" },
  { repoPath: "docs/voice-agent-architecture.md", icon: "architecture" },
  { repoPath: "docs/speech-to-speech-models.md", icon: "architecture" },
  { repoPath: "docs/gpt-live-1.md", icon: "architecture" },
  { repoPath: "docs/pantheon-2026-ai-roadmap.md", icon: "reading" },
  { repoPath: "docs/build-your-own-voice-agent.md", icon: "labs" },
  { repoPath: "docs/tools-and-guardrails.md", icon: "guardrails" },
  { repoPath: "docs/call-anatomy.md", icon: "telephony" },
  { repoPath: "docs/evaluating-voice-agents.md", icon: "evaluation" },
  { repoPath: "docs/livekit-hands-on.md", icon: "labs" },
  { repoPath: "docs/first-90-days-playbook.md", icon: "plan" },
  { repoPath: "docs/manager-alignment.md", icon: "team" },
  { repoPath: "docs/voice-agents-cheat-sheet.md", icon: "notes" },
  { repoPath: "docs/capstone-rubric.md", icon: "evaluation" },
  { repoPath: "senior-engineer/README.md", icon: "compass", slug: "senior-engineer" },
  { repoPath: "senior-engineer/what-i-need-to-know.md", icon: "compass", track: "senior-engineer" },
  { repoPath: "senior-engineer/architecture-review.md", icon: "compass", track: "senior-engineer" },
  { repoPath: "senior-engineer/latency-budget.md", icon: "compass", track: "senior-engineer" },
  { repoPath: "senior-engineer/eval-design.md", icon: "compass", track: "senior-engineer" },
  { repoPath: "senior-engineer/production-incident.md", icon: "compass", track: "senior-engineer" },
  { repoPath: "senior-engineer/first-pr-decision-tree.md", icon: "compass", track: "senior-engineer" },
  { repoPath: "senior-engineer/hypotheses.md", icon: "compass", track: "senior-engineer" },
  { repoPath: "docs/references.md", icon: "reading" },
  { repoPath: "notes/study-question.md", icon: "notes" },
  { repoPath: "notes/conversation-notes.md", icon: "notes" },
];

export const TEMPLATE_FILES = [
  "onboarding-log.md",
  "1on1-questions.md",
  "working-with-me.md",
  "pre-mortem.md",
  "brag-document.md",
  "weekly-status.md",
  "30-day-memo.md",
  "design-doc.md",
  "90-day-retro.md",
];

export function docSlug(page: DocPage): string {
  return page.slug ?? path.basename(page.repoPath, ".md");
}

/** Site route for a DOC_PAGES entry. */
export function docRoute(repoPath: string): string {
  const page = DOC_PAGES.find((d) => d.repoPath === repoPath);
  if (!page) throw new Error(`not a doc page: ${repoPath}`);
  return `/docs/${docSlug(page)}`;
}

/**
 * Map a repo-relative path (optionally with #hash) to a site route, or null to
 * link to the file on GitHub instead.
 */
export function repoLinkToRoute(target: string): string | null {
  const [rawPath, hash] = target.replace(/^\.\.?\//, "").split("#", 2);
  const clean = rawPath.replace(/\/$/, "");
  const withHash = (route: string) => (hash ? `${route}#${hash}` : route);
  if (clean === "" || clean === "README.md") return withHash("/");
  if (clean === "docs/whitepaper" || clean === "docs/whitepaper/README.md") return withHash("/whitepaper");
  if (clean.startsWith("docs/whitepaper/") && clean.endsWith(".md")) {
    const slug = path.basename(clean, ".md");
    if (slug === "claims-ledger") return null;
    return withHash(`/whitepaper/${slug}`);
  }
  if (clean === "senior-engineer") return withHash(docRoute("senior-engineer/README.md"));
  const page = DOC_PAGES.find((d) => d.repoPath === clean);
  if (page) return withHash(`/docs/${docSlug(page)}`);
  if (clean === "docs/reading-guide.md") return withHash("/reading");
  if (clean === "docs/podcast-prompts.md") return withHash("/podcasts");
  if (clean === "docs/capstone-rubric.md") return withHash("/docs/capstone-rubric");
  if (clean === "notes/glossary.md") return withHash("/glossary");
  if (clean === "plan/30-60-90-checklist.md") return withHash("/checklist");
  if (clean === "templates" || clean === "templates/README.md") return "/templates";
  if (clean.startsWith("templates/") && clean.endsWith(".md")) return `/templates#${path.basename(clean, ".md")}`;
  if (clean === "labs" || clean === "labs/README.md") return withHash("/labs");
  return null;
}

let cached: ContentBundle | undefined;

export function loadContent(): ContentBundle {
  if (cached) return cached;

  const checklist = parseChecklist(read("plan/30-60-90-checklist.md"), "plan/30-60-90-checklist.md");
  const reading = parseReadingGuide(read("docs/reading-guide.md"), "docs/reading-guide.md");
  const videos = parseVideos(read("docs/reading-guide.md"), "docs/reading-guide.md");
  const videoNotes = parseVideoNotes(read("docs/video-notes.md"), "docs/video-notes.md", videos);
  const podcasts = parsePodcastPrompts(read("docs/podcast-prompts.md"), "docs/podcast-prompts.md");
  const glossary = parseGlossary(read("notes/glossary.md"), "notes/glossary.md");

  const wpReadme = read("docs/whitepaper/README.md");
  const order = parseWhitepaperOrder(wpReadme, "docs/whitepaper/README.md");
  const chapters = order.map((f) => parseWhitepaperChapter(f, read(`docs/whitepaper/${f}`)));

  const labReadme = read("labs/README.md");
  const labRows = parseLabsReadme(labReadme, "labs/README.md");
  const labs = labRows.map((row) => {
    const filename = `${row.number}_${row.slug}.py`;
    const source = read(`labs/src/${filename}`);
    expectCondition("labs/README.md", `source ${filename}`, fs.existsSync(path.join(REPO_ROOT, "labs/src", filename)));
    expectCondition("labs/README.md", `generated ${row.number} notebook`, fs.existsSync(path.join(REPO_ROOT, "labs", `${row.number}_${row.slug}.ipynb`)));
    return parseLabSource(filename, source, { keys: row.keys, time: row.time });
  });
  const sourceLabs = fs.readdirSync(path.join(REPO_ROOT, "labs/src")).filter((f) => /^\d{2}_.+\.py$/.test(f));
  const notebookLabs = fs.readdirSync(path.join(REPO_ROOT, "labs")).filter((f) => /^\d{2}_.+\.ipynb$/.test(f));
  const stems = (files: string[]) => files.map((f) => f.replace(/\.(py|ipynb)$/, "")).sort().join(",");
  expectCondition("labs", "exactly matching source and generated lab sets",
    sourceLabs.length === labRows.length && stems(sourceLabs) === stems(notebookLabs));

  const docs = DOC_PAGES.map((d) => parseDoc(d.repoPath, d.slug));
  const slugs = docs.map((d) => d.slug);
  expectCondition("DOC_PAGES", "unique doc slugs", new Set(slugs).size === slugs.length);
  const templates = TEMPLATE_FILES.map((f) => parseDoc(`templates/${f}`));

  cached = { checklist, checklistItems: flattenChecklist(checklist), reading, podcasts, whitepaper: { order, chapters }, glossary, labs, videos, videoNotes, docs, templates };
  return cached;
}
