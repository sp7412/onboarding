# What I Need to Know Before Day 1

A compact readiness test. Don't aim for encyclopedic knowledge; aim to be able to follow a
design review on day one and ask good questions in it.

Rate each row **green** (I could explain it to a peer), **amber** (I recognize it but would
need notes), or **red** (new to me). Fix the reds first, using the "Where to learn it" column.

| Area | Know | Be able to explain | Be able to build or inspect | Where to learn it |
|---|---|---|---|---|
| Voice architecture | STT/LLM/TTS, speech-to-speech, full duplex | latency, accuracy and control trade-offs | trace one request end to end | [architecture](../docs/voice-agent-architecture.md), [speech-to-speech](../docs/speech-to-speech-models.md) |
| Turn-taking | VAD, endpointing, barge-in, backchannels | why turn-taking is a systems problem, not a model setting | inspect event and state transitions | lab 03 |
| Delegation | talker/thinker, GPT-Live-1 delegation | what the voice layer may say while the backend works | follow a delegated tool call back to speech | [GPT-Live-1](../docs/gpt-live-1.md), lab 08 |
| LiveKit | sessions, workers, rooms, tools | transport vs. application responsibilities | run and debug a simple agent | [LiveKit hands-on](../docs/livekit-hands-on.md), lab 04 |
| Orchestration | model/tool loops, workflows, handoffs | where control-plane logic belongs | follow a tool call to authoritative state | labs 05–06 |
| State | conversation context vs. business state | why context is not the source of truth | spot stale-state and retry hazards | lab 02, lab 06 |
| Tools | schemas, authorization, idempotency | model intent vs. authorized action | design a safe mutation interface | [tools and guardrails](../docs/tools-and-guardrails.md) |
| Evaluation | datasets, code evaluators, LLM judges, A/B tests | denominators, slices, repeat trials | build a failure-driven eval | [evaluating voice agents](../docs/evaluating-voice-agents.md), lab 07 |
| Observability | traces, spans, logs, latency percentiles | the evidence needed to debug one call | reconstruct a failed interaction | lab 07 |
| Reliability | timeouts, retries, circuit breakers | why retries can duplicate actions | design recovery behavior | lab 02, lab 06 |
| Safety | escalation, policy gates, claim grounding | hard invariants vs. soft quality | prove a forbidden mutation stays blocked | lab 02, [capstone rubric](../docs/capstone-rubric.md) |
| Multi-agent systems | shared context, arbitration, permissions | who may write which fact, and who decides | trace a fact from proposal to commit | labs 09–14 |
| Autonomy | approval modes, graduated trust, the five-level maturity model | what evidence justifies letting an agent act alone | define a promote/demote rule | [Pantheon brief](../docs/pantheon-2026-ai-roadmap.md), lab 11 |
| The business | booking rate, missed calls, average ticket, capacity | model metrics vs. contractor outcomes | define a measurable success metric | [how a contractor works](../docs/how-a-contractor-works.md), [whitepaper ch. 11](../docs/whitepaper/11-economics-and-metrics.md) |

## Self-check

You're ready when you can do these without notes:

- Draw the path of "my AC stopped working" from microphone to a committed booking, and name
  who owns each step.
- Explain why the agent must never say "you're booked" before the backend commits.
- Name two ways a "98% success" metric could be misleading (see [exercise 4](eval-design.md)).
- Explain, using public Pantheon 2026 material, why the voice agent's call facts matter to
  agents other than the voice agent itself.

---

Part of the [senior engineer judgment track](README.md).
