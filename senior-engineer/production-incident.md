# Exercise: Production Incident Simulation

## Scenario

At 10:05, the booking-quality dashboard shows:

- eligible inbound calls: 12,400
- successful bookings: 11,964
- baseline booking rate: 98.7%
- current booking rate: **96.5%**
- p95 response latency: 1.18 s, up from 0.91 s
- backend error rate: 0.4%, unchanged
- model error rate: unavailable
- human-transfer rate: 4.8%, up from 2.1%

A deployment occurred at 09:40.

Do not assume the deployment caused the regression.

## Investigation

Write the next five queries or observations you would request. For each, state what
decision it would enable.

Consider cohort/time-slice comparisons, trace/span latency, tool-call success and timeouts,
model/version/configuration changes, prompt/policy changes, intent distribution,
stale context, telephony health, transfer reasons, and backend state versus agent claims.

## Competing hypotheses

Rank at least five:

| Hypothesis | Evidence for | Evidence against | Confidence | Next test |
|---|---|---|---|---|
| | | | | |

## Incident response

Write:
1. immediate containment
2. diagnostic plan
3. rollback decision criteria
4. customer-impact assessment
5. permanent corrective action
6. regression test or eval that should prevent recurrence

## Senior-level extension

Assume the regression is isolated to rescheduling while new bookings are unchanged.
How does that alter your investigation?

Then assume it is concentrated in one telephony carrier.
How does that alter your response?

Separate **observed**, **inferred**, and **unknown** facts throughout.
