# Podcast Prompts (NotebookLM Audio Overviews)

Six technical episodes, three company-and-context episodes built on the
[background whitepaper](whitepaper/README.md), and four coaching episodes. Each episode below is **one
self-contained block**: copy it, then follow the steps. Listen **after** the matching readings,
not instead of them. The hosts are good at concepts, weaker on exact API names, config values and
numbers, so treat the [reading guide](reading-guide.md) and labs as the source of truth.

> **Public sources only.** Every source below is a public URL or a file from this public repo.
> Once employed, don't put ServiceTitan internal material into NotebookLM unless the company
> approves it.

## How to use a block
1. Create a **new notebook** in NotebookLM.
2. **Add source → Website** (or **YouTube** for video links): paste the URLs from the block's
   SOURCES list. You can paste several URLs at once, one per line. Repo files use
   `raw.githubusercontent.com` links so NotebookLM gets clean text.
3. **Audio Overview → Customize:** choose the format and length shown, and paste the block's
   CUSTOMIZE PROMPT.
4. If a site refuses to import (OpenAI's pages sometimes do), open it in your browser,
   **Print → Save as PDF**, and upload the PDF instead.
5. If the customize box truncates the prompt, trim its last sentence.
6. Listen, check the box, and add one line to your onboarding log.

Episodes are listed in **listening order**; numbers match references elsewhere in the repo.

## Optional: create episodes from the command line

`scripts/podcasts_to_nlm.py` reads the blocks below and, for each episode, creates a notebook,
adds its sources and requests the Audio Overview with the block's format, length and prompt,
using the unofficial [`nlm` CLI](https://github.com/jacob-bd/notebooklm-mcp-cli).

```bash
pipx install notebooklm-mcp-cli      # provides `nlm`
nlm login                            # personal Google account only
python scripts/podcasts_to_nlm.py                # dry run: prints every command
python scripts/podcasts_to_nlm.py --run --episodes 1
```

- Consumer NotebookLM has no public API. `nlm` drives its internal interface with your saved
  browser session, so it can break without notice. Use a personal account on a personal
  machine, never a work account or work laptop.
- Sites that block automated imports (OpenAI's pages often do) are reported as failed; save
  those pages as PDFs and add them with `nlm source add <notebook-id> --file page.pdf --wait`.
- Progress is saved in `.nlm-podcasts.json` (gitignored). Reruns reuse each episode's
  notebook, add only missing sources, and retry only the audio request.
- NotebookLM limits how many Audio Overviews an account can generate per day. When the limit
  is hit (`RESOURCE_EXHAUSTED`), the script stops requesting audio; run it again later.

### Put the finished audio in this guide

```bash
gh auth login                                    # once
python scripts/podcasts_to_nlm.py --publish      # download, upload, add Listen links
python scripts/podcasts_to_nlm.py --publish --share   # also link each public notebook
```

`--publish` downloads each finished episode, uploads it to a GitHub release named
`podcasts`, and adds a **Listen:** line under that episode below. The site turns those links
into audio players. Commit and push the updated file to publish them. Release assets in this
public repo are public; the audio is AI-generated from public sources.

---

## Episode 1: The Business: ServiceTitan, Contractors, and AI Voice Agents
- [ ] Generated · [ ] Listened · **When:** Week of Sept 28, after reading-guide items 1–3 and whitepaper chapters 01–03

```text
EPISODE 1: THE BUSINESS: SERVICETITAN, CONTRACTORS, AND AI VOICE AGENTS
Format: Deep Dive · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://www.servicetitan.com/features/pro/virtual-agent
https://www.servicetitan.com/blog/webinar-recap-ai-voice-agents-call-booking
https://www.servicetitan.com/press/servicetitan-introducing-the-next-evolution-of-ai-at-pantheon-2025-keynote
https://www.servicetitan.com/blog/pantheon-2025-vahe-keynote-atlas
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/01-company.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/02-the-trades-industry.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/03-how-a-contractor-works.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/05-pain-points.md
https://raw.githubusercontent.com/sp7412/onboarding/main/notes/glossary.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
The listener is a senior ML engineer from the defense industry who starts as a Senior AI Engineer on ServiceTitan's voice-agent team in a few weeks. He knows ML deeply but not the trades industry or SaaS. Explain how a residential HVAC/plumbing contractor runs: the inbound call, booking, capacity, dispatch, memberships, and why missed calls cost revenue. Then explain what ServiceTitan's AI Voice Agents do, how they escalate to human CSRs, and how they fit the Atlas AI strategy. End with 5 questions he should ask his new team. Stick to the sources.
```

---

## Episode 2: Anatomy of a Real-Time Voice Agent
- [ ] Generated · [ ] Listened · **When:** Week of Oct 5, after reading-guide items 4, 10–12

```text
EPISODE 2: ANATOMY OF A REAL-TIME VOICE AGENT
Format: Deep Dive · Length: Longer

SOURCES (NotebookLM → Add source → Website / YouTube):
https://voiceaiandvoiceagents.com/
https://www.youtube.com/watch?v=hMlLw1LeIK8
https://docs.livekit.io/agents/logic/turns/
https://livekit.com/blog/using-a-transformer-to-improve-end-of-turn-detection
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/voice-agent-architecture.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
Audience: an experienced ML/signal-processing engineer new to production voice agents. Walk through one phone call millisecond by millisecond: audio transport, voice activity detection, endpointing, semantic end-of-turn detection, the model's response, text-to-speech, playout. Spend real time on the tradeoffs: short vs long silence timers, interruptions vs backchannels like "uh-huh", and cascaded STT-LLM-TTS vs speech-to-speech. Use examples like a caller slowly reading a phone number or address. Finish with a simple latency budget he can remember.
```

---

## Episode 10: LiveKit 101 Production Course
- [ ] Generated · [ ] Listened · **When:** Week of Oct 5, alongside lab 04

```text
EPISODE 10: LIVEKIT 101 PRODUCTION COURSE
Format: Deep Dive · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://www.youtube.com/watch?v=Axg9TNZ5038
https://www.youtube.com/watch?v=SPB2T-eLrOg
https://www.youtube.com/watch?v=XbrlOY4Z-Ow
https://www.youtube.com/watch?v=Hj3cZIeB1nc
https://www.youtube.com/watch?v=KENbu2e7myY
https://www.youtube.com/watch?v=lOACxaBLwSI
https://www.youtube.com/watch?v=bc9kI5TRhX4
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/voice-agent-architecture.md
https://raw.githubusercontent.com/sp7412/onboarding/main/labs/src/03_turn_taking_and_interruptions.py
https://raw.githubusercontent.com/sp7412/onboarding/main/labs/src/04_livekit_agents.py

CUSTOMIZE PROMPT (Audio Overview → Customize):
You are coaching an experienced ML and signal-processing engineer through the supplied LiveKit 101 production voice-agent video course. Summarize the playlist as a sequence of architectural decisions, not a feature tour. Explain rooms and participants, agent sessions, VAD and turn detection, interruptions, tools, handoffs, telephony, deployment, and observability. For every topic, distinguish framework mechanism from application-owned policy and state. Compare the course examples with the raw Realtime event protocol and the deterministic simulators in labs 01–04. End with five concrete experiments to run in lab 04 and a short production-readiness checklist.
```

---

## Episode 11: The Company by the Numbers
- [ ] Generated · [ ] Listened · **When:** Week of Oct 5, after whitepaper chapters 01, 06 and 11

```text
EPISODE 11: THE COMPANY BY THE NUMBERS
Format: Deep Dive · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/01-company.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/06-product-landscape.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/11-economics-and-metrics.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/appendix-a-timeline.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
The listener is a senior ML engineer about to join ServiceTitan's AI voice-agent team. Using only the sources, explain how the company makes money and how leadership measures success: gross transaction volume, share of wallet, active customers, net and gross dollar retention, and the Core, FinTech and Pro structure. Walk through the phone products (Phones Pro, Contact Center Pro, AI Virtual Agents) and the AI strategy (Titan Intelligence, Atlas, Max). Keep company-reported results clearly attributed and call out which figures are analysis. End with how a voice-agent engineer should connect their work to these numbers, in contractor terms like booked jobs and recovered revenue.
```

---

## Episode 3: The Model vs. The Application: Where the Control Plane Begins
- [ ] Generated · [ ] Listened · **When:** Week of Oct 12, after reading-guide items 5, 7, 8, 13, 14

```text
EPISODE 3: THE MODEL VS. THE APPLICATION: WHERE THE CONTROL PLANE BEGINS
Format: Debate · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://www.youtube.com/watch?v=-OXiljTJxQU
https://openai.com/index/introducing-gpt-live-1-in-the-api/
https://developers.openai.com/api/docs/guides/live-delegation
https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/
https://developers.openai.com/api/docs/guides/voice-agents
https://developers.openai.com/api/docs/guides/realtime
https://developers.openai.com/cookbook/examples/realtime_prompting_guide
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/voice-agent-architecture.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
Frame this around one question: where does the realtime voice model's responsibility stop and the application's control plane begin? One host argues for giving the model more autonomy (reasoning effort, preambles, tool calling); the other argues for enforcing rules in code (tool-boundary validation, grounding confirmations in the actual transcript, idempotent bookings, emergency screening, limiting tools by call phase). Include GPT-Live-1's design, where a full-duplex voice model delegates reasoning and tools to a backend, as a third option. Use a home-services booking call as the running example. Converge on practical guidance for a senior engineer designing guardrails.
```

---

## Episode 4: Agents vs. Workflows: Orchestration with LangChain and LangGraph
- [ ] Generated · [ ] Listened · **When:** Week of Oct 12, after labs 05–06

```text
EPISODE 4: AGENTS VS. WORKFLOWS: ORCHESTRATION WITH LANGCHAIN AND LANGGRAPH
Format: Deep Dive · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://www.anthropic.com/engineering/building-effective-agents
https://blog.langchain.com/langchain-langgraph-1dot0/
https://docs.langchain.com/oss/python/langchain/middleware
https://docs.langchain.com/oss/python/langgraph/durable-execution
https://docs.langchain.com/oss/python/langgraph/interrupts

CUSTOMIZE PROMPT (Audio Overview → Customize):
Audience: a senior engineer deciding how much agency to give an LLM in a phone-booking system. Contrast model-directed agent loops with deterministic workflows. Explain LangChain create_agent and middleware, then LangGraph state, checkpointers, interrupts, durable execution, and the rule that interrupted nodes re-run on resume (so side effects must be idempotent). Discuss why multi-step agent loops usually sit behind the real-time voice model rather than between the caller and the next spoken word, and the "talker/thinker" pattern.
```

---

## Episode 12: Rules of the Road: Regulation and Risk
- [ ] Generated · [ ] Listened · **When:** Week of Oct 12, after whitepaper chapters 10 and 12

```text
EPISODE 12: RULES OF THE ROAD: REGULATION AND RISK
Format: Debate · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/10-regulation-and-compliance.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/12-risks-and-failure-modes.md
https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf

CUSTOMIZE PROMPT (Audio Overview → Customize):
Stage a debate for a senior engineer building AI phone agents for home-services contractors. One host argues for shipping capabilities fast (outbound reminders, broader automation, fewer handoffs); the other argues for compliance and safety first. Cover the FCC ruling that AI-generated voices are artificial under the TCPA, state call-recording consent, AI disclosure rules like Utah's, business texting registration, payment card data, privacy rights, emergency calls, false confirmations and wrong bookings. Make clear this is general education, not legal advice. Converge on a concrete list of design controls and evaluations that let the team move fast safely.
```

---

## Episode 5: Evals, Observability, and Winning the First 90 Days
- [ ] Generated · [ ] Listened · **When:** Week of Oct 19, after lab 07

```text
EPISODE 5: EVALS, OBSERVABILITY, AND WINNING THE FIRST 90 DAYS
Format: Deep Dive · Length: Longer

SOURCES (NotebookLM → Add source → Website / YouTube):
https://hamel.dev/blog/posts/evals/
https://hamel.dev/blog/posts/field-guide/
https://arxiv.org/pdf/2406.12045
https://arxiv.org/pdf/2506.07982
https://docs.langchain.com/langsmith/evaluation-concepts
https://docs.langchain.com/langsmith/observability-concepts
https://www.youtube.com/watch?v=fA9b4D8IsPQ
https://www.youtube.com/watch?v=iEgjJyk3aTw
https://hamel.dev/blog/posts/llm-judge/
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/evaluating-voice-agents.md
https://raw.githubusercontent.com/sp7412/onboarding/main/plan/30-60-90-checklist.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/first-90-days-playbook.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
Audience: a new Senior AI Engineer whose likely highest-leverage contribution is evaluating voice-agent quality. Cover error analysis on real traces, building eval datasets from failures, code checks vs LLM-as-judge, reliability across repeated trials (pass^k from tau-bench), dual-control scenarios where the caller must act, and tracing with LangSmith. Then connect it to his 30/60/90 plan: how to pick a first project, set a baseline, measure impact, and present wins in contractor outcomes like booked jobs and missed calls. Give concrete, actionable advice.
```

---

## Episode 13: The Competitive Arena and What Comes Next
- [ ] Generated · [ ] Listened · **When:** Week of Oct 19, after whitepaper chapters 07, 09, 13 and 14

```text
EPISODE 13: THE COMPETITIVE ARENA AND WHAT COMES NEXT
Format: Deep Dive · Length: Longer

SOURCES (NotebookLM → Add source → Website / YouTube):
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/07-ai-voice-agents.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/09-competitive-landscape.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/13-future-directions.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/14-implications-and-open-questions.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/pantheon-2026-ai-roadmap.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
Brief a senior ML engineer starting on ServiceTitan's voice-agent team. Using only the sources, explain what AI Virtual Agents do and how they're deployed, who competes (field-service software vendors named in the company's filings and AI-native voice vendors that integrate from outside), and the stated direction toward an Agentic Operating System with Atlas and Max. Keep stated direction separate from hypotheses and don't rank competitors. Then turn to the listener: the leverage areas for an engineer strong in evaluation, out-of-distribution detection and latency, the testable hypotheses to check in the first 60 days, and the best questions to ask each stakeholder.
```

---

## Episode 6: Coaching: Entering Well and Learning Fast
- [ ] Generated · [ ] Listened · **When:** Before day one

```text
EPISODE 6: COACHING: ENTERING WELL AND LEARNING FAST
Format: Deep Dive · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/first-90-days-playbook.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/manager-alignment.md
https://raw.githubusercontent.com/sp7412/onboarding/main/plan/30-60-90-checklist.md
https://raw.githubusercontent.com/sp7412/onboarding/main/templates/1on1-questions.md
https://raw.githubusercontent.com/sp7412/onboarding/main/templates/onboarding-log.md
https://larahogan.me/blog/first-one-on-one-questions/
https://staffeng.com/guides/staying-aligned-with-authority/

CUSTOMIZE PROMPT (Audio Overview → Customize):
Act as an experienced executive coach for a senior engineer entering a product SaaS company after a long defense-program career. Use only the supplied sources. Help the listener build a first-week operating system: how to align with the manager, create a learning agenda, distinguish observed facts from inferences, build relationships without seeming transactional, and choose a small early win. Explain what to do, what to avoid, and what evidence to collect. Cover the pre-mortem, the working-with-me doc, the brag document, day-30 calibration and remote working norms. End with a 10-minute preparation exercise for the first manager 1:1.
```

---

## Episode 7: Coaching: From Defense Rigor to Product Judgment
- [ ] Generated · [ ] Listened · **When:** Week 1

```text
EPISODE 7: COACHING: FROM DEFENSE RIGOR TO PRODUCT JUDGMENT
Format: Debate · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/first-90-days-playbook.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/servicetitan-101.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/how-a-contractor-works.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/evaluating-voice-agents.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
Act as two coaches debating how a rigorous defense-trained ML engineer should adapt to a customer-facing product team. One coach protects the strengths of formal analysis, safety cases, traceability, and edge-case thinking. The other coach pushes for shorter feedback loops, reversible experiments, customer outcomes, pragmatic scope, and comfort with ambiguity. Use the fictional contractor voice-agent workflow as the running example. Converge on five behaviors to keep, five behaviors to change, and three phrases for communicating uncertainty without blocking progress.
```

---

## Episode 8: Coaching: Choosing and Selling the First Win
- [ ] Generated · [ ] Listened · **When:** End of days 1–30, before the 30-day memo

```text
EPISODE 8: COACHING: CHOOSING AND SELLING THE FIRST WIN
Format: Deep Dive · Length: Longer

SOURCES (NotebookLM → Add source → Website / YouTube):
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/first-90-days-playbook.md
https://raw.githubusercontent.com/sp7412/onboarding/main/plan/30-60-90-checklist.md
https://raw.githubusercontent.com/sp7412/onboarding/main/templates/30-day-memo.md
https://raw.githubusercontent.com/sp7412/onboarding/main/templates/design-doc.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/evaluating-voice-agents.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
Coach a senior AI engineer through selecting a first project for days 31–60. Compare three fictional options: an evaluation harness, an emergency/OOD escalation guardrail, and a latency reduction. For each, ask what evidence, owner, denominator, baseline, rollout plan, guardrail, and rollback trigger are required. Teach the listener how to avoid choosing the most technically interesting project instead of the most valuable and reversible one. Finish by role-playing a five-minute manager conversation where the engineer proposes one project, states the uncertainty, asks for a decision, and negotiates a measurable definition of success.
```

---

## Episode 9: Coaching: Stakeholders, Feedback, and Difficult Signals
- [ ] Generated · [ ] Listened · **When:** Weeks 3–4, before the day-30 review

```text
EPISODE 9: COACHING: STAKEHOLDERS, FEEDBACK, AND DIFFICULT SIGNALS
Format: Deep Dive · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/first-90-days-playbook.md
https://raw.githubusercontent.com/sp7412/onboarding/main/plan/30-60-90-checklist.md
https://raw.githubusercontent.com/sp7412/onboarding/main/templates/1on1-questions.md
https://raw.githubusercontent.com/sp7412/onboarding/main/templates/weekly-status.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/call-anatomy.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
Act as a practical coach preparing a new senior engineer for stakeholder conversations. Use the supplied sources and fictional call scenarios only. Teach how to interview a manager, PM, infrastructure owner, evaluation owner, and support/CSR partner; how to ask questions that reveal ownership and failure costs; how to receive feedback without becoming defensive; and how to handle conflicting requests. Include role-play scenarios: a PM wants speed, an infrastructure owner warns about reliability, and a support partner reports caller frustration. End with a compact weekly update template containing progress, decisions needed, learning, and risks.
```
