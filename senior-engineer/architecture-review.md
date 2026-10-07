# Exercise: Architecture Review — Model vs Control Plane

A voice model hears: "Actually, make that Wednesday morning instead."

The model has access to scheduling tools. Decide which responsibilities belong to the
conversational model and which belong to the application control plane.

| Responsibility | Model | Control plane | Backend/source of truth | Explain |
|---|---|---|---|---|
| infer caller intent | | | | |
| remember conversational context | | | | |
| determine whether caller is authorized | | | | |
| choose a valid appointment slot | | | | |
| enforce same-day policy | | | | |
| execute mutation | | | | |
| make operation idempotent | | | | |
| verify mutation result | | | | |
| decide whether emergency language blocks routine action | | | | |
| phrase the response naturally | | | | |
| claim that the appointment changed | | | | |

## Design principle

Start from:

**The model proposes; the application controls; the source of truth verifies.**

Then identify exceptions and justify them.

## Review questions

- Where can stale context enter?
- What happens if the model calls the same mutation twice?
- What happens if the tool times out after the backend committed?
- Can the model ever override policy?
- What evidence is required before the agent says "you're all set"?
- Where do retries live?
- Where should authorization and audit evidence live?

## Deliverable

Produce a diagram or text architecture showing:

caller -> transport -> conversational model -> control plane -> tools -> source of truth

Include state, retries, authorization, observability, and human escalation.
