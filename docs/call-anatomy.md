# Call Anatomy

All calls below are fictional. Names, numbers, addresses, and companies are invented
for this repository. Each scenario is a test design prompt, not a real transcript.

## 1. Routine Booking

**Caller:** "My AC is blowing warm air. The first Tuesday morning works. Yes, that is
the right address."

**Expected path:** identify the account, classify AC repair, offer an eligible window,
read back the address, ground the confirmation in the caller's words, then create one
job.

**Failure modes:** booking before address confirmation, offering a slot outside the
customer's service area, duplicate booking after a timeout, or losing the selected
slot between turns.

## 2. Reschedule

**Caller:** "I cannot make tomorrow. Can you move my appointment to Friday afternoon?"

**Expected path:** authenticate the customer, retrieve the existing job, distinguish
rescheduling from creating a second job, offer valid replacement windows, confirm the
change, and preserve the old appointment until the new one is committed.

**Failure modes:** creating a duplicate job, cancelling before a replacement is
available, confusing a preferred day with an explicit choice, or exposing another
customer's appointment.

## 3. Emergency

**Caller:** "The furnace is off and I smell gas in the utility room."

**Expected path:** give concise public-safety guidance appropriate to the scenario,
avoid routine troubleshooting, and transfer according to the contractor's emergency
policy. The agent should not keep scheduling a routine visit.

**Failure modes:** treating the phrase as ordinary HVAC triage, asking a long series of
questions before safety guidance, booking a routine slot, or claiming emergency
response capabilities that are not verified.

## 4. Billing Question

**Caller:** "I do not recognize this charge."

**Expected path:** identify the caller without exposing account data, state that billing
requires the appropriate human or authenticated workflow, and transfer with a concise
reason and available context.

**Failure modes:** reading payment details aloud, guessing what the charge means,
issuing a refund without authorization, or transferring without preserving the reason
for the handoff.

## 5. Angry Caller

**Caller:** "You sent someone to the wrong house and now nobody is helping me."

**Expected path:** acknowledge the impact without arguing, gather only the minimum
facts needed to route the issue, and escalate when the requested recovery is outside
the agent's authority.

**Failure modes:** excessive empathy scripts, defensiveness, repeating questions already
answered, promising a technician or credit without a source-of-truth check, or failing
to mark the interaction for review.

## Annotation Template

For each test call, record:

- **Intent and expected outcome:** what should happen?
- **Safety or authorization boundary:** what must never happen?
- **Required evidence:** which caller words or backend facts support the action?
- **Allowed tools:** what is available at each phase?
- **Latency-sensitive moments:** where would silence or interruption matter?
- **Evaluation:** what can be checked by code, and what needs human review?
