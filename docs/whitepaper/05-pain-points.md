# 05 - Pain Points

**Estimated reading time:** 8 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. Contractors' core problem is converting demand into profitable, well-matched work with
   scarce people: technicians, CSRs and dispatchers.
2. The phone sits at the center: missed, abandoned and badly handled calls are lost revenue,
   and ServiceTitan builds products specifically to recover them. [1]
3. Skilled labor is structurally short: BLS projects tens of thousands of openings a year in
   HVAC and plumbing, mostly to replace workers who leave. [2][3]
4. Demand is volatile (season and weather), and many businesses still run on fragmented or
   rudimentary tools. [1]
5. Analysis: the best AI products relieve a *scarce resource* (CSR time, technician time,
   owner attention) without creating new work, like cleaning up bad bookings.

## The pain-point map

| Pain | Who feels it | Evidence | How it's handled today | Where AI helps (and doesn't) |
|---|---|---|---|---|
| **Missed and abandoned calls** | Owner, CSRs | ServiceTitan built Virtual Agents and Second Chance Leads to capture revenue that would otherwise be lost [1] | Overflow routing, voicemail, answering services | Booking overflow/after-hours calls; flagging unbooked calls. Doesn't fix bad capacity data |
| **After-hours coverage** | Owner, on-call staff | Virtual Agents target after-hours calls [1] | On-call rotations, answering services | Always-on booking and triage; emergencies still need humans |
| **Technician shortage** | Owner, dispatcher | BLS: ~40,100 HVAC and ~44,000 plumbing openings/yr through 2034, mostly replacement [2][3] | Hiring, training, overtime | Better matching (Dispatch Pro weighs skills, location, drive time, predicted value) [4]; can't create technicians |
| **Demand volatility** | Everyone | 10-K: summer and extreme weather drive demand [1] | Overtime, turning work away | Elastic phone capacity on peak days |
| **CSR turnover and training** | Call-center manager | General industry pain; no neutral statistic found | Scripts, shadowing, call review | Consistent handling; coaching from transcripts. Agents also need "training" (evals) |
| **Scheduling and capacity mismatch** | Dispatcher, CSR | Scheduling rules for job types, zones and capacity [5] | Manual juggling | Capacity-aware booking; risk of confidently wrong bookings |
| **Marketing waste** | Owner, marketing | Marketing Pro measures ads and connects to bookings [1] | Guesswork on which ads work | Attribution from call to job to invoice |
| **Fragmented tools** | Owner, office | 10-K: many trades businesses rely on rudimentary workflows [1] | Spreadsheets, paper, point tools | Integrated data makes agents possible; fragmented data makes them brittle |
| **Cash flow** | Owner, office | FinTech payments and financing offerings [1] | Paper invoices, late collection | Faster invoicing and payment; agents should stay out of card handling (chapter 10) |

## Missed calls: why this is the headline pain

The phone is where marketing spend turns into revenue. Analysis: a caller who reaches
voicemail can simply call the next contractor on the list. The 10-K describes Virtual Agents handling
overflow and after-hours calls, and Second Chance Leads using AI to find unbooked
interactions worth retrying, both framed as capturing revenue that may otherwise be lost. [1]
An AI-voice vendor's founders make the same point more vividly, contrasting a small missed
restaurant order with a missed HVAC installation worth tens of thousands of dollars. [6]
That's the high end: many calls are small service tickets, existing-customer questions or
not bookable at all. The economic case is real but must be measured on bookable calls
(chapter 11).

## Labor: the constraint behind everything

BLS projects HVAC employment to grow 8% from 2024 to 2034, with about 40,100 openings a
year, and plumbing 4% with about 44,000 openings a year; in both, most openings replace
workers who retire or leave. [2][3] Training takes years (apprenticeships or programs plus
on-the-job learning), and most states license plumbers. [2][3] Analysis: when technician
hours are the bottleneck, booking *more* jobs is worth less than booking the *right* jobs
into the right slots. A voice agent that optimizes booking rate alone can hurt.

## What we couldn't establish from public sources

Neutral, industry-wide figures for call mix, missed-call rates, CSR turnover and the average
value of a missed call weren't found in public primary sources. Vendor figures exist but are
marketing claims. These are good questions for internal data after joining.

## What this means for a voice-agent engineer

- Tie every agent improvement to a specific pain and a measurable outcome (recovered
  bookings, fewer abandoned calls, CSR hours saved).
- Respect the scarcest resource: technician time. Evaluate booking *quality*, not just count.
- Expect peak days to stress everything at once; test there.

## Questions to validate after joining

- Which pain do customers cite most when they buy Virtual Agents?
- What is the real distribution of call types and job values reaching the agent?
- Where do agent bookings create downstream work (reschedules, cancellations, callbacks)?

## Sources

1. ServiceTitan Form 10-K, fiscal 2026: <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
2. BLS, HVAC mechanics and installers: <https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm>
3. BLS, plumbers, pipefitters and steamfitters: <https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm>
4. ServiceTitan, Dispatch Pro: <https://www.servicetitan.com/features/pro/dispatch>
5. ServiceTitan, Scheduling Pro: <https://www.servicetitan.com/features/pro/scheduling>
6. Fortune, Term Sheet on Avoca (April 27, 2026): <https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/>
