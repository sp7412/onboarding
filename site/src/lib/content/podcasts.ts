import { contentId } from "./ids";
import { expectCondition } from "./errors";

export interface PodcastEpisode {
  id: string;
  /** Episode number as printed (1, 2, 10, 11, 3, …). */
  episode: string;
  title: string;
  /** Text after `**When:**` — when to listen. */
  when: string;
  /** The full fenced block verbatim (sources + prompt) for the copy button. */
  block: string;
  /** URLs listed in the block's SOURCES section. */
  sources: string[];
  generated: boolean;
  listened: boolean;
}

export function parsePodcastPrompts(markdown: string, file: string): PodcastEpisode[] {
  const lines = markdown.split("\n");
  const episodes: PodcastEpisode[] = [];
  let current: { episode: string; title: string; when: string; blockLines: string[]; inBlock: boolean } | undefined;

  const flush = () => {
    if (!current) return;
    const block = current.blockLines.join("\n").trimEnd();
    expectCondition(file, `episode ${current.episode} to have a fenced text block`, block.length > 0);
    const sources = [...block.matchAll(/^https?:\/\/\S+$/gm)].map((m) => m[0]);
    expectCondition(file, `episode ${current.episode} block to list sources`, sources.length > 0);
    expectCondition(
      file,
      `episode ${current.episode} block to contain a CUSTOMIZE PROMPT section`,
      /CUSTOMIZE PROMPT/i.test(block),
    );
    episodes.push({
      id: contentId("pod", `episode-${current.episode}`, `${current.episode}:${current.title}`),
      episode: current.episode,
      title: current.title,
      when: current.when,
      block,
      sources,
      generated: false,
      listened: false,
    });
    current = undefined;
  };

  for (const line of lines) {
    const em = line.match(/^## Episode (\d+|[A-Z]+): (.+)$/);
    if (em) {
      flush();
      current = { episode: em[1], title: em[2].trim(), when: "", blockLines: [], inBlock: false };
      continue;
    }
    if (!current) continue;

    const wm = line.match(/^- \[[ xX]\] Generated · \[[ xX]\] Listened · \*\*When:\*\* (.+)$/);
    if (wm) {
      current.when = wm[1].trim();
      continue;
    }
    if (/^```text/.test(line)) {
      current.inBlock = true;
      continue;
    }
    if (current.inBlock) {
      if (/^```$/.test(line.trim())) {
        current.inBlock = false;
      } else {
        current.blockLines.push(line);
      }
      continue;
    }
  }
  flush();

  // Per-file structural checks only; corpus-level expectations (episode count,
  // numbering) live in the repo integration tests.
  return episodes;
}
