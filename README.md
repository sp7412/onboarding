# ServiceTitan Onboarding

My personal onboarding workspace for a Senior AI Engineer joining a voice-agent / AI
team at ServiceTitan (start date: October 26, 2026). It holds a public-source domain
primer, a 30/60/90 plan, a study path for the real-time voice-agent stack, hands-on
tutorial notebooks, and templates for the documents I'll write along the way.

> **Keep this repo public-safe.** Nothing here should contain ServiceTitan internal
> information: no internal architecture, code, metrics, customer data, or call
> recordings. Internal notes belong in company systems. This repo is for my own
> learning, public material, and blank templates.

## Start Here

The path assumes an experienced ML or signal-processing engineer who is new to
contractor software and production voice agents. It is designed for roughly 5–7 hours
per week before the start date. Use only personal accounts for optional live exercises;
the complete path is useful offline.

| Week | Time | Focus | Deliverable |
|---|---:|---|---|
| Sept 28 | 4–6 h | Reading guide items 1–4; read [`docs/servicetitan-101.md`](docs/servicetitan-101.md), [`docs/how-a-contractor-works.md`](docs/how-a-contractor-works.md), and labs 00–03 | Explain the contractor job lifecycle and draw the control-plane boundary |
| Oct 5 | 5–7 h | Reading guide items 5–10; read [`docs/voice-agent-architecture.md`](docs/voice-agent-architecture.md), then labs 04–06 | Compare cascaded and realtime paths; demonstrate guarded booking and resume |
| Oct 12 | 4–6 h | Reading guide items 11–14; read [`docs/evaluating-voice-agents.md`](docs/evaluating-voice-agents.md), then labs 07–08 | Produce a small eval report and complete the study-question answer |
| Oct 19 | 3–5 h | Review [`docs/reading-list.md`](docs/reading-list.md), [`docs/first-90-days-playbook.md`](docs/first-90-days-playbook.md), and templates | Prepare manager questions, a first-PR hypothesis, and a measurable 30-day plan |

For each lab, read the objective first, run the offline cells, do the understanding
questions without looking at the answer key, then attempt the graded exercise. The
notebooks use fictional data only. Start with [`labs/README.md`](labs/README.md) for
the exact lab map and prerequisites.

## Layout

| Path | What's there |
|---|---|
| [`plan/30-60-90-checklist.md`](plan/30-60-90-checklist.md) | Week-by-week checklist from pre-start through day 90 |
| [`study-guide/`](study-guide/) | Voice-agent study guide (Markdown + original .docx) |
| [`docs/`](docs/) | Public-source domain primer, technical architecture, reading list, evaluation guide, and first-90-days playbook |
| [`docs/reading-guide.md`](docs/reading-guide.md) | Ranked blogs, papers and talks with four takeaways each (start here for reading) |
| [`docs/references.md`](docs/references.md) | Complete bibliography of every external source in the repo |
| [`docs/podcast-prompts.md`](docs/podcast-prompts.md) | Five NotebookLM podcast prompts for review listening |
| [`docs/livekit-hands-on.md`](docs/livekit-hands-on.md) | LiveKit track: Agent Builder → `lk` starter → fake ServiceTitan tools with guardrails |
| [`labs/`](labs/) | Nine Jupyter tutorials: OpenAI Realtime, LiveKit, LangChain/LangGraph, LangSmith, capstone |
| [`labs/solutions/`](labs/solutions/) | Offline-safe solution notes for the lab exercises |
| [`templates/`](templates/) | Onboarding log, 1:1 questions, weekly status, 30-day memo, design doc, 90-day retro |
| [`notes/`](notes/) | Public-safe personal notes: original conversation notes, glossary, study-question answer |
| [`scripts/run_notebooks.py`](scripts/run_notebooks.py) | Headless test runner: executes the notebooks offline |
| [`AGENTS.md`](AGENTS.md) | Instructions for AI coding agents working in this repo (`CLAUDE.md` points to it) |

## Getting Started With The Labs

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # optional; every notebook runs offline without keys
cd labs && jupyter lab
```

Work through `00` → `08` in order. See [`labs/README.md`](labs/README.md) for details.

To run the offline test suite without activating the environment:

```bash
.venv/bin/python scripts/run_notebooks.py
```

Never use `--live` in CI. Live runs can cost money and must use personal credentials
and fictional data.

## Progress

| Phase | Status |
|---|---|
| Pre-start (→ Oct 25) | ⬜ |
| Days 1–30 | ⬜ |
| Days 31–60 | ⬜ |
| Days 61–90 | ⬜ |

Progress is intentionally manual. Check off the corresponding items in
[`plan/30-60-90-checklist.md`](plan/30-60-90-checklist.md) as work is completed.
