# Changelog

This file records meaningful repository changes so the evolution of the
onboarding material is easy to scan without reading individual pull requests.

## 2026-10-08

### Pantheon and agent architecture

- Added public-source guidance on agentic orchestration, shared context,
  shared skills/capabilities, and running agents in production.
- Added a comparative guide to multi-agent architectures and the control
  surfaces around them.
- Added the **agent harness** model: the model proposes; the harness controls.
- Added a design-by-evaluation workflow covering traces, failure mining,
  regression evaluation, and staged rollout.
- Added MCP and external-agent trust-boundary guidance covering authorization,
  consent, idempotency, injection risks, auditability, and booking state.
- Refreshed the Pantheon 2026 roadmap and claims ledger as new public
  announcements and follow-up coverage became available.
- Turned the Command Center capacity-hold and duplicate-action details into a
  senior-engineer exercise covering atomic reservation, idempotent retries,
  stale recommendations, release/reconciliation, and authoritative state.
- Clarified the public status of ServiceTitan's MCP work: public material
  describes MCP connectivity, while the broader MCP server remains described
  as in development; the repository does not treat it as generally available
  or assume mutating scope.

### First-90-days workflow

- Added a focused first-90-days question bank for a voice-agent team.
- Expanded the repository from a broad study guide toward a practical
  first-90-days operating guide, including manager alignment, field
  observations, architecture questions, and a senior-engineer judgment track.

### Hands-on labs

- Expanded the lab path through multi-agent coordination, Mini-Max,
  earning autonomy, LLM evaluation, and MCP fundamentals.
- Added Codespaces/dev-container and Colab paths for running labs.
- Added the MCP server basics lab with a fictional contractor server,
  tools/resources/prompts, Streamable HTTP, Inspector, trust-boundary
  exercises, and safe mutation design.
- Kept labs offline-safe and based on fictional data; live integrations remain
  optional and must use personal credentials.

### Quality and safety

- Added explicit autonomy-promotion and demotion guidance using statistical
  confidence bounds, minimum sample sizes, cost asymmetry, calibration,
  drift/OOD checks, segmentation, and rollback triggers.
- Added repository guidance for public-safe content and post-Day-One handling
  of company knowledge.
- Added maintenance, source-ledger, and claims-verification practices so
  public claims are distinguishable from inference or fictional exercises.

## 2026-09 and earlier

The repository began as a broad ServiceTitan/voice-agent study workspace and
has progressively been reorganized into a practical onboarding system:

- company and product primer
- canonical 30/60/90 operating plan
- real-time voice-agent architecture and hands-on labs
- production metrics, evaluation, and failure analysis
- multi-agent coordination and agent-to-agent workflows
- earned-autonomy policy and senior-engineer judgment exercises
- public-source references, claims ledger, and reusable onboarding templates

For implementation-level detail, see the individual documents and the Git
history. This changelog intentionally summarizes the repository's evolution
rather than duplicating every commit.
