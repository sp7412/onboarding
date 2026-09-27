ServiceTitan Onboarding

**Real-Time Voice Agent Study Guide**

LiveKit · OpenAI Realtime · LangChain / LangGraph · LangSmith — Prepared
for Seth Patterson, Senior AI Engineer (start date: October 26, 2026)

Purpose and the core question

This guide turns the follow-up topics from the ServiceTitan
conversations into a structured, pre-start study plan. The goal is not
to memorize four vendor APIs. It is to build a clear mental model of a
production voice agent, so that on day one you can reason about where
latency comes from, where failures surface, and which layer owns which
decision.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>The key study question</strong></p>
<p>Where does each component stop, and where does the application's own
control plane, business logic, guardrails, and state management
begin?</p>
<p>Every section below ends with a “Where it stops” list. Your
deliverable by start date is a one-page answer to this question in your
own words (see Action Items).</p></td>
</tr>
</tbody>
</table>

Working mental model

| **Layer**                  | **Component**                                   | **Owns**                                                                                                           | **Does NOT own**                                                                    |
|----------------------------|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Transport                  | LiveKit (WebRTC + SIP, Agents SDK)              | Media streams, rooms/participants, VAD, turn detection, interruption plumbing, session lifecycle, telephony bridge | What to say, whether an action is allowed, business state                           |
| Conversation intelligence  | OpenAI Realtime (gpt-realtime-2 as of May 2026) | Speech understanding, reasoning, speech generation, deciding when to request a tool call                           | Executing tools, persisting state, enforcing policy, knowing the customer's account |
| Orchestration              | LangChain create_agent / LangGraph              | Multi-step workflows, tool routing, durable graph state, middleware hooks, human-in-the-loop                       | The audio hot path (usually), real-time turn-taking                                 |
| Observability & evaluation | LangSmith                                       | Traces, latency/error visibility, datasets, evaluators, experiments, online monitoring                             | Fixing anything; deciding what “good” means (you define evaluators)                 |
| Control plane (yours)      | ServiceTitan application code                   | Identity, permissions, booking rules, idempotency, guardrails, escalation, compliance, source-of-truth state       | —                                                                                   |

A useful framing: the vendors provide **mechanism** (move audio,
generate speech, run a graph, record a trace). The application provides
**policy** (who this caller is, what they may do, what a valid booking
looks like, when to hand off to a human, what counts as success).

1\. LiveKit — real-time voice transport

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>Role in the stack</strong></p>
<p>LiveKit is the real-time media layer: a WebRTC SFU plus an Agents
framework that joins a room as a participant, receives the caller's
audio, runs the voice pipeline (VAD → turn detection → model → TTS, or a
realtime model), and publishes audio back. It also bridges phone calls
via SIP.</p></td>
</tr>
</tbody>
</table>

Concepts to master

- **Rooms, participants, tracks.** A call is a room; the caller (SIP or
  WebRTC) and the agent are participants; audio flows as
  published/subscribed tracks. Understand how an agent worker is
  dispatched into a room.

- **AgentSession and Agent.** The session owns the pipeline and I/O; the
  Agent owns instructions and tools. Learn agent handoff (one Agent
  transferring control to another, e.g., intake → booking).

- **Pipeline modes.** Cascaded (STT → LLM → TTS) versus realtime
  (speech-to-speech model). Know the trade-offs: control and model
  choice versus latency and prosody.

- **Turn detection.** VAD detects speech presence; endpointing decides
  when a turn is finished. LiveKit's turn-detector model adds a semantic
  end-of-turn signal on top of VAD (it is a small distilled model that
  runs on CPU).

- **Interruptions / barge-in.** Allow/disallow interruptions,
  false-interruption handling (resume speaking if no words were actually
  spoken), and adaptive interruption handling on LiveKit Cloud, which
  separates true barge-ins from backchannels like “uh-huh.”

- **Interruption versus tool calls.** What happens to an in-flight tool
  call when the caller interrupts? When should a tool be
  non-interruptible (e.g., a payment or booking commit)?

- **Telephony.** SIP trunks, inbound dispatch rules, DTMF, call transfer
  (warm/cold) to a human CSR.

- **Latency sources.** Network jitter, codec/buffering, endpointing
  delay (often the single biggest knob), model time-to-first-audio, TTS
  time-to-first-byte.

Where it stops

- LiveKit decides **when** the caller finished speaking and **whether**
  the agent should stop talking. It does not decide **what** the agent
  should do about it.

- It carries the transcript and events; it is not the system of record
  for conversation state or customer data.

- Endpointing and interruption thresholds are tuning parameters, but the
  policy (e.g., “never allow barge-in while reading a legal disclosure”)
  is yours.

- When using a realtime model with server-side turn detection, some
  LiveKit interruption settings are ignored. Know which layer is
  actually making the turn decision in your configuration.

Hands-on lab

- Run the LiveKit Agents voice quickstart (Python) locally against
  LiveKit Cloud's free tier.

- Build it twice: once cascaded, once with the OpenAI Realtime plugin.
  Log end-of-user-speech → first-agent-audio for 20 turns in each mode
  and compare.

- Add a slow tool (sleep 4 s) and observe what happens when you
  interrupt mid-tool. Then make it non-interruptible and compare.

- Tune endpointing delay: have someone read a phone number or address
  slowly and find where the agent starts cutting them off.

Check yourself

- Draw the lifecycle of one inbound phone call from SIP INVITE to
  hang-up, naming every component that touches the audio.

- Explain the difference between VAD, endpointing, and semantic turn
  detection in two sentences each.

- Where would you put a “please hold while I check the schedule” filler,
  and which layer triggers it?

2\. OpenAI Realtime — conversational intelligence

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>Role in the stack</strong></p>
<p>The Realtime API exposes speech-to-speech models over WebRTC,
WebSocket, or SIP. The current flagship (gpt-realtime-2, released May 7,
2026) adds GPT-5-class reasoning with configurable effort, spoken
preambles while tools run, parallel tool calls, and better recovery from
tool failures. Companion models cover streaming transcription
(GPT-Realtime-Whisper) and live translation.</p></td>
</tr>
</tbody>
</table>

Concepts to master

- **Session model.** A session holds instructions, voice, tools,
  turn-detection config, and the conversation item list. Learn
  session.update and how instructions can change mid-call.

- **Event protocol.** Client events (append audio, create response,
  cancel response, truncate item) and server events (speech
  started/stopped, response deltas, function-call arguments, response
  done). This is the real API; SDKs wrap it.

- **Turn detection options.** Server VAD versus semantic VAD versus
  client-controlled turns (create_response off, where your app decides
  when the model replies).

- **Truncation on interruption.** When the caller barges in, the audio
  already played must be reconciled with what the model thinks it said.
  Understand conversation.item.truncate and why transcripts drift if
  this is wrong.

- **Tool calling.** The model emits a function call; your code executes
  it and returns a function_call_output item, then requests a new
  response. The model never touches your systems directly. Also note
  remote MCP support.

- **Reasoning effort versus latency.** Low effort is the default for
  speed; higher effort helps complex workflows but costs
  time-to-first-audio. Consider per-session or per-phase settings.

- **Context management.** Long calls grow the item list; know how to
  trim, summarize, or re-seed context, and the cost of audio tokens
  versus text tokens.

- **Speech-to-speech versus cascaded.** Speech-to-speech gives better
  prosody and latency; cascaded gives you a text checkpoint where you
  can inspect, filter, or redact before anything is spoken.

Where it stops

- The model proposes actions (tool calls); your application disposes.
  Validation, authorization, and execution are outside the model.

- The model has no durable memory. Customer history, open jobs,
  technician availability, and pricing must be fetched via tools or
  injected as context.

- Instructions are a soft guardrail. Hard rules (no price quotes outside
  the price book, no booking without address confirmation) must be
  enforced in code at the tool boundary.

- Speech output cannot be un-said. Anything that must never be spoken
  needs to be prevented upstream (constrained tools, response templates,
  or a cascaded path for sensitive turns).

Hands-on lab

- Connect directly to the Realtime API over WebSocket without a
  framework. Log every server event for one conversation and annotate
  the sequence.

- Implement one tool (check_availability) end to end, including a
  deliberate failure, and observe how the model recovers.

- Compare reasoning effort low versus high on a tricky scenario (caller
  changes their mind about the appointment window mid-sentence) and
  measure time-to-first-audio.

- Interrupt the model mid-sentence and verify the stored transcript
  matches what was actually heard.

Check yourself

- List five responsibilities that belong to the application, not the
  model, in a booking call.

- Why is a tool-level check stronger than an instruction like “never
  book outside business hours”?

- When would you choose a cascaded pipeline over speech-to-speech for a
  ServiceTitan use case?

3\. LangChain / LangGraph — agent and tool orchestration

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>Role in the stack</strong></p>
<p>In LangChain 1.x the core primitive is create_agent: a model plus a
“harness” of prompt, tools, and middleware, running on the LangGraph
runtime. LangGraph is the lower-level framework for explicit, durable,
stateful graphs that mix deterministic steps with agentic ones. For
voice, the key design question is what belongs on the real-time path and
what runs behind it.</p></td>
</tr>
</tbody>
</table>

Concepts to master

- **create_agent.** Model, tools, system prompt, and response format;
  the agent loop of model → tool → model until done.

- **Middleware.** before_model / after_model and wrap hooks for context
  injection, summarization, PII redaction, guardrails, budget limits,
  and dynamic model or tool selection. This is where much of the
  control-plane logic can live cleanly.

- **State and context.** Agent state (messages plus custom fields)
  versus runtime context (per-invocation data like tenant ID and caller
  identity). Keep secrets and identity in context, not in the prompt.

- **LangGraph fundamentals.** Nodes, edges, conditional routing,
  reducers, checkpointers (durable state across turns and restarts),
  interrupts for human-in-the-loop, subgraphs.

- **Deterministic versus agentic.** Encode the business process
  (identify caller → verify address → find slot → confirm → commit) as a
  graph, and let the model handle only the ambiguous parts.

- **Model and tool selection.** Routing cheap/fast models for
  classification and stronger models for planning; limiting the tool set
  per phase to reduce wrong calls.

- **Deep Agents** (built on create_agent) for long-running, background
  work. Likely more relevant to back-office agents than to the live
  call.

Where it stops

- A full agent loop with several model round-trips is usually too slow
  to sit between the caller and the next spoken word. In voice,
  LangChain/LangGraph typically sits **behind** the realtime model: as
  the implementation of tools, as a “thinker” that plans while the
  realtime model keeps talking, or as post-call processing.

- It orchestrates; it does not own the source of truth. Bookings,
  customers, and schedules live in ServiceTitan's systems, and graph
  state is a working copy.

- Middleware can enforce guardrails, but deciding what the guardrails
  are is a product and compliance decision.

Hands-on lab

- Build a create_agent “booking backend” with three tools
  (lookup_customer, find_slots, create_job) and middleware that blocks
  create_job unless address_confirmed is true in state.

- Re-implement the same flow as an explicit LangGraph with a
  checkpointer. Kill the process mid-flow and resume it.

- Expose the graph as a single tool to your LiveKit + Realtime agent
  from Modules 1–2 and measure the added latency.

Check yourself

- When should booking logic be a graph rather than a free-form agent
  loop?

- What goes in agent state versus runtime context versus your database?

- Sketch a “talker/thinker” split: what does each process own, and how
  do they communicate?

4\. LangSmith — tracing, debugging, and evaluation

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>Role in the stack</strong></p>
<p>LangSmith records traces (trees of runs covering model calls, tool
calls, and custom spans), attaches metadata and feedback, and runs
evaluations of an application against datasets, both offline (before
release) and online (on production traffic). It works with LangChain
agents automatically and with any code through the SDK or
OpenTelemetry.</p></td>
</tr>
</tbody>
</table>

Concepts to master

- **Traces and runs.** Run types (llm, tool, chain), parent/child
  nesting, inputs/outputs, token usage, latency, errors. Learn the
  @traceable decorator for non-LangChain code, such as your LiveKit
  event handlers.

- **Metadata and tags.** Tag every trace with call ID, tenant, agent
  version, prompt version, and model so you can slice by release and
  customer.

- **Threads.** Group the many runs of one phone call into a single
  conversation view.

- **Datasets and evaluators.** Build datasets from real (redacted)
  calls; write code evaluators (did the booking have a valid slot?),
  LLM-as-judge evaluators (was the tone appropriate?), and trajectory
  evaluators (right tools in the right order?).

- **Experiments.** Compare prompt/model/graph versions on the same
  dataset before shipping; regression-gate in CI.

- **Online evaluation and monitoring.** Sample production traces for
  automated scoring, dashboards for latency and error rates, alerts, and
  annotation queues for human review.

- **Privacy.** Masking inputs/outputs, handling audio and PII, and data
  retention. This is essential for customer calls.

Where it stops

- LangSmith sees what you instrument. Audio-layer timing (endpointing,
  TTS first byte, network) will not appear unless you emit spans for it,
  so pair it with LiveKit's own metrics and your standard APM.

- Evaluators encode your definition of success. Defining that for
  ServiceTitan's customers is the hard, domain-specific work.

- It observes and scores; it doesn't enforce guardrails at runtime.

Hands-on lab

- Instrument the lab agent end to end: one trace per call, spans for
  turn detection, model response, and each tool, all tagged with a call
  ID.

- Create a 25-example dataset of scripted booking scenarios (happy path,
  reschedule, angry caller, wrong address, out-of-area, request for a
  human).

- Write three evaluators: booking correctness (code), tool trajectory
  (code), and politeness/escalation (LLM judge). Run two prompt versions
  as an experiment and compare.

Check yourself

- Which latency metrics matter for voice, and which of them can
  LangSmith actually see?

- How would you turn a bad production call into a regression test?

- What would you redact before a call transcript ever reaches a trace?

5\. Putting it together — the control plane

The integrated picture: LiveKit carries the call and decides turn
boundaries; the realtime model converses and proposes tool calls; tool
calls land in your application, which may delegate multi-step work to
LangGraph; LangSmith observes the whole path. Surrounding all of it is
the application's control plane. That is where most of the engineering,
and most of the risk, lives.

What the application owns

| **Concern**                | **Examples in a home-services call**                                                                                                             |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Identity & authorization   | Matching caller ID to a customer; tenant (contractor) isolation; what the agent may change on this account                                       |
| Business rules             | Service area, business hours, job types the contractor accepts, pricing and membership rules                                                     |
| Transactional integrity    | Idempotent create_job (no double-booking on retries), hold-then-confirm for slots, compensation on failure                                       |
| Conversation state machine | Which phase the call is in, required fields collected, what has been confirmed aloud                                                             |
| Guardrails                 | Tool-level validation, allowed-tool sets per phase, no commitments outside policy, safety/emergency detection (gas leak → instruct and escalate) |
| Escalation                 | When and how to transfer to a human CSR, with context handed over                                                                                |
| Compliance & privacy       | Recording consent, PII/payment redaction, retention, audit logs                                                                                  |
| Resilience                 | Model or vendor timeouts, fallback voices/models, graceful degradation to “we'll call you back”                                                  |
| Measurement                | Definitions of success (booked, resolved, escalated appropriately), feeding back into evals                                                      |

Latency budget worksheet

Fill this in from your own lab measurements; the right-hand column is a
rough planning target, not a vendor figure.

| **Stage**                                           | **Your measurement** | **Planning target**                       |
|-----------------------------------------------------|----------------------|-------------------------------------------|
| End of caller speech → turn committed (endpointing) |                      | ~200–500 ms                               |
| Turn committed → first model audio (realtime)       |                      | ~300–800 ms                               |
| Tool round-trip (simple lookup)                     |                      | \< 500 ms, else speak a preamble          |
| Multi-step orchestration (LangGraph)                |                      | Off the hot path, or masked with filler   |
| Network + playout buffering                         |                      | ~100–200 ms                               |
| Total: caller stops → agent audible                 |                      | Aim for about 1 s or less on simple turns |

Design tensions to have opinions on

- **Speech-to-speech versus cascaded:** latency and naturalness against
  inspectability and control.

- **Framework versus direct API:** LiveKit/LangChain abstractions speed
  you up, but you must know the raw event protocol to debug them.

- **Agentic versus deterministic:** how much of the booking flow the
  model improvises versus what is a hard-coded state machine.

- **Single agent versus handoffs:** one agent with many tools, or
  specialized agents (triage, booking, billing) with handoffs.

- **Vendor lock-in:** which boundaries you would keep abstract so the
  model or transport can be swapped.

6\. Four-week plan (Sept 28 – Oct 25)

| **Week**    | **Focus**                                    | **Outcome**                                                                      |
|-------------|----------------------------------------------|----------------------------------------------------------------------------------|
| 1 (Sept 28) | LiveKit + raw Realtime API                   | Working voice agent in both modes; annotated event log; latency numbers          |
| 2 (Oct 5)   | Realtime tools + LangChain/LangGraph backend | Booking backend with guarded tools and a checkpointed graph wired in as a tool   |
| 3 (Oct 12)  | LangSmith tracing + evaluation               | End-to-end traces; 25-example dataset; 3 evaluators; one experiment run          |
| 4 (Oct 19)  | Synthesis + ServiceTitan context             | Architecture diagram, one-page control-plane answer, questions list for the team |

7\. Action items

- Set up accounts/keys: LiveKit Cloud (free tier), OpenAI API,
  LangSmith. Keep this personal work separate from any employer data.

- Complete the LiveKit Agents voice quickstart; build cascaded and
  realtime variants.

- Connect to the Realtime API directly over WebSocket; log and annotate
  one full conversation's events.

- Implement check_availability with a forced failure; observe recovery
  and preambles.

- Measure and fill in the latency budget worksheet (20+ turns per mode).

- Build the create_agent booking backend with guard middleware.

- Rebuild it as a LangGraph with a checkpointer; test crash-and-resume.

- Wire the graph into the voice agent as a tool; measure added latency.

- Instrument everything in LangSmith with call-ID threads and version
  tags.

- Build the 25-scenario dataset and three evaluators; run a two-version
  experiment.

- Write the one-page answer: “Where does each component stop, and where
  does the control plane begin?”

- Draw the full architecture diagram (transport, model, orchestration,
  observability, control plane).

- Push the capstone to GitHub as a clean, documented repo.

- Prepare questions for your first weeks (below).

8\. Capstone project

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>HVAC service-booking voice agent</strong></p>
<p>A caller phones a fictional HVAC contractor. The agent identifies
them, gathers the problem, recognizes emergencies, offers real slots
from a mock schedule, confirms the address aloud, books idempotently,
and transfers to a human on request or on failure.</p>
<p>Stack: LiveKit (SIP or browser) → gpt-realtime-2 → tools backed by a
LangGraph booking graph → LangSmith traces, dataset, and evaluators.
Include a README section that answers the key study question explicitly,
with your latency numbers.</p></td>
</tr>
</tbody>
</table>

9\. Questions to bring to the team

1.  Which parts of this stack are in production today, and which are
    being evaluated?

2.  Is the live call path speech-to-speech, cascaded, or both depending
    on the flow?

3.  Where do guardrails live today: prompts, tool validation, a policy
    service, or middleware?

4.  How are calls turned into evaluation datasets, and how is PII
    handled along the way?

5.  What are the current latency and success metrics, and which one is
    the team trying to move?

6.  How does the agent hand off to human CSRs, and what context
    transfers with it?

7.  What does the team's definition of “good enough” look like for
    shipping a new agent behavior?

Primary references

- LiveKit docs: Agents overview, Turns overview, Turn detector, Adaptive
  interruption handling, Telephony/SIP (docs.livekit.io)

- OpenAI: Realtime API guide and reference; “Advancing voice
  intelligence with new models in the API” (May 2026)
  (developers.openai.com, openai.com)

- LangChain docs: create_agent, Middleware, LangGraph concepts, Deep
  Agents (docs.langchain.com)

- LangSmith docs: Observability concepts, Tracing quickstart, Evaluation
  concepts, Online evaluation (docs.langchain.com/langsmith)

Note: model names and features change quickly. Re-check the vendor
changelogs before starting each week.
