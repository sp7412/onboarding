# Voice Agent Production Troubleshooting Runbook

Use this runbook when a live voice agent produces a poor interaction, an incorrect
business outcome, or a reliability regression. It is a symptom-first companion to
[Running Agents in Production](whitepaper/17-running-agents-in-production.md),
[Failure Modes](whitepaper/12-risks-and-failure-modes.md), and
[Evaluating Voice Agents](evaluating-voice-agents.md).

The examples are generic patterns, not descriptions of any company's internal systems.
Use fictional data in this repository. In production, follow approved policies for
transcript access, PII redaction, retention, and incident communications.

## Operating principle

**Start with the caller-visible symptom, trace backward to the failed stage, and verify
the fix against the committed business outcome.** A fluent transcript is not proof that
a booking succeeded. A green service health check is not proof that the workflow is
correct.

## 1. Triage and contain

Prioritize by harm and business impact, not just request volume.

| Severity | Examples | Immediate response |
|---|---|---|
| SEV-1 | Emergency routed to routine service; widespread unauthorized or incorrect actions; sensitive data exposed | Stop the unsafe action path, enable human handling, preserve relevant telemetry, notify the incident owner |
| SEV-2 | Duplicate/wrong bookings across multiple calls; core tool or telephony dependency unavailable; major call completion regression | Disable or constrain affected tools, switch to a tested fallback, consider rollback |
| SEV-3 | Isolated wrong answer, elevated latency, interruption or transcription defect with a safe fallback | Mitigate the affected cohort, collect traces, prioritize a targeted fix |
| SEV-4 | Cosmetic phrasing or low-impact quality issue with no policy or outcome violation | Record and evaluate; fix through the normal release process |

Severity depends on context. Follow the service's actual incident policy and escalation
chain; this table is a starting point, not a replacement.

### Safe containment options

- Route calls to a human or a tested fallback when the agent cannot safely proceed.
- Disable the specific tool/action or lower its autonomy level; avoid disabling unrelated
  capabilities without evidence.
- Roll back the prompt, model, tool schema, or release that correlates with the regression.
- Pause automated booking or other irreversible writes if commit state is uncertain.
- Preserve trace IDs, version identifiers, timestamps, error codes, and sanitized evidence
  before short-lived telemetry expires.

Do not repeatedly retry a write after a timeout until you know whether the original request
committed. The timeout may have occurred after the server applied the action.

## 2. Symptom-to-diagnosis guide

| Caller-visible symptom | Inspect first | Common causes | Corrective action |
|---|---|---|---|
| Agent talks over the caller or misses an interruption | Audio replay, VAD events, endpointing, barge-in events, transcript boundaries | Endpointing too aggressive; interruption policy ignores speech; noisy audio | Tune turn detection against representative audio; test interruptions and backchannels; confirm partial transcripts are not treated as final |
| Long silence before a response | Stage-level latency spans: end-of-turn, model first token/audio, tool call, TTS first audio | Slow endpointing; model/provider latency; serial tool calls; blocked dependency | Find the slow span; set stage-specific timeouts; parallelize only independent reads; give concise progress feedback when useful |
| Agent responds before caller finishes | Turn detector events, final/partial transcript, end-of-turn confidence | Endpointing too short; silence threshold mismatched to caller cadence | Tune with natural pauses and diverse speech; evaluate premature-turn and missed-turn rates together |
| Caller repeats details or the agent forgets context | Transcript sequence, session ID, conversation state, summary updates, tool arguments | Lost turns; incorrect state merge; session reset; stale summary or context truncation | Fix state lifecycle and transcript ordering; persist confirmed facts explicitly; test long calls and reconnects |
| Names, addresses, dates, or numbers are wrong | Audio, ASR alternatives, normalized slots, confirmation turn, downstream payload | ASR confusion; locale/format normalization; weak confirmation policy | Confirm high-impact fields explicitly; preserve original and normalized values; validate formats and eligibility server-side |
| Wrong appointment or technician | Intent/slot extraction, availability result, dispatch recommendation, policy decision, booking record | Stale availability; wrong entity mapping; policy gap; race condition | Validate against the source of truth at commit time; enforce business constraints in code; add a regression case |
| Agent says “booked” but no job exists | Tool invocation/result, HTTP status, transaction/commit record, spoken response | Confirmation based on proposed action; swallowed error; asynchronous commit not complete | Speak success only after authoritative confirmation; otherwise explain uncertainty and verify or hand off |
| Duplicate jobs after retry or reconnect | Idempotency key, request ID, retry history, write audit log, commit status | Non-idempotent tool; timeout after commit; retry creates a new request ID | Use stable idempotency keys; reconcile uncertain commits before retry; test timeout-after-commit and reconnect paths |
| Emergency handled as routine booking | Safety/intent classification, routing decision, policy version, escalation event | Emergency signal missed; policy runs too late; tool path bypasses safety check | Put safety routing before routine workflow actions; block routine booking when required; evaluate missed-emergency rate separately |
| Too many or too few human transfers | Transfer reason, confidence/abstention, policy decision, outcome after transfer | Threshold miscalibration; unsupported intent misclassified; handoff unavailable | Tune using labeled cases; monitor false-positive and missed-escalation rates by intent; test handoff failure and context transfer |
| Tool or provider errors spike | Error codes, timeout rate, dependency health, retry count, circuit-breaker state | Provider outage; credentials/configuration; rate limits; schema drift | Bound retries with backoff and jitter; use circuit breakers and deadlines; validate schemas; activate fallback or human handoff |
| Agent sounds fluent but outcome is wrong | Full trace plus authoritative final application/database state | Tool result ignored; invalid action accepted; policy or arbitration defect | Debug end-to-end; compare proposed, authorized, executed, and committed actions; add deterministic invariant checks |
| Quality regresses after a release | Release/model/prompt/tool versions, canary cohort, sliced metrics | Prompt/model change; dependency version change; cohort/distribution shift | Roll back if guardrails breach; compare matched cohorts; reproduce offline; gate promotion on safety and outcome metrics |

## 3. Reconstruct one failed call

Start with a conversation or trace ID and build a single timeline. Avoid searching raw
transcripts alone; the key evidence is how the system moved from caller input to action.

1. **Confirm the reported outcome.** Check the system of record, not only the agent's
   final utterance. Determine whether the action was proposed, authorized, attempted,
   committed, rejected, or later reversed.
2. **Find the correlated trace.** Join conversation/call ID to trace ID, application
   request ID, customer/job ID (using approved access), and the relevant tool request.
3. **Replay the timeline.** Include audio/turn events, transcript revisions, state updates,
   model and prompt versions, tool arguments/results, policy decisions, retries, handoff,
   and final business state.
4. **Find the earliest incorrect transition.** Examples: speech was truncated; a confirmed
   address became a different normalized address; availability was stale; a policy check
   was skipped; a failed write was narrated as successful.
5. **Classify the failure.** Separate perception/ASR, turn-taking, state/context, model
   proposal, orchestration, policy/authorization, tool integration, and downstream
   business-state failures.
6. **Compare with a successful call.** Prefer a matched intent, trade, channel, and backend
   condition. This often distinguishes a general defect from a cohort-specific one.
7. **Create a minimal reproduction.** Use synthetic or properly redacted input, a recorded
   audio fixture where permitted, and deterministic tool responses where possible.
8. **Add a regression test.** Encode the expected user-visible behavior and the business
   invariant that must hold. Include the original failure and nearby edge cases.

### Useful trace fields

Capture structured metadata so incidents can be queried without exposing unnecessary
conversation content:

```text
trace_id, conversation_id, call_id, request_id
agent_version, prompt_version, model/provider_version
tool_name, tool_version, tool_request_id, idempotency_key
turn_event, transcript_revision, latency_ms, timeout_ms
policy_name, policy_version, decision, reason_code
retry_count, error_code, handoff_reason
proposed_action, authorized_action, executed_action, commit_status
final_outcome, evaluator_result, release_cohort
```

Use stable IDs and timestamps across services. Keep transcripts and sensitive tool payloads
separately governed; apply redaction, least-privilege access, retention limits, and audit
logging. Do not put secrets or raw payment/authentication material into traces.

## 4. Diagnose latency by stage

Measure stage-level distributions, not just end-to-end average latency. Track p50, p95,
and p99, and segment by model/provider, tool, call channel, language where permitted,
intent, and release cohort.

| Stage | What to measure | Typical investigation |
|---|---|---|
| Audio ingress | Packet gaps, jitter, reconnects, dropped frames | Network, telephony, codec, room/transport health |
| Turn detection | End-of-turn delay, false endpointing, interruption detection | VAD/endpointing configuration and acoustic conditions |
| ASR / input processing | Finalization time, revision count, confidence where available | Audio quality, model latency, language/domain mismatch |
| LLM | Time to first token and completion, token count, provider errors | Prompt/context size, model choice, provider load, output length |
| Tool / backend | Queue time, execution time, timeout and retry rates | Slow dependency, N+1 calls, contention, rate limiting |
| TTS / output | Time to first audio, synthesis duration, playback gaps | Voice/model latency, chunking, transport and buffering |
| Full workflow | End-of-user-turn to useful first response; completion time | Critical path and accumulated waits, not just one component |

Use the latency budget and SLO defined for the actual product. Do not apply one universal
threshold to every voice-agent design. A fast response that is incorrect or unsafe is not
an improvement.

## 5. Correct the cause at the right layer

Prefer the narrowest reliable fix:

- **Perception/turn-taking:** improve audio handling, endpointing, interruption behavior,
  transcription normalization, or confirmation of ambiguous fields.
- **Context/state:** make state transitions explicit; version summaries; distinguish
  caller-provided, inferred, and server-confirmed facts.
- **Model/prompt:** tighten instructions, tool descriptions, or output schemas only after
  confirming the model/prompt is the failure source. Do not prompt-engineer around a
  missing backend invariant.
- **Orchestration/control plane:** enforce legal transitions, deadlines, retry budgets,
  cancellation, arbitration, and autonomy limits in deterministic code.
- **Tool/business layer:** validate identity, eligibility, availability, authorization, and
  idempotency server-side; return structured, unambiguous outcomes.
- **Dependency/reliability:** use bounded retries, circuit breakers, timeouts, backpressure,
  health checks, and tested fallbacks.
- **Evaluation/operations:** add monitors, improve trace correlation, build a slice-specific
  regression set, and document a safe rollback path.

The model may propose an action; the control plane decides whether it is allowed, and the
system of record determines whether it actually happened.

## 6. Verify recovery before restoring traffic

A fix is not done when the exception disappears. Verify all relevant layers:

- [ ] The original reproduction now passes.
- [ ] Deterministic safety and business invariants pass.
- [ ] Adjacent regression cases pass, including timeouts, retries, interruptions, and
      ambiguous caller input where relevant.
- [ ] No new regressions appear in critical slices.
- [ ] A canary or shadow comparison shows healthy latency and error rates.
- [ ] Final business outcomes (valid bookings, duplicates, missed escalations, correct
      handoffs) remain within the defined guardrails.
- [ ] Rollback and human fallback paths still work.
- [ ] The incident, root cause, owner, and follow-up actions are recorded.

Restore traffic gradually. Monitor guardrails first, then quality and business outcomes;
rollback if a hard invariant or agreed threshold is breached.

## 7. Turn incidents into durable learning

For each meaningful production failure, record:

- symptom and impact;
- affected release, model, prompt, tool, and cohort;
- trace ID and sanitized reproduction;
- earliest failed transition and root cause;
- immediate containment and permanent corrective action;
- regression test/evaluation added;
- recovery evidence and follow-up owner.

Add reviewed cases to the regression set, but do not let it consist only of spectacular
failures. Keep representative successful calls too, and report results by important slice.
Revisit recurring incident patterns to determine whether the real fix belongs in the model,
the control plane, the tool contract, or the operational process.

## Related material

- [Running Agents in Production](whitepaper/17-running-agents-in-production.md): traces, failure mining, canaries, and rollout.
- [Risks and Failure Modes](whitepaper/12-risks-and-failure-modes.md): hazard classes and mitigations.
- [Evaluating Voice Agents](evaluating-voice-agents.md): metrics, datasets, and release evaluation.
- [Voice Agent Architecture](voice-agent-architecture.md): system boundaries and workflow stages.
