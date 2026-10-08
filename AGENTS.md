# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Cursor, etc.) working in this repo.

## What this repo is

A personal onboarding workspace for a Senior AI Engineer role at ServiceTitan
(start date Oct 26, 2026): a 30/60/90 plan, a voice-agent study guide, blank templates, and
sixteen Jupyter tutorials on the real-time voice-agent stack (OpenAI Realtime, LiveKit,
LangChain/LangGraph, LangSmith) on multi-agent systems built around it (labs 09–14), and on validating an LLM judge (lab 15).

## Hard rules

00. **Never commit tool or machine state.** No `.opencode/`, `.claude/`, `.cursor/`, caches, hostnames,
   internal endpoints, or personal email addresses. Public, pre-employment research about the target
   company—its website, SEC filings, press, and public talks—is allowed and is the purpose of this repo.
   Never add internal or confidential information, anything learned under employment, anything taken from
   a current or former employer's systems, personal data, or secrets. Check `git status` before every commit.
0. **Links must be real.** Link-check every URL you add (HTTP 200 on the final page). Never
   construct URLs from a site's naming pattern. Add new external links to `docs/references.md`.

1. **No secrets.** Never commit `.env`, API keys, tokens, or notebook outputs that contain
   them. Keys belong in `.env` (gitignored); `.env.example` holds empty placeholders only.
2. **Don't commit executed notebook outputs.** Notebooks are stored clean (no outputs).
3. **Offline-first must keep working.** Every notebook must run end to end with no API keys.
   Live-only cells must be gated (e.g. `if stlab.have("openai"):`) and print a skip message.

## Layout

```
README.md                    start-here path + overview + progress table
docs/                        public-source domain and technical study guides
  reading-guide.md           canonical ranked reading/watch list; verify every link before adding entries
  references.md              complete bibliography; add a row for every new external link
  podcast-prompts.md         NotebookLM episode prompts mapped to reading-guide items
  livekit-hands-on.md        LiveKit Agent Builder / lk CLI / mock-tools track
  whitepaper/                background whitepaper: chapters 00–17, appendices A–B, claims-ledger.md
plan/30-60-90-checklist.md   week-by-week checklist (GitHub task-list checkboxes)
study-guide/                 archived source document and pointer to canonical architecture guide
senior-engineer/             judgment-track exercises (fictional scenarios + self-checks); answers stay private
templates/                   blank docs: onboarding log, 1:1 questions, working-with-me,
                             weekly status, field notes, pre-mortem, 30-day memo, design doc,
                             brag document, 90-day retro
notes/                       public-safe notes: glossary, study-question template/model answer
labs/
  00_…15_*.ipynb             generated notebooks, DO NOT hand-edit
  src/*.py                   notebook sources (jupytext "percent" format), EDIT THESE
  build_nb.py                src/*.py → *.ipynb
  stlab/                     shared teaching package (see below)
  solutions/                 offline-safe solution sketches for graded exercises
  agents/                    written by notebook 04 at runtime; gitignored
  data/                      synthetic call dataset (calls/) and CallFacts JSON schema (schemas/)
site/                        Astro site (bun); content parsers in site/src/lib/content
video/                       explainer-series sources (media lives in GitHub releases)
scripts/run_notebooks.py     headless notebook test runner
scripts/check_repo.py        notebook output and generated-file hygiene checks
scripts/check_sensitive.py   configurable sensitive-content and metadata checker
scripts/check_external_links.py, check_release_assets.py   link and release-asset checks
scripts/export_site_sims.py  regenerates the site's guardrail-simulation traces
scripts/fetch_transcripts.py, clean_transcripts.py, podcasts_to_nlm.py   media/podcast tooling
scripts/pre-commit            optional local pre-commit wrapper
tests/                       unittest suites for stlab, labs 09–14, the dataset and scripts;
                             test_sensitive.py uses fake placeholder patterns only
MAINTENANCE.md               review cadence and past audits
requirements.txt, .env.example
.devcontainer/                Codespaces / dev-container definition (Python 3.12, bun, optional key secrets)
.github/workflows/quality.yml  lint, hygiene, offline notebooks, site tests/type-check/build/links (PRs)
.github/workflows/deploy-site.yml, links.yml   site deploy and weekly external link check
```

## Setup and commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd labs && python build_nb.py            # rebuild notebooks after editing labs/src/*.py
cd .. && python scripts/check_repo.py     # generated notebooks present and output-free
python scripts/run_notebooks.py           # run all notebooks offline; must print 16/16 passed
python scripts/run_notebooks.py 02 06    # run a subset by filename prefix
python scripts/run_notebooks.py --live   # use keys from .env (costs money; ask first)
```

## Editing notebooks

- Edit `labs/src/NN_name.py`, never the `.ipynb`. Cells are delimited by `# %%` (code) and
  `# %% [markdown]` (markdown; each line prefixed with `# `).
- After editing: `cd labs && python build_nb.py`, then run the notebook test for that prefix.
- Commit the `src/*.py` change **and** the regenerated `.ipynb` together.
- Run `python scripts/check_repo.py`; committed notebooks must contain no outputs.
- `build_nb.py` adds two cells after each title: an Open in Colab badge and a Colab setup
  cell (a no-op elsewhere). Per-lab Colab packages live in its `COLAB_PACKAGES` map; edit that,
  not the notebooks. The sources stay free of these cells, so the site's parsers are unaffected.
- Top-level `await` is used in notebooks (Jupyter supports it). `%%writefile` cells in 04
  generate `labs/agents/*.py`.

## The `stlab` package (labs/stlab/)

Teaching fixtures, not production code. Keep them small and deterministic.

| Module | Purpose |
|---|---|
| `env.py` | `.env` loader, `have(service)`, `status()`; honors `STLAB_NO_DOTENV=1` |
| `backend.py` | mock home-services backend (customers, slots, seeded appointments A-2001/A-2002, idempotent `create_job` / `reschedule_appointment` / `cancel_appointment`, same-day-change policy, `PolicyError`, `LATENCY_MS`) |
| `tools.py` | Realtime tool schemas, `CallState` (incl. `changes` for claim grounding), guarded `execute_tool` (ownership, offered slots, grounded confirmations) |
| `fake_realtime.py` | offline OpenAI Realtime simulator (GA event names) with a rule-based "brain" |
| `realtime.py` | `connect(live=None)` live-or-fake client, `EventPrinter` |
| `loop.py` | reusable Realtime tool loop |
| `turn_sim.py` | VAD / endpointing / barge-in simulator |
| `scripted_model.py` | fake LangChain chat model with `bind_tools` for offline `create_agent` |
| `booking_graph.py` | LangGraph booking workflow + `advance()` helper |
| `scenarios.py` | eval dataset used by notebooks 07–08 (booking, reschedule, cancel, emergencies) |
| `context.py`, `coordination.py`, `learning.py`, `agent_gateway.py` | multi-agent labs 09–12: context ledger, arbitration, learning loop, agent-to-agent gateway |
| `calls.py` | shared synthetic call dataset for labs 13–14; `python -m stlab.calls` regenerates `data/calls/calls-v1.jsonl` (a test checks it matches) |
| `minimax.py` | lab 13: `CallFacts` contract (`data/schemas/call-facts.schema.json`), noisy extractor, bookability, commit, dispatch, claim guard, error sensitivity |
| `autonomy.py` | lab 14: Wilson promotion/demotion, SPRT, cost thresholds, calibration, PSI/OOD drift guard |
| `judge.py` | lab 15: bookability judge rubrics and JSON contract, `OpenAIJudge` (live) and `ScriptedJudge` (offline, deliberate flaws), kappa/agreement, evidence grounding, abstention sweep, pairwise position-bias test |

Conventions: the simulators must emit the same event/field names as the real APIs; if you
change the fake brain or backend, re-run notebooks 01, 02, 07, and 08 (they depend on
specific scripted behavior, e.g. the "early `create_job`" guardrail demo).

## Versions

Tested against livekit-agents 1.8.x, langchain 1.4, langgraph 1.x, langsmith 0.14, and the
GA Realtime event protocol with `gpt-realtime-2`. Vendor APIs move fast; when updating, check
the vendor docs, fix imports, and re-run the full offline suite.

## Markdown and checklists

- `plan/30-60-90-checklist.md` uses GitHub task lists (`- [ ]`); check items by changing to
  `- [x]`. Don't reorder or renumber weeks without being asked.
- Update the progress table in `README.md` when a phase completes.
- Keep prose plain and concise; no internal company details (see Hard rules).
- Never check boxes, fill in "my answer" sections, or write first-person reflections on
  the user's behalf. These are personal progress records and must be completed by the user.

## Quality checks

- `ruff check labs/stlab scripts` lints the deterministic teaching package and scripts.
- `python scripts/check_repo.py` checks that generated notebooks exist and contain no
  execution outputs.
- `python scripts/check_sensitive.py` scans tracked files and commit metadata using
   `SENSITIVE_PATTERNS` or ignored `.sensitive-patterns`; it never hard-codes employer
   names or domains.
- Sensitive scanning patterns come from the `SENSITIVE_PATTERNS` repository secret in CI or the local,
  gitignored `.sensitive-patterns` file. Real patterns are never committed; tests use fake placeholders only.
- Install the optional local hook with `ln -s ../../scripts/pre-commit .git/hooks/pre-commit`.
- `.github/workflows/quality.yml` runs these checks and the offline notebook suite on
  every push and pull request. It never uses secrets or `--live`.

## Commits

Small, focused commits with imperative messages (e.g. "Fix barge-in timing in fake realtime").
Run the offline notebook suite before committing any change under `labs/`.

## Site simulations data

The Guardrails simulation on the site replays recorded runs of `labs/stlab`. After changing
`labs/stlab/fake_realtime.py`, `tools.py`, `backend.py` or `scenarios.py`, run
`python scripts/export_site_sims.py` and commit the updated `site/src/data/guardrail-traces.json`.


## Day-one public-repo boundary

The start date is October 26, 2026. From that date forward this repository is a frozen,
sanitized pre-start guide. Never add anything learned inside the company: internal architecture,
code, metrics, traces, customer data, recordings, hostnames, endpoints, credentials, prompts,
or incidents. Put that material in company systems or an approved private location. Post-start
changes are limited to genuinely public, verified sources and public-safe improvements to the
synthetic teaching labs. See docs/after-day-one.md.
