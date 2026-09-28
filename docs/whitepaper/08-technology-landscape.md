# 08 - Voice-AI Technology Landscape

**Estimated reading time:** 8 minutes

## Five Takeaways

1. Transport, media processing, model inference, orchestration, authority, and evaluation
   are separate layers.
2. LiveKit documents realtime media, turn detection, tools, handoffs, telephony, and
   agent lifecycle abstractions. [1]
3. LangGraph documents deterministic and agentic steps, persistence, and human-in-the-loop
   orchestration. [2]
4. LangSmith documents offline and online evaluation loops. [3]
5. Technology choice cannot replace workflow policy or evidence-grounded testing.

## Layered Architecture

The canonical architecture document in this repository covers the detailed diagram. This
chapter keeps the boundary explicit: telephony or WebRTC carries media; STT, TTS, or a
realtime model handles speech; an orchestrator manages turns and tools; a policy/service
layer owns business mutations; observability records traces and outcomes.

LiveKit describes agents as realtime participants and includes abstractions for streaming
pipelines, turn detection, interruptions, tools, handoffs, telephony, and deployment. [1]
That is transport and agent-runtime capability. It does not decide whether a job may be
booked.

LangGraph describes mixing deterministic steps with LLM-driven steps and emphasizes
persistence and human oversight. [2] This makes it a useful conceptual fit for workflows
that must pause, resume, or require approval. The graph is still not the source of truth
for schedules or payments.

LangSmith documents datasets, evaluators, experiments, offline tests, online evaluators,
and feedback loops. [3] Those mechanisms support a quality program in which production
failures become regression cases, subject to privacy and retention controls.

## Latency And Reliability

Latency should be budgeted across capture, endpointing, network, model, tool, and speech
generation. A faster response that skips confirmation is not an improvement. Reliability
requires timeout behavior, retry classification, idempotent mutations, and transfer
fallback. Vendor package versions and exact provider mix remain `[unverified]` for any
private deployment.

## Sources

1. LiveKit Agents overview: <https://docs.livekit.io/agents/>
2. LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
3. LangSmith evaluation: <https://docs.langchain.com/langsmith/evaluation>
4. Repository architecture guide: [voice-agent-architecture](../voice-agent-architecture.md)
