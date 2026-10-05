import fs from "node:fs";
import path from "node:path";

const dist = path.resolve("dist");
const pages = ["index.html", "checklist/index.html", "whitepaper/00-introduction/index.html", "simulations/index.html", "glossary/index.html", "videos/index.html"];
const widths = [390, 1280];
const failures = [];
for (const relative of pages) {
  const file = path.join(dist, relative);
  if (!fs.existsSync(file)) { failures.push(`${relative}: missing page`); continue; }
  const html = fs.readFileSync(file, "utf8");
  for (const width of widths) {
    if (!/<main\b[^>]*id=["']main["']/i.test(html)) failures.push(`${relative}@${width}: missing main landmark`);
    if (!/<nav\b[^>]*aria-label=/i.test(html)) failures.push(`${relative}@${width}: unlabeled navigation`);
    for (const match of html.matchAll(/<img\b([^>]*)>/gi)) if (!/\balt=["']/i.test(match[1])) failures.push(`${relative}@${width}: image missing alt`);
    for (const match of html.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/gi)) if (!/aria-label=|>\s*[^<]+\s*</i.test(match[1]) && !match[2].replace(/<[^>]+>/g, "").trim()) failures.push(`${relative}@${width}: button missing accessible name`);
    if (/<body[^>]*style=[^>]*(?:width|min-width)\s*:\s*(?:1\d{4}|[5-9]\d{3})px/i.test(html)) failures.push(`${relative}@${width}: likely horizontal overflow`);
    if (relative === "videos/index.html") {
      const cards = [...html.matchAll(/<article[^>]*class="[^"]*explainer-card[^>]*>([\s\S]*?)<\/article>/g)];
      if (cards.length !== 4) failures.push(`${relative}@${width}: expected four explainer cards`);
      for (const [, card] of cards) {
        if (!/<video\b[^>]*preload="none"/i.test(card)) failures.push(`${relative}@${width}: video is not preload=none`);
        if (!/<track\b[^>]*kind="captions"/i.test(card)) failures.push(`${relative}@${width}: missing captions track`);
        if (!/data-check-id="explainer-/i.test(card)) failures.push(`${relative}@${width}: missing watched control`);
      }
    }
  }
}
console.log(`Accessibility smoke: ${pages.length} pages × ${widths.length} viewport widths; serious/critical static violations = ${failures.length}.`);
if (failures.length) { for (const failure of failures) console.error(failure); process.exitCode = 1; }
