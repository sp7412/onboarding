import { describe, expect, it } from "vitest";
import { renderMarkdown } from "./markdown";

const r = (md: string) =>
  renderMarkdown(md, { sourcePath: "docs/x.md", resolveRepoLink: (p) => (p === "docs/y.md" ? "/onboarding/docs/y/" : null) });

describe("renderMarkdown", () => {
  it("renders autolinks and bare URLs as links", () => {
    const { html } = r("See <https://example.com/a> and https://example.org/b.");
    expect(html).toContain('<a href="https://example.com/a"');
    expect(html).toContain('<a href="https://example.org/b"');
    expect(html).not.toContain("&lt;https://");
  });
  it("routes repo links and falls back to GitHub", () => {
    const { html } = r("[y](y.md) and [z](../labs/z.py)");
    expect(html).toContain('href="/onboarding/docs/y/"');
    expect(html).toContain('href="https://github.com/sp7412/onboarding/blob/main/labs/z.py"');
  });
  it("renders tables with headers", () => {
    const { html } = r("| A | B |\n|---|---|\n| 1 | <https://e.com> |");
    expect(html).toContain("<th>A</th>");
    expect(html).toContain('<td><a href="https://e.com"');
  });
  it("turns task items into persistent checkboxes", () => {
    const res = r("- [ ] Read the thing\n  - nested note");
    expect(res.checkIds).toHaveLength(1);
    expect(res.html).toContain('data-check-id="' + res.checkIds[0] + '"');
    expect(res.html).toMatch(/<ul[^>]*>.*<ul>/s);
  });
  it("skips the H1 and ids headings", () => {
    const { html, headings } = r("# Title\n\n## Five Takeaways\n\ntext");
    expect(html).not.toContain("Title</h");
    expect(headings[0]).toMatchObject({ id: "five-takeaways", level: 2 });
  });
  it("keeps code verbatim and escaped", () => {
    const { html } = r("```text\n<https://x.com> **not bold**\n```");
    expect(html).toContain("&lt;https://x.com&gt; **not bold**");
  });
  it("renders audio links as players with a download link", () => {
    const { html } = r("- **Listen:** [Episode 1 audio (m4a)](https://github.com/o/r/releases/download/podcasts/episode-01.m4a)");
    expect(html).toContain('<audio controls preload="none" src="https://github.com/o/r/releases/download/podcasts/episode-01.m4a">');
    expect(html).toContain(">Episode 1 audio (m4a)</a>");
  });
  it("keeps inline code inside link text", () => {
    const { html } = r("see [`docs/y.md`](y.md)");
    expect(html).toContain('href="/onboarding/docs/y/"><code>docs/y.md</code></a>');
  });
});
