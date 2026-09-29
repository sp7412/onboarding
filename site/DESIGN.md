# Onboarding: The Path to Integration — design plan (Phase 0)

A static Astro site in `/site`, deployed to GitHub Pages
(`https://sp7412.github.io/onboarding/`), that turns this repo's Markdown into a
game-like journey from pre-start through day 90. The Markdown stays the single source
of truth: every fact, task, reading, episode, chapter and lab is parsed at build time.
The site never duplicates repo content by hand.

## 1. Tech choices

**Astro (static output) with vanilla-TS islands.** Reasons:

- Zero JS by default fits the < 300 KB JS budget and the Lighthouse ≥ 90 targets.
  Progress and simulations need interactivity, but only in small, per-page islands
  (Preact would add a ~4 KB runtime for state we can hold in plain TS; the islands
  here are form-heavy, not component-tree-heavy).
- Astro's content pipeline makes "parse the repo Markdown at build time" a first-class
  feature (`getCollection`, glob loaders) and the build fails loudly on malformed
  sources — which is a hard requirement.
- GitHub Pages is the deploy target; a fully static `dist/` is all we need.

Fonts are self-hosted via `@fontsource` npm packages (OFL-licensed), no Google Fonts
calls. Simulations are pure TS functions (ported from `labs/stlab`) with unit tests,
plus thin DOM bindings.

**Build-time data flow:**

```
repo Markdown / lab sources
        │  Astro glob loader (site/src/lib/content/*.ts)
        ▼  validate + parse → typed records (zod-like hand validation)
site/src/content/*.json (generated at build time, never committed)
        ▼
Astro pages render SSR-at-build; islands receive serialized props
```

Parse functions are plain TS modules with their own unit tests (Vitest) run against
fixture files under `site/src/lib/content/__fixtures__/`. If a source file's shape
changes (missing heading, missing table, no `- [ ]` items in a week), the build fails
with the file name and the expectation that broke.

## 2. Design tokens

### Colors (WCAG AA on all text; contrast ratios against `--navy` base unless noted)

| Token | Hex | Role |
|---|---|---|
| `--navy` | `#0A1224` | page background (base) |
| `--panel` | `#111C33` | cards, deep panels |
| `--panel-edge` | `#1E2C4F` | borders, dividers |
| `--blue` | `#3E7BFF` | electric blue: primary actions, active path |
| `--cyan` | `#37E0FF` | cyan glow: highlights, focus, links |
| `--green` | `#4ADE80` | success: progress rings, checked items (AA on navy for text ≥ 16px; use `#2FA860`-darkened fills behind white text) |
| `--gold` | `#F5C044` | warm gold: achievements, trophy |
| `--ink` | `#E8EEFA` | body text on navy (14.8:1) |
| `--ink-dim` | `#A8B5D1` | secondary text (7.4:1) |
| `--danger` | `#FF7A6B` | failure states in simulations (5.6:1) |

Text never sits on raw gradients; if a glow sits behind text it is at ≤ 12% opacity or
backed by `--panel`. Buttons: `--blue` fill with `#FFFFFF` text (4.6:1). Links: `--cyan`
on navy (11.6:1).

### Type (two OFL options, self-hosted; decision in Phase 1 after rendering both)

- **Option A — headings "Space Grotesk", body "IBM Plex Sans".** Space Grotesk has a
  technical, engineered voice that matches circuit-trace art; IBM Plex Sans is quiet and
  very legible at small sizes on phones.
- **Option B — headings "Chakra Petch", body "Inter".** Chakra Petch is more overtly
  sci-fi/HUD; riskier for long sessions, strong for a game feel.

Both are OFL on Google Fonts and packaged as `@fontsource/*`. Proposal: **Option A** for
readability across a 90-day journey, with Chakra Petch reserved for the hero title only.
Sentence case everywhere; no all-caps eyebrow labels.

### Spacing scale

4-point scale: `--s1: 4px · --s2: 8px · --s3: 12px · --s4: 16px · --s6: 24px ·
--s8: 32px · --s12: 48px · --s16: 64px`. Radii: `--r1: 6px` (inputs), `--r2: 12px`
(cards), `--r3: 20px` (panels). One shadow: `0 0 24px rgba(55,224,255,.18)` reserved
for the active journey node and focused elements.

### Motion

- **Signature moment:** on home load, the journey path draws itself left → right
  (SVG stroke-dash animation ~1.2 s), stage rings fill to their current progress, and
  the "next step" node pulses once. Runs once per visit; skipped under
  `prefers-reduced-motion` (path renders already-drawn).
- Feedback: checkbox check draws in 180 ms; "copied" confirmation fades; achievement
  badge appears with a single soft glow pulse (no confetti).
- All animated content has a text equivalent; captions/text summaries for simulations.

## 3. Information architecture

```
/                     Journey map (home): five stages, progress, next actions
/checklist            Week-by-week tasks from plan/30-60-90-checklist.md
/reading              Reading guide: ranked cards, tier + lab filters
/podcasts             Podcast studio: episodes in listening order, copy block
/whitepaper           Whitepaper reader: chapters, essentials path
/whitepaper/[chapter] Chapter view
/architecture         Architecture explorer
/simulations/turn-taking      Turn-taking lab sim
/simulations/guardrails       Guardrail call simulator
/simulations/latency          Latency budget builder
/templates            Templates: readable + copy-to-clipboard
/glossary             Flashcards + stage quizzes
/labs                 Labs launcher
/achievements         Badge wall (also surfaced on home)
/about                About this site: privacy, data, public-safe rule
```

Global nav (persistent header): Journey · Checklist · Reading · Podcasts · Whitepaper ·
Architecture · Simulations · Glossary · Labs · Templates · About. On mobile the header
collapses to "Journey" + a hamburger sheet. The persistent **"Continue"** button
always reads the next unchecked item and deep-links to it — it lives in the header on
every page including home.

**Stages** (the five journey nodes): pre-start (Sept 28–Oct 25) → days 1–30 →
days 31–60 → days 61–90 → done (trophy). Progress per stage = weighted fraction of
checked checklist items in that stage (readings/podcasts count through the checklist
items that reference them, so one canonical number, no double counting).

## 4. Wireframes

### Home (journey map)

```
┌────────────────────────────────────────────────────────────────────┐
│ [logo/circuit mark]  ONBOARDING: THE PATH TO INTEGRATION   [Continue ▸]│
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   ┌─ hero banner SVG: circuit traces → bright central node ─────┐  │
│   │  "From first call to day 90."   total progress: 42%  ▓▓▓░░  │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  [ Continue where I left off → next unchecked item title + link ]  │
│                                                                    │
│   JOURNEY MAP (SVG background: rising stepped path, figures)       │
│                                                                    │
│   ●pre-start──▶●days 1–30──▶●days 31–60──▶●days 61–90──▶🏆done     │
│   (ring 68%)    (ring 0%)     (ring 0%)     (ring 0%)   (locked)   │
│                                                                    │
│  ▾ under the ACTIVE stage node:                                    │
│  ┌ Next three actions ──────────────────────────────────────────┐  │
│  │ ☐ Read the domain primer and contractor lifecycle  (45 min)  │  │
│  │ ☐ Run labs 00–03 offline with Python 3.12          (2 h)     │  │
│  │ ☐ Write one question each for customer, product…             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  [badges earned: 🥇 first lab] [stage quizzes: 2/5]  → achievements │
└────────────────────────────────────────────────────────────────────┘
```

### A content page (reading guide as the example)

```
┌────────────────────────────────────────────────────────────────────┐
│ nav …                                              [Continue ▸]    │
├────────────────────────────────────────────────────────────────────┤
│ Reading guide (h1)            filters: [tier 1|2|3|4] [pairs with ▾]│
│ ┌ card ──────────────────────────────────────────────────────────┐ │
│ │ 1 · ServiceTitan AI Voice Agent product page   [tier 1] 15 min │ │
│ │ why: this is the product you're joining …                      │ │
│ │ look for:  □ booking is driven by capacity rules …             │ │
│ │            □ explicit escalation path …                        │ │
│ │ pairs with: lab 02 ·  □ mark done                              │ │
│ └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

The four "look for" items render as reflection prompts (checkboxes, saved locally).
Marking the card done is one control; per-prompt checks are optional finer grain.

### One simulation (turn-taking)

```
┌────────────────────────────────────────────────────────────────────┐
│ Turn-taking simulator        (simulation — mirrors labs/stlab/turn_sim)│
├────────────────────────────────────────────────────────────────────┤
│ scenario: [phone number read slowly ▾]                             │
│ ┌ timeline (SVG) ────────────────────────────────────────────────┐ │
│ │ speech prob curve · VAD band · commits ▼ (red = premature)     │ │
│ └────────────────────────────────────────────────────────────────┘ │
│ VAD threshold 0.50 ──────●────   endpointing 500 ms ────●──        │
│ semantic detection [off] · eou accuracy 0.90 ──●──                 │
│ ┌ results ───────────────────────────────────────────────────────┐ │
│ │ premature cut-offs: 2   missed turns: 0   mean response gap:    │ │
│ │ 1180 ms        verdict: "the agent keeps cutting the caller off │ │
│ │ mid-number — raise endpointing or turn on semantic detection"   │ │
│ └────────────────────────────────────────────────────────────────┘ │
│ quiz: "why does a longer silence timer alone hurt?" [reveal]       │
└────────────────────────────────────────────────────────────────────┘
```

Sliders drive a pure `simulateTurnTaking(options)` function; the SVG is a render of
its output. Same function = unit-tested against the Python results.

## 5. Art plan (original SVG, `site/src/assets/brand/`)

All art is hand-authored SVG, original, no logos/trademarks/stock. Text baked in only
on the hero title. Files:

| File | Content (sketch in words) |
|---|---|
| `hero-banner.svg` | Wide 1440×480: deep navy field; 5 circuit traces enter from the left edge with elbow bends, cross small via-pads, and converge into a large bright central node (concentric cyan rings, soft glow) right of center; faint grid dots; the hero title is the only text. Small figure silhouettes omitted here — they live on the map. |
| `journey-map-bg.svg` | 1440×760: a stepped rising path from bottom-left to top-right, drawn as parallel glowing lines (electric blue core, cyan halo) with rounded switchbacks like a PCB trace; faint horizontal scan lines; subtle vignette so foreground nodes pop. Node positions are fixed anchors the home page overlays. |
| `icon-*.svg` ×16 | Circular badges, 96×96, ring + glyph: plan (clipboard), labs (flask), reading (book), podcasts (mic), whitepaper (document), templates (layers), notes (pencil), glossary (abc-cards), architecture (nodes-and-edges), guardrails (shield), evaluation (checklist-in-target), latency (stopwatch), telephony (handset), compliance (scales), milestone (flag), trophy. Glyphs stroke-based, 2.5 px, cyan/blue on panel circle; gold variant class for earned state. |

Icon set covers: plan, labs, reading, podcasts, whitepaper, templates, notes, glossary,
architecture, guardrails, evaluation, latency, telephony, compliance, milestone, trophy
(16 total). Each has `role="img"` + `<title>` alt text in the SVG and decorative
instances get `aria-hidden`. A small climbing-figures motif (3 simple silhouettes at
different heights) is drawn inline in the journey map component, not a separate asset,
so it can be aria-hidden consistently.

## 6. Parsing plan per source file

Every parser: strict shape validation, fail with `file + expectation` on drift, tested
against committed fixtures (small excerpts copied into `__fixtures__`).

| Source | Extracts | Approach / failure mode |
|---|---|---|
| `plan/30-60-90-checklist.md` | stage/week sections (`### Week …`, `## Days …`, `## Pre-Start…`), items as `- [ ]` lines (multi-line joined), week titles, day-30/60/90 exit-criteria groups, `**Output:**` lines as week outcomes | Split by `## ` then `### `; regex `- \[( |x)\] `. Fail if any stage has zero weeks or a week zero items. Stable IDs: `chk-<stage>-<weekslug>-<hash8(item text)>`. Links inside items are rewritten to internal routes where a doc maps to a site page. |
| `docs/reading-guide.md` | tier sections (Tier 1–4), numbered items `### N. Title`, `- [ ] <url> · type · time`, **Why**, **Look for** (4 numbered), **Pairs with** | Line scanner; treat "### Official documentation quick reference" table as Tier 2 sub-items (one card per row). Fail if an item lacks url/time/why or a tier heading is missing. IDs: `read-<n>-<hash8(title)>`. |
| `docs/podcast-prompts.md` | `## Episode N: Title` blocks in **file order** (listening order), the `- [ ] Generated · [ ] Listened · **When:**` line, and the fenced ` ```text ` block verbatim | Capture fence content exactly (copy button = sources + prompt). Fail if a block has no fence or no checkboxes. IDs: `pod-<epnum>-<hash8(title)>`. |
| `docs/whitepaper/*.md` | chapter number from filename, title from H1, `**Estimated reading time:**`, essentials-path flags (00,01,02,06,07,10,11,14 from README), takeaways (H2 "Five Takeaways" list) | Filename pattern `NN-slug.md`; fail on missing reading time or title. Order per whitepaper README. IDs: `wp-<NN>`. |
| `docs/*.md` (docs pages) | H1 title, estimated time if present, section list for in-page nav | Rendered as readable doc pages (architecture, call anatomy, servicetitan-101, how-a-contractor-works, evaluating-voice-agents, livekit-hands-on, first-90-days-playbook). |
| `templates/*.md` | title + body | Rendered verbatim below a copy button. IDs: `tmpl-<slug>`. |
| `notes/glossary.md` | term/meaning table rows | Pipe-table parser; fail on rows without 2 cells. IDs: `glos-<hash8(term)>`. |
| `labs/src/*.py` | notebook title from first `# %% [markdown]` H1 (`# NN · Title`), objective/first paragraph, "Where it stops"/**Goal** line, `## Check your understanding` questions, `**Graded exercise:**` text, time estimate from labs README table (30–60 / 60–90 min) | Percent-format cell splitter (`# %% [markdown]` / `# %%`). Fail if a file has no markdown H1 or no "Check your understanding". IDs: `lab-<NN>`. |
| `labs/stlab/turn_sim.py`, `tools.py`, `backend.py`, `scenarios.py` | Not parsed for content — ported as TS logic (simulations), with unit tests comparing TS vs the Python fixtures' expected outputs recorded in tests. Scenario texts for the guardrail sim come from `labs/stlab/scenarios.py` via a committed fixture (utterances/expected outcomes) so the TS and Python stay visibly paired. |

**Quiz content:** stage quizzes draw from labs' "Check your understanding" questions
(parsed, above). Those are open-ended in the repo; the site presents each question as a
reflection prompt with a "reveal key idea" toggle derived from the matching
`solutions/NN_*.md` section headings — no fabricated multiple-choice answers in
Phase 0 scope; multiple-choice authoring is deferred to the "later" list to avoid
paraphrasing repo content.

## 7. How features serve success criteria 1–5

| Feature | 1 first action <60 s | 2 visible progress | 3 pre-start fit, phone-first | 4 active checks | 5 zero-friction return |
|---|---|---|---|---|---|
| Journey map home | **Primary:** "Continue where I left off" at top with the next item's title; next three actions under the active node | progress rings update instantly on every toggle | stage layouts are single-column on mobile; map scrolls vertically | — | Continue button = next unchecked item |
| Checklist | linked from journey stages ("what to do next") | per-stage bars, check animation | weeks are short task lists, fine on a phone (labs flagged "needs laptop") | checkboxes are the base layer | persists via localStorage IDs |
| Reading guide | checklist items deep-link to filtered view | done toggle + per-prompt checks | cards stack; time estimates visible up front | the four takeaways become reflection prompts | — |
| Podcast studio | week items link to the episode | generated/listened toggles | copy-one-tap flow is phone-friendly (NotebookLM on phone) | listened toggle is itself the check | — |
| Whitepaper reader | checklist + reading links | mark chapter read; essentials path highlighted | reader is a single column with prev/next | essentials path = bounded 2 h path | chapter position remembered |
| Architecture explorer | reachable from week-of-Oct-5 items | — | tap layers instead of hover | one quiz question per layer; ends at the learner's own study-question page (never pre-filled) | — |
| Simulations | labs checklists link "try the idea first" | completion state per sim | portrait-friendly stacked controls | each sim ends with an interpretive question | — |
| Glossary flashcards/quizzes | — | quiz score per stage | swipeable cards | quizzes per stage | — |
| Templates | — | copy events tracked as done | — | copying is the action | — |
| Achievements | badge hint on home | — | — | milestones = proof of stages | — |
| Labs launcher | "run locally" commands with copy buttons | per-lab done flag | reading/understanding on phone; running needs laptop (stated) | links to sim versions for phone | — |

## 8. Later list (explicitly cut from scope)

- Multiple-choice quiz authoring beyond parsed reflection prompts (risk of paraphrasing
  repo content; revisit if the learner wants scoring).
- Accounts/sync, analytics, comments, search-as-you-type across all content.
- Leaderboards, streaks, daily notifications.
- A "phone wallpaper" progress export.
- Dark/light theme toggle (the site is dark-only by design).
- Localization.

## 9. Risks and mitigations

1. **Parser drift when repo Markdown changes** → strict validators that fail the build
   with file+expectation; fixtures per source; CI runs site build on every push.
2. **JS budget** on whitepaper + simulations pages → render prose at build; islands
   lazy-loaded; budget check in CI (per-page JS < 300 KB, target < 120 KB).
3. **Repo-coupled relative links** (`../docs/…`) inside parsed Markdown → link-rewrite
   map (doc path → site route) in the content pipeline; unresolved links fail the build.
4. **Public-safe rule** → no new external links beyond what sources already contain;
   any added link goes through `docs/references.md` per AGENTS.md. No employer-internal
   content; the About page repeats the rule.
5. **GitHub Pages asset paths** → `site` config uses `base: '/onboarding'`; asset URLs
   via Astro helpers only; workflow deploys `site/dist` with the official
   `actions/deploy-pages` flow and a `gh.io`-Pages-concurrency group.
6. **Sim fidelity** → TS ports tested against expected outputs recorded from the Python
   modules (same inputs → same outcomes documented in test fixtures); sim pages are
   labeled "simulation, mirrors the lab".
7. **Phone-first for labs** → labs launcher is explicit that running needs a laptop;
   reading/objectives/quiz parts are phone-friendly.

## 10. Self-review against the brief

Re-read after drafting. Fixes made:

- Draft called the "next three actions" list "roadmap" — renamed to plain "Next three
  actions"; the home must state *exactly* what to do next, not a second taxonomy. Now
  the journey's only next-step concept is the single "Continue" item + three actions.
- Draft had separate progress for readings vs checklist — merged into one canonical
  checklist-derived number per stage to avoid two sources of truth for progress.
- The glossary quiz idea read as generic trivia; cut multiple-choice scoring to the
  later list and kept parsed reflection prompts + stage quizzes sourced from the labs'
  own questions.
- Wireframe hero title used all-caps eyebrow text — removed; sentence case everywhere.
