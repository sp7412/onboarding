# What I Need to Know Before Day 1

Use this as a compact readiness test. Do not aim for encyclopedic knowledge.

| Area | Know | Be able to explain | Be able to build or inspect |
|---|---|---|---|
| Voice architecture | STT/LLM/TTS, speech-to-speech, realtime | latency, accuracy, determinism trade-offs | trace a request end to end |
| Full duplex | VAD, endpointing, barge-in, backchannels | why turn-taking is a systems problem | inspect event/state transitions |
| LiveKit | sessions, workers, rooms, tools | transport vs application responsibilities | run and debug a simple agent |
| Orchestration | model/tool loops, workflows, handoffs | where control-plane logic belongs | follow a tool call to authoritative state |
| State | conversation context vs business state | why context is not the source of truth | identify stale-state and retry hazards |
| Tools | schemas, authorization, idempotency | model intent vs authorized action | design a safe mutation interface |
| Evaluation | datasets, assertions, LLM/human evals, A/B tests | denominator and slice selection | build a failure-driven eval |
| Observability | traces, logs, latency, errors | evidence needed to debug a call | reconstruct a failed interaction |
| Reliability | timeouts, retries, circuit breakers | why retries can duplicate actions | design recovery behavior |
| Safety | escalation, policy gates, claim grounding | hard invariants vs soft quality | prove a forbidden mutation stays blocked |
| Customer outcome | booking, escalation, completion, latency | model metrics vs business outcomes | define a measurable success metric |
| Multi-agent systems | shared context, coordination, arbitration | when agents should delegate | reason about authority and permissions |
