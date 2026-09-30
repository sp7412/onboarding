# ServiceTitan / LiveKit Study Notes

*Public pre-employment study notes, lightly condensed, kept as the starting point for this repo.
 The hands-on plan is expanded in [`docs/livekit-hands-on.md`](../docs/livekit-hands-on.md).*

## Context

Public research prompted me to look into LiveKit, OpenAI GPT Realtime, LangChain and LangSmith.
The goal is to understand how these technologies fit together in a modern real-time voice AI and
agent architecture.

## Key concepts

**LiveKit = real-time communications infrastructure + agent runtime.** It handles audio streaming,
WebRTC, realtime sessions, turn-taking, interruptions/barge-in, telephony/SIP, realtime data, and
running AI agents as participants in rooms. LiveKit is not the LLM; it provides the realtime
infrastructure around the model.

```text
Customer → LiveKit → GPT Realtime → Agent / Tools / Business Logic → LiveKit → Customer
```

**GPT Realtime = conversational intelligence.** Streaming audio, speech-to-speech, conversational
context, tool calling, low latency, handling interruptions and overlapping speech.

> LiveKit provides the realtime infrastructure; GPT Realtime provides the conversational model.

**LangChain = agent/application orchestration.** Agents, tools, workflows, state, model/tool
selection, multi-step orchestration.

**LangSmith = observability, tracing, debugging, and evaluation.** LLM and tool-call traces,
latency, errors, agent evaluation, test datasets.

> LangChain builds/orchestrates the agent; LangSmith helps you observe and evaluate it.

## Architecture mental model

```text
Customer (voice/phone)
      ↓
LiveKit (realtime voice / SIP)
      ↓
GPT Realtime (conversational AI)
      ↓  tool / agent call
Orchestration (LangChain)
      ↓
Business logic / APIs (scheduling, CRM)

LangSmith across all of it: tracing, evaluation, debugging, metrics
```

**Key question:** where does each component stop, and where does the application's own control
plane, business logic, guardrails, and state management begin?

## Hands-on plan

1. **Quick prototype** with LiveKit Agent Builder: a service-technician scheduling assistant that
   never claims an appointment changed unless the scheduling tool confirms it.
2. **Build it in Python** with the LiveKit CLI and the `agent-starter-python` template.
3. **Add fake ServiceTitan tools:** `get_customer()`, `get_appointments()`,
   `reschedule_appointment()`, `cancel_appointment()`. The interesting flow: "Move my appointment
   to tomorrow afternoon" → look up appointments → business logic → reschedule → confirmation.

## Important principle: model proposes, harness controls

The LLM shouldn't have unrestricted authority over business-critical actions. Separate model
reasoning and tool selection from deterministic business rules, authorization, validation, state,
idempotency, guardrails, error handling, and human handoff. The model can *request*
`reschedule_appointment(...)`; application code decides whether it's permitted.

## Recommended learning order

1. LiveKit + GPT Realtime: realtime audio + LLM = voice agent
2. Python tools: LLM → tool → business logic → result → LLM
3. State and guardrails: model proposes → application validates → tool executes
4. LangChain: where does an orchestration framework actually add value?
5. LangSmith: what the agent did, why, which tools, how long, where it failed, how to evaluate it

## Core study question

How would I build a production-grade, low-latency voice agent where LiveKit handles realtime
communication, GPT Realtime provides conversational intelligence, an orchestration layer manages
tools and workflows, and my own control plane enforces business rules, state, guardrails, and
reliability?
