# Changelog

## 2026-10-17

### TTAN true daily VWAP

- Replaced monthly close/volume VWAP proxy with a one-minute-bar aggregation pipeline and a rolling 63-session VWAP.
- Added daily VWAP and raw closing-price charts with a ten-session inset and stable plot anchors.
- Added Alpaca IEX/SIP configuration instructions, feed-coverage caveats, and unit tests.

## 2026-10-16

### Coding-agent engineering practices

- Integrated eight practical topics into the existing multi-agent workstation chapter: permissions/trust boundaries, definition of done, isolated worktrees and integration, controlled coding-agent benchmarks, harness architecture and recovery, context engineering, structured observability/cost, and dependency/API verification.
- Added task-record templates, least-privilege guidance, an agent state model, sample Git worktree commands, a telemetry schema, and benchmark metrics with hard correctness/safety gates.
- Added official Git, GitHub security, evaluation, OpenTelemetry, and NIST SSDF references. Emphasized measured evidence, reproducibility, redaction, and human acceptance rather than agent self-report.

### Mac task tracking tools

- Added a practical comparison of Apple Reminders, Things 3, Todoist, TickTick, and OmniFocus for personal task management, plus Linear, GitHub Issues/Projects, Asana, and Trello for shared project work.
- Added selection guidance and an AI-assisted engineering task-record checklist covering ownership, worktree/branch, scope, acceptance criteria, tests, and review status.
- Added official/product references and cautions about duplicate backlogs and company-data handling.

### Slack call capture and conversation RAG

- Clarified on-demand MCP retrieval versus custom RAG indexing and hybrid retrieval; added a decision rule, example lookup sequence, and authorization, provenance, and deletion guardrails.
- Added a Slack call-capture comparison covering native Huddle AI notes and external meeting
  note/transcription tools, with explicit compatibility and consent checks.
- Documented authorized Slack exports versus scoped API ingestion and live MCP retrieval.
- Added a Slack-to-RAG pipeline, metadata schema, access-control and deletion requirements,
  and a production-readiness checklist for thread reconstruction, provenance, retrieval quality,
  and governance.

### Knowledge management, Mac productivity, and AI integrations

- Expanded the developer-tools catalog with Obsidian, DEVONthink, Apple Notes, Notion,
  Readwise Reader, and NotebookLM; distinguished personal notes, document archives,
  shared team knowledge, and source-grounded research.
- Added Raycast, Alfred, Keyboard Maestro, BetterTouchTool, and Rectangle as task-oriented
  Mac productivity options, including clipboard/privacy and automation guardrails.
- Documented how MCP connects knowledge stores and applications to Claude Desktop and
  Cursor, with links to official client docs and community Obsidian plugins.
- Added a capture → curate → retrieve → act → review workflow and guidance to start with
  read-only permissions and verify data flows before granting write access.

### Developer workstation tools catalog
### Multi-agent workstation tools

- Expanded the developer-tools catalog with WezTerm, tmux, cmux, ccmux, Zellij, Grok CLI, AnythingLLM, and Grok Bot.
- Distinguished terminal multiplexing from coding-agent orchestration and persistent cloud-agent delegation.
- Added a parallel-agent operating model covering git worktree isolation, task ownership, status visibility, review gates, and cost/safety controls.
- Added a comparison of live coding-agent session monitors and session-history browsers: Agent Sessions, AgentHUD, opensessions, and AgentsView, with guidance on choosing by workflow and checking local-data boundaries.


- Added a curated developer-tools page, starting with MacParakeet, OpenWispr, Apple Dictation, OpenWhispr, Wispr Flow, and Superwhisper.
- Compared hotkey ergonomics, local/cloud processing, platform support, licensing, and workflows; included a repeatable dictation evaluation checklist and a roadmap for future tool categories.
- Linked the page from the topic index, README, and published site's document registry.


### TTAN annual VWAP proxy and raw-price charts

- Replaced the stale selected-date stock chart with a one-year monthly close/volume-weighted proxy and a two-week daily inset.
- Added a separate raw closing-price plot with its own two-week daily inset and stable direct links.
- Explicitly documented that monthly close/volume checkpoints are a long-range proxy, not true daily or intraday VWAP.

### Self-licking ice cream cone: organizational incentives and AI delivery

- Added a source-grounded history of the phrase, a refined NotebookLM prompt, a two-host script, and a neutral AI product-team diagnostic.
- Kept contemporary examples illustrative and distinguished historical claims from the original author's interpretation.

### Evidence-first debugging with coding agents

- Added a practical guide to controls, high-fidelity signals, competing hypotheses,
  contradiction checks, verification, and diagnostic infrastructure improvements.
- Included a fictional voice-agent latency investigation, a compact evidence-record
  example, and guardrails for agent-assisted diagnosis.
- Linked the guide from the topic index, README, ranked reading guide, and bibliography;
  connected it to the existing production-incident exercise.

## 2026-10-15

### Voice-agent test scenario prompts and grading contracts

- Added a “food for thought” section on versioned caller prompts, hidden evaluator
  contracts, initial-state fixtures, fault injection, and reproducible run manifests.
- Included a fictional scheduling example and a starter matrix for task completion,
  ambiguity, audio/turn-taking, tool failures, policy, and adversarial requests.
- Emphasized separate audio conditions, deterministic state assertions, layered metrics,
  and distinct regression/discovery/holdout datasets; framed 20–30 scenarios as a
  practical starting milestone rather than a universal benchmark.

### Production voice-agent benchmark architecture

- Added an end-to-end benchmark and regression architecture diagram covering
  versioned scenarios, audio simulation, production-equivalent agent execution,
  sandbox business APIs, trace collection, deterministic assertions, baseline
  comparison, release gates, canaries, and failure mining.
- Documented CI/nightly/canary evaluation loops, reproducibility manifests, frozen
  regression/discovery/holdout sets, hard safety gates, statistical comparisons, and
  trace-based regression attribution.


### ServiceTitan public GitHub review

- Reviewed the public organization inventory (31 repositories in the captured listing) and added a detailed classification and deep dives on Stl.Fusion, its samples, LazyProxy, Claude Code Action, AzureChatGPT, recording-PWA-proto, and API/schema tooling.
- Distinguished documented repository behavior from engineering inference; explicitly recorded that the reviewed public inventory does not expose a clearly identified production Voice Agent implementation.
- Added source-level findings from Anvil2 examples: Voice Agent settings (Persona, Conversation Flow, Rules, Job Types/Fees, Escalations/Fallbacks), Agent Workflows/Interactions/Calls/Bookings/Call Analytics/Insights, action-log/evidence-disclosure patterns, Atlas UI, and a detailed escalation taxonomy.
- Read the Field Pro Recorder PWA implementation and identified likely chunk-flush/order races, a pagehide listener cleanup issue, missing upload/ASR code, and quota-handling gaps; findings are explicitly untested code-review hypotheses.
- Read the Moltbot/OpenClaw fork's voice-call extension: provider adapters, normalized call lifecycle events, Twilio WebSocket media streams, OpenAI Realtime transcription, TTS queue/barge-in behavior, inbound policy, webhook signature verification, and transcript logging. Classified it as an upstream-derived reference architecture, not ServiceTitan production evidence.
- Read Fusion operation identity/log-reader code to clarify that its AgentId identifies a distributed process/operation origin, not an LLM agent. Read Claude Code Action's executable input contract for prompt-injection, permissions, and secret/log exposure warnings.
- Linked the review from the README, topic-first index, and bibliography; documented scope and limitations so public code is not misrepresented as internal architecture.



### Voice-agent product evidence

- Added a public-source guide to the current Voice Agent workflows: speed-to-lead voice follow-up, technician notifications, parts-arrival booking, and cross-channel flows.
- Documented Voice Intelligence's Early Access status, evidence-backed call analysis, custom scorecards, and rollout caveats.
- Recorded vendor/customer-reported booking metrics with denominator and benchmark caveats; linked the guide from the README, guide index, Max map, business metrics, and bibliography.

### Max capability map and cross-agent workflows

- Added a source-grounded map of publicly named residential, commercial, and planned roofing Max capabilities, with dated rollout caveats and an explicit boundary around undisclosed internals.
- Connected the map from the README, topic-first index, Pantheon roadmap, and orchestration chapter; added the sources to the bibliography.
- Extended Lab 10 with a concurrency/reservation exercise covering stale state, atomic claims, idempotent retries, and approval-gated follow-up actions.

## 2026-10-14

### Jev decision workbench

- Added lab 17, a hands-on notebook for writing typed Jev decisions, defining operational
  intent criteria, comparing a simple offline baseline against reviewed labels, and inspecting
  classification errors.
- Added an opt-in live Jev System One request using the documented HTTP contract; live calls
  are disabled by default and may incur usage charges.
- Added Jev API key loading from Colab Secrets and linked the lab from the notebook index.

## 2026-10-14

### Agent-scale source control

- Added a source-grounded comparison of Anthropic Scion and GitLab next-gen SCM, including background, architecture, trade-offs, maturity caveats, reported metrics, and a workload-based evaluation plan.
- Added the guide to the topic-first index and bibliography; clearly distinguished vendor-reported performance claims from independently verified benchmarks.

## 2026-10-13

### Voice-agent testing and benchmarks

- Added a repeatable stress-test matrix for noise, pauses, interruptions, context
  shifts, and tool/transport faults.
- Linked LiveKit simulations and load testing, VoiceBench, and \u03c4-bench, clarifying
  how test frameworks, research benchmarks, and domain-specific production regression
  suites complement rather than replace one another.


## 2026-10-12

### Guide navigation

- Added a topic-first index that groups the growing document library by task, and linked it from the repository README.
- Added the guide index, Jev intent-classification guide, and Realtime evaluation guide to the published site's field guide so new pages are discoverable there too.


### Realtime voice-agent evaluation

- Added a practical guide adapted from the OpenAI Cookbook Realtime Eval Guide, covering Crawl/Walk/Run evaluation stages, separate task and audio quality, trace-level diagnosis, layered graders, regression/holdout sets, and release gates.
- Added a fictional rescheduling regression that checks corrections, tool timeout recovery, idempotency, authoritative state, and false confirmations.
- Added a sourced section on developer-reported failure patterns: missing required tool calls, VAD/turn-taking problems, out-of-context responses, and operational failures, with regression tests for each. Public reports are explicitly qualified as reports, not universal failure-rate evidence.


### GPT Live + Jev runtime integration

- Added an end-to-end architecture, rescheduling example, conceptual typed-decision
  contract, component responsibility boundaries, and latency/concurrency guidance.
- Emphasized that Jev classifies intent while the orchestrator and authoritative
  scheduling tools retain control of policy, availability, authorization, and commits.


### Low-latency call intent classification

- Added a Jev evaluation guide for typed call-intent decisions, deterministic routing,
  uncertainty handling, separation from bookability, safe fallback, and a measured
  shadow-mode evaluation plan. Vendor latency and API claims are explicitly not treated
  as verified production results.

### GPT-Live backend model routing

- Documented the distinction between GPT-Live's real-time voice role and delegated
  backend reasoning, including configured Responses delegation versus application-side
  routing. Added a cautious Astra/Sol/Luna/Terra routing example integrated with Jev,
  with official model/delegation references and explicit caveats against assuming
  undocumented automatic model switching.

## 2026-10-11

### Full-duplex voice model evaluation

- Added a source-based PersonaPlex-7B vs GPT-Live-1 comparison, corrected the open-source and latency caveats, calculated voice-layer costs and average concurrency for 100,000 monthly calls, and defined a controlled scheduling-agent evaluation plan.

This file records meaningful repository changes so the evolution of the
onboarding material is easy to scan without reading individual pull requests.

## 2026-10-10

### Pantheon public-source refresh

- Refreshed the Pantheon 2026 roadmap through October 10 with additional Day 3 and partner coverage.
- Added attributed notes on partner call experimentation, certified-partner booking, announced webhooks, and customer-reported setup/booking claims; separated public statements from engineering implications.
- Consolidated overlapping partner/customer bullets into existing sections and strengthened caveats so public statements are not treated as implementation facts or benchmarks.

## 2026-10-11

### Plan review

- Reconciled the pre-start table with the Oct 19 checklist (field exercise, After Day One boundary, first-PR decision tree, working hypotheses, podcast episode 14).
- Scheduled lab 16 and the MCP trust-boundary note, and added optional judgment-track exercises to weeks Oct 12, Oct 19, 2 and 3.
- Added a day-one boundary item to week 1 and `**Output:**` lines to weeks 4–13.
- Corrected the README judgment-track exercise count and time (ten, about 6¾ hours).

### Pantheon completeness pass

- Added section 2e to the Pantheon brief covering recaps missing from earlier passes: "Charging Ahead with AI and Max", Atlas's capability list and next-year goals, Homh's ranking signals, planned commercial and roofing Max agents, and the service-agreement and big-ticket-sales breakouts. Updated the update notes, team questions, and "still to watch".
- Recorded the claims in the claims ledger and superseded the October 8 "no recap" rows.
- Added hypothesis-map rows on tenant configuration and Homh ranking integrity, and a ranking-signals section in the Homh doc.

## 2026-10-09

### Podcast tooling

- Added a reusable template and review checklist for short, source-grounded
  NotebookLM episodes, in the same block format as the numbered episodes.

## 2026-10-08

### Consistency audit

- Aligned the root getting-started sequence with lab 15 and repaired a malformed
  Markdown table row in the repository layout.
- Extended the optional capstone evidence rubric to cover LLM-judge validation,
  human agreement, position bias, and calibrated abstention.

### Pantheon and agent architecture

- Added public-source guidance on agentic orchestration, shared context,
  shared skills/capabilities, and running agents in production.
- Added a comparative guide to multi-agent architectures and the control
  surfaces around them.
- Added the **agent harness** model: the model proposes; the harness controls.
- Added a design-by-evaluation workflow covering traces, failure mining,
  regression evaluation, and staged rollout.
- Added MCP and external-agent trust-boundary guidance covering authorization,
  consent, idempotency, injection risks, auditability, and booking state.
- Refreshed the Pantheon 2026 roadmap and claims ledger as new public
  announcements and follow-up coverage became available.
- Turned the Command Center capacity-hold and duplicate-action details into a
  senior-engineer exercise covering atomic reservation, idempotent retries,
  stale recommendations, release/reconciliation, and authoritative state.
- Clarified the public status of ServiceTitan's MCP work: public material
  describes MCP connectivity, while the broader MCP server remains described
  as in development; the repository does not treat it as generally available
  or assume mutating scope.

### First-90-days workflow

- Added a focused first-90-days question bank for a voice-agent team.
- Expanded the repository from a broad study guide toward a practical
  first-90-days operating guide, including manager alignment, field
  observations, architecture questions, and a senior-engineer judgment track.

### Hands-on labs

- Expanded the lab path through multi-agent coordination, Mini-Max,
  earning autonomy, LLM evaluation, and MCP fundamentals.
- Added Codespaces/dev-container and Colab paths for running labs.
- Added the MCP server basics lab with a fictional contractor server,
  tools/resources/prompts, Streamable HTTP, Inspector, trust-boundary
  exercises, and safe mutation design.
- Kept labs offline-safe and based on fictional data; live integrations remain
  optional and must use personal credentials.

### Quality and safety

- Added explicit autonomy-promotion and demotion guidance using statistical
  confidence bounds, minimum sample sizes, cost asymmetry, calibration,
  drift/OOD checks, segmentation, and rollback triggers.
- Added repository guidance for public-safe content and post-Day-One handling
  of company knowledge.
- Added maintenance, source-ledger, and claims-verification practices so
  public claims are distinguishable from inference or fictional exercises.

## 2026-09 and earlier

The repository began as a broad ServiceTitan/voice-agent study workspace and
has progressively been reorganized into a practical onboarding system:

- company and product primer
- canonical 30/60/90 operating plan
- real-time voice-agent architecture and hands-on labs
- production metrics, evaluation, and failure analysis
- multi-agent coordination and agent-to-agent workflows
- earned-autonomy policy and senior-engineer judgment exercises
- public-source references, claims ledger, and reusable onboarding templates

For implementation-level detail, see the individual documents and the Git
history. This changelog intentionally summarizes the repository's evolution
rather than duplicating every commit.


## 2026-10-13

- Added a LiveKit workshop crosswalk to the hands-on track, identified the missing explicit provider-failure/fallback drill, and added measurable latency/outcome, MCP negative-test, and consent/escalation acceptance checks. Documented SDK-version drift and added the workshop modules to the public-source bibliography.
