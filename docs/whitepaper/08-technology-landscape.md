# 08 - Voice-AI Technology Landscape

**Estimated reading time:** 8 minutes · **Facts as of:** September 27, 2026

For the full architecture with diagrams, see
[docs/voice-agent-architecture.md](../voice-agent-architecture.md). This chapter is the
market-level view.

## Five Takeaways

1. A production voice agent is a stack of separable layers: telephony and transport, speech
   (recognition, reasoning, synthesis), orchestration, the business control plane, and
   observability. [1]
2. Two architectures compete: **cascaded** (speech-to-text → LLM → text-to-speech) and
   **speech-to-speech** realtime models. Each trades control against latency and
   naturalness. [1][2]
3. Realtime models have improved fast: OpenAI's gpt-realtime-2 (May 2026) added reasoning
   with configurable effort, spoken preambles during tool calls and parallel tool calls. [3]
4. Turn-taking (when the caller has finished, when they interrupt) is a hard engineering
   problem that frameworks like LiveKit treat explicitly. [4][5]
5. Analysis: models and transport are commoditizing; the lasting differentiation is data,
   integration depth, policy and evaluation, which is where ServiceTitan argues its
   advantage lies. [6]

## The layers

| Layer | Job | Examples of public technology |
|---|---|---|
| Telephony | Connect the phone network (PSTN/SIP) to software; transfers | SIP trunks, VoIP phone systems (e.g. Phones Pro) [6] |
| Realtime transport | Stream audio with low latency; rooms, participants | WebRTC; LiveKit [4] |
| Speech and reasoning | Understand, decide, speak | STT + LLM + TTS pipelines, or realtime speech-to-speech models [2][3] |
| Orchestration | Tools, workflows, state, handoffs | Agent frameworks; LangGraph-style durable workflows [7] |
| Control plane | Identity, policy, validation, idempotent writes, escalation | The application's own code |
| Observability and evals | Traces, metrics, datasets, experiments | LangSmith and similar platforms [8] |

## Cascaded vs. speech-to-speech

- **Cascaded:** each stage can be chosen and inspected; there's a text checkpoint between
  hearing and speaking where you can validate or redact. The cost is extra hops and latency.
- **Speech-to-speech:** one model hears and speaks, so responses are faster and prosody more
  natural, but there's less opportunity to inspect or block output before it's spoken.

The *Voice AI & Voice Agents* primer and OpenAI's voice-agent guidance both walk through this
trade-off. [1][2] Analysis: many production systems mix the two, for example
speech-to-speech for conversation with deterministic checks at tool boundaries, which is the
pattern the labs teach.

## What changed in 2026

OpenAI introduced gpt-realtime-2 in May 2026 with GPT-5-class reasoning, adjustable reasoning
effort, spoken preambles while tools run, parallel tool calls, and better recovery from tool
failures. [3] Analysis: these features target exactly the pain points of phone agents
(silence during lookups, multi-step bookings, flaky backends), but they also move more
decisions into the model, which raises the bar for external guardrails and evaluation.

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

## Sources

1. *Voice AI & Voice Agents: An Illustrated Primer*: <https://voiceaiandvoiceagents.com/>
2. OpenAI, Voice agents guide: <https://developers.openai.com/api/docs/guides/voice-agents>
3. OpenAI, "Advancing voice intelligence with new models in the API" (May 2026): <https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/>
4. LiveKit, Turns overview: <https://docs.livekit.io/agents/logic/turns/>
5. LiveKit, "Using a transformer to improve end of turn detection": <https://livekit.com/blog/using-a-transformer-to-improve-end-of-turn-detection>
6. ServiceTitan Form 10-K, fiscal 2026: <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
7. LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
8. LangSmith evaluation: <https://docs.langchain.com/langsmith/evaluation>
