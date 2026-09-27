# First 90 Days: 30/60/90 Operating Plan

**Theme:** learn the domain → diagnose the situation → secure an early win → own a
measurable outcome.

This checklist is the execution companion to the [First 90 Days
Playbook](../docs/first-90-days-playbook.md). It is inspired by broadly useful
first-90-days practices, not a prediction of internal company processes. Adjust dates,
access, and scope with the manager after starting.

## The 90-Day Contract

| Checkpoint | Outcome, not activity | Evidence |
|---|---|---|
| **Day 30: Understand** | Explain the customer workflow, product context, architecture, owners, metrics, and top risks; ship one trust-building change | System map, stakeholder map, 30-day memo, first PR |
| **Day 60: Contribute** | Deliver a scoped project behind a safe rollout with an agreed baseline and guardrails | Design doc, baseline, review notes, weekly updates, working increment |
| **Day 90: Own** | Demonstrate measured impact or a well-supported stop decision; own the runbook/monitoring and propose the next bet | Before/after analysis, runbook, retro, next-quarter proposal |

## Pre-Start: Prepare (Now–Oct 25)

### Week of Sept 28 — Build the learning agenda

- [ ] Read the [domain primer](../docs/servicetitan-101.md) and [contractor
  lifecycle](../docs/how-a-contractor-works.md).
- [x] Run labs 00–03 offline with Python 3.12. (Verified locally: 9/9 full suite passed.)
- [ ] Write one question each for customer, product, technology, quality, team, and business.
- [ ] Start an evidence log with **observed / inferred / unknown** columns.
- [ ] Draft the manager's first-1:1 questions in [`templates/1on1-questions.md`](../templates/1on1-questions.md).
- [ ] [Reading guide](../docs/reading-guide.md) items 1–4.
- [ ] [Podcast](../docs/podcast-prompts.md) episode 1.

### Week of Oct 5 — Build technical depth

- [ ] Read [`docs/voice-agent-architecture.md`](../docs/voice-agent-architecture.md).
- [x] Complete labs 04–06 and compare realtime, cascaded, and workflow paths. (Verified locally offline.)
- [ ] Measure the lab latency categories; label simulated versus live measurements.
- [ ] Break the fictional agent five ways: interruption, slow number, backchannel, emergency phrase, wrong address.
- [ ] Write a first hypothesis about where the application control plane begins.
- [ ] [LiveKit hands-on](../docs/livekit-hands-on.md) Phases 1–2: Agent Builder prototype, `lk` starter and debugger.
- [ ] Reading guide items 5–10; podcast episode 2.

### Week of Oct 12 — Build evaluation judgment

- [x] Complete labs 07–08. (Verified locally offline.)
- [ ] Read [`docs/evaluating-voice-agents.md`](../docs/evaluating-voice-agents.md).
- [x] Write the answer in [`notes/study-question.md`](../notes/study-question.md).
- [ ] Define three hard invariants and three softer quality questions for a fictional call set.
- [ ] Prepare a one-page list of assumptions that must be tested after joining.
- [ ] LiveKit hands-on Phase 3: fake ServiceTitan tools (reschedule/cancel) behind the control plane.
- [ ] Reading guide items 11–14; podcast episodes 3 and 4.

### Week of Oct 19 — Prepare relationships and logistics

- [ ] Read the [`docs/reading-list.md`](../docs/reading-list.md) items paired to any unfinished lab.
- [ ] Read [`docs/call-anatomy.md`](../docs/call-anatomy.md) and annotate likely failure modes.
- [ ] Finalize manager, PM, infrastructure, evaluation, and support questions.
- [ ] Prepare a personal first-week plan and take at least two full days off before Oct 26.
- [ ] Podcast episode 5 and coaching episode 6.
- [ ] Do not create employer accounts, access employer data, or copy internal information into this public repo.

## Days 1–30: Understand And Earn Trust

### Week 1 (Oct 26–30) — Establish the contract

- [ ] Complete required HR, security, privacy, and compliance onboarding.
- [ ] Ask the manager to confirm day-30, day-60, and day-90 outcomes and decision rights.
- [ ] Confirm authorized access and data-handling rules before reviewing calls or traces.
- [ ] Meet manager, PM/product partner, senior engineer, and evaluation/observability partner.
- [ ] Start the internal copy of [`templates/onboarding-log.md`](../templates/onboarding-log.md).
- [ ] Get the development environment running and make a list of setup gaps.

**Output:** written success contract, stakeholder list, access plan, and learning agenda.
- [ ] Reading guide Tier 3 (items 15–23), spread across weeks 1–4.

### Week 2 (Nov 2–6) — Map the system

- [ ] Trace one authorized interaction end to end: caller → transport → model → tools/workflow → source of truth → traces.
- [ ] Draw the architecture with owners, state boundaries, retries, and observability.
- [ ] Ask each owner to correct your map; record disagreements as learning items.
- [ ] Identify the definition and denominator for the key quality metrics.
- [ ] Ship the first small PR: documentation, test, logging, or developer-experience fix.

**Output:** reviewed system map, owner map, and first merged contribution.

### Week 3 (Nov 9–13) — Learn customer and quality reality

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
- [ ] Weekly: one stakeholder conversation outside the immediate pair/team.
- [ ] Weekly: one authorized call, trace, regression case, or metric slice review.
- [ ] Friday: update assumptions, risks, checklist, and next week's learning goal.

## Watch-outs

- **Do not diagnose too early:** first impressions are hypotheses.
- **Do not confuse activity with progress:** every phase needs an artifact and evidence.
- **Do not overreach on the first win:** reversible and measurable beats impressive.
- **Do not hide uncertainty:** label what is observed, inferred, and unknown.
- **Do not frame wins only as model metrics:** connect them to contractor and customer outcomes.
