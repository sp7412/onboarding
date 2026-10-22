# Guide index

A topic-first map of the onboarding material. Use the **learning path** when you want an order; use this index when you need to find a specific answer.

## Start here

- [ServiceTitan 101](servicetitan-101.md) — company, products, and the contractor workflow.
- [10-hour minimum path](minimum-path.md) — the shortest coherent route through the material.
- [30/60/90 checklist](../plan/30-60-90-checklist.md) — the canonical onboarding schedule and progress checklist.
- [Reading guide](reading-guide.md) — ranked external articles, papers, and talks.
- [LiveKit hands-on track](livekit-hands-on.md) — build a guarded scheduling agent.

## Voice-agent architecture and runtime

- [Voice-agent architecture](voice-agent-architecture.md) — component boundaries and control plane.
- [On-device voice agents](on-device-voice-agents.md) — compare embedded local voice stacks with client/server agents; focus on interruption, playback-aware context, and a testable prototype.
- [ServiceTitan voice-agent public evidence](voice-agent-public-evidence.md) — documented workflows, Voice Intelligence, booking figures, and rollout caveats.
- [ServiceTitan public GitHub review](servicetitan-github-review.md) — source-level clues in Voice Agent settings, Atlas/AI Kit, the upstream Moltbot voice-call extension, recording PWA, Fusion, and harness security.
- [Speech-to-speech models](speech-to-speech-models.md) — full-duplex models versus cascaded pipelines.
- [GPT-Live-1](gpt-live-1.md) — model behavior, delegation, and control-plane responsibilities.
- [Build your own voice agent](build-your-own-voice-agent.md) — compare chained and realtime implementations.
- [System One models for production AI](system-one-models.md) — typed decisions, structured extraction, hybrid architectures, and evaluation.
- [Jev call-intent classification](jev-call-intent-classification.md) — low-latency typed intent decisions, routing, fallback, and evaluation.
- [Agent harness](agent-harness.md) — state, memory, RAG, tools, and the side-effect boundary.
- [Tools and guardrails](tools-and-guardrails.md) — safe tool design, authorization, and prompt-injection defenses.
- [Call anatomy](call-anatomy.md) — a booking call broken down by event and turn.
- [Voice-agents cheat sheet](voice-agents-cheat-sheet.md) — concise architecture, latency, and turn-taking reminders.

## Reliability, evaluation, and production

- [Evidence-first debugging](evidence-first-debugging.md) — controls, high-fidelity signals, falsifiable hypotheses, and agent-assisted diagnosis.
- [TTAN daily VWAP data](ttan-vwap-data.md) — intraday VWAP methodology, Alpaca setup, and IEX/SIP feed coverage.
- [Realtime voice-agent evaluation](realtime-voice-agent-evaluation.md) — eval design, layered graders, trace diagnosis, regression sets, and release gates.
- [Evaluating voice agents](evaluating-voice-agents.md) — task success, latency, containment, and quality metrics.
- [Design by evaluation](design-by-evaluation.md) — use failures and evals to shape the architecture.
- [Earning autonomy](earning-autonomy.md) — calibration, drift, evidence thresholds, and safe promotion.
- [Capstone rubric](capstone-rubric.md) — acceptance criteria for the end-to-end workflow.
- [Business metrics](business-metrics.md) — connect call outcomes to bookings, revenue, trust, and operating cost.

## Multi-agent coordination and booking trust

- [Pantheon 2026 AI roadmap](pantheon-2026-ai-roadmap.md) — public roadmap context and implications for voice.
- [Max public capability map](max-capability-map.md) — named capabilities, rollout caveats, and cross-agent workflows grounded in Pantheon disclosures.
- [Call facts contract](call-facts-contract.md) — proposed versus verified facts shared across agents.
- [Homh and AI-agent booking](homh-and-agent-booking.md) — trust boundaries for homeowner-side AI.
- [MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md) — authorization, consent, idempotency, and audit.
- [Comparative agent architectures](comparative-agent-architectures.md) — where orchestration, policy, and evaluation sit across vendors.
- [Pantheon hypothesis map](hypothesis-map.md) — public claims translated into validation questions.

## Developer workstation and tools

- [Developer tools catalog](developer-tools.md) — Mac dictation, AI-assisted coding, operational log diagnostics, observability utilities, and practical tool-selection criteria.
- [Build a personal knowledge base with Grok Bot](grok-bot-knowledge-workflow.md) — step-by-step setup, source connections, Markdown structure, skills, daily/weekly routines, and safety checks.
- [Obsidian personal knowledge workflow](obsidian-personal-knowledge-workflow.md) — local-first Markdown vault, ChatGPT/repository imports, Grok Bot access models, source provenance, and approval-gated maintenance.

## Hands-on learning

- [Lab index](../labs/README.md) — all notebooks, prerequisites, estimated time, and Colab links.
- [Lab environments](lab-environments.md) — Codespaces/dev container versus single-notebook Colab.
- [Senior engineer judgment track](../senior-engineer/README.md) — scenario exercises on architecture, incidents, latency, and autonomy.
- [Solutions](../labs/solutions/) — consult after attempting each exercise.
- [Podcast prompts](podcast-prompts.md) — NotebookLM episode prompts for technical topics and company context.
- [Self-licking ice cream cone](self-licking-ice-cream-cone.md) — sourced history, refined NotebookLM prompt, full two-host script, and an AI-product-team diagnostic.

## First 90 days and working notes

- [First 90 days playbook](first-90-days-playbook.md) — execution companion to the checklist.
- [Manager alignment](manager-alignment.md) — turn early conversations into explicit goals.
- [First-90-days question bank](first-90-days-question-bank.md) — questions organized by role and conversation.
- [Field exercise](field-exercise.md) — a bounded, ethical way to learn how contractors handle calls.
- [After day one](after-day-one.md) — keep company information out of this public repository.
- [Study question](../notes/study-question.md) — the central control-plane question.
- [Conversation notes](../notes/conversation-notes.md) — original motivation and framing.

## Reference

- [Agent-scale source control](agent-scale-source-control.md) — background, architecture, pros/cons, and evaluation plan for Anthropic Scion vs. GitLab next-gen SCM.
- [References and source ledger](references.md) — sources cited throughout the repository.
- [Whitepaper chapters](whitepaper/README.md) — longer-form technical background.
- [Glossary](../notes/glossary.md) — terms and definitions.
- [Changelog](../CHANGELOG.md) — what has changed and why.
- [Templates](../templates/) — reusable blank working documents.

---

**Public-safe rule:** this repository is for personal learning, public sources, fictional examples, and blank templates. Do not add internal architecture, code, metrics, customer data, or call recordings.
