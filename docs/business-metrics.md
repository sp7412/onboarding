# Business Metrics for Voice Agents

**Facts as of: October 8, 2026 · Last reviewed: October 8, 2026**

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
| Punctuality (Homh-facing) | on-time arrivals / scheduled visits (public Homh score) | How AI agents and homeowners rank the contractor | correct slot, skill, and travel-aware booking | can rise while booked jobs are low-value or poorly matched |
| Hired rate (Homh-facing) | jobs accepted after the visit / eligible visits (public Homh score) | Conversion after the first meeting | match job type and tech capability on the call | can be hurt by optimistic booking that sends the wrong tech |
| Job quality / satisfaction (Homh-facing) | customer feedback on completed work (public Homh score) | Long-term reputation in agent marketplaces | accurate problem capture and handoff notes | short-term booking gains can trade off against quality scores |

The three Homh-facing rows above are taken from ServiceTitan's Pantheon 2026 live-blog
coverage of the consumer demand platform: punctuality, hired rate, and job quality and
satisfaction. The same coverage says they are becoming part of ServiceTitan reports whether
or not a contractor is on Homh. Treat definitions and denominators as company claims to
validate after joining; see [Homh and AI-agent booking](homh-and-agent-booking.md). [1]

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

## Value calculator

Try the [illustrative value calculator](https://sp7412.github.io/onboarding/value-calculator/) on the site. It estimates the gross profit an agent adds by answering missed after-hours calls for one contractor, net of wasted truck rolls and agent cost, and shows the wrong-booking rate at which it stops paying. Every input is an assumption you set; nothing is stored.

## Value bridge

A useful chain is:

**calls → eligible opportunities → valid bookings → completed jobs → revenue → profit**

Voice-agent quality sits inside that chain. It should not be evaluated independently of the
downstream state. Homh-facing scores sit further downstream: a valid booking that produces a
late arrival or a declined estimate still shows up in punctuality and hired rate.

## Related

- [Lab 13: Mini-Max](../labs/README.md) (section 5 computes these metrics from the synthetic dataset)
- [Lab 14: earning autonomy](../labs/README.md)
- [Senior engineer track: evaluation and denominator design](../senior-engineer/eval-design.md)
- [Evaluating voice agents](evaluating-voice-agents.md)
- [Homh and AI-agent booking](homh-and-agent-booking.md)
- [Pantheon 2026 AI roadmap](pantheon-2026-ai-roadmap.md)

## Sources

1. ServiceTitan, Pantheon 2026 live coverage (Homh scoring dimensions in the Kuzoyan keynote
   summary): <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
