# 11 - Economics And Metrics

**Estimated reading time:** 7 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. ServiceTitan's customers invoiced $82.1 billion through the platform in fiscal 2026,
   averaging roughly $7.6 million per Active Customer (a skewed average). [1]
2. The company earns about 1.2% of that volume (analysis from reported figures) and grows by
   raising this share with add-ons. [1][2]
3. The economic case for a voice agent is recovered revenue: calls that would otherwise go
   unanswered, abandoned or unbooked. Vendors frame one missed call as potentially a
   five-figure installation, but that is the high end, not the average. [3]
4. Booking rate alone is a misleading success metric; job value, capacity use, escalation
   quality and customer experience matter too.
5. Measuring impact needs baselines and counterfactuals, because demand swings with season
   and weather. [1]

## The money flowing through the platform

| Metric | Value | Source |
|---|---|---|
| GTV, fiscal 2026 | $82.1 billion | [1] |
| GTV, fiscal 2025 | $68.5 billion | [1] |
| Active Customers, Jan 31, 2026 | ~10,800 (over $10k annualized billings each) | [1] |
| Revenue, fiscal 2026 | ~$961 million | [4] |
| GTV, fiscal Q2 2027 | $26.8 billion (+17% YoY) | [2] |

Analysis: $82.1 billion ÷ ~10,800 customers ≈ $7.6 million invoiced per customer per year,
and ~$961 million ÷ $82.1 billion ≈ 1.2% share of wallet. Both are back-of-envelope figures
from public numbers; the real distributions are unknown from outside.

## Unit economics of a call (framework)

The value of answering and booking a call depends on four things:

**Value of a call ≈ P(bookable) × P(booked | answered well) × expected job value × margin
− cost of handling the call**

- **P(bookable):** many calls are not new jobs (existing appointments, billing, vendors,
  spam). Classification matters.
- **P(booked | answered well):** conversion when the call is answered promptly and
  handled correctly, compared with voicemail or a slow callback.
- **Expected job value:** ranges from a small service fee to a full system replacement.
  Avoca's founders contrast a missed restaurant order with a missed HVAC installation worth
  tens of thousands of dollars. [3] That is the tail, not the mean; many calls lead to modest
  service tickets.
- **Margin and capacity:** a booked job only has value if a qualified technician can do it
  profitably in the promised window. Booking into overbooked or mismatched capacity can
  destroy value.
- **Handling cost:** CSR labor, answering-service fees, or agent compute and telephony.

Analysis: this is why overflow and after-hours are attractive first deployments: the
counterfactual (voicemail, abandonment, an answering service that only takes messages)
converts poorly, so recovered value is large and easy to argue.

## Metrics for an AI voice agent

| Metric | Definition to agree on | Watch out for |
|---|---|---|
| Booking rate | Booked calls ÷ **bookable** calls | Denominator games (excluding hard calls) |
| Containment | Calls completed without a human | Rewarding the agent for not escalating when it should |
| Escalation correctness | Correct transfers ÷ calls that required one | Hard to label; needs human review |
| Revenue influenced | GTV from jobs booked by the agent | Attribution overlap with marketing and CSRs |
| Job quality | Cancellations, reschedules, callbacks, wrong job type | Lagging; shows up days later |
| Abandonment and speed to answer | Calls abandoned, time to first word | Seasonality and peak-day effects |
| Customer experience | CSAT or complaint rate | Low response rates |
| Claim accuracy | Spoken confirmations that match committed state | Needs transcript + state comparison |

ServiceTitan's Phones Pro already reports human CSR KPIs such as abandonment rate and
average call duration. [5] Analysis: agent metrics should be defined so managers can compare
agent and human performance on the same calls and denominators.

## Measuring impact honestly

- **Seasonality and weather:** demand peaks in summer and during extreme weather. [1]
  Compare like periods or use concurrent controls, not before/after across seasons.
- **Selection:** agents handle overflow and after-hours calls, which differ from daytime
  calls. Compare against the same call types.
- **Experiments:** where possible, randomize which overflow calls go to the agent vs. the
  existing path, or stagger rollouts across locations.
- **Customer-reported results:** testimonials (such as an 80–85% booking rate quoted on the
  product page) are evidence of satisfaction, not causal estimates. [6]
- **Program results:** management reported strong early outcomes from the Max pilot, such as
  higher average tickets. [4] Those come from a selected pilot group and blend many changes,
  so they don't isolate any single product's effect.

## What this means for a voice-agent engineer

- Instrument the **denominator** (bookable calls) as carefully as the numerator.
- Log committed state and downstream outcomes (cancellations, completed jobs, invoices) so
  impact can be tied to GTV, the company's core metric.
- Present wins in contractor terms: recovered jobs and revenue, fewer missed calls, CSR
  hours saved.

## Questions to validate after joining

- What is the official definition of booking rate and containment for Virtual Agents?
- Is there an experiment framework for agent changes, and how are seasonality and weather
  handled?
- How is agent-influenced GTV attributed?

## Sources

1. ServiceTitan Form 10-K, fiscal 2026 (MD&A: GTV, Active Customers; Seasonality): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
2. ServiceTitan fiscal Q2 2027 results: <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm>
3. Fortune, Term Sheet on Avoca (April 27, 2026): <https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/>
4. Yahoo Finance, "ServiceTitan Q4 Earnings Call Highlights": <https://finance.yahoo.com/news/servicetitan-q4-earnings-call-highlights-031828218.html>
5. ServiceTitan Form 10-K, fiscal 2026 (Phones Pro): same as [1]
6. ServiceTitan, AI Virtual Agent product page: <https://www.servicetitan.com/features/pro/virtual-agent>
