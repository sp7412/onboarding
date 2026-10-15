# ServiceTitan voice agent: public product evidence

**Evidence reviewed:** October 15, 2026  
**Scope:** public product behavior, rollout notes, and vendor/customer-reported results. This is not an internal architecture specification.

## The product is a workflow participant, not only a phone-answering bot

ServiceTitan describes its AI Virtual Agent as native to the operational platform: it can use customer history and current scheduling/dispatch information to handle calls and book jobs. The public material emphasizes the operational data behind a booking decision, rather than just speech quality. See the [AI Virtual Agent product page](https://www.servicetitan.com/features/pro/virtual-agent) and [April 2026 webinar recap](https://www.servicetitan.com/blog/webinar-recap-ai-virtual-agents-call-booking).

The documented workflows now extend beyond inbound voice:

| Workflow | Publicly documented behavior | Important boundary |
|---|---|---|
| Inbound voice booking | Handles calls, books jobs, reschedules, answers configured questions, recognizes memberships, and can escalate to a live CSR | Eligibility, business-unit configuration, skills, location, job type, and available capacity constrain what can be booked |
| Speed to Lead | When a lead does not respond to an initial text, the workflow can escalate to an AI voice call | This is an outbound follow-up workflow, not simply inbound call answering |
| After-hours technician notification | After the Voice Agent books an eligible standard after-hours job, it can call and text the assigned technician with job details; if the technician does not answer, it retries once | The call is informational. A change to the appointment still goes through the office |
| Parts-arrival follow-up | When a part arrives and the job is tagged—or a configured Dispatch Pro Console rule detects it—the agent texts the customer and can book a return visit using the original job type and duration | Adaptive Capacity must be configured so it can offer valid slots |
| Replies to marketing texts | The SMS agent can respond to replies to specified missed-call, aging-equipment, and recurring-service campaigns and continue toward booking | The message is part of a configured customer workflow; it is not evidence of an unrestricted messaging agent |
| Website booking | Webchat gives website visitors a conversational route to book, configured alongside voice and text agents | Treat channel parity as a product capability, not proof that every channel uses an identical runtime |

Primary sources: [ST-80 residential release notes](https://help.servicetitan.com/release-hub/docs/st-80-residential-service-and-replacement-release-notes), [parts follow-up documentation](https://help.servicetitan.com/release-hub/docs/automatically-follow-up-with-customers-when-parts-arrive-using-the-virtual-agent), and the [ST-80 release hub](https://help.servicetitan.com/release-hub/docs/st-80-release-hub).

### A useful end-to-end trace to imagine

1. A caller reports a failed system after hours.
2. The agent identifies the job type and gathers the required booking facts.
3. Scheduling rules determine whether an appropriate slot is available.
4. The booking is committed to the operational system.
5. The assigned on-call technician receives a call and SMS with job details; one retry is documented if the technician does not answer.
6. If a required part is unavailable, a later parts-arrival trigger can initiate customer outreach and book the return visit.
7. Evaluation should distinguish the conversation, tool proposal, committed booking, technician notification, and completed service outcome.

Steps 1–6 summarize public product examples; step 7 is a recommended observability model, not a claim about ServiceTitan's private trace schema.

## Voice Intelligence: a separate call-analysis and coaching capability

Voice Intelligence should not be conflated with the real-time Virtual Agent. ServiceTitan's [September 23, 2026 help article](https://help.servicetitan.com/release-hub/docs/use-voice-intelligence-in-servicetitan-calls-to-review-every-recorded-call) describes Voice Intelligence with ServiceTitan Max as **Early Access** at publication. It analyzes recorded calls and produces:

- A graded scorecard.
- The purpose of the call.
- Whether the conversation was a genuine booking opportunity.
- Objections raised.
- The call outcome.
- Transcript evidence supporting those assessments.

The product surfaces include **Call Analysis** for individual calls and **Insights** for aggregate trends, including opportunity-versus-loss and performance views. The help article says the evidence-backed analysis is available about 15 minutes after a call ends; this is an analysis turnaround, not a real-time voice-response latency target.

This addresses a major measurement problem: a CSR's post-call disposition can be wrong or missing. Voice Intelligence attempts to classify the conversation itself and flag mismatches between what was said and how the call was recorded. Custom scorecards are also documented in the [Voice Intelligence custom-scorecards release note](https://help.servicetitan.com/release-hub/docs/score-calls-your-way-with-voice-intelligence-custom-scorecards).

**Rollout caveat:** the cited September article says Voice Intelligence with Calls is available in Early Access for ServiceTitan Max. Availability, eligible call sources, and permissions can vary by release and configuration. The release notes specifically caution that when Contact Center Pro and ServiceTitan Core telephony are both enabled, only Contact Center Pro calls are analyzed in the described configuration.

## Published booking and adoption figures

These are vendor-published webinar or customer-story figures, not independent benchmark results.

| Reported result | Source and interpretation |
|---|---|
| **90% booking rate without capacity-related issues; 70% when capacity issues are included** | ServiceTitan's [April 17 webinar recap](https://www.servicetitan.com/blog/webinar-recap-ai-virtual-agents-call-booking). The distinction matters: a caller requesting an unavailable time is not the same failure as the agent mishandling an available booking. The public article does not provide a complete benchmark protocol or independent audit. |
| **500+ jobs in 30 days, reported as 23% of that customer's monthly jobs** | Same webinar recap; an early-adopter example, not a representative population estimate. |
| **More than 1,300 calls in just over three months; over 90% resulting in booked jobs; 72% completed without human intervention** | ServiceTitan's [June 9 Bill Joplin customer announcement](https://www.servicetitan.com/press/bill-joplins-air-conditioning-and-heating-books-over-90-of-calls-with-servicetitan-ai-voice-agent). The company also reported roughly three minutes per call and estimated incremental booked revenue and operating-cost savings. These are customer/vendor-reported outcomes. |

Do not compare these percentages without aligning denominators. In particular, distinguish:

- Calls answered from calls eligible to book.
- Genuine booking opportunities from all conversations.
- Booked appointments from completed jobs and collected revenue.
- Autonomous completions from calls that eventually booked after a human handoff.
- Capacity-related losses from model, policy, or execution failures.

For a practical measurement framework, see [Business Metrics for Voice Agents](business-metrics.md) and [Realtime voice-agent evaluation](realtime-voice-agent-evaluation.md).

## Engineering implications and questions

The public behavior suggests several questions worth validating with the team rather than assuming answers:

1. **Authoritative state:** What response or read-after-write check establishes that a job was actually booked?
2. **Capacity semantics:** How are slot availability, technician skill, geography, job duration, and capacity reserved atomically?
3. **Cross-channel continuity:** What state is shared when a lead moves from SMS to voice, or from voice to a technician notification?
4. **Retry safety:** How are duplicate bookings or duplicate technician notifications prevented after timeouts and retries?
5. **Human boundary:** Which actions can the agent complete, which are informational only, and which require office approval?
6. **Evaluation denominator:** Who determines that a call was genuinely bookable, and how are capacity constraints separated from agent errors?
7. **Evidence and privacy:** What retention and permission controls govern recordings, transcripts, and quoted evidence in call scorecards?
8. **Outcome linkage:** Can evaluation connect call-level decisions to the committed job, technician response, completed service, invoice, and revenue without attributing unrelated effects to the agent?

These are engineering questions derived from public product behavior—not assertions about internal implementation.

## Sources

- [AI Virtual Agent product page](https://www.servicetitan.com/features/pro/virtual-agent)
- [Introducing AI Virtual Agents: Never Miss a Call (April 17, 2026)](https://www.servicetitan.com/blog/webinar-recap-ai-virtual-agents-call-booking)
- [Bill Joplin AI Voice Agent results (June 9, 2026)](https://www.servicetitan.com/press/bill-joplins-air-conditioning-and-heating-books-over-90-of-calls-with-servicetitan-ai-voice-agent)
- [ST-80 residential release notes (September 23, 2026)](https://help.servicetitan.com/release-hub/docs/st-80-residential-service-and-replacement-release-notes)
- [Schedule Parts Follow-Up](https://help.servicetitan.com/release-hub/docs/automatically-follow-up-with-customers-when-parts-arrive-using-the-virtual-agent)
- [Voice Intelligence in ServiceTitan Max (September 23, 2026)](https://help.servicetitan.com/release-hub/docs/use-voice-intelligence-in-servicetitan-calls-to-review-every-recorded-call)
- [Voice Intelligence custom scorecards](https://help.servicetitan.com/release-hub/docs/score-calls-your-way-with-voice-intelligence-custom-scorecards)

## Related onboarding material

- [ServiceTitan Max capability map](max-capability-map.md)
- [Business metrics](business-metrics.md)
- [Voice-agent architecture](voice-agent-architecture.md)
- [Realtime voice-agent evaluation](realtime-voice-agent-evaluation.md)
- [Chapter 17: Running agents in production](whitepaper/17-running-agents-in-production.md)
