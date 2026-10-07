# Call Facts Contract

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

Public-source framing only. Pantheon 2026 described a coordination system where agents
share context and judgment: "What the voice agent hears, the dispatch agent will know."
Lead scoring was described as using what was said on the call, the customer's tone, and
details about the home, homeowner, and equipment. [1][2]

This note is a **teaching schema** for what a voice agent might need to capture so that
downstream agents can act. It is not an internal ServiceTitan schema, API, or product
spec. After joining, replace every field with the real contract the team uses.

## Why a contract matters

Without an explicit contract:

- The model invents fields that dispatch cannot consume.
- Confidence is implicit ("sounds urgent") and cannot be audited.
- Booking becomes a free-form string instead of a verified proposal.
- Learning-loop outcomes cannot be tied back to specific call signals.

The pattern taught in this repo still holds:

**The model proposes → the application controls → the source of truth verifies.**

Call facts are the model's proposals about the world. The control plane decides what is
written, with what confidence, and under which policy. The source of truth (CRM, schedule,
job record) is the only place a commitment becomes real.

## Draft field groups (fictional, public-safe)

**Important:** these are design dimensions, not a proposed ServiceTitan API. Keep the contract
small enough that every field has a producer, provenance, verification rule, and downstream
consumer. Do not copy internal field names, IDs, or payloads into this public repo.

Use these groups as a starting checklist. Every field should eventually answer:

1. Who produces it (model, tool, human, system)?
2. What is its provenance, and how is it verified before another agent relies on it?
3. What happens if confidence is low?

### Identity and contact

| Field | Example values | Notes |
|---|---|---|
| `caller_role` | homeowner, tenant, property_manager, unknown | Model proposes; verify against account when possible |
| `contact_method` | phone, text, web_chat, ai_assistant | Channel affects consent and identity |
| `account_match` | matched, ambiguous, new, unresolved | Tool or lookup result, not free text |
| `preferred_callback` | E.164 or "none" | Never invent a number |

### Intent and job

| Field | Example values | Notes |
|---|---|---|
| `primary_intent` | book, reschedule, cancel, status, membership, emergency, other | Single primary; secondary intents as a list |
| `job_type` | diagnostic, repair, install, maintenance, membership_visit | Must map to capacity rules |
| `urgency` | emergency, same_day, scheduled, flexible | Emergency phrases need policy, not prompt-only handling |
| `equipment_hints` | free text + structured tags if any | Model proposes; do not invent model numbers |
| `access_constraints` | e.g. "car in garage", "gate code needed" | High value for dispatch; mark confidence |

### Scheduling proposal (not a commitment)

Treat these as a state machine rather than independent strings: `proposed → confirmed` only
through a successful source-of-truth write; failed or superseded proposals remain non-committed.

| Field | Example values | Notes |
|---|---|---|
| `requested_window` | date + time range | Caller preference |
| `offered_slots` | list of slot ids from capacity tool | Only slots the tool returned |
| `selected_slot` | one offered slot id or null | Must be subset of offered |
| `booking_status` | proposed, confirmed, escalated, abandoned | Confirmed only after source of truth accepts |

### Quality and confidence

| Field | Example values | Notes |
|---|---|---|
| `transcript_confidence` | low / medium / high or numeric | Especially for addresses and alphanumerics |
| `claim_grounding` | which caller utterance supports each material claim | Prevents "booked" language before commit |
| `escalation_reason` | policy, low_confidence, customer_request, out_of_scope | Required when handing to a human |
| `bookability_signals` | structured hints for a downstream judge | See [bookability judge exercise](../senior-engineer/bookability-judge.md) |

## Verification rules (application-owned)

These are design prompts, not production rules:

- **No silent invention.** Phone numbers, addresses, account ids, and slot ids must come
  from tools or explicit caller confirmation.
- **Offer before select.** `selected_slot` must be in `offered_slots`.
- **Confirm before commit.** Spoken "you're booked" requires a successful create/update in
  the source of truth.
- **Confidence gates.** Low-confidence identity or address → clarify or escalate; do not
  pass a weak fact to dispatch as truth.
- **Channel-aware consent.** Recording and AI disclosure depend on channel and jurisdiction;
  see the repo's public regulation notes, not this file.
- **Version corrections.** If a later turn or tool corrects a fact, preserve the prior value and
  provenance in the trace; do not silently overwrite evidence that a downstream evaluator needs.

## Questions to bring to the team

- What is the actual shared-context schema between voice and dispatch / lead scoring?
- Which fields are required vs optional for a booking to be considered complete?
- How is confidence represented, and who is allowed to overwrite a field?
- How are call facts versioned when a later agent corrects them?
- What is logged for the learning loop without retaining unnecessary PII?

## Related material

- [Pantheon 2026 AI roadmap brief](pantheon-2026-ai-roadmap.md)
- [Tools and guardrails](tools-and-guardrails.md)
- Labs 09–12 (shared context, coordination, learning loop, agent-to-agent)
- [Homh and agent booking](homh-and-agent-booking.md)

## Sources

1. Investing.com, ServiceTitan Pantheon 2026 keynote summary and transcript (October 6, 2026):
   <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
2. ServiceTitan, Pantheon 2026 live coverage:
   <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
