# 07 - AI Voice Agents In The Trades

**Estimated reading time:** 9 minutes · **Facts as of:** October 7, 2026

## Five Takeaways

1. ServiceTitan's Virtual Agents handle overflow and after-hours calls to book, reschedule and confirm appointments, using platform data and the contractor's rules. [1][2]
2. At Pantheon 2026 the voice agent was presented as one of 30 agents in Max, coordinated through shared context, shared judgment, coordinated action, arbitration and centralized supervision. [7]
3. The CEO placed voice agents at level 2 of a five-level AI maturity model: automating one workflow is the start, not the destination. [7]
4. The company said in-product booking rates are easy to game, so it built a "voice intelligence" agent that reviews every call to judge whether it was a bookable lead. [7]
5. Analysis: success is committed state (a correct job in the schedule), measured against a defensible bookable-call denominator, and handed cleanly to the other agents.

## What the product does

The 10-K describes Virtual Agents as AI that, combined with the platform's underlying
functionality, automatically handles overflow and after-hours calls to book, reschedule
and confirm appointments, helping customers capture revenue they might otherwise lose. [1]

The product page lists capabilities including: [2]

- **Booking with Adaptive Capacity**, according to job type, location, required skills and more
- **Appointment confirmation and rescheduling**
- **Membership greetings** and **recurring services**
- **Job-type selection** and **custom dispatch-fee messaging**
- **Live escalation** to a CSR when a call falls outside defined rules or needs human judgment
- **Transcripts, summaries and AI call classification** for review and audit

The page says the agent uses real-time ServiceTitan data (customer records, addresses, job
types, availability) together with the business's rules. [2]

## Deployment modes

| Mode | When the agent answers | Main risk |
|---|---|---|
| After-hours | Nights, weekends, holidays | Emergencies with no human on shift; next-day capacity rules |
| Overflow | When CSRs are busy or the queue is long | Handoffs mid-peak; inconsistent experience vs. humans |
| Specific call types | Confirmations, reschedules, recurring visits | Identity and ownership checks on existing appointments |
| All calls | Every call, with CSRs on standby for escalations | Escalation quality becomes the whole safety net |

The CEO's Pantheon keynote said the voice agent started with off-hours calls and calls that
arrived while CSRs were busy, that it now "books as well as a good CSR," and that some
customers let it handle 100% of their calls with CSRs standing by for escalations. [7]
These are company-reported claims.

Analysis: overflow and after-hours are natural starting points because the alternative is
often voicemail or an answering service, so the baseline is low and the value is easy to
see. They are also the hardest moments: peaks and nights.

## What Pantheon 2026 changed

ServiceTitan's October 6, 2026 keynotes and announcements reframed the voice agent from a
standalone product into one part of a coordinated system. Full notes are in the
[Pantheon 2026 AI roadmap brief](../pantheon-2026-ai-roadmap.md).

**One agent among 30.** The keynote transcript describes Max as 30 agents across 18 key
business drivers, connected by five capabilities: shared context, shared judgment,
coordinated action, arbitration and centralized supervision. [7] The CEO's motivating
example was a voice agent that recognized a high-value job and booked it, while a dispatch
agent without that context assigned a junior technician. [7] The press release calls Max
"the fully loaded version of ServiceTitan's Agentic Operating System." [6]

**Level 2 of five.** The CEO's maturity model runs from asking AI questions (level 1) to
a system that learns from every decision (level 5). He placed "a voice agent that answers
calls and books appointments" at level 2, automating individual workflows. [7]

**Measuring bookability.** He said the company couldn't rely on booking rates inside
ServiceTitan because they are "very easy to game," and built a voice intelligence agent to
review every call and decide whether it was a bookable lead. [7] Voice intelligence was then
extended to grade and coach human CSRs. [7]

**A new booking channel.** The press release announced Homh, which connects homeowners
"and their AI agents" with ServiceTitan contractors, works with ChatGPT, Gemini and Claude,
and offers confirmed booking directly into ServiceTitan. [6] The company's live blog
describes Homh as an app plugin live on those assistants. [8] Analysis: a plugin inside a
consumer assistant is not a demonstrated agent-to-agent protocol, so authentication,
idempotency and authorization for these bookings are open questions; see
[Homh and AI-agent booking](../homh-and-agent-booking.md).

Analysis for a voice engineer:

- What the agent captures (intent, urgency, constraints, job-value signals) becomes shared
  context for dispatch and lead scoring. The repo's teaching schema is the
  [call facts contract](../call-facts-contract.md); [lab 13](../../labs/13_minimax_capstone.ipynb)
  builds on it.
- A booking becomes one proposal that other agents may arbitrate, so the control plane must
  stay authoritative about what was committed. [Chapter 15](15-agentic-orchestration.md)
  covers coordination and arbitration; [chapter 16](16-shared-skills-and-capabilities.md)
  covers reusable capabilities such as "check capacity" and "book".
- Moving from overflow to all calls is a question of earned autonomy, which
  [lab 14](../../labs/14_earning_autonomy.ipynb) models with promotion and demotion rules.

## The competitive and market context

Independent AI voice companies target the same contractors. Avoca, for example, describes
its product as AI agents that answer calls and book jobs for HVAC, plumbing, electrical and
roofing businesses, and markets integration with contractor systems. [3] In April 2026
Kleiner Perkins, an investor, described Avoca as building an AI workforce for service
businesses starting with voice, and Fortune reported it as a roughly $1 billion startup. [4][5]

Analysis: ServiceTitan's structural advantage is being the system of record (capacity,
customer history, memberships, pricebook). Pantheon's partner announcements cut both ways:
the press release says AI CSRs get access to Adaptive Capacity, the intelligence behind
ServiceTitan's own scheduling, [6] which (analysis) widens the field of agents booking into
the same schedule.

## Evidence and how to read it

- The product page quotes a customer saying the agent's booking rate runs 80–85% with
  average talk time under five minutes. [2]
- ServiceTitan's live blog reports that Davis AC, a Houston customer, credits its virtual
  agent with a 98% booking rate and with answering multiple calls at once in peak season. [8]

Treat both as customer claims: the denominator (all calls? bookable calls?), period and
comparison group are not given. The company's own statement that in-product booking rates
are easy to game [7] is the best reason to ask. Chapter 11 covers how to measure impact.

## Evaluation design

Score both the conversation and the resulting state:

- **Outcome correctness:** right customer, job type, location, slot, technician skills;
  no duplicate or phantom bookings.
- **Bookability:** was the call a real booking opportunity, judged independently of the
  agent's own outcome (the [bookability judge](../../senior-engineer/bookability-judge.md)
  exercise).
- **Escalation correctness:** transferred when rules or judgment require it, and not
  otherwise.
- **Claim grounding:** never says "you're booked" unless the booking committed.
- **Handoff quality:** the facts passed to dispatch are complete and verified.
- **Safety:** emergencies (gas, CO, electrical, flooding) handled with safety instructions
  and immediate escalation.
- **Slices:** trade, new vs. existing customer, after-hours vs. overflow, phone vs.
  AI-assistant channel, weather-peak days.

Labs 02 and 07 implement fictional versions of these checks; labs 09–14 extend them to
shared context, arbitration and earned autonomy.

## Questions to validate after joining

- What share of calls reach the agent in each mode, and what are the escalation reasons?
- How does voice intelligence define a bookable call, and how is that judge evaluated?
- What does the voice agent write into shared context, and who consumes it?
- How are bookings from Homh and partner AI CSRs validated against the same rules?

## Sources

1. ServiceTitan Form 10-K, fiscal 2026 (Business section, Virtual Agents): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
2. ServiceTitan, AI Virtual Agent product page: <https://www.servicetitan.com/features/pro/virtual-agent>
3. Avoca website: <https://www.avoca.ai/>
4. Kleiner Perkins, "Avoca: Bringing AI to the backbone of the real economy" (April 27, 2026): <https://www.kleinerperkins.com/perspectives/avoca-bringing-ai-to-the-backbone-of-the-real-economy/>
5. Fortune, Term Sheet on Avoca (April 27, 2026): <https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/>
6. ServiceTitan press release, "ServiceTitan Announcing New and Expanded Capabilities at Pantheon 2026" (October 6, 2026): <https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html>
7. Investing.com, ServiceTitan at Pantheon 2026, keynote summary and transcript (October 6, 2026): <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
8. ServiceTitan, "Pantheon 2026: Live coverage from ServiceTitan" (live blog, read October 7, 2026): <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
