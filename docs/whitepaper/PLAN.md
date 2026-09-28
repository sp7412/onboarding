# Background Whitepaper Research Plan

## Phase 1 Scope

This is a research and writing plan only. No whitepaper chapter has been written yet.
The final paper will use public sources, cite every factual claim, attribute customer
results, label analysis and hypotheses, and omit unsupported numbers. URLs below are
candidate sources that were checked during this planning pass unless explicitly noted
as a gap. New sources will be added to `docs/references.md` when the corresponding
chapters are written.

## Writing Conventions

- Every chapter begins with five takeaways and an estimated reading time.
- Every factual claim gets an inline citation and a numbered source list in that chapter.
- Every dated number says “as of” and identifies the source.
- Customer-reported outcomes remain attributed to the customer case study.
- Analysis is labeled `Analysis:`; forward-looking reasoning is labeled `Hypothesis:`.
- Fictional examples are explicitly labeled fictional.
- Regulatory material begins with a general-education, not-legal-advice notice.
- `claims-ledger.md` records claim, chapter, URL, date checked, and support status.

## Source Tiers

### Verified public source candidates

These pages returned usable content during planning:

- ServiceTitan company: <https://www.servicetitan.com/company>
- ServiceTitan features/platform: <https://www.servicetitan.com/features>
- ServiceTitan products: <https://www.servicetitan.com/products>
- ServiceTitan industries: <https://www.servicetitan.com/industries>
- ServiceTitan AI Virtual Agent: <https://www.servicetitan.com/features/pro/virtual-agent>
- ServiceTitan Contact Center Pro: <https://www.servicetitan.com/features/pro/contact-center>
- ServiceTitan Scheduling Pro: <https://www.servicetitan.com/features/pro/scheduling>
- ServiceTitan Dispatch Pro: <https://www.servicetitan.com/features/pro/dispatch>
- ServiceTitan Atlas: <https://www.servicetitan.com/features/atlas>
- ServiceTitan Pantheon 2025 press release: <https://www.servicetitan.com/press/servicetitan-introducing-the-next-evolution-of-ai-at-pantheon-2025-keynote>
- ServiceTitan Pantheon 2025 Atlas recap: <https://www.servicetitan.com/blog/pantheon-2025-vahe-keynote-atlas>
- ServiceTitan investor relations: <https://investors.servicetitan.com/>
- EPA Section 608: <https://www.epa.gov/section608>
- PCI DSS overview: <https://www.pcisecuritystandards.org/standards/pci-dss/>
- California DOJ CCPA FAQ: <https://oag.ca.gov/privacy/ccpa>
- OpenAI Realtime guide: <https://developers.openai.com/api/docs/guides/realtime>
- OpenAI Realtime reference: <https://platform.openai.com/docs/api-reference/realtime>
- OpenAI voice agents guide: <https://developers.openai.com/api/docs/guides/voice-agents>
- LiveKit Agents overview: <https://docs.livekit.io/agents/>
- LiveKit turns: <https://docs.livekit.io/agents/logic/turns/>
- LiveKit telephony: <https://docs.livekit.io/telephony/>
- LiveKit 101 video playlist: <https://www.youtube.com/playlist?list=PLWx-Xa8RhJXuv8fu2Qz9rj2MPb4qgXir>
- LangChain agents: <https://docs.langchain.com/oss/python/langchain/agents>
- LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
- LangGraph persistence: <https://docs.langchain.com/oss/python/langgraph/persistence>
- LangSmith observability: <https://docs.langchain.com/langsmith/observability>
- LangSmith evaluation: <https://docs.langchain.com/langsmith/evaluation>
- Anthropic, Building Effective Agents: <https://www.anthropic.com/engineering/building-effective-agents>
- Tau-bench paper: <https://arxiv.org/abs/2406.12045>
- Tau-squared-bench paper: <https://arxiv.org/abs/2506.07982>
- Moshi paper: <https://arxiv.org/abs/2410.00037>
- LiveKit end-of-turn transformer article: <https://livekit.com/blog/using-a-transformer-to-improve-end-of-turn-detection>

### Sources requiring a second verification pass before citation

The following are relevant but were blocked, moved, or returned a non-200 response in
the automated fetcher during planning. They must not be cited in a final chapter until
the final page is manually or programmatically verified:

- SEC filing index and company facts endpoints.
- BLS occupational and industry pages.
- FCC consumer and AI-robocall guidance.
- FTC Telemarketing Sales Rule page.
- DOJ Section 508 page.
- DOE heat-pump material.
- State call-recording statutes and state bot-disclosure laws.
- TCPA and A2P 10DLC primary sources.

If these cannot be verified, the relevant section will state the limitation, cite an
accessible primary source where possible, or be omitted. No URL will be fabricated.

## Chapter Plan

### 00 — Introduction

- **Purpose:** Explain how to read the paper and distinguish fact, analysis, hypothesis,
  fictional example, and unverified item.
- **Executive summary:** One page synthesizing company, contractor workflow, product,
  voice technology, economics, competition, regulation, and risks. Written last.
- **Scope:** Public research only; no internal architecture, metrics, customers, or org
  claims.
- **Sources:** Cross-references to chapters 01–14 and appendix B; no duplicate research.
- **Open validation:** Which public claims remain uncertain at publication time?

### 01 — Company

- **Content:** Founding story and mission; public company description; IPO/public listing;
  customer segments; product and revenue language from filings and investor materials;
  acquisitions; leadership only where publicly documented; stated priorities.
- **Source candidates:** ServiceTitan company, investor relations, products, Pantheon
  press release, and SEC filings after verification.
- **Required caution:** Do not infer internal org structure, roadmap, margins, or strategy
  beyond public statements. Separate company-reported metrics from independent analysis.
- **Engineer lens:** Why a workflow platform makes voice-agent correctness a product
  and transaction problem, not only a speech problem.
- **Validation questions:** Current segment mix, product attach rates, internal owners,
  and roadmap are not public and remain questions after joining.

### 02 — The Trades Industry

- **Content:** Residential versus commercial; HVAC, plumbing, electrical, roofing,
  garage door, pest, landscaping, and adjacent trades; fragmentation; seasonality;
  weather demand; labor supply; roll-ups; memberships; financing; warranties.
- **Source candidates:** ServiceTitan industries page; government labor and industry
  sources after verification; public trade associations and reputable research.
- **Known gap:** No single verified public source covers all requested trades, market
  sizes, labor shortage, roll-ups, financing, and warranties. Use a source-per-claim
  approach and omit unsupported market-size synthesis.
- **Engineer lens:** Translate domain variation into intent, capacity, routing, policy,
  language, and evaluation slices.
- **Validation questions:** Customer-specific trade mix, regional seasonality, and actual
  operating policies cannot be inferred from public pages.

### 03 — How A Contractor Works

- **Content:** Lead → call → booking → dispatch → visit → diagnosis/estimate → sale →
  invoice → payment → membership → follow-up; roles and KPI definitions.
- **Source candidates:** ServiceTitan features, products, industries, Scheduling Pro,
  Dispatch Pro, Contact Center Pro, AI Virtual Agent, and the existing public-safe
  `docs/how-a-contractor-works.md`.
- **Diagrams:** Lead-to-cash Mermaid flow; role handoff diagram; capacity-to-dispatch
  sequence; voice-agent insertion points.
- **Known gap:** KPI definitions such as booking rate and close rate vary by contractor.
  Present definitions as working measurement conventions unless sourced.
- **Engineer lens:** Identify system-of-record boundaries and mutation points.
- **Validation questions:** Actual schemas, permissions, workflow states, and KPI SQL are
  internal and must be validated after joining.

### 04 — The Contact Center

- **Content:** Inbound call types; peaks and weather events; after-hours/overflow;
  answering services; CSR hiring/training/turnover; scripts; booking rules;
  capacity-aware scheduling; emergency handling; missed-call economics; CSR metrics.
- **Source candidates:** Contact Center Pro, AI Virtual Agent, Scheduling Pro, industries
  page, company pages, customer case studies, and government/regulatory sources after
  verification.
- **Known gap:** Public sources do not establish general call mix, turnover, missed-call
  cost, or peak distributions. These become `[unverified]` or are expressed as questions.
- **Engineer lens:** Model the call as a constrained operational workflow with human
  fallback, not as an unconstrained FAQ bot.
- **Validation questions:** Actual queue, transfer, staffing, and quality definitions.

### 05 — Pain Points

- **Taxonomy:** Missed calls; after-hours coverage; CSR turnover; technician shortage;
  schedule/capacity mismatch; marketing waste; data silos; cash flow; expectations.
- **Per pain point:** Public evidence; affected role; current handling; software/AI help;
  limits and failure modes; measurable outcome.
- **Source candidates:** ServiceTitan product pages and customer case studies; public
  labor/regulatory sources after verification; existing `docs/evaluating-voice-agents.md`.
- **Rule:** A product page demonstrates positioning, not prevalence or causal impact.
  Customer results remain attributed and not generalized.
- **Engineer lens:** Convert pain point into a falsifiable hypothesis and baseline.
- **Validation questions:** Which pain is highest priority internally and which metric is
  trusted are not public.

### 06 — ServiceTitan Product Landscape

- **Content:** Core platform; Pro products; Contact Center, Marketing, Scheduling,
  Dispatch, Field, Pricebook, Payments; Titan Intelligence; Atlas; AI Voice/Virtual
  Agents; Max; integrations and ecosystem.
- **Source candidates:** ServiceTitan products, features, industries, Contact Center Pro,
  Scheduling Pro, Dispatch Pro, Atlas, AI Virtual Agent, and Pantheon press materials.
- **Map:** Each public capability to the lifecycle in chapter 03.
- **Known gap:** Product pages do not prove implementation boundaries, adoption, pricing,
  roadmap, or internal ownership.
- **Engineer lens:** Treat product claims as external contracts and identify where
  configuration becomes policy.
- **Validation questions:** Packaging, APIs, entitlements, tenancy, and internal service
  boundaries require authorized information.

### 07 — AI Voice Agents In The Trades

- **Content:** Booking, rescheduling, confirmation, membership visits, escalation;
  overflow/after-hours/24-7 deployment; controls; public results with attribution;
  known limits; customer evaluation.
- **Source candidates:** AI Virtual Agent, Contact Center Pro, Scheduling Pro, OpenAI
  Realtime docs, LiveKit docs, existing call-anatomy and evaluation docs.
- **Known gap:** Public claims about booking percentages and implementation time are
  vendor/customer-reported and may not be comparable. Include attribution, date, sample
  caveats, and no generalization.
- **Engineer lens:** Build a claims/evidence chain from caller utterance to committed state.
- **Validation questions:** Actual production error taxonomy, deployment mix, and fallback
  policy are not public.

### 08 — Voice-AI Technology Landscape

- **Content:** Link to canonical architecture doc rather than duplicate it; cascaded vs
  speech-to-speech; transport, STT/TTS, realtime models, orchestration, observability;
  SIP/PSTN/transfers; latency and reliability; commoditizing versus differentiating.
- **Source candidates:** OpenAI Realtime, LiveKit Agents/turns/telephony, LangChain,
  LangGraph, LangSmith, Anthropic agent patterns, LiveKit 101 playlist, existing labs.
- **Known gap:** Vendor feature claims change quickly; record verification date and
  tested package versions.
- **Engineer lens:** Separate transport mechanism, model proposal, workflow authority,
  and business outcome instrumentation.
- **Validation questions:** Actual provider mix, SLOs, cost model, and deployment topology.

### 09 — Competitive Landscape

- **Content:** Field-service-management platforms; AI voice/answering startups serving
  trades; horizontal contact-center AI; answering-service incumbents. Compare positioning
  dimensions, not rankings.
- **Source candidates:** Competitor official product pages and investor materials only
  after individual URL verification; public analyst/reputable press only for corroboration.
- **Known gap:** A complete market map is unstable and likely to overstate equivalence.
  Use a dated comparison matrix and omit vendors without verified public sources.
- **Engineer lens:** Compare data/workflow integration, transaction authority, deployment,
  evaluation, transfer, and operational control.
- **Validation questions:** Win/loss data, competitive pricing, and actual differentiation.

### 10 — Regulation And Compliance

> General education, not legal advice. Requirements vary by jurisdiction, role, channel,
> contract, and facts; counsel and compliance owners must validate any design.

- **Content:** Recording consent; TCPA/outbound calling/texting; A2P 10DLC; FCC AI voice
  treatment; bot disclosure; PCI DSS; CCPA/privacy; accessibility; retention.
- **Source candidates:** EPA/PCI/California DOJ verified pages; FCC, FTC, DOJ, state
  statutes, FCC orders, and carrier guidance only after second verification.
- **Known gap:** Many regulator URLs were blocked or moved during planning. No legal
  conclusion should be written until primary pages are re-verified.
- **Engineer lens:** Consent state, disclosure, redaction, retention, transfer, payment
  isolation, auditability, and jurisdiction metadata become explicit design inputs.
- **Validation questions:** Applicable jurisdictions, contracts, counsel interpretations,
  recording policy, and retention schedule.

### 11 — Economics And Metrics

- **Content:** Call/job unit economics; sourced industry figures; booking, containment,
  escalation correctness, CSAT, revenue per call; baselines/counterfactuals/seasonality;
  attribution and contractor-outcome reporting.
- **Source candidates:** ServiceTitan investor relations and product/customer pages;
  public case studies; SEC filings after verification; existing evaluation guide.
- **Known gap:** Unit economics vary too much for a universal model. Use equations and
  sensitivity analysis; label hypothetical numbers clearly rather than inventing inputs.
- **Engineer lens:** Define denominators, slices, counterfactual, guardrails, and causal
  limits before optimizing model quality.
- **Validation questions:** Actual pricing, costs, margins, and attribution windows.

### 12 — Risks And Failure Modes

- **Content:** Gas/CO/electrical/flooding; wrong/double booking; unauthorized commitments;
  hallucinated confirmations; trust; accents/languages; noise; elderly callers;
  adversarial callers; outages/fallbacks.
- **Source candidates:** Existing labs and evaluation docs; EPA Section 608; official
  vendor docs; accessibility/regulatory sources after verification.
- **Matrix:** Severity, likelihood reasoning, mitigations, detection, offline tests,
  online monitors, human review, and rollback.
- **Known gap:** Severity and likelihood values must be analysis, not asserted statistics.
- **Engineer lens:** Combine OOD detection, policy enforcement, fault containment, and
  evidence-grounded evaluation.
- **Validation questions:** Incident history, risk acceptance, escalation contracts, and
  safety review process.

### 13 — Future Directions

- **Public direction:** Atlas, automation, agentic back office, and public AI product
  statements.
- **Analysis labels:** Outbound agents, multimodal assistance, predictive capacity, and
  technician copilots are clearly marked `Hypothesis:` and never presented as roadmap.
- **Source candidates:** Pantheon press release/recap, current Atlas and AI Virtual Agent
  pages, investor materials after verification, vendor research papers.
- **Known gap:** No private roadmap or internal timing will be inferred.
- **Engineer lens:** Identify experiments that test value without committing to a future
  architecture.
- **Validation questions:** Actual roadmap, investment, sequencing, and success criteria.

### 14 — Implications And Open Questions

- **Content:** Synthesis for an ML engineer with evaluation, OOD, and edge-inference
  experience; leverage areas; hypotheses to validate; questions for manager, PM,
  CSR/support partners, and customers.
- **Source candidates:** Prior chapters, existing architecture/evaluation/90-day docs,
  and public sources already cited.
- **Rule:** Write options and hypotheses, not first-person reflections or claims about
  internal needs.
- **Engineer lens:** Evaluation harnesses, failure taxonomy, turn/OOD detectors, edge
  latency, safe fallbacks, and measurement design.
- **Validation questions:** Consolidated post-joining questions, explicitly unanswered.

### Appendix A — Timeline

- **Content:** Dated founding, public listing, public product, acquisition, AI, and
  Pantheon milestones.
- **Sources:** Investor relations, official press releases, SEC filings after verification.
- **Rule:** Every date gets a source; no inferred milestones.

### Appendix B — Sources

- Deduplicated source list grouped by company/IR, industry/government, regulation,
  technology/vendor, competition, research, and press.
- Include final URLs, title, publisher, publication/update date where available, and the
  chapters that cite each source.

### Claims Ledger

- Columns: claim, chapter, URL, date checked, supported (yes/partial/no), notes.
- Every `partial` claim is narrowed or labeled; every `no` claim is removed before final QA.
- Final report counts total claims, supported, partial, removed, and `[unverified]` items.

## Known Research Gaps

- General market sizes, call mix, CSR turnover, missed-call economics, technician shortage,
  and private-equity roll-up prevalence need primary or reputable sources before inclusion.
- Current SEC, FCC, FTC, BLS, DOE, DOJ accessibility, TCPA/A2P, and state-law pages need
  URL verification from accessible final pages.
- Competitor coverage needs a fresh, neutral source pass; no competitor should be named
  merely because a URL is guessed or familiar.
- Public pages cannot establish internal architecture, owners, customer-level telemetry,
  roadmap, pricing, or incident history. Those remain post-joining questions.
- No company or customer metric will be used as a general industry statistic without an
  independent denominator and source.

## Structure Recommendations

- Keep all requested chapters separate: the audience benefits from distinct company,
  industry, workflow, contact-center, product, technology, economics, regulation, risk,
  and competition lenses.
- Use the existing `docs/voice-agent-architecture.md` as the technical architecture
  cross-reference; do not duplicate its diagrams or lab explanations.
- Keep `appendix-b-sources.md` separate from per-chapter numbered source lists because
  chapter-local citation context and a deduplicated bibliography serve different needs.
- Keep `claims-ledger.md` separate from sources because support status is a research QA
  artifact, not reader-facing bibliography.
- Do not merge the regulatory chapter into risks: compliance obligations and engineering
  failure modes overlap but require different evidence and review standards.
- Do not add a competitor ranking. Use comparison dimensions and dated public claims.

## Phase Sequence After Approval

1. Write chapters 01–05, one focused commit per chapter, with claims ledger entries.
2. Write chapters 06–09, one focused commit per chapter, with competitor URLs verified
   individually before inclusion.
3. Write chapters 10–14 and appendices, one focused commit per requested unit; leave
   unsupported legal/market sections out rather than filling them with generalities.
4. Write chapter 00 last, then integrate links and references.
5. Run consistency, URL, claims-ledger, sensitive-content, notebook, unit-test, lint, and
   repository checks before each commit; run the notebook suite once at the end as requested.
6. Delete this plan in Phase 5 only after all chapters and QA are complete.
