# GPT-Live-1: Full-Duplex Voice with Delegation

**Facts as of: September 30, 2026 · Last reviewed: September 30, 2026**

What OpenAI's GPT-Live-1 is, how it differs from the Realtime models the labs use, how its
delegation model maps onto this repo's control-plane lessons, and what it means for a phone
booking agent. This is very likely the "GPT Live" a contact at the company suggested studying.
Vendor claims and benchmark numbers below are OpenAI-reported and labeled as such.

## Five Takeaways

1. **Full duplex.** GPT-Live-1 listens and speaks at the same time in one model, so it
   handles interruptions, backchannels ("mm-hmm") and background noise as they happen,
   instead of waiting for strict turns. [1][2]
2. **Delegation is the architecture.** GPT-Live handles the conversation; a separate backend
   model or agent does the reasoning and tool calls. You pick the backend independently. [1][2]
3. **Your application still owns the rules.** OpenAI's own guide says the application checks
   permissions, gets required confirmations, runs functions that touch your systems, and
   saves task progress. That's the control plane from labs 02 and 07. [2]
4. **New API, new pricing.** It uses its own `v1/live/sessions` endpoint (not the Realtime
   endpoint) and costs $0.05 per minute for the voice layer, billed per second, with backend
   model and tool usage billed separately. [3]
5. Analysis: it's the "talker/thinker" pattern from lab 08 as a first-class product. The
   engineering focus shifts from turn-taking plumbing to delegation design, grounding and
   evaluation.

## 1. What it is

OpenAI introduced GPT-Live in ChatGPT and brought GPT-Live-1 to the API on September 10,
2026. [1] The model page describes it as a full-duplex voice model that can listen and speak
simultaneously and delegate reasoning and tool use to a backend agent. [3]

| Detail | Value | Source |
|---|---|---|
| Model ID | `gpt-live-1` | [3] |
| Input / output | Audio and text in; audio and text out (no image or video) | [3] |
| Knowledge cutoff | July 31, 2025 | [3] |
| Endpoint | `v1/live/sessions` only (not Realtime, Responses or Chat Completions) | [3] |
| Pricing | $0.05 per minute of voice session, billed per second; backend usage billed separately | [3] |
| Rate limits | Measured in concurrent sessions: 25 (Tier 1), 50 (Tier 2), 200 (Tier 3); not available on the free tier | [3] |
| Connections | WebRTC (browser), WebSockets (server), SIP (phone calls), plus an optional server-side "sideband" WebSocket to monitor or steer a session | [2] |
| Partner integrations | LiveKit, Twilio, Telnyx, Daily/Pipecat | [2] |
| Voices | A larger set of new voices across accents, dialects and languages; custom voices through sales | [1] |
| Transcripts | Native ASR transcripts and response text, with keyword biasing and improved alphanumeric understanding | [1] |
| Turn detection | Supported natively, though the model isn't turn-based | [1] |

## 2. How it differs from the Realtime models

| | Realtime (`gpt-realtime-2`, `-2.1`) | GPT-Live-1 |
|---|---|---|
| Conversation style | Turn-based: VAD or semantic detection decides when you're done | Full duplex: listens while speaking |
| Reasoning | Inside the voice model (configurable effort) | Delegated to a backend model or agent you choose |
| Tool calls | The voice model emits function calls | The backend runs tools; GPT-Live talks while it works |
| Pricing | Per token, with audio tokens priced higher | Per minute for voice, plus backend usage |
| Endpoint | `v1/realtime` | `v1/live/sessions` |

OpenAI reports that GPT-Live-1 scores 30 percentage points higher than GPT-Realtime-2.1 on
Full Duplex Bench, and cuts measured turn-taking latency from about 1.41 s to about 0.80 s.
Paired with a GPT-6 Astra backend at medium reasoning effort, it reports 86.2% pass@1 on its
Tau3 voice benchmark, vs 45.7% for GPT-Realtime-2.1. [1] These are vendor benchmarks run by
OpenAI; verify on your own calls before relying on them.

The labs in this repo still use the Realtime protocol (`gpt-realtime-2`), which remains the
right way to learn turn-taking, events, truncation and tool calls from first principles.

## 3. Delegation: the core idea

GPT-Live has two parts: the live model handles the conversation and decides when to ask for
help, and the backend handles delegated tasks. [2] Give GPT-Live a short prompt about style
and when to delegate; keep detailed instructions, business rules and tool workflows in the
backend. [2][4]

**Two delegation modes** (chosen when you create the session; changing modes means a new
session): [5]

- **Responses delegation:** OpenAI calls the Responses model you configure, supplies
  conversation context, and returns results to the conversation. Your application still runs
  your own function tools.
- **Client delegation:** your application prepares the context, runs any model, agent or
  workflow, and sends results back. Choose this when you need to validate, redact, combine or
  discard results before GPT-Live hears them, or need custom routing, fallbacks and budgets.
  The delegation event carries metadata, not task text, so your app must keep its own
  conversation context from transcript events.

**Three ways to send information back to the live model** (each up to 500 tokens): [5]

| Event | What GPT-Live does with it | Booking-call example |
|---|---|---|
| `session.instructions.append` | Treats it as system-level direction; can interrupt current speech | "Possible gas emergency: give the safety instruction and transfer now." |
| `session.thinking.append` | Keeps it for reasoning; doesn't say it on arrival | "Checking Thursday availability. No appointment has been booked." |
| `session.commentary.append` | Says it aloud, paraphrased | "Booked for Thursday 8–10 with Kara, job J-123." (only after the backend committed it) |

Backend work can keep running when the caller interrupts; your application decides whether
to finish or cancel it. [2] GPT-Live can keep speaking while your app reviews a result, and
playback controls exist if your app must control when the caller hears audio. [5]

## 4. What this means for a trades booking agent

Analysis, mapping GPT-Live onto this repo's lessons:

- **Use client delegation for anything that changes state.** Booking, rescheduling and
  cancelling should go through your control plane (identity, ownership, offered and chosen
  slot, address confirmation, same-day rules, idempotency), exactly as `stlab/tools.py`
  enforces. Only verified results should reach `commentary.append`.
- **Claim grounding gets easier and more important.** Because GPT-Live speaks whatever you
  send as commentary, never append "you're booked" until the backend has committed. Use
  `thinking.append` for progress. That's lab 07's claim guard, moved upstream.
- **Interrupt-safe writes.** The caller may interrupt while a booking is in flight. The write
  must be idempotent, and the app must decide whether to finish or cancel, then tell GPT-Live
  what actually happened.
- **Emergency guardrails via instructions.** A transcript-watching sideband can append an
  instruction to redirect the conversation, but OpenAI notes this steers the live model and
  doesn't cancel backend work. [5] Block the related actions in application state too.
- **Cost model.** Analysis: at $0.05 per minute, a 4-minute call costs about $0.20 for the
  voice layer, plus backend model and tool usage. Per-minute pricing maps cleanly onto
  contact-center economics (cost per call vs. value of a booked job, whitepaper chapter 11).
- **Peak-day capacity.** Rate limits are concurrent sessions per usage tier, so weather-driven
  call spikes (whitepaper chapter 02) need capacity planning and overflow to humans.
- **Telephony fit.** SIP support and LiveKit/Twilio/Telnyx integrations mean it can slot into
  existing phone stacks, the transport layer from labs 03–04.
- **Evaluation is still yours.** OpenAI's own guidance is to compare latency, task success and
  cost on your own workload. [5] Lab 07's scenarios and evaluators are the starting point.

## 5. Prompting, briefly

OpenAI's prompting guide recommends a short conversation prompt for GPT-Live with three
named sections: a backchannel policy, an interruption policy and a delegation policy (when to
delegate and when not to), and putting procedures and tools in the backend. It also says the
application checks permissions and required confirmations before executing actions. [4]

## Questions to validate after joining

- Is the team evaluating or using GPT-Live, Realtime, a cascaded pipeline, or a mix?
- If GPT-Live: Responses or client delegation, and where is the control plane enforced?
- How do commentary updates get verified before they're spoken?
- What concurrency tier and overflow plan cover peak call days?

## Related repo material

- [Speech-to-speech models](speech-to-speech-models.md): Realtime lineup and speech-to-speech vs. cascaded
- [Voice-agent architecture](voice-agent-architecture.md) and whitepaper [chapter 08](whitepaper/08-technology-landscape.md)
- Labs 02 (control plane), 07 (claim guard and evals), 08 (talker/thinker and latency)

## Sources

1. OpenAI, "Build more natural voice experiences with GPT-Live-1 in the API" (September 10, 2026): <https://openai.com/index/introducing-gpt-live-1-in-the-api/>
2. OpenAI, Getting started with GPT-Live: <https://developers.openai.com/api/docs/guides/live>
3. OpenAI, GPT-Live 1 model page: <https://developers.openai.com/api/docs/models/gpt-live-1>
4. OpenAI, Prompting GPT-Live: <https://developers.openai.com/api/docs/guides/live-prompting>
5. OpenAI, Delegation and tools in GPT-Live: <https://developers.openai.com/api/docs/guides/live-delegation>
6. OpenAI, Managing GPT-Live sessions: <https://developers.openai.com/api/docs/guides/live-conversations>
7. OpenAI, Migrate to GPT-Live: <https://developers.openai.com/api/docs/guides/live-migration>
8. OpenAI, GPT-Live partner integrations: <https://developers.openai.com/api/docs/guides/live-partner-integrations>
