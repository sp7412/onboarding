# First 90 Days Playbook

This complements the [30/60/90 checklist](../plan/30-60-90-checklist.md). It is a
public-safe operating guide, not a prediction of ServiceTitan's internal processes.

## First 30 Days: Build A Map

- Ask your manager for the outcomes that matter, the decision rights you have, and the
  first reversible contribution that would build trust.
- In 1:1s, ask for examples: "What does a good call look like?", "Where does quality
  degrade?", and "Which metric has a trustworthy denominator?"
- Trace one representative flow end to end, then draw it with owners, sources of truth,
  failure boundaries, and observability gaps.
- Listen to or review only data you are authorized to access. Record patterns, not
  customer-identifying details.
- Ship a small documentation, test, or logging change before proposing a broad redesign.

The 30-day memo should separate **observed**, **inferred**, and **unknown**. Include
three risks with evidence, not a catalog of hypothetical concerns.

## Days 31–60: Pick A Measurable Slice

Choose one problem with a clear owner, baseline, reversible rollout, and customer-facing
outcome. Good candidates include:

- a regression dataset and evaluator for a recurring failure;
- a guardrail or escalation path with a measurable false-positive tradeoff;
- a latency waterfall and one targeted reduction in dead air.

Write the design doc before building. Define the denominator, baseline period, slices,
rollback signal, and what will not change. Review it with the manager and a senior peer.

## Days 61–90: Ship And Multiply

- Roll out to a test cohort or behind a flag.
- Compare before/after outcomes and include null or negative results.
- Add monitoring, a runbook, and an owner.
- Share the approach so another engineer can reproduce the measurement.
- Propose the next problem only after showing what the first change taught you.

## Running Effective 1:1s

Bring three items:

1. **Progress:** what changed since the last meeting.
2. **Decision:** what you need the manager to choose or unblock.
3. **Learning:** what evidence changed your understanding.

Send a short pre-read when the topic needs context. Do not turn the meeting into a
status dump; use it for tradeoffs, feedback, and prioritization.

## From Defense Programs To Product SaaS

Your rigor transfers well: explicit assumptions, failure analysis, traceability,
verification, and attention to edge cases. The operating context changes:

- feedback arrives continuously from customers, operators, and production telemetry;
- the best first version is often smaller and reversible rather than comprehensive;
- ambiguity is a product input, not only a requirements defect;
- uptime, cost, latency, support burden, and customer effort matter alongside model
  accuracy;
- a technically correct feature that does not improve a contractor outcome is not yet a
  product win.

Keep the discipline, shorten the feedback loop, and make uncertainty visible early.

## Communicating Wins

Frame updates as:

> For **[eligible population]**, we changed **[behavior]**. The baseline was
> **[denominator and period]**; after **[rollout]**, **[customer/contractor outcome]**
> moved from **[before]** to **[after]**, with **[safety/quality guard]** unchanged or
> improved. The remaining uncertainty is **[unknown]**.

Never invent an internal metric or claim production impact before it is measured and
approved for sharing.
