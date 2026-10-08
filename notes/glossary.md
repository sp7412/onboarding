# Trades + Contact-Center Glossary (public-safe)

These are general industry terms and fictional examples, not definitions of any
private system. Product names are linked in [`docs/servicetitan-101.md`](../docs/servicetitan-101.md).

| Term | Meaning |
|---|---|
| CSR | Customer service representative who answers calls and books jobs |
| Dispatch board | Schedule view assigning technicians to jobs |
| Capacity | How many jobs of a type the business can take in a time window, set by technician availability, skills, and operational slots |
| Membership / service agreement | Recurring maintenance plan with perks (priority scheduling, discounts) |
| Job type | Category of work (e.g., AC repair, water heater service) that sets skills and duration |
| Estimate | Priced proposal a technician presents in the home |
| Booking rate | Share of calls/leads that become booked jobs |
| Containment | Share of calls fully handled by the AI agent without a human |
| Escalation | Handing a call to a human CSR |
| Atlas | ServiceTitan's AI assistant (public product) |
| Contact Center Pro | ServiceTitan's contact-center product, including AI Voice Agents (public product) |
| A2P 10DLC | Application-to-person texting over standard 10-digit US numbers. Carriers and messaging providers generally require the sending business to register its brand and messaging campaigns; exact requirements and exceptions depend on the provider and carrier |
| Agent handoff | Transfer of a conversation from one automated or human role to another with useful context |
| Appointment window | A range of time offered for a technician visit, such as 10:00–12:00 |
| Backchannel | A short listener signal such as "uh-huh" that usually should not interrupt the agent |
| Full duplex | A voice model that listens and speaks at the same time (e.g. OpenAI GPT-Live-1), so interruptions and backchannels are handled as they happen rather than turn by turn |
| Delegation (voice) | A voice model handing reasoning and tool calls to a separate backend model or agent while it keeps talking; GPT-Live-1 supports Responses and client delegation |
| Barge-in | The caller speaking while the agent is speaking, causing the agent to yield or stop |
| Baseline | The measured value of a metric before a change, over an agreed period and population. Every before/after claim in this repo requires one (see the playbook and design-doc template) |
| Booked job | A scheduled work commitment created after required confirmations and policy checks |
| Call disposition | The final categorized outcome of a call, such as booked, transferred, or no booking |
| Caller ID | Telephony metadata that may help identify a caller; it is not proof of authorization by itself |
| Cancellation | Removing a scheduled appointment under the contractor's policy |
| Callback | A later return call when the current interaction cannot be completed safely or promptly |
| Canary rollout | Releasing a change to a small cohort or flagged slice of traffic first, with a rollback trigger and owner agreed before launch |
| CCPA | California Consumer Privacy Act: state privacy law granting consumers rights over personal data, relevant to call recordings, transcripts, and retention policies |
| Cascaded pipeline | A voice architecture that chains separate models — speech-to-text → LLM → text-to-speech. Each stage is easy to inspect and constrain, at the cost of extra latency and handoff points compared with speech-to-speech |
| Commercial contractor | A trades business serving commercial properties or facilities; workflows may differ from residential work |
| Customer lifetime value | A business estimate of value over a customer's relationship; not a call-level quality metric |
| Denominator | The population a rate is measured against, such as booking rate per *bookable* call. Instrumenting it honestly is what separates a useful metric from a flattering one |
| Dispatch | Assigning and coordinating jobs for technicians in the field |
| Dispatcher | Person or process coordinating field technicians and job timing |
| DTMF | Touch-tone digits sent over a phone call, often used for menus or verification |
| Emergency escalation | Routing a potentially dangerous situation to a human or emergency process instead of routine booking |
| Endpointing | Deciding that a caller's spoken turn is complete after speech and silence cues |
| Field service management | Software and processes for scheduling, dispatching, and completing work in the field |
| Flat-rate pricing | Pricing a defined service rather than billing only by time and materials |
| Furnace repair | Fictional job type in the labs representing heating-system service |
| Gross dollar retention (GDR) | Revenue retained from an existing customer cohort before upsells and churn; ServiceTitan reported over 95% in fiscal 2024–2026 |
| GTV (gross transaction volume) | The total dollars customers invoice their own end customers through a platform; ServiceTitan reports it in public filings as a core business metric and proxy for customer revenue |
| HVAC | Heating, ventilation, and air conditioning |
| Inbound lead | A new service opportunity arriving through a call, form, message, or other channel |
| Idempotency key | An application-owned key that makes a retried transaction return the same result instead of duplicating it |
| Job | A unit of field work associated with a customer, location, technician, and status |
| Membership | A recurring service agreement that may provide maintenance, priority, or pricing benefits |
| Net dollar retention (NDR) | Revenue from an existing customer cohort this period versus last, including upsells and churn; above 100% means the cohort grows without new customers |
| No-show | An appointment where the customer or technician does not arrive as expected |
| OOD / out of distribution | A request outside the supported intents, policies, or training/evaluation coverage |
| Pass^k | Reliability metric from the τ-bench paper: whether an agent completes a task k times in a row, not just once. Measures consistency across repeated trials |
| Preemptive generation | Starting response preparation before endpointing is fully certain, trading latency for risk |
| Preventive maintenance | Planned service intended to reduce failures, often recurring or seasonal |
| PSTN | Public switched telephone network used for traditional phone calls |
| Recall | A return visit or follow-up related to a previous job or unresolved issue |
| Reschedule | Moving an existing appointment rather than creating a second appointment |
| Routing | Selecting a destination, queue, agent, workflow, or technician based on policy and context |
| Semantic turn detection | Predicting whether a caller's turn is complete from transcript context (a small transformer layered on VAD), so slowly spoken numbers and addresses are not cut off |
| Service area | Geographic region or ZIP-code set a contractor serves |
| Service agreement | Another term for a recurring maintenance or membership plan |
| Service call | A visit or job request to diagnose, repair, install, or maintain equipment |
| Share of wallet | The fraction of a customer's total transaction volume that flows through one vendor; estimated publicly as platform revenue ÷ GTV (analysis, not a company-reported ratio) |
| Slot | A specific available appointment window and technician assignment |
| Speech-to-speech | A realtime model that maps audio directly to audio — one model handles listening, understanding, and speaking — instead of a cascaded pipeline |
| System of record | The authoritative store for a fact (customer, appointment, job, payment). The agent and its tools read from and write through it; they never become it |
| TCPA | Telephone Consumer Protection Act: US law restricting automated and artificial-voice calls and texts. The FCC ruled in 2024 that AI-generated voices count as "artificial" (FCC 24-17) |
| Technician | Field worker who diagnoses, estimates, repairs, installs, or maintains equipment |
| Tenant isolation | Keeping one contractor's data, permissions, and operations separate from another's |
| Time to first audio | Elapsed time from a committed turn to the first audible output — a major component of perceived dead air. The audio analogue of time-to-first-token |
| Transfer | Connecting a caller to a human or another workflow, ideally with reason and context |
| Turn detection | Combining speech activity and semantic cues to decide when a caller has finished speaking |
| VAD | Voice activity detection: detecting whether audio currently contains speech |
| Warm transfer | A handoff where the receiving human gets context before or while joining the caller |
| Work order | An operational record describing authorized work to be performed |

## Multi-agent, autonomy and Pantheon 2026 terms

Teaching definitions as this repo's labs 09–14 and docs use them. They describe general
patterns, not any company's internal design.

| Term | Meaning |
|---|---|
| A2A (Agent2Agent) | An open protocol for handing work to another, independently run agent. An agent publishes an Agent Card (skills, endpoint, auth); work is a task with states such as working, input-required and completed. Peers stay opaque. See [whitepaper chapter 15, section 14](../docs/whitepaper/15-agentic-orchestration.md#14-mcp-and-a2a-are-not-orchestration) |
| Agent gateway | The API an outside AI agent books through. It must establish what a phone call gets from people: client identity, scopes, signed and non-replayed requests, idempotent retries and quoted slots (lab 12) |
| Arbitration | Choosing among competing agent proposals for the same resource by expected value net of cost, without ever trading away hard constraints such as consent, emergencies or capacity (lab 10) |
| Bookability | Whether a call was a lead the business could and should have booked. It is the denominator a booking rate needs, and it is easy to game if the same system judges its own calls ([bookability judge](../senior-engineer/bookability-judge.md)) |
| Calibration | How well stated confidence matches observed accuracy: of the calls an extractor marks 0.9 confident, about 90% should be right. Expected calibration error (ECE) summarizes the gap (lab 14) |
| CallFacts | This repo's teaching schema for the structured facts one call produces (intent, job type, urgency, emergency, bookability, sentiment and more), each with a confidence, consumed by other agents ([call facts contract](../docs/call-facts-contract.md), lab 13) |
| Claim guard | A check that the agent's spoken claim ("you're booked") is grounded in committed application state before it is said (labs 07 and 13) |
| Confidence floor | The minimum confidence a fact needs before a downstream decision may use it; below it the system asks a person instead of acting (lab 13) |
| Context ledger | An append-only log of typed facts with provenance and status (proposed → verified → committed, or retracted) that agents share instead of raw transcripts (lab 09) |
| Cost threshold | The probability above which acting has lower expected cost than not acting: wrong-action cost ÷ (wrong-action cost + missed-opportunity cost) (lab 14) |
| Homh | ServiceTitan's consumer demand platform, announced at Pantheon 2026, that makes selected contractors discoverable and bookable from AI assistants (public product; [Homh doc](../docs/homh-and-agent-booking.md)) |
| Max | ServiceTitan's bundle of AI agents, described publicly as the fully loaded version of its agentic operating system (public product; [Pantheon brief](../docs/pantheon-2026-ai-roadmap.md)) |
| MCP (Model Context Protocol) | An open protocol connecting an AI application (host) to servers that offer tools to call, resources to read and prompt templates, over JSON-RPC. It standardizes the connection, not the policy: consent, validation and idempotency stay in your harness. See [whitepaper chapter 15, section 14](../docs/whitepaper/15-agentic-orchestration.md#14-mcp-and-a2a-are-not-orchestration) |
| Mini-Max | Lab 13's small teaching system: one call becomes CallFacts, then bookability, commit, dispatch and a claim guard. Inspired by public descriptions, not a real implementation |
| Pantheon | ServiceTitan's annual customer conference; the 2026 edition is summarized in the [Pantheon brief](../docs/pantheon-2026-ai-roadmap.md) |
| Promotion / demotion | Moving an agent up or down one autonomy level based on evidence gathered at its current level, such as an error-rate upper bound against a target (lab 14) |
| Prompt injection | Text from a caller, document or other agent that tries to change the agent's instructions. Treat it as untrusted data that can never grant permissions |
| PSI (population stability index) | A drift score comparing two category mixes, such as this week's call types against the reference period; above about 0.25 is a large shift (lab 14) |
| SPRT (sequential probability ratio test) | A test that checks the evidence after every observation and stops as soon as it is decisive, often needing fewer samples than a fixed-size test (lab 14) |
| Wilson interval | A confidence interval for a rate that behaves well with small samples and rates near 0 or 1. Lab 14 promotes only when the upper bound on the error rate is below target |
