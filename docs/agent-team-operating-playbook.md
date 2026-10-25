# Agent Team Operating Playbook

A vendor-neutral field guide for building reliable multi-agent workflows without
confusing more agents with more progress. This guide synthesizes transferable
operating patterns from the [GrokBot Field Manual](https://mikesblogdesign.com/grokbotfieldmanual/)
and connects them to this repository's agent harness, multi-agent labs, and
design-by-evaluation material. Product-specific Grok Bot limits and UI behavior
are not treated as general facts.

## Five takeaways

1. **Start with one coordinator and one bounded job.** Add specialists only when
   a measured bottleneck or distinct responsibility justifies them.
2. **A bot is a role with a contract, not a personality.** Specify its job,
   evidence sources, decision rule, deliverable, forbidden actions, and escalation.
3. **Chat is not durable state.** Handoffs must carry evidence and point to
   durable artifacts; completion must be independently checkable.
4. **Promote autonomy gradually.** Run manually, correct errors, evaluate the
   repeatable procedure, then schedule it with approvals, monitoring, and rollback.
5. **Permission boundaries beat screen boundaries.** Shared VMs, files, browser
   sessions, credentials, and connector scopes can turn convenience into shared
   blast radius. Treat every skill and tool as executable code with permissions.

## 1. Build the smallest useful team

Use a coordinator to route work, track status, gather deliverables, and escalate.
It should not silently become another specialist that performs every task itself.

Create a specialist when at least one of these is true:

- The task has a distinct input/output contract and stable ownership.
- It needs a materially different tool or permission set.
- Independent review improves the quality or safety of a consequential result.
- Parallel execution reduces measured end-to-end latency without creating
  coordination overhead that outweighs the benefit.

Do not create agents just to mirror organizational titles. A single well-scoped
workflow with deterministic tools may be simpler, cheaper, and more reliable than
a swarm.

### Specialist contract

Every specialist should have an explicit contract:

| Field | Required question |
|---|---|
| Job | What outcome does this specialist own? |
| Sources | Which sources are authoritative, and what evidence must be retained? |
| Judgment | How is the result validated; when must it abstain? |
| Output | What artifact or structured result must it return? |
| Forbidden | Which tools, side effects, data, and decisions are out of bounds? |
| Escalation | What uncertainty, failure, or approval requirement stops the run? |

Keep the contract versioned alongside the workflow. A prompt alone is not an
authorization system; enforce permissions and invariants in the harness.

## 2. Make handoffs durable

A handoff should not require the receiving agent to reconstruct the task from a
long conversation. Use a durable artifact in the repository, task tracker, or
approved workspace. A minimal HANDOFF.md can use this template:

~~~markdown
# Handoff

- Task: <requested outcome>
- Status: complete | partial | blocked
- Owner: <current owner>
- Next owner: <who continues>
- Deliverable: <path or stable URL>
- Evidence: <source links, test output, timestamps, trace IDs>
- Decisions: <important choices and rationale>
- Uncertainties: <what is not yet established>
- Blockers: <dependency, permission, or missing input>
- Next action: <one concrete action>
- Do-not-assume: <facts that must be rechecked>
~~~

The artifact is the handoff; chat is a notification and discussion surface. Keep
secrets and sensitive customer or company data out of public repositories and
unapproved artifacts.

### Define completion so a model cannot self-certify

Prefer externally verifiable conditions:

- A required file exists and passes schema/format checks.
- A test suite or regression case passes.
- A pull request is actually open, with the expected base and changed files.
- An authoritative system confirms the intended state transition.
- A reviewer has approved a consequential action.

Record the evidence. “The agent says it ran” is not evidence that it ran.

## 3. Separate shared workspace from security boundaries

Some hosted agent products deliberately share a persistent VM or browser state
between agents. That can make handoffs efficient, but a separate screen or bot
identity does **not** necessarily imply isolation.

Before connecting an agent to tools, establish:

- Whether filesystem, browser cookies, CLI credentials, environment variables,
  and sessions are shared across agents.
- Which principal the external service sees, and what each connector can read or
  mutate.
- Whether imported skills can execute commands or access signed-in sessions.
- Where durable files live and which locations are ephemeral.
- How logs, traces, transcripts, and artifacts are retained and redacted.
- How to revoke access, rotate credentials, and investigate a compromised skill.

Use least privilege, scoped identities, short-lived credentials where available,
and explicit approval for sending messages, spending money, publishing, deleting,
or changing authoritative business state. Never paste passwords or one-time codes
into prompts or transcripts.

For ServiceTitan-style voice workflows, the application control plane remains
responsible for authorization, evidence grounding, idempotency, policy, and
escalation; model-generated tool calls are proposals, not permission.

## 4. Promote work into automation in stages

Do not schedule an unproven task just because the first run looked successful.

~~~text
Manual task
    -> correct observed failures
    -> write a repeatable skill / workflow
    -> test with safe inputs and explicit assertions
    -> shadow or supervised runs
    -> scheduled automation with bounded permissions
    -> monitored promotion or rollback
~~~

At each transition, preserve representative examples and add regression tests
for mistakes. A learned procedure needs, at minimum:

- Trigger and intended use.
- Required inputs, sources, and permissions.
- Steps and decision points.
- Validation and stop conditions.
- Output contract and destination.
- Side effects that require human approval.
- Missing-data, timeout, retry, and recovery behavior.

A “test run” may still perform real work. Use a sandbox when available; otherwise
choose safe inputs and keep consequential writes behind approval. Retries must be
idempotent, and delayed completion must be checked before resubmitting an action
that could duplicate a message or transaction.

## 5. Budget operations, not just model tokens

Agent systems also consume connector calls, browser sessions, wall-clock time,
parallel capacity, and human review. Repeated polling or syncing can dominate the
cost of an otherwise small workflow.

- Batch reads and syncs when freshness requirements permit.
- Prefer event-driven triggers over tight polling where the integration supports them.
- Set per-run and per-day budgets for time, tool calls, retries, and spend.
- Track queue time, execution time, handoff latency, retries, failures, and review
  burden separately.
- Preserve a run summary with inputs, versions, evidence, outcomes, and cost.
- Fail visibly on missing or stale data; never silently substitute a remembered value.
- Test concurrency and duplicate delivery, not just the happy path.

Measure whether adding a specialist improves end-to-end outcomes. Parallelism is
not free: contention, duplicate work, and review costs can erase the apparent gain.

## 6. Independent review and feedback

The producer should not be the only judge of its output when correctness matters.
Use deterministic assertions for hard invariants, an independent evaluator for
graded qualities, and human review for high-impact or ambiguous decisions.

When a result is wrong, turn the correction into a testable change:

1. Preserve the failed example and the evidence.
2. Classify the failure: missing source, bad judgment, tool failure, stale state,
   permission error, or unclear contract.
3. Update the source data, contract, policy, or workflow—not just the chat.
4. Add a regression case and compare against a held-out set.
5. Roll out gradually and monitor for regressions.

Do not convert every user edit into a global preference or shared skill. Corrections
may be factual, tenant-specific, stylistic, or policy-related and should be routed
to the right owner.

## 7. First-week rollout checklist

- [ ] Pick one repetitive, low-risk task with a measurable outcome.
- [ ] Run it manually and collect representative failures.
- [ ] Write the specialist contract and durable handoff artifact.
- [ ] Verify tool permissions, credential scope, data retention, and shared-state risks.
- [ ] Add deterministic acceptance checks and an independent review where warranted.
- [ ] Test missing data, timeouts, retries, duplicate triggers, and partial completion.
- [ ] Run supervised repetitions and track cost, latency, and correction rate.
- [ ] Schedule only after it passes the acceptance criteria.
- [ ] Keep consequential side effects approval-gated.
- [ ] Define an owner, alert, kill switch, rollback path, and review date.
- [ ] Add a second specialist only after evidence shows a real need.

## How this fits the onboarding path

- **Architecture:** [Agent harness](agent-harness.md) and
  [voice-agent architecture](voice-agent-architecture.md) define the control
  plane and side-effect boundary.
- **Coordination:** labs [09](../labs/09_shared_context.ipynb), [10](../labs/10_coordination_and_arbitration.ipynb), [11](../labs/11_learning_loop.ipynb), and [12](../labs/12_agent_to_agent_booking.ipynb) cover shared context, arbitration, learning, and
  agent-to-agent workflows.
- **Autonomy:** [lab 14](../labs/14_earning_autonomy.ipynb) and [Earning autonomy](earning-autonomy.md) cover
  evidence-based promotion and demotion.
- **Evaluation:** [lab 15](../labs/15_llm_judge.ipynb) and [Design by evaluation](design-by-evaluation.md)
  turn failures into regression tests and staged releases.
- **External tools:** [MCP and external-agent trust boundary](mcp-and-external-agent-trust-boundary.md)
  covers authorization, consent, idempotency, injection, and audit.

The Grok Bot article is a useful operational case study, not a universal platform
specification. Verify product-specific limits, connector behavior, and persistence
guarantees against current official documentation before relying on them.
