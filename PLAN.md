# Repository Improvement Plan

## Audit Scope

Audited `AGENTS.md`, `README.md`, `plan/`, `study-guide/`, `templates/`, `notes/`,
`labs/README.md`, every `labs/src/*.py`, and every `labs/stlab/*.py`. The original
binary study-guide `.docx` is committed alongside its Markdown source but is not
machine-readable through the repository tools; the Markdown version was audited.

This plan is audit-only. No implementation files have been changed.

## Baseline

The exact requested command was run:

```text
$ python scripts/run_notebooks.py
zsh:1: command not found: python
```

The equivalent command available in this environment was also run:

```text
$ python3 scripts/run_notebooks.py
PASS  00_setup_and_mental_model.ipynb
PASS  01_realtime_protocol.ipynb
PASS  02_realtime_tools_and_guardrails.ipynb
PASS  03_turn_taking_and_interruptions.ipynb
FAIL  04_livekit_agents.ipynb   ModuleNotFoundError: No module named 'livekit'
FAIL  05_langchain_create_agent.ipynb   ModuleNotFoundError: No module named 'langchain_core'
FAIL  06_langgraph_booking_workflow.ipynb   ModuleNotFoundError: No module named 'langgraph'
FAIL  07_langsmith_tracing_evals.ipynb   ModuleNotFoundError: No module named 'langsmith'
FAIL  08_capstone_talker_thinker.ipynb   ModuleNotFoundError: No module named 'langgraph'

4/9 passed (offline)
```

The repository has no `.venv` at audit time. A dependency installation was started
before the audit request arrived, but it was stopped by the tool timeout before it
completed; no repository files were changed by that attempt.

## Strengths

- The public-safe boundary is explicit and repeated in `AGENTS.md`, `README.md`, and
  the lab material.
- The lab sequence has a coherent technical spine: raw Realtime events, control-plane
  tools, turn-taking, LiveKit, LangChain, LangGraph, LangSmith, then a talker/thinker
  capstone.
- `labs/stlab/` provides deterministic fixtures for the backend, Realtime events,
  turn-taking, orchestration, and evaluation. This is the strongest part of the repo.
- The mock backend demonstrates several senior-level production concerns directly:
  structured policy errors, authoritative records, emergency detection, idempotency,
  audit logging, and simulated latency.
- The notebooks repeatedly make the important mechanism-versus-policy distinction:
  vendors provide mechanisms while application code owns authorization, business
  rules, state, and safety.
- The existing exercises are practical and deliberately include unsafe or unreliable
  behavior, such as early booking, ungrounded confirmation, interruptions, retries,
  and slow tools.
- The 30/60/90 checklist is concrete and outcome-oriented, with useful prompts for
  architecture mapping, call review, baseline measurement, and stakeholder work.

## Gaps And Weaknesses

### Audience and learning path

- README has only a short quick start. It does not provide a day-by-day pre-start path,
  estimated time, prerequisites, stopping points, or a recommended order tying docs to
  labs.
- The existing material assumes familiarity with home-services operations and contact
  center vocabulary. The glossary has only 15 terms and does not explain a contractor's
  job lifecycle.
- The study guide is a 575-line monolith with HTML artifacts from document conversion.
  It is useful as reference material but less effective as a self-paced guide.
- The audience's defense/edge/OOD background is not explicitly used as a bridge to
  production SaaS concepts such as tenant isolation, operational ownership, rollout,
  incident response, and customer-facing metrics.

### Domain and company context

- There is no `docs/` section separating public company/product context from technical
  study material.
- ServiceTitan and product references in the current guide are mostly uncited. The
  repo needs inline links and careful labels for public facts versus learning questions.
- There is no contractor job lifecycle, call anatomy, or fictional annotated scenario
  material covering common call types beyond the lab's booking scenarios.
- Membership, estimate, invoice, dispatch, reschedule, billing, and commercial versus
  residential context are underdeveloped.

### Technical study material

- The study guide contains architecture prose and one text diagram, but not the
  requested Mermaid reference architecture, call-turn sequence, latency budget
  diagram, or talker/thinker diagram in a standalone document.
- There is no curated reading list with verified URLs, reading time, and lab mapping.
- Evaluation concepts appear in lab 07, but there is no standalone treatment of metric
  definitions, sampling/dataset design, judge bias, online/offline tradeoffs, or OOD
  routing.
- Several claims are time-sensitive, especially model names, release dates, SDK APIs,
  and LiveKit configuration names. They need source links, version/date stamps, and a
  clear distinction between verified current behavior and illustrative simulator
  behavior.

### Labs and assessment

- Labs have exercises, but not consistent "check your understanding" sections,
  explicit grading criteria, answer keys, or learner-editable self-check assertions.
- There is no `labs/solutions/` directory.
- The notebooks are generated artifacts, so any lab additions require coordinated
  source edits and regeneration. There is no automated check that generated notebooks
  match sources.
- Offline execution currently depends on all declared packages for labs 04-08, even
  where much of the conceptual or simulator content could be gated. This makes a
  fresh minimal install failure-prone and obscures whether a failure is a live-only
  dependency issue or a lab bug.
- Lab 04 contains substantial current-API assumptions and generated agent programs;
  these need verification against current official docs before being called stable.
- Lab 07 mutates the imported `SCENARIOS` list when adding a regression case. That is
  acceptable for a demo cell but weak as reusable test hygiene.
- Some notebook examples use illustrative targets and simulated values. These are
  generally labeled, but the distinction should be made more consistently.
- A lab 09 is not yet justified. Telephony/SIP and production readiness are real gaps,
  but adding another notebook before improving navigation, assessment, and dependency
  gating would increase surface area without fixing the core learning experience.

### Repository quality and automation

- There is no GitHub Actions workflow.
- There is no Ruff configuration or lint command for `labs/stlab` and `scripts`.
- There is no automated notebook-output hygiene check.
- `.gitignore` excludes common generated files but does not itself prove notebooks are
  clean or prevent accidental generated artifacts from being committed.
- `AGENTS.md` accurately describes the current layout but will need updates if `docs/`,
  `labs/solutions/`, CI, linting, or output checks are added.
- The documented command uses `python`, which is normal for an activated venv and CI,
  but this macOS environment only exposes `python3`; the setup guidance could make the
  interpreter assumption clearer.
- There are no ordinary unit tests for the deterministic `stlab` package outside
  notebook execution. A small focused test suite would make regressions easier to
  diagnose than a failed notebook kernel.

### Templates and personal operating system

- Templates are intentionally blank and concise, but they lack short fictional filled-in
  examples, prompts for evidence, and guidance on what good completion looks like.
- The 1:1 questions are good starters but could be organized by manager, PM, peer,
  infrastructure, evaluation, and customer-facing conversations.
- The study-question note is a useful scaffold but remains empty; the self-paced path
  should tell the learner when and how to complete it without inventing employer facts.

## Proposed Improvements, Ranked

| Rank | Improvement | Value | Effort | Recommendation |
|---:|---|---|---|---|
| 1 | Create a clear README start path with four pre-start weeks, time estimates, prerequisites, progress tracking, and links to docs/labs/templates | Very high | Low | Do first |
| 2 | Split the study guide into `docs/voice-agent-architecture.md`, a verified `docs/reading-list.md`, and `docs/evaluating-voice-agents.md`, retaining the existing study guide as a compatibility/reference artifact if desired | Very high | Medium | Do first |
| 3 | Add public-source, citation-heavy domain context: `servicetitan-101.md`, `how-a-contractor-works.md`, and `call-anatomy.md` | Very high | Medium | Do before domain-focused checklist work |
| 4 | Add a 40+ term public-safe trades/contact-center glossary with explicit fictional examples and source links where claims are factual | High | Low | Do with domain docs |
| 5 | Add consistent notebook assessment: 3–5 understanding questions, graded exercises, assertions, and offline-safe solutions | Very high | High | Do in lab-focused phase |
| 6 | Verify current vendor APIs and links, especially LiveKit 1.x, OpenAI Realtime GA events, LangChain/LangGraph 1.x, and LangSmith 0.14+; record verification dates and isolate simulator-only assumptions | Very high | High | Do before editing lab APIs |
| 7 | Add dependency-aware offline gating and focused unit tests for `stlab`; keep every notebook end to end offline after a complete requirements install | Very high | Medium | Do before CI |
| 8 | Add GitHub Actions for dependency installation, notebook execution, Ruff, source/notebook consistency, and output hygiene | High | Medium | Do after local checks are reliable |
| 9 | Add `docs/first-90-days-playbook.md` connecting the checklist to 1:1s, first PRs, baselines, product-SaaS operating style, and contractor outcomes | High | Medium | Do after the learning path |
| 10 | Improve templates with short fictional examples and evidence-oriented prompts | Medium | Low | Do alongside the playbook |
| 11 | Add a standalone production-readiness or telephony/SIP lab 09 | Medium | High | Defer unless the revised path still has a measurable gap |

## Proposed Phases

### Phase A: Domain And Navigation

- Add `docs/servicetitan-101.md`, `docs/how-a-contractor-works.md`, and
  `docs/call-anatomy.md` using only verified public sources.
- Expand `notes/glossary.md` to 40+ terms.
- Add a skimmable README start path with time estimates and a progress table.
- Add source links and caveats rather than unsupported company-specific assertions.

### Phase B: Technical Study Path

- Add `docs/voice-agent-architecture.md` with Mermaid diagrams for the reference
  architecture, one call turn, latency budget, and talker/thinker pattern.
- Add `docs/reading-list.md` with official links, estimated time, and lab pairings.
- Add `docs/evaluating-voice-agents.md` covering business metrics, quality/safety
  metrics, datasets, judge limitations, online/offline evaluation, and OOD routing.
- Decide whether to keep `study-guide/voice-agent-study-guide.md` as the detailed
  source/reference or reduce it to a link into the new docs; do not silently delete the
  original content.

### Phase C: Labs And Assessment

- Establish a repeated notebook pattern: objectives, prerequisites, understanding check,
  graded exercise, assert-based self-check, solution link, and offline/live boundary.
- Add `labs/solutions/` with public-safe, deterministic solutions.
- Edit only `labs/src/*.py`, regenerate notebooks, and run targeted then full offline
  suites after each lab group.
- Add focused tests or self-checks for backend policies, tool grounding, emergency
  routing, idempotency, turn-taking, graph resume, and evaluation invariants.
- Verify stale APIs against official docs and update version notes.

### Phase D: First 90 Days And Templates

- Add `docs/first-90-days-playbook.md`.
- Add short fictional examples to all templates without implying they are employer data.
- Cross-link the playbook, checklist, domain docs, study path, and study-question note.

### Phase E: Repo Quality

- Add Ruff configuration and a lint command for `labs/stlab` and `scripts`.
- Add notebook checks for non-empty outputs and generated-source consistency.
- Add GitHub Actions for installation, lint, hygiene, and offline notebook execution.
- Update `AGENTS.md`, `README.md`, and `labs/README.md` to reflect the final layout.
- Run the full offline suite before each labs-related commit.

## What I Would Cut Or Defer

- Do not add lab 09 yet. First close the navigation, domain, assessment, and automation
  gaps; then reassess whether telephony/SIP or production readiness deserves a separate
  lab rather than a short document or exercise.
- Do not add more vendor frameworks or model providers. The current stack is already
  broad; depth, boundaries, and evaluation are more valuable than another integration.
- Do not reproduce the entire public ServiceTitan product catalog. Include only product
  context needed to understand contractor workflows and AI voice-agent relevance.
- Do not add live API calls to CI. CI must remain offline, deterministic, and secret-free.
- Do not turn fictional scenarios into realistic customer transcripts or use any
  employment-derived examples.
- Do not delete the `.docx` or existing study-guide Markdown without an explicit decision
  about compatibility and source-of-truth ownership.
- Do not add a large production-style application framework. The small deterministic
  fixtures are a teaching strength and should remain easy to inspect.

## Open Questions

1. Should the new `docs/` material become the primary study path while
   `study-guide/voice-agent-study-guide.md` remains a detailed reference, or should the
   old guide be rewritten as a shorter index?
2. Are public ServiceTitan product pages and investor materials the preferred sources,
   or should reputable third-party coverage also be included where official material is
   silent?
3. Should filled-in template examples live inline in each template, or in a separate
   `templates/examples/` directory to keep blank copies easy to duplicate?
4. Is installing the full `requirements.txt` in CI acceptable, or should optional live
   integrations be split into an explicitly named extra while preserving the current
   documented setup?
5. Should the generated notebooks remain committed, as `AGENTS.md` currently requires,
   with a consistency check, or should generation happen only in CI? I recommend keeping
   them committed and checking them.
6. Which current vendor API versions should be treated as the target baseline at the time
   of implementation? The repository currently names LiveKit Agents 1.8.x, LangChain 1.4,
   LangSmith 0.14, and `gpt-realtime-2`, all of which require source verification.
7. Should unit tests be added under `tests/`, or should the repository keep all tests in
   notebooks plus small executable checks under `scripts/`? I recommend `tests/` for
   deterministic fixtures and notebooks for teaching.
8. Is a public-facing company-context document desired at all, given the strict public
   safety rule? If yes, every claim will be linked to a public source and uncertain claims
   will be omitted or labeled unverified.

## Approval Gate

Awaiting approval before editing implementation files or adding dependencies. After
approval, work should proceed in small phases, with a summary and offline test result at
the end of each phase.
