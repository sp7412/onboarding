import fs from "node:fs";
import path from "node:path";

const root = path.resolve("dist");
const html = fs.readFileSync(path.join(root, "videos/index.html"), "utf8");
const failures = [];
const cards = [...html.matchAll(/<article[^>]*class="[^"]*explainer-card[^>]*>([\s\S]*?)<\/article>/g)].map((m) => m[1]);
if (cards.length !== 4) failures.push(`expected 4 explainer cards, got ${cards.length}`);
for (const [i, card] of cards.entries()) {
  if (!/<video[^>]+preload="none"/.test(card)) failures.push(`episode ${i + 1}: preload`);
  if (!/<track[^>]+kind="captions"/.test(card)) failures.push(`episode ${i + 1}: captions`);
  if (!/poster="[^"]+\/explainers\/[^".]+\.png"/.test(card)) failures.push(`episode ${i + 1}: PNG poster`);
  if (!/data-check-id="explainer-/.test(card)) failures.push(`episode ${i + 1}: watched control`);
}
for (const asset of ["voice-agents-01-anatomy.png", "voice-agents-02-turn-taking.png", "voice-agents-03-architecture.png", "voice-agents-04-control-plane.png"]) {
  if (!fs.existsSync(path.join(root, "explainers", asset))) failures.push(`missing committed poster ${asset}`);
}
if (failures.length) { console.error(failures.join("\n")); process.exit(1); }
console.log("Explainer asset/accessibility smoke: 4 cards, PNG posters, captions, preload=none, watched controls.");
