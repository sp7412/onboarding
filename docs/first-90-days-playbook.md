# First 90 Days Playbook

This operating plan is loosely based on Michael D. Watkins, *The First 90 Days, Updated
and Expanded* (Harvard Business Review Press, 2013; ISBN 9781422188613). It uses the
broad ideas of preparing, learning quickly, diagnosing the situation, securing early
wins, and negotiating success.

Use this document to decide **how to operate**. Use the [30/60/90 checklist](../plan/30-60-90-checklist.md)
to decide **what to do each week**.

## The Objective

By day 90, you should have:

1. a trustworthy map of the product, customer workflow, architecture, owners, and
   quality metrics;
2. relationships strong enough to make decisions and get help quickly;
3. one small, reversible improvement shipped with a measured contractor outcome; and
4. a clear next-quarter proposal based on evidence rather than first impressions.

Do not optimize for appearing busy. Optimize for increasing the team's confidence that
you understand the system, choose good problems, and can deliver safely.

## Exit Criteria At A Glance

The checkpoint outcomes, mirrored from the [30/60/90 checklist](../plan/30-60-90-checklist.md),
which holds the canonical list. Use these to test yourself before each review; the checklist's
checkboxes track completion. If you edit one list, edit both — or better, edit the checklist and
re-copy here.

**Day 30 — Understand**

- I can explain the customer/job lifecycle and production architecture without relying on a diagram.
- I can name the owner and source of truth for each major boundary.
- I have a stakeholder map and a reviewed learning agenda.
- I have shipped at least one useful, low-risk contribution.
- My top risks distinguish evidence from inference.
- The day-60 problem, baseline plan, and success metric are agreed in writing.

**Day 60 — Contribute**

- Show baseline versus current results with denominators and slices.
- Demonstrate safety/quality guardrails and rollback behavior.
- Confirm the project is still the right bet; stop or re-scope if evidence says otherwise.
- Agree on the day-90 rollout, ownership, and next-quarter decision.

**Day 90 — Own**

- I can explain the customer outcome, baseline, and measured result of my contribution.
- One deliverable is rolled out, safely stopped, or explicitly re-scoped with evidence.
- Monitoring, runbook, rollback, and ownership are clear.
- I am a reliable contact for at least one technical or quality area.
- The next-quarter proposal has been reviewed and prioritized.

## Before Day One: Prepare

### Define your learning agenda

Write one question under each heading before starting:

| Area | Question |
|---|---|
| Customer | What does a contractor consider a successful call and a successful job? |
| Product | Which workflow is the team trying to improve, and for whom? |
| Technology | Where do transport, model, workflow, policy, and systems of record meet? |
| Quality | Which failures are unsafe, expensive, or merely awkward? |
| Team | Who owns each decision, metric, and operational boundary? |
| Business | Which outcome matters: booked work, missed leads, CSR effort, speed, or retention? |

Keep a separate evidence log with three columns: **observed**, **inferred**, and
**unknown**. This prevents a plausible architecture story from becoming an assumed fact.

### Prepare a first-week contract

Ask your manager to agree on:

- what success looks like at days 30, 60, and 90;
- the first small contribution that is useful and reversible;
- who should help you learn the system;
- how often and in what format to communicate;
- what access, privacy, and production-safety boundaries apply.

## Days 1–30: Learn, Diagnose, And Earn Trust

### Build the map

Trace one representative interaction end to end, with authorized data only:

```text
customer request → transport → turn detection → model → tools/workflow
→ source of truth → response/transfer → trace and outcome metric
```

For every boundary, record:

- owner and on-call path;
- authoritative state;
- allowed and forbidden actions;
- timeout, retry, and rollback behavior;
- observable evidence;
- your confidence: high, medium, or low.

### Diagnose the situation

Classify the current situation using evidence:

| Situation | Signals | Your response |
|---|---|---|
| **Turnaround** | serious quality, reliability, or trust failures | stabilize, measure, reduce risk, then improve |
| **Realignment** | good components but unclear ownership, priorities, or metrics | clarify strategy, interfaces, and decision rights |
| **Accelerated growth** | demand is rising faster than process or capacity | add structure, automation, and scalable evaluation |
| **Sustaining success** | results are healthy and the system is well understood | improve incrementally without creating needless disruption |

This is a working hypothesis, not a label to announce. Review it with your manager
after you have enough evidence.

### Build relationships deliberately

In the first month, meet people who represent different views of the system. Use the [First-90-Days Question Bank](first-90-days-question-bank.md) to choose two to four high-value questions for each conversation rather than treating these as a questionnaire:

- manager: outcomes, priorities, decision rights;
- PM or product partner: customer problem and tradeoffs;
- senior engineer: architecture, review norms, operational risk;
- infrastructure/telephony owner: transport, latency, incidents;
- evaluation/observability owner: definitions, datasets, monitoring;
- support or CSR-facing partner: caller effort and failure cost.

Ask each person a small selection from the [question bank](first-90-days-question-bank.md), then capture the answer, concrete example, implication, and follow-up in your private evidence log. At minimum, learn what they think you should understand sooner, what failure is most costly, what useful contribution looks like, and where the source of truth lives.

### Secure an early learning win

Choose a change that is:

- useful even if your larger hypothesis is wrong;
- small enough to review in one sitting;
- safe to roll back;
- measurable or clearly reduces future uncertainty;
- visible to the people who will depend on it.

Good examples are a missing test, a trace field, a runbook correction, a redacted
regression case, or a small documentation fix. Avoid a broad prompt rewrite as your
first proof of value.

### Day-30 contract

Review a one-page memo with your manager. It should state:

- how the system works, with confidence levels;
- what you observed from customers, operators, and telemetry;
- three risks and the evidence for each;
- what remains unknown;
- your situation diagnosis and alternatives considered;
- the proposed day-60 deliverable and its success metric;
- support or decisions you need from your manager.

## Days 31–60: Align, Design, And Deliver

### Negotiate success

Start this conversation in week one with [Setting Goals With Your New Manager](manager-alignment.md).
Use its first conversation to learn the manager's priorities, expectations, pace, decision rights,
working norms, and feedback preferences. By the end of week two, turn the discussion into a
one-page written agreement and ask: "If I hit these, would you consider the first 90 days a
success?"

Before building, agree in writing on:

- the problem and eligible population;
- baseline period and denominator;
- primary outcome and guardrail metrics;
- scope and explicit non-goals;
- decision-maker and reviewers;
- rollout cohort or flag;
- rollback trigger and owner;
- weekly communication rhythm.

This is not bureaucracy. It prevents a technically successful project from being judged
against a different definition of success later.

### Choose one measurable slice

Potential slices for a voice-agent team include:

- an evaluator that turns reviewed failures into regression tests;
- a guardrail or escalation path for restricted/OOD calls;
- a latency waterfall and one targeted dead-air reduction;
- a reliability improvement for retries, timeouts, or handoffs.

Pick one. A senior contribution is often the discipline to say no to the other three.

### Design before implementation

Write the design doc and review it with the manager and a senior peer. Include the
baseline, alternatives, failure modes, privacy implications, rollout, monitoring, and
what evidence would cause you to stop. Ship in thin increments and report learning,
including null results.

### Day-60 contract

Show:

- baseline versus current result, with denominator and slices;
- what shipped and what remains behind a flag;
- safety and quality guardrails;
- feedback from operators or customers, if authorized;
- the next decision: continue, change direction, or stop.

Ask directly: **What should I do more of, less of, or differently?**

## Days 61–90: Own, Ship, And Multiply

### Turn contribution into ownership

- complete the rollout or make the stop decision;
- measure before/after and document uncertainty;
- add monitoring and a debugging/runbook path;
- identify a durable owner and escalation path;
- teach the approach to at least one other person;
- propose the next-quarter problem and why now.

### Day-90 contract

The review should answer:

1. What changed for customers, contractors, operators, or engineers?
2. What was the baseline, and how reliable is the comparison?
3. What did not work, and what did you learn?
4. What do you now own?
5. What is the next-quarter proposal, with expected impact and risks?

## Weekly Operating Rhythm

| Habit | Output |
|---|---|
| Daily learning log | one observed fact, one uncertainty, one next question |
| Weekly manager update | done, next, blocked; include one decision needed |
| One relationship conversation | a new perspective on product, system, or customers |
| Quality review | a call, trace, regression case, or metric slice, as authorized |
| Friday review | update assumptions, risks, checklist, and next week's learning goal |

## Moving From Defense Programs To Product SaaS

Keep the rigor: explicit assumptions, testable claims, failure analysis, traceability,
and disciplined release criteria. Change the operating loop:

- feedback is continuous and often incomplete;
- ambiguity is a product input, not only a requirements defect;
- small reversible experiments beat large up-front designs;
- cost, latency, support burden, and customer effort matter with accuracy;
- a technically correct feature is not a product win unless it improves an outcome.

The goal is not to abandon rigor. It is to apply rigor at the speed of learning.

## Communicating Wins

Use this format:

> For **[eligible population]**, we changed **[behavior]**. The baseline was
> **[denominator and period]**; after **[rollout]**, **[customer/contractor outcome]**
> moved from **[before]** to **[after]**, while **[safety/quality guard]** was
> **[unchanged/improved]**. Remaining uncertainty: **[unknown]**.

Never invent an internal metric or claim production impact before it is measured and
approved for sharing.
