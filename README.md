# ServiceTitan Onboarding

My personal onboarding workspace for a Senior AI Engineer joining a voice-agent / AI
team at ServiceTitan (start date: October 26, 2026). It holds a public-source domain
primer, a 30/60/90 plan, a study path for the real-time voice-agent stack, hands-on
tutorial notebooks, and templates for the documents I'll write along the way.

> **Keep this repo public-safe.** Nothing here should contain ServiceTitan internal
> information: no internal architecture, code, metrics, customer data, or call
> recordings. Internal notes belong in company systems. This repo is for my own
> learning, public material, and blank templates.

## Start here in 5 minutes

1. Read [`docs/servicetitan-101.md`](docs/servicetitan-101.md) (5 min) — what the company does and the
   mental model: a voice agent inside a contractor's booking workflow, not a chatbot.
2. Skim [`plan/30-60-90-checklist.md`](plan/30-60-90-checklist.md) "Pre-Start" (3 min) — this week's
   concrete tasks; the `site/` folder builds them into an interactive checklist.
3. Do reading-guide [item 1](docs/reading-guide.md) (15 min) — the AI Voice Agent product page, with
   four things to look for.
4. Open [`notes/study-question.md`](notes/study-question.md) (1 min) — the one question everything
   else builds toward answering.

Reading on a phone works for steps 1–4; labs need a laptop. After that, follow the weekly
path below.

## Short on time?

Start with the [10-hour minimum path](docs/minimum-path.md). It is the fastest route from the Pantheon 2026 system model to labs 13–14, business value, field observations, and manager alignment.

## The Full Path

The path assumes an experienced ML or signal-processing engineer who is new to contractor
software and production voice agents. Follow the single, canonical four-week schedule in the
[`Pre-Start canonical path`](plan/30-60-90-checklist.md#canonical-pre-start-path) (4–6 hours
per week). Use only personal accounts for optional live exercises; the complete path is useful
offline. Finish with the [`capstone rubric`](docs/capstone-rubric.md).

Alongside the labs, the [senior engineer judgment track](senior-engineer/README.md) has eight
short written exercises (about five and a half hours in total) on denominators, bookability judging,
incident diagnosis, latency budgets, architecture boundaries and choosing a first PR.

For each lab, read the objective first, run the offline cells, do the understanding
questions without looking at the answer key, then attempt the graded exercise. The
notebooks use fictional data only. Start with [`labs/README.md`](labs/README.md) for
the exact lab map and prerequisites.

## Layout

| Path | What's there |
|---|---|
| [`plan/30-60-90-checklist.md`](plan/30-60-90-checklist.md) | Operating plan (loosely based on Watkins, *The First 90 Days*) with 30/60/90 outcomes, weekly actions, stakeholder work, and exit criteria |
| [`study-guide/`](study-guide/) | Voice-agent study guide (Markdown + original .docx) |
| [`docs/`](docs/) | Public-source domain primer, Pantheon system model, autonomy policy, metrics, field exercise, and first-90-days playbook |
| [`docs/pantheon-2026-ai-roadmap.md`](docs/pantheon-2026-ai-roadmap.md) | Pantheon 2026 public AI announcements and implications for voice |
| [`docs/call-facts-contract.md`](docs/call-facts-contract.md) | Teaching schema for shared context a voice agent might capture |
| [`docs/homh-and-agent-booking.md`](docs/homh-and-agent-booking.md) | Trust surfaces for Homh and AI-assistant booking channels |
| [`docs/whitepaper/`](docs/whitepaper/) | Public-source background whitepaper: chapters 00–16 (15–16: agentic orchestration and shared skills), appendices, and source ledger |
| [`docs/reading-guide.md`](docs/reading-guide.md) | Ranked blogs, papers and talks with four takeaways each (start here for reading) |
| [`docs/references.md`](docs/references.md) | Complete bibliography of every external source in the repo |
| [`docs/podcast-prompts.md`](docs/podcast-prompts.md) | NotebookLM podcast prompts: seven technical and three company-context episodes plus four coaching episodes |
| [`docs/livekit-hands-on.md`](docs/livekit-hands-on.md) | LiveKit track: Agent Builder → `lk` starter → fake ServiceTitan tools with guardrails |
| [`labs/`](labs/) | Fifteen Jupyter tutorials: OpenAI Realtime, LiveKit, LangChain/LangGraph, LangSmith, multi-agent coordination (09–12), Mini-Max (13), and earning autonomy (14) |
| [`labs/solutions/`](labs/solutions/) | Offline-safe solution notes for the lab exercises |
| [`senior-engineer/`](senior-engineer/) | Judgment track: eight fictional exercises with self-checks (including bookability judge) |
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

Work through `00` → `08` in order, then `09` → `12` for multi-agent coordination, followed by 13–14 for the system capstone and autonomy policy. See [`labs/README.md`](labs/README.md) for details.

To run the offline test suite without activating the environment:

```bash
.venv/bin/python scripts/run_notebooks.py
```

Never use `--live` in CI. Live runs can cost money and must use personal credentials
and fictional data.

## Local Sensitive-Content Hook

Install the repository's optional pre-commit check with:

```bash
ln -s ../../scripts/pre-commit .git/hooks/pre-commit
```

For private local patterns, set `SENSITIVE_PATTERNS` or create the ignored
`.sensitive-patterns` file. Never commit the pattern file.

## Progress

| Phase | Status |
|---|---|
| Pre-start (→ Oct 25) | ⬜ |
| Days 1–30 | ⬜ |
| Days 31–60 | ⬜ |
| Days 61–90 | ⬜ |

Progress is intentionally manual. Check off the corresponding items in
[`plan/30-60-90-checklist.md`](plan/30-60-90-checklist.md) as work is completed.


## Day-one boundary

October 26, 2026 is the start date. From that date forward, this public repository is a
frozen, sanitized pre-start guide. Company knowledge belongs in company systems or an approved
private location; only genuinely public, verified sources belong here. See
[After Day One](docs/after-day-one.md).
