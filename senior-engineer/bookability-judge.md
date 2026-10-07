# Bookability Judge

**Time:** ~45 minutes  
**Builds on:** [Evaluating voice agents](../docs/evaluating-voice-agents.md), [eval design](eval-design.md), labs 07–08, [Pantheon 2026 brief](../docs/pantheon-2026-ai-roadmap.md)

## Why this exercise exists

At Pantheon 2026, the keynote described in-product booking rates as easy to game and said
ServiceTitan built a separate voice-intelligence capability to review calls and determine
whether they represented bookable leads. That is a denominator problem with product
consequences: if the judge is wrong, agent performance, CSR coaching, and capacity decisions
can drift. This is a **company-reported product claim**, not an internal implementation detail. [1]

This exercise is fictional. You design a **public-safe** bookability definition and audit
plan for a made-up home-services call center. Do not invent ServiceTitan internal labels.

## Scenario (fictional)

You join a team that runs a voice agent for after-hours and overflow calls for plumbing and
HVAC contractors. Marketing reports "booking rate" as:

```text
bookings_created / calls_handled
```

After a prompt change, bookings_created rises 12% week over week. Support reports more
"ghost" appointments (customer says they never agreed). Dispatch reports more same-day
cancels. Leadership asks whether the agent improved or the metric was gamed.

Your job: propose a **bookability judge** that is harder to game than raw booking creates.

## Deliverable

Before writing, choose the judge's operating point. A production-quality evaluator should
be able to **pass, fail, or abstain/escalate** rather than forcing every ambiguous call into a
binary label. State what downstream decisions are allowed to use the judge and what decisions
must remain gated by the source of truth.

Write (in a private copy) one to two pages covering:

1. **Definition.** A precise definition of a "bookable lead" and of a "successful booking"
   for this fictional system. State the unit of analysis (call, lead, account, job).
2. **Inputs.** Which signals the judge may use (transcript spans, tool results, schedule
   state, customer confirmations). Mark each as observed vs inferred.
3. **Failure modes.** At least five ways a naive booking-rate metric can be gamed or
   misread (e.g. booking without consent, booking the wrong slot, counting non-leads).
4. **Judge policy.** Pass / fail / needs_human rules. Include at least one case where the
   agent created a calendar row but the judge should still fail the call.
5. **Audit sample.** How you would sample calls for human review (including rare/emergency,
   ambiguous, and high-value segments), and what agreement metric you would track between judge
   and human. State how you would handle class imbalance.
6. **Calibration and abstention.** What evidence would make you trust the judge's confidence,
   and what uncertainty threshold causes abstention rather than a forced decision.
7. **Rollout.** How you would shadow the judge before using it for agent evaluation or
   capacity decisions.

## Constraints

- Public-safe and fictional only. No real customer data.
- Prefer reversible design: the judge can be wrong; downstream systems must not treat it as
  infallible law on day one.
- Separate **lead quality** (was this worth pursuing?) from **process quality** (did the
  agent follow policy while booking?).
- Label uncertainty. If a signal is weak (garbled address, ambiguous consent), the judge
  should not silently pass.

## Self-check

A strong answer usually includes most of the following (not an answer key):

- [ ] Denominator excludes non-leads (wrong number, vendor spam, already-booked status calls)
      with an explicit rule, not a vibe.
- [ ] "Booked" requires evidence of customer agreement **and** a successful write to the
      source of truth, not merely a tool call attempt.
- [ ] At least one example where a created appointment still fails bookability (e.g. no
      consent, impossible address, policy-violating job type).
- [ ] Gaming paths are named: optimizing for creates, avoiding escalation, truncating calls,
      selecting soft slots that later cancel.
- [ ] Human audit plan has a sampling method and a disagreement process.
- [ ] Shadow mode is described before the judge affects agent scores or dispatch.
- [ ] Rare and ambiguous cases are intentionally over-sampled for audit rather than relying on
      random sampling alone.
- [ ] Confidence is calibrated and the judge has an abstain/escalate path.
- [ ] Connection is made to shared context: what the voice agent must capture so a judge (or
      downstream agent) can decide without re-listening to every call.
  See [call facts contract](../docs/call-facts-contract.md).

## After you finish

- Compare your definition to the questions in the Pantheon brief under "Questions to bring
  to the team."
- If you already did [eval design](eval-design.md), reconcile the two: the funnel and the
  judge should use the same denominator language.

## Sources

1. Investing.com, ServiceTitan Pantheon 2026 keynote summary and transcript (October 6, 2026):
   <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
