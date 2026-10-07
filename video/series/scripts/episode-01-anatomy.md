# Episode 1 — Anatomy of one call

Target length: 3:35 · Approx. 510 words · Running example: “my AC stopped working.”

## Cold open — 0:00–0:10

Imagine saying, “My AC stopped working,” and hearing a useful answer one second later.
That second is not one event. It is a relay race across audio, models, tools, and playback.

*Source: `docs/voice-agent-architecture.md`, “One Call Turn” and “Latency Budget”.*

## Scene 1 — The signal enters — 0:10–0:45

The microphone does not hand the model a neat sentence. It hands the transport a stream of
audio. Voice activity detection estimates whether speech is present. Endpointing decides
when a turn is committed. Only then does the next stage receive a stable piece of the call.
In our example, the caller says, “My AC stopped working.” The system turns that sound into a
turn event, then speech-to-text produces words the reasoning system can inspect.

*Source: `docs/voice-agent-architecture.md`, “One Call Turn”; `site/src/pages/simulations.astro`, turn-taking simulation; `labs/src/03_turn_taking.py`.*

## Scene 2 — The relay race — 0:45–1:35

Now watch the pipeline. Endpointing commits the turn. Speech-to-text produces a transcript.
The language model interprets the request and may propose a tool call, such as finding open
service slots. The application runs that tool against an authoritative source of truth. The
result returns to the model. Text-to-speech turns the response into audio, and the transport
streams that audio back to the caller.

Each box has a different owner. Transport owns media and turn boundaries. The model owns
interpretation and proposed language. The application owns the action. That separation is
the first principle: a model can suggest “find availability,” but it does not own the
schedule.

*Source: `docs/voice-agent-architecture.md`, “Reference Architecture”, “One Call Turn”, and “Ownership Rules”; `labs/src/01_realtime_protocol.py`; `labs/src/02_tools_and_guardrails.py`.*

## Scene 3 — The latency waterfall — 1:35–2:25

Put time under every handoff. Start at the moment the caller stops speaking. Add endpointing
delay. Add model time to first token or audio. Add the tool or workflow round trip. Add the
time to generate the response, then network buffering and playout. The caller experiences
the sum, not the labels.

Dead air can come from a slow endpoint decision, a slow first model sound, a backend lookup,
or buffering at the edge. Measure them separately at p50 and p95, and keep failure cases
visible. A spoken preamble like “one moment while I check that” can make the wait feel
intentional. It does not make the tool faster. It changes perceived silence, not the
waterfall underneath.

*Source: `docs/voice-agent-architecture.md`, “Latency Budget”; `site/src/pages/simulations.astro`, “Latency budget”; `labs/src/08_latency_and_scale.py`; `docs/video-notes.md`, “Deploy Voice AI Agents to Production with Full Observability”.*

## Scene 4 — The control boundary — 2:25–3:10

Suppose the caller accepts a slot. The model may propose booking it, but the application
still checks identity, policy, the offered slot, and the current phase before writing. The
workflow commits the authoritative result. Only then should the voice say what happened.
This is why tracing needs more than model tokens. Connect the caller turn, the model event,
the tool call, the backend result, and the audio response into one trace.

*Source: `docs/voice-agent-architecture.md`, “Where Each Component Stops”; `docs/evaluating-voice-agents.md`, “Code Evaluators First”; `labs/src/02_tools_and_guardrails.py`; `labs/src/07_evaluation.py`.*

## Recap and end card — 3:10–3:35

One call is a chain of boundaries: hear, decide, propose, validate, commit, and speak.
Your job is to measure each boundary instead of arguing from one end-to-end number. The
question to carry into lab 08 is: **what adds the most latency in your pipeline?**

*Source: `docs/voice-agent-architecture.md`, “Latency Worksheet”; `labs/src/08_latency_and_scale.py`.*
