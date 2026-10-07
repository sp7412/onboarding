# Voice-Agent Capstone Rubric

This rubric is the acceptance test for lab 08 and the pre-start path. Use fictional data
only. A pass requires evidence for every hard criterion; an unanswered criterion is not a
pass.

## Pass/fail criteria

| Criterion | Pass condition | Evidence to produce | Demonstrated by |
|---|---|---|---|
| Grounded slot confirmation | The booking path refuses an offered-but-unconfirmed slot and accepts only a choice grounded in the latest caller text. | Tool result and test output for refusal and success. | Lab 02; `tests/test_stlab.py` slot-choice tests |
| Grounded address confirmation | The booking path refuses `create_job` until the service address confirmation is grounded in the latest caller text. | Tool result and test output for refusal and success. | Lab 02; `tests/test_stlab.py` address tests |
| Claim grounding | The agent does not claim a mutation succeeded unless the backend recorded the change. | Trace or transcript showing a failed mutation and corrected response. | Lab 07; `claims_grounded` evaluator |
| Emergency escalation | Emergency language blocks routine mutation tools and transfers to a human. | Scenario result showing blocked routine action and successful transfer. | Lab 02; `tests/test_stlab.py` emergency test |
| Safe retries | Repeating the same mutation with the same idempotency key returns the original result and creates no duplicate. | Before/after job or appointment state plus replay result. | Lab 00; backend idempotency tests |
| Disconnect handling | A simulated interruption or disconnect does not invent completion; the workflow can resume or reports an unresolved state. | State checkpoint and recovery transcript, or explicit unresolved outcome. | Lab 06; lab 08 failure-mode exercise |
| Same-day policy | Same-day reschedule/cancel requests are refused by the backend and routed to human handling. | Policy error and unchanged appointment state. | Lab 02; direct backend tests |
| Audit evidence | The run records caller text, tool calls, policy results, final state, and evaluator outcome without secrets or personal data. | Redacted trace or structured evaluation report. | Labs 07–08; `labs/stlab` audit log |

## Required submission

1. Run labs 00–08 offline.
2. Attach one short fictional transcript or trace for each failed-path criterion.
3. Attach the evaluator output and identify any criterion that remains unverified.
4. Write the study-question answer only in `notes/study-question.md`; do not copy private or
   employer-internal material into this public repository.

**Pass rule:** all eight criteria have evidence, no hard policy is bypassed, and the report
distinguishes simulated behavior from any live measurement.

## Extension: multi-agent and autonomy criteria (labs 09–14)

Optional, and separate from the pass rule above. Use these when you run labs 09–14 (the
plan schedules them before day one and in weeks 2–3). The same evidence standard applies.

| Criterion | Pass condition | Evidence to produce | Demonstrated by |
|---|---|---|---|
| Facts before action | A proposed fact is invisible to consumers until the control plane verifies it, and an agent cannot write a key it isn't permitted to. | Ledger view before and after verification, plus a `not_permitted` refusal. | Lab 09; `tests/test_multiagent.py` ledger tests |
| Hard constraints survive arbitration | The arbiter never trades away consent, emergencies or capacity, however much value a proposal claims. | One rejected high-value proposal and the constraint that rejected it. | Lab 10; arbitration test |
| Outside agents are untrusted callers | The agent gateway refuses a bad signature, a replayed nonce, an unoffered slot and a missing scope, retries are idempotent, and it does not reveal whether a phone number is a customer. | Gateway refusals and an idempotent replay. | Lab 12; gateway tests |
| Costliest extraction error named | You identify which CallFacts error costs the most and show a sensitivity number for it, and emergencies are never booked even when the extractor misses them. | The lab 13 sensitivity table with the top row explained. | Lab 13; `tests/test_minimax.py` |
| Promotion is earned, not assumed | A promotion decision cites a bound on the error rate against a target, a minimum sample, the cost threshold, and a drift guard that pauses on a shifted population. | The lab 14 decision table and one drift-paused example. | Lab 14; `tests/test_autonomy.py` |

