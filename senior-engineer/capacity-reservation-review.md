# Capacity reservation and concurrent recommendations

**Time:** 30 minutes  
**Scenario:** fictional; inspired by public Pantheon 2026 coverage, not a description of ServiceTitan internals.

## Scenario

A contractor schedules a marketing campaign expected to generate demand next week. The forecast says the campaign needs 12 appointment slots, so the system temporarily holds that capacity. If bookings fall short, unused holds should be released.

Two authorized users see the same recommendation and click **Launch campaign** within a few milliseconds of each other. A third service is updating the schedule at the same time. A retry arrives after the first request times out, and the campaign is later canceled.

Design the smallest safe control-plane contract. Do not assume the UI, an LLM, or a distributed lock alone is the source of truth.

## Deliverable

Write a one-page state machine and a short test plan covering:

1. **State transitions:** proposed → validated → reserved → committed/active → released or expired. Define which transitions are allowed and who owns them.
2. **Atomicity:** explain how two users attempting the same action cannot reserve the same capacity twice. Identify the authoritative transaction or conditional state change.
3. **Idempotency:** define the key and response behavior for a duplicate request and a retry after a timeout.
4. **Staleness:** state what gets revalidated at commit time if capacity, campaign assumptions, permissions, or schedule versions changed after the recommendation was shown.
5. **Release and reconciliation:** define when unused holds expire or are released, how partial booking shortfall is handled, and how the system recovers if release fails.
6. **Explainability and audit:** record the recommendation, its expected outcome, the policy/state checks, the actor, the result, and why the hold was retained or released.
7. **Failure behavior:** say what the user sees if the reservation cannot be confirmed. Never report a campaign as launched merely because the model recommended it or the request was sent.

## Self-check

A strong answer should include all of the following:

- The server rechecks authorization and current capacity at the mutation boundary; a client-side disabled button is only a usability aid.
- A unique idempotency key plus an atomic conditional write or transaction prevents duplicate effects. A retry returns the original result rather than creating a second reservation.
- Reservation and campaign activation have explicit states and recoverable transitions. Holds have an owner, scope, expiry/release policy, and observable failure path.
- A stale recommendation is revalidated, rejected, or recomputed rather than blindly applied.
- The audit record distinguishes **proposed**, **accepted**, **committed**, and **observed outcome**.
- Concurrent tests prove one winner, retries are safe, and release is eventually reconciled. Tests include partial bookings, cancellation, stale schedule versions, and a failed release.
- The design does not claim these are ServiceTitan's implementation details. The public source establishes the problem shape; this exercise applies standard engineering controls to a fictional system.

## Public grounding

ServiceTitan's Pantheon 2026 live coverage described Atlas placing holds on open capacity when a campaign launches, releasing holds if bookings fall short, and recommendations that explain their reasoning. The same coverage noted the need to register when another user has already acted on a recommendation so two users do not execute the same action. These are public descriptions of product behavior, not a published implementation design.

See the [Pantheon 2026 roadmap brief](../docs/pantheon-2026-ai-roadmap.md) and [hypothesis map](../docs/hypothesis-map.md). Keep any observations about actual internal implementation in approved company systems after day one.
