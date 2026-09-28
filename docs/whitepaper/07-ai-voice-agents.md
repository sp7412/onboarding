# 07 - AI Voice Agents In The Trades

**Estimated reading time:** 8 minutes

## Five Takeaways

1. Public positioning centers on booking, confirmation, rescheduling, and escalation. [1]
2. Capacity, job type, location, and skill are business constraints, not conversational
   decoration. [1]
3. Customer-reported booking rates and implementation times are not general benchmarks.
4. A safe agent separates proposal, confirmation, mutation, and evidence.
5. Evaluation should score both conversation and committed state.

## A Claims Chain

The chain from utterance to outcome is: audio, transcript, intent, structured facts,
policy decision, availability proposal, explicit confirmation, mutation result, and
spoken response. A failure at any link can make the final claim false. The AI Virtual
Agent page describes real-time booking, native workflows, adaptive capacity, appointment
confirmation, rescheduling, and live escalation. [1] Those public capabilities support
this chain as an engineering model, not a claim about private implementation.

## Deployment Shapes

Overflow and after-hours are bounded starting points because their routing policy can be
defined. Existing-customer confirmation and rescheduling are also distinct workflows,
not generic chat. A deployment should specify eligibility, allowed tools, transfer rules,
and rollback before optimizing voice style. The agent should be able to say “I could not
complete that” when the operation did not commit.

## Public Results

The page includes attributed customer statements and reports one customer's booking rate
and talk-time experience. [1] The figures are not comparable without denominator, period,
selection, and counterfactual. They remain customer evidence, not an industry promise.

## Evaluation Design

Use fictional scenarios for new booking, reschedule, confirmation, unavailable slot,
duplicate retry, identity mismatch, restricted request, and human transfer. Label exact
state transitions. Include trade, residential/commercial, new/existing, after-hours, and
backend-error slices. A fluent transcript is not a pass if the booking is wrong.

## Sources

1. ServiceTitan, AI Virtual Agent: <https://www.servicetitan.com/features/pro/virtual-agent>
2. ServiceTitan, Contact Center Pro: <https://www.servicetitan.com/features/pro/contact-center>
