# Autonomy Promotion Review

**Time:** ~45 minutes  
**Builds on:** [Earning autonomy](../docs/earning-autonomy.md), [lab 14](../labs/14_earning_autonomy.ipynb), [bookability judge](bookability-judge.md), [whitepaper chapter 15](../docs/whitepaper/15-agentic-orchestration.md), [whitepaper chapter 17](../docs/whitepaper/17-running-agents-in-production.md)

## Why this exercise exists

A promotion request usually arrives as one good-looking number. The senior engineer's job is
to ask what was counted, for which traffic, measured by whom, and what a wrong call costs.
Lab 14 gives you the tools (a Wilson bound, a minimum sample, a cost threshold, calibration
and a drift guard). This exercise asks you to use them on a messy, realistic request and
defend the decision in writing.

Everything here is fictional: the company, the levels, the segments and the numbers. The
level names and targets match lab 14's teaching policy, not any real system.

## Scenario (fictional)

A booking agent for a made-up HVAC and plumbing call center runs at level 2, **act and
notify**: it books routine work itself and a CSR reviews a notification afterwards. The
product manager asks to promote it to level 3, **act autonomously within limits**, before peak
season. Lab 14's policy promotes from level 2 only when the 95% upper bound on the error rate
is below **5%**, with at least **200** samples per decision.

The request includes this table, built from the last eight weeks:

| Segment | Calls handled | Booking errors found | Error rate |
|---|---:|---:|---:|
| A. Routine HVAC tune-ups | 1,200 | 30 | 2.5% |
| B. Water heater repairs | 260 | 9 | 3.5% |
| C. Plumbing leaks (launched three weeks ago) | 90 | 1 | 1.1% |
| D. After-hours "no cooling" calls | 140 | 11 | 7.9% |
| **All segments** | **1,690** | **51** | **3.0%** |

Other facts in the request:

- "Booking errors found" are bookings a CSR reversed while reviewing the notification. Nobody
  audits bookings the CSR approved, and nobody audits calls the agent declined to book.
- A wrong booking costs about **$180** (a wasted truck roll and a goodwill credit). A missed
  booking costs about **$350** in gross profit.
- The extractor's expected calibration error is 0.03 overall and 0.11 on segment D.
- A heat wave is forecast. During last summer's heat wave, the weekly call mix moved from
  50/30/15/5 (A/B/C/D) to 38/27/15/20 within a week (a different season from the eight
  weeks above, so the mixes don't match the table). The drift guard pauses autonomy when PSI exceeds 0.25.
- The PM's summary: "3.0% is well under the 5% target. Ship it."

## Deliverable

Write (in a private copy) a one-page decision memo:

1. **Decision per segment.** Promote, hold or demote each segment, with the bound you
   computed and the rule that decided it. Lab 14's `promotion_policy(errors, n, 2)` will check
   your arithmetic.
2. **The pooled number.** Say in one paragraph why the all-segments row can say "promote"
   while one segment shows evidence of being worse than the target.
3. **The measurement.** What is wrong with "errors found by the reviewing CSR" as the
   numerator? Name the errors it cannot see, and say what you would audit before trusting any
   bound built on it.
4. **Cost.** Compute the cost threshold. What does it imply for borderline bookings, and why
   is calibration on segment D the number that makes this threshold unsafe to use there?
5. **Drift.** Compute PSI for last summer's shift, compare it with the 0.25 limit, and say what
   you would do before the heat wave rather than after it.
6. **What you'd ship.** The smallest promotion you would approve, its rollback trigger and
   owner, and the one new measurement you would add first.

## Constraints

- Promotion is per segment. A pooled number never promotes a segment on its own.
- Too little data is a reason to hold, never to demote. Clear evidence of harm is different:
  lab 14 demotes on the lower bound even before the minimum sample, because losing
  autonomy should be faster than earning it.
- Treat any numerator you can't audit as a lower bound on the true error count.
- Keep it fictional. Don't import anything learned inside a real company.

## Self-check

A strong memo usually includes most of the following (not an answer key):

- [ ] Arithmetic matches lab 14: the pooled upper bound is about 3.9%, segment A's about
      3.5% (promote), B's about 6.4% (hold), C is held for sample size (90 of 200), and D's
      bound runs from about 4.4% to 13.5%.
- [ ] Segment D is not waved through because it is "only" 140 calls: even its optimistic
      (lower) bound of about 4.4% is close to the 5% target. It is held for sample size, not
      demoted (its lower bound is under level 2's 10% bar), and gets a focused audit before the
      season in which it grows.
- [ ] The pooled 3.0% is identified as an average dominated by easy tune-up calls, the same
      shape as lab 14 section 7, "Aggregates hide weak segments".
- [ ] The numerator problem is named: reviewers see only what they reverse, so approved bad
      bookings and wrongly declined calls are invisible. A random audit of approved bookings
      and of declines comes first.
- [ ] The cost threshold is about 0.34 (180 ÷ 530), so the business should book when it is
      more than about one-in-three sure. That only works if confidence is calibrated, which
      segment D's 0.11 error says it isn't.
- [ ] PSI for last summer's shift is about 0.24, just under the limit, and the memo says so
      rather than rounding it into "stable". A heat wave on top of that is a reason to watch
      the guard daily, not to relax it.
- [ ] The shipped change is small and reversible: promote segment A only, with a named owner,
      a rollback trigger stated as a bound (not a vibe), and a re-validation date.

## After you finish

- Run lab 14 sections 6 and 7 (drift and aggregates) again with this exercise's numbers.
- Compare your measurement critique with the [bookability judge](bookability-judge.md): both
  are about who decides what counts as an error.
- Add your open questions about autonomy levels to your private
  [working hypotheses](hypotheses.md).
