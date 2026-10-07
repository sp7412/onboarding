/**
 * Jargon tooltips: key voice-AI terms get a dashed underline and a definition
 * tooltip on first use per page. Definitions mirror notes/glossary.md — if you
 * change a definition there, change it here (and vice versa).
 *
 * Build time: renderMarkdown() wraps matches in <span class="jargon"> with an
 * embedded .jargon-tip definition (skipping <pre>/<code>). A small script in
 * BaseLayout then removes all but the first occurrence per page, so only the
 * first mention on a page is a tooltip.
 */

export interface JargonTerm {
  /** Matches plain text outside of tags; must have no capturing groups. */
  pattern: RegExp;
  /** Human term shown in the tooltip title row. */
  label: string;
  /** Definition shown in the tooltip (kept in sync with notes/glossary.md). */
  definition: string;
}

export const JARGON: JargonTerm[] = [
  {
    pattern: /\bendpointing\b/gi,
    label: "Endpointing",
    definition:
      "Deciding that a caller's spoken turn is complete after speech and silence cues.",
  },
  {
    pattern: /\bbarge[- ]in\b/gi,
    label: "Barge-in",
    definition:
      "The caller speaking while the agent is speaking, causing the agent to yield or stop.",
  },
  {
    pattern: /\bcontainment\b/gi,
    label: "Containment",
    definition: "Share of calls fully handled by the AI agent without a human.",
  },
  {
    pattern: /\btime to first token\b/gi,
    label: "Time to first token (TTFT)",
    definition:
      "How long the model takes to start producing its first token after receiving input — a big lever on perceived latency.",
  },
  {
    pattern: /\bVAD\b/g,
    label: "VAD",
    definition: "Voice activity detection: detecting whether audio currently contains speech.",
  },
  {
    pattern: /\bvoice activity detection\b/gi,
    label: "Voice activity detection (VAD)",
    definition: "Detecting whether audio currently contains speech.",
  },
];

/** One alternation over every term, so inserted tooltip HTML is never rescanned. */
const COMBINED = new RegExp(JARGON.map((t) => `(${t.pattern.source})`).join("|"), "gi");

function escapeAttr(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}

function tipFor(term: JargonTerm, matched: string): string {
  return (
    `<span class="jargon" tabindex="0" data-jargon="${escapeAttr(term.label)}">` +
    `${matched}` +
    `<span class="jargon-tip" role="tooltip"><strong>${escapeAttr(term.label)}</strong>` +
    `${escapeAttr(term.definition)}</span></span>`
  );
}

/** Build a single tooltip span for use in .astro templates on static text. */
export function jargonSpan(key: "endpointing" | "barge-in" | "containment" | "ttft" | "vad" | "vad-long", text: string): string {
  const term = JARGON.find((t) => t.label.toLowerCase().startsWith(key === "ttft" ? "time to first token" : key === "vad" ? "vad" : key === "vad-long" ? "voice activity" : key));
  return term ? tipFor(term, text) : text;
}

/**
 * Wrap jargon terms in an HTML string with tooltip markup. Tags are respected:
 * text inside <pre>, <code>, headings and existing .jargon spans is never touched.
 */
export function markupJargon(html: string): string {
  const parts = html.split(/(<[^>]+>)/g);
  const openTags: string[] = [];
  let firstWrapDone = false; // reserved: build-time wraps all; runtime dedupes
  void firstWrapDone;

  return parts
    .map((part) => {
      if (part.startsWith("<")) {
        const name = /^<\s*\/?\s*([a-zA-Z][a-zA-Z0-9-]*)/.exec(part)?.[1]?.toLowerCase();
        if (name && !part.startsWith("</") && !part.endsWith("/>")) openTags.push(name);
        else if (name) {
          const idx = openTags.lastIndexOf(name);
          if (idx !== -1) openTags.splice(idx, 1);
        }
        return part;
      }
      // Headings are self-links (permalinks); a focusable tooltip inside a link is invalid.
      if (["pre", "code", "h1", "h2", "h3", "h4", "h5", "h6"].some((t) => openTags.includes(t))) return part;
      return part.replace(COMBINED, (match, ...groups) => {
        // groups: one per term (which fired), then offset/string — find the index.
        const hit = groups.findIndex((g, i) => g !== undefined && i < JARGON.length);
        if (hit === -1) return match;
        return tipFor(JARGON[hit], match);
      });
    })
    .join("");
}
