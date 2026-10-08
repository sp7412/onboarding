# Comparative Agent Architectures

**Estimated reading time:** 20 minutes · **Facts checked:** October 7, 2026

This chapter compares public engineering approaches from ServiceTitan, Salesforce,
Microsoft, OpenAI, and Anthropic. It is deliberately comparative: the goal is not to
declare one framework "best", but to understand where each system puts reasoning,
orchestration, state, tools, governance, and evaluation.

> **Evidence boundary:** ServiceTitan's public material describes product capabilities and
coordination concepts, but not its private implementation. Where this chapter presents a
ServiceTitan architecture, it is labeled as analysis or a reference design rather than an
internal fact.

## 1. The common problem

All five approaches are trying to solve some version of the same problem:

> How do you turn an LLM into a reliable system that can reason, use tools, coordinate
> work, maintain context, and improve without allowing every model decision to become an
> uncontrolled side effect?

The implementations differ substantially.

| System | Primary abstraction | Coordination emphasis | Control emphasis | Evaluation emphasis |
|---|---|---|---|---|
| **ServiceTitan / Max** | Domain agents + shared context/judgment | Arbitration + centralized supervision | Business-level coordination | Outcomes, supervision, learning loop |
| **Salesforce Agentforce** | Primary/superagent + specialists | SOMA/MOMA | Agent Gateway, trust boundaries | Platform governance + agent quality |
| **Microsoft Agent Framework** | Agents + explicit workflows + Harness Agent | Graph/workflow orchestration | Harness, middleware, approvals | Built-in agent/workflow evaluation |
| **OpenAI Agents SDK** | Agents + tools + handoffs | Handoffs / agents-as-tools | Guardrails + human review | Traces → graders → eval runs |
| **Anthropic** | Agents + tools + harnesses | Model-driven loops / multi-agent patterns | Permissions, sandboxing, harness design | Trajectory-aware evals and regression |

The key difference is **where the control plane lives**.

## 2. ServiceTitan: domain operating system

ServiceTitan publicly describes Max as a coordinated system of more than 30 agents
across business drivers, with shared context, shared judgment, coordinated action,
arbitration, and centralized supervision.

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

Salesforce's Agentforce documentation makes the layers unusually explicit.

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

> **MCP is not orchestration. A2A is not governance.**

Salesforce's public documentation says its Agent Gateway governs MCP and A2A interactions,
including registry, policy, authentication, quotas, and validation.

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
autonomous planning, and a workflow when execution order is well-defined.

Supported workflow patterns include:

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

### The Harness Agent

Microsoft also now uses **Agent Harness** as an explicit runtime concept. Its documented
architecture combines:

1. chat client;
2. chat pipeline;
3. agent/context providers;
4. middleware/decorators;
5. application UX.

Capabilities include state/context management, tool invocation, approval handling,
observability, compaction, and bounded multi-step execution.

This is important for our onboarding material because "harness" is no longer merely a
metaphor. Microsoft defines it as runtime scaffolding that turns a language model into an
agent capable of sustained work.

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

The OpenAI Agents SDK intentionally exposes a small set of primitives:

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
- human approval before sensitive side effects.

Tracing records model calls, tool calls, handoffs, guardrails, and custom spans.

The evaluation path then becomes:

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
   Eval dataset
        |
        v
     Eval run
```

### When this model fits

This is attractive when the application team wants to own the surrounding product system:
deployment, tool implementations, state storage, approval decisions, and infrastructure,
while the SDK supplies the agent loop and common control primitives.

## 6. Anthropic: harness engineering and trajectory evaluation

Anthropic's public engineering work emphasizes a related but slightly different lesson:
long-running agents require **harness engineering**, not just better prompts.

An agent may:

1. inspect state;
2. call tools;
3. modify state;
4. observe results;
5. revise its plan;
6. continue for many turns.

Therefore evaluating only the final answer misses important failure modes.

```text
Goal
 |
 v
Agent
 |
 +--> tool --> result
 |       |
 +-------+
 |
 +--> tool --> result
 |
 +--> state change
 |
 v
Final result
```

An effective evaluation should be able to inspect the **trajectory**, not merely the
final string:

- did it select the correct tool?
- were arguments valid?
- did it recover from a tool failure?
- did it take an unnecessary action?
- did it violate a policy mid-run?
- did the final success depend on a lucky recovery?

Anthropic's 2026 eval guidance explicitly frames evals as a way to avoid reactive production
loops and to make behavioral changes visible before deployment.

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

**Optimizes:** reliable long-running autonomy.

The strongest contribution is treating the harness, permissions, context engineering, and
trajectory evaluation as first-class engineering concerns.

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

1. ServiceTitan, Pantheon 2026 public materials — see [Chapter 15](15-agentic-orchestration.md)
   for the repo's source ledger and evidence boundary.
2. [Salesforce Help — SOMA, MOMA, A2A and MCP](https://help.salesforce.com/s/articleView?id=005317683&language=en_US&type=1)
3. [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
4. [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness)
5. [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
6. [OpenAI Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
7. [OpenAI tracing](https://openai.github.io/openai-agents-js/guides/tracing/)
8. [OpenAI agent workflow evaluation](https://developers.openai.com/api/docs/guides/agent-evals)
9. [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
