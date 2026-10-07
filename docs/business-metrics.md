# Business Metrics for Voice Agents

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

The engineering objective is not "make the model score higher." It is to improve a contractor's
customer and operating outcomes without increasing safety or operational risk.

This primer uses the economics and metrics framing in [whitepaper chapter 11](whitepaper/11-economics-and-metrics.md)
and public product/roadmap material. Vendor-reported figures remain vendor-reported; numbers
below that are not explicitly sourced are illustrative.

| Metric | Definition / formula | Why it matters | How voice AI can move it | How it can be gamed or misread |
|---|---|---|---|---|
| Booking rate | valid booked jobs / eligible service opportunities | Captures recovered demand | answers missed/after-hours calls and completes booking | rises if the denominator quietly excludes hard calls |
| Missed/abandoned calls | calls that never reach a useful interaction | Lost demand | answer overflow and after-hours traffic | lower abandonment can hide poor call quality |
| After-hours capture | eligible after-hours calls converted to valid jobs | Extends coverage beyond CSR hours | autonomous handling and callback | can improve while daytime quality falls |
| Speed to answer | time from inbound to useful response | Caller experience and abandonment | fast routing/turn detection | fastest response is not useful if the answer is wrong |
| Average ticket | revenue per completed job | Measures job value, not just volume | replacement signals, routing and proposals | higher ticket can come from fewer, riskier jobs |
| Revenue per call | completed revenue / inbound calls | Connects call handling to economics | better conversion and job-value identification | mixes acquisition quality with agent quality |
| Replacement-opportunity identification | replacement signals correctly identified / eligible calls | Important high-value opportunity | structured extraction and downstream lead scoring | can be inflated by labeling every repair a replacement lead |
| Membership conversion | new members / eligible non-member opportunities | Recurring relationship value | recognize eligible calls and present offers | a higher rate can reflect poor eligibility filtering |
| Human handoff rate | transferred calls / handled calls | Measures containment and workload | automation can reduce unnecessary transfers | lower is not always better; emergencies should transfer |
| False-booking rate | invalid/unsafe bookings / autonomous bookings | Direct trust and operational cost | claim guard, policy gates, authoritative state | zero can mean the system simply refuses everything |
| Wasted truck-roll cost | false bookings × average wasted-roll cost | Converts errors into dollars | safer booking and verification | estimate is sensitive to which incidents are counted |
| CSR hours saved | handled minutes that no longer require a CSR | Operating leverage | automate routine work | can hide extra review/rework time |
| Cost per handled minute | AI/telephony/infra cost / handled minutes | Unit economics | efficient routing, model choice, latency control | cheap minutes are useless if outcome quality falls |

## Metric discipline

Every dashboard metric should state:

1. denominator;
2. eligibility rule;
3. time window;
4. important slices;
5. confidence interval or uncertainty where practical;
6. whether it is a business outcome, system capability, or diagnostic.

The most important anti-pattern is a booking-rate numerator without an independent definition
of which calls were genuinely bookable. Public ServiceTitan material explicitly discusses
voice intelligence evaluating calls for bookability; treat that as a company claim, not as a
description of an internal implementation.

## Value bridge

A useful chain is:

**calls → eligible opportunities → valid bookings → completed jobs → revenue → profit**

Voice-agent quality sits inside that chain. It should not be evaluated independently of the
downstream state.

## Related

- [Lab 13](../labs/src/13_minimax_capstone.py)
- [Lab 14](../labs/src/14_earning_autonomy.py)
- [Evaluating voice agents](evaluating-voice-agents.md)
- [Pantheon 2026 AI roadmap](pantheon-2026-ai-roadmap.md)
