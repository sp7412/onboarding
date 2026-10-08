# 08 - Voice-AI Technology Landscape

**Estimated reading time:** 10 minutes · **Facts as of:** October 7, 2026

For the full architecture with diagrams, see
[docs/voice-agent-architecture.md](../voice-agent-architecture.md). This chapter is the
market-level view. To compare the three architectures below block by block, with latency and
cost, use the site's [architecture explorer](https://sp7412.github.io/onboarding/architecture/).

## Five Takeaways

1. A production voice agent is a stack of separable layers: telephony, transport, speech, orchestration, the business control plane, and observability. [1]
2. Three architectures now compete: cascaded (STT, LLM, TTS), turn-based speech-to-speech, and full-duplex voice with delegation to a backend model. [1][2][9]
3. OpenAI's current lineup includes gpt-realtime-2 (May 2026), gpt-realtime-2.1 and 2.1-mini (July 2026), gpt-live-transcribe (July 2026) and full-duplex gpt-live-1 (September 2026). [3][10][11][9]
4. Turn-taking (when the caller has finished, when they interrupt) is a hard engineering problem that frameworks like LiveKit treat explicitly. [4][5]
5. Analysis: models and transport are commoditizing; lasting differentiation is data, integration depth, policy and evaluation, where ServiceTitan argues its advantage lies. [6]

## The layers

| Layer | Job | Examples of public technology |
|---|---|---|
| Telephony | Connect the phone network (PSTN/SIP) to software; transfers | SIP trunks, VoIP phone systems (e.g. Phones Pro) [6] |
| Realtime transport | Stream audio with low latency; rooms, participants | WebRTC; LiveKit [4] |
| Speech and reasoning | Understand, decide, speak | STT + LLM + TTS pipelines, realtime speech-to-speech models, or full-duplex voice with a backend model [2][3][9] |
| Orchestration | Tools, workflows, state, handoffs | Agent frameworks; LangGraph-style durable workflows [7] |
| Control plane | Identity, policy, validation, idempotent writes, escalation | The application's own code |
| Observability and evals | Traces, metrics, datasets, experiments | LangSmith and similar platforms [8] |

## Three architectures

- **Cascaded:** each stage can be chosen and inspected; there's a text checkpoint between
  hearing and speaking where you can validate or redact. The cost is extra hops and latency.
- **Speech-to-speech (turn-based):** one model hears and speaks, so responses are faster and
  prosody more natural, but there's less opportunity to inspect or block output before it's
  spoken. Voice activity detection still decides when the caller's turn ends.
- **Full duplex with delegation:** a voice model listens while it speaks and hands reasoning
  and tool calls to a separate backend model or agent. OpenAI describes GPT-Live-1 this way:
  it can delegate reasoning and tool calls to a backend text model or a third-party model. [9]
  OpenAI's guide says the application still checks permissions, gets required confirmations
  and runs functions that touch your systems. [13]

| | Cascaded | Speech-to-speech | Full duplex + delegation |
|---|---|---|---|
| Who reasons | Text LLM | The voice model | A backend model you choose |
| Text checkpoint before speech | Yes | No | Only for what the app sends back |
| Interruptions | Endpointing and cancel logic | VAD plus cancel and truncate | Handled inside the voice model |
| Pricing shape | Per stage | Per token, audio priced higher | Per minute for voice, backend billed separately |

The *Voice AI & Voice Agents* primer and OpenAI's voice-agent guidance both walk through the
cascaded vs. speech-to-speech trade-off. [1][2] Analysis: many production systems mix them,
for example speech-to-speech or full duplex for conversation with deterministic checks at
tool boundaries, which is the pattern the labs teach. In a delegation design, those checks
live in the backend that decides what the voice model is told to say.

## The current OpenAI lineup

Vendor-reported facts, checked against OpenAI's pages on October 7, 2026. More detail is in
[speech-to-speech models](../speech-to-speech-models.md) and [GPT-Live-1](../gpt-live-1.md).

| Model | Released | What it is | Price (vendor-reported) |
|---|---|---|---|
| `gpt-realtime-2` | May 2026 | Reasoning speech-to-speech model; minimal to xhigh reasoning effort, spoken preambles, parallel tool calls [3] | $4 / $24 text, $32 / $64 audio per 1M tokens in / out [14] |
| `gpt-realtime-2.1` | July 6, 2026 | Updates gpt-realtime-2 with better alphanumeric recognition, silence and noise handling, and interruption behavior [10][15] | $4 / $24 text, $32 / $64 audio per 1M tokens [15] |
| `gpt-realtime-2.1-mini` | July 6, 2026 | Mini reasoning model for faster, lower-cost voice interactions [10][16] | $0.60 / $2.40 text, $10 / $20 audio per 1M tokens [16] |
| `gpt-live-transcribe` | July 29, 2026 | Low-latency speech-to-text for realtime transcription; no spoken reply [11][17] | $0.017 per minute [17] |
| `gpt-live-1` | September 10, 2026 | Full-duplex voice model with delegation; its own `v1/live/sessions` endpoint [9][12] | $0.05 per minute, billed per second; backend billed separately [12] |

OpenAI says the July release cut p95 latency by at least 25% across Realtime voice models
through improved caching, [10] and that GPT-Live-1 improves Full Duplex Bench performance by
30 percentage points over GPT-Realtime-2.1. [9] Both are vendor-reported. Analysis: these
features target the pain points of phone agents (silence during lookups, multi-step
bookings, interruptions), but they also move more decisions into models, which raises the
bar for external guardrails and evaluation on your own calls.

## Turn-taking and latency

Callers judge an agent by timing: how fast it responds, whether it cuts them off, whether
it stops when interrupted. LiveKit documents endpointing, interruption handling and
turn-detection options, [4] and describes a transformer model that uses the conversation's
words to decide whether the caller has finished speaking, reducing interruptions of callers
who pause mid-sentence (reading a phone number, for instance). [5] Latency accumulates across
endpointing, network, model and synthesis, so it has to be budgeted end to end (lab 08).

## Reliability realities

Phone calls don't pause for outages. Production agents need timeouts, safe retries,
idempotent writes, fallbacks to humans, and graceful behavior when a backend is slow or
wrong. Durable workflow engines help keep multi-step processes consistent across failures. [7]

## What's commoditizing vs. differentiating

**Commoditizing (analysis):** speech recognition and synthesis quality, realtime transport,
generic agent frameworks, and base model capability, all available from multiple vendors.

**Differentiating (analysis):** proprietary data and workflow integration (customer history,
capacity, pricebook), trade-specific policies, evaluation datasets built from real calls, and
reliable escalation. ServiceTitan's 10-K frames its AI advantage in similar terms: large
proprietary data, similar customer profiles with common workflows, and an end-to-end platform
where insights can be acted on. [6]

## Questions to validate after joining

- Which architecture does the production agent use today, and why?
- Where are latency budgets set and measured?
- How are model upgrades (e.g. new realtime versions) evaluated before rollout?
- Has the team evaluated full duplex with delegation, and where would the control plane sit?

## Sources

1. *Voice AI & Voice Agents: An Illustrated Primer*: <https://voiceaiandvoiceagents.com/>
2. OpenAI, Voice agents guide: <https://developers.openai.com/api/docs/guides/voice-agents>
3. OpenAI, "Advancing voice intelligence with new models in the API" (May 7, 2026): <https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/>
4. LiveKit, Turns overview: <https://docs.livekit.io/agents/logic/turns/>
5. LiveKit, "Using a transformer to improve end of turn detection": <https://livekit.com/blog/using-a-transformer-to-improve-end-of-turn-detection>
6. ServiceTitan Form 10-K, fiscal 2026: <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
7. LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
8. LangSmith evaluation: <https://docs.langchain.com/langsmith/evaluation>
9. OpenAI, "Build more natural voice experiences with GPT-Live-1 in the API" (September 10, 2026): <https://openai.com/index/introducing-gpt-live-1-in-the-api/>
10. OpenAI Developer Community, "New Realtime models on the API: gpt-realtime-2.1 and gpt-realtime-2.1-mini" (July 6, 2026): <https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896>
11. OpenAI Developer Community, "GPT-Live-Transcribe and GPT-Transcribe: Two New Transcription Models in the API" (July 29, 2026): <https://community.openai.com/t/gpt-live-transcribe-and-gpt-transcribe-two-new-transcription-models-in-the-api/1388318>
12. OpenAI, GPT-Live 1 model page: <https://developers.openai.com/api/docs/models/gpt-live-1>
13. OpenAI, Getting started with GPT-Live: <https://developers.openai.com/api/docs/guides/live>
14. OpenAI, GPT-Realtime-2 model page: <https://developers.openai.com/api/docs/models/gpt-realtime-2>
15. OpenAI, GPT-Realtime-2.1 model page: <https://developers.openai.com/api/docs/models/gpt-realtime-2.1>
16. OpenAI, GPT-Realtime-2.1 Mini model page: <https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini>
17. OpenAI, GPT-Live-Transcribe model page: <https://developers.openai.com/api/docs/models/gpt-live-transcribe>
