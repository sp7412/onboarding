# Jev for Low-Latency Call Intent Classification

**Status:** evaluation candidate, not an assumed production dependency  
**Scope:** classify the caller's current intent early enough to route the voice-agent
workflow; do not use this classifier to decide whether a job is bookable or to commit
a booking.

**Hands-on lab:** [Lab 17 — Prompting Jev for typed decisions](../labs/17_jev_decision_workbench.ipynb) walks through state design, question instructions, criteria, a small labeled evaluation set, error analysis, and an opt-in live API call.

## Why consider it

A voice agent often needs a small, bounded judgment immediately after a caller turn:
is the caller trying to book service, reschedule, cancel, ask a question, report an
emergency, or reach a person? A general-purpose language model can solve this, but
generating prose and parsing it back into a label adds unnecessary work when the
application only needs a typed decision.

[Jev](https://www.jev.guide/en/learn/what-is-jev) is presented by its maker as a
typed, probabilistic decision model. That makes it a candidate for this narrow
classification step. Treat vendor performance statements as claims to verify on the
actual workload; do not assume a published latency is an end-to-end voice latency
guarantee.

## Proposed placement

This is the proposed control flow, not a claim about a deployed ServiceTitan
implementation. The key boundary is that **Jev returns a typed decision; the
orchestrator validates it and owns every workflow transition and side effect.**

~~~mermaid
flowchart TB
    CALLER[Caller audio] --> LIVE[GPT Live session<br/>audio, turn-taking, response]
    LIVE --> TURN[Committed utterance<br/>plus relevant session state]
    TURN --> ORCH[Application orchestrator<br/>build typed request]
    ORCH --> JEV[Jev<br/>intent and bounded judgments]
    JEV --> VALIDATE[Validate schema, labels,<br/>taxonomy version, uncertainty]
    VALIDATE --> GATE{Policy and workflow gate}

    GATE -->|Supported and clear| ROUTER[Deterministic workflow router]
    ROUTER --> TOOLS[Authorized workflow / tools]
    TOOLS --> SOURCE[Authoritative source system<br/>availability and booking state]
    SOURCE --> RESULT[Validated tool result]
    RESULT --> ORCH
    ORCH --> LIVE

    GATE -->|Missing facts or ambiguous| CLARIFY[Ask one focused clarification]
    CLARIFY --> LIVE

    GATE -->|Safety or human request| ESCALATE[Approved safety / human handoff]
    ESCALATE --> LIVE

    JEV -. timeout, error, invalid output .-> FALLBACK[Bounded fallback or clarification]
    VALIDATE -. unsupported or low confidence .-> FALLBACK
    FALLBACK --> LIVE

    ORCH -. decision, route, latency .-> TRACE[Trace, metrics, final outcome]
    JEV -. label, model/version, duration .-> TRACE
    TOOLS -. invocation, result, error .-> TRACE
    SOURCE -. confirmed business outcome .-> TRACE
~~~

Jev sits after a transcript or committed turn is available. It does not replace speech
recognition, VAD, endpointing, the conversational model, the workflow engine, or the
application control plane. If the transport has not committed the turn, do not classify
partial words as final intent unless the product explicitly supports streaming
provisional predictions.

## Keep the label space small and operational

Start with a versioned taxonomy tied to distinct next actions. Example labels for a
fictional service contractor:

| Intent | Example utterance | Initial route |
|---|---|---|
| schedule_service | “I need someone to look at my AC.” | Booking workflow |
| reschedule_service | “Can I move tomorrow's appointment?” | Existing appointment lookup |
| cancel_service | “Please cancel my visit.” | Cancellation workflow and policy checks |
| appointment_status | “What time is the technician coming?” | Status lookup |
| pricing_or_service_question | “Do you work on heat pumps?” | Answer / information workflow |
| existing_job_followup | “The repair from yesterday still isn't working.” | Existing-job workflow |
| emergency_or_safety | “I smell gas.” | Safety policy and approved urgent escalation |
| human_agent_request | “Let me speak to a person.” | Human handoff |
| other_or_unclear | Insufficient or out-of-taxonomy evidence | Clarify or general-model fallback |

This is a starting taxonomy, not a claim about ServiceTitan's internal labels. Review
overlaps with real call examples, product policy, and operations before adopting it.
Keep labels mutually distinguishable where possible; merge labels if they do not lead
to different actions. Keep the emergency path conservative and explicitly tested.

## Decision contract

Use the vendor's supported structured output rather than inventing an API schema. At
the application boundary, normalize the result to an internal contract similar to:

~~~json
{
  "intent": "schedule_service",
  "confidence": 0.93,
  "alternatives": [
    {"intent": "pricing_or_service_question", "confidence": 0.04}
  ],
  "needs_clarification": false,
  "taxonomy_version": "call-intent-v1"
}
~~~

The values above are illustrative, not measured results or guaranteed Jev fields.
Confirm the actual SDK/API fields and semantics against current vendor documentation.
If the model does not return calibrated probabilities, do not label its scores as
probabilities or interpret them as calibrated confidence.

## Runtime policy: model proposes, harness controls

1. **Validate the output.** Reject unknown labels, malformed values, missing fields,
   and taxonomy-version mismatches.
2. **Route only supported intents.** A high score is not authorization to call a tool.
   The router checks session state, tenant configuration, permissions, and workflow
   preconditions.
3. **Use an explicit uncertainty band.** Set thresholds from held-out data and the
   relative cost of mistakes. Low-confidence or close competing predictions should
   trigger clarification or a fallback, not a guessed booking action.
4. **Handle high-cost classes separately.** Emergency/safety language and requests for
   a human must not be silently routed to a routine booking path. Define conservative
   policy and fallback behavior with the appropriate product/safety owners.
5. **Keep business decisions separate.** Intent is not bookability. A caller may intend
   to schedule while job type, service area, capacity, skill, or policy makes the
   requested booking unavailable. A separate bookability judge and authoritative
   scheduling checks own that decision.
6. **Fail to a useful fallback.** On timeout, provider error, invalid output, or an
   unavailable dependency, use a bounded fallback classifier or ask a concise
   clarification question. Never block the caller indefinitely.
7. **Log decisions safely.** Trace model/version, taxonomy version, latency, selected
   label, uncertainty/fallback reason, downstream route, and final outcome. Apply
   retention, redaction, access, and tenant-isolation rules to transcripts and traces.

## Latency and evaluation plan

Measure the classifier as one segment of the full call-turn budget. Report p50, p95,
and p99 latency, timeout/error rate, and end-of-speech-to-route time. Separate provider
latency from network, transcript availability, orchestration, and fallback overhead.
Do not treat a vendor's headline latency as a measured result for this system.

Compare Jev against a simple baseline and the current general-model approach using the
same frozen test set:

- **Quality:** macro-F1, per-class precision/recall, confusion matrix, and cost-weighted
  error rate.
- **Uncertainty:** selective accuracy versus coverage, abstention rate, calibration
  error if scores are meaningful, and performance near thresholds.
- **Safety and trust:** missed emergency/human requests, unsupported-label rate, and
  incorrect workflow-routing rate.
- **Operations:** p50/p95/p99 latency, timeout/error rate, fallback frequency, and cost
  per 1,000 turns.
- **Robustness:** accents, ASR substitutions, interruptions, short/fragmentary turns,
  negation (“don't cancel”), corrections, multiple intents, noisy transcripts,
  and out-of-taxonomy requests.
- **Segmentation:** report results by intent, call phase, transcript length, and other
  approved slices; do not rely on aggregate accuracy alone.

Use fictional or properly approved, privacy-reviewed data in this public onboarding
workspace. Keep a human-reviewed gold set, freeze it before comparisons, and document
taxonomy changes. Begin in shadow mode, compare against adjudicated intent and final
business outcomes, then canary only after thresholds and rollback criteria are agreed.
A shadow prediction must not change the live route.

## GPT-Live: separate the voice model from backend reasoning

GPT-Live's real-time conversational role does **not** imply that it automatically
switches among Astra, Sol, Luna, and Terra on every caller turn. Treat model selection
as an explicit configuration or application-level routing decision, and verify the
current API behavior before relying on any particular delegation mode.

The documented architecture has two useful patterns:

- **Responses delegation:** configure a backend Responses model for GPT-Live to call.
  The delegated model is a separate choice from the real-time voice model; do not
  assume it changes dynamically unless the API explicitly supports that behavior.
- **Client-side delegation:** let the application orchestrator choose the backend
  model or workflow. This is the flexible option for applying Jev intent labels,
  workflow state, policy, latency budgets, and escalation rules to model selection.

Use the model tiers as a starting hypothesis, not as a hard-coded truth about every
request:

| Backend choice | Initial use case | Routing caution |
|---|---|---|
| **Luna** | Focused, common, well-bounded tasks where low cost and throughput matter | Route only when the required action and context are clear |
| **Sol** | More involved multi-step reasoning where a stronger model is justified | Escalate based on complexity or uncertainty, not merely on a particular intent label |
| **Astra** | Difficult reasoning, conflicting context, unusual exceptions, or high-impact cases needing the strongest available reasoning | Keep permissions and business-state checks in the harness; a stronger model is not authority to act |
| **Terra** | Compatibility with an existing GPT-5.6-based integration, if still available and validated | Treat as an earlier-generation option, not the default for a new design; verify current availability |

The current model catalog and delegation guide are authoritative for model names,
capabilities, availability, and configuration:

- [OpenAI model catalog](https://developers.openai.com/api/docs/models)
- [GPT-Live delegation guide](https://developers.openai.com/api/docs/guides/live-delegation)
- [Connect voice to Decisions](https://developers.openai.com/api/docs/guides/decisions-voice)

### Example: Jev plus an explicit router

1. Wait for the committed transcript/turn, then use Jev to classify the caller's
   **intent** into the versioned taxonomy above.
2. Apply deterministic policy and session-state checks. Safety, human handoff,
   authorization, and tool permissions are governed by the application, not by the
   model-tier choice.
3. Keep simple, well-bounded requests on the least expensive backend that passes the
   quality bar. Use Sol when the task requires broader reasoning; reserve Astra for
   genuinely difficult or consequential cases where evaluation shows a benefit.
4. Ask a clarifying question or use a deterministic workflow when intent or required
   facts are missing. Do not escalate every low-confidence case to a larger model if
   clarification is safer and cheaper.
5. Log the routing reason, selected model, latency, outcome, and fallback. Evaluate
   quality and p50/p95/p99 end-to-end turn latency by intent and complexity, then tune
   thresholds from held-out and shadow-mode results.

For example, a clear appointment-status request may need only a status lookup; a
reschedule may require appointment lookup, availability checks, and confirmation; an
unusual exception with conflicting records may justify stronger reasoning. These are
illustrative policies, not claims about OpenAI's hidden internal router or ServiceTitan's
production implementation. The model may propose a plan, but the harness validates
business state and controls side effects.

## Suggested hands-on exercise

1. Create a small, balanced, fictional transcript set for the labels above, including
   ambiguous and out-of-taxonomy cases.
2. Define a typed internal interface and validate labels before routing.
3. Run a baseline classifier and Jev on the same examples; record per-class errors and
   latency distributions without hard-coding vendor latency claims.
4. Add uncertainty handling and a deterministic fallback.
5. Test that schedule_service does not imply bookability and that safety/human intents
   cannot fall through to routine scheduling.
6. Write a short evaluation note with quality, p95/p99 latency, fallback rate, and
   unresolved risks before proposing a live canary.

## Questions to answer before adopting

- Does the current Jev API support the required label/choice structure, confidence
  semantics, concurrency, timeout controls, and deployment/data-handling requirements?
- What are measured p95/p99 latencies from the actual region and runtime, including
  network overhead?
- How are taxonomy updates versioned and rolled back?
- What is the agreed fallback if Jev is slow or unavailable?
- Which mistakes are expensive enough to require clarification or human handoff?
- How will drift, ASR changes, and newly observed intents enter the evaluation loop?

## References

- [Jev: What is Jev?](https://www.jev.guide/en/learn/what-is-jev) — vendor description;
  verify current API details and claims before implementation.
- [Voice-Agent Architecture](voice-agent-architecture.md) — component ownership,
  latency budget, control-plane boundaries, and observability.
- [Business Metrics](business-metrics.md) — connect classification quality to customer
  outcomes rather than optimizing latency in isolation.
- [Realtime Voice-Agent Evaluation](realtime-voice-agent-evaluation.md) — evaluate the
  full audio-to-tool pipeline with staged replay, trace-level diagnosis, and regression
  gates; Jev classification is only one component of that system.


## GPT Live + Jev: a practical runtime design

Use GPT Live for the real-time voice interaction and Jev for narrow, typed decisions.
Keep the application orchestrator as the control plane: it validates decisions, owns
workflow state, checks permissions, and executes side effects. This avoids turning
both models into competing autonomous agents.

~~~mermaid
flowchart TD
    A[Caller audio] --> B[GPT Live: voice, turn-taking, response]
    B --> C[Committed utterance / relevant session state]
    C --> D[Jev: typed intent and decision signals]
    D --> E{Orchestrator policy gate}
    E -->|Clear supported intent| F[Deterministic workflow / tool]
    E -->|Missing facts or uncertain intent| G[GPT Live asks a focused clarification]
    E -->|Safety or human request| H[Approved escalation path]
    F --> I[Authoritative tool result]
    I --> B
    G --> B
    H --> B
~~~

### Example: rescheduling an appointment

Caller: “Can you move my appointment to Friday afternoon?”

1. GPT Live acknowledges the caller naturally while the backend works, without
   claiming the change is already made.
2. The orchestrator supplies Jev the committed utterance and only the relevant,
   authorized session/workflow state.
3. Jev classifies the request as `reschedule_service` and can separately assess
   whether the next step needs clarification or human handoff.
4. The orchestrator verifies customer and appointment identity, invokes the scheduling
   workflow, and asks the authoritative system for availability.
5. GPT Live communicates actual available options. The agent confirms a change only
   after the scheduling system reports success.

Jev identifies intent; it cannot establish that Friday has availability, authorize a
change, or prove that a booking succeeded.

### Illustrative Jev decision contract

The following is conceptual pseudocode for the decision inputs and questions, not a
copy-paste Jev API payload. Use the current Jev SDK's documented request syntax and
typed-question schema when implementing it.

~~~text
state:
  latest_utterance: "Can you move my appointment to Friday afternoon?"
  conversation_summary: "Caller has an existing service appointment."
  appointment_identified: true
  workflow_state: "awaiting_reschedule_request"

questions:
  intent:
    type: choice
    options:
      - reschedule_service
      - schedule_service
      - cancel_service
      - appointment_status
      - pricing_or_service_question
      - existing_job_followup
      - emergency_or_safety
      - human_agent_request
      - other_or_unclear
    instruction: "Classify the caller's current request from the evidence."

  needs_clarification:
    type: noul
    instruction: "Is information missing before the next valid workflow step?"

  human_handoff:
    type: noul
    instruction: "Does the caller request a person or require human assistance?"
~~~

Keep each label tied to a distinct next action. Define the exact `choice` options and
`noul` semantics using the installed Jev API version; do not assume the illustrative
field names above are accepted verbatim. Treat scores as calibrated probabilities only
if the API and evaluation establish that interpretation.

### Latency and concurrency rules

- **Do not invoke Jev on every audio frame.** Start with committed turns. Evaluate
  provisional partial-transcript classification only if the runtime supports it and
  early decisions measurably help.
- **Acknowledge in parallel, act serially.** GPT Live may say “I can help with that”
  while Jev runs, but only the orchestrator should commit a workflow transition or tool
  action. Prevent duplicate/conflicting tool calls.
- **Batch related judgments.** When supported, ask intent, clarification, and handoff
  questions against the same state in one Jev evaluation.
- **Clarify instead of blindly escalating.** If the utterance is ambiguous or required
  facts are missing, GPT Live should ask one targeted question. Route safety and explicit
  human requests through separately tested policy paths.
- **Measure the whole path.** Record end-of-speech-to-decision and end-of-speech-to-route
  p50/p95/p99, Jev service time, network/orchestration overhead, fallback rate, and
  downstream outcomes. Compare quality and latency against a simple baseline in shadow
  mode before changing live routing.

### Responsibility boundaries

| Component | Owns | Must not own |
|---|---|---|
| GPT Live | Audio conversation, turn-taking, natural phrasing, clarification | Authoritative appointment state or unvalidated side effects |
| Jev | Bounded typed judgments from supplied state | Booking availability, permissions, or confirmation of tool success |
| Orchestrator | State machine, validation, policy, retries, idempotency, tool authorization | Delegating its control responsibilities to model prose |
| ServiceTitan tools / source systems | Authoritative customer, job, availability, and booking results | Inferring caller intent from conversational context alone |

Start with this separation even if the first implementation uses a single backend model.
Only add dynamic backend-model selection when an evaluation shows that the quality gain
justifies its added latency, cost, and operational complexity.
