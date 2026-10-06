import { expectCondition } from "./errors";
import type { Video } from "./videos";
import { EXPLAINERS } from "./explainers";

export interface VideoNote {
  id: string;
  title: string;
  url: string;
  itemNumber: string;
  time: string;
  takeaways: string[];
  why: string;
  questions: string[];
}

const URL_RE = /^https:\/\/(?:www\.)?youtube\.com\/watch\?v=([\w-]{11})$/;
const EXPLAINER_RE = /^https:\/\/github\.com\/sp7412\/onboarding\/releases\/download\/explainer-series\/(voice-agents-\d{2}-[a-z-]+)-1080p\.mp4$/;

function sectionBody(lines: string[], heading: string, file: string, title: string): string[] {
  const start = lines.indexOf(heading);
  expectCondition(file, `note "${title}" to have a ${heading.replace(/\*\*/g, "") } section`, start >= 0);
  const end = lines.findIndex((line, i) => i > start && line.startsWith("- **"));
  return lines.slice(start + 1, end < 0 ? lines.length : end).filter((line) => line.trim());
}

function inlineSection(lines: string[], heading: string, file: string, title: string): string[] {
  const line = lines.find((value) => value.startsWith(heading));
  expectCondition(file, `note "${title}" to have a ${heading.replace(/\*\*/g, "") } section`, Boolean(line));
  return [line!.slice(heading.length).trim()].filter(Boolean);
}

function numbered(lines: string[], file: string, title: string, kind: string): string[] {
  const values = lines.filter((line) => /^\s*\d+\.\s+/.test(line)).map((line) => line.replace(/^\s*\d+\.\s+/, "").trim());
  expectCondition(file, `note "${title}" to have ${kind}`, values.length > 0);
  return values;
}

/** YouTube video ID, or the explainer ID for this repo's own explainer series. */
export function videoId(url: string): string | undefined {
  return url.match(URL_RE)?.[1] ?? url.match(EXPLAINER_RE)?.[1];
}

export function parseVideoNotes(markdown: string, file: string, videos: Video[]): VideoNote[] {
  const known = new Map<string | undefined, { title: string; itemNumber: string }>(videos.map((video) => [videoId(video.url), video]));
  for (const e of EXPLAINERS) known.set(e.id, { title: e.title, itemNumber: "0" });
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const headings = lines.map((line, i) => ({ line, i })).filter(({ line }) => /^## /.test(line));
  const notes: VideoNote[] = [];

  for (let index = 0; index < headings.length; index++) {
    const { line, i } = headings[index];
    const title = line.slice(3).trim();
    const end = headings[index + 1]?.i ?? lines.length;
    const block = lines.slice(i + 1, end).filter((line) => line.trim());
    const meta = block.shift() ?? "";
    const match = meta.match(/^- Video: <([^>]+)> · (.+) · reading-guide item (\d+[A-Z]?)$/);
    expectCondition(file, `note "${title}" to have a valid Video line`, Boolean(match), meta);
    const url = match![1];
    const id = videoId(url);
    expectCondition(file, `note "${title}" to have a YouTube or explainer video URL`, Boolean(id), url);
    const video = known.get(id!);
    expectCondition(file, `note "${title}" to match a video on the Videos page`, Boolean(video), url);
    const normalizeTitle = (value: string) => value
      .replace(/,\s+(?=(Tracing|Types of Runs|Debugging with Studio|Playground & Prompts|Datasets & Evaluations|Annotation Queues|Automations & Online Evaluation|Dashboards)$)/, ": ")
      .replace(/\s*\([^)]*\)$/, "")
      .replace(/\s+\(again\)$/i, "")
      .toLowerCase();
    expectCondition(file, `note "${title}" title to match its video`, normalizeTitle(title) === normalizeTitle(video!.title), video!.title);
    expectCondition(file, `note "${title}" reading-guide item to match its video`, match![3] === video!.itemNumber, video!.itemNumber);

    const takeaways = numbered(sectionBody(block, "- **Takeaways:**", file, title), file, title, "takeaways");
    expectCondition(file, `note "${title}" to have no more than five takeaways`, takeaways.length <= 5);
    const whyLines = inlineSection(block, "- **Why it matters here:**", file, title);
    expectCondition(file, `note "${title}" analysis to be labeled`, whyLines.join(" ").startsWith("Analysis:"));
    const why = whyLines.join(" ").replace(/^Analysis:\s*/, "").trim();
    expectCondition(file, `note "${title}" to have an analysis`, Boolean(why));
    const questions = numbered(sectionBody(block, "- **Questions to discuss:**", file, title), file, title, "questions");
    expectCondition(file, `note "${title}" to have no more than two questions`, questions.length <= 2);
    notes.push({ id: id!, title, url, itemNumber: match![3], time: match![2], takeaways, why, questions });
  }

  expectCondition(file, "at least one video note", notes.length > 0);
  expectCondition(file, "unique video note IDs", new Set(notes.map((note) => note.id)).size === notes.length);
  return notes;
}
