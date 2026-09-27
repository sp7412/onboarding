# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Cursor, etc.) working in this repo.

## What this repo is

Seth Patterson's personal onboarding workspace for a Senior AI Engineer role at ServiceTitan
(start date Oct 26, 2026): a 30/60/90 plan, a voice-agent study guide, blank templates, and
nine Jupyter tutorials on the real-time voice-agent stack (OpenAI Realtime, LiveKit,
LangChain/LangGraph, LangSmith).

## Hard rules

0. **Links must be real.** Link-check every URL you add (HTTP 200 on the final page). Never
   construct URLs from a site's naming pattern. Add new external links to `docs/references.md`.

1. **This repo is public.** Never add ServiceTitan internal information: internal code,
   architecture, metrics, customer data, call recordings or transcripts, names of internal
   systems, or anything learned under employment. If a request would add such content, stop
   and ask. Public sources (product pages, conference talks, vendor docs) are fine.
2. **No secrets.** Never commit `.env`, API keys, tokens, or notebook outputs that contain
   them. Keys belong in `.env` (gitignored); `.env.example` holds empty placeholders only.
3. **Don't commit executed notebook outputs.** Notebooks are stored clean (no outputs).
4. **Offline-first must keep working.** Every notebook must run end to end with no API keys.
   Live-only cells must be gated (e.g. `if stlab.have("openai"):`) and print a skip message.

## Layout

```
README.md                    start-here path + overview + progress table
PLAN.md                      audit and improvement plan
docs/                        public-source domain and technical study guides
  reading-guide.md           ranked reading/watch list; verify every link before adding entries
  references.md              complete bibliography; add a row for every new external link
  podcast-prompts.md         NotebookLM episode prompts mapped to reading-guide items
  livekit-hands-on.md        LiveKit Agent Builder / lk CLI / mock-tools track
plan/30-60-90-checklist.md   week-by-week checklist (GitHub task-list checkboxes)
study-guide/                 study guide (.md generated from the .docx; both committed)
templates/                   blank docs: onboarding log, 1:1 questions, weekly status,
                             30-day memo, design doc, 90-day retro
notes/                       public-safe notes: glossary, study-question answer
labs/
  00_…08_*.ipynb             generated notebooks, DO NOT hand-edit
  src/*.py                   notebook sources (jupytext "percent" format), EDIT THESE
  build_nb.py                src/*.py → *.ipynb
  stlab/                     shared teaching package (see below)
  solutions/                 offline-safe solution sketches for graded exercises
  agents/                    written by notebook 04 at runtime; gitignored
scripts/run_notebooks.py     headless notebook test runner
scripts/check_repo.py        notebook output and generated-file hygiene checks
requirements.txt, .env.example
.github/workflows/quality.yml  lint, hygiene, and offline notebook CI
```

## Setup and commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd labs && python build_nb.py            # rebuild notebooks after editing labs/src/*.py
cd .. && python scripts/check_repo.py     # generated notebooks present and output-free
python scripts/run_notebooks.py           # run all notebooks offline; must print 9/9 passed
python scripts/run_notebooks.py 02 06    # run a subset by filename prefix
python scripts/run_notebooks.py --live   # use keys from .env (costs money; ask first)
```

## Editing notebooks

- Edit `labs/src/NN_name.py`, never the `.ipynb`. Cells are delimited by `# %%` (code) and
  `# %% [markdown]` (markdown; each line prefixed with `# `).
- After editing: `cd labs && python build_nb.py`, then run the notebook test for that prefix.
- Commit the `src/*.py` change **and** the regenerated `.ipynb` together.
- Run `python scripts/check_repo.py`; committed notebooks must contain no outputs.
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

## Quality checks

- `ruff check labs/stlab scripts` lints the deterministic teaching package and scripts.
- `python scripts/check_repo.py` checks that generated notebooks exist and contain no
  execution outputs.
- `.github/workflows/quality.yml` runs these checks and the offline notebook suite on
  every push and pull request. It never uses secrets or `--live`.

## Commits

Small, focused commits with imperative messages (e.g. "Fix barge-in timing in fake realtime").
Run the offline notebook suite before committing any change under `labs/`.
