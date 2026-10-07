# Exercise: Evaluation and Denominator Design

## Scenario

You are asked:

> "Are our voice agents getting better at booking?"

The team currently reports:

> "98% booking success."

Your first job is to determine what that number means.

## Define the funnel

Specify the denominator for each:
- all inbound calls
- answered calls
- calls with a bookable intent
- calls with sufficient information to attempt booking
- calls where policy permits autonomous booking
- calls where a valid slot is offered
- calls where the caller accepts a slot
- calls where the backend commits the booking
- calls where the agent correctly reports the final state

For each stage, state whether it is a **business outcome**, **system capability**, or
**diagnostic metric**.

## Build an evaluation

Define:
- primary outcome
- three hard invariants
- three soft quality metrics
- two safety guardrails
- minimum sample size or stopping rule
- important slices
- baseline and comparison periods
- failure taxonomy

Include slices for at least one of: new booking vs reschedule/cancel, business unit/job type,
transfer vs autonomous completion, or short vs long calls.

## Adversarial cases

Create five cases that a headline success metric could hide:
1. hallucinated booking
2. duplicate booking after retry
3. correct refusal of a forbidden action
4. unnecessary human transfer
5. stale address or slot

For each, specify expected authoritative state and expected spoken claim.

## Senior-level extension

Design an eval that distinguishes:

**"the model sounded correct"**

from

**"the system actually completed the intended transaction safely."**

## Evidence

Produce a one-page funnel, metric definitions, ten fictional test cases, and a short
recommendation about what should and should not appear on the executive dashboard.
