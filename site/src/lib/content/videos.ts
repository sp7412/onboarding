/**
 * Collects every YouTube link in docs/reading-guide.md into a list for the Videos page.
 * The reading guide stays the single source of truth; checkbox IDs match the Reading page,
 * so marking a video watched on either page counts for both.
 */
import { contentId } from "./ids";
import { expectCondition } from "./errors";

export interface Video {
  id: string;
  url: string;
  title: string;
  itemNumber: string;
  itemTitle: string;
  tier: number;
  kind: string;
  time: string;
  minutes: number | null;
  mustWatch: boolean;
  isPlaylist: boolean;
  pairsWith?: string;
  why?: string;
}

const LINE = /^- \[[ xX]\] (?:(.+?): )?<(https:\/\/(?:www\.)?youtube\.com\/(?:watch\?v=[\w-]{11}|playlist\?list=[\w-]+))> · (.+)$/;

function cleanLabel(label: string): string {
  let t = label.replace(/^Optional\s*/i, "");
  if (t.startsWith("(")) t = `Getting Started with LangSmith ${t}`;
  return t.replace(/\((\d\/\d)\),\s*/, "($1): ");
}

export function minutesOf(time: string): number | null {
  const m = time.match(/^(\d+)\s*min$/);
  return m ? Number(m[1]) : null;
}

export function parseVideos(markdown: string, file: string): Video[] {
  const videos: Video[] = [];
  let tier = 0;
  let item: { number: string; title: string; start: number } | undefined;
  let pending: Video[] = [];
  const finishItem = (lines: string[]) => {
    if (!item || !pending.length) { pending = []; return; }
    const block = lines.slice(item.start);
    const pairs = block.find((l) => l.startsWith("- **Pairs with:**"))?.replace("- **Pairs with:**", "").trim();
    const why = block.find((l) => l.startsWith("- **Why:**"))?.replace("- **Why:**", "").trim();
    for (const v of pending) videos.push({ ...v, pairsWith: pairs, why });
    pending = [];
  };
  const lines = markdown.split("\n");
  lines.forEach((line, i) => {
    const t = line.match(/^## Tier (\d)/);
    if (t) tier = Number(t[1]);
    const h = line.match(/^### (\d+[A-Z]?)\. (.+)$/);
    if (h) {
      finishItem(lines.slice(0, i));
      item = { number: h[1], title: h[2].trim(), start: i };
      return;
    }
    const v = line.match(LINE);
    if (v && item) {
      const body = line.replace(/^- \[[ xX]\] /, "");
      const parts = v[3].split("·").map((p) => p.trim()).filter(Boolean);
      const time = parts[parts.length - 1] ?? "";
      const label = v[1]?.trim();
      const optional = /^optional\b/i.test(label ?? "");
      pending.push({
        id: contentId("reading", body, body),
        url: v[2],
        title: label ? cleanLabel(label) : item.title,
        itemNumber: item.number,
        itemTitle: item.title,
        tier,
        kind: parts.slice(0, -1).join(" · "),
        time,
        minutes: minutesOf(time),
        mustWatch: tier > 0 && tier <= 2 && !optional,
        isPlaylist: v[2].includes("playlist?list="),
      });
    }
  });
  finishItem(lines);
  expectCondition(file, "at least one YouTube video in the reading guide", videos.length > 0);
  return videos;
}

export const VIDEO_TOPICS: { key: string; title: string; blurb: string; items: string[] }[] = [
  { key: "voice", title: "Voice agents in practice", blurb: "How production voice agents are designed, from teams that ship them.", items: ["5", "10", "23"] },
  { key: "livekit", title: "LiveKit", blurb: "The real-time transport layer: pipelines, turn detection, telephony.", items: ["11A", "11B", "11C"] },
  { key: "langsmith", title: "LangSmith: tracing and evaluation", blurb: "What traces, runs, datasets and experiments look like in the tool.", items: ["14A"] },
  { key: "background", title: "Background", blurb: "Broader context on building AI products.", items: [] },
];

export const WATCH_WHEN: Record<string, string> = {
  "11B": "Week of Sept 28, before lab 03",
  "5": "Week of Oct 5",
  "10": "Week of Oct 5",
  "11A": "Week of Oct 5, with lab 04",
  "14A": "Week of Oct 12, before lab 07",
  "23": "First 30 days",
  "27": "Anytime",
};

export function topicOf(itemNumber: string): string {
  return VIDEO_TOPICS.find((t) => t.items.includes(itemNumber))?.key ?? "background";
}
