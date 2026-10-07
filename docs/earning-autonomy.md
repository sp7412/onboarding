# Earning Autonomy

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

At Pantheon 2026 ServiceTitan described a five-level AI maturity model, placed voice agents
at level 2, and said some customers already let the agent take every call with CSRs on
standby (company claims; see the [Pantheon brief](pantheon-2026-ai-roadmap.md)). Autonomy is
granted gradually. This document turns that public idea into an engineering policy for the
synthetic labs. It is a teaching model, not ServiceTitan's internal policy.

## 1. Autonomy is a release decision

An agent should not become more autonomous because a demo looks good. Promotion should be a
bounded decision with:

- an explicit error definition;
- a target error rate for the next level;
- a minimum sample size;
- an upper confidence bound;
- cost asymmetry;
- calibration evidence;
- distribution-shift and OOD monitoring;
- segment-specific results;
- a rollback/demotion rule.

Lab 14 implements five original labels:

1. suggest only
2. act with human approval
3. act and notify
4. act autonomously within limits
5. fully autonomous

They are inspired by the public Pantheon discussion but are not ServiceTitan's names or
policy. (The company's model describes how much of a business is automated; these levels
describe how much a single agent may do without review.)

## 2. Why use a Wilson upper bound?

Suppose an agent makes 4 errors in 500 decisions. The observed error rate is 0.8%.
That point estimate does not say the true rate is 0.8%. A promotion gate needs to account for
sampling uncertainty.

For a binomial proportion, the Wilson interval gives a more useful finite-sample bound than
the naive estimate. For a target error rate t, promote only when:

**Wilson upper bound(error rate) < t**

and the minimum sample requirement has been met.

Promotion is one level at a time, and evidence resets after every level change. A hold is a
valid outcome; it means the evidence is not yet strong enough to change the operating mode.

**Demotion uses the other side of the interval.** Demote when the Wilson *lower* bound is
above the target the current level was earned against. That is evidence the agent is worse
than required. Demoting because the upper bound is high punishes small samples, not bad
agents, and makes the level flap from week to week.

The asymmetry is deliberate: the minimum sample gates promotion, not demotion. Thin data
can't demote, because a wide interval keeps the lower bound low, but clear evidence of harm
demotes as soon as it appears, even in a small sample. Losing autonomy should be faster than
earning it.

## 3. Sequential testing

A fixed sample can be wasteful when evidence becomes decisive early. Lab 14 also implements a
Sequential Probability Ratio Test (SPRT).

The teaching version compares:

- H0: error rate = p0
- H1: error rate = p1, where p1 > p0
- alpha: probability of incorrectly rejecting H0 (demoting an agent that is actually fine)
- beta: probability of incorrectly rejecting H1 (promoting an agent that is actually at p1)

The likelihood ratio is evaluated after each observation. Cross the lower boundary to
promote, the upper boundary to demote, or continue when neither boundary is crossed.

SPRT does not remove the need to define the error, the target, and the cost of mistakes.

## 4. Cost asymmetry

Accuracy is not the business objective.

A false "booked" action can create a wasted truck roll and damage trust. A false
"not bookable" decision can lose a valuable job. If:

- C_wrong is the cost of booking when the call is not bookable;
- C_missed is the cost of declining when it is bookable;
- p is the estimated probability that the call is bookable;

then:

- cost(book) = (1 - p) C_wrong
- cost(decline) = p C_missed

Book when cost(book) <= cost(decline), giving a threshold:

**p >= C_wrong / (C_wrong + C_missed)**

The numbers in the lab are illustrative. A real team should estimate costs from its own
outcomes rather than importing the lab's assumptions.

## 5. Calibration is not optional

An agent that says "99% confident" is not necessarily safer than one that says "80%."
Calibration measures whether predicted probabilities correspond to observed frequencies.

Lab 14 computes a reliability diagram and expected calibration error (ECE). The important
operational rule is:

> confidence can support a decision; confidence cannot certify itself.

A promotion policy should therefore use observed outcomes and confidence bounds, not a
model's self-reported confidence alone.

## 6. Drift and OOD

A policy validated on ordinary traffic may fail during a heat wave, after a new trade launch,
or when the channel mix changes.

The lab combines:

- a population stability index (PSI) on the call-type mix;
- an OOD *rate*: the share of current calls whose Mahalanobis distance exceeds the 99th
  percentile of the reference (training) data. A rate, not a maximum, so one odd call never pauses
  the system but a shifted population does;
- a pause rule: drop one level, reset the evidence, and re-validate on the new traffic.

This is intentionally simple. Production monitoring would require historical baselines,
segment-aware thresholds, alert suppression, missing-data handling, and incident response.

## 7. Segment-specific autonomy

A single aggregate score can hide a weak segment. Grant autonomy independently where the
risk and evidence justify it.

Useful segments include trade, intent, after-hours calls, emergencies, reschedules,
new/existing customers, and channel. Watch for Simpson's-paradox-style effects when traffic
mix changes.

The practical consequence is that one segment may be allowed to act while another remains
human-approved.

## 8. What the team should watch

A useful autonomy dashboard contains:

| Dimension | Example |
|---|---|
| Outcome | bookability, valid bookings, completed jobs |
| Safety | false bookings, missed emergencies |
| Statistical evidence | error count, n, Wilson upper bound |
| Cost | expected cost and realized incident cost |
| Calibration | reliability curve, ECE |
| Distribution | PSI, OOD rate |
| Segments | trade, intent, channel, after-hours |
| Operations | latency, transfer rate, retries |
| Governance | current level, last promotion, last demotion, owner |

The dashboard should make it easy to answer: **What changed, where, how much evidence do we
have, and what happens if we stop trusting the agent?**

## Related

- [Lab 14](../labs/src/14_earning_autonomy.py)
- [Lab 13](../labs/src/13_minimax_capstone.py)
- [Evaluating voice agents](evaluating-voice-agents.md)
- [Pantheon 2026 AI roadmap](pantheon-2026-ai-roadmap.md)
- [Autonomy promotion review](../senior-engineer/autonomy-promotion.md): a judgment exercise using these tools
- [Whitepaper chapter 15, Agentic orchestration](whitepaper/15-agentic-orchestration.md): canary releases, shadow mode and supervision
- Interactive lesson: [When has the agent earned it?](https://sp7412.github.io/onboarding/lessons/earned-autonomy/) (on the site; lab 14 covers the same calculations offline)
