# Repository Audit

Audit date: 2026-09-30

## Overall Assessment

The repository has a strong teaching spine: the progression from protocol to tools, turn
taking, orchestration, durability, and evaluation is coherent; the fixtures are mostly
deterministic; the generated notebooks are clean; and the site build and internal link
checker pass. It is not yet world-class because several high-value claims and examples are
not current against vendor documentation, the public-safety policy and existing notes are
in tension, the core booking lesson does not enforce slot confirmation, and the full offline
notebook command is not reliable in this environment. The material also lacks a durable
review process, a single canonical source for some metadata, and complete site coverage of
the learning path. Phase 2 should fix correctness and safety first, then consolidate the
path and add durability before expanding site polish.

## Findings

| ID | File(s) | Category | Severity (critical/high/medium/low) | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| A1 | `docs/livekit-hands-on.md`, `labs/src/04_livekit_agents.py` | A: factual accuracy and freshness | high | LiveKit guidance required freshness verification. | Current Agent Builder docs say Builder supports cascaded LiveKit Inference models and does not support realtime-model plugins; the Python quickstart documents CLI/starter/AgentSession/realtime paths. Local examples were checked with `livekit-agents` 1.8.3. | Closed by `60cb6b4`; recheck when the installed SDK or vendor docs change. |
| A2 | `docs/reading-guide.md:118-119` | C: links | medium | Two LiveKit quick-reference links use dead `.md` paths. | The repository bibliography already contains the working trailing-slash routes at `docs/reading-guide.md:66-67`, while the quick-reference table still uses `turns.md` and `telephony.md`. | Use the already verified working routes and rerun the scoped external link check through the proxy. |
| A3 | `docs/speech-to-speech-models.md`, `labs/src/01_realtime_protocol.py` | A, J: factual accuracy and durability | high | OpenAI model claims needed a current verification record. | OpenAI model pages and changelog returned HTTP 403 through the configured proxy on September 30, 2026. The lab remains on `gpt-realtime-2`; numeric claims are explicitly source-attributed and marked unverified rather than guessed. | Closed as a documented verification limitation by `60cb6b4`; manually reverify before relying on prices or limits. |
| A4 | `docs/references.md`, `docs/reading-guide.md`, `docs/whitepaper/claims-ledger.md` and factual docs | J: durability | medium | Review dates were inconsistent across the corpus. | Reverified files now use `Facts as of` and `Last reviewed`; the maintenance guide and weekly workflow define the ongoing convention. | Closed by `60cb6b4` and `6768229`; older unreviewed documents intentionally retain prior dates. |
| A5 | `docs/references.md:15`, `docs/reading-guide.md:22`, `docs/servicetitan-101.md:37` | A/B: factual accuracy and consistency | medium | The product URL is still an older route although the current public site exposes a newer canonical product path. | The old URL resolves, but the current public navigation labels the product differently and uses the newer route. | Verify the canonical URL from the current public site, update references and claims-ledger rows together, and retain redirects only when intentionally documented. |
| A6 | `notes/glossary.md:19`, `docs/whitepaper/10-regulation-and-compliance.md:80-84` | A: factual accuracy | medium | A2P 10DLC wording overgeneralizes registration requirements. | Current provider documentation distinguishes application traffic, provider/carrier scope, and exceptions; the repository says businesses generally must register without that qualification. | Narrow the wording to U.S. application traffic over 10DLC, state that provider/carrier rules and exceptions apply, and update the claims ledger. |
| A7 | `notes/conversation-notes.md`, `AGENTS.md` | I: public safety | high | Notes contained conversation-derived framing that conflicted with the clarified public-safe policy. | Batch 1 rewrote two framing sentences while retaining the learner’s technical notes; `AGENTS.md` now explicitly permits public pre-employment research and forbids employment-derived, confidential, personal, or system-derived material. | Closed by `c1f1c85`. |
| A8 | `labs/stlab/tools.py:81-84,131-143`, `tests/test_stlab.py:38-43`, `docs/livekit-hands-on.md:126-130` | G: labs and code | high | Booking checks address confirmation and offered-slot state but does not enforce explicit slot confirmation. | `CallState` has `slot_confirmed`, but `create_job` does not require it; tests cover missing address confirmation, not missing slot confirmation. | Add a grounded slot-confirmation operation or application-owned state transition, require it in `create_job`, and test missing, changed, and grounded confirmations. |
| A9 | `scripts/run_notebooks.py:27-41`, `requirements.txt`, `labs/README.md:42-49`, `.github/workflows/quality.yml:20-33` | G: labs and code | high | The all-notebook offline command is not robust enough to support the offline-first claim. | The audit run passed notebooks 00–07, then notebook 08 killed the kernel and the runner itself crashed while formatting the exception instead of reporting a controlled failure. The current environment has the listed dependencies installed, so this is not only a missing-package issue. | Fix runner exception handling and isolate/report kernel deaths; add a dependency preflight; rerun all 9 notebooks in CI and locally before closing this finding. |
| A10 | `labs/stlab/backend.py`, `labs/stlab/tools.py`, `tests/test_stlab.py` | G: labs and code | medium | Backend authorization and invariants relied primarily on the tool wrapper. | Backend mutations now validate customer existence, job type, appointment ownership, slot availability/skill, and same-day policy; direct tests cover customer/type/ownership. | Closed by `45b0800`. |
| A11 | `site/src/lib/content/repo.ts:94-107`, `site/src/components/DocBody.astro:23-34`, `site/scripts/check-links.mjs:53-60` | H: site | medium | Markdown fragment links are stripped or not preserved when mapped to site routes. | `repoLinkToRoute` splits off `#fragment`; `DocBody` emits the mapped route without restoring it. The checker can validate anchors only if the renderer preserves them. | Preserve fragments, generate stable heading IDs, and add fixture/tests for mapped links with anchors. |
| A12 | `site/src/components/DocBody.astro:12-16,54-116` | H: site | medium | The custom Markdown renderer loses important document structure. | It does not render H1s, semantic tables, images, nested lists, heading IDs, or language-specific code fences; tables become paragraph rows. | Replace it with a maintained, sanitized Markdown pipeline or expand it with fixtures covering every construct used in repo Markdown. |
| A13 | `site/src/lib/content/labs.ts`, `site/src/lib/content/whitepaper.ts`, `site/src/lib/content/repo.ts` | H/J: site and durability | medium | Parser validation was weaker than the design contract and lab metadata was duplicated. | Parsers now require 00–08, exact 17-chapter order, matching source/notebook sets, and a canonical Time column in `labs/README.md`; tests cover malformed tables. | Closed by `45b0800`. |
| A14 | `site/src/pages/index.astro:70-72,193-216`, `site/DESIGN.md:133-141` | H: site | medium | The home page displays a hard-coded 68% progress ring despite no completed repository checklist state. | The source defines `PRE_START_PCT = 0.68` as a placeholder while the README and checklist remain unchecked. | Render zero/unknown until client state is connected, then derive progress from the checklist’s stable IDs. |
| A15 | `site/src/pages/checklist.astro:60-71` | H: site | medium | Malformed checklist `localStorage` can break initialization. | `JSON.parse(localStorage.getItem(key) ?? "{}")` is not guarded or schema-validated. | Catch malformed data, validate the object shape, preserve valid entries where possible, and add a browser-level regression test. |
| A16 | `site/src/components/SiteHeader.astro`, `site/scripts/check-a11y.mjs` | H: site | low | Mobile navigation lacked complete keyboard and focus behavior. | Menu now moves focus into the first link, closes on Escape and selection, restores focus to the toggle, and keeps `aria-expanded` synchronized. CI runs 5 pages × 2 widths with zero serious/critical static violations. | Closed by `420a45e`. |
| A17 | `README.md`, `plan/30-60-90-checklist.md` | B/F: consistency and learning design | medium | The path had overlapping schedules and time totals. | The checklist now owns a four-week canonical path with 4–6 hour weekly totals, explicit read/watch/listen/run work, and one deliverable per week; README links to it instead of duplicating the schedule. | Closed by `26b570c`. |
| A18 | `docs/capstone-rubric.md`, `labs/README.md`, `plan/30-60-90-checklist.md`, site docs | D/F/H: gaps and learning design | medium | The learning loop lacked one end-to-end acceptance rubric. | Added eight pass/fail criteria covering confirmations, claim grounding, emergency, idempotency, disconnects, same-day policy, and audit evidence; linked from labs/checklist/home and built as `/docs/capstone-rubric/`. | Closed by `26b570c`. |
| A19 | `docs/first-90-days-playbook.md:3-6`, `plan/30-60-90-checklist.md:6-9` | A/C: sourcing | low | “Watkins-inspired” is an uncited attribution. | The documents name a framework but do not identify its public bibliographic source. | Add a real bibliography row after verifying the source, or use an unattributed plain description. |
| A20 | `labs/src/07_langsmith_tracing_evals.py:399-407` | A: factual clarity | low | A future production-looking identifier may be mistaken for real evidence. | The example uses `prod-flag-2026-11-02` while describing a production failure; it is not clearly fictional. | Rename it to an explicitly fictional regression identifier. |
| A21 | `scripts/check_sensitive.py`, `tests/test_sensitive.py`, `AGENTS.md` | I/J: safety and durability | low | Sensitive scanning contract was underdocumented and historical metadata made the check fail. | `AGENTS.md` documents CI-secret/local-file pattern sources; tests cover fake-pattern detection and no-pattern pass; the scanner warns rather than fails on historical non-noreply metadata while still failing on content patterns. | Closed by `c1f1c85`; real CI patterns remain secret-managed and never committed. |

## Top 10 Fixes By Impact

1. Fix and re-run the offline notebook runner so all 9 notebooks produce controlled, meaningful results.
2. Resolve the public-safety policy conflict around employer identifiers and conversation-derived notes before adding more public material.
3. Enforce explicit slot confirmation in the backend/tool state and add regression tests.
4. Revalidate the OpenAI and LiveKit model/API examples through the proxy, update stale examples, and record exact review dates.
5. Replace the two dead LiveKit links and perform a scoped external-link audit over tracked source files only.
6. Establish one canonical pre-start learning path with realistic weekly time and active deliverables.
7. Strengthen parser validation and remove duplicated lab time metadata.
8. Preserve Markdown fragments and improve the renderer’s structural fidelity.
9. Remove misleading hard-coded progress and harden checklist browser storage.
10. Add scheduled link/freshness checks and a short maintenance procedure before expanding site routes.

## Proposed Phase 2 Plan

### Batch 1: Correctness and safety

- Reconcile the public-safe policy and remove or clearly classify conversation-derived material.
- Fix stale/dead LiveKit and product links.
- Revalidate model/API claims and update the claims ledger with current sources and dates.
- Narrow regulatory wording where sources support only a qualified claim.

### Batch 2: Lab correctness

- Repair notebook-runner error handling and run all notebooks offline.
- Enforce slot confirmation and backend invariants.
- Update LiveKit examples against the tested SDK version.
- Add tests for the capstone safety invariants and live-path limitations.

### Batch 3: Canonical learning path

- Make one schedule canonical in README/checklist/site.
- Add prerequisites, time estimates, active checks, and a capstone acceptance rubric.
- Remove or redirect redundant planning material without deleting learner notes.

### Batch 4: Site fidelity

- Preserve Markdown anchors and improve renderer semantics.
- Strengthen parser drift tests.
- Connect progress to checklist state and harden `localStorage`.
- Add accessibility smoke checks and ship only high-value routes justified by the path.

### Batch 5: Durability

- Add `Facts as of` and `Last reviewed` metadata to factual documents.
- Add a weekly non-deploying external-link/freshness workflow using the configured proxy-compatible CI environment.
- Add `MAINTENANCE.md` with monthly model/API, filings, legal, and link review procedures.

## Closure and Verification Record

- Repository worktree was clean before the audit.
- Git identity is `sp7412@users.noreply.github.com`.
- `python scripts/check_repo.py`: passed.
- `python -m unittest discover -s tests -p 'test_*.py'`: 13 passed.
- `ruff check labs/stlab scripts`: passed.
- `python scripts/check_sensitive.py`: passed with warnings for absent custom patterns and historical non-GitHub-noreply metadata.
- `python scripts/run_notebooks.py`: 9/9 passed offline.
- `cd site && npm test`: 45 passed; CI uses frozen Bun install and the same test suite.
- `cd site && npm run build`: passed, 42 pages built.
- `cd site && node scripts/check-links.mjs`: passed, 1,188 internal links checked, broken = 0.
- `cd site && npm run test:a11y`: passed, 5 pages × 2 viewport widths, serious/critical static violations = 0.
- `python scripts/check_external_links.py`: passed, 130 URLs, 0 hard failures; 23 bot-blocked/timeout URLs are explicitly reported UNVERIFIED for human review.
- Batch deploys succeeded for `c1f1c85`, `60cb6b4`, `45b0800`, `420a45e`, `26b570c`, `6768229`, `1778706`, and the renderer correction `7490cd4`.
- Live proxy checks returned the home page, checklist, all navigation pages, and `/docs/capstone-rubric/`; the checklist no longer contains undefined link labels.

The original audit artifact was moved from untracked `AUDIT.md` to this tracked `docs/AUDIT.md` after closure updates. No local build output or tool state was committed.
