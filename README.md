# ServiceTitan Onboarding

My personal onboarding workspace for the Senior AI Engineer role at ServiceTitan
(start date: October 26, 2026). It holds the 30/60/90 plan, a study guide for the
real-time voice-agent stack, hands-on tutorial notebooks, and templates for the
documents I'll write along the way.

> **Keep this repo public-safe.** Nothing here should contain ServiceTitan internal
> information: no internal architecture, code, metrics, customer data, or call
> recordings. Internal notes belong in company systems. This repo is for my own
> learning, public material, and blank templates.

## Layout

| Path | What's there |
|---|---|
| [`plan/30-60-90-checklist.md`](plan/30-60-90-checklist.md) | Week-by-week checklist from pre-start through day 90 |
| [`study-guide/`](study-guide/) | Voice-agent study guide (Markdown + original .docx) |
| [`labs/`](labs/) | Nine Jupyter tutorials: OpenAI Realtime, LiveKit, LangChain/LangGraph, LangSmith, capstone |
| [`templates/`](templates/) | Onboarding log, 1:1 questions, weekly status, 30-day memo, design doc, 90-day retro |
| [`notes/`](notes/) | Public-safe personal notes: glossary, study-question answer |

## Getting started with the labs

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # optional; every notebook runs offline without keys
cd labs && jupyter lab
```

Work through `00` → `08` in order. See [`labs/README.md`](labs/README.md) for details.

## Progress

| Phase | Status |
|---|---|
| Pre-start (→ Oct 25) | ⬜ |
| Days 1–30 | ⬜ |
| Days 31–60 | ⬜ |
| Days 61–90 | ⬜ |
