# 07 - AI Voice Agents In The Trades

**Estimated reading time:** 7 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. ServiceTitan's Virtual Agents handle **overflow and after-hours** calls to book,
   reschedule and confirm appointments, using platform data and the contractor's business
   rules. [1][2]
2. The job is transactional: book the right job type, at the right location, with the right
   skills, into real capacity, and escalate to a live CSR when a call falls outside the
   rules. [2]
3. The category is competitive and well funded. Independent vendors such as Avoca sell AI
   voice agents to the same contractors, often integrating with ServiceTitan itself. [3][4]
4. Published results are customer testimonials (for example, a quoted 80–85% booking rate),
   not benchmarks. [2]
5. Analysis: success is measured in committed state (a correct job in the schedule) and
   in revenue captured, not in conversation quality alone.

## What the product does

The 10-K describes Virtual Agents as AI that, combined with the platform's underlying
functionality, automatically handles overflow and after-hours calls to book, reschedule
and confirm appointments, helping customers capture revenue they might otherwise lose. [1]

The product page adds detail. [2] Listed capabilities include:

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

Analysis: overflow and after-hours are natural starting points because the alternative is
often voicemail or an answering service, so the baseline is low and the value is easy to
see. They are also the hardest moments: peaks and nights.

## The competitive and market context

Independent AI voice companies target the same contractors. Avoca, for example, describes
its product as AI agents that answer calls and book jobs for HVAC, plumbing, electrical and
roofing businesses, and markets integration with contractor systems. [3] In April 2026
Kleiner Perkins, an investor, described Avoca as building an AI workforce for service
businesses starting with voice, and Fortune reported it as a roughly $1 billion startup. [4][5]
Its founders' framing is instructive: a missed restaurant call loses a small order, while a
missed home-services call can lose a five-figure HVAC installation. [5]

Analysis: ServiceTitan's structural advantage is being the system of record (capacity,
customer history, memberships, pricebook). A third-party agent has to reach that data
through integrations. The flip side is that point-solution vendors can move quickly and
serve contractors on multiple software platforms.

## Evidence and how to read it

The product page quotes a customer saying the agent's booking rate runs 80–85% with average
talk time under five minutes. [2] Treat that as a single customer's experience: the
denominator (all calls? bookable calls?), period and comparison group are not given.
Chapter 11 covers how to measure impact properly.

## Evaluation design

Score both the conversation and the resulting state:

- **Outcome correctness:** right customer, job type, location, slot, technician skills;
  no duplicate or phantom bookings.
- **Escalation correctness:** transferred when rules or judgment require it, and not
  otherwise.
- **Claim grounding:** never says "you're booked" unless the booking committed.
- **Safety:** emergencies (gas, CO, electrical, flooding) handled with safety instructions
  and immediate escalation.
- **Slices:** trade, new vs. existing customer, after-hours vs. overflow, residential vs.
  commercial, weather-peak days.

The labs in this repo (02 and 07) implement fictional versions of these checks.

## Questions to validate after joining

- What share of calls reach the agent in each mode, and what are the escalation reasons?
- How are bookings audited, and who reviews transcripts?
- Which competitor integrations do shared customers use alongside ServiceTitan?

## Sources

1. ServiceTitan Form 10-K, fiscal 2026 (Business section, Virtual Agents): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
2. ServiceTitan, AI Virtual Agent product page: <https://www.servicetitan.com/features/pro/virtual-agent>
3. Avoca website: <https://www.avoca.ai/>
4. Kleiner Perkins, "Avoca: Bringing AI to the backbone of the real economy" (April 27, 2026): <https://www.kleinerperkins.com/perspectives/avoca-bringing-ai-to-the-backbone-of-the-real-economy/>
5. Fortune, Term Sheet on Avoca (April 27, 2026): <https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/>
