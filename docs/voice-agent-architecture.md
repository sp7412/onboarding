# Voice-Agent Architecture

This is a vendor-neutral reference architecture illustrated with the vendors used in
the labs. The mock backend and simulator are fictional teaching fixtures.

## Reference Architecture

```mermaid
flowchart TB
    Caller[Caller: PSTN or browser]
    Transport[Transport: SIP/WebRTC, media, VAD, endpointing, playout]
    Talker[Realtime talker: speech understanding and response generation]
    Control[Application control plane: identity, policy, state, safety, escalation]
    Workflow[Workflow thinker: deterministic graph or agent loop]
    Record[Systems of record: customer, schedule, job, billing]
    Observe[Observability and evaluation: traces, metrics, datasets, review]
    Caller <--> Transport <--> Talker
    Talker <--> Control
    Control <--> Workflow
    Control <--> Record
    Transport -. timing .-> Observe
    Talker -. tokens and errors .-> Observe
    Control -. outcomes and policy .-> Observe
    Workflow -. trajectory .-> Observe
```

## One Call Turn

```mermaid
sequenceDiagram
    participant C as Caller
    participant T as Transport
    participant M as Talker
    participant P as Control plane
    participant W as Thinker/workflow
    participant S as Source of truth
    C->>T: Speak and pause
    T->>T: VAD and endpointing
    T->>M: Transcript/turn event
    M->>P: Tool proposal with arguments
    P->>P: Validate phase, identity, evidence, policy
    P->>W: Run approved workflow step
    W->>S: Read or commit authoritative state
    S-->>W: Result or policy error
    W-->>P: Structured result
    P-->>M: Tool output or escalation instruction
    M-->>T: Stream response audio
    T-->>C: Audible response
    P-->>P: Record audit and outcome metrics
```

## Latency Budget

Treat these as planning categories, not universal targets. Measure p50, p95, and
failure cases in the actual deployment.

```mermaid
flowchart LR
    A[Caller stops] --> B[Endpointing]
    B --> C[Model TTFT]
    C --> D[Tool or workflow latency]
    D --> E[Response generation]
    E --> F[Network and playout]
    F --> G[Caller hears useful answer]
```

The caller experiences the sum. A preamble can reduce perceived dead air, but it does
not make the underlying tool faster. Track separately:

| Segment | Owner | Useful measurement |
|---|---|---|
| End of speech to committed turn | Transport | endpointing delay and premature cutoffs |
| Committed turn to first sound | Talker/model | time to first token or audio |
| Tool proposal to tool result | Control plane/workflow/backend | p50/p95, timeout, retry, policy errors |
| Result to useful answer | Talker | second response latency |
| Stream to caller | Transport | first-byte, buffering, playout interruption |

## Talker And Thinker

```mermaid
flowchart LR
    Audio[Audio and turn-taking] --> Talker[Talker: fast, brief, conversational]
    Talker -->|verbatim evidence + intent| Thinker[Thinker: workflow, tools, durable state]
    Thinker -->|structured say/done/outcome| Talker
    Thinker --> Backend[Authoritative backend]
    Talker --> Metrics[Turn and speech metrics]
    Thinker --> Metrics[Business outcome and policy metrics]
```

The talker should not be trusted as the source of truth. In the capstone, the control
plane passes the transcript evidence to the workflow rather than blindly trusting a
model-paraphrased tool argument. This is analogous to separating a detector from the
authority that decides whether an action is allowed.

## Ownership Rules

- Transport owns media movement, turn boundaries, and local playout state.
- The model owns interpretation and proposed language or tool calls.
- The control plane owns authorization, phase transitions, grounding, idempotency,
  redaction, and escalation policy.
- The workflow owns a durable process, not the system of record itself.
- Observability records what is instrumented; it does not enforce runtime policy.

## Where Each Component Stops

| Component | Owns | Stops at |
|---|---|---|
| LiveKit / transport | Media, rooms, participants, turn handling, interruptions, and session lifecycle | Business rules, source-of-truth state, authorization, and what the agent should do |
| Realtime model | Speech understanding, response generation, context, and proposed tool calls | Tool execution, authoritative facts, durable state, policy enforcement, and knowing exactly what audio was heard |
| LangChain / LangGraph | Model/tool orchestration, middleware, workflow transitions, checkpoints, and interrupts | Audio transport, turn-taking, systems of record, and defining allowed actions |
| LangSmith | Traces, metadata, datasets, evaluators, experiments, and monitoring | Runtime enforcement, uninstrumented audio timing, and deciding what success means |
| Application control plane | Identity, authorization, policy, evidence grounding, phase state, idempotency, safety, escalation, redaction, and outcome definitions | It delegates mechanisms to vendors and decisions to product/compliance owners |

## Latency Worksheet

Fill this in with measured values from the labs or an authorized test environment. The
right-hand values are planning categories, not vendor guarantees.

| Stage | Your measurement | Planning category |
|---|---:|---:|
| End of caller speech → turn committed | | endpointing delay |
| Turn committed → first model audio | | model time to first audio |
| Simple tool round trip | | backend and control-plane latency |
| Multi-step workflow | | off the hot path or masked with filler |
| Network and playout buffering | | transport latency |
| Caller stops → useful answer | | total customer-perceived latency |

The labs provide executable evidence for these boundaries: lab 01 demonstrates
cancellation and truncation, lab 02 blocks an early booking, lab 05 separates context
from state, lab 06 makes confirmation a graph edge, and lab 08 passes verbatim transcript
evidence to the thinker.

See the labs for executable examples.
