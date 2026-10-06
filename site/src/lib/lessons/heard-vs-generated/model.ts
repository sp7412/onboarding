export type Playback = {
  generated: string;
  heard: string;
  interrupted: boolean;
};

export function truncateAtWord(text: string, wordCount: number): string {
  if (!Number.isInteger(wordCount) || wordCount < 0) throw new Error("word count must be a non-negative integer");
  return text.trim().split(/\s+/).filter(Boolean).slice(0, wordCount).join(" ");
}

export function playback(generated: string, heardWords: number | null): Playback {
  const clean = generated.trim().replace(/\s+/g, " ");
  if (heardWords === null) return { generated: clean, heard: clean, interrupted: false };
  return { generated: clean, heard: truncateAtWord(clean, heardWords), interrupted: true };
}

export function playbackSummary(result: Playback): string {
  if (!result.interrupted) return `Generated and heard: ${result.generated}`;
  const generated = result.generated.split(" ").filter(Boolean).length;
  const heard = result.heard.split(" ").filter(Boolean).length;
  return `Generated ${generated} words; heard ${heard}. The rest was truncated by the barge-in.`;
}
