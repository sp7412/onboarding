# Reading Guide: ranked by priority

A curated list of blogs, docs, papers and talks for onboarding onto ServiceTitan's
voice-agent work, **ranked in the order to consume them**. Each entry has a time estimate,
why it's on the list, four things to look for while you read or watch, and the lab it
pairs with.

- **Tier 1** (before day 1, must-do): the business, and the core mental models
- **Tier 2** (before day 1 if possible): the stack in depth
- **Tier 3** (first 30 days): orchestration and evaluation depth
- **Tier 4** (as needed): research and background

All links were checked on Oct 3, 2026. Vendor docs change fast, so if a link moves,
search for the title. The takeaways are prompts for your own reading, not summaries to
replace it. Check items off (`- [x]`) as you finish them.

---

## Tier 1: Must-do before day 1

### 0. Voice Agents from First Principles — four-episode explainer series
- [ ] Episode 1, Anatomy of one call: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-01-anatomy-1080p.mp4> · video · 3 min
- [ ] Episode 2, Turn-taking: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-02-turn-taking-1080p.mp4> · video · 4 min
- [ ] Episode 3, Choosing an architecture: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-03-architecture-1080p.mp4> · video · 4 min
- [ ] Episode 4, The control plane: <https://github.com/sp7412/onboarding/releases/download/explainer-series/voice-agents-04-control-plane-1080p.mp4> · video · 4 min
- **Why:** A compact visual starting point for tracing one call, understanding turn-taking, choosing an architecture, and locating the application's control plane.
- **Look for:**
  1. Which boundary owns each latency segment from caller stop to useful answer.
  2. Why a pause inside a phone number is not necessarily the end of a turn.
  3. What cascaded, speech-to-speech, and full-duplex delegation trade off for a booking call.
  4. Which checks and durable state the application must own regardless of model choice.
- **Pairs with:** labs 01, 02, 03, 07 and 08; [`voice-agents-cheat-sheet.md`](voice-agents-cheat-sheet.md)

### 1. ServiceTitan AI Voice Agent product page
- [ ] <https://www.servicetitan.com/features/pro/virtual-agent> · product page · 15 min
- **Why:** this is the product you're joining. Read it as a spec of what customers were promised.
- **Look for:**
  1. Booking is driven by capacity rules (job type, location, required skills), so the agent is a front end to scheduling logic, not a free-form chatbot.
  2. There's an explicit escalation path to a live CSR when a call falls outside the defined rules. Ask yourself how "outside the rules" is detected.
  3. It works with Contact Center Pro *or* third-party phone systems, which shapes the telephony layer.
  4. Customers review recordings, booking outcomes and metrics, so there's a customer-facing quality loop that your evals should line up with.
- **Pairs with:** lab 02 (tools and guardrails)

### 2. ServiceTitan webinar recap: AI Voice Agents
- [ ] <https://www.servicetitan.com/blog/webinar-recap-ai-voice-agents-call-booking> · blog · 15 min
- **Why:** more detail on the feature set and the configuration knobs contractors control.
- **Look for:**
  1. The call types handled beyond booking: confirmations, capacity-aware rescheduling, membership maintenance visits.
  2. Membership awareness: the agent recognizes valued members. What data has to be in context for that?
  3. Contractors choose which job types the agent may book, per business unit. That's policy living in configuration, not in the prompt.
  4. Which phone systems are supported, and what that implies for the transport layer.
- **Pairs with:** lab 00 (mock backend), lab 06 (workflow)

### 3. Pantheon 2025: Atlas and the AI strategy
- [ ] Press release: <https://www.servicetitan.com/press/servicetitan-introducing-the-next-evolution-of-ai-at-pantheon-2025-keynote> · 10 min
- [ ] Keynote recap: <https://www.servicetitan.com/blog/pantheon-2025-vahe-keynote-atlas> · 10 min
- **Why:** where voice agents sit in the company's broader AI bet.
- **Look for:**
  1. Atlas as an assistant that *acts* inside ServiceTitan (reports, finding jobs, dispatch) and how voice booking fits alongside it.
  2. The "first call to final invoice" automation framing. Voice is the first step of that chain.
  3. The Max program: pairing Pro products with expert guidance. Think about what that implies for adoption and support.
  4. The recurring argument that ServiceTitan's data is the moat. Where does your work use that data?
- **Pairs with:** [`notes/glossary.md`](../notes/glossary.md)

### 4. Voice AI & Voice Agents: An Illustrated Primer
- [ ] <https://voiceaiandvoiceagents.com/> · long-form guide · 2–3 h (can be split)
- **Why:** the best single overview of how production voice agents are built, from people who ship them.
- **Look for:**
  1. The latency budget: where every millisecond goes between the caller stopping and hearing a reply.
  2. Turn detection and interruption handling as first-class engineering problems.
  3. Cascaded (STT → LLM → TTS) vs speech-to-speech trade-offs, and when each wins.
  4. How function calling, scripting and evals change when the interface is voice.
- **Pairs with:** labs 01 and 03

### 5. Building Effective Voice Agents (OpenAI, AI Engineer World's Fair 2025)
- [ ] <https://www.youtube.com/watch?v=-OXiljTJxQU> · talk · 20 min
- **Why:** OpenAI solution architects on what works in customer deployments.
- **Look for:**
  1. The chained vs speech-to-speech decision framed around accuracy, determinism, latency and telephony.
  2. Delegation: a fast voice model hands hard reasoning to a stronger model (compare the talker/thinker pattern in lab 08).
  3. Keeping tool sets small and constrained, plus agent handoffs.
  4. Their view on evaluation and observability for voice.
- **Pairs with:** labs 02 and 08

### 6. Your AI Product Needs Evals (Hamel Husain)
- [ ] <https://hamel.dev/blog/posts/evals/> · blog · 45 min
- **Why:** evaluation is where you'll likely create the most leverage. This is the canonical practical guide.
- **Look for:**
  1. The three levels: unit-test-style assertions, human and model evaluation, and A/B testing.
  2. Looking at your data (traces) as the highest-value activity, and how rarely teams do it.
  3. Building evals from real failure cases rather than generic benchmarks.
  4. How the eval loop speeds up every other improvement.
- **Pairs with:** lab 07

### 7. Advancing voice intelligence with new models in the API (OpenAI, May 2026)
- [ ] <https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/> · announcement · 15 min
- **Why:** introduces `gpt-realtime-2`, the model the labs target. Note that `gpt-realtime-2.1` and `2.1-mini` followed in July 2026 with lower latency, so check which one the team uses.
- **Look for:**
  1. Configurable reasoning effort, and what that does to time-to-first-audio.
  2. Spoken preambles ("let me check that") while tools run.
  3. The larger context window: what it enables for long calls, and what it doesn't fix (state still belongs in the app).
  4. The companion models (streaming transcription, live translation) and where they'd fit in a contractor's call center.
- **Pairs with:** lab 01 §3; background: [`speech-to-speech-models.md`](speech-to-speech-models.md)

### 7A. GPT-Live-1: full-duplex voice with delegation (OpenAI, September 2026)
- [ ] Launch post: <https://openai.com/index/introducing-gpt-live-1-in-the-api/> · announcement · 10 min
- [ ] Getting started guide: <https://developers.openai.com/api/docs/guides/live> · docs · 15 min
- [ ] Delegation and tools: <https://developers.openai.com/api/docs/guides/live-delegation> · docs · 30 min
- [ ] Repo explainer: [GPT-Live-1](gpt-live-1.md) · guide · 15 min
- **Why:** likely the "GPT Live" the team suggested. It's OpenAI's newest voice model, and its delegation design is the talker/thinker pattern from lab 08 made into a product.
- **Look for:**
  1. What full duplex changes about interruptions, backchannels and noise compared with turn-based Realtime models.
  2. The split between the live model (conversation) and the backend (reasoning, tools), and when to choose Responses vs client delegation.
  3. The three ways to send information back (instructions, thinking, commentary), and which one is safe to use before a booking is committed.
  4. Pricing (per minute, plus backend usage) and concurrency limits, and what they mean for peak call days.
- **Pairs with:** labs 02, 07 and 08

### 8. OpenAI voice agents guide
- [ ] <https://developers.openai.com/api/docs/guides/voice-agents> · docs · 30 min
- **Why:** OpenAI's reference architecture for voice agents.
- **Look for:**
  1. When they recommend speech-to-speech vs a chained pipeline.
  2. How the Agents SDK structures voice agents, tools and handoffs.
  3. Where they put guardrails.
  4. Anything that contradicts or sharpens your lab 08 study-question table.
- **Pairs with:** labs 02 and 04

---

## Tier 2: The stack in depth (before day 1 if possible)

### Official documentation quick reference

Use these official pages for API behavior and pair them with the labs. The linked pages
were checked during the repository update where the vendor site allowed automated access.
OpenAI's documentation returned an automated-access 403 to the checker but the URLs are
official; vendor documentation can move, so search for the page title if a link moves.

| Read | Why | Time | Pair with |
|---|---|---:|---|
| [OpenAI Realtime overview](https://developers.openai.com/api/docs/guides/realtime) | Session model, audio turns, streaming, and tool calling | 30 min | Lab 01 |
| [OpenAI Realtime reference](https://platform.openai.com/docs/api-reference/realtime) | Raw client/server event names and fields | 30 min | Labs 01–02 |
| [LiveKit Agents overview](https://docs.livekit.io/agents/) | Agent sessions, workers, tools, and voice pipeline | 30 min | Lab 04 |
| [LiveKit turn handling](https://docs.livekit.io/agents/logic/turns/) | VAD, endpointing, interruptions, and semantic turn detection | 25 min | Lab 03 |
| [LiveKit telephony](https://docs.livekit.io/telephony/) | SIP concepts and call transport boundaries | 20 min | Lab 04, optional |
| [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) | `create_agent`, tools, middleware, and model/tool loops | 35 min | Lab 05 |
| [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Explicit stateful workflows and durable execution | 25 min | Lab 06 |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Checkpoints, threads, and resume behavior | 20 min | Lab 06 |
| [LangSmith observability](https://docs.langchain.com/langsmith/observability) | Traces, runs, metadata, and debugging | 25 min | Lab 07 |
| [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation) | Datasets, evaluators, experiments, and online evaluation | 30 min | Labs 07–08 |

For each page, write down three boundaries: what mechanism the vendor provides, what
state or policy remains the application's responsibility, and which event, metric, or
failure would prove your understanding. Do not copy vendor examples containing real
credentials, customer information, or live audio into this public repository.

### 9. Building Effective Agents (Anthropic)
- [ ] <https://www.anthropic.com/engineering/building-effective-agents> · essay · 30 min
- **Why:** the clearest framework for *how much* agency to give an LLM, which is central to voice-agent design.
- **Look for:**
  1. The distinction between workflows (predefined code paths) and agents (model-directed).
  2. "Start simple": add complexity only when it measurably helps.
  3. The patterns (routing, prompt chaining, orchestrator-workers, evaluator-optimizer) and which ones a booking call needs.
  4. Tool design as an interface you engineer carefully.
- **Pairs with:** labs 05 and 06

### 10. Designing Voice Agents for Real Conversations (AWS, AI Engineer World's Fair 2026)
- [ ] <https://www.youtube.com/watch?v=hMlLw1LeIK8> · talk · 30 min
- **Why:** a focused, practical session on turn-taking, the knob callers feel most.
- **Look for:**
  1. Three turn-detection approaches compared: VAD silence, provider endpointing, and a local end-of-turn classifier layered on VAD.
  2. Why turn-taking is an audio-engineering problem, not an LLM problem.
  3. How interruption cancellation works in a streaming pipeline.
  4. The production latency components they break out, compared with your lab 08 table.
- **Pairs with:** lab 03

### 11. LiveKit Agents docs: Turns overview
- [ ] <https://docs.livekit.io/agents/logic/turns/> · docs · 30 min
- [ ] Framework home: <https://docs.livekit.io/agents/> · skim 20 min
- **Why:** the exact configuration surface for endpointing and interruptions.
- **Look for:**
  1. Endpointing delay settings and how semantic turn detection extends them.
  2. Interruption modes, minimum duration and word thresholds, and false-interruption resume.
  3. Which settings are ignored when a realtime model does its own turn detection.
  4. Preemptive generation: starting the LLM before the turn is final.
- **Pairs with:** labs 03 and 04

### 11A. LiveKit 101: Build Production-Ready Voice AI Agents
- [ ] <https://www.youtube.com/playlist?list=PLWx-Xa8RhJxXuv8fu2Qz9rj2MPb4qgXir> · official video course playlist · 2–4 h (sample first, then choose modules)
- **Why:** a practical, official LiveKit course that connects agent sessions, turn handling, tools, handoffs, deployment, and production concerns. Treat it as a multi-video course, not one talk.
- **Look for:**
  1. Which responsibilities belong to the transport/session framework versus application code.
  2. How the examples handle interruptions, tools, state, and human handoffs.
  3. Which deployment and observability concerns appear before production.
  4. What differs from the deterministic `stlab` simulators and the raw Realtime protocol in labs 01–04.
- **Pairs with:** labs 03–04 and [`docs/voice-agent-architecture.md`](voice-agent-architecture.md)

### 11B. Voice Agent Pipeline Explained: VAD, STT, LLM & TTS (LiveKit 101, video 2)
- [ ] <https://www.youtube.com/watch?v=SPB2T-eLrOg> · video · watch before lab 03
- **Why:** the one video from the LiveKit 101 course to watch first. It walks through the exact pipeline labs 03 and 04 build on, so the labs make more sense with it fresh in mind.
- **Look for:**
  1. What each stage (voice activity detection, speech-to-text, LLM, text-to-speech) is responsible for, and what it hands to the next.
  2. Where latency accumulates across the stages, and which stages can overlap or stream.
  3. How the pipeline decides the caller has finished speaking, and how interruptions are handled.
  4. Which parts are framework configuration versus application logic, which is the study question in miniature.
- **Pairs with:** lab 03 (turn-taking) and lab 04 (LiveKit agents); podcast episode 10 covers the full playlist

### 11C. LiveKit 101 bonus videos
- [ ] Fix AI Voice Interruptions with Semantic Turn Detection: <https://www.youtube.com/watch?v=XbrlOY4Z-Ow> · video · 15 min
- [ ] Deploy Voice AI Agents to Production with Full Observability: <https://www.youtube.com/watch?v=KENbu2e7myY> · video · 18 min
- [ ] Production Voice AI Workflows: Consent and Escalations: <https://www.youtube.com/watch?v=bc9kI5TRhX4> · video · 13 min
- [ ] Connect Voice Agents to External Services with MCP: <https://www.youtube.com/watch?v=lOACxaBLwSI> · video · 15 min
- **Why:** these modules extend the pipeline lesson into the production concerns most relevant to a booking agent.
- **Look for:**
  1. How semantic turn detection reduces premature cutoffs and false interruptions.
  2. Which traces, metrics, and failure signals matter once an agent is deployed.
  3. Where consent, escalation, and human handoff belong in the workflow.
  4. What MCP adds at the integration boundary, and which authorization checks remain application-owned.
- **Pairs with:** labs 03, 04, 07, and 08

### 12. Using a transformer to improve end-of-turn detection (LiveKit)
- [ ] <https://livekit.com/blog/using-a-transformer-to-improve-end-of-turn-detection> · blog · 15 min
- **Why:** the design behind LiveKit's semantic turn detector, and a nice small-model ML problem.
- **Look for:**
  1. Why VAD silence alone cuts callers off mid-thought.
  2. Using transcript context to predict end-of-utterance.
  3. The model-size and latency constraints (it must run fast on CPU).
  4. How they measured improvement. Think about how you'd evaluate it on trades calls (addresses, phone numbers, model numbers).
- **Pairs with:** lab 03 §3

### 13. OpenAI Realtime API guide
- [ ] <https://platform.openai.com/docs/guides/realtime> · docs · 45 min
- **Why:** the protocol you learned in lab 01, straight from the source.
- **Look for:**
  1. Session configuration: instructions, tools, voice and turn detection.
  2. The client and server event lifecycle, especially `response.done` and function calls.
  3. Interruption handling and conversation truncation.
  4. WebRTC vs WebSocket vs SIP connection options, and when each fits.
- **Pairs with:** lab 01

### 14. Realtime prompting guide (OpenAI Cookbook)
- [ ] <https://developers.openai.com/cookbook/examples/realtime_prompting_guide> · guide · 30 min
- **Why:** prompting a voice model differs from prompting a chat model.
- **Look for:**
  1. How they structure system prompts into sections.
  2. Controlling pacing, verbosity and tone for spoken output.
  3. Handling unclear audio and alphanumerics (phone numbers, addresses).
  4. Conversation flow and state described in the prompt vs enforced in code. Where would you draw that line?
- **Pairs with:** lab 02

### 14A. LangSmith in video: tracing, runs and evaluation (LangChain)
- [ ] What Is LangSmith? Explained in 5 Minutes: <https://www.youtube.com/watch?v=kYtnLaJeia8> · video · 5 min
- [ ] Getting Started with LangSmith (1/8), Tracing: <https://www.youtube.com/watch?v=fA9b4D8IsPQ> · video · 9 min
- [ ] Getting Started with LangSmith (2/8), Types of Runs: <https://www.youtube.com/watch?v=WplpUxEyl9o> · video · 10 min
- [ ] Getting Started with LangSmith (5/8), Datasets & Evaluations: <https://www.youtube.com/watch?v=iEgjJyk3aTw> · video · 13 min
- [ ] Getting Started with LangSmith (7/8), Automations & Online Evaluation: <https://www.youtube.com/watch?v=z69cBXTJFZ0> · video · 6 min
- [ ] Optional (3/8), Debugging with Studio: <https://www.youtube.com/watch?v=NJXu-4nDo50> · video · 10 min
- [ ] Optional (4/8), Playground & Prompts: <https://www.youtube.com/watch?v=h4f6bIWGkog> · video · 8 min
- [ ] Optional (6/8), Annotation Queues: <https://www.youtube.com/watch?v=rxKYHA-2KS0> · video · 5 min
- [ ] Optional (8/8), Dashboards: <https://www.youtube.com/watch?v=VxsIvf9NdxI> · video · 7 min
- **When:** the first five (about 45 minutes) before lab 07; the optional four anytime after.
- **Why:** LangChain's official walkthrough of the tool. Lab 07 instruments a voice loop by hand; these videos show what the same traces, runs and experiments look like in the LangSmith UI.
- **Look for:**
  1. How a trace breaks down into runs (LLM, tool, chain), and what metadata and tags you can attach. Compare with the call ID and version tags in lab 07 §1.
  2. Where latency, token usage, errors and inputs/outputs appear for each run, and how you'd find the slowest step of one phone call.
  3. How datasets, evaluators and experiments fit together, and how that maps to lab 07 §5's offline evaluation.
  4. What online evaluation and automations add in production, such as sampling live traces, scoring them and routing bad ones to review. That's lab 07 §6's failure-to-regression loop.
- **Pairs with:** lab 07 (and lab 08 for end-to-end traces)

### 14B. Questions for our first 1:1 (Lara Hogan)
- [ ] <https://larahogan.me/blog/first-one-on-one-questions/> · essay · 10 min
- **Why:** the questions a good manager asks a new report, from the manager's side.
- **Look for:**
  1. Which questions you can answer ahead of time in your "working with me" doc.
  2. How a manager uses these answers later: for feedback, recognition and support.
  3. The feedback and recognition preferences you should state explicitly.
  4. Which questions you'd want to ask your manager back.
- **Pairs with:** [Setting goals with your new manager](manager-alignment.md)

### 14C. Get your work recognized: write a brag document (Julia Evans)
- [ ] <https://jvns.ca/blog/brag-documents/> · essay · 15 min
- **Why:** a running record of your work is how good work gets seen in reviews, especially with a new manager.
- **Look for:**
  1. What to include beyond shipped work: glue work, help given, learning.
  2. How to describe impact, not just activity.
  3. When to share it: before check-ins, reviews and manager changes.
  4. How a regular cadence keeps it from becoming a once-a-year scramble.
- **Pairs with:** the [brag document template](../templates/brag-document.md)

### 14D. Staying aligned with authority (Will Larson, StaffEng)
- [ ] <https://staffeng.com/guides/staying-aligned-with-authority/> · essay · 20 min
- **Why:** how senior engineers keep their influence by staying aligned with the people who sponsor their work.
- **Look for:**
  1. Why a senior engineer's authority is lent by a sponsor, usually the manager.
  2. Habits for predicting what your manager would want when they're not in the room.
  3. How disagreement works without losing alignment.
  4. Signs you're drifting out of alignment, and how to recover.
- **Pairs with:** [Setting goals with your new manager](manager-alignment.md)

### 14E. Work on what matters (Will Larson, StaffEng)
- [ ] <https://staffeng.com/guides/work-on-what-matters/> · essay · 20 min
- **Why:** choosing work, and pacing yourself, as expectations rise faster than your available time.
- **Look for:**
  1. How to tell high-leverage work from work that only looks important.
  2. Why pacing yourself is part of doing senior work well.
  3. Which kinds of work are commonly underinvested in, and worth volunteering for.
  4. How to use this when choosing your first win with your manager.
- **Pairs with:** the [first 90 days playbook](first-90-days-playbook.md)

### 14F. When your manager isn't supporting you, build a Voltron (Lara Hogan)
- [ ] <https://larahogan.me/blog/manager-voltron/> · essay · 10 min
- **Why:** no single manager can give every kind of support; build a crew on purpose from the start.
- **Look for:**
  1. The different kinds of support no single manager can provide.
  2. Where to find each: mentors, peers, sponsors, coaches.
  3. How to ask for help without making it transactional.
  4. Which gaps to fill first in a new job.
- **Pairs with:** "Build your support crew" in [Setting goals with your new manager](manager-alignment.md)

---

## Tier 3: First 30 days

### 15. A Field Guide to Rapidly Improving AI Products (Hamel Husain)
- [ ] <https://hamel.dev/blog/posts/field-guide/> · blog · 45 min
- **Look for:**
  1. Error analysis as the core loop: read traces, categorize failures, fix the biggest bucket.
  2. Building simple custom data viewers. Compare the call-replay debugger idea.
  3. Empowering domain experts (CSRs, contractors) to write and judge examples.
  4. Measuring progress with experiments, not features shipped.
- **Pairs with:** lab 07

### 16. τ-bench: tool-agent-user interaction in real-world domains
- [ ] <https://arxiv.org/abs/2406.12045> · paper · 1 h
- **Why:** the benchmark design closest to customer-service booking agents.
- **Look for:**
  1. Evaluating by the final database state rather than the transcript.
  2. Domain policies the agent must follow, and how violations are counted.
  3. The pass^k metric: reliability across repeated trials, not just single-run success.
  4. How the simulated user is built, and how you'd adapt it for trades callers.
- **Pairs with:** lab 07 (scenarios and evaluators)

### 17. τ²-bench: conversational agents in a dual-control environment
- [ ] <https://arxiv.org/abs/2506.07982> · paper · 45 min
- **Look for:**
  1. "Dual control": the user also acts on the environment. Compare a caller who must check a thermostat or breaker while on the call.
  2. How coordinating with the user changes the failure modes.
  3. How the tasks and the user simulator are built.
  4. What the results say about agent reliability when users must take actions.
- **Pairs with:** lab 07

### 18. LangChain and LangGraph 1.0
- [ ] <https://blog.langchain.com/langchain-langgraph-1dot0/> · blog · 15 min
- **Look for:**
  1. `create_agent` as the standard agent loop.
  2. Middleware as the extension point.
  3. The split between LangChain (high level) and LangGraph (runtime).
  4. Stability and versioning commitments. Relevant if the team pins versions.
- **Pairs with:** lab 05

### 19. LangChain middleware docs
- [ ] <https://docs.langchain.com/oss/python/langchain/middleware> · docs · 30 min
- **Look for:**
  1. Hook points: before and after the model, and wrapping model and tool calls.
  2. Built-ins: summarization, PII, human-in-the-loop, call limits, fallbacks.
  3. Changing the tool set or model per request.
  4. Which control-plane rules from lab 02 you'd implement as middleware, and which you wouldn't.
- **Pairs with:** lab 05 §4

### 20. LangGraph: durable execution and interrupts
- [ ] <https://docs.langchain.com/oss/python/langgraph/durable-execution> · docs · 20 min
- [ ] <https://docs.langchain.com/oss/python/langgraph/interrupts> · docs · 20 min
- **Look for:**
  1. Checkpointers and what "durable" guarantees.
  2. The re-execution rule when resuming after an interrupt.
  3. Determinism and idempotency requirements for side effects.
  4. Human-in-the-loop patterns, e.g. CSR approval.
- **Pairs with:** lab 06 §§5–6

### 21. LangSmith evaluation and observability concepts
- [ ] <https://docs.langchain.com/langsmith/evaluation-concepts> · docs · 30 min
- [ ] <https://docs.langchain.com/langsmith/observability-concepts> · docs · 20 min
- **Look for:**
  1. Datasets, experiments and evaluators, and how they map to lab 07.
  2. Offline vs online evaluation.
  3. Traces, runs and threads. How would one phone call map onto them?
  4. Feedback and annotation queues: the path from a production failure to a regression test.
- **Pairs with:** lab 07

### 22. Using LLM-as-a-Judge (Hamel Husain)
- [ ] <https://hamel.dev/blog/posts/llm-judge/> · blog · 45 min
- **Look for:**
  1. Starting from a domain expert's pass/fail judgments with written critiques.
  2. Iterating the judge prompt until it agrees with the expert.
  3. Why binary judgments beat 1–5 scales.
  4. Where you'd need a judge for voice calls (tone, escalation appropriateness) vs where code checks suffice.
- **Pairs with:** lab 07 (`tone_ok`)

### 23. Engineering voice agents: latency, quality, and scale (Together AI)
- [ ] <https://www.youtube.com/watch?v=N7b1PJc7SFc> · talk · 25 min
- **Look for:**
  1. Conversational latency budgets and aggressive transcription targets.
  2. Streaming speech models vs chunked (Whisper-style) transcription.
  3. Colocating models to cut network hops.
  4. Their answers on function-calling evals and classifier-based guardrails.
- **Pairs with:** lab 08 §4

---

## Tier 4: As needed

### 24. Patterns for Building LLM-based Systems & Products (Eugene Yan)
- [ ] <https://eugeneyan.com/writing/llm-patterns/> · essay · 1 h
- **Look for:** evals, guardrails, defensive UX, and collecting user feedback. Which patterns map to a phone channel, where there's no screen?

### 25. Building AI Voice Agents for Production (DeepLearning.AI × LiveKit)
- [ ] <https://www.deeplearning.ai/courses/building-ai-voice-agents-for-production> · course · 1 h
- **Look for:** a guided LiveKit build, latency measurement, and multi-user deployment. Useful if lab 04 felt rushed.

### 26. Moshi: a speech-text foundation model for real-time dialogue
- [ ] <https://arxiv.org/abs/2410.00037> · paper · 1–2 h
- **Look for:** full-duplex modeling (listening while speaking), overlapping speech and backchannels, and why this may eventually replace turn-based pipelines. Good background for where the field is heading.

### 27. Software Is Changing (Again) (Andrej Karpathy)
- [ ] <https://www.youtube.com/watch?v=LCEmiRjPEtQ> · talk · 40 min
- **Look for:** partial-autonomy products, human-verification loops, and the "autonomy slider." A useful frame for how far to let a voice agent go before handing off to a CSR.

---

## After each item
Add one line to your onboarding log: *what changed in my mental model, and which lab or
checklist item it affects.* Update `notes/study-question.md` when something shifts your
answer.
