# Video Notes

## Anatomy of one call
- Video: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-01-anatomy-1080p.mp4> · 3 min · reading-guide item 0
- **Takeaways:**
  1. One answer is a relay across boundaries: VAD and endpointing commit the turn, speech-to-text produces words, the model interprets and may propose a tool call, the application runs it, and text-to-speech plus playout return the answer.
  2. Each stage has a different owner: transport owns media and turn boundaries, the model owns interpretation and proposed language, and the application owns the action.
  3. The caller experiences the sum of endpointing, first model sound, tool round trip, response generation and playout, so measure each segment separately at p50 and p95.
  4. A spoken preamble ("one moment while I check") changes perceived silence; it doesn't make the tool faster.
  5. A useful trace links the caller turn, model event, tool call, backend result and audio response, not just model tokens.
- **Why it matters here:** Analysis: This is the mental model behind labs 01 and 08 and the latency simulation on this site. When a call feels slow, the first question is which boundary added the time.
- **Questions to discuss:**
  1. Which segment of the latency waterfall is largest in the team's production calls, at p50 and at p95?
  2. Where does a single trace connect the audio turn to the backend write today, and where does it break?

## Turn-taking
- Video: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-02-turn-taking-1080p.mp4> · 4 min · reading-guide item 0
- **Takeaways:**
  1. Turn-taking starts with a per-frame speech probability: VAD detects speech, a minimum duration ignores coughs, and a silence timer decides when to close the turn.
  2. Silence inside a thought, like a caller reading a phone number, can trigger a premature cut-off with a timer alone.
  3. Semantic end-of-turn detection asks whether the thought sounds complete; it complements VAD, trading a little decision time for fewer cut-offs.
  4. Backchannels ("uh-huh") and interruptions ("no, the second floor") need different responses, so the agent needs an interruption policy, not just a volume threshold.
  5. After an interruption, truncate history to what the caller actually heard, and measure both failure directions (cut-offs and waiting too long) by utterance type.
- **Why it matters here:** Analysis: This is lab 03's simulator and lab 01 section 4's truncation in one picture. Addresses, phone numbers and model numbers are where a booking agent's turn detection gets tested hardest.
- **Questions to discuss:**
  1. How should uncertainty about whether the caller has finished change what the agent does next?
  2. Which false interruption costs the caller the most in a booking call?

## Choosing an architecture
- Video: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-03-architecture-1080p.mp4> · 4 min · reading-guide item 0
- **Takeaways:**
  1. Cascaded pipelines add hops but keep a text checkpoint you can inspect, filter or tune, and let you swap stages independently.
  2. Native speech-to-speech keeps cues like tone and hesitation and can feel more natural with fewer hops, but it's harder to filter before speaking, and audio tokens can cost more.
  3. Full duplex with delegation listens while speaking and sends reasoning and tools to a backend that returns instructions, thinking or commentary.
  4. Commentary that claims an outcome ("you're booked") must wait until the backend has committed it; progress messages are fine.
  5. The architecture moves where latency and uncertainty live, but authorization, grounded evidence, durable state and evaluation stay with the application.
- **Why it matters here:** Analysis: This connects the speech-to-speech and GPT-Live docs with the build-your-own guide. Whatever the team runs, the control-plane questions are the same.
- **Questions to discuss:**
  1. Which architecture does the team run today, and what drove that choice?
  2. Where would a full-duplex delegation path change the control plane, and where would it stay the same?

## The control plane
- Video: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-04-control-plane-1080p.mp4> · 4 min · reading-guide item 0
- **Takeaways:**
  1. The model proposes and the application decides: identity comes from the transport and verified records, and every state-changing operation is checked against the customer and current call phase.
  2. Confirmations must be grounded: the chosen slot must have been offered, and the caller's own words must support the slot and address; a model paraphrase isn't enough.
  3. Never say "you're booked" before the authoritative write commits; a preamble can say the system is checking, but can't turn intent into fact.
  4. Interruptions during a write are a correctness problem: writes must be idempotent, and the application decides whether to finish or cancel, then reports what actually happened.
  5. Escalation and evaluation are policy too: the model can spot an emergency clue, but the application owns routing; repeat trials gate hard invariants (offered slot, verified customer, grounded address, no emergency booking, idempotent retry) with deterministic checks that no soft quality score can override.
- **Why it matters here:** Analysis: This is the core of labs 02 and 07, the tools-and-guardrails guide, and probably the day-to-day work on the team: deciding what the agent is allowed to do and proving it did it.
- **Questions to discuss:**
  1. Which state-changing actions does the production agent take, and where is each one checked?
  2. How does the team detect a spoken claim that doesn't match the system of record?

## Building Effective Voice Agents
- Video: <https://www.youtube.com/watch?v=-OXiljTJxQU> · 20 min · reading-guide item 5
- **Takeaways:**
  1. The talk focuses on practical patterns for production audio agents.
  2. Speech-to-speech and cascaded approaches trade off latency, control, accuracy, and telephony compatibility rather than having one universally better choice.
  3. Audio agents benefit from a small, well-described tool surface instead of exposing every backend capability to the model.
  4. Deliberate delegation lets a fast conversational model hand difficult reasoning to a stronger model without making every turn slow.
  5. Evaluation and observability must cover audio timing, tool behavior, handoffs, and the final business outcome.
- **Why it matters here:** Analysis: This is the architectural frame for labs 02, 07, and 08. Guardrails decide which actions are legal, delegation controls where reasoning happens, and evaluation checks whether the call produced the right committed state rather than merely fluent text.
- **Questions to discuss:**
  1. Which tasks should stay with the voice model, and which should always be deterministic backend operations?
  2. What evidence would justify delegating a turn: complexity, tool count, latency budget, or a prior failure pattern?

## Designing Voice Agents for Real Conversations
- Video: <https://www.youtube.com/watch?v=hMlLw1LeIK8> · 30 min · reading-guide item 10
- **Takeaways:**
  1. Turn-taking is primarily an audio-engineering problem rather than an LLM problem.
  2. Silence detection, provider endpointing, and learned end-of-turn detection make different assumptions about pauses, partial phrases, and conversational context.
  3. Interruption response speed strongly affects perceived quality because callers notice whether the agent stops and listens immediately.
  4. A detector can fail in both directions: cutting off a caller too early or making the caller wait through an unnecessary timeout.
  5. Turn detection requires an explicit latency and error budget, plus testing against real caller behaviors rather than clean scripted speech.
- **Why it matters here:** Analysis: This gives lab 03 a concrete reason to simulate VAD, endpointing, and barge-in separately. A useful test is whether the system preserves addresses, phone numbers, and restarted phrases while still responding promptly.
- **Questions to discuss:**
  1. Which detector or combination should handle a caller who pauses inside an address, trails off, or interrupts the agent?
  2. Which timestamps should an offline test record to distinguish slow detection from slow cancellation or slow first audio?

## Voice Agent Pipeline Explained: VAD, STT, LLM & TTS
- Video: <https://www.youtube.com/watch?v=SPB2T-eLrOg> · watch before lab 03 · reading-guide item 11B
- **Takeaways:**
  1. Voice agents commonly use VAD, speech-to-text, an LLM, and text-to-speech.
  2. VAD and end-of-turn detection decide what audio becomes a turn, while STT, the LLM, and TTS transform that turn into a response.
  3. Noise handling and endpointing affect both transcript quality and whether the agent responds at the right moment.
  4. Pipeline stages add latency, so streaming and overlap are important; waiting for one stage to finish before starting the next makes the delay visible.
  5. Speech-to-speech models are an alternative to cascaded pipelines, but still need explicit tools, state, policies, and evaluation.
- **Why it matters here:** Analysis: This is the mental model behind labs 03 and 04. It separates framework responsibilities such as audio transport and turn handling from application responsibilities such as booking state, tool authorization, and the definition of a successful call.
- **Questions to discuss:**
  1. Which stages can overlap in the repo's simulators, and which dependencies force them to remain sequential?
  2. Where should latency be measured so a slow STT, model, tool, or TTS stage is distinguishable?

## Fix AI Voice Interruptions with Semantic Turn Detection
- Video: <https://www.youtube.com/watch?v=XbrlOY4Z-Ow> · 15 min · reading-guide item 11C
- **Takeaways:**
  1. VAD alone can mistake pauses or restarts for completed turns.
  2. Semantic turn detection considers whether the utterance expresses a complete thought instead of treating every short silence as completion.
  3. Better turn detection reduces interruptions and provides fuller STT segments, giving downstream reasoning more context.
  4. Semantic detection complements VAD: VAD identifies speech activity while the semantic signal estimates whether the thought is finished.
  5. The production trade-off is a small additional decision cost in exchange for fewer premature cutoffs and retries.
- **Why it matters here:** Analysis: This gives lab 03 a concrete model for reducing premature cutoffs during addresses, phone numbers, and other booking details. It also suggests measuring false end-of-turn decisions separately from overall response latency.
- **Questions to discuss:**
  1. How should the system handle uncertainty about turn completion: wait briefly, ask for confirmation, or begin cancellable preemptive work?
  2. Which false interruptions matter most in booking calls, and how would their cost appear in an eval dataset?

## Deploy Voice AI Agents to Production with Full Observability
- Video: <https://www.youtube.com/watch?v=KENbu2e7myY> · 18 min · reading-guide item 11C
- **Takeaways:**
  1. Important production metrics include time to first audio, time to first token, token use, interruptions, and fallbacks.
  2. Usage collection aggregates measurements across conversation turns and components, so call-level metrics need consistent boundaries and identifiers.
  3. Development logs support detailed debugging, while production dashboards need stable aggregates that reveal regressions without exposing sensitive content.
  4. Preemptive generation can reduce perceived latency by starting work before the turn is final, but that work must be cancellable and must not commit an action prematurely.
  5. Observability is useful when metrics lead to a diagnosis, not when they are just a large list of counters.
- **Why it matters here:** Analysis: The measurements complement lab 08's latency table and turn it into an operational question: can a slow or failed booking be traced from caller turn through model response, tool call, handoff, and final backend result? Offline traces should preserve that causal shape without recording real call data.
- **Questions to discuss:**
  1. Which latency component should be optimized first, and what caller-facing symptom would prove the optimization helped?
  2. How should preemptive generation avoid acting on incomplete intent, stale slots, or a caller interruption?

## Production Voice AI Workflows: Consent and Escalations
- Video: <https://www.youtube.com/watch?v=bc9kI5TRhX4> · 13 min · reading-guide item 11C
- **Takeaways:**
  1. Production agents may need explicit recording consent before proceeding.
  2. Consent collection is modeled as a structured task with a clear boolean outcome rather than an ambiguous conversational impression.
  3. Agents should escalate when they cannot help, when policy requires it, or when the caller requests a person.
  4. A handoff is a workflow transition, not just a sentence announcing transfer; the receiving person needs relevant context and current state.
  5. Declined consent and failed escalation paths need explicit outcomes so the system does not silently continue or strand the caller.
- **Why it matters here:** Analysis: This maps to the guarded tools and workflow-state patterns in labs 02 and 06. Consent, escalation, and handoff state should be represented explicitly before a booking mutation or transfer, with no reliance on implied policy.
- **Questions to discuss:**
  1. Which state must survive a human handoff: caller identity, intent, collected fields, consent result, tool errors, and the next safe action?
  2. What should happen when consent is declined or a live transfer is unavailable, and how should that outcome be evaluated?

## Connect Voice Agents to External Services with MCP
- Video: <https://www.youtube.com/watch?v=lOACxaBLwSI> · 15 min · reading-guide item 11C
- **Takeaways:**
  1. Tools let agents retrieve current information and change external systems.
  2. A function-tool interface exposes a narrow application function to model-directed calls, but the model is not the authority that decides whether the call is permitted.
  3. Tool context can provide session state and interruption-related information without putting the whole backend state into the prompt.
  4. External integrations turn a conversational agent into an action-taking system, so retries, errors, idempotency, and authorization become part of conversation design.
  5. The integration boundary should make failures legible to the agent while keeping committed state and policy in application code.
- **Why it matters here:** Analysis: The integration boundary resembles lab 02's guarded tools and mock backend. The model may propose a booking operation, but ownership checks, offered-slot checks, confirmation grounding, and the committed result must remain outside the model.
- **Questions to discuss:**
  1. Which authorization, ownership, freshness, and idempotency checks must remain outside the model?
  2. How should a tool failure be communicated to the caller, traced for operators, retried safely, and represented in evaluation?

## What Is LangSmith? Explained in 5 Minutes
- Video: <https://www.youtube.com/watch?v=kYtnLaJeia8> · 5 min · reading-guide item 14A
- **Takeaways:**
  1. LangSmith combines tracing, evaluation, prompt work, and monitoring.
  2. Traces expose execution steps, costs, latency, and conversation threads, making a response inspectable rather than a single opaque completion.
  3. Monitoring can combine operational metrics with qualitative evaluators, so a technically healthy call can still be flagged for poor caller experience.
  4. Human corrections can improve evaluator alignment when automated judgments disagree with expert review.
  5. Tracing, evaluation, prompt iteration, and monitoring form a loop: observe a failure, reproduce it, change the system, and verify the change.
- **Why it matters here:** Analysis: This is the conceptual platform model behind lab 07's hand-built instrumentation. The important unit is a debuggable booking interaction whose model turns, tool calls, policy decisions, and outcome can be connected and then evaluated.
- **Questions to discuss:**
  1. What should identify a conversation thread versus an individual call, turn, tool invocation, and retry?
  2. Which qualitative metrics are worth tracking, and how can reviewers distinguish a pleasant answer from a correct and safe one?

## Getting Started with LangSmith (1/8), Tracing
- Video: <https://www.youtube.com/watch?v=fA9b4D8IsPQ> · 9 min · reading-guide item 14A
- **Takeaways:**
  1. LangSmith provides observability and evaluation across application frameworks.
  2. Tracing projects collect application traces for inspection.
  3. A traced application can expose its workflow for debugging.
  4. The example combines web search with an LLM response.
- **Why it matters here:** Analysis: The tracing model gives lab 07 a reference point for representing a phone call as a debuggable sequence of model and tool work.
- **Questions to discuss:**
  1. What should constitute one trace for a phone call?
  2. Which metadata best isolates regressions?

## Getting Started with LangSmith (2/8), Types of Runs
- Video: <https://www.youtube.com/watch?v=WplpUxEyl9o> · 10 min · reading-guide item 14A
- **Takeaways:**
  1. Different run types make LLM application traces easier to interpret.
  2. The video covers model, retriever, tool, chain, prompt, and parser runs as distinct parts of one application execution.
  3. Run types distinguish model calls, data retrieval, external actions, and transformations, which makes a trace useful for both debugging and measurement.
  4. Structured inputs and outputs improve trace rendering and make downstream filtering and evaluation more reliable.
  5. A useful taxonomy should reflect real causal boundaries, not merely mirror whichever SDK wrapper happens to be in use.
- **Why it matters here:** Analysis: A similar trace taxonomy could separate audio, model, tool, and workflow latency in a booking call. It would let lab 07 answer whether a failure came from misunderstood speech, a bad decision, a rejected tool call, or a backend result.
- **Questions to discuss:**
  1. Which run types should represent a complete voice turn, including interruptions and cancelled work?
  2. Which fields are essential for debugging a failed booking without storing unnecessary caller content?

## Getting Started with LangSmith (3/8), Debugging with Studio
- Video: <https://www.youtube.com/watch?v=NJXu-4nDo50> · 10 min · reading-guide item 14A
- **Takeaways:**
  1. Studio provides a visual environment for inspecting LangGraph agents.
  2. A configuration file identifies the graphs available for debugging, making the workflow a named and repeatable artifact.
  3. Different implementations can be run side by side, including buggy or flaky variants, so a failure can be compared against a known-good path.
  4. Visual execution views help locate problematic steps and expose unexpected state transitions.
  5. A visual debugger is most useful when graph state includes the data and policy decision that caused the next transition.
- **Why it matters here:** Analysis: This relates to lab 06's explicit workflow graphs and suggests inspecting booking-state transitions rather than treating the agent as one free-form loop. The debugger should show why a mutation was allowed, blocked, retried, or escalated.
- **Questions to discuss:**
  1. Which graph states and policy facts should be visible in a call debugger?
  2. How should flaky external tools be reproduced while keeping the same scenario replayable?

## Getting Started with LangSmith (4/8), Playground & Prompts
- Video: <https://www.youtube.com/watch?v=h4f6bIWGkog> · 8 min · reading-guide item 14A
- **Takeaways:**
  1. The playground lets developers modify prompts against an existing traced input.
  2. Prompt changes can be compared by their effect on the same traced input instead of relying on memory or anecdotal examples.
  3. Models or providers can be changed during prompt experimentation, which makes the test set and comparison conditions important.
  4. Prompt Hub provides saved and versioned prompts so a successful experiment can become a reproducible artifact.
  5. Prompt iteration should preserve the application logic and regression cases that establish whether a change improved the product.
- **Why it matters here:** Analysis: This suggests a controlled workflow for improving voice prompts while keeping application logic and regression cases visible. For this repo, brevity, confirmation behavior, and safe tool timing should be evaluated alongside naturalness.
- **Questions to discuss:**
  1. Which prompt changes require regression tests, and which failures should block adoption even if the new answer sounds better?
  2. How should spoken brevity be evaluated without rewarding answers that omit necessary confirmation or safety context?

## Getting Started with LangSmith (5/8), Datasets & Evaluations
- Video: <https://www.youtube.com/watch?v=iEgjJyk3aTw> · 13 min · reading-guide item 14A
- **Takeaways:**
  1. Offline evaluation uses datasets and experiments to compare application changes.
  2. Datasets contain inputs and, where available, reference outputs, but voice applications often need structured outcome assertions in addition to text references.
  3. Golden examples represent responses or behaviors an application should emulate and should come from important real failure modes.
  4. Dataset examples can be created manually or imported, then reused to compare experiments over time.
  5. A useful dataset records enough context to reproduce the decision while excluding secrets and unnecessary personal data.
- **Why it matters here:** Analysis: This relates to lab 07's scenarios and offline evaluators, where committed booking outcomes, policy compliance, and escalation behavior matter more than fluent text alone. The scenario set is valuable because it makes those expectations executable.
- **Questions to discuss:**
  1. Which voice-call outcomes need reference outputs, and which are better represented as structured fields or state transitions?
  2. Which assertions should remain code-based because a model judge must never decide them?

## Getting Started with LangSmith (6/8), Annotation Queues
- Video: <https://www.youtube.com/watch?v=rxKYHA-2KS0> · 5 min · reading-guide item 14A
- **Takeaways:**
  1. Annotation queues let developers and subject-matter experts review outputs.
  2. Queues define reviewer instructions, feedback categories, and review counts, turning an informal review request into a repeatable process.
  3. Traces can be added individually or in bulk, which supports focused investigation as well as systematic sampling.
  4. Reservations support coordinated review work and reduce duplicated effort among reviewers.
  5. Reviewer feedback should become a durable failure case or evaluator improvement rather than disappearing after the review session.
- **Why it matters here:** Analysis: This fits the human-review and failure-to-regression loop in lab 07, especially for caller experience, consent, and escalation quality. Human review is the bridge between what the metrics detect and what the product team considers acceptable.
- **Questions to discuss:**
  1. Which voice failures need expert review rather than an automated score?
  2. How should disagreements between reviewers be handled, recorded, and used to improve the rubric?

## Getting Started with LangSmith (7/8), Automations & Online Evaluation
- Video: <https://www.youtube.com/watch?v=z69cBXTJFZ0> · 6 min · reading-guide item 14A
- **Takeaways:**
  1. Automations apply rules to production traces.
  2. Sampling can control the cost of expensive evaluators while rules can ensure high-risk calls are always reviewed.
  3. Online evaluation scores live traces without curated reference outputs, so its criteria must be explicit and monitored for drift.
  4. Automations can route traces to datasets, annotation queues, evaluators, or webhooks, connecting detection to the next corrective action.
  5. A production evaluation policy should balance coverage, privacy, evaluator cost, and the severity of the failure being detected.
- **Why it matters here:** Analysis: This connects lab 07's production failure loop to continuous monitoring of booking calls. The right policy might always inspect rejected mutations and escalations while sampling ordinary successful calls for broader quality signals.
- **Questions to discuss:**
  1. Which calls should always be evaluated because the risk or business impact is high?
  2. Which calls can be sampled, and what evidence would show that the sampling strategy misses an important failure class?

## Getting Started with LangSmith (8/8), Dashboards
- Video: <https://www.youtube.com/watch?v=VxsIvf9NdxI> · 7 min · reading-guide item 14A
- **Takeaways:**
  1. Production dashboards expose usage, latency, errors, token use, cost, and feedback.
  2. Run-type breakdowns help locate slow or failing workflow stages instead of hiding every problem inside one end-to-end average.
  3. Feedback metrics provide a view beyond infrastructure health, including whether callers received useful, safe, and successful assistance.
  4. Dashboards support communication about application performance and cost, but aggregates should link back to representative traces.
  5. A dashboard is most useful when each metric has an owner, a target, and a clear investigation path.
- **Why it matters here:** Analysis: This provides a UI-oriented counterpart to lab 07's trace and evaluation outputs for a phone booking system. A useful dashboard would connect caller-facing latency and outcome rates to the exact turn, tool, policy, or backend stage that needs attention.
- **Questions to discuss:**
  1. Which dashboard metrics represent caller experience: interruption recovery, time to first audio, successful booking, escalation, or something else?
  2. What aggregation hides important individual-call failures, and which trace links are needed to investigate them?

## Engineering Voice Agents: Latency, Quality, and Scale
- Video: <https://www.youtube.com/watch?v=N7b1PJc7SFc> · 25 min · reading-guide item 23
- **Takeaways:**
  1. The talk examines why voice remains important for customer interactions.
  2. It presents a pipeline architecture as a current production approach, with explicit boundaries between speech, reasoning, and response generation.
  3. The system involves trade-offs among component quality, latency, cost, reliability, and scale rather than optimizing a single benchmark.
  4. Bottlenecks can come from any stage or from coordination between stages, so end-to-end measurements matter more than isolated model claims.
  5. It also considers possible next-generation voice architectures without removing the need for application state, policy, and observability.
- **Why it matters here:** Analysis: This complements lab 08's latency and scale analysis and frames architecture choice as a measurable trade-off. The repo's talker/thinker and pipeline comparisons should therefore state which caller experience, safety property, or operating cost each architecture improves.
- **Questions to discuss:**
  1. Which pipeline component is the dominant bottleneck for this repo, and which measurement would prove it?
  2. What improvement in latency, quality, reliability, or operating cost would justify replacing the pipeline architecture?

## Software Is Changing (Again)
- Video: <https://www.youtube.com/watch?v=LCEmiRjPEtQ> · 40 min · reading-guide item 27
- **Takeaways:**
  1. The talk frames AI as changing how software is built and operated.
  2. Neural-network behavior depends more on data and optimization than directly authored rules, which makes behavior harder to inspect from source code alone.
  3. AI applications introduce a different relationship between code, models, prompts, data, and observed behavior.
  4. The speaker presents the field as undergoing rapid change, so teams need experiments and regression evidence rather than assumptions about stable behavior.
  5. The shift does not eliminate traditional software engineering: deterministic boundaries, tests, versioning, and operational ownership remain necessary.
- **Why it matters here:** Analysis: This reinforces treating prompts, datasets, evaluators, and simulations as engineering artifacts alongside code. For a voice agent, the model can be probabilistic while booking policy, backend mutations, and safety-critical checks remain explicit and testable.
- **Questions to discuss:**
  1. Which parts of a voice agent should remain deterministic because an incorrect result has a business or safety cost?
  2. How should changes in model behavior be reviewed when the source code is unchanged but traces, evals, or customer outcomes shift?
