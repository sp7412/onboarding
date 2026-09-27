# Podcast Prompts (NotebookLM Audio Overviews)

Six technical review episodes and four coaching episodes, generated with Google NotebookLM. Use them for commutes and walks
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

## Episode 10: LiveKit 101 Production Course
- [ ] Generated · [ ] Listened
- **When:** week of Oct 5, after reading-guide item 11A and before or alongside lab 04
- **Sources:** the [LiveKit 101 playlist](https://www.youtube.com/playlist?list=PLWx-Xa8RhJxXuv8fu2Qz9rj2MPb4qgXir); `docs/voice-agent-architecture.md`; labs 03–04
- **Format / length:** Deep Dive · Default

```text
You are coaching an experienced ML and signal-processing engineer through the supplied LiveKit 101 production voice-agent video course. Summarize the playlist as a sequence of architectural decisions, not a feature tour. Explain rooms and participants, agent sessions, VAD and turn detection, interruptions, tools, handoffs, telephony, deployment, and observability. For every topic, distinguish framework mechanism from application-owned policy and state. Compare the course examples with the raw Realtime event protocol and the deterministic simulators in labs 01–04. End with five concrete experiments to run in lab 04 and a short production-readiness checklist. Do not invent private company architecture or claim that a simulator is a real service.
```

---

## Coaching episodes

Career-coaching episodes built from the playbook and checklist. NotebookLM's audio formats are
Deep Dive, Brief, Critique and Debate, so use **Deep Dive** and let the prompt set the coaching style.

### Coaching Episode 6: Entering Well and Learning Fast
- [ ] Generated · [ ] Listened
- **When:** before day one, after reading `docs/first-90-days-playbook.md`
- **Sources:** `docs/first-90-days-playbook.md`; `plan/30-60-90-checklist.md`; `templates/1on1-questions.md`; `templates/onboarding-log.md`
- **Format / length:** Deep Dive · Default

```text
Act as an experienced executive coach for a senior engineer entering a product SaaS company after a long defense-program career. Use only the supplied sources. Help the listener build a first-week operating system: how to align with the manager, create a learning agenda, distinguish observed facts from inferences, build relationships without seeming transactional, and choose a small early win. Explain what to do, what to avoid, and what evidence to collect. End with a 10-minute preparation exercise for the first manager 1:1.
```

### Coaching Episode 7: From Defense Rigor to Product Judgment
- [ ] Generated · [ ] Listened
- **When:** week 1, after reading the SaaS transition section
- **Sources:** `docs/first-90-days-playbook.md`; `docs/servicetitan-101.md`; `docs/how-a-contractor-works.md`; `docs/evaluating-voice-agents.md`
- **Format / length:** Debate · Default

```text
Act as two coaches debating how a rigorous defense-trained ML engineer should adapt to a customer-facing product team. One coach protects the strengths of formal analysis, safety cases, traceability, and edge-case thinking. The other coach pushes for shorter feedback loops, reversible experiments, customer outcomes, pragmatic scope, and comfort with ambiguity. Use the fictional contractor voice-agent workflow as the running example. Do not invent company practices. Converge on five behaviors to keep, five behaviors to change, and three phrases for communicating uncertainty without blocking progress.
```

### Coaching Episode 8: Choosing and Selling the First Win
- [ ] Generated · [ ] Listened
- **When:** end of days 1–30, before the 30-day memo
- **Sources:** `docs/first-90-days-playbook.md`; `plan/30-60-90-checklist.md`; `templates/30-day-memo.md`; `templates/design-doc.md`; `docs/evaluating-voice-agents.md`
- **Format / length:** Deep Dive · Longer

```text
Coach a senior AI engineer through selecting a first project for days 31–60. Compare three fictional options: an evaluation harness, an emergency/OOD escalation guardrail, and a latency reduction. For each, ask what evidence, owner, denominator, baseline, rollout plan, guardrail, and rollback trigger are required. Teach the listener how to avoid choosing the most technically interesting project instead of the most valuable and reversible one. Finish by role-playing a five-minute manager conversation where the engineer proposes one project, states the uncertainty, asks for a decision, and negotiates a measurable definition of success.
```

### Coaching Episode 9: Stakeholders, Feedback, and Difficult Signals
- [ ] Generated · [ ] Listened
- **When:** weeks 3–4, before the day-30 review
- **Sources:** `docs/first-90-days-playbook.md`; `plan/30-60-90-checklist.md`; `templates/1on1-questions.md`; `templates/weekly-status.md`; `docs/call-anatomy.md`
- **Format / length:** Deep Dive · Default

```text
Act as a practical coach preparing a new senior engineer for stakeholder conversations. Use the supplied sources and fictional call scenarios only. Teach how to interview a manager, PM, infrastructure owner, evaluation owner, and support/CSR partner; how to ask questions that reveal ownership and failure costs; how to receive feedback without becoming defensive; and how to handle conflicting requests. Include role-play scenarios: a PM wants speed, an infrastructure owner warns about reliability, and a support partner reports caller frustration. End with a compact weekly update template containing progress, decisions needed, learning, and risks.
```
