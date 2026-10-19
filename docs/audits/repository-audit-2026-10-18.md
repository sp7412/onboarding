# Repository Audit

**Audit date:** October 18, 2026
**Scope:** tracked documentation, labs and generated-notebook consistency, reusable teaching
code and tests, site source and workflows, plus selected vendor documentation. The historical
[September audit](../AUDIT.md) remains a record of its earlier repository state.

## Method

- Read the repository instructions, source/generated-artifact rules, workflows, content parsers,
  and maintained documentation.
- Preserved pre-existing worktree changes: `.gitignore`, `.DS_Store`, and
  `scripts/notebooklm_manual_download.mjs` were not modified by this audit.
- Ran the available Python hygiene, lint, unit, generated-notebook, and offline-notebook checks
  before edits. Reviewed internal links structurally and added targeted regressions for a
  rendered-anchor defect.
- Compared the LiveKit track with the official LiveKit Agents documentation already cataloged in
  `docs/references.md`. OpenAI and Jev pages could not be fetched through this environment
  (HTTP 403/502), so this
  audit did not convert inaccessible pages into new API or model claims.

## Implemented Improvements

- Corrected the authoritative curriculum inventory: the repository has labs `00` through `19`,
  not 17 labs through `16`. README and contributor guidance now describe the full path and the
  correct `20/20` offline suite result.
- Repaired two confirmed internal documentation targets: Templates now points to its directory;
  whitepaper chapter 17 correctly links the technician-feedback notebook as lab 18.
- Fixed the site Lessons progress card to derive all 11 IDs from the canonical lesson dataset.
- Removed a noncanonical hidden podcast anchor. The Markdown renderer now owns the normalized
  anchor, with renderer and built-link-checker regression tests.
- Added the missing optional `JEVMODEL_API_KEY` placeholder to `.env.example`; offline mode still
  strips it and never initiates live calls.
- Restored source traceability for the explainer series after lab-source renames. Added a
  dedicated, optional video-rendering requirements file and a documented ffmpeg preflight.
- Made the LiveKit exercise time estimate distinguish the guided path from validation work, and
  linked its measurement task to the actual latency worksheet.
- Corrected project-site lesson links in the GitHub-rendered checklist.
- Extended the existing weekly external-link source scan to include site Astro/TypeScript sources,
  while excluding test fixtures and URL-processing code.

## Findings

The machine-readable [findings ledger](repository-audit-2026-10-18.json) records ten findings:

| Severity | Count | Resolution |
|---|---:|---|
| P1 | 4 | Fixed and verified |
| P2 | 5 | 4 fixed and verified; 1 rejected after LiveKit research |
| P3 | 1 | Fixed and verified |

No P0 issue was found. The most material deferred gap is test depth for the deliberately
self-contained logic in labs 17–19. Their notebooks pass, but their safety/error branches are
not independently unit-tested. Extracting selected pure helpers into `labs/stlab` before adding
those tests would be a focused follow-up, rather than importing notebook sources directly.

## Verification

Baseline Python checks passed:

```text
.venv/bin/python scripts/check_repo.py                         passed
.venv/bin/python scripts/check_sensitive.py                    passed (expected configuration/history warnings)
.venv/bin/ruff check labs/stlab scripts                        passed
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'  81 passed
.venv/bin/python labs/check_nb.py                              passed
```

The complete offline suite also passed before this documentation/site-only change:

```text
.venv/bin/python scripts/run_notebooks.py                      20/20 passed (offline)
```

The site validation suite passed after installing Bun: `bun run test` completed 131 tests,
`bunx astro check` completed with no errors (two existing unused-code hints), `bun run build`
built 96 pages, the generated-site checker found 0 broken links among 4,099 internal links, and
the accessibility/explainer smoke checks passed. The expanded external-link checker now includes
site source, excludes test fixtures and source templates, and recognizes the documented
bot-protection behavior of Colab, Slack, Jev, and similar source hosts. Confirmed stale
destinations were repaired: the Max map now uses the live ServiceTitan press-release route,
Apple Notes uses current Apple Support documentation, and the Friedman book citation uses its
working Google Books search record. After these repairs and documented bot-protection rules, the
checker completed with 0 hard failures across 520 concrete URLs. The weekly CI workflow remains
the appropriate repeatable full validation path.

## Remaining Risks And Follow-Up

- Treat model names, pricing, and live API snippets as version-sensitive. Revalidate against the
  official docs before a live exercise or dependency upgrade.
- Use the new site-source external-link coverage to detect rot, but investigate bot protection,
  rate limiting, and transient failures manually before changing citations.
- Move a small set of labs 17–19 pure decision helpers into importable teaching modules and add
  negative-path tests for invalid labels, denied release gates, and simulated invariant failures.
- The deployment workflow refreshes market data during deployment rather than through a reviewed
  source update. Consider a reviewed refresh workflow if chart provenance or reproducibility
  becomes more important than same-day data.
