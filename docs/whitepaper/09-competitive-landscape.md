# 09 - Competitive Landscape

**Estimated reading time:** 6 minutes · **Facts as of:** September 27, 2026

Neutral and factual by design: this chapter describes who competes and on what
dimensions. It does not rank vendors.

## Five Takeaways

1. ServiceTitan says the market for trades software is still early, with many businesses
   running on rudimentary workflows. [1]
2. Its 10-K groups competitors into four types and names examples: Salesforce, SAP,
   FieldEdge, WorkWave, ServiceTrade, AccuLynx, BuildOps, Housecall Pro, JobNimbus and
   Jobber. [1]
3. AI is now a competitive axis: the 10-K warns competitors may add AI faster or better. [1]
4. Well-funded AI-native vendors sell voice agents directly to contractors, often
   integrating with ServiceTitan rather than replacing it. [2][3]
5. Analysis: voice agents are where vertical platforms, point-solution AI startups and
   horizontal contact-center AI meet, so this is one of the most contested surfaces in the
   company.

## How ServiceTitan frames competition

The 10-K says incumbent technology in the trades has had limited impact because it
typically lacks one purpose-built platform that integrates mission-critical workflows
across the project lifecycle and supports a mobile workforce. [1] It competes directly or
indirectly with four kinds of software vendor: [1]

| Type (per the 10-K) | What it means |
|---|---|
| Point-specific tools | Software for one part of the trade workflow |
| Horizontal solutions | General-purpose software for generic functions |
| Legacy field service management | Older, often on-premise field-service applications |
| Narrow bundled solutions | Simpler bundles aimed at smaller, down-market trades businesses |

The 10-K lists its ten example vendors in a single sentence without assigning them to
these types, so this paper doesn't either. [1] Their own positioning varies: Housecall Pro
presents itself as business software for home service businesses, FieldEdge as field
service management software, JobNimbus as roofing CRM and business software, and BuildOps
as commercial contractor management software. [4][5][6][7] Salesforce and SAP are the
horizontal platforms in the list. [1]

The company says it expects competition to grow,
including from consumer platforms and from AI-enabled point solutions. [1]

## The AI voice layer

Separately from field-service software, a category of AI front-office vendors sells voice
agents to contractors. Avoca is the most visible: it markets AI agents that answer calls and
book jobs for HVAC, plumbing, electrical and roofing contractors [2], and was described in
April 2026 as a roughly $1 billion Kleiner Perkins-backed company. [3] Such vendors often
integrate with the contractor's existing system of record, including ServiceTitan. [2]

Other adjacent competitors to watch, as categories rather than named vendors:

- **Traditional answering services and outsourced call centers**, the human baseline many
  contractors use for after-hours coverage.
- **Horizontal contact-center AI** from large cloud and CCaaS providers.
- **Consumer platforms and marketplaces** that capture demand before it reaches the
  contractor's phone, which the 10-K also flags. [1]

## Comparison dimensions

For any competitor, compare:

1. **Transaction authority:** can it book, reschedule and cancel in the system of record, or
   only take messages?
2. **Data depth:** customer history, memberships, capacity, pricebook, technician skills.
3. **Coverage:** after-hours only, overflow, all calls, outbound, texting and chat.
4. **Escalation:** how and when it hands off to humans, with context.
5. **Evaluation and audit:** transcripts, classification, reporting next to human CSRs.
6. **Deployment effort:** time to configure job types, rules and greetings.
7. **Trades focus:** vertical depth vs. horizontal breadth.

## What this means for a voice-agent engineer

- Your users can buy a competing voice agent that writes into the same platform, so
  quality, integration depth and trust are directly compared.
- The system-of-record advantage only counts if the agent actually uses it: capacity,
  history and rules in every decision.
- Watch point-solution vendors' public claims (booking rates, coverage) as signals of what
  contractors are being promised.

## Questions to validate after joining

- Which competitors do customers most often mention in voice-agent evaluations?
- How many customers run third-party AI answering on top of ServiceTitan today?
- Where does ServiceTitan's agent win or lose in head-to-head trials?

## Sources

1. ServiceTitan Form 10-K, fiscal 2026 (Business: Competition; Risk Factors): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
2. Avoca website: <https://www.avoca.ai/>
3. Fortune, Term Sheet on Avoca (April 27, 2026): <https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/>
4. Housecall Pro: <https://www.housecallpro.com/>
5. FieldEdge: <https://fieldedge.com/>
6. JobNimbus: <https://www.jobnimbus.com/>
7. BuildOps: <https://buildops.com/>
