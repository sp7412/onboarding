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
