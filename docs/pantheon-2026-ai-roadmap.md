# Pantheon 2026: The AI Roadmap Brief

**Facts as of: October 7, 2026 (morning) · Last reviewed: October 7, 2026**

ServiceTitan's annual user conference, Pantheon, is a three-day event in Orlando; the 2026 keynotes
opened it on Tuesday, October 6. [1][3] This brief
covers what was publicly announced and said about AI, and what it means for an engineer
joining the voice-agent team. It uses only public sources: the company's press release, a
published keynote transcript and the conference live blog. Company claims are attributed as
such, and anything marked **Analysis** is this repo's interpretation.

> **Update planned:** this version covers the opening keynote, the official announcements and
> the live blog's coverage of the Oct 6 keynotes (section 2a). The Oct 7 sessions, including
> "Charging Ahead with AI and Max", will be added when coverage or transcripts are published.
> The press release says replays are available for 90 days. [1]

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

## 2a. The Oct 6 keynotes (live-blog coverage)

From ServiceTitan's own live blog, which summarizes and quotes the keynotes rather than
transcribing them. All of these are company or customer claims. [3]

**Abhishek Mathur, chief technology and product officer** (live-blog post headlined "One Open
Slot, One AI Agent, and the Case for Max"):

- Everything shown was described as "real and in production today."
- Max was framed as agents that autonomously do the work rather than just track it, and Atlas
  as a conversational agent that lets employees "ask questions, get guidance and take action."
- The live blog reports him saying that some customers on Pro and Max products grew revenue
  twice as fast year over year as non-Max peers, and naming four factors: insights, automation, a connected brain and
  personalization.
- **New tools:** the Atlas app for the office on mobile, a no-code Automation Hub, and an
  **MCP server connecting Claude or ChatGPT to ServiceTitan data**.
- **Max availability, stated more narrowly than the press release:** "Max will be open after
  Pantheon to all ServiceTitan customers in plumbing, heating, electrical and garage doors with
  four or more technicians." The press release says "all residential in-home contractors." [1]
- In the same session, senior vice president Vincent Payen said average revenue realization
  in the room is about 60%, while top performers reach the high 80s.

**Vahe Kuzoyan, co-founder and president** (live-blog post headlined "Max, Atlas, and Homh take
the next step at Pantheon"):

- In the blog's own narration (not quotes): Max opens to commercial and roofing through a
  limited pilot; Atlas is now a chief-of-staff-level agent with a dedicated mobile app; and the
  Homh app plugin is already live on ChatGPT, Google Gemini and Claude, as a curated
  marketplace connecting top contractors with consumers.
- "We're ServiceTitan, the agentic operating system of the trades." (in quotation marks at the
  close of the blog's coverage of his keynote, without a speaker tag). On AI adoption, a
  quote the blog attributes to him directly: "Keep
  testing. The most dangerous thing you can do at this moment is treat one failed attempt as
  proof of what will never be possible."

**Alex Kablanian, GM of Commercial & Construction** (live-blog post headlined "Max brings AI
agents to commercial contractors"): commercial agents include an Equipment Agent, a Findings Agent that reviews
completed work orders for missed findings, a Daily Log Agent that builds a foreman's log from
voice notes and photos, and an Invoice Agent. One customer's invoice prep reportedly dropped
"from 30 minutes to under 5 minutes."

**Voice-relevant items elsewhere in the day-one coverage:**

- The live blog reports that a customer, Davis AC in Houston, credits its AI Virtual Agent
  ("Nell") with a 98% booking rate and the ability to answer multiple calls at once during
  peak season. This is a customer claim, and "booking rate" is the in-product metric the
  company itself called easy to game (takeaway 3).
- In its summary of CEO Ara Mahdessian's opening keynote, the live blog makes the point that a
  CSR can't take a call on one line and also answer a text within 15 seconds, before the
  customer turns to a competitor. (This is the blog's narration, not a verbatim quote.)

## 3. What this means for a voice-agent engineer

Analysis:

- **The voice agent's outputs are inputs to other agents.** What it captures (intent, urgency,
  constraints like "car stuck in the garage", job value signals) becomes shared context for
  dispatch and lead scoring. Expect work on that context contract: what to capture, how
  reliably, and how it's verified. Teaching draft: [Call facts contract](call-facts-contract.md).
- **"Bookable" needs a definition you can defend.** The company's own answer to gameable booking
  rates was a separate judging agent. That makes evaluation design (what counts, who decides,
  how it's audited) central, which is the denominator lesson in this repo. Practice:
  [Bookability judge](../senior-engineer/bookability-judge.md). A customer's reported 98%
  booking rate (section 2a) is exactly the kind of number to read with that lens: 98% of
  what denominator, judged by whom?
- **Booking decisions become arbitrated decisions.** With capacity-aware booking (Adaptive
  Capacity) and dispatch able to move appointments, the voice agent's booking is one proposal
  among several. The control plane must stay authoritative about what was actually committed.
- **AI-agent-assisted booking changes the trust model.** Homh publicly describes homeowners'
  AI agents participating in discovery and booking. Identity, authorization, consent,
  idempotency and abuse handling are therefore useful trust-boundary questions; the public
  announcement does not specify the protocol. Notes: [Homh and AI-agent booking](homh-and-agent-booking.md).
- **AI assistants reach the platform from two directions.** Homh puts contractors inside
  consumer assistants, and the new MCP server connects Claude or ChatGPT to a contractor's own
  ServiceTitan data. Both make permissions and what an assistant may read or do first-class
  design questions, the same trust boundary as tool calls in lab 02.
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
- What can the MCP server read or do, and how are its permissions scoped per user and per
  customer?

The [hypothesis map](hypothesis-map.md) expands these into more than a dozen public-grounded hypotheses,
each with how to test it and whom to ask in weeks 1–2.

## 5. Still to watch (replays)

From the conference schedule: [1][3]

- **Charging Ahead with AI and Max**, Oct 7, 11:15 am ET
- **Built Together: The Power of the ServiceTitan Ecosystem**, Oct 7, 10:15 am ET
- **All-Star Titans** (closing session), Oct 7, 2 pm ET
- Full transcripts of the Oct 6 keynotes, to check the live blog's summaries (section 2a)
  against the speakers' actual words

When replays or transcripts appear, extract only new **publicly verifiable** claims about
voice, bookability, Homh, Adaptive Capacity for AI CSRs, or coordination. Attribute company
claims, distinguish inference from fact, and update this brief and the [claims ledger](whitepaper/claims-ledger.md).

## Related repo material

- [Call facts contract](call-facts-contract.md) — teaching schema for shared context from a call
- [Homh and AI-agent booking](homh-and-agent-booking.md) — trust surfaces when an AI assistant is in the booking path
- [Bookability judge](../senior-engineer/bookability-judge.md) — judgment exercise on gameable booking rates
- Whitepaper [chapter 01](whitepaper/01-company.md) (company), [chapter 06](whitepaper/06-product-landscape.md) (products), [chapter 13](whitepaper/13-future-directions.md) (future directions)
- [Tools and guardrails](tools-and-guardrails.md), [Evaluating voice agents](evaluating-voice-agents.md)
- Lessons: denominator, claims vs. state, worth-it
- Labs 09–14 (teaching models of the general patterns): shared context ledger, coordination and
  arbitration, the learning loop, agent-to-agent booking, the call-facts capstone and earning
  autonomy

## Sources

1. ServiceTitan press release, "ServiceTitan Announcing New and Expanded Capabilities at Pantheon 2026" (October 6, 2026): <https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html>
2. Investing.com, "ServiceTitan at Pantheon 2026: ai push aims to make trades self-running" (summary and full keynote transcript, October 6, 2026): <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
3. ServiceTitan, "Pantheon 2026: Live coverage from ServiceTitan" (live blog, read October 7, 2026): <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
