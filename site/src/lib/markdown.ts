/**
 * Small, dependency-free Markdown renderer for repo content (trusted input).
 * Supports: h2–h4 (with ids), paragraphs, **bold**, *em*, `code`, [links](...),
 * <https://autolinks>, bare https:// URLs, nested lists, GitHub task lists
 * (rendered as persistent checkboxes), tables, multi-line blockquotes, fenced
 * code (mermaid shown as source with a GitHub link), and horizontal rules.
 */
import { contentId, slugify } from "./content/ids";

export interface RenderOptions {
  /** Repo-relative path of the source file (used to resolve relative links). */
  sourcePath: string;
  /** Map a repo-relative path (may include #hash) to a site URL, or null for GitHub. */
  resolveRepoLink: (repoPath: string) => string | null;
  /** Prefix for task-list checkbox ids (defaults to a slug of sourcePath). */
  idPrefix?: string;
  /** Drop the first H1 (pages render their own title). Default true. */
  skipH1?: boolean;
}

export interface RenderResult {
  html: string;
  checkIds: string[];
  headings: { level: number; text: string; id: string }[];
}

const REPO = "https://github.com/sp7412/onboarding/blob/main/";

export function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export function resolveRelative(from: string, target: string): string {
  const [pathname, hash] = target.split("#", 2);
  const base = pathname === "" ? from.split("/") : [...from.split("/").slice(0, -1), ...pathname.split("/")];
  const out: string[] = [];
  for (const part of base) {
    if (!part || part === ".") continue;
    if (part === "..") out.pop();
    else out.push(part);
  }
  return `${out.join("/")}${hash ? `#${hash}` : ""}`;
}

export function renderMarkdown(md: string, opts: RenderOptions): RenderResult {
  const idPrefix = opts.idPrefix ?? slugify(opts.sourcePath.replace(/\.md$/, ""));
  const checkIds: string[] = [];
  const headings: RenderResult["headings"] = [];
  const usedIds = new Map<string, number>();
  const skipH1 = opts.skipH1 ?? true;

  const href = (target: string): { url: string; external: boolean } => {
    if (/^(https?:|mailto:)/i.test(target)) return { url: target, external: true };
    if (target.startsWith("#")) return { url: target, external: false };
    const repoPath = resolveRelative(opts.sourcePath, target);
    const site = opts.resolveRepoLink(repoPath);
    if (site) return { url: site, external: false };
    return { url: REPO + repoPath, external: true };
  };

  const anchor = (url: string, external: boolean, textHtml: string) =>
    `<a href="${esc(url)}"${external ? ' rel="noopener noreferrer" target="_blank"' : ""}>${textHtml}</a>`;

  function inline(src: string, allowLinks = true): string {
    const slots: string[] = [];
    const hold = (html: string) => `\u0000${slots.push(html) - 1}\u0000`;
    let s = src;
    s = s.replace(/`([^`]+)`/g, (_m, code: string) => hold(`<code>${esc(code)}</code>`));
    if (allowLinks) {
      s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_m, text: string, target: string) => {
        const { url, external } = href(target);
        return hold(anchor(url, external, inline(text, false)));
      });
      s = s.replace(/<((?:https?:\/\/|mailto:)[^>\s]+)>/g, (_m, u: string) => hold(anchor(u, true, esc(u))));
    }
    s = esc(s);
    if (allowLinks) {
      s = s.replace(/(^|[\s(])(https?:\/\/[^\s<)\u0000]+[^\s<).,;:!?\u0000])/g, (_m, pre: string, u: string) =>
        `${pre}${hold(anchor(u.replace(/&amp;/g, "&"), true, u))}`);
    }
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s).,;:!?]|$)/g, "$1<em>$2</em>");
    s = s.replace(/(^|[\s(])_([^_\s][^_]*?)_(?=[\s).,;:!?]|$)/g, "$1<em>$2</em>");
    return s.replace(/\u0000(\d+)\u0000/g, (_m, i: string) => slots[Number(i)]);
  }

  const headingId = (text: string) => {
    const base = slugify(text.replace(/[`*_[\]()]/g, "")) || "section";
    const n = usedIds.get(base) ?? 0;
    usedIds.set(base, n + 1);
    return n ? `${base}-${n}` : base;
  };

  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const out: string[] = [];
  let i = 0;
  let seenH1 = false;

  const isBlockStart = (l: string) =>
    /^#{1,6} /.test(l) || /^\s*([-*+]|\d+\.) /.test(l) || l.startsWith(">") || l.startsWith("```") ||
    l.trim().startsWith("|") || /^(-{3,}|\*{3,})\s*$/.test(l.trim());

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed === "") { i++; continue; }

    // fenced code
    if (trimmed.startsWith("```")) {
      const lang = trimmed.slice(3).trim();
      const body: string[] = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) body.push(lines[i++]);
      i++;
      const code = esc(body.join("\n"));
      if (lang === "mermaid") {
        out.push(`<figure class="mermaid-src"><figcaption>Diagram source (Mermaid). <a href="${REPO}${opts.sourcePath}" rel="noopener noreferrer" target="_blank">View it rendered on GitHub</a>.</figcaption><pre><code>${code}</code></pre></figure>`);
      } else {
        out.push(`<pre class="code-block"${lang ? ` data-lang="${esc(lang)}"` : ""}><code>${code}</code></pre>`);
      }
      continue;
    }

    // headings
    const h = /^(#{1,6}) (.+)$/.exec(trimmed);
    if (h) {
      const level = h[1].length;
      const text = h[2].trim();
      i++;
      if (level === 1 && skipH1 && !seenH1) { seenH1 = true; continue; }
      const lvl = Math.min(Math.max(level, 2), 4);
      const id = headingId(text);
      headings.push({ level: lvl, text, id });
      out.push(`<h${lvl} id="${id}">${inline(text)}</h${lvl}>`);
      continue;
    }

    // hr
    if (/^(-{3,}|\*{3,})$/.test(trimmed)) { out.push("<hr />"); i++; continue; }

    // table
    if (trimmed.startsWith("|")) {
      const rows: string[][] = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        const cells = lines[i].trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
        rows.push(cells);
        i++;
      }
      const isSep = (r: string[]) => r.every((c) => /^:?-{2,}:?$/.test(c));
      const header = rows.length > 1 && isSep(rows[1]) ? rows[0] : null;
      const bodyRows = header ? rows.slice(2) : rows.filter((r) => !isSep(r));
      const thead = header ? `<thead><tr>${header.map((c) => `<th>${inline(c)}</th>`).join("")}</tr></thead>` : "";
      const tbody = `<tbody>${bodyRows.map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody>`;
      out.push(`<div class="table-wrap"><table>${thead}${tbody}</table></div>`);
      continue;
    }

    // blockquote (multi-line)
    if (trimmed.startsWith(">")) {
      const inner: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith(">")) inner.push(lines[i++].trim().replace(/^>\s?/, ""));
      const paras = inner.join("\n").split(/\n\s*\n/).map((p) => `<p>${inline(p.replace(/\n/g, " "))}</p>`);
      out.push(`<blockquote>${paras.join("")}</blockquote>`);
      continue;
    }

    // lists (nested by indentation)
    if (/^\s*([-*+]|\d+\.) /.test(line)) {
      const items: { indent: number; ordered: boolean; text: string }[] = [];
      while (i < lines.length) {
        const l = lines[i];
        const m = /^(\s*)([-*+]|\d+\.) (.*)$/.exec(l);
        if (m) {
          items.push({ indent: m[1].replace(/\t/g, "    ").length, ordered: /\d/.test(m[2]), text: m[3] });
          i++;
          continue;
        }
        // continuation line (indented, non-empty, not a new block)
        if (l.trim() !== "" && /^\s{2,}/.test(l) && !isBlockStart(l.trim()) && items.length) {
          items[items.length - 1].text += " " + l.trim();
          i++;
          continue;
        }
        break;
      }
      out.push(renderList(items));
      continue;
    }

    // paragraph
    const para: string[] = [];
    while (i < lines.length && lines[i].trim() !== "" && !isBlockStart(lines[i]) && !isBlockStart(lines[i].trim())) {
      para.push(lines[i].trim());
      i++;
    }
    if (para.length) out.push(`<p>${inline(para.join(" "))}</p>`);
    else i++;
  }

  function renderItem(text: string): string {
    const task = /^\[( |x|X)\]\s+(.*)$/.exec(text);
    if (!task) return inline(text);
    const body = task[2];
    const id = contentId(idPrefix, body, body);
    checkIds.push(id);
    // Extra inline boxes on the same line, e.g. "Generated · [ ] Listened".
    let n = 0;
    const rendered = inline(body).replace(/\[( |x|X)\]\s+([A-Za-z][\w-]*)/g, (_m, _x: string, label: string) => {
      const extra = contentId(idPrefix, `${body}#${++n}`, `${body}#${n}`);
      checkIds.push(extra);
      return `<label class="task"><input type="checkbox" data-check-id="${extra}" /> ${label}</label>`;
    });
    if (n === 0) return `<label class="task"><input type="checkbox" data-check-id="${id}" /> <span>${rendered}</span></label>`;
    const firstLabel = esc(body.split(/\s·\s|\s\[/)[0].replace(/[*_`]/g, "").trim() || "Done");
    return `<span class="task"><input type="checkbox" data-check-id="${id}" aria-label="${firstLabel}" /> <span>${rendered}</span></span>`;
  }

  function renderList(items: { indent: number; ordered: boolean; text: string }[]): string {
    let html = "";
    const stack: { indent: number; tag: string }[] = [];
    for (const it of items) {
      while (stack.length && it.indent < stack[stack.length - 1].indent) {
        html += `</li></${stack.pop()!.tag}>`;
      }
      const top = stack[stack.length - 1];
      if (!top || it.indent > top.indent) {
        const tag = it.ordered ? "ol" : "ul";
        const hasTask = /^\[( |x|X)\]\s/.test(it.text);
        html += `<${tag}${hasTask ? ' class="task-list"' : ""}>`;
        stack.push({ indent: it.indent, tag });
      } else {
        html += "</li>";
      }
      html += `<li>${renderItem(it.text)}`;
    }
    while (stack.length) html += `</li></${stack.pop()!.tag}>`;
    return html;
  }

  return { html: out.join("\n"), checkIds, headings };
}
