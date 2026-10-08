# First 90 Days: 30/60/90 Operating Plan

**Theme:** learn the domain → diagnose the situation → secure an early win → own a
measurable outcome.

This checklist is the execution companion to the [First 90 Days
Playbook](../docs/first-90-days-playbook.md). Adjust dates, access, and scope with the
manager after starting.

## The 90-Day Contract

| Checkpoint | Outcome, not activity | Evidence |
|---|---|---|
| **Day 30: Understand** | Explain the customer workflow, product context, architecture, owners, metrics, and top risks; ship one trust-building change | System map, stakeholder map, 30-day memo, first PR |
| **Day 60: Contribute** | Deliver a scoped project behind a safe rollout with an agreed baseline and guardrails | Design doc, baseline, review notes, weekly updates, working increment |
| **Day 90: Own** | Demonstrate measured impact or a well-supported stop decision; own the runbook/monitoring and propose the next bet | Before/after analysis, runbook, retro, next-quarter proposal |

## Pre-Start: Prepare (Now–Oct 25)

## Canonical pre-start path

Follow this table in order. It is the single pre-start schedule. Each week ends with one
artifact or demonstration. The total is designed for 4–6 hours per week.

| Week | Read/watch/listen/run | Time | Active deliverable |
|---|---|---:|---|
| Sept 28 | Read docs 101 and contractor lifecycle; read speech-to-speech and GPT-Live-1 background; read/watch reading-guide items 1–4 and 11B; run labs 00–03; listen to podcast episodes 1 and 6 | 4–6 h | A one-page contractor lifecycle map with the application control-plane boundary and six observed/inferred/unknown questions |
| Oct 5 | Read architecture; read/watch reading-guide items 5–10; run labs 04–06; complete LiveKit hands-on Phases 1–2; listen to episodes 2, 10 and 11 | 4–6 h | A comparison of cascaded, realtime and workflow paths plus five simulated failure observations |
| Oct 12 | Read evaluation guide and reading-guide items 11–14; watch the LangSmith videos (item 14A); run labs 07–08; complete LiveKit hands-on Phase 3; listen to episodes 3, 4 and 12 | 4–6 h | A fictional eval report, study-question draft, and capstone evidence matrix |
| Oct 19 | Use the [10-hour minimum path](../docs/minimum-path.md) if time is tight; read the hypothesis map, business metrics, field exercise, and after-day-one boundary; run labs 09–10 and 13 (labs 11, 12 and 14 are scheduled in weeks 2–3; the minimum path pulls lab 14 forward if you take it); listen to episodes 5, 13 and 14; review templates and capstone rubric | 4–6 h | System-level question set, Mini-Max/autonomy evidence, first-PR hypothesis, personal first-week plan, and capstone open-criteria list |

The acceptance criteria are in [`docs/capstone-rubric.md`](../docs/capstone-rubric.md).

### Week of Sept 28 — Build the learning agenda

- [ ] Read the [domain primer](../docs/servicetitan-101.md) and [contractor
  lifecycle](../docs/how-a-contractor-works.md).
- [ ] Watch explainer episodes 1–2: [Voice Agents from First Principles](../docs/reading-guide.md#0-voice-agents-from-first-principles-four-episode-explainer-) item 0.
- [ ] Read [Speech-to-speech models](../docs/speech-to-speech-models.md) before lab 01.
- [ ] Read [GPT-Live-1](../docs/gpt-live-1.md) (reading-guide item 7A): OpenAI's full-duplex voice model with delegation.
- [ ] Watch LiveKit's "Voice Agent Pipeline Explained" before lab 03 ([reading guide](../docs/reading-guide.md) item 11B).
- [ ] Run labs 00–03 offline with Python 3.12 (needs a laptop).
- [ ] Write one question each for customer, product, technology, quality, team, and business.
- [ ] Start an evidence log with **observed / inferred / unknown** columns.
- [ ] Read the [Pantheon hypothesis map](../docs/hypothesis-map.md) and mark the questions you most need answered in weeks 1–2.
- [ ] Draft the manager's first-1:1 questions in [`templates/1on1-questions.md`](../templates/1on1-questions.md).
- [ ] Read the [First-90-Days Question Bank](../docs/first-90-days-question-bank.md) and choose at least three questions to ask across different roles.
- [ ] Read [Setting Goals With Your New Manager](../docs/manager-alignment.md) and prepare the 20-minute pre-1:1 exercise.
- [ ] [Reading guide](../docs/reading-guide.md) items 1–4.
- [ ] [Podcast](../docs/podcast-prompts.md) episodes 1 and 6 (coaching: entering well — it's scheduled before day one).

### Week of Oct 5 — Build technical depth

- [ ] Read the [Pantheon 2026 AI roadmap brief](../docs/pantheon-2026-ai-roadmap.md) (reading-guide item 7B); watch the keynote replays when available.
- [ ] Skim the [call facts contract](../docs/call-facts-contract.md) and list three fields you would insist on verifying before dispatch consumes them.
- [ ] Read [Homh and AI-agent booking](../docs/homh-and-agent-booking.md) and note trust questions for AI-assistant channels.
- [ ] Read [`docs/voice-agent-architecture.md`](../docs/voice-agent-architecture.md).
- [ ] Try interactive lessons 4, 6 and 2: [Lessons](/lessons).
- [ ] Watch explainer episodes 3–4: [Voice Agents from First Principles](../docs/reading-guide.md#0-voice-agents-from-first-principles-four-episode-explainer-) item 0.
- [ ] Complete labs 04–06 and compare realtime, cascaded, and workflow paths (needs a laptop).
- [ ] Read [Build your own voice agent](../docs/build-your-own-voice-agent.md): the chained vs. GPT-Live implementation differences.
- [ ] Measure the lab latency categories; label simulated versus live measurements (needs a laptop).
- [ ] Break the fictional agent five ways: interruption, slow number, backchannel, emergency phrase, wrong address (needs a laptop).
- [ ] Write a first hypothesis about where the application control plane begins.
- [ ] [LiveKit hands-on](../docs/livekit-hands-on.md) Phases 1–2: Agent Builder prototype, `lk` starter and debugger (needs a laptop).
- [ ] Reading guide items 5–10; podcast episodes 2, 10 and 11.

### Week of Oct 12 — Build evaluation judgment

- [ ] Watch the must-watch LangSmith videos ([reading guide](../docs/reading-guide.md) item 14A) before lab 07.
- [ ] Complete labs 07–08 (needs a laptop).
- [ ] Read [Tools and guardrails](../docs/tools-and-guardrails.md) and run its checklist against the lab tools.
- [ ] Do the [bookability judge](../senior-engineer/bookability-judge.md) exercise (private notes only).
- [ ] Try interactive lessons 1, 3, 5 and 9: [Lessons](/lessons).
- [ ] Use [`docs/capstone-rubric.md`](../docs/capstone-rubric.md) to collect pass/fail evidence.
- [ ] Read [`docs/evaluating-voice-agents.md`](../docs/evaluating-voice-agents.md).
- [ ] Write the answer in [`notes/study-question.md`](../notes/study-question.md).
- [ ] Define three hard invariants and three softer quality questions for a fictional call set.
- [ ] Prepare a one-page list of assumptions that must be tested after joining.
- [ ] LiveKit hands-on Phase 3: fake ServiceTitan tools (reschedule/cancel) behind the control plane (needs a laptop).
- [ ] Reading guide items 11–14; podcast episodes 3, 4 and 12.

### Week of Oct 19 — Prepare relationships and logistics

- [ ] Run labs 09–10 (shared context; coordination and arbitration) (needs a laptop).
- [ ] Read the essentials path of [whitepaper chapter 15, Agentic orchestration](../docs/whitepaper/15-agentic-orchestration.md): the architecture map behind labs 09–14.
- [ ] Run [lab 13](../labs/13_minimax_capstone.ipynb): trace 20 calls and identify the most costly extraction error.
- [ ] Read the [business metrics primer](../docs/business-metrics.md) and try the [value calculator](https://sp7412.github.io/onboarding/value-calculator/).
- [ ] Read the [`docs/reading-guide.md`](../docs/reading-guide.md) items paired to any unfinished lab.
- [ ] Read [`docs/call-anatomy.md`](../docs/call-anatomy.md) and annotate likely failure modes.
- [ ] Finalize manager, PM, infrastructure, evaluation, and support questions.
- [ ] Read reading-guide items 14B–14F (working with your manager, about 75 minutes).
- [ ] Draft your [working-with-me doc](../templates/working-with-me.md) and start a [brag document](../templates/brag-document.md).
- [ ] Prepare a personal first-week plan and take at least two full days off before Oct 26.
- [ ] Podcast episodes 5 and 13.
- [ ] Do not create employer accounts, access employer data, or copy internal information into this public repo.

## Days 1–30: Understand And Earn Trust

### Week 1 (Oct 26–30) — Establish the contract

- [ ] Complete required HR, security, privacy, and compliance onboarding.
- [ ] Ask the manager to confirm day-30, day-60, and day-90 outcomes and decision rights.
- [ ] Hold the first alignment 1:1: priorities, success criteria, pace, working norms, feedback, and close.
- [ ] Share your working-with-me doc; ask what your manager is judged on this quarter and for the career ladder for your level.
- [ ] Agree on remote norms: overlap hours, written updates, and when to use Slack, docs or calls.
- [ ] Confirm authorized access and data-handling rules before reviewing calls or traces.
- [ ] Meet manager, PM/product partner, senior engineer, and evaluation/observability partner; use the [First-90-Days Question Bank](../docs/first-90-days-question-bank.md) for two to four questions per conversation.
- [ ] Start the internal copy of [`templates/onboarding-log.md`](../templates/onboarding-log.md).
- [ ] Get the development environment running and make a list of setup gaps (needs a laptop).
- [ ] Try interactive lessons 7, 8 and 10: [Lessons](/lessons).

**Output:** written success contract, stakeholder list, access plan, and learning agenda.
- [ ] Reading guide Tier 3 (items 15–23), spread across weeks 1–4.

### Week 2 (Nov 2–6) — Map the system

- [ ] Run labs 11–12 (learning loop; agent-to-agent booking) and compare them with how the team actually shares context between agents.
- [ ] Trace one authorized interaction end to end: caller → transport → model → tools/workflow → source of truth → traces.
- [ ] Read [whitepaper chapter 17, Running agents in production](../docs/whitepaper/17-running-agents-in-production.md) before your first trace or failure review.
- [ ] Draw the architecture with owners, state boundaries, retries, and observability.
- [ ] Ask each owner to correct your map; record disagreements as learning items.
- [ ] Identify the definition and denominator for the key quality metrics.
- [ ] Ship the first small PR: documentation, test, logging, or developer-experience fix.
- [ ] Run the 15-minute [pre-mortem](../templates/pre-mortem.md) with your manager.
- [ ] Draft and send the written 30/60/90 agreement to the manager by the end of week 2, including the pre-mortem's top risks.

**Output:** reviewed system map, owner map, and first merged contribution.

### Week 3 (Nov 9–13) — Learn customer and quality reality

- [ ] Run [lab 14](../labs/14_earning_autonomy.ipynb): defend a promotion policy with a Wilson bound, cost asymmetry, calibration, and drift guard.
- [ ] Try the [earned-autonomy lesson](https://sp7412.github.io/onboarding/lessons/earned-autonomy/), then do the [autonomy promotion review](../senior-engineer/autonomy-promotion.md) exercise (private notes only).
- [ ] Review authorized calls/traces or approved substitutes; record patterns without PII.
- [ ] Tag successes, failures, and awkward moments; identify the top five patterns.
- [ ] Meet telephony/infra, support or CSR-facing, and product stakeholders.
- [ ] Read recent approved incident reports or postmortems if available.
- [ ] Separate observed failures from hypotheses about causes.
- [ ] Ship a second small PR or agree why one larger first PR is better.

**Output:** failure taxonomy, metric definitions, and evidence-backed risk list.

### Week 4 (Nov 16–20) — Diagnose and align

- [ ] Classify the situation hypothesis: turnaround, realignment, accelerated growth, or sustaining success.
- [ ] Write the [30-day memo](../templates/30-day-memo.md): observed, inferred, unknown, risks, contribution options.
- [ ] Day-30 calibration: you and your manager rate each goal separately, then compare.
- [ ] Review it with the manager; revise based on feedback.
- [ ] Choose one day-60 problem with a clear owner, denominator, baseline, and reversible scope.
- [ ] Agree in writing on the day-60 deliverable and success/guardrail metrics.

### Day-30 exit criteria

- [ ] I can explain the customer/job lifecycle and production architecture without relying on a diagram.
- [ ] I can name the owner and source of truth for each major boundary.
- [ ] I have a stakeholder map and a reviewed learning agenda.
- [ ] I have shipped at least one useful, low-risk contribution.
- [ ] My top risks distinguish evidence from inference.
- [ ] The day-60 problem, baseline plan, and success metric are agreed in writing.

## Days 31–60: Align, Design, And Contribute

### Weeks 5–6 — Design the first measurable slice

- [ ] Write the [design doc](../templates/design-doc.md).
- [ ] Define eligible population, denominator, baseline period, primary metric, guardrails, and non-goals.
- [ ] Compare at least two approaches, including the option to do nothing.
- [ ] Review with manager, senior engineer, product partner, and relevant owner.
- [ ] Decide rollout, flag/cohort, rollback trigger, and monitoring owner.

### Weeks 7–8 — Build in thin increments

- [ ] Ship the smallest useful increment behind a flag or to a test cohort.
- [ ] Add or update regression cases and deterministic evaluators.
- [ ] Publish a weekly status with evidence, decisions, and blockers.
- [ ] Pair with a teammate and shadow an incident review or operational workflow.
- [ ] Ask for mid-point feedback: more of, less of, differently.

### Day-60 check

- [ ] Show baseline versus current results with denominators and slices.
- [ ] Demonstrate safety/quality guardrails and rollback behavior.
- [ ] Confirm the project is still the right bet; stop or re-scope if evidence says otherwise.
- [ ] Agree on the day-90 rollout, ownership, and next-quarter decision.

## Days 61–90: Own And Multiply

### Weeks 9–10 — Roll out or stop deliberately

- [ ] Complete the target rollout or make a documented stop/rollback decision.
- [ ] Measure before/after impact, including null results and uncertainty.
- [ ] Add monitoring, alerts, and a debugging path for regressions.
- [ ] Write the runbook: behavior, dependencies, failure modes, rollback, and owner.

### Weeks 11–12 — Multiply the learning

- [ ] Write a two-page next-quarter proposal: problem, evidence, why now, impact, risks, plan.
- [ ] Review it with manager and product partner.
- [ ] Run one knowledge-share or publish a public-safe technical note.
- [ ] Review PRs or pair in the area you now understand best.
- [ ] Ensure another engineer can reproduce the measurement and operate the change.

### Week 13 — Reflect and reset

- [ ] Write the [90-day retro](../templates/90-day-retro.md).
- [ ] Review what shipped, what failed, what surprised you, and what you will own next.
- [ ] Update the stakeholder map, risk register, and learning agenda for the next quarter.
- [ ] Use only approved, public-safe wording for any résumé or LinkedIn update.

### Day-90 exit criteria

- [ ] I can explain the customer outcome, baseline, and measured result of my contribution.
- [ ] One deliverable is rolled out, safely stopped, or explicitly re-scoped with evidence.
- [ ] Monitoring, runbook, rollback, and ownership are clear.
- [ ] I am a reliable contact for at least one technical or quality area.
- [ ] The next-quarter proposal has been reviewed and prioritized.

## Recurring Weekly Rhythm

- [ ] Daily: five minutes of evidence-log notes.
- [ ] Weekly: three-line manager status — done, next, blocked/decision needed.
- [ ] Weekly: five minutes on the brag document, linked to your goals.
- [ ] Weekly: one stakeholder conversation outside the immediate pair/team.
- [ ] Weekly: one authorized call, trace, regression case, or metric slice review.
- [ ] Friday: update assumptions, risks, checklist, and next week's learning goal.

## Watch-outs

- **Do not diagnose too early:** first impressions are hypotheses.
- **Do not confuse activity with progress:** every phase needs an artifact and evidence.
- **Do not overreach on the first win:** reversible and measurable beats impressive.
- **Do not hide uncertainty:** label what is observed, inferred, and unknown.
- **Do not frame wins only as model metrics:** connect them to contractor and customer outcomes.
