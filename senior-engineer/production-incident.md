# Exercise: Production Incident Simulation

**Time:** 60 minutes · **Builds on:** labs 07–08 (tracing, latency), labs 09–10 (shared context, coordination)

## Scenario

At 10:05, the booking-quality dashboard shows (all numbers fictional):

| Signal | Baseline | Now (since 09:00) |
|---|---:|---:|
| Eligible inbound calls | — | 12,400 |
| Successful bookings | — | 11,964 |
| Booking rate | 98.7% | **96.5%** |
| p95 response latency | 0.91 s | 1.18 s |
| Backend error rate | 0.4% | 0.4% |
| Model error rate | — | unavailable |
| Human-transfer rate | 2.1% | 4.8% |

A deployment happened at 09:40. Notice the window: "now" starts at 09:00, so it mixes 40
minutes before the deployment with 25 minutes after.

Don't assume the deployment caused the regression.

## Investigation

Write the next five queries or observations you would ask for. For each, state the decision it
would let you make.

Consider:

- before/after and cohort comparisons on matching time windows
- trace and span latency by stage
- tool-call success, timeouts and retries
- model, version and configuration changes
- prompt and policy changes
- the intent and channel mix
- stale context
- telephony health
- transfer reasons
- backend state vs. what the agent claimed
- changes in *other* agents that feed or consume the voice agent's facts

## Competing hypotheses

Rank at least five:

| Hypothesis | Evidence for | Evidence against | Confidence | Next test |
|---|---|---|---|---|
| | | | | |

## Incident response

Write:

1. immediate containment
2. a diagnostic plan
3. rollback decision criteria
4. a customer-impact assessment
5. a permanent corrective action
6. the regression test or eval that should prevent a recurrence

## Extensions

- The regression is isolated to rescheduling; new bookings are unchanged. How does that change
  your investigation?
- It's concentrated in one telephony carrier. How does that change your response?
- Nothing in the voice agent changed. An upstream change made a demand-generation agent send
  more callers with a different mix of jobs. How would you detect that, and is it an incident?

Separate **observed**, **inferred**, and **unknown** facts throughout.

## Self-check

A strong answer:

- Checks the arithmetic and the window first. 11,964 ÷ 12,400 = 96.5%, but the window straddles
  the deploy, so the post-deploy rate is probably worse than 96.5%. Compare 09:40–10:05 with
  the same window on a normal day.
- Notices the transfer rate rose by about as much as the booking rate fell (+2.7 points vs.
  −2.2 points). Calls are probably being *handed off*, not failing silently. Transfer reasons
  become the top query.
- Treats "backend errors unchanged" plus "latency up" as pointing at the model, the prompt, tool
  timeouts or turn-taking rather than the backend. It confirms this with per-span latency
  before believing it.
- Checks for a **mix shift** before blaming the code. If the share of hard intents rose, the
  overall rate can fall even when every slice is unchanged (Simpson's paradox).
- Defines rollback criteria in advance (for example, "if post-deploy transfer reasons are
  dominated by tool timeouts, roll back"). It doesn't wait for certainty while customers are
  affected.
- Verifies there were no false confirmations by comparing claims with backend state. A quiet
  rise in hallucinated bookings is worse than a visible rise in transfers.

---

Part of the [senior engineer judgment track](README.md).
