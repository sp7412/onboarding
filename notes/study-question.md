# Where does each component stop?

> Where does each component stop, and where does the application's own control
> plane, business logic, guardrails, and state management begin?

| Component | Owns | Stops at | Evidence from the labs |
|---|---|---|---|
| LiveKit | Media transport, rooms, participants, turn handling, interruptions, and session lifecycle | Business rules, source-of-truth state, authorization, and what the agent should do | Lab 03 shows VAD/endpointing tradeoffs; lab 04 reuses the same guarded tools across agent sessions |
| Realtime model | Speech understanding, response generation, conversational context, and proposed tool calls | Tool execution, authoritative facts, durable state, policy enforcement, and knowing exactly what audio was heard | Lab 01 demonstrates cancellation/truncation; lab 02 demonstrates an early `create_job` proposal being blocked |
| LangChain / LangGraph | Model/tool orchestration, middleware hooks, explicit workflow transitions, checkpoints, and interrupts | Audio transport, turn-taking, systems of record, and the product definition of an allowed action | Lab 05 shows middleware and context/state; lab 06 makes confirmation a graph edge and resumes after a simulated crash |
| LangSmith | Traces, run metadata, datasets, evaluators, experiments, and monitoring | Runtime enforcement, uninstrumented audio timing, and deciding what success means | Lab 07 compares trusting and guarded versions and separates code evaluators from LLM judges |
| Control plane | Identity, authorization, policy, evidence grounding, phase state, idempotency, emergency screening, escalation, redaction, and outcome definitions | It delegates mechanisms to vendors and decisions to product/compliance owners | Labs 00, 02, 06, and 08 show authoritative records, tool guards, durable workflow state, and verbatim transcript handoff |

## My answer

The vendors provide mechanisms, but the application control plane provides authority. LiveKit
can move audio and help decide when a turn begins or ends; the realtime model can interpret
the caller, speak, and propose a tool call; LangChain and LangGraph can run orchestration;
and LangSmith can observe and score what we instrument. None of those boundaries makes a
booking valid by itself. The control plane must establish identity, consult the source of
truth, enforce phase and safety policy, ground confirmations in the caller's actual words,
make commits idempotent, and decide when to escalate. The labs made this visible by blocking
an early booking, truncating interrupted speech to what was actually played, forcing the
graph through address confirmation, and passing verbatim transcript evidence to the thinker.
In production, I would keep those hard decisions outside prompts and model context, then
measure both the technical path and the contractor outcome.
