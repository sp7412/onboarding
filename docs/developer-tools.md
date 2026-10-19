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
| Desktop LLM workspace with knowledge and tool integrations | [AnythingLLM](https://anythingllm.com/) | Run workspace-based chats with configurable models, documents/knowledge, agent tools, and custom tools/MCP integrations; it is not a dashboard for arbitrary terminal coding-agent sessions |

## Command-line toolkit for AI-assisted software engineering

The CLI is often the fastest, most scriptable interface for inspecting repository state,
reviewing changes, and diagnosing CI failures. Learn the tools that remove repeated friction
before collecting a large toolbox. Install only what you use, and check each tool's official
installation instructions for the current operating system and release.

### Start with these tools

| Tool | Best fit | High-value uses |
|---|---|---|
| [GitHub CLI (`gh`)](https://cli.github.com/) | GitHub repositories and pull requests | Inspect PRs, review diffs, check required CI, browse runs, manage issues and releases |
| [GitLab CLI (`glab`)](https://gitlab.com/gitlab-org/cli) | GitLab projects and merge requests | Inspect MRs, pipelines and jobs; create or review MRs; interact with GitLab from scripts |
| [Git](https://git-scm.com/docs) | Source control and recovery | Branches, worktrees, bisect, reflog, and safe change inspection |
| [ripgrep (`rg`)](https://github.com/BurntSushi/ripgrep) + [fd](https://github.com/sharkdp/fd) | Fast code and file search | Find symbols, configuration, tests, and files without noisy recursive output |
| [fzf](https://github.com/junegunn/fzf) | Interactive selection | Filter branches, files, command history, and search results |
| [jq](https://jqlang.org/) + [yq](https://github.com/mikefarah/yq) | Structured data | Inspect and transform JSON/YAML from APIs, test reports, and CI jobs |
| [mise](https://mise.jdx.dev/) | Tool-version management | Pin and activate language/runtime versions per project |
| [just](https://just.systems/) | Repeatable project commands | Expose memorable recipes for lint, tests, notebooks, and local development |
| [direnv](https://direnv.net/) | Per-directory environment variables | Load project environment settings when entering a directory; keep secrets out of version control |

### Install a small Mac-first baseline

With Homebrew installed, a reasonable starting set is:

```bash
brew install gh glab jq yq ripgrep fd fzf mise just direnv
```

This installs several independent tools; it does not configure authentication, project
versions, shell integration, or repository-specific recipes. Follow the official setup
instructions for `gh`, `glab`, `mise`, `direnv`, and `fzf` before relying on them.
On Linux or managed corporate machines, use the approved package manager or installation
method instead of assuming Homebrew or unrestricted network access is available.

### Source-control and CI triage examples

Use the CLI that matches the repository host. Git commands work across both hosts; `gh`
and `glab` are not interchangeable.

```bash
# GitHub: orient, inspect, and verify a pull request
gh pr status
gh pr list
gh pr view 123
gh pr diff 123
gh pr checks 123
gh run list
gh run view <run-id> --log-failed

# GitLab: inspect merge requests and pipeline activity
glab mr list
glab mr view 123
glab ci list
glab ci view

# Find source/configuration and inspect structured output
rg "TODO|FIXME" src tests
fd "config" .
jq '.jobs[] | {name, status}' result.json
```

Replace example IDs and paths with real values. CLI subcommands and flags can vary by
version; check `gh help`, `glab help`, or the linked manuals when a command is unavailable.
For GitLab projects, pipeline visibility also depends on the user's project permissions.

### A reliable agent-assisted PR loop

1. **Inspect before editing:** check the current branch, working tree, and intended base.
2. **Keep parallel tasks isolated:** use one Git worktree per independently writable agent.
3. **Use the host CLI for evidence:** inspect the PR/MR diff and required checks; open failed
   job logs rather than treating a green summary or agent statement as proof.
4. **Verify locally:** run the repository's documented tests, lint, type checks, or build.
5. **Review before mutation:** examine staged and final diffs; explicitly authorize pushes,
   merges, releases, or other consequential actions.
6. **Record what happened:** capture the commit SHA, checks run, failures, and skipped checks.

A CLI command is an interface, not a safety boundary: it acts with the credentials and
permissions of the logged-in user. Authenticate with least privilege, avoid printing tokens
or secret-bearing environment variables, and treat issue/PR text and downloaded artifacts as
untrusted input. Prefer read-only inspection until a write operation is actually needed.

### Add these only when the workflow needs them

| Tool | Add it when | Caution |
|---|---|---|
| [lazygit](https://github.com/jesseduffield/lazygit) | You want a terminal UI for staging, commits, branches, and diffs | Review the resulting diff; the UI does not replace Git knowledge |
| [delta](https://github.com/dandavison/delta) | You want syntax-highlighted, navigable Git diffs | Optional pager/configuration; plain `git diff` remains portable |
| [ShellCheck](https://www.shellcheck.net/) + [shfmt](https://github.com/mvdan/sh) | You maintain shell scripts | Add them to CI where the project can support the tooling |
| [act](https://github.com/nektos/act) | You want to test some GitHub Actions workflows locally | Runner images, secrets, services, and GitHub-hosted behavior may differ; local success is not proof hosted CI will pass |
| [Docker CLI](https://docs.docker.com/reference/cli/docker/) and [kubectl](https://kubernetes.io/docs/reference/kubectl/) | Your project uses containers or Kubernetes | Follow team-approved contexts, namespaces, credential policies, and deployment gates |

**Selection rule:** start with `git`, the host-specific CLI (`gh` or `glab`), `rg`,
`fd`, `fzf`, and `jq`. Add environment/task runners when they make project setup
reproducible. Avoid installing overlapping tools just because they are popular; choose based
on a repeated task, a measurable reduction in friction, and an acceptable security boundary.

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
| [Agent Deck](https://github.com/asheshgoplani/agent-deck) | Agent-aware session command center for Claude Code, Codex, OpenCode, Gemini, and more | Tracks running/waiting/idle sessions, groups and searches sessions, supports session forking and Git worktrees, and adds agent-aware status on top of tmux | Best first evaluation when you need agent-specific status and session operations; it uses tmux and is more opinionated than a plain terminal multiplexer |
| [cmux](https://cmux.com/) | Agent-centric terminal workspaces | Organizes each task in a workspace; keeps coding agents beside tests, logs, and browser surfaces; notifications and agent state are tied to workspace surfaces | Strong alternative if you prefer a native graphical Mac workflow; evaluate platform and remote-workflow requirements |
| [WezTerm](https://wezterm.org/) | A powerful terminal GUI for macOS, Linux, and Windows | Native tabs, panes, workspaces, remote multiplexing, configurable Lua workflows, and a CLI that can spawn or target panes | Excellent general-purpose terminal, but it organizes terminal processes rather than understanding agent tasks or deciding which agent needs attention |
| [tmux](https://github.com/tmux/tmux/wiki) | Persistent terminal sessions, especially over SSH | Mature session/window/pane model; scripts well; sessions survive terminal disconnects | The underlying session layer for Agent Deck; more keyboard- and configuration-oriented when used directly |
| [ccmux](https://ccmux.dev/) | Finding and switching among many agents already running in tmux | Open-source session picker for agent sessions, with search and previews; works with existing tmux habits | A focused, lighter option if you already use tmux; lower priority if Agent Deck covers your needs |
| [Zellij](https://zellij.dev/) | A modern terminal multiplexer alternative | Sessions, panes, tabs, layouts, and plugin support | A credible tmux alternative, but less additive if you choose a tmux-based agent manager |

**Practical starting point:** evaluate Agent Deck first if you need to supervise multiple
OpenCode/Codex sessions and want agent-aware status plus Git worktree support. Choose cmux
instead if you prefer a native graphical Mac workspace. WezTerm is the best general-purpose
terminal choice in this list; add or use tmux directly when durable sessions, remote SSH, or
scripting are the main requirements. Consider ccmux if you want a narrower session picker,
and choose Zellij primarily if you prefer it over tmux as your multiplexer. Avoid adopting
multiple overlapping session managers until you have identified a specific gap.

#### WezTerm: tiled panes versus separate windows

WezTerm's built-in layout model is **panes inside a terminal window**. Split a window
horizontally or vertically to tile shells side by side; resize panes as the workload
changes. Tabs and workspaces organize larger collections of windows and panes. You can
also define repeatable startup layouts with Lua configuration and the `gui-startup` /
`mux-startup` events.

Do not confuse pane tiling with desktop-window management: **WezTerm does not automatically
tile or cascade multiple independent macOS windows** just because they are opened. If you
want separate application windows arranged across the desktop, use a macOS window manager
such as [AeroSpace](https://github.com/nikitabobko/AeroSpace) (keyboard-driven tiling) or
[Rectangle](https://rectangleapp.com/) (manual and shortcut-based window placement).

**A practical multi-agent layout:**
1. Start with one WezTerm window and one pane per active coding-agent session.
2. Keep each agent in its own Git worktree and branch; avoid having agents edit the same
   working tree concurrently.
3. Give each pane a stable task/agent label in your own notes or task tracker. A terminal
   pane is not an agent supervisor: inspect diffs, tests, and tool activity separately.
4. Use a saved Lua startup layout only after the pane arrangement stabilizes. Use a desktop
   tiler only if you specifically need multiple independent windows.

Official references: [WezTerm features and panes](https://github.com/wez/wezterm/blob/main/docs/features.md)
and [WezTerm workspaces and startup layouts](https://wezterm.org/recipes/workspaces.html).

### Live dashboard for agent sessions

[Agent Sessions](https://github.com/ozankasikci/agent-sessions) is a macOS dashboard
for keeping track of multiple Claude Code and OpenCode sessions. It shows live session
states (such as thinking, processing, waiting, and idle), lets you switch to a session,
supports custom session names, and can surface development-server URLs. It supports
iTerm2 and Apple's Terminal.

**Use it when:** the bottleneck is knowing which agent needs attention across many
simultaneous sessions. Pair it with WezTerm or tmux for terminal organization, and keep
each independently writable task in its own Git worktree. Agent Sessions improves
visibility; it does not replace code review, worktree isolation, or CI verification.

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

#### Grok Bot in practice: persistent agents and Slack

Grok Bot is a cloud-computer delegation product, not the same thing as the Grok chatbot or
Grok CLI. Its agents can use a persistent browser, filesystem, terminal, and connectors; they
can continue working while the user's Mac is closed. The macOS app is a control surface, but
the work computer is hosted in the cloud, so this is **not an on-device-only workflow**.

- **Personal Bots:** named agents retain role context and memory. Bots on one account share
  that account's cloud computer, including files, browser sessions, and logins. Do not use
  separate Bots as a security boundary.
- **Team Bots:** publish a configured Bot for teammates to use from Grok Bot or Slack. The
  owner configures shared plugins, secrets, skills, files, and team memory; individual
  conversations remain separate. Treat shared Bot setup and credentials as team-wide access.
- **Slack entry point:** a published Team Bot can be installed as its own Slack app. Teammates
  can DM it or @mention it in channels. It replies to DMs and to mentioned channel/group-DM
  threads; it does not automatically process every top-level channel message unless a
  channel-listener routine is configured. Installation requires the Bot owner/manager to
  connect a Slack workspace, and workspace app-approval rules may apply.
- **Execution boundary:** direct chats and Slack channel/thread conversations can use different
  cloud-computer contexts. Official docs say channel/group-DM threads use a shared computer
  for that Team Bot, so don't place information in a thread that should not be available to
  channel participants or the Bot's shared context.
- **Good first trial:** use a non-sensitive task that produces a draft or report, give it
  read-only access where practical, inspect the result, and only then consider a reusable
  skill or scheduled routine. Require explicit approval for external messages, destructive
  changes, or other consequential actions.
- **Before adoption:** verify current plan eligibility, usage limits, connector permissions,
  retention and training settings, auditability, and company approval. Do not connect work
  repositories, customer data, or credentials to a personal account without authorization.

Official starting points: [Grok Bot overview](https://docs.x.ai/grok-bot/overview) and
[Team Bots and Slack setup](https://docs.x.ai/grok-bot/team-bots).

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

## AI coding environments: OpenCode, Cursor, and VS Code

These tools overlap, but they are not interchangeable. Compare the *control surface*
you want (terminal agent vs. AI-native editor vs. general-purpose IDE), the model and
provider choices available to your account, and the data path approved for the repository.
Product features and plan limits change; use the linked official docs as the current source
of truth rather than treating this comparison as a permanent feature matrix.

### At a glance

| Dimension | [OpenCode](https://opencode.ai/) | [Cursor](https://cursor.com/) | [VS Code](https://code.visualstudio.com/) |
|---|---|---|---|
| Core interaction | Terminal-first coding agent, with a desktop app also available | AI-focused editor with integrated agent workflows | General-purpose editor/IDE; AI experience comes from built-in features, GitHub Copilot, and/or extensions |
| Model flexibility | Provider-oriented; supports multiple hosted providers and local model endpoints where compatible | Model choice depends on Cursor's supported models, account/plan, and feature | Depends on Copilot plan and selected extensions/providers; no single universal model policy |
| Repository context | Agent tools inspect and edit the working tree; configure project instructions and tools | Editor indexing, rules, agent tools, and project context | Language services, workspace search, Copilot/extension context, and repository instructions |
| MCP | Configurable MCP servers and tool permissions | MCP configuration through `.cursor/mcp.json` and the UI | MCP availability and configuration depend on the selected agent/client version |
| Multi-agent work | Primary agents and subagents; pair parallel work with separate Git worktrees | Integrated agent workflows and cloud agents, depending on product/plan | Agent and parallel-session experience depends on Copilot/extension capabilities and version |
| Best reason to choose it | You want a scriptable, terminal-native agent and control over provider routing | You want a cohesive AI-centric editor experience | You want a mature, extensible IDE that can serve non-AI development workflows too |

This is a workflow comparison, not a benchmark. Evaluate on your actual task mix: navigating
an unfamiliar service, implementing a bounded change, diagnosing a failing test, reviewing a
diff, and working behind your organization's proxy and access controls.

### OpenCode: a practical Mac starting point

OpenCode is a strong candidate when you prefer an agent that fits into the terminal and lets
you select among supported model providers. It is still an agent harness: provider choice
does not remove the need to control tools, permissions, and the working directory.

1. **Install from the official instructions.** Use [OpenCode's installation guide](https://opencode.ai/docs/).
   Check the current install method and version rather than copying an old one-liner into a
   managed machine.
2. **Choose the model route deliberately.** Configure an approved hosted provider, or a
   compatible local endpoint if you want local inference. Confirm context-window limits,
   tool-calling support, latency, and license/usage terms. A local model does not imply every
   connected tool or request is local.
3. **Start inside a repository.** Run `opencode` from the project root, inspect the current
   branch and `git status`, and ask the Plan agent to map the relevant code and propose a
   testable plan before allowing edits.
4. **Add durable project guidance.** Use the current OpenCode instructions/configuration
   mechanism to record build commands, test commands, style rules, generated-file boundaries,
   and acceptance criteria. Keep secrets and environment-specific values out of committed
   configuration.
5. **Set permissions intentionally.** OpenCode's documented `permission` settings can allow,
   deny, or ask for approval for tools. For an initial trial, keep edits and shell commands
   approval-gated where practical; do not assume defaults are least-privilege.
6. **Add MCP only for a real need.** Start with one trusted, read-only server. Review its code,
   authentication scopes, network destinations, and returned data before enabling write tools.
7. **Verify the result yourself.** Inspect `git diff`, run the relevant tests and static checks,
   and confirm the working tree contains only intended changes.

Official references: [installation and getting started](https://opencode.ai/docs/),
[agents](https://opencode.ai/docs/agents/), [tools and permissions](https://docs.opencode.ai/docs/tools/),
[models](https://opencode.ai/docs/models/), and [MCP servers](https://opencode.ai/docs/mcp-servers/).

### Cursor and VS Code: when the editor matters

**Cursor** is worth evaluating if you want agent interaction, codebase context, rules, and MCP
configuration integrated in one AI-focused editor. Its docs describe project-level MCP in
`.cursor/mcp.json`, global configuration, and approval controls. Agent changes can save
directly into workspace files, so use version control and review diffs continuously. Check
Privacy Mode, model routing, indexing, and cloud-agent settings against the organization's
data policy before opening a work repository.

**VS Code** is a strong default if you want the broader editor ecosystem and the freedom to
choose an AI experience. Decide explicitly whether you are using GitHub Copilot's agent
features, another extension, or a terminal agent such as OpenCode in the integrated terminal.
Do not assume that all extensions share the same model, context policy, MCP support, or
telemetry behavior. Pin down the extension/version and inspect its current official
documentation before standardizing team instructions.

Official references: [Cursor MCP](https://prod.cursor.com/docs/mcp),
[Cursor agent security](https://prod.cursor.com/docs/agent/security),
[Cursor privacy and data governance](https://prod.cursor.com/docs/enterprise/privacy-and-data-governance),
[VS Code documentation](https://code.visualstudio.com/docs),
[VS Code AI](https://code.visualstudio.com/docs/copilot/overview),
and [GitHub Copilot coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent).

### A repeatable evaluation for your team

Run the same small set of tasks in each candidate, using the same repository snapshot and
acceptance tests:

- **Explore:** explain a call path and identify the files/tests that establish the behavior.
- **Change:** implement a bounded feature with explicit non-goals and acceptance criteria.
- **Debug:** diagnose a failing test from logs and propose a falsifiable root cause before editing.
- **Review:** find defects in a supplied diff without modifying it.
- **Tool use:** invoke one approved MCP tool and show the evidence used.
- **Recovery:** stop an incorrect run, inspect partial changes, and restore a clean state.

Record task success, escaped defects, test pass rate, time to a reviewable diff, manual correction
time, token/API cost, context loss, and unsafe or unnecessary tool calls. Use a fixed commit,
fixed instructions, and repeat trials; one impressive demo is not a benchmark.

### Shared safety and parallel-work rules

- **One writable Git worktree per concurrent coding task.** Multiple panes or IDE windows
  pointing at the same directory do not isolate edits.
- Keep `.env`, credentials, proprietary datasets, and restricted files out of model context
  unless the exact product/provider path is approved. Review ignore/exclusion rules, but do not
  treat them as a complete security boundary.
- Treat MCP servers, extensions, skills, hooks, shell commands, and repository instructions as
  executable or influence-bearing inputs. Install only trusted components and grant the minimum
  permissions needed.
- Separate planning/review from implementation when possible. Use read-only review mode first;
  require human review for changes, dependency updates, external messages, and destructive actions.
- Verify proxy/certificate behavior, model endpoints, telemetry, retention, and licensing on the
  managed workstation. "Uses my API key" or "runs in the terminal" does not by itself prove that
  source code stays local.
- Before merging, review the diff, run tests, and check generated artifacts. An agent's claim that
  tests passed is not evidence unless you can inspect the command and result.

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

### Capture a Slack message as a task

If the goal is to turn a specific Slack message into a personal follow-up, [Todoist's official
Slack integration](https://www.todoist.com/help/todoist/integrations/use-slack-with-todoist)
is the most direct documented option:

1. Authorize Todoist for the intended Slack workspace.
2. Open the message's **More actions** menu (three dots) and choose **Add a task**.
3. Edit the task title, project, priority, and due date as needed. The integration also supports
   the `/todoist` command for creating tasks directly in Slack.
4. **Verify the backlink:** Todoist's guide confirms message-to-task creation, but does not
   guarantee in every client/version that the resulting task preserves a clickable permalink to
   the exact source message. Test this with a non-sensitive message on both desktop and mobile
   before relying on it. If the link is missing, use a supported automation/API workflow that
   explicitly writes the Slack permalink into the task description.

| Destination | Slack capture pattern | Link-preservation note |
|---|---|---|
| [Todoist](https://todoist.com/) | Native Slack message menu → Add a task | Best first test; verify the resulting task links back to the exact message |
| [Microsoft To Do](https://to-do.office.com/) | Automation such as Power Automate or a third-party connector, where supported | Map Slack's message permalink into a task notes field explicitly; test authentication, thread links, and workspace policy |
| [Apple Reminders](https://support.apple.com/guide/reminders/welcome/mac) | Shortcut or custom automation | Possible, but generally requires custom capture logic to carry the Slack permalink; not a native Slack workflow |

Todoist and Microsoft To Do are cloud-backed services, not strict local-only stores. Apple
Reminders is native to Apple platforms but may sync through iCloud. For confidential work,
use only company-approved apps and connectors; the source permalink may itself expose
restricted conversation context to anyone who can open the task.

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


## Agent skills, MCP servers, and plugins

These are different layers. Keep the distinction explicit when evaluating or teaching an
AI-assisted development setup:

- **Skill:** reusable instructions, examples, and optionally scripts that teach an agent
  how to perform a workflow. A skill should state when to use it, required inputs,
  procedure, verification, and stop conditions.
- **MCP server:** a protocol-level integration that exposes tools, resources, or prompts
  to a compatible client. It supplies capabilities; it does not guarantee that an agent
  will use them correctly.
- **Plugin/extension:** a product-specific package that can bundle skills, commands,
  hooks, MCP configuration, or other integrations. Names and packaging differ by host.
- **Agent:** the runtime that reasons, selects tools, applies instructions, and proposes
  changes. The harness and human review still own permissions and acceptance.

### Skills worth evaluating

| Skill or project | Use case | Adoption guidance |
|---|---|---|
| [OpenCode skills](https://opencode.ai/docs/skills) | Discover reusable `SKILL.md` instructions in a coding workflow | Good starting point for the repo's CLI-first path; check current discovery paths and frontmatter requirements |
| [Agent Skills specification](https://agentskills.io/) | Share skills across compatible agent products | Prefer portable instructions and explicit tool assumptions; test behavior in each host rather than assuming identical support |
| [Superpowers](https://github.com/obra/superpowers) | Structured development workflow: clarify requirements, plan, test-driven development, debugging, and review | Evaluate the actual skill/plugin version and host support; adopt only workflows that improve measured outcomes |
| Team-owned skills in `.agents/skills/` | Encode repo-specific test, review, debugging, and PR procedures | Version-control them with the project; keep secrets out, scope them narrowly, and require commands/tests to be independently verified |

The repository includes starter examples under `.agents/skills/`. They are teaching artifacts,
not privileged automation: read them, adapt their commands to the project, and verify every
result. Skills should not silently bypass approval gates or claim that tests passed without
running them.

### MCP servers and plugins worth evaluating

| Integration | Why it is useful | Guardrail |
|---|---|---|
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | Issues, pull requests, repository context, and review workflows through MCP | Start with least-privilege/read-only access where possible; separate review from write/merge authority |
| [Context7](https://github.com/upstash/context7) | Retrieve library documentation relevant to a framework or package | Pin or identify library versions; check retrieved content against official docs and lockfiles |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Inspect and debug MCP server capabilities and exchanges | Use a non-sensitive test environment and test unauthorized and malformed requests |
| [Claude Code plugins](https://docs.anthropic.com/en/docs/claude-code/plugins) | Example of a product-specific package for commands, skills, hooks, and integrations | Do not assume a Claude Code plugin installs or behaves identically in OpenCode, Cursor, or VS Code |
| [Cursor plugins](https://docs.cursor.com/plugins) | Product-specific packaging for Cursor workflows | Review permissions, scripts, remote endpoints, and version/update behavior before enabling |

Links and feature names can change quickly; verify the current official documentation before
installing. A marketplace listing is not a security audit.

### Four starter skills in this repository

The sample skills are intentionally agent-agnostic and require the agent to report evidence,
not just conclusions:

1. **Code review:** identify correctness, regression, security, and maintainability risks;
   cite exact changed lines and distinguish confirmed defects from questions.
2. **Evidence-first debugging:** state competing hypotheses, gather discriminating evidence,
   and avoid editing code until the failure mechanism is sufficiently supported.
3. **Test and evaluate:** map acceptance criteria to deterministic tests, run the relevant
   checks, and report failures, skipped checks, and environmental limits.
4. **PR preparation:** inspect the diff, summarize behavior and risk, verify tests, and leave
   merging/deployment as a separate authorized decision.

### Safe evaluation checklist

Before enabling any skill, plugin, or MCP server:

- Inspect its source, scripts, dependencies, update mechanism, and network destinations.
- Record which files, shell commands, credentials, and external systems it can access.
- Start with read-only and least-privilege access; require approval for writes, releases,
  external messages, and destructive actions.
- Test prompt-injection resistance using untrusted repository text and tool output.
- Run it on a disposable branch or fixture repository before using production code.
- Measure task success, regression rate, review findings, tool failures, and cost.
- Keep a human-owned verification gate; never treat the agent's self-reported success as proof.
