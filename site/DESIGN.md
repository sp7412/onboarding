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

### Colors (ServiceTitan-aligned dark UI; validate text pairs against WCAG AA)

This site uses the published ServiceTitan brand palette as its starting point, adapted
for a dark engineering documentation experience. These are official brand hex values,
not a claim that the live marketing site uses this exact dark-mode combination.

| Token | Hex | Role |
|---|---|---|
| `--navy` | `#17191C` | graphite page background (official Darkest) |
| `--panel` | `#22252A` | raised surfaces (official Dark) |
| `--panel-edge` | `#444445` | borders and dividers (official gray neutral) |
| `--blue` | `#0265DC` | primary actions and active path (Titan Blue) |
| `--cyan` | `#6DBAF8` | links, focus indicators, restrained accents (Skyline; legacy token name) |
| `--green` | `#49CC93` | positive status and progress (official Green) |
| `--gold` | `#FFE278` | warning and achievement accents (official Yellow) |
| `--ink` | `#FFFFFF` | primary text (White/Surrender) |
| `--ink-dim` | `#BCBCBD` | secondary text (official gray neutral) |
| `--danger` | `#E24F4F` | critical status (official Critical red) |

Use Titan Blue for primary actions with white labels. Use Skyline for text links and focus
indicators on graphite; reserve the brighter brand colors for status rather than long
paragraphs. Keep the UI flat and calm: no neon cyan, large radial glows, or gradients
behind content. Critical red is best used for icons, borders, and status cues; verify
any red text or filled alert treatment against WCAG AA before shipping. Normal text
should meet 4.5:1 contrast and large text 3:1, per WCAG 2.2 AA. Automated static
contrast checks are a guardrail, not a replacement for rendered-page testing.

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
(cards), `--r3: 20px` (panels). Shadows are avoided for ordinary UI; use borders,
spacing, and restrained color accents to communicate hierarchy.

### Motion

- Feedback: checkbox check draws in 180 ms; "copied" confirmation fades; achievement
  badge appears with a single soft pulse (no confetti).
- All animated content has a text equivalent; captions/text summaries for simulations.

## 3. Information architecture

