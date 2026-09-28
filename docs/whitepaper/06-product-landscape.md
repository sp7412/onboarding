# 06 - ServiceTitan Product Landscape

**Estimated reading time:** 8 minutes

## Five Takeaways

1. The public catalog presents a broad platform for commercial and residential trades. [1]
2. Public Pro pages group capabilities around marketing, scheduling, dispatch, contact
   center, field work, and pricing. [1][2]
3. Atlas is publicly positioned as a conversational assistant for information and field
   support, with some office capabilities marked forthcoming. [3]
4. AI Virtual Agent is positioned around configured, capacity-aware booking and escalation.
   [4]
5. Catalog language does not establish packaging, APIs, adoption, ownership, or roadmap.

## Lifecycle Map

| Lifecycle need | Public capability language | Boundary to validate |
|---|---|---|
| Demand | Marketing and lead tools | Attribution and lead identity |
| Intake | Contact Center and AI Virtual Agent | Intent, identity, and transfer policy |
| Booking | Scheduling Pro and adaptive capacity | Commit and conflict semantics |
| Assignment | Dispatch Pro | Objective, override, and audit behavior |
| Field work | Field and Atlas positioning | Source grounding and permissions |
| Commercial state | Payments, accounting, and reporting | Data ownership and retention |

The map is a reader aid, not an architecture diagram. The public products page names the
family of offerings and the Contact Center page describes calls linked to jobs. [1][2]

## Product Claims As External Contracts

**Analysis:** Public capability language should be treated like an external contract with
three layers: what the user is promised, what inputs the system requires, and what result
is authoritative. “Book based on real capacity” implies that the available option comes
from a configured capacity source, but it does not disclose the API or state machine. [4]
An engineer should convert the promise into tests for stale availability, invalid job
types, duplicate retries, and truthful confirmation.

## Atlas And Field Assistance

The Atlas page describes answers from ServiceTitan data, equipment information, manuals,
troubleshooting, and calculators. It also labels office features such as proactive
suggestions and dispatcher support as coming soon. [3] The safe interpretation is that
retrieval and assistance are public positioning; no private rollout or roadmap should be
inferred. A field assistant should cite or link the source it used, distinguish retrieved
facts from suggestions, and transfer when the request exceeds its authorization.

## Questions Left Open

Packaging, pricing, entitlements, tenancy, API contracts, event semantics, permissions,
customer adoption, internal ownership, and roadmap are `[unverified]` here. They require
exact authorized documentation.

## Sources

1. ServiceTitan, products: <https://www.servicetitan.com/products>
2. ServiceTitan, features: <https://www.servicetitan.com/features>
3. ServiceTitan, Atlas: <https://www.servicetitan.com/features/atlas>
4. ServiceTitan, AI Virtual Agent: <https://www.servicetitan.com/features/pro/virtual-agent>
