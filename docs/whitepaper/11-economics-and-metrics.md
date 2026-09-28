# 11 - Economics And Metrics

**Estimated reading time:** 6 minutes

## Five Takeaways

1. Economics needs denominators, attribution windows, and a counterfactual.
2. Booking volume is not equivalent to valid or profitable work.
3. Customer case-study figures remain attributed and non-generalizable. [1]
4. Safety and correctness metrics are guardrails, not secondary outcomes.
5. Private costs, prices, margins, and attribution windows are `[unverified]`.

## A Unit Model

For a defined period, an illustrative contribution model is:

`incremental value = valid incremental jobs x contribution per job - incremental system cost - avoidable harm`.

Every term needs a local definition. “Valid” can require successful commit, no duplicate,
correct address and window, later completion, and an acceptable cancellation rate.
Contribution is not the same as booking revenue. System cost may include telephony,
inference, tooling, human review, and implementation. No numeric inputs are invented here.

## Metric Families

Track funnel metrics, state metrics, human metrics, and customer outcomes separately:

- Funnel: answered, qualified, offered, confirmed, committed.
- State: conflict, duplicate, unauthorized, stale, corrected, cancelled.
- Human: transfer, context completeness, review time, escalation correctness.
- Outcome: completed job, repeat contact, customer satisfaction, attributed value.

The Contact Center page reports customer-specific booking and missed-call outcomes. [1]
Those are evidence for measurement questions, not a universal expected lift.

## Attribution And Seasonality

Before-and-after comparisons can be confounded by weather, staffing, campaigns, pricing,
seasonality, or product configuration. A holdout, matched comparison, or interrupted time
series may be stronger, but the method depends on traffic and operational constraints.
The result must state what was measured and what was not identified causally.

## Sources

1. ServiceTitan Contact Center Pro: <https://www.servicetitan.com/features/pro/contact-center>
2. Repository evaluation guide: [evaluating voice agents](../evaluating-voice-agents.md)
