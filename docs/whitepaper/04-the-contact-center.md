# 04 - The Contact Center

**Estimated reading time:** 8 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. For most residential contractors the phone is the front door, and the contact center
   (from one office manager to a multi-location team of CSRs) decides how much demand
   becomes booked work.
2. Demand is peaky: summer heat and cold snaps drive surges, exactly when staff are
   stretched. [1]
3. Coverage gaps (overflow, lunch, nights, weekends) are traditionally filled by voicemail,
   answering services or callbacks, which book poorly. ServiceTitan's Virtual Agents target
   precisely these gaps. [1][2]
4. Contact centers are managed by numbers: answer speed, abandonment, call duration, booking
   rate, with call recordings and transcripts for coaching. [1]
5. Analysis: an AI agent joins this operation as a new kind of CSR, so it must be measured,
   reviewed and escalated like one, alongside the humans.

## Who answers the phone

Small contractors often have an owner or office manager answering calls between other work.
Larger ones run dedicated CSR teams, and multi-location operators centralize them. Contact
Center Pro is positioned for this: an omnichannel, multi-location, AI-powered cloud contact
center with a Universal Inbox across channels and businesses. [1][3]

## What calls look like

Typical inbound call types (a general taxonomy; mixes vary widely by trade and business):

| Call type | What the agent must do | Notes |
|---|---|---|
| New service request | Qualify, offer windows, book | The revenue call |
| Emergency | Safety instruction, escalate | Gas, CO, electrical, flooding, no heat in freezing weather |
| Existing appointment | Confirm, reschedule, cancel, "where's my tech?" | Needs identity and ownership checks |
| Membership | Book maintenance visits, answer plan questions | Priority rules for members |
| Estimate or sales follow-up | Route to sales advisor | High value, not for scripts |
| Billing and payments | Route to office | Payment data rules apply (chapter 10) |
| Vendors, spam, wrong numbers | Classify, end politely | Pollutes metrics if counted as bookable |

ServiceTitan's Virtual Agents include AI call classification, and Second Chance Leads flags
unbooked calls worth retrying, both signs that call classification is itself a product
problem. [1][2]

## Peaks, overflow and after-hours

The 10-K says customer demand rises in summer and with extreme weather such as cold spikes.
[1] Analysis: phone traffic follows the same curve, so the hardest hours for staffing are
the most valuable hours for revenue. Contractors cover gaps in a few ways:

- **Overflow routing** to other CSRs or locations
- **Voicemail and callbacks**, which risk losing callers to competitors
- **Answering services**, which usually take messages rather than book into the schedule
- **AI agents**, which can book directly into capacity when integrated with the system of
  record; ServiceTitan's Virtual Agents handle overflow and after-hours calls to book,
  reschedule and confirm. [1]

## How contact centers are managed

Phones Pro routes calls through the platform so the business knows which CSR handled each
call and can report KPIs such as abandonment and average duration; it also provides call
transcripts and automated escalation alerts. [1] Call Booking and Recording shows CSRs the
caller's property details and history as the call starts. [1]

Common management metrics: speed to answer, abandonment, booking rate on bookable calls,
average handle time, escalations, and quality scores from reviewed recordings.

**Staffing analysis.** Contact-center staffing follows queueing math: when arrival rates
spike, a fixed team's wait times rise sharply rather than linearly, so modest surges can
produce large abandonment. That nonlinearity is what makes elastic, AI-based overflow
valuable on peak days.

## Escalation as a feature

The Virtual Agent product page says calls outside defined rules or needing human judgment
can be escalated or transferred to a live CSR. [2] Analysis: good escalation is
**warm** (context passed along: who, where, what, urgency, what was offered and done),
**fast**, and **measured** (escalation reasons are one of the best signals of where the
agent needs work).

## Quality review

Transcripts, summaries and call classification make AI calls reviewable. [2] Analysis: the
same review loop that coaches human CSRs (listen, score, coach) should feed the agent's
evaluation dataset, turning bad calls into regression tests (lab 07).

## Public Evidence

- **Labor constraints upstream.** BLS projects about 40,100 HVAC and 44,000 plumbing
  openings a year through 2034, mostly replacement demand. [4][5] Analysis: office and CSR
  roles compete in the same local labor markets, though BLS data here covers technicians only.
- **Vendor framing of missed calls.** An AI-voice vendor's founders contrast a small missed
  restaurant order with a missed HVAC installation worth tens of thousands of dollars;
  treat that as the high end, not the average. [6]
- **Customer-reported results.** The Virtual Agent page quotes one customer's 80–85% booking
  rate; that is a testimonial, not a benchmark. [2]

## What this means for a voice-agent engineer

- Design for **peak days**: load, latency and graceful fallback when everything spikes at once.
- Make the agent **comparable to human CSRs** on the same metrics and denominators.
- Treat **escalation reasons and call classification** as first-class outputs.

## Questions to validate after joining

- What share of calls reaches the agent as overflow vs. after-hours, and how does it change
  on peak days?
- What does a warm transfer carry today, and what do CSRs wish it carried?
- How are agent calls reviewed, and by whom?

## Sources

1. ServiceTitan Form 10-K, fiscal 2026 (Business; Seasonality): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
2. ServiceTitan, AI Virtual Agent: <https://www.servicetitan.com/features/pro/virtual-agent>
3. ServiceTitan, Contact Center Pro: <https://www.servicetitan.com/features/pro/contact-center>
4. BLS, HVAC mechanics and installers: <https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm>
5. BLS, plumbers, pipefitters and steamfitters: <https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm>
6. Fortune, Term Sheet on Avoca (April 27, 2026): <https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/>
