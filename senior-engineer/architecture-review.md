# Exercise: Architecture Review — Model vs. Control Plane

**Time:** 45 minutes · **Builds on:** lab 02, labs 09–10, [tools and guardrails](../docs/tools-and-guardrails.md), [whitepaper ch. 15](../docs/whitepaper/15-agentic-orchestration.md)

## Scenario

A caller with an existing Thursday appointment says: "Actually, make that Wednesday morning
instead." The voice model has scheduling tools. Another agent (dispatch) also wants to use
Wednesday morning for a higher-value job.

For each responsibility, mark which layer owns it and explain why. Some rows have a shared
owner; say who has the final say.

| Responsibility | Model | Control plane | Backend / source of truth | Explain |
|---|---|---|---|---|
| infer the caller's intent | | | | |
| remember conversational context | | | | |
| identify the caller and check they own the appointment | | | | |
| choose a valid appointment slot | | | | |
| enforce the same-day-change policy | | | | |
| execute the mutation | | | | |
| make the operation idempotent | | | | |
| verify the mutation result | | | | |
| decide whether emergency language blocks routine actions | | | | |
| resolve a conflict with another agent's claim on the slot | | | | |
| write "caller prefers mornings" to shared context | | | | |
| phrase the response naturally | | | | |
| claim that the appointment changed | | | | |

## Design principle

Start from **the model proposes; the application controls; the source of truth verifies.**
Then find the exceptions and justify each one.

## Review questions

- Where can stale context enter (the caller's earlier words, a cached slot list, a fact
  another agent wrote)?
- What happens if the model calls the same mutation twice?
- What happens if the tool times out *after* the backend committed?
- Can the model ever override policy? Can another agent?
- What evidence is required before the agent says "you're all set"?
- Where do retries live, and who owns the idempotency key?
- Where do authorization and the audit record live?
- If two agents want the same slot, who arbitrates, and what does the caller hear while that
  happens?

## Deliverable

A diagram or text architecture showing

`caller → transport → conversational model → control plane → tools → source of truth`

with state, retries, authorization, observability, shared context, and human escalation marked.

## Self-check

A strong answer:

- Puts identity, ownership, policy, idempotency keys and verification in the control plane or
  backend, never in the model. Compare with `execute_tool` and `CallState` in
  `labs/stlab/tools.py`.
- Treats the model's slot choice as a *proposal* that must match a slot the application
  actually offered.
- Handles "timed out after commit" by reading authoritative state before retrying or speaking.
- Separates the model *writing a proposed fact* from the control plane *verifying it*, as in
  the context ledger of lab 09, and routes slot conflicts through arbitration with consent, as
  in lab 10, not through whichever agent writes last.
- Lets the model phrase the confirmation, but only from a committed result. The claim itself
  belongs to the control plane.

---

Part of the [senior engineer judgment track](README.md).
