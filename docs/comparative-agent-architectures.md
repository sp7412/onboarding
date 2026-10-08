# Comparative Agent Architectures

**Estimated reading time:** 20 minutes · **Facts checked:** October 7, 2026

This doc compares public engineering approaches from ServiceTitan, Salesforce,
Microsoft, OpenAI, and Anthropic. It is deliberately comparative: the goal is not to
declare one framework "best", but to understand where each system puts reasoning,
orchestration, state, tools, governance, and evaluation. It builds on
[whitepaper chapter 15](whitepaper/15-agentic-orchestration.md), which covers the coordination
problem and the MCP/A2A split in more depth; this doc adds the harness and evaluation view.

> **Evidence boundary:** ServiceTitan's public material describes product capabilities and
coordination concepts, but not its private implementation. Where this chapter presents a
ServiceTitan architecture, it is labeled as analysis or a reference design rather than an
internal fact. Vendor descriptions are the vendors' own and are cited by number.

## 1. The common problem

All five approaches are trying to solve some version of the same problem:

> How do you turn an LLM into a reliable system that can reason, use tools, coordinate
> work, maintain context, and improve without allowing every model decision to become an
> uncontrolled side effect?

The implementations differ substantially.

| System | Primary abstraction | Coordination emphasis | Control emphasis | Evaluation emphasis |
|---|---|---|---|---|
| **ServiceTitan / Max** | Domain agents + shared context/judgment [1] | Arbitration + centralized supervision [1] | Business-level coordination | Not publicly specified |
| **Salesforce Agentforce** | Primary/superagent + specialists [2] | SOMA/MOMA [2] | Agent Gateway, trust boundaries [2] | Not covered by the cited source |
| **Microsoft Agent Framework** | Agents + explicit workflows + agent harness [3][5] | Workflow orchestration patterns [4] | Harness, middleware, approvals [5] | Agent and workflow evaluators [12] |
| **OpenAI Agents SDK** | Agents + tools + handoffs [6] | Handoffs / agents-as-tools [6] | Guardrails + human review [7] | Traces → graders → datasets → eval runs [9] |
| **Anthropic** | Workflows vs. agents; start with the simplest pattern [11] | Composable workflow patterns, agents only when needed [11] | Agent harness and evaluation harness as named concepts [10] | Grade outcomes; read transcripts to check the graders [10] |

The key difference is **where the control plane lives**.

## 2. ServiceTitan: domain operating system

ServiceTitan publicly describes Max as 30 agents across 18 business drivers, coordinated
through shared context, shared judgment, coordinated action, arbitration, and centralized
supervision [1]. Chapter 15, section 3, walks through each public claim.

The conceptual model is:

```text
                     EXPERIENCE
                  voice / web / app
                         |
                         v
              +----------------------+
              |   MAX COORDINATION   |
              | context / judgment   |
              | arbitration / policy |
              | supervision          |
              +----------+-----------+
                         |
              +----------+----------+
              |          |          |
              v          v          v
           Voice      Booking    Dispatch
           Agent       Agent       Agent
              |          |          |
              +----------+----------+
                         |
                         v
                   BUSINESS STATE
                         |
                         v
                  TOOLS / SYSTEMS
```

This is best understood as a **domain-specific AI operating system**: the interesting
unit is not merely an agent runtime, but a coordinated set of business capabilities.

The implementation is not public. In particular, do not turn the diagram above into a
claim about internal databases, queues, model routing, or service boundaries.

### What is distinctive

ServiceTitan's public framing puts unusually strong emphasis on **system-level outcomes**.
A booking agent optimizing booking probability can be locally correct while harming
technician utilization or travel. Arbitration exists to resolve those competing objectives.

**Lesson:** once multiple agents can affect the same business outcome, local agent quality
is necessary but insufficient.

## 3. Salesforce: agent platform + trust boundaries

Salesforce's Agentforce documentation makes the layers unusually explicit [2].

### SOMA

**Single-Org Multi-Agent** uses a primary/superagent to delegate to specialist agents
within one Salesforce org.

```text
                    USER
                      |
                      v
              +---------------+
              | SUPERAGENT    |
              +-------+-------+
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Sales       Service     Specialist
       Agent        Agent        Agent
```

### MOMA

**Multi-Org Multi-Agent** extends the model across Salesforce org boundaries while
preserving trust and user identity constraints.

### Protocols versus architecture

Salesforce explicitly separates:

- **SOMA/MOMA:** how agents are organized;
- **MCP:** agent-to-tool/data connectivity;
- **A2A:** agent-to-agent interoperability;
- **Agent Gateway:** governance and control.

```text
ARCHITECTURE
  SOMA / MOMA
       |
       +----------------------+
                              |
PROTOCOLS                     |
  MCP  <---- tools/data       |
  A2A  <---- agents           |
                              v
GOVERNANCE
  Agent Gateway
  auth / policy / quotas /
  schema validation / visibility
```

That separation is valuable because it prevents a common category error:

> **MCP is not orchestration. A2A is not governance.** (Chapter 15, section 18, explains
> both protocols from their specifications.)

Salesforce's public documentation describes its Agent Gateway as the governance layer for
MCP and A2A interactions [2].

### When this model fits

This model is particularly compelling when an enterprise has:

- multiple business domains;
- multiple organizational trust boundaries;
- many agents owned by different teams;
- interoperability requirements;
- centralized governance requirements.

## 4. Microsoft: explicit workflows plus a harness

Microsoft Agent Framework is the clearest example of separating **open-ended agent
reasoning** from **explicit workflow execution**.

Microsoft's current guidance says to use an agent when the task is open-ended or requires
autonomous planning, and a workflow when execution order is well-defined [3].

Supported workflow orchestration patterns include [4]:

- sequential;
- concurrent;
- handoff;
- group chat;
- Magentic/manager-driven orchestration.

```text
Sequential:    A ---> B ---> C

Concurrent:    A --\
               B ----+---> Aggregate
               C --/

Handoff:       A ---> B ---> C

Manager:             +---------+
                     | Manager |
                     +----+----+
                          |
                    +-----+-----+
                    |     |     |
                    v     v     v
                    A     B     C
```

### The agent harness

Microsoft also now uses **agent harness** as an explicit runtime concept (`HarnessAgent` in
.NET, `create_harness_agent` in Python). Its documented architecture combines [5]:

1. chat client;
2. chat pipeline;
3. agent/context providers;
4. middleware/decorators;
5. application UX.

Capabilities include state/context management, tool invocation with an iteration limit,
approval handling, observability, compaction, and optional bounded re-invocation (some
capabilities, such as looping and background agents, are still experimental) [5].

This is important for our onboarding material because "harness" is no longer merely a
metaphor. Microsoft defines an agent harness as "the runtime scaffolding that turns a
language model into an agent that can perform work" [5].

### When this model fits

Use explicit workflows when you know the process:

```text
if you can write a deterministic function,
prefer the function.

if the order is known,
prefer a workflow.

if the next action depends on model reasoning,
use an agent.

if both are needed,
put agents inside an explicit workflow.
```

That is a much more useful design heuristic than "use an agent framework."

## 5. OpenAI: minimal agent primitives plus control surfaces

The OpenAI Agents SDK intentionally exposes a small set of primitives [6]:

- agents;
- tools;
- agents-as-tools / handoffs;
- guardrails;
- sessions/state;
- human-in-the-loop;
- tracing.

The runtime can therefore be viewed as:

```text
Agent
  |
  +--> model
  +--> tools
  +--> handoffs
  +--> sessions
  +--> guardrails
  +--> human approval
  +--> tracing
```

OpenAI makes the control boundaries particularly explicit:

- input guardrails;
- output guardrails;
- tool guardrails;
- human approval before sensitive side effects [7].

Tracing records model calls, tool calls, handoffs, guardrails, and custom spans [8].

OpenAI's evaluation guidance then moves from individual traces to repeatable datasets and
eval runs [9]:

```text
Production / test run
        |
        v
      Trace
        |
        v
      Grader
        |
        v
   Dataset
        |
        v
     Eval run
```

### When this model fits

This is attractive when the application team wants to own the surrounding product system:
deployment, tool implementations, state storage, approval decisions, and infrastructure,
while the SDK supplies the agent loop and common control primitives.

## 6. Anthropic: simple patterns first, and evals that grade outcomes

Anthropic's public engineering writing makes two points that complement the others.

**Start with the simplest pattern.** *Building Effective Agents* distinguishes *workflows*,
where models and tools follow predefined code paths, from *agents*, which direct their own
process, and recommends the simplest solution that works, adding agentic complexity only
when it pays for itself [11]. That is the same heuristic as Microsoft's agents-versus-workflows
guidance [3].

**Grade what the agent produced.** *Demystifying evals for AI agents* separates the
**transcript** (the full record of a trial: outputs, tool calls, reasoning and intermediate
results) from the **outcome** (what actually changed in the environment). Its example: a
flight-booking agent may say it succeeded, but the outcome is whether a reservation exists
in the database. It advises that "it's often better to grade what the agent produced, not the
path it took," because many different paths can be valid, and it treats reading transcripts
as the way to check that the graders themselves are working [10].

```text
Goal --> Agent --> tool calls, retries, messages   (transcript: read it to debug and to
                         |                            check the graders)
                         v
              Environment state                    (outcome: grade this first)
```

Trajectory checks still have a place: when a step is itself a policy (never call
`create_job` before the caller confirms), check that step directly. The same article
defines the **agent harness** (the system that lets a model act as an agent) and the
**evaluation harness** (the infrastructure that runs evals end to end), and argues that without
evals teams get stuck in reactive loops, while evals "make problems and behavioral changes
visible before they affect users" [10].

## 7. What is actually different?

The approaches overlap heavily at the component level. The architectural differences are
more useful:

### ServiceTitan

**Optimizes:** the business system.

The agent is a participant in a domain operating system. Shared judgment and arbitration
matter because multiple business objectives interact.

### Salesforce

**Optimizes:** enterprise agent composition across trust boundaries.

The strongest conceptual contribution is the clean separation of architecture (SOMA/MOMA),
protocols (MCP/A2A), and governance (Agent Gateway).

### Microsoft

**Optimizes:** explicit execution topology.

The strongest contribution is making workflows first-class and distinguishing deterministic
coordination from open-ended agent reasoning.

### OpenAI

**Optimizes:** a small, composable runtime.

The strongest contribution is a compact set of primitives with explicit guardrails, human
review, tracing, and evaluation surfaces.

### Anthropic

**Optimizes:** the simplest system that works, verified by its outcomes.

The strongest contribution is the discipline: prefer workflows until an agent earns its
complexity, and grade the state the agent left behind rather than the story it tells.

## 8. The synthesis for this onboarding repo

The most useful architecture is not "pick one vendor."

It is a layered synthesis:

```text
                    USER / VOICE
                         |
                         v
                +------------------+
                | INPUT CONTROLS   |
                | validation       |
                | auth / context   |
                +--------+---------+
                         |
                         v
                +------------------+
                | ORCHESTRATION    |
                | route / workflow |
                | handoff          |
                | arbitration      |
                +--------+---------+
                         |
                         v
                +------------------+
                | AGENT / MODEL    |
                | reason / propose  |
                +--------+---------+
                         |
                         v
                +------------------+
                | CONTROL HARNESS  |
                | policy           |
                | permissions      |
                | schema           |
                | state validation |
                | risk             |
                | idempotency      |
                | approval         |
                +--------+---------+
                         |
                         v
                    TOOLS / APIs
                         |
                         v
                +------------------+
                | TRACE + OUTCOME  |
                +--------+---------+
                         |
                         v
                  EVALUATION LOOP
                         |
                         +------> design change
```

This is **our reference architecture**, not a claim that any one company implements it
exactly this way.

## 9. Design questions to ask

When designing a new capability, ask these in order:

1. **Can this be deterministic?** If yes, write the function/workflow.
2. **Does the system need model-driven choice?** If yes, introduce an agent.
3. **Is one agent overloaded?** Split responsibilities into specialists.
4. **Do specialists need common facts?** Create typed shared state.
5. **Can proposals conflict?** Add deterministic arbitration.
6. **Can an action create a side effect?** Put it behind the control harness.
7. **Does the action need approval?** Add HITL at the side-effect boundary.
8. **Can you observe the decision?** Trace the entire trajectory.
9. **Can you prove the behavior?** Create an evaluation before rollout.
10. **Can a new version regress another consumer?** Run per-agent and system-level evals.

## 10. Bottom line

The common mistake is to treat "agent" as the architecture.

It is only one layer.

A production system is closer to:

> **reasoning + orchestration + state + tools + control + observability + evaluation.**

The most transferable lesson from comparing these companies is therefore not a particular
framework. It is knowing **where deterministic control should replace model discretion** and
where evaluation should constrain architecture.

## Sources

Checked October 7, 2026. Vendor descriptions are each vendor's own.

1. ServiceTitan, Pantheon 2026 public materials: see [whitepaper chapter 15](whitepaper/15-agentic-orchestration.md) (sources 1–2) and the [Pantheon 2026 brief](pantheon-2026-ai-roadmap.md)
2. [Salesforce Help: SOMA, MOMA, A2A and MCP](https://help.salesforce.com/s/articleView?id=005317683&language=en_US&type=1)
3. [Microsoft Agent Framework overview (agents vs. workflows)](https://learn.microsoft.com/en-us/agent-framework/overview/)
4. [Microsoft Agent Framework: workflow orchestrations](https://learn.microsoft.com/agent-framework/workflows/orchestrations)
5. [Microsoft Agent Framework: agent harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness)
6. [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/)
7. [OpenAI: guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
8. [OpenAI Agents SDK (Python): tracing](https://openai.github.io/openai-agents-python/tracing/)
9. [OpenAI: evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)
10. [Anthropic: Demystifying evals for AI agents (January 9, 2026)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
11. [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
12. [Microsoft Agent Framework: evaluation](https://learn.microsoft.com/agent-framework/agents/evaluation)
