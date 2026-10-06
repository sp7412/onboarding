# Pantheon 2026: The AI Roadmap Brief

**Facts as of: October 6, 2026 (evening) · Last reviewed: October 6, 2026**

ServiceTitan's annual user conference, Pantheon, ran October 5–7, 2026 in Orlando. This brief
covers what was publicly announced and said about AI, and what it means for an engineer
joining the voice-agent team. It uses only public sources: the company's press release, a
published keynote transcript and the conference live blog. Company claims are attributed as
such, and anything marked **Analysis** is this repo's interpretation.

> **Update planned:** this version covers the opening keynote and the official
> announcements. As of this evening, no transcripts or detailed coverage of the CTPO's
> residential keynote or Vahe Kuzoyan's keynote (both Oct 6) had been published; they and the
> "Charging Ahead with AI and Max" session (Oct 7) will be added when available. Replays are
> available for 90 days. [1][3]

## Five Takeaways

1. **The voice agent is now one agent inside a coordinated system.** Max bundles 30 agents
   across 18 business drivers, connected by a coordination system for shared context,
   shared judgment, coordinated action, arbitration and centralized supervision. [2]
2. **Leadership places voice agents at level 2 of a five-level AI maturity model:** valuable,
   but described as the beginning of the transition, not the destination. The target is a
   self-learning business. [2]
3. **Measurement is a first-class problem.** The company said its in-product booking rates are
   easy to game, so it built a "voice intelligence" agent that reviews every call to decide
   whether it was a bookable lead. [2]
4. **New booking channels are arriving, including other companies' AI agents.** Homh makes
   selected contractors discoverable and bookable by homeowners and their AI agents
   (ChatGPT, Gemini, Claude), with confirmed booking directly into ServiceTitan. [1]
5. **The guardrail philosophy is explicit.** The co-founder and president described AI agents
   needing business context, the ability to work alongside people, and "clear rules for when to
   act and when to ask." [1] Analysis: that's the control plane this repo's labs teach.

## 1. What was announced

From the official press release: [1]

- **Max for all residential in-home contractors.** Max is described as the fully loaded version
  of ServiceTitan's Agentic Operating System, whose agents use context across demand, field and
  office to decide what should happen next and carry it out across connected workflows.
- **A limited Max pilot for commercial and roofing,** with field agents (site-walk write-ups,
  daily logs, invoice review) and more described as coming soon.
- **The Atlas mobile app,** letting owners ask about performance and get answers grounded in
  company-wide data.
- **Homh,** a consumer demand-generation platform: real-time availability, performance
  signals and confirmed booking into ServiceTitan, reachable directly and through consumer AI
  assistants.
- **Partner ecosystem additions,** including giving AI CSRs access to Adaptive Capacity (the
  intelligence behind ServiceTitan's own scheduling) for capacity-aware booking, a Ramp
  integration, a supplier self-service portal and financing pre-approvals.

The release notes that features not yet generally available, including those described as
coming soon, may not arrive on the anticipated timeline. [1]

## 2. The opening keynote

From the published transcript of CEO Ara Mahdessian's keynote: [2]

**The AI maturity model.** Level 1: ask AI questions (Atlas). Level 2: automate individual
workflows, such as a voice agent that answers and books. Level 3: many automated workflows.
Level 4: coordinated automations. Level 5: a system that learns from every decision. He argued
the value jumps sharply at each level.

**How the voice agent evolved.** They started with the most visible missed opportunities:
off-hours calls and calls arriving while CSRs were busy, with an agent that could be set up in
minutes. It improved over months. To measure it honestly, they built voice intelligence to
judge whether each call was a bookable lead, and he said the agent now books as well as a good
CSR. Some customers reportedly let it handle all calls with CSRs on standby for escalations.
Voice intelligence was then extended to grade and coach human CSRs. Text and web-chat agents
followed. These are company-reported results.

**Why coordination was needed.** With 30 independent agents, each optimized its own metric and
the business still made poor decisions: ads kept spending with a full schedule; the voice agent
booked a high-value job but dispatch, lacking the context, sent a junior technician; a
speed-to-lead agent couldn't ask dispatch to free a slot. He framed the cost as an
"effectiveness tax" (money left on the table) and an "overhead tax" (people resolving
conflicts).

**The coordination system.** Five capabilities: shared context (what the voice agent hears,
dispatch knows), shared judgment (common lead-scoring and demand-forecasting models),
coordinated action (one agent can ask another to act, with customer consent where needed),
arbitration (choose the action with the highest expected value at the lowest expected cost) and
centralized supervision (one place to configure and monitor all agents).

**The learning loop.** Every outcome is tied back to the decisions that produced it (which ad,
what the customer said, which technician, predicted vs. actual job value), so the assumptions
behind each judgment improve over time.

**Adoption and scale.** Customers can adopt individual agents, third-party agents, their own
agents, or full Max (all 30 agents, all Pro products and a dedicated specialist). He said 700
locations are expected on Max by fiscal year-end, and some new customers start directly on Max.

**Details worth noting for the voice team** (second pass through the transcript):

- **Call content feeds other agents' judgment.** Lead scoring was described as using what was
  said on the call and the customer's tone, alongside details about the home, homeowner and
  equipment. Dispatch Pro was upgraded to consider every data point about a job, including the
  ad that produced the lead and what was said on the call.
- **Booking is multi-channel:** phone, text, web chat and Google. He said the web-chat agent
  captured new appointments rather than taking them from online scheduling.
- **The 30 agents span demand** (Google and Meta ads with multi-touch attribution, ad
  experiments, email campaigns, speed-to-lead for marketplace leads, social publishing,
  reputation), **booking**, and **revenue** (dispatch, good-better-best proposals with
  financing, estimate follow-ups, technician coaching). More agents are planned, particularly
  for the back office.
- **Demand forecasting drives standing down:** when the schedule is forecast full, demand
  agents pause and wait for a lighter day.
- **One command center** lets contractors configure each agent, see its metrics, review the
  actions it took, and act on insights it raises.
- **Partial adoption:** customers on individual Pro products get a subset of the agents; the
  platform was rebuilt so agents have the tools to act, and customers can bring third-party
  agents or build their own.
- **New competitive surfaces:** he expects contractors to have to compete in AI-assistant
  advertising as well as search ads.

**An illustrative profit model** (his example, not a forecast): improving leads, booking rate
and average ticket by 10% each lifts revenue about 33%, but can roughly double profit, because
much of the added revenue comes from the same marketing budget and truck rolls.

## 3. What this means for a voice-agent engineer

Analysis:

- **The voice agent's outputs are inputs to other agents.** What it captures (intent, urgency,
  constraints like "car stuck in the garage", job value signals) becomes shared context for
  dispatch and lead scoring. Expect work on that context contract: what to capture, how
  reliably, and how it's verified.
- **"Bookable" needs a definition you can defend.** The company's own answer to gameable booking
  rates was a separate judging agent. That makes evaluation design (what counts, who decides,
  how it's audited) central, which is the denominator lesson in this repo.
- **Booking decisions become arbitrated decisions.** With capacity-aware booking (Adaptive
  Capacity) and dispatch able to move appointments, the voice agent's booking is one proposal
  among several. The control plane must stay authoritative about what was actually committed.
- **Agent-to-agent booking changes the trust model.** With Homh, the caller may be another
  company's AI agent. Identity, authorization, consent, idempotency and abuse handling matter
  even more when no human is on the line.
- **The learning loop needs traceability.** Tying outcomes back to decisions requires linked
  traces from call to booking to job outcome, which is what lab 07 practices.
- **"When to act and when to ask" is the guardrail spec.** Escalation rules, confirmations and
  the claim guard are exactly that, made explicit and testable.

## 4. Questions to bring to the team

- How does the voice agent share context with the coordination system today, and what's the
  contract (fields, confidence, verification)?
- How does voice intelligence define a bookable call, and how is that judge evaluated?
- When agents disagree (booking vs. dispatch vs. demand), where is the arbitration logic, and
  how is it tested?
- How are bookings arriving through Homh and consumer AI assistants authenticated and validated?
- Which outcomes feed the learning loop for the voice agent, and how quickly?

## 5. Still to watch (replays)

From the conference schedule: [1][3]

- **Run Your Business, Not Your Software** (residential keynote, CTPO Abhi Mathur), Oct 6
- **The New World** (Vahe Kuzoyan, co-founder and president), Oct 6
- **The Next Era of Commercial** (Alex Kablanian), Oct 6
- **Charging Ahead with AI and Max**, Oct 7
- **The Power of the Ecosystem: ServiceTitan Partners**, Oct 7

## Related repo material

- Whitepaper [chapter 01](whitepaper/01-company.md) (company), [chapter 06](whitepaper/06-product-landscape.md) (products), [chapter 13](whitepaper/13-future-directions.md) (future directions)
- [Tools and guardrails](tools-and-guardrails.md), [Evaluating voice agents](evaluating-voice-agents.md)
- Lessons: denominator, claims vs. state, worth-it
- Labs 09–12 (teaching models of the general patterns): shared context ledger, coordination and
  arbitration, the learning loop, and agent-to-agent booking

## Sources

1. ServiceTitan press release, "ServiceTitan Announcing New and Expanded Capabilities at Pantheon 2026" (October 6, 2026): <https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html>
2. Investing.com, "ServiceTitan at Pantheon 2026: ai push aims to make trades self-running" (summary and full keynote transcript, October 6, 2026): <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
3. ServiceTitan, "Pantheon 2026: Live coverage from ServiceTitan": <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
