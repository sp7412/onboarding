# 12 - Risks And Failure Modes

**Estimated reading time:** 8 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. The most dangerous failures are silent ones: the agent says something happened that
   didn't (or books something wrong) and nobody notices until a technician shows up.
2. Safety emergencies (gas, carbon monoxide, electrical, flooding) must override every
   booking flow.
3. Reliability has to be measured across repeated trials, not single demos; research
   benchmarks for customer-service agents show large drops when the same task is repeated. [1]
4. Legal and privacy risks (AI-voiced outbound calls, recording consent, payment data) are
   design constraints, not afterthoughts. [2][3][4]
5. ServiceTitan's own 10-K flags AI competition, regulatory and reputational risks; a bad
   agent experience threatens contractor trust, which underpins retention above 95%. [5]

## Risk register

| Risk | Example | Severity | Mitigations | How to evaluate |
|---|---|---|---|---|
| **Missed emergency** | Caller mentions a gas smell while booking a tune-up | Critical | Screen every utterance; safety script; immediate human transfer; tool lock-down | Emergency scenarios in every eval run; zero-tolerance metric |
| **False confirmation** | "You're all set" after a failed booking | High | Claim guard comparing speech with committed state; correct out loud | Claim-grounding evaluator (lab 07) |
| **Wrong booking** | Wrong customer, address, job type or window | High | Verify identity and address; offer only valid windows; confirmation before commit | State-level correctness on labeled scenarios |
| **Duplicate booking** | Retry after a timeout books twice | Medium–High | Idempotency keys owned by the app | Fault-injection tests |
| **Unauthorized commitments** | Quoting prices, promising same-day, discussing financing terms | High | Tool and prompt limits; escalate pricing and financing | Red-team prompts; transcript audits |
| **Acting on the wrong record** | Changing another customer's appointment | High | Identity from caller ID and verification, not model arguments; ownership checks | Adversarial and confusion scenarios |
| **Over- or under-escalation** | Transferring everything, or never | Medium | Explicit escalation policy; measured reasons | Escalation-correctness labels |
| **Hearing failures** | Accents, Spanish-speaking callers, noise, poor connections, speakerphones | Medium–High | Robust speech models; confirmation read-backs; language routing | Slice evals by audio condition and language |
| **Vulnerable callers** | Elderly callers, distressed callers | Medium | Slower pacing, easy human transfer | Scenario coverage; complaint review |
| **Adversarial callers** | Prompt injection by voice, social engineering for account data | Medium | Never expose other customers' data; policy outside the model | Red-team scripts |
| **Regulatory breach** | AI-voiced outbound call without consent; recording without notice | High | Consent store; jurisdiction-aware notices (chapter 10) | Compliance test suite |
| **Payment data exposure** | Caller reads a card number to the agent | High | Out-of-band payment capture; transcript redaction | Redaction tests on traces and datasets |
| **Outages and slowness** | Model, telephony or backend degraded on a peak day | High | Timeouts, fallbacks to humans or voicemail, capacity planning | Chaos and load tests at peak volume |

## Reliability is a distribution, not a demo

The τ-bench benchmark evaluates tool-using agents in simulated customer-service domains by
checking the final database state against policy, and introduces pass^k: the chance an agent
succeeds on *all* of k repeated trials of the same task. Its results showed agents that pass
a task once often fail it on repeats. [1] Analysis: a voice agent handling thousands of calls
a day needs consistency, so evaluations should repeat scenarios and report the worst case,
not the best.

## Legal and trust risks

- AI-generated voices are "artificial" under the TCPA, so outbound AI-voiced calls need prior
  express consent absent an emergency or exemption. [2]
- Recording consent varies by state (chapter 10).
- Payment card data falls under PCI DSS; keep it out of model context. [3]
- Consumer privacy laws such as the CCPA give callers rights over their data. [4]
- The 10-K notes risks from AI (including competitors adopting it faster), laws restricting
  calls and texts, and reputational harm. [5]

## Business risk

Analysis: ServiceTitan's customers keep it because the platform runs their business (gross
dollar retention above 95%). [5] A voice agent that mishandles a contractor's customers
damages the contractor's brand, and that damage lands on the platform relationship. The Max
program ties the company's strategy even more tightly to AI working well. [6]

## What this means for a voice-agent engineer

- Rank risks by severity × likelihood × detectability, and invest most in the silent ones.
- Every risk in the table should map to a guardrail *and* an evaluator.
- Keep a living red-team scenario set, and grow it from production incidents.

## Questions to validate after joining

- What incidents have occurred, and how were they detected?
- Which of these risks have explicit owners and metrics today?
- How are languages other than English and difficult audio handled?

## Sources

1. Yao et al., "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains" (2024): <https://arxiv.org/abs/2406.12045>
2. FCC Declaratory Ruling FCC 24-17: <https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf>
3. PCI Security Standards Council, PCI DSS: <https://www.pcisecuritystandards.org/standards/pci-dss/>
4. California Department of Justice, CCPA: <https://oag.ca.gov/privacy/ccpa>
5. ServiceTitan Form 10-K, fiscal 2026 (Risk Factors; retention): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
6. ServiceTitan fiscal Q2 2027 results: <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm>
