# 04 - The Contact Center

**Estimated reading time:** 7 minutes

## Five Takeaways

1. Contact Center Pro is publicly positioned as a trades-focused contact-center product with multi-location call handling. [1]
2. Its page describes calls linked to jobs and an inbox intended to centralize interactions. [1]
3. The page positions AI Virtual Agents for overflow and after-hours handling, booking, confirmation, rescheduling, and escalation. [1]
4. Published customer outcomes are attributed to named customer cases and are not general industry benchmarks. [1]
5. Public sources do not establish general call mix, peak distribution, CSR turnover, missed-call cost, or staffing requirements. Those items are [unverified].

## Public Operating Picture

The Contact Center Pro page describes a multi-location contact center built for the
trades, with calls in one inbox and calls linked to the appropriate job. [1] It also
describes AI Manager Assist features such as call summaries, sentiment analysis, and
second-chance lead identification. [1] These are product-page descriptions and should be
treated as positioning until implementation and performance are independently validated.

The same page positions AI Virtual Agents for overflow and after-hours calls and lists
booking based on real capacity, appointment rescheduling and confirmation, and live
escalation. [1] A useful operational interpretation is a constrained workflow with a
human fallback, not an unconstrained FAQ bot.

## Contact Center Work Is Not One Intent

An inbound contact center is a routing system as much as a conversation system. The
caller may want to start service, ask about an existing appointment, reschedule, confirm,
provide information, request an estimate, discuss a membership, report a problem, or
reach a person. The public Contact Center Pro page names calls linked to jobs, an inbox,
manager-assist functions, and AI Virtual Agent capabilities. [1] It does not publish a
general distribution of intents. This chapter therefore treats the list as a design
inventory, not a call-mix statistic.

Each intent should have an allowed action set. A confirmation may require retrieval but
not mutation. A reschedule requires retrieval, eligibility, a new proposed window, and a
confirmed mutation. A new booking requires intake and availability. A request that is
outside configuration should produce a transfer or callback task. The model may choose
which path to propose, but a policy layer should determine which tools are callable.

## Peaks, Overflow, And After Hours

The product page explicitly positions AI Virtual Agents for overflow and after-hours
handling. [1] Scheduling Pro also publicly describes booking at any time and a customer
experience that can capture requests outside ordinary office coverage. [2] These sources
support a deployment pattern, not a universal claim that demand peaks at a particular
hour or that after-hours calls are more valuable.

An after-hours experiment should define the baseline first. Is the comparison a voicemail,
an answering service, a callback queue, a human night shift, or no response? What counts
as an eligible call? What is the allowed transfer destination? What happens when the
caller requests an unsafe or unsupported action? A good experiment measures valid
completion and safe escalation alongside answer rate, containment, and booking.

Overflow has a similar requirement. If the agent handles calls only when a queue is full,
the routing policy should be observable. Otherwise a change in staffing, advertising, or
weather can be mistaken for an AI effect. The public page's customer outcomes are
attributed to Bonney Plumbing, Electrical, Heating and Air and should not be generalized.
[1]

## CSR Workflow And Manager Review

The Contact Center Pro page describes AI call summaries, sentiment analysis, and second-
chance lead identification. [1] These features suggest a manager-review workflow in
which a human can inspect calls and recover missed opportunities. They do not establish
how a contractor defines sentiment, lead quality, review priority, or success.

For engineering, summaries should be treated as derived evidence rather than an
authoritative business record. A summary can omit a negation, confuse a proposed slot
with a booked slot, or misstate who made a commitment. A useful review interface should
link summary fields to transcript spans, tool calls, backend results, and transfer
outcomes. When a reviewer corrects a field, that correction can become a labeled example
or an evaluation case, subject to privacy and retention policy.

## Capacity-Aware Booking

The public product language emphasizes real capacity and links calls to jobs. [1] This
is stronger than a generic calendar promise because the valid answer depends on the
contractor's configured operating model. It still does not disclose the schema or
conflict behavior. The agent should ask only questions needed to select a job type and
retrieve eligible options. It should read back the exact selected window and confirm
before commit. A successful tool response, not the model's intention, determines whether
the agent may say “booked.”

## Human Escalation As A Product Feature

Escalation is not an admission that the agent failed. It is a controlled outcome for
unsupported, ambiguous, high-risk, or customer-preferred interactions. The public AI
Virtual Agent page lists live escalation and configurable greetings, job types, dispatch
fee messaging, transcripts, summaries, and call classification. [3] Those capabilities
make escalation design explicit: when to transfer, what context to send, what the caller
hears during transfer, and what happens if no human answers.

A transfer without context simply moves the cost to another queue. A useful transfer
packet should include the reason, verified facts, caller's desired outcome, options
already offered, and any error or restriction returned by the backend. Metrics should
separate transfer rate from transfer correctness and resolution after transfer.

## Attributed Outcomes And Measurement Discipline

The page reports 60% fewer missed calls, a 17% increase in booking rate, a 97% lead-to-
booked-call rate, and an 11% booking increase for Bonney. [1] These statements are
customer-case-study material presented by the vendor. They do not disclose enough here
to establish a common denominator, comparison period, selection process, or causal effect
for another contractor. They should be retained only with attribution and caveats.

The measurement design should record call id, channel, tenant or location scope,
timestamp, intent, eligibility, action, transfer, backend result, and later correction or
cancellation. Privacy controls and retention rules are not specified by these product
pages and remain deployment questions. Aggregate numbers should be sliceable by trade,
time, new/existing customer, after-hours status, and failure mode.

## Queue Design And Fallback

Even a successful AI path needs a queue model. The queue may contain a live transfer,
callback request, unresolved booking, review task, or exception generated by a backend.
These are different work items. A single “escalated” label hides whether a human received
the caller, whether the context arrived, and whether the issue was resolved.

The fallback state should be designed before the agent is deployed. If the agent cannot
reach a human, it should tell the caller what will happen next and record the minimum
context needed for that next action. If the call is urgent or unsafe, a generic callback
promise may be insufficient; the applicable policy owner must define the route. This
chapter does not state a universal emergency protocol.

## Quality Review As A Feedback Loop

Manager review can turn production failures into a maintained evaluation set. A reviewer
can label intent, eligibility, confirmation quality, transfer quality, and backend-state
agreement. The labels should preserve uncertainty and disagreement rather than forcing a
false binary. Repeated failures can become targeted offline tests, while sampled online
checks can detect distribution changes after a prompt, model, policy, or configuration
change.

The feedback loop must respect privacy and retention rules. Public product pages describe
transcripts and summaries, but do not specify a universal retention schedule or access
policy. [2] Those controls remain deployment requirements to validate with the relevant
owners.

## Attributed Outcomes

The page reports that Bonney Plumbing, Electrical, Heating and Air saw 60% fewer missed
calls and a 17% increase in booking rate, while the page headline also says bookings
increased by 11%. [1] These figures are customer-case-study claims presented by the
vendor; the page does not provide enough context here to treat them as comparable or
causal estimates for all contractors. They should remain attributed, dated, and paired
with denominator and study-design questions.

## Engineer Implications

**Analysis:** A call-center agent needs explicit routing states: in scope, needs more
information, safe to book, needs a human, and emergency or restricted. Each state should
have allowed tools, required evidence, transfer context, and observable outcomes.

**Hypothesis:** Overflow and after-hours are good candidates for controlled experiments
because the baseline, transfer policy, and eligibility rules can be defined before
optimizing conversational style. The experiment must measure missed-escalation and
workflow correctness alongside containment or booking.

## Validation Questions

- What are the actual inbound intents and their proportions by time and season?
- What are the queue, transfer, callback, and after-hours service-level definitions?
- Which calls may be booked, confirmed, or rescheduled without a human?
- What context must accompany a transfer, and how is transfer success measured?
- What denominators, dates, and counterfactuals support every customer outcome claim?

## Sources

1. ServiceTitan, “AI-Powered Contact Center for the Trades | Contact Center Pro,” checked September 27, 2026: <https://www.servicetitan.com/features/pro/contact-center>
2. ServiceTitan, “AI Virtual Agent,” checked September 27, 2026: <https://www.servicetitan.com/features/pro/virtual-agent>
