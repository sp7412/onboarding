# 03 - How A Contractor Works

**Estimated reading time:** 8 minutes

## Five Takeaways

1. The workflow in this chapter is a simplified fictional model, not a description of any private system.
2. The fictional model's lifecycle is demand, triage, booking, dispatch, visit, completion, and follow-up.
3. Public product pages describe scheduling and dispatch in terms of availability, job type, skill, location, and configuration. [1][2]
4. A voice agent belongs at the intake and booking boundary, while authoritative state changes belong behind policy-controlled tools.
5. KPI definitions such as booking rate and close rate are working conventions here and must be validated per contractor.

## Fictional Lifecycle

The following is an explicitly **fictional teaching model**:

```mermaid
flowchart LR
    A[Lead] --> B[Call or request]
    B --> C[Triage and identity]
    C --> D[Eligible windows]
    D --> E[Explicit confirmation]
    E --> F[Create one job]
    F --> G[Dispatch]
    G --> H[Visit and diagnosis]
    H --> I[Estimate and work]
    I --> J[Invoice and payment]
    J --> K[Membership or follow-up]
```

In this model, triage determines whether a request is safe and in scope for routine
scheduling. Booking requires an eligible window, confirmed identity and address, and an
idempotent write. Dispatch uses policy and capacity; the visit may produce a diagnosis,
estimate, and authorized work; completion produces invoice and payment records. None of
these fictional states should be mistaken for an actual schema.

The public Scheduling Pro page says availability can be based on a dispatch board and
configurations such as buffers, arrival windows, and blocked dates. [1] The public
Dispatch Pro page describes assignment inputs including technician skill, performance,
location, and drive time. [2] These statements support the existence of those public
product concepts, not the fictional sequence's implementation details.

## The Lifecycle As A Set Of Contracts

The diagram is intentionally linear, but real work can loop. A lead can be incomplete.
A caller can change an address after a slot was proposed. A dispatch board can change
between availability lookup and commit. A visit can turn into an estimate, a return
visit, a membership opportunity, or a no-charge follow-up. The linear diagram is useful
for orientation; it is not a claim that every contractor has the same states or order.

The safer abstraction is a set of contracts between stages. Each contract declares its
inputs, permitted outputs, authority, failure behavior, and evidence. That makes it
possible to change a conversational component without making it responsible for all
downstream state. It also gives evaluation a target more precise than “the call sounded
good.”

### Lead To Intake

The lead boundary identifies the channel and captures enough context to decide whether
the request is in scope. A voice agent may collect a name, callback number, address,
trade, problem description, customer status, and preferred timing. The exact fields are
deployment-specific. The agent should distinguish what the caller said from what the
backend verified. A caller saying “I am already a customer” is a claim to check, not an
authorization token.

### Intake To Triage

Triage is a classification and routing boundary, not a diagnosis engine. It can identify
that a request is routine, missing information, outside configured service area, or in
need of a human. It should also recognize safety-sensitive language and stop making
ordinary booking promises when policy requires escalation. The public pages establish
trade workflows and booking concepts; they do not publish a universal emergency policy.
[1][2] Any specific emergency rule in a deployment must therefore be supplied by the
authorized owner.

### Triage To Availability

Availability is a constrained proposal. Scheduling Pro publicly describes real-time
availability, customer data, job types, buffers, arrival windows, blocked dates, and
other configurations. [1] The engineering implication is that a caller should be
offered only values returned by the availability authority. A model should not invent a
time because it sounds plausible. If the caller asks for a time that is not returned, the
agent should say it cannot offer that time and continue within policy.

### Availability To Commit

The commit boundary is the highest-value correctness boundary in the model. A robust
design rechecks the proposal, validates identity and address, verifies authorization,
requires explicit confirmation, and performs one idempotent mutation. If the operation
fails, the spoken response must describe failure or pending status rather than success.
If the network retries, an idempotency key or equivalent mechanism should prevent a
duplicate job. These are engineering recommendations, not public claims about a private
implementation.

### Booking To Dispatch

Dispatch is not simply “find the nearest technician.” The public Dispatch Pro page names
job type, skill, performance, location, drive time, goal settings, and route controls.
[2] A system may trade off these objectives differently, and the page does not disclose
the objective function. Therefore, a voice agent should not promise a technician,
arrival time, or special skill unless an authoritative operation has returned it.

### Visit To Completion

The visit stage produces information that may affect an estimate, work authorization,
invoice, payment, equipment history, or follow-up. The fictional model keeps these
separate because each can have a different owner and risk. A voice agent receiving a
post-visit question should retrieve the current status or transfer with context rather
than reconstructing a financial or technical record from memory.

## Roles And Handoffs

The model includes at least a caller, CSR, dispatcher, technician, manager, and system
of record. A caller supplies intent and facts. A CSR handles communication and policy
exceptions. A dispatcher manages capacity and assignments. A technician performs field
work and records results. A manager reviews exceptions and outcomes. The system of record
holds authoritative business state. These role descriptions are a teaching model, not an
internal organization chart.

Handoffs should be explicit. A transfer packet can include verified caller identity,
service address, stated intent, urgency classification, job type, offered options,
selected option, unresolved questions, and tool outcomes. It should avoid claiming that
an unverified field is true. A human should be able to see whether a booking was proposed,
confirmed, committed, rejected, or merely discussed.

## Working KPI Definitions

This paper uses the following working conventions only:

- **Answered call:** a call connected to an agent or human and reached a defined outcome.
- **Qualified request:** a call with enough information to enter the configured workflow.
- **Eligible booking:** a request for which policy and availability allow a booking.
- **Correct booking:** an eligible booking whose committed fields match the confirmed
  fields and whose backend record exists exactly once.
- **Containment:** a call completed without human transfer, with a separate correctness
  check.
- **Escalation correctness:** a transfer made when policy required it, with useful context.

Contractors may define these differently. A reported rate is meaningless without the
population, numerator, denominator, time window, and exclusions. That is why this chapter
does not present benchmark values.

## Failure And Recovery Paths

Every transition needs a recovery path. If identity cannot be verified, the agent should
ask for an allowed alternative or transfer; it should not guess. If availability becomes
stale, the agent should retrieve again and explain the change. If a commit times out, the
agent should report an unresolved status until the operation can be checked. If a human
transfer fails, the system should preserve a callback task and the context already
collected. These behaviors are analysis derived from the need to keep spoken claims aligned
with authoritative state.

Retries also need boundaries. A read can often be repeated safely, but a mutation may
create a duplicate unless the operation is idempotent. A model-level instruction such as
“do not book twice” is weaker than a backend constraint keyed by a request identifier.
Likewise, a transcript is not an audit trail unless it records the tool request, policy
decision, operation result, and time. A production design should define which evidence is
retained and who may inspect it.

## From Fictional Model To Authorized Validation

The model becomes useful after each box is replaced with an authorized contract. For each
transition, document the owner, input schema, output schema, invariants, errors, retry
semantics, privacy classification, and test fixtures. Then ask whether the voice agent may
read, propose, mutate, or never access each field. This is the point at which a generic
workflow diagram becomes a safe implementation plan, without claiming that the plan is
the current private architecture.

## Voice-Agent Insertion Points

The safest insertion point is the front door: answer, identify, gather structured facts,
classify urgency, offer eligible windows, read back the proposed state, and transfer
when policy says the agent should stop. The agent should not be the system of record for
customers, schedules, jobs, prices, or payments. **Analysis:** that separation makes
tool calls auditable and lets deterministic policy reject an invalid mutation.

## Engineer Implications

Model each boundary as a contract:

| Boundary | Minimum validation question |
|---|---|
| Caller to identity | What evidence verifies the customer and service address? |
| Triage to safety | Which signals require transfer or non-routine guidance? |
| Availability to booking | Is the slot rechecked at commit time? |
| Proposal to mutation | Was the exact job, address, and window explicitly confirmed? |
| Booking to dispatch | Which fields are required for assignment? |
| Completion to follow-up | Is the contact consented, useful, and measurable? |

## Validation Questions

- What are the real workflow states, transitions, and invariants?
- Which system owns customer, availability, job, payment, and communication state?
- What does “booked” mean operationally and analytically?
- What retries, conflicts, and cancellation policies exist at commit time?
- Which fields may a voice agent read, propose, mutate, or never access?

## Sources

1. ServiceTitan, “Scheduling Pro,” checked September 27, 2026: <https://www.servicetitan.com/features/pro/scheduling>
2. ServiceTitan, “Dispatch Pro,” checked September 27, 2026: <https://www.servicetitan.com/features/pro/dispatch>
