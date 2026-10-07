# Exercise: Evaluation and Denominator Design

**Time:** 60 minutes · **Builds on:** [evaluating voice agents](../docs/evaluating-voice-agents.md), lab 07, lab 11

## Scenario

You're asked:

> "Are our voice agents getting better at booking?"

The team currently reports:

> "98% booking success."

Your first job is to work out what that number means.

## Define the funnel

Give the denominator for each stage:

- all inbound contacts (phone, SMS, web chat, and bookings requested by external AI assistants)
- answered contacts
- contacts with a bookable intent
- contacts the system judged bookable (and how often that judgment was right)
- contacts with enough information to attempt a booking
- contacts where policy permits autonomous booking
- contacts where a valid slot was offered
- contacts where the caller accepted a slot
- contacts where the backend committed the booking
- contacts where the agent correctly reported the final state
- booked jobs that were actually completed (not cancelled, no-show, or wrong job type)

For each stage, say whether it is a **business outcome**, a **system capability**, or a
**diagnostic metric**.

## Build an evaluation

Define:

- the primary outcome
- three hard invariants
- three soft quality metrics
- two safety guardrails
- a minimum sample size or stopping rule
- the important slices
- baseline and comparison periods
- a failure taxonomy

Include slices for at least two of: new booking vs. reschedule or cancel; job type or trade;
channel; after-hours vs. business hours; transfer vs. autonomous completion; short vs. long
calls.

## Adversarial cases

Create five cases that a headline success metric could hide:

1. a hallucinated booking (said "booked", nothing committed)
2. a duplicate booking after a retry
3. a correct refusal of a forbidden action (counted as a "failure"?)
4. an unnecessary human transfer
5. a stale address or slot

For each, give the expected authoritative state and the expected spoken claim.

## Extensions

- Design an eval that distinguishes **"the model sounded correct"** from **"the system
  actually completed the intended transaction safely."**
- Your agent passes a scenario 95% of the time. How often does it pass the same scenario five
  times in a row? What does that imply for how you run regression tests?

## Deliverable

A one-page funnel, metric definitions, ten fictional test cases, and a short recommendation
on what should and should not appear on an executive dashboard.

## Self-check

A strong answer:

- Finds that "98%" is almost certainly *committed ÷ attempted* (or similar) with a narrow
  denominator, and that it ignores contacts that were never judged bookable, never offered a
  slot, or were transferred.
- Makes the **bookability judgment** its own measured stage. A system can raise its booking
  rate by calling fewer contacts bookable. (Publicly, the company described this exact problem
  and built a separate post-call judge for it; see the [Pantheon brief](../docs/pantheon-2026-ai-roadmap.md).)
  The judge then needs its own evaluation against human labels.
- Uses state-based checks (backend state vs. spoken claim) as hard invariants: zero false
  confirmations, zero duplicates, zero emergency bookings.
- Picks a sample size that can detect the change it cares about. Small differences around 98%
  need thousands of contacts per arm, not dozens.
- Computes pass^k: 0.95⁵ ≈ 0.77, so a "95%" scenario fails a five-run check almost one time in
  four. It therefore runs repeat trials and tracks per-scenario reliability, not one run each.
- Keeps diagnostic metrics off the executive dashboard and shows a small set of business
  outcomes with their denominators stated.

---

Part of the [senior engineer judgment track](README.md).
