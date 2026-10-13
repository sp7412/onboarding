# Evaluating Realtime Voice Agents

**Purpose:** turn a promising GPT Realtime / GPT Live demo into a repeatable,
diagnosable reliability evaluation. This guide adapts the methodology in the
[OpenAI Cookbook Realtime Eval Guide](https://github.com/openai/openai-cookbook/blob/main/examples/Realtime_eval_guide.ipynb)
for a voice agent that must understand callers, invoke tools correctly, and report
real workflow outcomes without inventing success.

## The core rule

A realtime turn is a pipeline, not one model call. Speech start/stop, audio buffering,
turn commit, response generation, tool selection, tool execution, audio playback, and
interruption handling can fail independently. A fluent final answer does not prove
that the agent understood the caller or completed the requested action.

Evaluate two independent dimensions:

- **Task/content correctness:** intent, instruction following, tool choice and
  arguments, policy compliance, workflow state, and final outcome.
- **Audio/interaction quality:** turn-taking, latency, interruptions, cutoffs, silence,
  overlap, intelligibility, pronunciation, pacing, and naturalness.

A transcript is evidence, not ground truth: ASR can omit or normalize words and digits,
and a clean transcript does not prove that the model heard the audio correctly. Use
transcripts and traces for scalable grading, preserve the original audio where approved,
and periodically audit sessions end to end.

## Build evaluation complexity in stages

Use the OpenAI Cookbook's **Crawl → Walk → Run** progression. Keep test inputs and
runtime settings fixed while isolating one source of variance at a time.

| Stage | Input / interaction | What it isolates | Entry criterion |
|---|---|---|---|
| **Crawl** | Synthetic or TTS audio, one user turn, one assistant turn; deterministic turn boundary where possible | Intent, instruction following, tool choice, arguments, structured output | Repeatable single-turn cases pass the basic correctness bar |
| **Walk** | Saved human audio with realistic phone compression, noise, hesitations, accents, and self-corrections; still single-turn | Audio perception, transcription, endpointing and robustness | Single-turn correctness is stable on clean inputs |
| **Run** | Simulated multi-turn conversations, user corrections, missing details, and injected tool errors | State retention, clarification, sequencing, recovery, duplicate actions and episode completion | Single-turn and audio robustness are understood |
| **End-to-end audit** | Human-reviewed full sessions with real interaction timing and audio | Whether the experience feels reliable to callers | Run throughout development; not a one-time final gate |

The stages are complementary, not replacements for one another. Do not jump directly
to complicated multi-turn runs when a simple tool-selection test is still failing.

OpenAI's reference implementations are available in the
[Realtime eval harnesses](https://github.com/openai/openai-cookbook/tree/main/examples/evals/realtime_evals):
[Crawl harness](https://github.com/openai/openai-cookbook/tree/main/examples/evals/realtime_evals/crawl_harness),
[Walk harness](https://github.com/openai/openai-cookbook/tree/main/examples/evals/realtime_evals/walk_harness),
and [Run harness](https://github.com/openai/openai-cookbook/tree/main/examples/evals/realtime_evals/run_harness).
Use them as reference implementations and verify compatibility with the API version
and runtime being evaluated.

## Start with a small, reviewed gold set

Begin with roughly 10–50 carefully reviewed examples that cover high-value flows and
the failures that would be costly. Expand based on observed gaps rather than maximizing
dataset size.

For a fictional service-booking agent, include both **positive and negative** examples
for each important behavior:

- Schedule, reschedule, cancel, and appointment-status requests.
- Missing identity, date, time, address, or other required details that should trigger
  one focused clarification instead of a guessed tool call.
- Similar-looking intents that must route differently.
- Explicit human requests and safety-related utterances with their approved paths.
- Negation, corrections, interruptions, short acknowledgements, and multiple intents.
- Tool timeouts, malformed tool results, unavailable slots, and retry conditions.
- Cases where the agent must **not** call a tool or must not claim success.

Tag each example with a stable ID, intent, expected outcome, audio condition, turn count,
expected tool and arguments (if any), expected clarification/escalation, and expected
final workflow state. Keep a held-out set untouched for occasional checks against
overfitting. Use only fictional or properly approved, privacy-reviewed data in this
public onboarding repo.

## Grade with a layered grader stack

Use the simplest trustworthy grader for each requirement.

1. **Deterministic graders** for objective facts: expected tool called, arguments valid,
   required fields present, prohibited tool absent, schema valid, final state correct,
   no duplicate mutation, and success not claimed before authoritative confirmation.
2. **LLM graders** for qualities that need interpretation: whether the answer addresses
   the request, the clarification is appropriate, instructions were followed, and the
   response is complete. Calibrate them against human-reviewed examples; don't treat
   an LLM judge as ground truth.
3. **Audio and interaction graders** for measurable behaviors: silence duration,
   response-start latency, speech overlap, interruption recovery, truncated output,
   and turn-boundary errors. Pair automated measures with listening audits for pacing,
   prosody, and perceived naturalness.
4. **Human review** of audio plus full traces to find failures that automated metrics
   miss and to catch mislabelled examples or biased graders.

Avoid compressing everything into one aggregate score. A high task score can conceal
bad audio, and a natural voice can conceal an incorrect or missing tool action.

## Instrument the full turn

Persist enough trace data to locate the failing stage. Use correlation IDs and timestamps
for events such as:

- Audio input started/ended; chunk sizes and transport errors.
- VAD / endpointing decision and user-turn commit.
- Transcript and any relevant confidence/quality signals, with privacy controls.
- Response requested, first output audio/text, completion event, and interruption.
- Tool name, validated arguments, invocation/result/error, retry, timeout, and idempotency
  outcome.
- Orchestrator decision, policy/authorization result, workflow state before and after,
  fallback reason, and final authoritative business outcome.

Measure latency by segment as well as end to end: end-of-speech-to-first-audio,
end-of-speech-to-tool-call, tool duration, end-of-speech-to-final-response, and total
task completion time. Report p50, p95, and p99 plus timeouts, errors, retries, and
fallbacks. A slow turn may be caused by endpointing, network, tool latency, or
orchestration rather than model generation alone.

Do not log sensitive audio or transcripts into this public repository. Apply retention,
redaction, access-control, and tenant-isolation requirements in any real environment.

## Core release metrics

| Metric | What it answers |
|---|---|
| Task / episode completion | Did the caller's goal actually finish? |
| Required-tool invocation rate | Did the agent call the tool when required? |
| Incorrect or unnecessary tool-call rate | Did it mutate state when it should not? |
| Tool argument correctness | Were entity, date/time, and other arguments correct? |
| False-confirmation rate | Did it claim an action succeeded when the source system did not confirm it? |
| Clarification / escalation precision and recall | Did it ask or hand off when appropriate, without doing so for everything? |
| State and recovery correctness | Did it handle corrections, errors, and retries without losing state or duplicating a mutation? |
| Audio interaction failures | Did it cut off the caller, miss short turns, overlap, or produce unacceptable silence? |
| Latency distributions | What do typical and tail users experience? |
| Cost and fallback rate | What does reliability cost at real workload volume? |

Segment results by intent, audio condition, turn length, call phase, and other approved
slices. Track high-cost safety and false-confirmation failures separately instead of
letting aggregate accuracy wash them out.

## Regression and production feedback loop

Maintain three sets:

- **Regression suite:** previously observed failures and fixed edge cases. Run it for
  every relevant prompt, model, VAD, tool-schema, orchestration, and dependency change.
- **Rolling discovery set:** newly observed failures and near misses, reproduced and
  reviewed before becoming permanent test cases.
- **Holdout set:** examples not used to tune prompts or thresholds; run periodically to
  detect overfitting.

For each regression, record the symptom, trace-based root cause, expected behavior, and
the stage responsible. Change one major factor at a time, rerun the fixed suite, and
check both improvements and regressions. Compare model versions on the same frozen
corpus and runtime configuration; a newer model is not automatically a more reliable
model.

Before a live canary, agree on acceptance thresholds, rollback triggers, fallback
behavior, and who owns incidents. Shadow evaluation may record proposed decisions, but
must not change live routing or perform side effects.

## Example test: reschedule without false confirmation

**Scenario:** caller says, “Move my appointment to Friday afternoon,” then corrects
the date, and the scheduling tool times out once.

Expected behavior:

1. The agent identifies rescheduling intent, but does not assume which Friday or an
   available time if required details are missing.
2. It asks a focused clarification where needed.
3. The orchestrator validates identity and workflow preconditions and checks authoritative
   availability.
4. A timeout is handled within a bounded retry policy with idempotency protection.
5. The corrected request is the one reflected in the final workflow state.
6. The agent confirms the change only after an authoritative success result.
7. The trace shows the turn boundary, tool attempt(s), timeout, retry decision, and final
   state; the regression grader detects duplicate changes or a false confirmation.

Add variants for “don't reschedule,” “Friday—actually Saturday,” a short “yeah,” barge-in
during the agent's response, and an unavailable slot.

## Adoption checklist

- [ ] Freeze a small human-reviewed gold set and record its version.
- [ ] Make single-turn tool selection and arguments deterministic and repeatable.
- [ ] Test clean TTS and realistic saved audio separately.
- [ ] Add multi-turn corrections, tool failures, and duplicate-action tests.
- [ ] Combine deterministic, LLM, audio, and human graders.
- [ ] Trace each stage and report segment plus end-to-end p50/p95/p99 latency.
- [ ] Track task completion, tool correctness, false confirmations, and safety failures.
- [ ] Keep regression, rolling discovery, and holdout sets separate.
- [ ] Define canary thresholds, fallback, and rollback before changing live traffic.

## References

- [OpenAI Cookbook: Realtime Eval Guide notebook](https://github.com/openai/openai-cookbook/blob/main/examples/Realtime_eval_guide.ipynb)
- [OpenAI Cookbook: Realtime eval harness implementations](https://github.com/openai/openai-cookbook/tree/main/examples/evals/realtime_evals)
- [OpenAI Realtime server events](https://platform.openai.com/docs/api-reference/realtime-server-events)
- [Jev call-intent classification guide](jev-call-intent-classification.md) — intent quality and low-latency routing as one component of the wider voice-agent evaluation.
