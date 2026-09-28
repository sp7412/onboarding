# 02 - The Trades Industry

**Estimated reading time:** 6 minutes

## Five Takeaways

1. The public industry page explicitly covers both commercial and residential contractors. [1]
2. The listed categories span mechanical, home-service, property-service, construction-adjacent, and safety-related work. [1]
3. A trade label is not enough to define a common workflow: service area, job type, skills, and capacity rules still need local validation.
4. Public sources checked for this phase do not establish a defensible market-size, labor-supply, seasonality, weather-demand, roll-up, financing, or warranty synthesis. [1]
5. Analysis: trade variation should become evaluation and routing slices, not merely prompt examples.

## What Public Pages Establish

The official industries page describes the platform as built for commercial and
residential contractors. [1] It names HVAC, plumbing, electrical, garage door, chimney,
roofing, irrigation, water treatment, septic, painting, pool service, landscaping, lawn
care, pest control, and several other categories. [1]

The page uses different capability language for different categories. For example, its
HVAC description mentions memberships and account reconciliation; its plumbing
description mentions intake, scheduling, and dispatch; and its chimney description
mentions customer profiles and job histories. [1] These are vendor positioning claims,
not evidence that every business in a category operates in that way.

## Why A Category List Is Not A Market Model

The industries page is best read as a taxonomy of intended product conversations. It
contains recognizable labels, but the labels do not have equal granularity. HVAC and
plumbing describe broad fields; garage door and chimney describe narrower service
contexts; landscaping, lawn care, and pest control can contain recurring or route-based
work as well as one-time requests. Commercial food equipment, fire and life safety, and
dock and door introduce business-to-business contexts with different site, access, and
service-contract considerations. [1]

The page also mixes the language of trade, customer type, and operating activity. A
residential plumbing request and a commercial plumbing request may share a technical
discipline but differ in authorization, site access, scheduling windows, purchase order
requirements, or communication path. Those differences are not settled by the word
“plumbing.” Likewise, a membership is a business policy, not a universal property of
HVAC. The page's examples are useful hypotheses about what to investigate, not evidence
that the same feature is configured everywhere.

## Residential And Commercial As Distinct Contexts

The source explicitly says the platform serves commercial and residential contractors.
[1] That distinction is operationally meaningful even before adding market statistics.
Residential calls commonly present a person, household, property, and immediate service
need. Commercial calls may present a business location, an authorized requester, an
equipment fleet, a facilities process, or a contract relationship. Those are examples of
possible data differences, not universal rules.

For a voice agent, the distinction should affect questions and tests. An evaluation should
ask whether the agent captured the service location, requester role, urgency, and job type
needed for the configured workflow. It should not assume that a single residential-style
script generalizes to commercial work. The right abstraction is a policy-driven intake
contract with trade and customer-context fields, not a long prompt containing every trade
name.

## Trade Variation As Workflow Variation

Trade variation can change at least six engineering dimensions:

1. **Intent:** maintenance, repair, installation, inspection, recurring service, or a
   project request may have different next steps.
2. **Required facts:** equipment, symptoms, property type, access constraints, or prior
   job history may be relevant in different combinations.
3. **Capacity:** a valid slot may depend on geography, skill, duration, inventory, or a
   service agreement.
4. **Urgency:** a request can be routine, time-sensitive, or unsafe to handle as a normal
   booking. The caller's description alone should not authorize technical diagnosis.
5. **Handoff:** the right destination can be a CSR, dispatcher, technician, manager, or
   emergency channel, depending on local policy.
6. **Outcome:** “scheduled” may mean a service call, estimate, inspection, recurring
   visit, or callback, and the denominator must be defined accordingly.

These dimensions are analysis. The public page supplies the category vocabulary, while
the actual values must be validated per deployment. [1]

## Seasonal And Weather Questions Without Invented Statistics

It is reasonable to ask whether weather changes demand in some trades. It is not
reasonable to state a universal seasonal curve without a verified source, geography,
trade definition, and time period. The same caution applies to labor supply, private-
equity roll-ups, financing, warranties, and market size. This package leaves all of
those items `[unverified]` rather than importing a number from a loosely related study.

A useful next step is a measurement specification: define geography, trade, job type,
date window, demand event, denominator, and source of truth. If a weather experiment is
ever run, the analysis should separate demand changes from staffing, advertising, outage,
and policy changes. A voice-agent evaluation can then include “weather surge” as a slice
without pretending that the slice is a general industry fact.

## Memberships, Financing, And Warranties

The official page mentions memberships for HVAC and other pages in the public catalog
mention financing and related capabilities. [1] The existence of a product concept does
not tell us the contractual rules. A membership may affect greeting, eligibility,
priority, price, or recurring service. Financing may require disclosure, consent, or a
separate process. A warranty request may require a product, installer, date, and proof.

These are exactly the kinds of fields that should be represented explicitly. The agent
should retrieve or ask for the minimum information, then defer eligibility and financial
decisions to an authoritative policy operation. It should not infer that a caller is a
member, that a repair is covered, or that financing is approved from conversational
context alone.

## Evaluation Slices

An aggregate success rate can hide a category failure. A practical public-safe benchmark
can cross the following axes: trade, residential/commercial context, new/existing
customer, routine/urgent request, booking/reschedule/cancel intent, offered/unoffered
slot, and backend success/conflict/error. The benchmark should record both conversational
quality and state correctness.

For example, a test may ask a fictional caller to schedule a plumbing visit while the
requested window is not available. The expected behavior is not “be helpful” in the
abstract. It is to explain the constraint, offer only valid alternatives, obtain an
explicit selection, and avoid creating a job until the commit succeeds. The data and
expected state are fictional; the engineering principle follows from the public framing
of intake, scheduling, and dispatch. [1]

## A Practical Research Boundary

The public category list is sufficient to define a research vocabulary, but not to answer
how large or profitable any category is. It does not establish the number of businesses,
regional mix, labor conditions, weather sensitivity, or adoption of any operating model.
Those gaps are not defects in the source; they are limits on what this whitepaper can
claim. A later researcher can add a government or trade-association source per question,
but should preserve the definitions and geography of each source rather than merge them
into a synthetic market number.

Until then, the most defensible engineering output is a configurable domain model and a
test matrix. The model should make trade, customer context, job type, service area,
required skill, capacity, urgency, and policy visible. The test matrix should include
unknown and conflicting values. This approach produces useful software questions without
turning a marketing taxonomy into an unsupported industry conclusion.

It also keeps configuration separate from model behavior.

The same boundary applies to language. A caller may use local terminology, abbreviations,
or a trade word that does not map cleanly to one job type. The system should preserve the
original utterance, ask a clarifying question when the mapping is consequential, and let
the configured workflow return the permitted choices. This is preferable to silently
normalizing an ambiguous phrase into a transaction. The example is a design analysis, not
a claim about the behavior of a current product.

## What This Research Does Not Establish

The checked sources do not provide a reliable single denominator for the number of
contractors, trade mix, residential/commercial split, seasonality, weather sensitivity,
technician supply, private-equity roll-up prevalence, financing use, or warranty
practices. These items are **[unverified]** in this phase. A future version should use
one verified primary or reputable source per claim and should avoid combining unlike
geographies or definitions.

## Engineering Translation

**Analysis:** A caller's trade is only one routing feature. A production system may need
to distinguish intent, urgency, service area, customer status, job type, required skill,
capacity, policy, and escalation destination. Those dimensions should be represented in
test data and tool authorization rather than left implicit in prose.

**Hypothesis:** A useful benchmark will report slices such as `trade x intent x
new/existing customer x backend condition`, because an aggregate booking score could
hide a trade-specific or safety-sensitive failure.

## Validation Questions

- Which trade categories and subcategories are in scope for each deployment?
- How are residential and commercial requests represented and routed?
- Which job types require distinct skills, equipment, licensing, or escalation?
- How do service area, weather, and seasonal capacity change the valid booking policy?
- Which membership, financing, and warranty rules are contractor-specific?

## Sources

1. ServiceTitan, “Industries We Serve,” industries page, checked September 27, 2026: <https://www.servicetitan.com/industries>
