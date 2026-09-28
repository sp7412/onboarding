# 01 - Company

**Estimated reading time:** 7 minutes

## Five Takeaways

1. The company describes its origin as building software to help the founders' fathers run contracting businesses. [1]
2. Its public mission is to serve home and commercial services contractors with tools, training, and support. [1]
3. The company page says it has more than 11,800 trade customers as of the page checked on September 27, 2026. [1]
4. The public product catalog presents a family of offerings for contractors across multiple industries, rather than a single call product. [2]
5. Analysis: a voice agent in this setting is a workflow and transaction component, not only a speech interface.

## Public Description

The company page says Ara and Vahe originally built the business to help their fathers
run contracting businesses and describes a mission to serve people in the field-services
trades. [1] This is company-authored history and positioning, not an independently
verified account of founding circumstances. The same page identifies Ara Mahdessian as
co-founder and CEO and Vahe Kuzoyan as co-founder and president. [1]

The page states “more than 11,800 trade customers” as of the page checked on September
27, 2026. [1] This is a company-reported figure with no denominator, methodology, or
independent audit presented on that page; it should not be converted into market share.

## Reading Public Positioning Carefully

The company page is useful because it states the problem the company says it exists to
solve. It is not a neutral market survey. Its language combines an origin story, a mission
statement, a customer count, named founders, and links to products and industries. Those
are different kinds of evidence. The origin story is a first-person company account. The
customer count is a dated public assertion. The product and industry links are catalog
evidence. None of them, alone, establishes how customers operate, what capabilities are
adopted, or which product produces a particular outcome.

This distinction matters for an engineer. A product page can tell us what an external
user may reasonably expect the vendor to offer. It cannot tell us the hidden invariants
that make a workflow safe. For example, a page may describe booking against capacity,
but a public reader still does not know the exact conflict policy, permissions model,
retry semantics, or audit record. Those are implementation questions and must remain
validation questions in this paper.

The public catalog also uses several levels of abstraction. The company page points to
commercial and residential solutions and to industry pages. The products page describes
a family of offerings, including ServiceTitan and other products. [2] The industries page
then presents trade-specific language. [3] This is a useful map of intended audiences,
not a data model. A product family can share a brand while having different workflows,
entitlements, deployment histories, or integration boundaries. A trade page can describe
a customer need without implying that every customer has that need.

## Company, Product, And Customer Are Different Objects

For research purposes, it helps to keep three objects separate:

1. **Company:** the legal and organizational entity described by company and investor
   materials. This paper does not infer private structure, reporting lines, or priorities.
2. **Product catalog:** the public set of products, features, and solution categories.
   Catalog language is evidence of positioning and intended capability.
3. **Customer workflow:** the contractor's actual people, policies, schedules, data, and
   outcomes. Customer workflow evidence requires customer-specific documentation or
   authorized operational data.

Confusing these objects creates predictable research errors. A catalog feature becomes an
assumed universal workflow. A customer case study becomes an industry benchmark. A public
mission becomes an assumption about internal priorities. The whitepaper avoids those
conversions. Where a section moves from source to interpretation, it says `Analysis:` or
`Hypothesis:` explicitly.

## Public Company Status And Financial Questions

The plan calls for public listing, revenue language, acquisitions, and investor material.
This version does not add those claims because the accessible source set used for this
pass does not provide a verified, stable filing extract that can support them at chapter
level. The investor-relations URL is a valid place to continue the work, but a link's
existence is not evidence for a particular date, revenue figure, acquisition, or segment
definition. A later revision should cite the exact filing or investor document, state its
period and “as of” date, and distinguish reported results from analysis.

This restraint is especially important for a public company. Numbers can change because
of fiscal periods, definitions, acquisitions, restatements, or page updates. A sentence
such as “the company serves X customers” is incomplete unless it identifies whether X is
customers, locations, users, or service professionals and when the count was measured.
The current company page supplies a customer-count phrase, but not the denominator or
methodology needed for a market-share calculation. [1]

## Engineer Lens: Workflow Correctness

The public description points toward a platform that connects operational work rather
than a standalone voice experience. The products page names mission-critical areas such
as marketing, scheduling, dispatch, contact center, pricebook, sales, fleet, and payments.
[2] Even without access to internal boundaries, the implication for an AI engineer is
clear: a voice interaction may cross from conversation into business state.

That crossing creates a layered correctness problem:

- **Perception:** What did the caller say, and with what confidence?
- **Interpretation:** What intent, entity, urgency, and constraints are present?
- **Policy:** Is the request allowed for this caller, trade, location, and job type?
- **Availability:** Is the proposed resource still eligible at commit time?
- **Mutation:** Did exactly one authorized state change occur?
- **Evidence:** Can a human later see what was proposed, confirmed, rejected, or transferred?

Speech quality is necessary but not sufficient. A fluent answer that invents a slot or
claims a booking that failed is a product failure even if the transcript sounds natural.
Conversely, a transfer that preserves the caller's structured context may be a successful
outcome even if the agent does not contain the call. This is an analysis, not a claim about
any private system.

## A Public-Source Operating Model

The public pages support a bounded model for future research. Demand arrives through a
channel. A contractor's configured workflow collects enough information to decide what
can happen next. Scheduling and dispatch use operational constraints. Contact-center
tools connect conversations to jobs. AI may assist with intake, retrieval, booking, or
handoff. The actual authority for a transaction must be defined by the product and
contractor configuration, not inferred from a marketing sentence.

This model also explains why the paper keeps asking about ownership. A voice agent should
not silently become the source of truth for a customer record, a schedule, a price, or a
payment. It can gather facts, request a proposal, present an option, and call an
authorized operation. The operation should validate its own preconditions and return an
outcome that the agent can state accurately.

## What Remains Open

The following questions are intentionally unresolved: current segment mix; public versus
internal definitions of a customer; product attach rates; pricing and packaging; actual
API and permission boundaries; revenue attribution; roadmap; and the relationship between
catalog capabilities and customer adoption. The answers should come from authorized
materials or exact public filings, not from extrapolation.

## Public Product and Segment Language

The products page describes a family of companies and solutions serving contractors
across multiple industries. [2] Its public categories include residential and
commercial solutions, enterprise and franchise contexts, and products such as
ServiceTitan, FieldRoutes, Aspire, Convex, and Conduit. [2] These labels establish
public positioning only; they do not establish product boundaries, adoption, pricing,
revenue mix, or technical integration details.

The public industries page lists HVAC, plumbing, electrical, garage door, chimney,
roofing, irrigation, water treatment, septic, painting, pool service, landscaping,
lawn care, pest control, and other adjacent categories. [3] It also distinguishes
commercial and residential contractors. [3] It does not provide a validated industry
market-size synthesis or customer segment mix.

## Engineer Implications

**Analysis:** A workflow platform creates correctness obligations at the point where a
conversation changes business state. Speech recognition and response quality matter,
but a successful interaction also needs identity, scope, authorization, availability,
confirmation, idempotency, and audit evidence. The agent should propose through tools;
the system of record and policy layer should decide whether a mutation is legal.

**Hypothesis:** The most durable engineering leverage is likely to come from explicit
workflow contracts and evaluation slices by trade, role, and transaction, rather than
from treating every call as an unconstrained conversation.

## Validation Questions

- What are the current customer and product segment definitions?
- Which public customer-count figures have a documented “as of” date and denominator?
- Which product capabilities are authoritative for scheduling, dispatch, payments, and calls?
- What are the supported workflow states and permission boundaries for voice actions?
- Which outcomes are company-reported, customer-reported, or independently measured?

## Sources

1. ServiceTitan, “About ServiceTitan - The operating system for the trades,” company page, checked September 27, 2026: <https://www.servicetitan.com/company>
2. ServiceTitan, “ServiceTitan Product Offerings,” products page, checked September 27, 2026: <https://www.servicetitan.com/products>
3. ServiceTitan, “Industries We Serve,” industries page, checked September 27, 2026: <https://www.servicetitan.com/industries>
