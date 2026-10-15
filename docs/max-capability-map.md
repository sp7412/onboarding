# ServiceTitan Max: public capability map and coordination examples

**Evidence reviewed:** October 15, 2026  
**Purpose:** summarize publicly disclosed Max capabilities without implying access to the private agent registry or implementation.

This page is an evidence map, not a complete inventory of the advertised "30-plus agents." ServiceTitan has described Max as a coordinated system spanning demand, field work, and office workflows. Its public material names some agents and describes others as product capabilities, but it does not publish a complete agent-by-agent technical registry.

## Residential: demand, booking, and revenue

| Capability family | Publicly described work | Coordination implication |
|---|---|---|
| Marketing and demand | Google and Meta advertising, multi-touch attribution, ad experiments, email campaigns, social publishing, reputation and reviews | Spend and outreach should respond to forecast capacity, not optimize lead volume in isolation. |
| Lead response and booking | Voice, text, web chat, Google booking, speed-to-lead, recovery of leads that did not convert | A promising lead may require coordination with scheduling before the system can safely promise an appointment. |
| Scheduling and dispatch | Adaptive Capacity, demand-versus-capacity views, matching technicians to jobs, moving appointments where permitted | A booking decision depends on slot availability, technician skills, travel, urgency, customer consent, and existing commitments. |
| Sales and revenue | Good-better-best proposals, financing, unsold-estimate follow-up, technician coaching | A recommendation should reflect job context and customer needs, not simply maximize average ticket. |
| Command Center / Atlas | Configure and monitor automations, inspect metrics and actions, review insights; Atlas can report, research, monitor, and help create or modify workflows as availability permits | Operators need to distinguish recommendations, approval requests, executed actions, and verified outcomes. |

**Sources:** ServiceTitan's [Pantheon 2026 live coverage](https://www.servicetitan.com/blog/pantheon-2026-live-coverage), [Max help documentation](https://help.servicetitan.com/v1/docs/servicetitan-max), and [October 6 press release](https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html). Product names, rollout status, and availability can change; consult the linked current documentation.

## Commercial: named field and back-office capabilities

ServiceTitan announced a limited commercial and roofing Max pilot at Pantheon on October 6, 2026. The announcement distinguishes agents already in the pilot from capabilities described as coming soon.

| Publicly named capability | Disclosed function | Public status in the announcement |
|---|---|---|
| Site-walk / findings write-up copilot | Drafts findings from a site walk | Listed among agents already live in the pilot |
| Equipment Agent | Enriches equipment records, including manufacturer/date information and compatible filters, belts, and refrigerant details | Demonstrated/described in commercial coverage; do not infer broad availability from the demo alone |
| Findings Agent | Reviews completed work orders and recommends findings that may have been missed | Demonstrated/described in commercial coverage; rollout scope is not fully specified |
| Daily Log Agent | Drafts a foreman's daily log from voice notes and jobsite photos; public coverage says a field conflict can trigger an RFI or change-order workflow | Listed among agents already live in the pilot |
| Invoice review agent | Compares invoice information with work performed and drafts a correction for approval; a keynote example caught an installed but unbilled smart thermostat | Listed among agents already live in the pilot |
| Agreement review agent | Reviews service agreements and flags issues with a suggested next step | Announced as coming soon |
| Touchless AP autopilot | Automates accounts-payable work | Announced as coming soon |
| Collections agent | Supports collections workflow | Announced as coming soon |
| Applications-for-payment (AFP) recommendation advisor | Advises on applications for payment | Announced as coming soon |

Sources: [ServiceTitan press release](https://www.servicetitan.com/news/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026), [Pantheon live coverage](https://www.servicetitan.com/blog/pantheon-2026-live-coverage), and [industry reporting on the commercial pilot](https://constructionmetrics.com/2026/10/11/servicetitan-max-pilot-commercial-daily-log-invoice/). Treat the table as a dated public snapshot, not a live feature-availability guarantee.

## Announced future direction: commercial and roofing

The Pantheon live coverage describes planned additions for the following year:

- **Commercial cross-sell:** turn new installs into service-agreement proposals and surface replacement opportunities with total-cost-of-ownership analysis.
- **Technician development:** schedule technicians toward the hours needed to advance certifications.
- **Construction estimate variance:** forecast project variance using historical budgets and actuals.
- **Roofing claims and supplements:** reconcile an adjuster's scope against an estimate and draft supplements.
- **Roofing production:** break a sold estimate into jobs, schedule crews and deliveries, and reschedule around weather.
- **Subcontractor management:** match jobs to subcontractors, issue work orders, calculate pay, and score performance.

These are announced plans, not evidence that the capabilities are currently generally available. See the [Pantheon live coverage](https://www.servicetitan.com/blog/pantheon-2026-live-coverage) and verify status against current product documentation before relying on them.

## Cross-agent examples worth understanding

### 1. Capacity-aware demand and booking

1. Demand forecasting estimates that the schedule will be full.
2. Demand-generation automations pause or reduce activity rather than continuing to buy leads that cannot be served.
3. When capacity is expected to open, the system can increase demand generation.
4. If a high-value lead arrives while the schedule is full, booking can request help from dispatch rather than making an impossible promise.
5. A proposed move must respect customer consent and hard business constraints; an approved change must still be committed and verified in the authoritative scheduling system.

The first four steps are consistent with public Max examples. The last step is the engineering control model this onboarding teaches; it is not a claim about Max's undisclosed implementation.

### 2. Field observation to office action

1. A foreman supplies voice notes and photos.
2. A Daily Log Agent drafts the daily log.
3. A detected field conflict may initiate an RFI or change-order workflow.
4. The workflow should preserve provenance from source evidence to draft, make approval requirements explicit, and distinguish a draft from an approved/submitted document.

Public coverage describes the log drafting and cross-agent handoff, but does not disclose the detection algorithm, message schema, or approval implementation. See [industry reporting](https://constructionmetrics.com/2026/10/11/servicetitan-max-pilot-commercial-daily-log-invoice/).

### 3. Work performed to invoice correction

1. The invoice review agent compares billing details with completed work.
2. It identifies a possible omission, such as installed equipment that was not billed.
3. It drafts a correction for one-click approval.
4. The system should verify the resulting invoice state and prevent duplicate corrections on retry.

The keynote example supports the first three steps. Idempotency and post-write verification are recommended engineering controls, not disclosed Max internals. Source: [Pantheon live coverage](https://www.servicetitan.com/blog/pantheon-2026-live-coverage).

## What the public evidence does—and does not—establish

**Publicly described:** 30-plus agents, 18 business drivers, shared context and judgment, coordinated action, arbitration, centralized supervision, outcome-linked learning, and examples across residential and commercial workflows.

**Not publicly established by these sources:** a complete list of all agents; whether every advertised "agent" is a separate LLM process or service; internal message schemas; whether coordination uses events, RPC, a workflow graph, or a hybrid; the arbitration algorithm; consistency/locking mechanisms; model assignments; private telemetry schemas; or exact production rollout for every feature.

Use "agent" as ServiceTitan's product/architecture term unless a source gives a more precise technical definition. Do not convert a product capability into a claim about deployment topology.

## Engineering questions to carry into the role

- What is the authoritative state for an appointment, job, invoice, or change order?
- Which decisions are hard constraints, and which are utility trade-offs?
- How are reservations, concurrent updates, stale reads, retries, and idempotency handled?
- Which agent actions require consent or approval, and how is that decision audited?
- How are proposed actions tied to verified outcomes for evaluation and attribution?
- How can an operator inspect the triggering context, agent proposal, arbitration result, committed action, and final outcome?

## Related onboarding material

- [Pantheon 2026 AI roadmap](pantheon-2026-ai-roadmap.md) — source-by-source public announcements and caveats.
- [ServiceTitan voice-agent public evidence](voice-agent-public-evidence.md) — voice workflows, Voice Intelligence, reported metrics, and rollout caveats.
- [Chapter 15: Agentic orchestration](whitepaper/15-agentic-orchestration.md) — architecture patterns and arbitration.
- [Lab 10: Coordination and arbitration](../labs/10_coordination_and_arbitration.ipynb) — local optimization and competing requests.
- [Chapter 17: Running agents in production](whitepaper/17-running-agents-in-production.md) — traces, failure mining, evaluation, and rollout.
