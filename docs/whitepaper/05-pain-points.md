# 05 - Pain Points

**Estimated reading time:** 8 minutes

## Five Takeaways

1. Public product pages frame missed calls, booking availability, after-hours demand, and dispatch efficiency as contractor problems the products address. [1][2][3]
2. A product page demonstrates vendor positioning, not prevalence or causal impact.
3. Each pain point should become a falsifiable hypothesis with a baseline, denominator, guardrail, and time window.
4. The highest-risk failure is not merely a poor answer; it is an incorrect state change such as an unauthorized or wrong booking.
5. Internal priority, trusted metric, and actual economic impact are [unverified] until validated with authorized operational data.

## Pain-Point Taxonomy

| Pain point | Public evidence | Engineering translation | Outcome to measure |
|---|---|---|---|
| Missed calls | Contact Center Pro says it aims to reduce missed calls and centralize calls. [1] | Detect unanswered/abandoned paths; preserve callback and transfer context. | Answered-call rate, qualified lead recovery, transfer correctness. |
| After-hours coverage | Scheduling Pro describes booking 24/7; Contact Center Pro describes overflow and after-hours AI handling. [1][2] | Gate actions by schedule, capacity, and escalation policy. | Eligible bookings, safe containment, after-hours escalation. |
| Capacity mismatch | AI Virtual Agent and Scheduling Pro describe real-time or configured availability. [1][2] | Recheck availability at commit; make slot selection and policy observable. | Valid booking rate, conflict rate, reschedule rate. |
| Dispatch mismatch | Dispatch Pro describes assignment using skill, location, drive time, and performance. [3] | Treat assignment as constrained optimization with human override. | Assignment validity, travel-time proxy, rework or reassignment. |
| Data and handoff gaps | Contact Center Pro describes linking calls to jobs and summaries. [1] | Carry structured context across agent, CSR, job, and review systems. | Handoff completeness, correction rate, review time. |

## What Cannot Be Generalized

The pages do not establish that any listed pain has a universal frequency, cost, or rank.
The Contact Center Pro page reports customer-specific results, including fewer missed
calls and increased booking rate for Bonney Plumbing, Electrical, Heating and Air. [1]
Those results remain attributed to that case study. The page does not establish that the
same change will occur for another contractor, trade, geography, staffing model, or
baseline.

The following remain **[unverified]**: general missed-call cost, CSR turnover, technician
shortage, marketing waste, cash-flow impact, schedule mismatch prevalence, and customer
expectation failure rates. The correct next step is measurement design, not a borrowed
benchmark.

## Turning A Pain Point Into A Testable Claim

“Missed calls are expensive” may be true for a particular contractor, but it is not yet
a testable claim. A testable version names the population, time window, baseline, and
desired outcome: among inbound calls in a defined channel and period, does a configured
answering path increase the share that reaches a valid outcome without increasing unsafe
or incorrect transactions? The result can then be measured without pretending that all
calls, contractors, or seasons are alike.

The same discipline applies to “AI books more jobs.” The denominator could be all calls,
qualified new leads, eligible requests, or calls presented to the agent. The numerator
could be proposed bookings, committed bookings, or bookings that remained valid after a
later correction. These quantities are not interchangeable. Public product pages describe
capabilities and customer results, but they do not settle a universal definition. [1][2]

## Missed Calls And Lead Recovery

The Contact Center Pro page positions centralized call handling as a way to miss fewer
leads and reports a customer case with fewer missed calls. [1] The engineering problem
has at least three layers: detecting that a call was not answered, preserving enough
context to recover it, and determining whether recovery produced a valid business
outcome. A callback task with no intent or contact context may be operationally weak even
if the call was technically logged.

Useful measures include answered-call rate, abandonment rate, callback completion,
qualified-request rate, transfer correctness, and later correction. A system should
distinguish a caller who hung up before any interaction from a caller whose call was
answered but abandoned during a long workflow. Without that distinction, a single
“missed” number can hide different interventions.

## After-Hours Coverage

Scheduling Pro publicly promotes booking outside ordinary office coverage, and Contact
Center Pro positions AI for after-hours and overflow. [1][2] The benefit hypothesis is
that an eligible caller can reach a useful outcome when a human CSR is unavailable. The
guardrails are that the agent must honor service area, capacity, job-type, identity,
disclosure, and escalation policies.

An after-hours test should compare equivalent periods or a randomized routing policy when
possible. It should report eligible requests separately from unsupported requests. A
higher containment rate is not an improvement if it comes from failing to transfer a
caller who needed a human. The release criterion should include unsafe non-escalation and
incorrect booking, not only speed or containment.

## CSR Turnover And Knowledge Transfer

CSR turnover is listed in the plan as a research gap, not a sourced industry statistic.
The public pages do support a narrower engineering question: can call summaries,
classification, and structured context reduce the amount of information a human must
reconstruct? Contact Center Pro publicly describes summaries, sentiment analysis, and
second-chance leads. [1]

That question can be tested without claiming a turnover rate. Measure review time,
correction rate, handoff completeness, time to first useful action, and agreement between
the summary and transcript or tool trace. A summary should never be the only evidence for
a financial commitment or safety decision. The human needs access to the underlying call
and the authoritative operation result.

## Technician And Dispatcher Constraints

“Technician shortage” and “dispatch inefficiency” are distinct claims. The public
Dispatch Pro page describes skill, performance, location, drive time, goal-based settings,
and job-value prediction. [3] This supports an engineering model of constrained
assignment. It does not establish how common a shortage is or that any public percentage
applies broadly.

A voice agent can make this problem worse by booking demand without checking the same
constraints used downstream. Therefore, booking and dispatch tests should share job type,
required skill, location, duration, and capacity fixtures. The measured outcomes can be
valid booking, reassignment, conflict, drive-time proxy, and human override. Any revenue
or efficiency result must identify its customer, period, baseline, and method.

## Marketing Waste And Attribution

The public product catalog includes marketing and lead-generation capabilities. [2] It
does not establish a general rate of wasted marketing spend or prove that a voice agent
caused an increase in return. An attribution design should preserve the source channel,
campaign, call, qualification state, booking state, and later job outcome. It should also
account for callers who would have booked through another channel.

The safe claim is therefore conditional: better capture and correct routing may improve
the observable path from lead to job if the baseline and counterfactual support that
interpretation. This is a `Hypothesis:`, not a result. A controlled holdout or a carefully
matched comparison is stronger than before-and-after totals alone.

## Data Silos And Cash Flow

The workflow model in chapter 03 identifies customer, job, schedule, dispatch, invoice,
payment, and follow-up as potentially different state boundaries. The public products
page names accounting and payments among the broader platform capabilities. [2] That
does not prove the absence or presence of silos for any customer.

The engineering response is to make cross-system state explicit. A tool response should
identify the operation, record identifier, status, timestamp, and retry behavior. Payment
questions should be routed through the authorized payment flow rather than collected as
free-form sensitive text. Cash-flow impact should be measured with a defined attribution
window and reconciled financial source, not inferred from bookings.

## Failure Modes And Falsifiable Hypotheses

Each pain point should produce both a benefit hypothesis and a harm hypothesis:

| Pain point | Benefit hypothesis | Harm to rule out |
|---|---|---|
| Missed calls | More callers reach a valid outcome. | More low-quality callbacks or duplicate leads. |
| After hours | More eligible requests are handled safely. | Restricted requests are contained instead of escalated. |
| Capacity | More valid options are presented. | Stale availability creates conflicts. |
| Dispatch | Better assignments reduce avoidable rework. | Optimization favors a proxy while violating policy. |
| Handoffs | Humans receive better context. | Summaries omit decisive facts or overstate certainty. |

The second column is often more important than the first. A system that improves a
headline metric while creating silent state errors is not a successful automation.

## Engineer Implications

**Analysis:** For each pain point, define `population`, `eligible denominator`, `desired
state`, `guardrails`, and `review label` before selecting a model metric. A booking-rate
increase without eligibility and correctness is not sufficient evidence of improvement.

**Hypothesis:** A small offline suite can expose the most important transaction failures:
wrong customer, unoffered slot, missing confirmation, duplicate retry, restricted request
booked, and transfer without useful context. Live monitoring can then add latency,
distribution shift, and human-review outcomes.

## Validation Questions

- Which pain point is highest priority, and who owns its baseline?
- What is the trusted denominator for booking, containment, and missed-call measures?
- Which safety and privacy metrics are release-blocking?
- How are weather, seasonality, trade, customer type, and after-hours slices defined?
- What customer outcomes can be attributed to the system rather than to demand or staffing changes?

## Sources

1. ServiceTitan, “AI-Powered Contact Center for the Trades | Contact Center Pro,” checked September 27, 2026: <https://www.servicetitan.com/features/pro/contact-center>
2. ServiceTitan, “Scheduling Pro,” checked September 27, 2026: <https://www.servicetitan.com/features/pro/scheduling>
3. ServiceTitan, “Dispatch Pro,” checked September 27, 2026: <https://www.servicetitan.com/features/pro/dispatch>
