# Episode 4 — The control plane

Target length: 3:40 · Approx. 525 words · Running example: booking service after “my AC stopped working.”

## Cold open — 0:00–0:10

The model says, “I can book Thursday.” But has anything been booked? In a safe voice agent,
the model proposes. The application decides.

*Source: `docs/voice-agent-architecture.md`, “Ownership Rules”; `docs/video-notes.md`, “Building Effective Voice Agents”.*

## Scene 1 — Identity and ownership — 0:10–0:55

Start with identity. The transport knows which session and participant supplied the audio.
The model can interpret the caller’s words, but it should not invent authority. Before a
state-changing action, the control plane verifies the customer and checks that the requested
operation belongs to that customer and current call phase.

This boundary is deliberately boring. Boring is good when a voice model is probabilistic.
It turns “please book it” into a proposed operation with evidence, policy, and an owner.

*Source: `docs/voice-agent-architecture.md`, “Where Each Component Stops”; `labs/src/02_tools_and_guardrails.py`; `docs/gpt-live-1.md`, section 4.*

## Scene 2 — Grounded confirmation — 0:55–1:40

Now draw the slot and address as cards. The system offered Thursday from ten to noon. The
caller confirmed that slot and the service address. The control plane checks that the chosen
slot was actually offered and that the address came from the caller’s evidence. A model
paraphrase is not enough.

The same rule applies to spoken claims. Never say “you’re booked” before the authoritative
write commits. A preamble may say that the system is checking. It must not turn an intention
into a fact.

*Source: `docs/voice-agent-architecture.md`, “Talker And Thinker”; `docs/evaluating-voice-agents.md`, “Code Evaluators First”; `labs/src/02_tools_and_guardrails.py`; `labs/src/07_evaluation.py`.*

## Scene 3 — Interrupt-safe writes — 1:40–2:25

The caller interrupts during the booking request. This is not only an audio problem. It is a
write problem. The application needs an idempotency key so a retry does not create a duplicate
job. It needs an explicit policy for whether an in-flight operation finishes or is cancelled.
Then the next spoken response must describe the committed result, not the model’s previous
plan.

Observability records the trajectory: proposal, checks, backend response, retry, and final
outcome. That trace lets evaluation ask whether the workflow was legal, not just whether the
last sentence sounded confident.

*Source: `docs/gpt-live-1.md`, sections 3–4; `docs/evaluating-voice-agents.md`, “Code Evaluators First”; `labs/src/01_realtime_protocol.py`; `labs/src/02_tools_and_guardrails.py`.*

## Scene 4 — Emergency escalation — 2:25–3:05

Not every request belongs in the booking workflow. Emergency language, a request for a human,
or an unsupported case can trigger escalation. The control plane defines the evidence, the
safety guidance allowed before transfer, the context handed to the human, and how missed
escalations are measured.

The model can detect a clue. The application owns the routing policy. That distinction keeps
an OOD detector from becoming a magic classifier and keeps a safety decision out of a prompt
alone.

*Source: `docs/evaluating-voice-agents.md`, “OOD Detection And Routing”; `docs/whitepaper/12-risks-and-failure-modes.md`; `labs/src/02_tools_and_guardrails.py`.*

## Scene 5 — Repeat trials — 3:05–3:25

Finally, evaluate it repeatedly. Use smoke paths, capability cases, adversarial interruptions,
and regression failures. Gate hard invariants with deterministic checks: offered slot,
verified customer, grounded address, no emergency booking, and idempotent retry. Use human or
judge review for tone and clarity, but never let a soft score override a hard invariant.

*Source: `docs/evaluating-voice-agents.md`, “Dataset Strategy”, “Code Evaluators First”, and “Offline And Online Evaluation”; `labs/src/07_evaluation.py`.*

## Recap and end card — 3:25–3:40

The control plane owns identity, authorization, evidence grounding, phase state, idempotency,
safety, escalation, redaction, and outcome definitions. The model can be swapped. Those
responsibilities cannot disappear. Start with labs 02 and 07.

*Source: `docs/voice-agent-architecture.md`, “Where Each Component Stops”; `labs/src/02_tools_and_guardrails.py`; `labs/src/07_evaluation.py`.*
