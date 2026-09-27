# Evaluating Voice Agents

Evaluation starts with a definition of a good customer outcome, then connects it to
quality, safety, latency, and operational measurements. A single aggregate score hides
the failures that matter most.

## Metrics

| Metric | Definition | Important cuts |
|---|---|---|
| Booking rate | Eligible service opportunities that become valid booked jobs | trade, contractor, caller intent, new/existing customer |
| Containment | Calls completed without a human transfer | intent, transfer availability, unresolved outcomes |
| Escalation correctness | Appropriate escalations divided by all escalations, plus missed-escalation rate | emergency, billing, OOD, angry caller |
| Workflow correctness | Calls whose final state and tool trajectory satisfy policy | duplicate jobs, wrong customer, unconfirmed address |
| Latency | p50/p95/p99 endpointing, first audio, tool, and useful answer times | model, network, turn type, retries |
| CSAT or customer effort | Survey or structured review of the interaction | response rate, selection bias, intent |
| Safety/privacy | Rate of unsafe action, unsupported claim, or PII leakage | severity and review status |

Report denominators and confidence intervals where practical. Booking rate without an
eligibility denominator is not a useful comparison.

## Dataset Strategy

Maintain several complementary sets:

- **Smoke set:** a few deterministic happy paths for every release.
- **Capability set:** representative booking, reschedule, billing, emergency, and
  transfer scenarios.
- **Adversarial set:** interruptions, backchannels, ambiguous confirmations, noisy
  numbers, wrong addresses, tool timeouts, duplicate requests, and prompt injection.
- **Regression set:** redacted failures from review, each with an expected outcome and
  the invariant that was violated.
- **Slice set:** scenarios selected by trade, language/accent where permitted, call
  channel, new/existing customer, and time-of-day or backend condition.

Use fictional scenarios in this repository. In a real system, define access controls,
redaction, retention, consent, and annotation policy before importing call data.

## Code Evaluators First

Use deterministic checks for facts:

- Was the selected slot actually offered?
- Was the customer verified?
- Was address confirmation grounded in the caller's transcript?
- Was an emergency never booked as routine service?
- Was a retry idempotent?
- Was the tool trajectory legal for the current phase?

Use human review or a judge for qualities that are difficult to specify, such as clarity,
tone, and whether a handoff preserved useful context. Keep these separate from hard
safety gates.

## LLM-As-Judge Risks

An LLM judge can be useful for triage, but it is not ground truth. Check for:

- preference for verbose or culturally specific language;
- self-preference when the judge and agent share a model family;
- sensitivity to transcript artifacts, ASR errors, or missing audio prosody;
- leakage of the reference answer into the judge prompt;
- poor calibration on rare, high-severity failures;
- score drift after changing the judge model or rubric.

Keep a human-labeled calibration set, blind the judge to version where possible, record
the rubric and judge version, and never let a soft judge override a hard invariant.

## Offline And Online Evaluation

Offline evaluation is repeatable and safe for release comparison, but it misses live
audio, network, caller adaptation, and distribution shift. Online evaluation sees real
conditions, but requires sampling, privacy controls, delayed labels, and rollback
discipline.

Use both:

1. Gate releases on deterministic offline invariants and representative slices.
2. Shadow or canary changes where possible.
3. Sample live traces for human review and automated monitors.
4. Add reviewed failures back to the regression set.
5. Compare business outcomes and safety metrics, not only model scores.

## OOD Detection And Routing

An OOD detector should not be treated as a single magic classifier. Combine intent
signals, confidence or abstention, policy rules, and conversation history. Examples of
OOD or restricted requests include billing disputes, unsupported trades, requests for a
human, and emergency language.

The routing policy should define:

- what evidence triggers a transfer;
- whether the detector runs before the model speaks or only after transcription;
- what safety guidance is allowed before transfer;
- what context is handed to the human;
- how false positives and missed escalations are measured.

This is close to a defense OOD problem but with asymmetric product costs: a false
positive may increase CSR load, while a missed emergency or unauthorized booking may be
far more serious. Measure both rates by slice and severity.
