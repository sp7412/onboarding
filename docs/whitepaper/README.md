# Background Whitepaper

This whitepaper is a public-source research primer on contractor workflows and the
engineering implications of voice agents.

## Status

Research passes completed September 27–28, 2026. Every chapter is now built on public
primary sources where they exist (SEC filings, the FCC, BLS, regulators, vendor
documentation), with analysis labeled. Chapter 14 is a working brief for the first 90 days.

**Essentials path (about 2 hours):** 00 → 01 → 02 → 06 → 07 → 10 → 11 → 14.

## Reading Order

1. [00 - Introduction](00-introduction.md)
2. [01 - Company](01-company.md)
3. [02 - The Trades Industry](02-the-trades-industry.md)
4. [03 - How A Contractor Works](03-how-a-contractor-works.md)
5. [04 - The Contact Center](04-the-contact-center.md)
6. [05 - Pain Points](05-pain-points.md)
7. [06 - Product Landscape](06-product-landscape.md)
8. [07 - AI Voice Agents](07-ai-voice-agents.md)
9. [08 - Technology Landscape](08-technology-landscape.md)
10. [09 - Competitive Landscape](09-competitive-landscape.md)
11. [10 - Regulation And Compliance](10-regulation-and-compliance.md)
12. [11 - Economics And Metrics](11-economics-and-metrics.md)
13. [12 - Risks And Failure Modes](12-risks-and-failure-modes.md)
14. [13 - Future Directions](13-future-directions.md)
15. [14 - Implications And Open Questions](14-implications-and-open-questions.md)
16. [15 - Agentic Orchestration](15-agentic-orchestration.md)
17. [16 - Shared Skills and Capability Libraries](16-shared-skills-and-capabilities.md)
18. [Appendix A - Timeline](appendix-a-timeline.md)
19. [Appendix B - Sources](appendix-b-sources.md)

The [claims ledger](claims-ledger.md) records the research checks behind the chapter
source lists. `[unverified]` marks a claim that needs a source or validation.

## Scope Gaps

Industry-wide call-mix, CSR turnover and missed-call cost statistics from neutral sources
remain gaps; figures from vendors are attributed as vendor claims.

## Agentic orchestration chapter

Chapter 15 is the architecture map for the existing multi-agent labs. It compares the
publicly described approaches from ServiceTitan, Salesforce, and Microsoft, then uses
LangChain/LangGraph and Microsoft Agent Framework as open-source implementation references.

It is intentionally explicit about the boundary between:

- public facts about ServiceTitan;
- architectural analysis and hypotheses;
- implementation patterns demonstrated by open-source projects.

For the hands-on path, pair Chapter 15 with Labs 05–14, especially the LangGraph,
shared-context, arbitration, learning-loop, and agent-to-agent labs.

## Shared skills chapter

Chapter 16 adds the reusable capability layer that sits between agents and orchestration.
It treats skills as versioned, evaluated business capabilities rather than prompt fragments,
and explicitly distinguishes the public ServiceTitan evidence for Skills & Capabilities from
the stronger hypothesis of a cross-agent skill registry or marketplace.

## Comparative architecture and harness docs

The companion docs make the architecture concrete beyond Chapter 15:

- [Comparative Agent Architectures](../comparative-agent-architectures.md) compares
  ServiceTitan, Salesforce, Microsoft, OpenAI, and Anthropic.
- [Agent Harness](../agent-harness.md) separates RAG, state, memory, tools, guardrails,
  workflows, and deterministic control.
- [Design by Evaluation](../design-by-evaluation.md) treats evaluation as a design input
  and connects traces, failure mining, regression, and rollout.

Use these after Chapter 15 when the question is not just "what are the patterns?" but
"where does control live, and how do we know the resulting system works?"
