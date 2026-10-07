# Pantheon Hypothesis Map

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

This is a **public-to-private validation map**. Every row is a hypothesis about how a
voice-agent system might work, not a statement of ServiceTitan's internal architecture.
Vendor statements are explicitly labeled as company claims. The public repo contains only
the hypothesis, public evidence, and questions; answers learned after joining belong in
company systems.

| Hypothesis | Public evidence | Confidence | How I'd validate in weeks 1–2 | Question to ask, and of whom | Why it matters |
|---|---|---|---|---|---|
| Bookability is judged by a separate post-call model/agent, not only the voice agent's prompt | **Company claim:** a voice-intelligence agent reviews calls to judge whether each was a real opportunity to book, backed by transcript evidence. [Pantheon brief](pantheon-2026-ai-roadmap.md), [help center](https://help.servicetitan.com/release-hub/docs/coming-soon-get-ready-for-voice-intelligence-in-servicetitan-core) | High | Trace the post-call path | Is bookability its own service/model? Ask evals owner or PM. | Determines eval ownership and the facts contract. |
| Voice-derived facts can influence lead scoring and dispatch | **Company claims:** lead scoring uses what was said on the call and the caller's tone; Dispatch Pro considers what was said on the call; Max agents "work from the same context". [Pantheon brief](pantheon-2026-ai-roadmap.md), [help center](https://help.servicetitan.com/docs/an-introduction-to-servicetitan-max-what-it-is-and-why-it-matters) | High | Follow one call's fields across traces | Where is the authoritative context store? Ask infra/evals owner. | Defines provenance and stale-state risks. |
| Coordination includes shared judgment, not only shared data | **Company claim:** public Pantheon material describes shared judgment such as lead scoring and demand forecasting. [Pantheon brief](pantheon-2026-ai-roadmap.md) | High | Compare scoring/forecast inputs and versions | Which judgments are centralized versus agent-owned? Ask architecture owner. | Prevents agents from optimizing incompatible objectives. |
| Agents can request coordinated actions from one another | **Company claim:** Pantheon describes coordinated action and arbitration. [Pantheon brief](pantheon-2026-ai-roadmap.md) | Medium | Inspect one cross-agent request | Who authorizes the receiving agent's action? Ask platform/infra. | Defines permission and arbitration boundaries. |
| Autonomy is granted incrementally as trust is earned | **Company claims:** voice agents sit at level 2 of a five-level AI maturity model; some customers reportedly let the agent take all calls with CSRs on standby. [Pantheon brief](pantheon-2026-ai-roadmap.md) | High | Find an actual rollout or promotion example | What evidence is required before autonomy increases? Ask manager/evals owner. | Connects evaluation to deployment policy. |
| Autonomy levels may differ by segment or workflow | Public material describes many specialized agents and workflows; segment-specific policy is a hypothesis, not a stated internal design. [Pantheon brief](pantheon-2026-ai-roadmap.md) | Low | Compare error rates by trade/intent/channel | Is autonomy scoped per workflow, customer, or segment? Ask PM/evals. | Aggregate metrics can hide weak segments. |
| Phone, text, webchat, and external AI bookings share a control plane | **Company claims:** webchat is set up "in the same place as your voice and text agents"; Pantheon describes booking by external AI agents. [Pantheon brief](pantheon-2026-ai-roadmap.md), [help center](https://help.servicetitan.com/release-hub/docs/book-jobs-from-your-website-with-webchat-in-virtual-agent) | Medium | Trace the same booking invariant across channels | What is channel-specific versus shared? Ask platform owner. | Avoids duplicating authorization and idempotency rules. |
| External assistant bookings pass through a controlled agent gateway | **Company claim:** Pantheon announces Homh and booking by external AI assistants. [Pantheon brief](pantheon-2026-ai-roadmap.md) | Medium | Trace one public-facing booking flow if available | Where are authentication, consent, quote expiry and idempotency enforced? Ask API/platform owner. | External callers have different trust and replay risks. |
| Voice content is evaluated against business outcomes, not only agent self-reports | **Company claim:** Pantheon says internal booking rates are easy to game and describes voice intelligence review. [Pantheon brief](pantheon-2026-ai-roadmap.md) | High | Compare call-level labels with final job state | Which metric is the source of truth for booking quality? Ask evals owner. | Prevents optimizing a gamable numerator. |
| Demand forecasting can change marketing/call volume decisions | **Company claim:** public Pantheon material describes demand orchestration and coordination around capacity. [Pantheon brief](pantheon-2026-ai-roadmap.md) | Medium | Follow a demand signal into one downstream action | Which forecast feeds which action, and with what delay? Ask PM/infra. | Changes the distribution seen by the voice agent. |
| Arbitration is a hard control boundary, not just an LLM prompt | **Company claim:** Pantheon describes arbitration and clear rules for when agents act or ask. [Pantheon brief](pantheon-2026-ai-roadmap.md) | High | Find one vetoed action and its policy owner | Which rules are non-negotiable and where are they enforced? Ask architecture owner. | Hard constraints must not be traded for expected value. |
| Shared context has provenance/version semantics | Public materials say agents share context; provenance/versioning is an engineering hypothesis. [Pantheon brief](pantheon-2026-ai-roadmap.md) | Low | Inspect a fact change or correction | How are stale/conflicting facts represented? Ask infra/evals owner. | Determines whether downstream decisions are auditable. |
| Call content may become a durable signal for later workflows | **Company claim:** Pantheon describes voice intelligence and using call information in downstream workflows. [Pantheon brief](pantheon-2026-ai-roadmap.md) | Medium | Trace one call-derived attribute beyond booking | What retention and access rules apply? Ask data owner. | Creates privacy, drift, and feature-governance concerns. |
| The highest-leverage voice-agent work may sit at system boundaries | **Analysis:** public announcements emphasize coordination, shared context, business outcomes, and autonomy. [Pantheon brief](pantheon-2026-ai-roadmap.md) | Medium | Ask where current failure costs concentrate | Which boundary currently causes the most customer impact? Ask manager. | Helps choose a useful first project instead of polishing the demo agent. |

## Keeping the log

Copy the rows you care most about into the [working-hypotheses template](../senior-engineer/hypotheses.md)
in a **private** place before day one, and track what you observe against each. Labs
[13](../labs/13_minimax_capstone.ipynb) and [14](../labs/14_earning_autonomy.ipynb) (with the
[earning-autonomy guide](earning-autonomy.md)) let you practise the two hypotheses
that matter most for a voice engineer: the facts contract and earned autonomy.

## Validation rule

Never turn a row into a "fact" because a diagram or teammate's shorthand sounds plausible.
Record the observed behavior, owner, evidence, and uncertainty in private company systems after
day one.
