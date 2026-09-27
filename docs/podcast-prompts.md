# Podcast Prompts (NotebookLM Audio Overviews)

Five review episodes generated with Google NotebookLM. Use them for commutes and walks
**after** the matching readings, not instead of them. The hosts are good at concepts and
intuition, weaker on exact API names, config values and numbers. Treat the
[reading guide](reading-guide.md) and labs as the source of truth.

> **Public sources only.** Load only reading-guide links and files from this repo. Once
> employed, don't put ServiceTitan internal material into NotebookLM unless the company
> approves it.

## How to generate an episode
1. Create a **new notebook** for each episode.
2. Add the listed sources: paste URLs, and upload repo files as `.md`.
3. Under **Audio Overview**, choose **Customize**, pick the format and length, and paste the prompt.
4. If the customize box truncates the prompt, trim its last sentence.
5. Listen, then add one line to your onboarding log about what changed in your mental model.

---

## Episode 1: The Business: ServiceTitan, Contractors, and AI Voice Agents
- [ ] Generated · [ ] Listened
- **When:** week of Sept 28, after reading-guide items 1–3
- **Sources:** reading-guide items 1–3; `docs/servicetitan-101.md`; `docs/how-a-contractor-works.md`; `notes/glossary.md`
- **Format / length:** Deep Dive · Default

```text
The listener is a senior ML engineer from the defense industry who starts as a Senior AI Engineer on ServiceTitan's voice-agent team in a few weeks. He knows ML deeply but not the trades industry or SaaS. Explain how a residential HVAC/plumbing contractor runs: the inbound call, booking, capacity, dispatch, memberships, and why missed calls cost revenue. Then explain what ServiceTitan's AI Voice Agents do, how they escalate to human CSRs, and how they fit the Atlas AI strategy. End with 5 questions he should ask his new team. Stick to the sources; don't speculate about internal systems.
```

## Episode 2: Anatomy of a Real-Time Voice Agent
- [ ] Generated · [ ] Listened
- **When:** week of Oct 5, after reading-guide items 4 and 10–12
- **Sources:** reading-guide items 4, 10, 11, 12; `docs/voice-agent-architecture.md`
- **Format / length:** Deep Dive · Longer

```text
Audience: an experienced ML/signal-processing engineer new to production voice agents. Walk through one phone call millisecond by millisecond: audio transport, voice activity detection, endpointing, semantic end-of-turn detection, the model's response, text-to-speech, playout. Spend real time on the tradeoffs: short vs long silence timers, interruptions vs backchannels like "uh-huh", and cascaded STT-LLM-TTS vs speech-to-speech. Use examples like a caller slowly reading a phone number or address. Finish with a simple latency budget he can remember.
```

## Episode 3: The Model vs. The Application: Where the Control Plane Begins
- [ ] Generated · [ ] Listened
- **When:** week of Oct 12, after reading-guide items 5, 7, 8, 13, 14
- **Sources:** reading-guide items 5, 7, 8, 13, 14; `study-guide/voice-agent-study-guide.md`
- **Format / length:** Debate · Default

```text
Frame this around one question: where does the realtime voice model's responsibility stop and the application's control plane begin? One host argues for giving the model more autonomy (reasoning effort, preambles, tool calling); the other argues for enforcing rules in code (tool-boundary validation, grounding confirmations in the actual transcript, idempotent bookings, emergency screening, limiting tools by call phase). Use a home-services booking call as the running example. Converge on practical guidance for a senior engineer designing guardrails.
```

## Episode 4: Agents vs. Workflows: Orchestration with LangChain and LangGraph
- [ ] Generated · [ ] Listened
- **When:** week of Oct 12, after labs 05–06 and reading-guide items 9, 18–20
- **Sources:** reading-guide items 9, 18, 19, 20
- **Format / length:** Deep Dive · Default

```text
Audience: a senior engineer deciding how much agency to give an LLM in a phone-booking system. Contrast model-directed agent loops with deterministic workflows. Explain LangChain create_agent and middleware, then LangGraph state, checkpointers, interrupts, durable execution, and the rule that interrupted nodes re-run on resume (so side effects must be idempotent). Discuss why multi-step agent loops usually sit behind the real-time voice model rather than between the caller and the next spoken word, and the "talker/thinker" pattern.
```

## Episode 5: Evals, Observability, and Winning the First 90 Days
- [ ] Generated · [ ] Listened
- **When:** week of Oct 19, after lab 07 and reading-guide items 6, 15–17, 21–22
- **Sources:** reading-guide items 6, 15, 16, 17, 21, 22; `docs/evaluating-voice-agents.md`; `plan/30-60-90-checklist.md`; `docs/first-90-days-playbook.md`
- **Format / length:** Deep Dive · Longer

```text
Audience: a new Senior AI Engineer whose likely highest-leverage contribution is evaluating voice-agent quality. Cover error analysis on real traces, building eval datasets from failures, code checks vs LLM-as-judge, reliability across repeated trials (pass^k from tau-bench), dual-control scenarios where the caller must act, and tracing with LangSmith. Then connect it to his 30/60/90 plan: how to pick a first project, set a baseline, measure impact, and present wins in contractor outcomes like booked jobs and missed calls. Give concrete, actionable advice.
```
