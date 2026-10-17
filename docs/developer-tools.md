# Developer tools: the working engineer's toolkit

A living, task-oriented catalog of small tools that reduce friction while building,
debugging, testing, and documenting software. Start with tools that remove repeated
context switches; add complexity only when a tool solves a real workflow problem.

This page is deliberately broader than the voice-agent stack. It covers the local
developer workstation and the practical utilities around an AI-assisted coding loop.
Prefer tools with clear data-flow, predictable shortcuts, and easy removal. Re-check
pricing, release status, platform support, and privacy claims before adopting a tool;
these change faster than the rest of this guide.

## Quick-start shortlist

| Need | Start here | Why |
|---|---|---|
| Dictate prompts into any focused Mac text field | [MacParakeet](https://www.macparakeet.com/) | Free, open-source, system-wide push-to-talk; also handles files, media URLs, and meeting transcription |
| Minimal local voice-to-text | [OpenWispr](https://open-wispr.com/) | Free, open-source, on-device Whisper transcription with a configurable global hotkey |
| No-install fallback | [Apple Dictation](https://support.apple.com/guide/mac-help/dictate-messages-and-documents-mh40584/mac) | Built into macOS; try it before adding another background app |
| Cross-platform local/cloud voice workflows | [OpenWhispr](https://github.com/openwhispr/openwhispr) | Open-source desktop dictation and transcription with local model choices, including Parakeet and Whisper |
| Polished commercial dictation | [Wispr Flow](https://wisprflow.ai/) | A managed option if its editing workflow is worth the subscription and cloud-processing trade-off |

## Mac dictation for AI-assisted coding

The goal is simple: place the cursor in OpenCode, VS Code, a terminal prompt, an issue,
or a document; press and hold a shortcut; speak a complete instruction; release; review
the inserted text; then submit it. This avoids switching to a separate transcription
window and makes longer prompts less tedious.

### MacParakeet

- **Best fit:** a general-purpose, local-first Mac dictation and transcription utility.
- **Trigger:** Fn/Globe by default; configurable hotkeys are supported.
- **Workflows:** system-wide dictation, audio/video and URL transcription, meeting
  recording, custom vocabulary, and a CLI for automation.
- **Cost and license:** free and open source under GPL-3.0, according to the project.
- **Platform:** Apple Silicon Mac; the project currently documents macOS 14.2 or later.
- **Privacy boundary:** core speech recognition runs locally. URL transcription still
  downloads the source media, and optional external AI providers can introduce network
  data flows. Review settings before using it with sensitive material.
- **Links:** [Website and downloads](https://www.macparakeet.com/) ·
  [Source repository](https://github.com/moona3k/macparakeet) ·
  [Agent/CLI integration guide](https://macparakeet.com/agents/)

### OpenWispr

- **Best fit:** lightweight push-to-talk dictation when local transcription is the main
  requirement.
- **Trigger:** hold the Globe/Fn key, speak, release to transcribe; the project documents
  configurable shortcuts, including F5.
- **Speech engine:** local Whisper via whisper.cpp with Metal acceleration on Apple
  Silicon.
- **Cost and license:** free and open source under MIT, according to the project.
- **Platform:** Apple Silicon and a recent macOS version; check the current repository
  for exact requirements.
- **Trade-off:** more focused than MacParakeet; MacParakeet is the broader choice if
  file/URL transcription, meeting recording, or its CLI are also useful.
- **Links:** [Website and installation](https://open-wispr.com/) ·
  [Source repository](https://github.com/human37/open-wispr)

### Apple Dictation

- **Best fit:** trying voice input without installing or maintaining another app.
- **Trigger:** configure the Dictation shortcut in macOS Keyboard settings; exact behavior
  depends on macOS version and settings.
- **Trade-off:** fewer app-specific controls than dedicated push-to-talk tools. Test
  recognition quality, insertion behavior, and privacy requirements on your own Mac
  before deciding it is insufficient.
- **Link:** [Apple's Dictation guide](https://support.apple.com/guide/mac-help/dictate-messages-and-documents-mh40584/mac)

### Other options to evaluate

| Tool | When to consider it | Check before adopting |
|---|---|---|
| [OpenWhispr](https://github.com/openwhispr/openwhispr) | You want a cross-platform workflow or selectable local models such as NVIDIA Parakeet and Whisper | Model/runtime setup, platform-specific hotkeys, and whether any optional cloud path is enabled |
| [Wispr Flow](https://wisprflow.ai/) | You value polished cleanup and a managed user experience | Current free-tier limits, subscription price, and cloud data handling |
| [Superwhisper](https://superwhisper.com/) | You want configurable modes and multiple transcription workflows | Current plan limits, supported models, and which modes process data locally |

## Managing many simultaneous agent sessions

Dictation solves input friction; multi-agent session management solves attention and
coordination friction. The useful setup depends on whether you need to organize terminal
processes, supervise coding agents, or delegate independent work to persistent cloud agents.
These are related but different jobs.

### Terminal workspaces and multiplexers

| Tool | Best fit | Strengths | Trade-offs |
|---|---|---|---|
| [WezTerm](https://wezterm.org/) | A powerful terminal GUI for macOS, Linux, and Windows | Native tabs, panes, workspaces, remote multiplexing, configurable Lua workflows, and a CLI that can spawn or target panes | It organizes terminal processes; it does not itself understand agent tasks or decide which agent needs attention |
| [tmux](https://github.com/tmux/tmux/wiki) | Persistent terminal sessions, especially over SSH | Mature session/window/pane model; scripts well; sessions survive terminal disconnects | More keyboard- and configuration-oriented; session status is not automatically agent-aware |
| [cmux](https://cmux.com/) | Agent-centric terminal workspaces | Organizes each task in a workspace; keeps coding agents beside tests, logs, and browser surfaces; notifications and agent state are tied to workspace surfaces | Evaluate its current platform and remote-workflow requirements; it is a workspace layer, not a universal agent orchestrator |
| [ccmux](https://ccmux.dev/) | Finding and switching among many agents already running in tmux | Open-source session picker for agent sessions, with search and previews; works with existing tmux habits | Depends on a tmux-based workflow and the agents/session patterns it recognizes |
| [Zellij](https://zellij.dev/) | A modern terminal multiplexer alternative | Sessions, panes, tabs, layouts, and plugin support | Like tmux, it manages terminal layout and persistence rather than agent-level coordination |

**Practical starting point:** use WezTerm if you want a configurable native terminal with
workspaces and panes. Add tmux when durable sessions, remote SSH workflows, or automation
matter. Evaluate cmux or ccmux if the hard part is seeing which agent is running, waiting,
or finished—not simply keeping terminals open.

### Coding-agent session orchestration

| Tool / pattern | Best fit | What to evaluate |
|---|---|---|
| [Grok CLI](https://github.com/superagent-ai/grok-cli) | A terminal coding agent using the Grok API | Its TUI, persistent sessions, sub-agents, MCP support, and Telegram remote control; verify API costs and project maturity |
| [OpenCode](https://opencode.ai/) and editor/CLI agents | Running coding agents directly in repository worktrees | Session resume, permission controls, worktree isolation, branch ownership, and whether parallel runs can edit the same files |
| Git worktrees + one agent per worktree | A tool-agnostic way to parallelize repository tasks | Separate branches and working directories, clear task boundaries, independent tests, and a defined integration/review step |

The core safety rule is **one independently writable worktree per parallel coding task**.
Separate terminal panes do not isolate file edits: two agents in the same working directory
can overwrite each other's changes or leave the repository in a confusing state. Assign
each agent a bounded task, explicit acceptance criteria, and an owner responsible for review
and integration.

### Additional orchestration projects to watch

| Project | Why it belongs on the watchlist | Maturity check |
|---|---|---|
| [Agentdesktop](https://github.com/agentdesktop-dev/agentdesktop) | Inventory and configure multiple AI developer tools, MCP servers, skills, and policy across a workstation or fleet | More of a governance/configuration layer than a live terminal-session switcher; check supported tools and deployment requirements |
| [Agents in a Box](https://github.com/stevengonsalvez/agents-in-a-box) | Terminal-native agent management with multiple coding-agent integrations and git-worktree isolation | Broad, fast-moving toolkit; inspect setup complexity and supported agents before adopting |
| [TermSnap](https://github.com/Dannykkh/TermSnap-releases) | Explores an AI workstation that orchestrates agents across terminals, desktop applications, and remote systems | Treat as an exploratory candidate; verify release cadence, platform fit, and actual integration depth |

### Desktop AI workbenches and persistent bots

| Tool | Category | Where it fits | Important distinction |
|---|---|---|---|
| [AnythingLLM](https://anythingllm.com/) | Desktop/local-first LLM workspace with agent tools | Workspace-based chats, configurable models, agent skills, and custom tools/MCP integrations | Useful for model- and knowledge-centric workflows; not primarily a dashboard for managing arbitrary terminal coding sessions |
| [Grok Bot](https://docs.x.ai/grok-bot/overview) | Persistent cloud AI teammates | Bots have persistent cloud computers, browser/filesystem/terminal access, retained context, and can coordinate in parallel or group chats | A delegation and cloud-computer model, not a local terminal multiplexer; check account eligibility, approvals, and data access |
| [Grok CLI](https://github.com/superagent-ai/grok-cli) | Local terminal coding agent | Works inside a terminal workflow and documents sub-agents and Telegram remote control | Separate product/project from Grok Bot; do not conflate their capabilities, billing, or execution environments |

For cloud bots, assess permissions and data boundaries separately from local coding agents:
what repositories and credentials can the bot access, where does execution happen, how are
actions approved, and what persists between tasks? For local tools, assess shell permissions,
filesystem scope, model/API routing, and whether transcripts or source code are sent to a
provider.

### A simple operating model for parallel agents

1. **Coordinator:** maintain the task list, assign bounded tasks, and own integration.
2. **Workers:** one task and one worktree per agent; avoid concurrent edits to the same files.
3. **Shared task record:** write down objective, branch/worktree, files in scope, acceptance
   criteria, tests to run, and current status.
4. **Visible state:** use distinct workspace/session names and status labels such as
   `working`, `waiting for input`, `tests running`, and `ready for review`.
5. **Review gate:** inspect diffs and run tests before merging. Agent completion is not proof
   of correctness.
6. **Budget and safety:** set limits for tool calls/API spend and require approval for
   destructive operations, external messages, and credential-sensitive actions.

Start with two agents on independent tasks before scaling up. Measure completed tasks per
hour, human context-switching time, integration conflicts, review defects, and cost—not the
raw number of agents running.


### From task to verified change: an agent operating contract

The terminal/worktree setup above covers coordination. This section defines the contract each
task follows, regardless of which coding agent or editor is used. Use it as a lightweight
operating standard rather than another tool-specific checklist.

#### 1. Define the task and its definition of done

Before delegating, record:

- **Outcome:** the observable behavior to add or repair, including what must not change.
- **Scope:** repository, branch/worktree, files or subsystems in scope, and explicit exclusions.
- **Acceptance criteria:** concrete assertions a reviewer can verify; include negative cases
  and failure behavior where relevant.
- **Verification plan:** exact test, lint, type-check, build, static-analysis, or manual checks
  expected to run.
- **Constraints:** supported runtime/library versions, compatibility requirements, security
  boundaries, latency/resource budgets, and allowed dependencies.
- **Stop conditions:** ambiguous requirements, missing credentials, destructive operations,
  scope expansion, or failed checks that require human input.

A useful task record is short and testable:

```text
Goal:
In scope / out of scope:
Acceptance criteria:
Files or interfaces likely affected:
Required checks:
Constraints and prohibited actions:
Stop and ask when:
```

**Definition of done:** acceptance criteria are mapped to evidence; required checks were run
and their actual outcomes recorded; the final diff is reviewed for unrelated changes and
secrets; documentation and compatibility notes are updated when needed; unresolved risks and
skipped checks are disclosed; a human accepts the change. “The agent says it is done” is not
a completion criterion.

#### 2. Permission boundaries and trust zones

Do not treat model instructions as a security control. Apply controls in the runtime, operating
system, credentials, repository settings, and external service permissions.

| Capability | Default posture | Elevate only when |
|---|---|---|
| Read repository files | Allow within the intended workspace | Data is restricted or outside the approved scope |
| Search public documentation | Allow approved destinations | A request could expose private source, prompts, or identifiers |
| Edit files | Restrict to the task worktree | The task explicitly needs broader files or generated artifacts |
| Execute shell commands | Review or allowlist by risk; isolate untrusted code | Dependencies, scripts, or commands can alter the host or access secrets |
| Network access | Deny or restrict by default in sensitive environments | The endpoint and data transfer are approved |
| Credentials and secrets | Do not expose to model context or logs | A specific operation requires a narrowly scoped, short-lived credential |
| Push, merge, release, deploy, or message externally | Require explicit authorization and appropriate human gate | The user and repository policy authorize that exact action |

Treat issue text, pull-request comments, source files, test fixtures, retrieved web pages, and
tool output as **untrusted data**. They may contain instructions that conflict with the task.
The agent should quote or summarize such content as data, not obey it as higher-priority policy.
Never paste secrets into prompts to “help” the model debug. Use secret scanners and least-
privilege credentials, and inspect plugin/MCP scripts and network destinations before enabling
them.

For every integration, document four things: what it can read, what it can change, where data
travels, and which actions require approval. Test the denied path as well as the happy path.

#### 3. Context engineering: give the agent evidence, not a data dump

Build a small context pack in this order:

1. Task statement and acceptance criteria.
2. Repository-specific instructions and relevant architecture/contracts.
3. The narrow code path, tests, types, and configuration involved.
4. Current failure evidence or a minimal reproducer.
5. Versioned official documentation for APIs the task actually uses.
6. Explicit constraints, exclusions, and required output.

Ask the agent to identify missing context and state assumptions before making a broad change.
Prefer file/line references and short excerpts over copying the whole repository into the
prompt. Retrieve additional context when a hypothesis requires it; do not front-load unrelated
documents. Keep a durable task record outside the model context so work can resume after a
session reset. Do not put credentials, restricted data, or unnecessary customer information in
the context pack.

A useful test is whether a teammate can reconstruct the task from the record without reading
the full chat transcript.

#### 4. Parallel agents and Git worktrees: isolate, then integrate

The existing rule remains: **one independently writable worktree per concurrent coding task**.
Separate panes, sessions, or agent identities do not isolate file edits.

Example for two independent tasks from the same repository:

```bash
git status --short
git worktree add ../repo-task-a -b agent/task-a origin/main
git worktree add ../repo-task-b -b agent/task-b origin/main
git worktree list
```

Use the repository's actual remote/base branch; do not assume `origin/main` exists in every
environment. Give each agent a distinct scope and acceptance criteria. Avoid assigning both
agents the same files or shared generated outputs. Keep dependencies between tasks explicit:
if task B needs task A's interface, either agree on the interface first or run them sequentially.

Before integration, each worker must report its branch, changed files, tests run, test results,
and unresolved assumptions. The integration owner then inspects each diff, resolves interface
or merge conflicts, runs the combined tests, and checks for regressions that neither branch
could expose independently. Remove a worktree only after its changes are safely integrated or
deliberately discarded. Parallelism is successful when it reduces elapsed time without
increasing rework, defects, or reviewer load.

#### 5. Harness architecture and failure recovery

Think of the harness as the control plane around the model. A minimal coding-agent harness has:

- **Task/state store:** objective, owner, status, branch/worktree, budget, and checkpoints.
- **Context builder:** approved repository instructions, selected files, relevant docs, and
  reproducible failure evidence.
- **Policy layer:** tool allowlists, filesystem/network boundaries, approval requirements,
  and secret handling.
- **Tool adapters:** shell, Git, test runner, documentation search, issue/PR system, and MCP.
- **Verification layer:** deterministic tests, linters, type checks, diff checks, and policy
  assertions independent of the model's self-report.
- **Telemetry and recovery:** structured events, bounded retries, timeouts, cancellation,
  checkpoints, and a human escalation path.

Use a bounded state machine such as `queued → running → verifying → review → accepted`, with
explicit `blocked`, `failed`, and `cancelled` states. A failed test must not silently become
a pass after a retry. Retry only when the failure is plausibly transient, cap attempts, and
record each attempt. Never retry a non-idempotent external action blindly. Before resuming an
interrupted task, inspect Git status and diff, active processes, test artifacts, and external
side effects; reconstruct state from durable records rather than assuming the last model turn
completed atomically.

Provide a safe stop path: cancel execution, preserve logs, inspect partial writes, revert only
the task's unintended changes, and report the exact point where work stopped. Require human
approval for destructive recovery or actions with external consequences.

#### 6. Verify dependency and API assumptions

Generated code frequently fails because examples target a different library or runtime version.
Before using an API:

1. Inspect the manifest and lockfile, runtime/toolchain versions, and repository compatibility
   policy.
2. Prefer official documentation or source for the installed version; distinguish stable,
   preview, and deprecated APIs.
3. Verify function signatures, return/error semantics, authentication, timeout behavior,
   and async/concurrency requirements.
4. Add or update a focused test that exercises the real contract, including an error path.
5. Avoid adding a dependency when the existing stack already provides the capability; if one
   is needed, assess maintenance, license, transitive dependencies, and security advisories.
6. Regenerate lockfiles only with the project's intended package manager and explain material
   dependency changes in the diff.

If documentation and installed code disagree, report the mismatch and test the installed
version. Do not “fix” a type error by weakening types, pinning an arbitrary version, or copying
an example from a different major release without explaining the compatibility trade-off.

#### 7. Observability and cost tracking

Record enough information to reconstruct the task without storing secrets or unnecessary source
content. A useful event schema includes:

| Field | Purpose |
|---|---|
| `task_id`, `attempt_id`, `parent_task_id` | Correlate retries, subagents, and integration work |
| `agent`, `model`, `model_version`, `skill_version` | Attribute behavior to the execution configuration |
| `repo_revision`, `branch`, `worktree` | Reproduce the starting state and locate the diff |
| `event_type`, `timestamp`, `duration_ms` | Reconstruct sequence, waits, and latency |
| `tool_name`, `sanitized_args_summary`, `exit_code` | Understand tool use without logging credentials or full sensitive payloads |
| `test_name`, `result`, `failure_category` | Distinguish verification from the agent's narrative |
| `input_tokens`, `output_tokens`, `tool_calls`, `estimated_cost` | Track consumption and identify runaway loops |
| `changed_files`, `review_findings`, `final_disposition` | Connect activity to the delivered engineering result |

Capture structured events rather than relying on a final free-form summary. Redact tokens,
credentials, personal data, and sensitive source snippets at collection time; define access,
retention, and deletion policies. Do not treat estimated model cost as a complete cost metric:
include tool/runtime usage and human review or rework when measurable.

Track cost and outcomes together: task success, time to accepted change, regression rate,
reviewer correction time, retry/loop rate, and cost per accepted task. A cheaper run that
creates more review burden may be more expensive end to end.

#### 8. Benchmark coding agents with controlled tasks

Build a small, version-controlled benchmark from real, sanitized repository tasks. Include
bug fixes, feature changes, refactors, test failures, dependency/API changes, and code review.
Each task needs a fixed starting commit, task prompt, acceptance tests, allowed tools, time/cost
budget, and scoring rubric. Use synthetic or public-safe data.

**Protocol**

1. Freeze the task set and starting revisions; record model, agent, harness, skill, and
   dependency versions.
2. Run each candidate from a clean worktree with the same tools and equivalent budgets.
3. Repeat stochastic tasks where feasible; do not compare one lucky run against one failure.
4. Evaluate outputs with deterministic tests and blinded human review where judgment is needed.
5. Separate development/tuning tasks from a held-out set to reduce benchmark overfitting.
6. Report failures, timeouts, tool errors, and skipped tasks; do not drop unsuccessful runs.
7. Re-run the baseline when prompts, models, skills, harness, or dependencies change.

| Metric | Definition |
|---|---|
| Acceptance pass rate | Fraction of tasks meeting all mandatory criteria |
| Regression rate | Fraction introducing failures in previously passing checks |
| Review defect density | Confirmed actionable defects per change or changed-line band |
| Time to accepted change | Wall-clock time through verification and human acceptance |
| Human correction/rework | Reviewer and author effort needed after agent completion |
| Cost per accepted task | Total measured model/tool cost divided by accepted tasks |
| Reliability | Run-to-run variance, timeout rate, and incomplete-task rate |
| Safety violations | Unauthorized tool use, secret exposure, or bypassed approval gates |

Do not collapse everything into a single score without retaining the underlying metrics. Treat
security and correctness requirements as hard gates, not benefits that can be averaged away by
speed. A benchmark is a decision aid, not proof that an agent is safe for every repository.

## Knowledge management and personal information systems

A knowledge tool is useful only if notes remain findable and can be reused. Choose the
system of record first; add AI access as a separate integration layer. Avoid scattering
the same canonical information across several competing stores.

| Tool | Best fit | Strengths | Trade-offs and checks |
|---|---|---|---|
| [Obsidian](https://obsidian.md/) | Personal technical knowledge base | Local Markdown vault, links/backlinks, graph, community plugins, portable files | Plugins can add maintenance and permissions risk; choose a sync and backup strategy deliberately |
| [DEVONthink](https://www.devontechnologies.com/) | Mac document archive and research library | Strong document organization and search across accumulated references | Mac-centric and more document-library-oriented than a plain-Markdown vault; evaluate export and automation needs |
| [Apple Notes](https://www.apple.com/ios/notes/) | Fast, low-friction capture | Built in to Apple platforms; convenient for short notes, scans, and checklists | Less suitable as a version-controlled, agent-facing technical knowledge repository |
| [Notion](https://www.notion.com/) | Shared team wiki and structured workspace | Pages, databases, project documentation, and collaboration | Cloud workspace; distinguish team-authoritative content from personal notes and check access controls |
| [Readwise Reader](https://readwise.io/read) | Reading inbox and highlight collection | Collects web articles and reading material and supports highlight workflows | It complements rather than replaces a canonical project wiki or source repository |
| [NotebookLM](https://notebooklm.google.com/) | Source-grounded exploration of a selected corpus | Useful for asking questions of supplied sources and generating audio overviews | Treat outputs as a research aid; verify claims against the cited source material |

**Suggested default:** keep durable technical notes in a well-backed-up Markdown vault or
team repository; keep team decisions and project status in the team's approved systems;
keep transient capture lightweight. Store secrets and restricted company material only in
approved locations.

### Make knowledge available to Claude Desktop and Cursor

Model Context Protocol (MCP) is one way to expose a knowledge store or application to an
AI client. It is an integration protocol, not a knowledge base in itself.

- [Obsidian MCP Connector](https://community.obsidian.md/plugins/mcp-tools-istefox) is a
  community plugin that documents vault search, file operations, and connections to
  Claude Desktop, Cursor, and other MCP clients. Confirm the current plugin source,
  permissions, and release activity before installing.
- [Obsidian MCP Server](https://community.obsidian.md/plugins/mcp-server) is another
  community-plugin option. Compare its capabilities and setup instructions rather than
  assuming all plugins named “MCP” provide the same tools or transport.
- [Claude Desktop local MCP setup](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
  documents local MCP servers and desktop extensions, including a simpler extension-based
  installation path for supported servers.
- [Cursor MCP documentation](https://prod.cursor.com/docs/mcp) covers local and remote
  MCP servers, project-level `.cursor/mcp.json`, global configuration, and tool approvals.
  Cursor also supports reusable plugins, rules, skills, subagents, commands, and hooks
  ([plugin documentation](https://prod.cursor.com/docs/plugins)).

Before connecting an agent, answer four questions: what can it read, what can it modify,
where does data travel, and which actions require approval? Prefer read-only access for
search and retrieval. Keep write, shell, external-message, and destructive tools disabled
until their need and approval boundary are explicit. Do not point consumer AI clients at
sensitive work notes or repositories unless that use is approved.

## Slack calls, conversation capture, and RAG

Treat Slack calls and Slack messages as two different ingestion sources. A huddle transcript
captures spoken discussion; a thread export captures the written context, follow-ups, and
corrections around it. A useful knowledge system links the two when possible instead of
flattening everything into anonymous text.

### Recording and transcribing Slack calls

| Option | Best fit | Important details |
|---|---|---|
| [Slack AI huddle notes](https://slack.com/help/articles/31377193680019-Use-AI-to-take-huddle-notes-in-Slack) | First option to evaluate for Slack Huddles | Available on paid plans; a participant starts notes, and people are notified. Notes and transcript are placed in a canvas in the huddle thread. Slack says the embedded transcript does not appear in search results, so it may not by itself meet a searchable RAG requirement. |
| [Slack Huddles notes canvas](https://api.slack.com/help/articles/4402059015315-Use-huddles-in-Slack) | Human-written meeting notes and shared links | Useful as a durable location for decisions and follow-ups, even if automated transcription is not enabled. |
| [Granola](https://www.granola.ai/) | Mac meeting notes workflow to evaluate | Check current support for capturing Slack Huddles specifically, audio-routing requirements, storage/retention, and company approval before relying on it. |
| [Otter](https://otter.ai/) or [Fireflies](https://fireflies.ai/) | Meeting transcription and summaries for supported meeting workflows | Verify Slack Huddle compatibility rather than assuming a bot that joins Zoom/Meet/Teams can capture a Slack Huddle. Review recording disclosure, retention, data processing, and workspace policy. |

**Recommendation:** start with Slack's native huddle notes if the workspace plan supports them.
If you need external capture, run a short, approved compatibility test on a non-sensitive meeting.
Confirm that every participant receives the required notice and that the resulting transcript can
be exported or retrieved through a supported interface. Do not work around organization recording
controls or upload confidential conversations to an unapproved service.

### Exporting Slack threads

There are two paths, suited to different scopes:

- **One-time or periodic archive:** use Slack's owner/admin export workflow. The export options
  depend on plan and authorization. Public-channel message exports are broadly available to
  authorized owners/admins; exports of private channels and DMs have additional plan and approval
  requirements. Exports generally contain file links, not the underlying file contents.
  See [Slack's export guide](https://slack.com/help/articles/201658943-Export-your-workspace-data).
- **Ongoing, scoped ingestion:** use an approved Slack app and API. The
  [`conversations.replies` API](https://docs.slack.dev/reference/methods/conversations.replies/)
  retrieves a thread; history/search APIs can discover messages in the approved scope. Design
  around scopes, pagination, rate limits, and the actual token type's access. Do not assume a bot
  token can read every private channel or DM.

For interactive, current lookups, Slack's [MCP server](https://slack.com/help/articles/48855576908307-Guide-to-the-Slack-MCP-server)
can let compatible AI clients search and retrieve authorized Slack messages and threads.

#### MCP retrieval, custom RAG, or both?

**MCP (Model Context Protocol) is a tool-access protocol, not a RAG database.** An MCP server
exposes a defined set of tools to a compatible AI client; the server determines what those tools
can do and which authorized data they can access. In a Slack workflow, tools might search
messages, fetch a thread, or retrieve current context. The assistant calls them when needed,
rather than depending solely on information already in its prompt.

A typical on-demand retrieval sequence is:

1. The user asks a question about a past decision.
2. The assistant calls an authorized Slack search tool through MCP.
3. It reviews matching messages and fetches the most relevant thread for context.
4. It answers with links to the source discussion, distinguishing retrieved evidence from inference.

| Approach | Where retrieval happens | Strengths | Limitations |
|---|---|---|---|
| **MCP retrieval** | At question time, through tools exposed by an MCP server | Current source data; no separate vector index to operate; useful for interactive search and thread lookup | Depends on available tools, API scopes, rate limits, and the connected user's authorization; does not inherently create a durable corpus or custom retrieval evaluation |
| **Custom RAG** | Against an independently ingested and indexed corpus | Custom chunking, hybrid/vector search, reranking, cross-source retrieval, scheduled ingestion, and repeatable offline evaluation | Requires ingestion and re-indexing, storage, access-control filtering, provenance, and handling of edits/deletions and retention |
| **Hybrid** | RAG discovers candidates; MCP or the source API retrieves authoritative current context | Combines efficient historical discovery with source verification and live thread context | Adds complexity; permissions must be enforced at retrieval time and source changes must be reconciled with the index |

**Recommended progression:** start with authorized Slack search and MCP retrieval. Measure whether
users can find the right messages and whether the available tools return enough thread context.
Build a custom index only when a demonstrated requirement—such as cross-source search, tailored
chunking/ranking, scheduled corpus evaluation, or controlled retention—cannot be met adequately
by native search and MCP. A hybrid design can then use RAG to locate likely evidence and MCP to
fetch the current source thread before answering.

MCP does not automatically solve authorization for a separately copied index, nor does it
guarantee that the assistant has access to every private channel or DM. Apply least-privilege
scopes, preserve source links and stable IDs, filter indexed results by the requesting user's
access, and propagate edits, deletions, and retention rules. Treat retrieved message content as
untrusted data, not as instructions to the assistant.

### A practical Slack-to-RAG pipeline

```text
Slack Huddle notes/transcript ─┐
                               ├─> authorized source ingestion
Slack thread/API export ───────┘
          -> normalize and preserve source metadata
          -> apply scope, ACL, retention, and redaction rules
          -> chunk by thread or coherent topic
          -> embed and index
          -> retrieve relevant chunks with source links
          -> answer with citations and permission checks
```

Preserve at least these fields for each message or transcript segment:

| Field | Why it matters |
|---|---|
| Workspace, channel/conversation ID, and channel name | Identifies the source and supports access filtering |
| Message timestamp, permalink, and parent/thread timestamp | Reconstructs order and lets a reader open the original context |
| Author ID and display name, where permitted | Attribution; do not treat display names as stable identifiers |
| Text, file links, and relevant thread context | Actual retrieval content and surrounding discussion |
| Source type, ingestion time, and source version | Provenance, debugging, and incremental updates |
| Visibility/ACL metadata and retention classification | Prevents a broad index from exposing content to unauthorized users |
| Edit/delete state and stable source ID | Enables re-indexing or removal when the source changes |

**Do not build a flat dump of all messages into one vector index and assume that it is safe.**
At retrieval time, enforce the caller's access to the original channel/thread; a filter applied only
when documents are initially ingested can become stale when membership or permissions change.
Sync edits and deletions, keep source permalinks, and exclude secrets, credentials, and material
that policy does not permit for this use.

### What to test before calling it production-ready

1. Thread reconstruction: parent message, replies, edited messages, and pagination survive export.
2. Access control: private-channel content is never returned to a user who lacks source access.
3. Deletion and retention: removed or expired source material disappears from retrieval and caches.
4. Attribution: every answer links to the exact source thread or transcript segment.
5. Quality: evaluate retrieval recall, citation correctness, stale/conflicting answers, and abstention
   when the corpus does not support a claim.
6. Governance: obtain workspace-owner/security approval and follow applicable consent, retention,
   privacy, and company data-handling rules.

## Task tracking tools for Mac

Choose a tracker based on whether the work is personal, shared across a team, or tied directly to code. Avoid maintaining duplicate backlogs unless one system is explicitly authoritative.

### Personal tasks

| Tool | Best fit | Strengths | Trade-offs |
|---|---|---|---|
| [Apple Reminders](https://support.apple.com/guide/reminders/welcome/mac) | Free, built-in option | Lists, tags, smart lists, subtasks, recurring reminders, shared lists, Siri capture | Lightweight rather than full project management; some features depend on iCloud |
| [Things 3](https://culturedcode.com/things/) | Polished Apple-only personal planning | Inbox, Today and Upcoming views, projects, tags, natural-language scheduling, calendar events | Paid; Apple ecosystem only; no team project management |
| [Todoist](https://todoist.com/) | Best general-purpose cross-platform choice | Fast capture, natural-language dates, filters, integrations, shared projects | Some advanced features require a paid plan |
| [TickTick](https://ticktick.com/) | All-in-one personal planner | Tasks, calendar views, recurring work, habits, focus/Pomodoro tools | Busier interface; verify current plan limits |
| [OmniFocus](https://www.omnigroup.com/omnifocus) | Complex personal workflows / GTD | Defer dates, Forecast, reviews, custom perspectives, automation | More setup and maintenance; primarily Apple-focused |

### Shared projects and engineering work

| Tool | Best fit | Strengths | Trade-offs |
|---|---|---|---|
| [Linear](https://linear.app/features) | Product and engineering teams | Issues, cycles, projects/roadmaps, triage, integrations, coding-session workflows | Use the team's existing tracker rather than creating a parallel backlog |
| [GitHub Issues and Projects](https://github.com/features/issues) | Work tied to repositories and pull requests | Issues, sub-issues, milestones, custom fields, board/table views, links to code, CLI support | Best when the team works in GitHub; not a general personal task manager |
| [Asana](https://asana.com/features/project-management) | Cross-functional project coordination | Ownership, dependencies, list/board/timeline views, status updates | More process overhead than an individual to-do list |
| [Trello](https://trello.com/) | Simple visual workflows | Kanban boards, cards, checklists, lightweight automation | Can become cumbersome for large dependency-heavy programs |

### Selection rule

- **Free and native:** Apple Reminders.
- **Focused Mac experience:** Things 3.
- **Cross-platform or shared tasks:** Todoist.
- **Tasks plus calendar and focus tools:** TickTick.
- **Complex personal system:** OmniFocus.
- **Software delivery:** the team's existing Linear or GitHub Issues/Projects workflow.

For AI-assisted engineering, the task record should include an owner, goal, branch/worktree, scope, acceptance criteria, test results, and status such as `working`, `blocked`, or `ready for review`. Link tasks to branches and pull requests; an agent saying it finished is not proof of correctness.

Before using a task app for company work, check approved data handling, account boundaries, export options, integrations, and external AI processing. Keep restricted work out of personal accounts unless that use is approved.

## Mac productivity and workflow automation

These utilities reduce the small interruptions that accumulate during engineering work.
Choose by task instead of installing overlapping tools that all try to own the same shortcut.

| Tool | Best fit | Useful capabilities | Evaluation notes |
|---|---|---|---|
| [Raycast](https://www.raycast.com/) | Keyboard-first launcher and command surface | App/file search, snippets, clipboard history, quicklinks, extensions, window controls, and optional AI workflows | Many features are free; some AI and retention capabilities are paid. Review extension permissions and clipboard exclusions |
| [Alfred](https://www.alfredapp.com/) | Launcher and custom workflows | Fast search, snippets, hotkeys, and extensible workflows | Some advanced workflows require the Powerpack; compare with Raycast rather than running both by default |
| [Keyboard Maestro](https://www.keyboardmaestro.com/main/) | Multi-step Mac automation | Triggered macros across applications, keyboard shortcuts, text actions, and repeatable procedures | Powerful automation can act in the wrong window or context; include explicit guards and test destructive actions |
| [BetterTouchTool](https://folivora.ai/) | Custom input and window actions | Trackpad, keyboard, mouse, and window-management customization | Overlaps with other automation tools; evaluate whether it solves a specific ergonomic problem |
| [Rectangle](https://rectangleapp.com/) | Window layout | Keyboard-driven window snapping and placement | Simple, focused alternative when full workflow automation is unnecessary |

Raycast's official documentation describes clipboard history, snippets, extensions, and AI
extensions that can invoke actions from installed tools. See its
[extensions guide](https://manual.raycast.com/extensions) and
[clipboard history guide](https://manual.raycast.com/clipboard-history). Clipboard tools
can capture credentials and confidential text, so configure exclusions and retention before
enabling them on a work machine.

### Integration patterns worth testing

1. **Capture:** use a launcher, dictation, or quick note to capture an idea without changing
   context.
2. **Curate:** move durable knowledge into the chosen vault or repository with source,
   date, project, and status.
3. **Retrieve:** connect a compatible AI client through a narrowly scoped integration such
   as MCP; start with search/read access.
4. **Act:** expose write or automation tools only when the workflow requires them, with
   explicit approval and an audit trail where possible.
5. **Review:** periodically remove stale notes, broken links, unused integrations, and
   plugins that no longer need access.

## How to choose a dictation tool

1. **Shortcut ergonomics:** can you hold one key, speak, release, and continue typing
   without changing windows? Check whether the key conflicts with IDE or macOS shortcuts.
2. **Insertion reliability:** does text land at the active cursor in your editor, terminal,
   browser, and remote-desktop session? Some secure or elevated fields may behave
   differently.
3. **Recognition quality:** test actual coding vocabulary, acronyms, filenames, class
   names, punctuation, and commands. Compare the raw transcript rather than judging from
   a marketing demo.
4. **Latency:** measure the time from key release to usable inserted text, not only the
   model's claimed real-time factor.
5. **Privacy and retention:** distinguish local speech recognition from optional cloud
   cleanup, telemetry, saved transcripts, crash reports, media downloads, and update checks.
   Do not dictate secrets or company-sensitive content into an unapproved tool.
6. **Correction cost:** a fast transcript that mangles identifiers can be slower overall
   than a slightly slower, more accurate one. Maintain a short test script of representative
   prompts and repeat it after updates.
7. **Operational footprint:** check login-item/background behavior, accessibility and
   microphone permissions, CPU/memory use, updates, and uninstall steps.

## Starter evaluation

Run the same five prompts through each candidate and record the results:

- A normal prose instruction to an AI coding agent.
- A prompt containing acronyms and product names.
- A code-oriented prompt with identifiers, paths, and punctuation.
- A multi-sentence debugging hypothesis with explicit acceptance criteria.
- A prompt spoken in a realistic environment with keyboard/fan noise.

Record word error rate if you have a reference transcript, but also track identifier
accuracy, manual correction time, end-to-end latency, insertion failures, and whether audio
or text leaves the device. Use fictional or public-safe examples.

## Growing the developer-tools catalog

Keep entries task-oriented rather than collecting tools for their own sake. Useful future
categories include:

- **AI coding:** terminal agents, editor integrations, code review, and repository-aware
  workflows.
- **Navigation and automation:** launchers, clipboard history, window management, and
  repeatable shell workflows.
- **Debugging and observability:** structured logs, trace viewers, profilers, and local
  inspection tools.
- **API and data work:** HTTP clients, database explorers, JSON/JSONL viewers, and event
  stream inspection.
- **Knowledge capture:** Markdown notes, screenshots, screen recording, and local search.
- **Testing:** request replay, fixtures, mock services, load generation, and diffable
  evaluation reports.

For each new entry, capture: problem solved, supported platforms, install method, price and
license, local/cloud data path, keyboard workflow, maintenance status, and one concrete
reason to use it. Treat vendor claims as claims until verified with a small hands-on test.
