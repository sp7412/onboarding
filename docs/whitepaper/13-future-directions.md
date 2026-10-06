# 13 - Future Directions

**Estimated reading time:** 6 minutes · **Facts as of:** September 27, 2026

Stated direction is sourced. Everything labeled **Analysis** or **Hypothesis** is this
paper's interpretation, not company plans.


> **Update (Pantheon 2026, October 6, 2026):** Max is now available to all residential in-home contractors, with a limited commercial and roofing pilot; the company also announced the Atlas mobile app and Homh. See the [Pantheon 2026 AI roadmap brief](../pantheon-2026-ai-roadmap.md).

## Five Takeaways

1. ServiceTitan's stated direction is an **Agentic Operating System for the Trades**:
   automating contractor workflows end to end with AI. [1]
2. Atlas (introduced in fiscal 2026) is the agentic layer; Max is the program bringing it to
   customers, with more than 700 enrolled locations expected by fiscal year-end. [1][2]
3. The company is also using AI internally to raise its own development speed. [1][3]
4. Voice models are gaining reasoning and tool-use ability quickly, which expands what a
   phone agent can safely attempt. [4]
5. Analysis: voice will likely become one front door into a broader agent system, not a
   standalone product.

## What the company has said

- **Agentic Operating System.** Fiscal 2027 results describe delivering an agentic operating
  system to the trades and leveraging AI for organizational velocity. [1] The company's
  boilerplate now describes ServiceTitan as "AI for the trades." [1]
- **Atlas.** The 10-K introduces Atlas as an agentic AI layer, the next evolution of the Titan
  Intelligence engine, [2] and the Atlas page lists some capabilities as coming soon. [5]
- **Max.** Leadership doubled Max locations in fiscal Q2 2027 and expects more than 700 by
  year-end, citing execution with existing and select new customers. [1]
- **Internal AI.** Leadership described adopting AI across all functions to speed up product
  development. [3]

## Plausible directions (analysis and hypotheses)

1. **From answering to orchestrating.** *Hypothesis:* voice agents evolve from booking calls to
   triggering downstream work (dispatch adjustments, parts checks, follow-ups) through the same
   agent layer as Atlas.
2. **Outbound and proactive contact.** *Hypothesis:* maintenance reminders, rescheduling
   around weather or capacity, and missed-call follow-ups. This is where TCPA consent rules
   bite hardest (chapter 10). [6]
3. **Omnichannel continuity.** *Analysis:* callers move between phone, text and web; Contact
   Center Pro's Universal Inbox points toward one conversation across channels. [2]
4. **Technician copilots.** *Hypothesis:* field-facing assistants for diagnosis, options and
   documentation, sharing tools and policies with front-office agents.
5. **Better models, same constraints.** *Analysis:* realtime models with reasoning and parallel
   tools [4] make more ambitious flows possible, which makes evaluation, grounding and
   escalation *more* important, not less.

## What this means for a voice-agent engineer

- Build components (policy checks, evaluators, escalation contracts) that can serve more than
  one agent.
- Expect the definition of "voice agent" to widen; keep interfaces to the rest of the
  platform clean.

## Questions to validate after joining

- How do voice agents, Atlas and Max share architecture, tools and roadmaps?
- Is outbound voice on the roadmap, and how will consent be handled?
- How is internal AI adoption changing engineering practice on the team?

## Sources

1. ServiceTitan fiscal Q2 2027 results (September 8, 2026): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm>
2. ServiceTitan Form 10-K, fiscal 2026: <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
3. The Motley Fool, ServiceTitan Q4 fiscal 2026 earnings call transcript: <https://www.fool.com/earnings/call-transcripts/2026/03/12/servicetitan-ttan-q4-2026-earnings-transcript/>
4. OpenAI, "Advancing voice intelligence with new models in the API": <https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/>
5. ServiceTitan, Atlas: <https://www.servicetitan.com/features/atlas>
6. FCC Declaratory Ruling FCC 24-17: <https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf>
