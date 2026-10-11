# Pantheon 2026: The AI Roadmap Brief

**Facts as of: October 10, 2026 · Last reviewed: October 10, 2026**

ServiceTitan's annual user conference, Pantheon, is a three-day event in Orlando; the 2026 keynotes
opened it on Tuesday, October 6. [1][3] This brief
covers what was publicly announced and said about AI, and what it means for an engineer
joining the voice-agent team. It uses only public sources: the company's press release, a
published keynote transcript, the conference live blog, and current ServiceTitan help documentation. Company claims are attributed as
such, and anything marked **Analysis** is this repo's interpretation.

> **Update (October 10):** the live blog now includes additional partner and customer recaps
> plus a public write-up of the "Charging Ahead with AI and Max" breakout. Strengthened caveats
> on partner-reported A/B testing, certified-partner booking, planned webhooks and programmatic
> onboarding, and customer anecdotes (sections 2b–2d). Section 2e covers the remaining recaps:
> Atlas capability list and next-year goals, Homh ranking signals, planned commercial and
> roofing Max agents, and the service-agreement and big-ticket-sales breakouts. Full session
> recordings are still expected through Academy about 4–6 weeks after the event. Atlas help
> documentation shows a permissioned, action-taking interface (section 5). [3][4][5][6]

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

## 2b. The Oct 7 partner-ecosystem keynote (live-blog coverage)

The live blog recaps a Wednesday keynote that followed one job through ServiceTitan's partner
ecosystem (the schedule lists "Built Together: The Power of the ServiceTitan Ecosystem" for
that morning). All of this is the blog's summary of company and partner claims. [3]

- **Partner trust as a product.** Girish Chander, VP of Product, framed integrations around
  cybersecurity and described a partner certification program that sets security and
  data-handling standards. His words: "It has to be one where we offer you a choice that you
  can trust."
- **Booking by a third-party AI.** Avoca, an AI voice company, books jobs against a
  contractor's real capacity through an API open to certified partners. The blog does not
  specify the API's authentication, authorization, idempotency, or transaction semantics;
  those remain questions, not facts.
- **Integration plumbing (planned).** Webhooks to notify connected apps when a job changes are
  due by year-end, and programmatic onboarding aims to cut partner setup to minutes. These are
  announced plans, not a guarantee of current availability.
- **MCP, demonstrated as in development.** Chander asked Claude, connected through a
  ServiceTitan Model Context Protocol server described as still in development, to find
  materials unused for a year and then two; Claude offered to deactivate the stale items. "You
  didn't need to know what the APIs were," he said.

The blog also recaps a Tuesday session on Atlas and the Max Command Center: Atlas places
holds on open capacity when a campaign launches and releases them if bookings fall short,
each recommendation shows its reasoning ("Every recommendation tells you why Atlas made it and
what it expects to happen," said Juliette Armour), and Command Center is in private preview
for Max customers. The session also highlighted the need to record when another user has
already acted on a recommendation, so an owner and marketing manager do not both execute the
same action. [3]

**Engineering interpretation (not a claim about the implementation):** this is a reservation
and concurrency problem, not just an agent-planning problem. A safe design needs an authoritative
capacity check at commit time, idempotent retries, a clear hold lifecycle, and a release or
reconciliation path when actual bookings differ from the forecast. A recommendation should
remain a proposal until the application confirms the state change. The public coverage does not
specify the underlying transaction, locking, or idempotency mechanism.

Analysis: the Oct 6 coverage listed the MCP server among new tools; the Oct 7 demo describes it
as still in development, so treat availability as unconfirmed. Two booking paths now run
through outside AI: a partner voice agent calling a certified API, and consumer assistants via
Homh. Both make the guarded booking boundary in lab 12 and the
[MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md) note directly
relevant. And the demo's offer to deactivate stale items is a write action proposed through
MCP: the confirm-before-commit step around it is the control plane.

## 2c. Live-blog wrap-up items (read October 8)

The live blog has closed out the conference ("That's a wrap for Pantheon 2026!!"). Its later
posts add a few items that the summaries above leave out. Where the blog places a post under a
day heading that doesn't match the session, this brief doesn't assign it a day. [3]

- **Atlas availability is narrower than "launched".** The blog quotes Kuzoyan directly:
  "Atlas is in closed alpha for admins only." and "We haven't set pricing and packaging yet."
  Read this alongside section 2a's "chief-of-staff-level agent with a dedicated mobile app".
- **Agent booking on a contractor's own website.** In the same post, the blog describes
  contractors being able to "add a direct booking connection (MCP) to your website so agents
  can book jobs", and adds "The numbers are small today." This is a third outside-AI booking
  path, alongside Homh in consumer assistants and certified partners like Avoca (section 2b).
- **Partner evaluation practice.** Avoca "tests every change, down to the greeting, by
  splitting calls between two versions" and, per the blog, rolls out a winner only when the
  result is statistically significant. This is a useful example of evaluating voice-agent
  changes as controlled experiments, but the public post does not disclose sample sizes,
  stopping rules, metrics, or experimental design.
- **Setup time for an AI Virtual Agent.** A customer story says Superior Plumbing's AI Virtual
  Agent ("Piper") "took about 30 minutes to get running" and handles appointment booking,
  freeing CSRs for callers who need hands-on help. This is a customer claim, with no booking
  metric given. Like the Davis AC 98% booking-rate claim in section 2a, treat these as
  attributed anecdotes, not benchmarks or expected performance targets.
- **Other partner items:** Affirm pay-over-time is live in estimates; Ramp bill pay and expense
  management is generally available; Ford Pro vehicle data (model year 2020 and newer) flows
  into Fleet Pro with no extra hardware; and a supplier-connected catalog is being built with
  design partners.
- **Next year:** Pantheon 2027 is Sept. 13–16, 2027, in Nashville.

Analysis: a booking connection on the contractor's own site turns MCP from an internal-data
tool into a public booking surface. The trust questions in the
[MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md) note
(authorization, idempotency, confirm before commit) then apply to unknown outside agents, not
just to a contractor's own assistant. "Closed alpha" and "the numbers are small today" both
say the same thing: these surfaces are early, so plan for them changing rather than treating
them as settled interfaces.

## 2d. Engineering implications of the expanded partner coverage (reviewed October 10)

The partner and customer details in sections 2b and 2c sharpen a few engineering questions
without establishing ServiceTitan's internal implementation. [3]

- **Cross-product state.** Affirm's "no information black holes" framing means partner-side
  changes should flow back into the platform. Treat partner callbacks as potentially
  duplicated, delayed, or out of order; verify authoritative state and design idempotent
  consumers. This is a general design recommendation, not a claim about the implementation
  ServiceTitan uses.
- **What changed in the onboarding interpretation.** The partner ecosystem is not only a
  discovery or tool-calling concern. It includes the lifecycle of externally initiated bookings
  and events, and the measurement discipline needed to decide whether voice-agent changes
  actually improve outcomes. The existing
  [MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md),
  [capacity reservation review](../senior-engineer/capacity-reservation-review.md), and
  [bookability judge](../senior-engineer/bookability-judge.md) remain the right exercises;
  this update adds evidence and caveats rather than inventing a new architecture.

## 2e. Remaining live-blog coverage: Atlas, Homh, Max pilots and breakouts (read October 10)

Earlier passes covered the headline keynotes. This pass adds the live blog's remaining
AI-relevant recaps. All of it is the blog's summary of company, partner and customer
statements, not a transcript, and results are self-reported without denominators. Sessions
without substantial AI implementation detail (including roofing M&A, private equity, the
roofing process-and-pricing story, the Prometheus Awards, and the Manning fireside, whose AI
references were general adoption and leadership observations) are intentionally left out. [3]

**"Charging Ahead with AI and Max" (Oct 7 breakout).** Three early Max customers, seated by
ServiceTitan's chief revenue officer, Ross Biestman:

- **HomeX Services Group (CTO Jennifer D'Ambra).** Dispatch Pro ran across its Northeast
  brands, but its optimization rate stayed near 30%. Moving to Max became a reason to
  standardize skills, job types and business units. After that, she said, Dispatch Pro showed a
  large jump that she credited mostly to the cleaned-up definitions. No new figure is given. Her
  lesson: an AI tool fed unstandardized data returns poor results however sophisticated it is.
- **Guild Garage Group (COO Jake Wold).** 29 businesses, over 1,000 employees and about $350
  million in revenue; Wold wants revenue to grow faster than headcount. Two Guild businesses
  already have AI answer the call, book it and dispatch a technician. Moving to Max let Guild
  drop 29 other monthly invoices, including API add-ons that lived outside ServiceTitan.
- **A thin-margin operator (Steven Gurley, Goodrich family office).** Retail backup power earns
  less than HVAC, plumbing or garage doors, so he wants a clear benefit before adopting any AI
  tool, and he questions asking technicians to juggle many apps.
- **Advice.** Wold: take the demo, build a business case, then commit. D'Ambra: be intentional
  and get the team on board first.

**Atlas, beyond "closed alpha" (Kuzoyan keynote recap).** The blog lists what Atlas does today:
reporting from existing reports, with a custom query when the metric doesn't exist; "why"
analysis, including review of customer conversations from jobs that ended in recalls (with
consent); building and modifying rule-based workflows and recommending who should act;
monitoring that notifies when a rule trips (for example, variance above 5%); and cleaning
marketing cost data for return on ad spend. It also has a voice mode and picks up on the web
where a conversation left off, and the blog says it will over time replace the Office app.
Stretch goals for next year's Pantheon include connecting to email and calendar, joining
meetings to capture commitments, and building or modifying other agents. Atlas pricing and
packaging are not set. These are goals, not commitments.

**Homh ranking signals (Kuzoyan keynote recap).** Homh scores contractors on punctuality, hired
rate (whether the homeowner chooses to proceed after meeting the contractor) and job
quality and satisfaction. The blog says these metrics are becoming part of ServiceTitan
reports, visible whether or not a contractor is on Homh. Three stated commitments: contractors
cannot pay to rank higher, and will not be charged to remove a negative comment or to promote
a positive review. Homh is invite-only in a few areas for now, and profiles build on existing
ServiceTitan history. The keynote's framing is that a homeowner's AI agent becomes the customer
and picks the contractor it believes will solve the problem.

**Planned Max agents for commercial and roofing pilots.** The blog lists agents planned by next
year. Commercial: cross-sell agents that turn new installs into service-agreement proposals and
flag replacement opportunities with a total-cost analysis; a technician-development agent that
schedules toward certification hours; and a construction estimate-variance agent. Roofing: a
claims and supplement agent that reconciles the adjuster's scope with the estimate; a
production agent that breaks a sold estimate into jobs, books crews and deliveries and
reschedules for weather; and a subcontractor-management agent. Separately, the commercial keynote
said the Daily Log Agent can call an RFI Agent or Change Order Agent when it spots a field
conflict, and a customer (Gulfshore Air and Heating) reported days to payment down 70% with the
Invoice Agent.

**Service agreements breakout (Gallo Mechanical).** The product team showed technicians
logging findings by voice, photo or text, with the application scanning notes, photos and job
summaries for problems no one wrote up and flagging a pattern when the same issue appears
three times, to give sales a reason to revisit a declined recommendation. An agreement-review
agent flagged a problem with the first two quarterly invoices on a live agreement. Gallo's COO
said agreements grew 38% this year and that follow-on work runs far higher margin than the
agreement itself. Company-reported.

**Big-ticket sales breakout.** Peterman Brothers said it connects a customer to one of six
virtual salespeople over Zoom when a technician finds a broken system, closing in the 60% range
by its own account, and ties more first-call price requests to ChatGPT. Redwood Services said it
uses call recording and AI to check whether salespeople hit the main steps of its process,
without a script. Both are self-reported.

Analysis: three themes matter for a voice-agent engineer. (1) Agent quality depends on
configuration quality: a before/after claim can confound the model with a tenant's cleanup, so
evaluations should record the configuration they ran against. (2) Homh's ranking signals are
derived from operational data, which makes them an integrity surface: who can influence
punctuality, hired-rate or feedback data, and how gaming is detected (see
[Homh and AI-agent booking](homh-and-agent-booking.md)). (3) AI review of recorded calls and
unstructured findings is evaluation against steps and extracted facts, the same shape as the
[bookability judge](../senior-engineer/bookability-judge.md) and the
[call facts contract](call-facts-contract.md), with the same denominator, consent and
recording-rule questions. Atlas's stretch goals (meetings, email, building agents) widen the
trust-boundary questions in the [MCP note](mcp-and-external-agent-trust-boundary.md) rather
than settle them.

## 3. What this means for a voice-agent engineer

Analysis:

The public material points at a system where the voice agent is one participant among many,
not a standalone product. That has concrete consequences for anyone building or hardening a
voice path:

- **Bookability is a judgment problem, not a metric.** The company built a separate agent to
  decide whether a call was bookable because the in-product rate is gameable. A voice team that
  optimizes only the rate the product already shows will be optimizing the wrong thing. The
  [bookability judge](../senior-engineer/bookability-judge.md) exercise is the practical form of
  that point.
- **Capacity is shared and contended.** Adaptive Capacity for AI CSRs, Atlas holds on open
  capacity, and partner booking against real capacity all assume a single source of truth for
  what is still available. Concurrent agents (and concurrent humans) need an authoritative
  check at commit time, not only a plan-time forecast. See the
  [capacity reservation review](../senior-engineer/capacity-reservation-review.md).
- **Outside agents are already in the booking path.** Homh (consumer assistants), certified
  partners like Avoca, and a contractor-website MCP connection are three external booking
  surfaces. Authorization, tenant scoping, idempotency, and confirm-before-commit are not
  optional extras; they are the trust boundary. The
  [MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md) note is the
  checklist.
- **Configuration quality gates agent quality.** A customer reported that Dispatch Pro's
  optimization rate moved only after standardizing skills, job types and business units
  (section 2e). Expect agent work to depend on how clean each tenant's setup is, and to
  need evaluations sliced by configuration.
- **Coordination is the product.** Shared context, shared judgment, coordinated action,
  arbitration and centralized supervision are how the company describes Max. A voice agent that
  cannot hand off context, accept an override, or report an outcome cleanly will be a liability
  inside that system.
- **The learning loop needs traceability.** Tying outcomes back to decisions requires linked
  traces from call to booking to job outcome, which is what lab 07 practices.
- **"When to act and when to ask" is the guardrail spec.** Escalation rules, confirmations and
  human-in-the-loop are the product of that philosophy.

None of this is a claim about ServiceTitan's internal implementation. It is what the public
announcements imply for an engineer who has to design a voice agent that will live in (or next
to) such a system.

## 4. Adaptive Capacity for AI CSRs

From the press release and live blog: partners and AI CSRs can use Adaptive Capacity — the same
intelligence behind ServiceTitan's own scheduling — so bookings respect real capacity rather than
a static calendar. [1][3] Analysis: that is a capacity-reservation problem at the boundary between
an external agent and the platform's source of truth. The
[capacity reservation review](../senior-engineer/capacity-reservation-review.md) is the exercise.

## 5. Atlas as a permissioned, action-taking interface

ServiceTitan's current Atlas documentation adds implementation-relevant evidence:

- Personas and access controls determine what Atlas can see and do. [4]
- Atlas can be used inside Adaptive Capacity strategic rules. [5]

The repo's new [MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md) note turns the Pantheon MCP/Homh announcements into a focused engineering checklist: authorization, tenant/resource scoping, consent, idempotency, injection resistance, auditability, and authoritative outcome verification.

## 6. Still to watch (replays and transcripts)

The live blog now includes additional partner coverage and a public recap of the "Charging
Ahead with AI and Max" breakout (section 2e), but that is not the same as a full session
transcript. The following remain useful verification targets as of October 10:

- **Charging Ahead with AI and Max**, Oct 7, 11:15 am ET: a live-blog recap is public as of
  October 10 (section 2e); verify the full recording when it becomes available. ServiceTitan
  says breakout recordings go to Academy about 4–6 weeks after the event [6].
- **All-Star Titans** (closing session), Oct 7, 2 pm ET: look for a public replay or recap.
- Full transcripts of the Oct 6 keynotes, to check the live blog's summaries (section 2a)
  against the speakers' actual words.

When replays or transcripts appear, extract only new **publicly verifiable** claims about voice,
bookability, Homh, Adaptive Capacity for AI CSRs, partner integrations, or coordination. Attribute
company and partner claims, distinguish inference from fact, and update this brief and the
[claims ledger](whitepaper/claims-ledger.md).

## Related repo material

- [Call facts contract](call-facts-contract.md) — teaching schema for shared context from a call
- [Homh and AI-agent booking](homh-and-agent-booking.md) — trust surfaces when an AI assistant is in the booking path
- [MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md) — authorization and control boundaries for external AI agents
- [Bookability judge](../senior-engineer/bookability-judge.md) — judgment exercise on gameable booking rates
- [Capacity reservation review](../senior-engineer/capacity-reservation-review.md) — concurrent actions, idempotency, hold lifecycle, and source-of-truth checks
- Whitepaper [chapter 01](whitepaper/01-company.md) (company), [chapter 06](whitepaper/06-product-landscape.md) (products), [chapter 13](whitepaper/13-future-directions.md) (future directions)
- [Tools and guardrails](tools-and-guardrails.md), [Evaluating voice agents](evaluating-voice-agents.md)
- Lessons: denominator, claims vs. state, worth-it
- Labs 09–14 (teaching models of the general patterns): shared context ledger, coordination and
  arbitration, the learning loop, agent-to-agent booking, the call-facts capstone and earning
  autonomy

## Sources

1. ServiceTitan press release, "ServiceTitan Announcing New and Expanded Capabilities at Pantheon 2026" (October 6, 2026): <https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html>
2. Investing.com, "ServiceTitan at Pantheon 2026: ai push aims to make trades self-running" (summary and full keynote transcript, October 6, 2026): <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
3. ServiceTitan, "Pantheon 2026: Live coverage from ServiceTitan" (live blog, reviewed October 10, 2026; publication date October 6, 2026): <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
4. ServiceTitan Help Center, "Assign Atlas personas and manage access" (updated September 28, 2026): <https://help.servicetitan.com/docs/assign-atlas-access-and-personas>
5. ServiceTitan Help Center, "Use Atlas in Adaptive Capacity Strategic Rules" (updated October 8, 2026): <https://help.servicetitan.com/commercial/docs/use-atlas-in-adaptive-capacity-strategic-rules-1>
6. ServiceTitan Help Center, "How can I access Pantheon slides and video recordings?" (updated April 9, 2026): <https://help.servicetitan.com/docs/how-can-i-access-pantheon-slides-and-video-recordings>
