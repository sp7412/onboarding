# Jev for Low-Latency Call Intent Classification

**Status:** evaluation candidate, not an assumed production dependency  
**Scope:** classify the caller's current intent early enough to route the voice-agent
workflow; do not use this classifier to decide whether a job is bookable or to commit
a booking.

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

~~~mermaid
flowchart LR
    A[Caller audio] --> B[STT / committed transcript]
    B --> C[Jev intent decision]
    C --> D{Confidence and policy gate}
    D -->|Clear supported intent| E[Deterministic router]
    D -->|Ambiguous or unsupported| F[Clarify or general model]
    D -->|Safety / human request| G[Approved escalation path]
    E --> H[Workflow / tools]
    F --> H
    G --> H
    H --> I[Trace and outcome]
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
