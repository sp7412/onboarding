# 02 - The Trades Industry

**Estimated reading time:** 8 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. The trades are large and fragmented. ServiceTitan's IPO prospectus estimates that end
   customers in the U.S. and Canada spend about $1.5 trillion a year on trades services. [1]
2. "The trades" covers many different businesses: HVAC, plumbing, electrical, garage door,
   pest control, landscaping, roofing and more, serving both homes and commercial
   buildings. [1][2]
3. Demand is seasonal and weather-driven. Summer heat raises HVAC demand, and cold snaps
   raise furnace and repair demand; ServiceTitan's own revenue shows the pattern. [3]
4. Skilled labor is the binding constraint. BLS projects about 40,100 HVACR and 44,000
   plumbing openings a year through 2034, mostly to replace retiring or departing
   workers. [4][5]
5. Analysis: when technicians are scarce, every booked job must be the *right* job in the
   *right* slot. That makes a voice agent a capacity-allocation system, not just an
   answering service.

## Size and shape

The prospectus estimates roughly $1.5 trillion of annual end-customer spending on trades
services in the U.S. and Canada, and argues the market has historically been underserved
by technology. [1] Treat this as a company estimate made to support an IPO, not an
independent market study. The 10-K itself cautions that its addressable-market estimates
rely on third-party data and internal assumptions that may prove inaccurate. [3]

The businesses in this market vary widely in size. ServiceTitan's own customers range from
family businesses with a few employees to national enterprises and franchise networks
whose combined businesses invoice over $1 billion a year. [3] The owner is usually the
buyer, even at larger firms. [3]

## Which trades

ServiceTitan's industries page lists the categories it targets across residential and
commercial work, including HVAC, plumbing, electrical, garage door, chimney, roofing,
irrigation, water treatment, septic, painting, pool service, landscaping, lawn care and
pest control. [2] Its acquisitions show how trade-specific the software must be: separate
products serve pest and lawn care (FieldRoutes) and commercial landscaping (Aspire). [1]

Trades differ in ways that matter for a voice agent:

| Dimension | Example contrast | Why it matters for voice |
|---|---|---|
| Urgency | Burst pipe or no heat in winter vs. annual tune-up | Emergency detection, priority booking, safety scripts |
| Ticket size | Service call vs. full system replacement | A missed call can be worth very different amounts |
| Recurrence | Pest control routes and memberships vs. one-off repairs | Rescheduling and recurring-visit calls dominate some trades |
| Customer | Homeowner vs. commercial property manager | Different vocabulary, authority and contracts |
| Skills and licensing | Gas work, electrical, refrigerant handling | Booking must match technician skills and certifications |

## Residential vs. commercial

Residential service is high-volume and consumer-facing: homeowners call when something
breaks, often stressed, and choose quickly. Commercial work involves property managers,
contracts, maintenance agreements and larger projects; ServiceTitan's Convex acquisition
targets contractors serving commercial buildings with property, permit and contact data. [3]
Analysis: most voice-agent booking flows are residential; commercial calls are more likely
to need account lookups, contract rules and a human.

## Seasonality and weather

The 10-K states that customer demand tends to rise in ServiceTitan's fiscal second quarter
(May–July) because summer heat drives trades demand, and that extreme weather such as cold
spikes increases demand for furnace and other home repairs. [3] The company's quarterly GTV
reflects this: fiscal Q2 2027 GTV was $26.8 billion versus $21.7 billion in fiscal Q1. [6][7]
On the fiscal 2026 fourth-quarter call, management attributed part of a GTV slowdown to
unusual weather and one fewer business day. [8]

Analysis: call volume likely spikes on the same days demand does: the first heat wave,
the first freeze. Those are exactly the days human CSRs are overwhelmed, and the days a
voice agent's overflow handling, latency and capacity awareness matter most.

## The labor constraint

BLS projects:

| Occupation | Employment growth 2024–2034 | Openings per year | Median pay (May 2024) | Source |
|---|---|---|---|---|
| HVAC and refrigeration mechanics and installers | +8% (much faster than average) | ~40,100 | $59,810 | [4] |
| Plumbers, pipefitters and steamfitters | +4% (about average) | ~44,000 | $62,970 | [5] |

For both occupations BLS says most openings come from replacing workers who retire or
leave the field, not from growth. [4][5] Both require long training (apprenticeships or
postsecondary programs plus on-the-job learning), and many states require licenses. [4][5]
The 10-K lists labor shortages among industry factors that could hurt demand for its
platform. [3]

Analysis: the scarce resource is technician hours. A voice agent that fills the schedule
with low-value or badly matched jobs can make a contractor worse off, even while "booking
rate" goes up.

## Consolidation, franchises and private equity

The 10-K names industry consolidation among the factors that can affect its business, and
describes large customers that aggregate many locations through franchise networks or
common buying partners. [3] Analyst coverage of ServiceTitan's fiscal 2026 results notes
the company targets private-equity networks that are consolidating trades businesses. [9]
Analysis: consolidated, multi-location operators tend to run centralized contact centers,
which is the audience for multi-location products like Contact Center Pro.

## Memberships and financing

Memberships (service agreements with recurring maintenance visits) and consumer financing
are common revenue tools in residential trades. ServiceTitan's industries page highlights
membership management for HVAC, and its FinTech offering includes third-party consumer
financing. [2][3] Analysis: for voice agents, memberships create predictable outbound and
rescheduling traffic and "member" priority rules; financing is not something an agent
should discuss without explicit, compliant scripts (chapter 10).

## What this means for a voice-agent engineer

- Build evaluation slices by **trade, urgency, residential vs. commercial and season**, not
  one global booking rate.
- Plan for **peak-day load** tied to weather, including graceful overflow to humans.
- Treat **technician capacity and skills** as hard constraints the agent must respect.

## Questions to validate after joining

- Which trades and customer sizes generate the most voice-agent traffic?
- How do call volume and booking behavior change on weather-spike days?
- How do capacity rules (job types, skills, zones, memberships) reach the agent?

## Sources

1. ServiceTitan IPO prospectus (Form 424B4, December 2024): <https://www.sec.gov/Archives/edgar/data/1638826/000119312524277099/d577298d424b4.htm>
2. ServiceTitan industries page: <https://www.servicetitan.com/industries>
3. ServiceTitan Form 10-K, fiscal 2026: <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
4. BLS Occupational Outlook Handbook, HVAC and refrigeration mechanics and installers: <https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm>
5. BLS Occupational Outlook Handbook, plumbers, pipefitters and steamfitters: <https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm>
6. ServiceTitan fiscal Q2 2027 results (September 8, 2026): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm>
7. ServiceTitan fiscal Q1 2027 results (Form 8-K Exhibit 99.1): <https://www.sec.gov/Archives/edgar/data/0001638826/000163882626000044/ttan-ex99_1.htm>
8. Yahoo Finance, "ServiceTitan Q4 Earnings Call Highlights": <https://finance.yahoo.com/news/servicetitan-q4-earnings-call-highlights-031828218.html>
9. Investing.com, "ServiceTitan Q4 FY26 slides": <https://www.investing.com/news/company-news/servicetitan-q4-fy26-slides-21-revenue-growth-path-to-25-margins-93CH-4558725>
