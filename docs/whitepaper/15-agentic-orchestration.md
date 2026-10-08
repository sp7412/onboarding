# 15 - Agentic Orchestration: From Single Agents to an AI Operating System

**Estimated reading time:** 31 minutes (essentials path: 12 minutes) · **Facts as of:** October 7, 2026

**Audience:** engineers who understand ML and LLMs but are new to multi-agent production systems.
ServiceTitan material is separated into **public claim** and **analysis/hypothesis** throughout;
no internal ServiceTitan architecture is asserted.

## Five Takeaways

1. Many specialist agents fail by **local optimization**: each makes a reasonable choice and the business still loses. Orchestration (shared context, shared judgment, arbitration, supervision) is the fix.
2. ServiceTitan publicly describes Max as 30 agents across 18 business drivers, coordinated through shared context, shared judgment, coordinated action, arbitration and centralized supervision [1][2]. How it is built is not public.
3. Salesforce organizes the same problem as a primary agent delegating to specialists, with MCP and A2A as protocols and an Agent Gateway for governance [3][4]; Microsoft Agent Framework makes the topology explicit as workflows (sequential, concurrent, handoff, group chat, Magentic) [5][6].
4. MCP and A2A are connectivity, not orchestration. Arbitration, policy and side effects belong to deterministic application code: the model proposes, the harness controls.
5. Running these agents in production (traces, failure mining, evaluation, canary rollout) is chapter 17. ServiceTitan's job listings name Kafka, Snowflake and Airflow in its data platform [7][8]; their role in agent telemetry is a hypothesis.

> **Essentials path (12 minutes):** read sections 1–6 for the problem and the three approaches,
> section 13 ("Arbitration does not have to be an LLM") and section 14 ("MCP and A2A are not
> orchestration"), then section 18 ("What we can and cannot infer about ServiceTitan") and the
> lab map (section 17). The rest is implementation detail to return to after day one; the
> production playbook (tracing, failure mining, evaluation and rollout) is
> [chapter 17](17-running-agents-in-production.md).

## 1. Why orchestration matters

A single agent is easy to understand:

```text
User
  |
  v
+----------------+
|      Agent     |
| reason + tools |
+-------+--------+
        |
        v
      APIs
```

This works well while the agent has one coherent objective. A production business quickly develops several competing objectives:

- book valuable work;
- preserve technician capacity;
- minimize travel;
- respond quickly;
- increase average ticket;
- protect customer experience;
- control marketing spend;
- collect payment;
- escalate risky decisions.

A common first response is to create specialist agents:

```text
BUSINESS
   |
   +------------+------------+
   |            |            |
   v            v            v
 Sales       Booking      Dispatch
 Agent        Agent        Agent
   |            |            |
  tools        tools       tools
```

That creates a second problem: **local optimization**.

A booking agent can make a good booking decision while a dispatch agent makes a good dispatch decision, yet the combination can be bad for the business.

For example:

```text
Booking agent:
  "This is a high-value customer. Book immediately."

Dispatch agent:
  "The best technician is already committed."

Demand agent:
  "Buy more leads."

Current business state:
  "Tomorrow is already over capacity."

                     |
                     v

            WITHOUT COORDINATION
            --------------------
            Three individually
            reasonable actions
            can produce a bad
            system-level result.
```

The engineering problem therefore becomes:

> **How do multiple specialized agents share enough context and judgment to optimize the system rather than merely their individual tasks?**

That is the orchestration problem.

## 2. The five building blocks

A useful production mental model is:

```text
                     +-----------------------+
                     |       EXPERIENCE      |
                     | Voice / Web / Mobile  |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     |    ORCHESTRATION      |
                     |                       |
                     | route / plan          |
                     | arbitrate / supervise |
                     | enforce policy        |
                     +-----------+-----------+
                                 |
                  +--------------+--------------+
                  |              |              |
                  v              v              v
              +-------+      +-------+      +-------+
              |Agent A|      |Agent B|      |Agent C|
              +---+---+      +---+---+      +---+---+
                  |              |              |
                  +--------------+--------------+
                                 |
                                 v
                     +-----------------------+
                     |     SHARED STATE      |
                     | facts / forecasts /   |
                     | decisions / history   |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     | TOOLS / SYSTEMS       |
                     | APIs / DB / MCP / etc.|
                     +-----------------------+
```

The five concepts are related but distinct:

| Concept | Question it answers |
|---|---|
| **Agent** | How should I reason about this task? |
| **Shared state** | What does the system currently know? |
| **Orchestration** | Who should act, and what happens next? |
| **Tools/protocols** | How does an agent access the outside world? |
| **Governance** | What is the system allowed to do? |

A useful rule is:

> **Agents provide intelligence. Orchestration provides coordination. State provides memory. Tools provide capability. Governance provides control.**

## 3. ServiceTitan's Pantheon 2026 model

ServiceTitan publicly describes Max as a coordinated system of **30 agents across 18 business drivers**. The opening keynote described five coordination capabilities [1][2]:

1. shared context;
2. shared judgment;
3. coordinated action;
4. arbitration;
5. centralized supervision.

The keynote also described a learning loop in which outcomes are tied back to the decisions that produced them.

See the repo's [Pantheon 2026 AI roadmap](../pantheon-2026-ai-roadmap.md) for the source-by-source treatment.

### Public claim: shared context

The keynote's example is deliberately simple: what the voice agent hears should be known by dispatch.

The important architectural interpretation is **not** that every agent should receive every raw transcript. A scalable implementation is more likely to promote verified facts into a shared business state:

```text
Voice interaction
      |
      v
+-----------------------+
| Fact extraction       |
| intent                |
| urgency               |
| constraints           |
| customer signals      |
+-----------+-----------+
            |
            v
+-----------------------+
| Shared business state |
|                       |
| customer              |
| job                   |
| appointment           |
| value                 |
| capacity              |
| constraints           |
+-----------+-----------+
            |
       +----+----+
       |         |
       v         v
   Dispatch    Lead score
```

**This diagram is an architectural interpretation, not a claim about ServiceTitan's internal database schema.**

The repo already teaches this distinction in [Call Facts](../call-facts-contract.md): proposed facts, verification, permissions, versions, and state transitions matter more than simply copying a transcript between agents.

### Public claim: shared judgment

ServiceTitan describes common lead-scoring and demand-forecasting models that agents can use.

That is different from shared data:

```text
                SHARED JUDGMENT
                      |
         +------------+------------+
         |            |            |
         v            v            v
      Lead value   Demand       Capacity
        model      forecast       model
         |            |            |
         +------------+------------+
                      |
                      v
               Common decision
                 vocabulary
```

Two agents can see exactly the same facts and still disagree if they have different definitions of "valuable."

### Public claim: arbitration

ServiceTitan describes choosing among competing actions by the highest expected value at the lowest expected cost [2].

A conceptual implementation is:

```text
Agent A proposes ----\
Agent B proposes -----+--> Candidate actions
Agent C proposes ----/             |
                                   v
                            +-------------+
                            | Arbitration |
                            |             |
                            | policy      |
                            | value       |
                            | cost        |
                            | capacity    |
                            | risk        |
                            +------+------+
                                   |
                          +--------+--------+
                          |                 |
                        reject            execute
```

The important lesson is:

> **A model can propose an action without owning the authority to execute it.**

### Public claim: centralized supervision

ServiceTitan describes a command center where contractors configure each agent and see its metrics [1][2].

That suggests an operational requirement beyond prompts:

- agent configuration;
- metrics;
- action history;
- failures;
- policy outcomes;
- evaluation;
- human intervention.

## 4. Salesforce: primary agent + specialist agents + gateway

Salesforce approaches the same problem through Agentforce multi-agent orchestration and **SOMA (Single-Org Multi-Agent)**.

Salesforce's documentation describes a primary orchestrator (a "Superagent") that delegates to specialized agents within one Salesforce org; MOMA extends the same model across orgs in one trust boundary [3][4].

```text
USER
  |
  v
+----------------+
| PRIMARY AGENT  |
| / SUPERAGENT   |
+-------+--------+
        |
   +----+----+----+
   |    |    |    |
   v    v    v    v
 Sales Service Specialist ...
 Agent  Agent   Agent
   |    |        |
   +----+--------+
         |
         v
   Salesforce data
```

Salesforce also draws an important boundary between [4]:

- **SOMA/MOMA** — architectures for organizing agents;
- **MCP/A2A** — protocols for agents/tools and agents/agents;
- **Agent Gateway** — governance and control.

That separation is useful well beyond Salesforce.

```text
Architecture
  |
  +-- SOMA: agents inside one org
  |
  +-- MOMA: agents across org boundaries
  |
Protocols
  |
  +-- MCP: agent <-> tool/data
  |
  +-- A2A: agent <-> agent
  |
Governance
  |
  +-- Agent Gateway
       auth / policy / quotas /
       schema validation / observability
```

This is a somewhat different emphasis from ServiceTitan.

**Salesforce is exposing a reusable enterprise agent platform. ServiceTitan is applying the same general ideas to a domain-specific operating system for the trades.**

## 5. Microsoft: workflows and an explicit runtime

Microsoft's current **Microsoft Agent Framework (MAF)** is especially useful as an open-source engineering reference.

MAF supports graph-based workflows and explicit orchestration patterns including [6]:

- sequential;
- concurrent;
- handoff;
- group chat;
- Magentic/manager-driven orchestration.

```text
Sequential:
    A --> B --> C

Concurrent:
    A --\
    B ---+--> aggregator
    C --/

Handoff:
    A --> B --> C

Magentic:
              +---------+
              | Manager |
              +----+----+
                   |
          +--------+--------+
          |        |        |
          v        v        v
          A        B        C
```

This is valuable because it exposes a principle that is easy to miss in agent demos:

> **Not every part of an agentic system should be left to an LLM.**

Microsoft's guidance is explicit: use an agent when the task is open-ended, and use a workflow when the process has well-defined steps, you need explicit control over execution order, or multiple agents and functions must coordinate. It adds: if you can write a function to handle the task, do that instead of using an AI agent [5].

For example:

```text
LLM decides:
  "I think we should reschedule this job."

                   |
                   v

Workflow/harness decides:
  Is rescheduling allowed?
  Is the appointment committed?
  Has this action already run?
  Does policy require approval?
                   |
            +------+------+
            |             |
          reject        execute
```

That division is closely related to the **model proposes, harness controls** pattern.

## 6. The three approaches compared

| Dimension | ServiceTitan | Salesforce | Microsoft |
|---|---|---|---|
| Primary goal | Run a trades business | Enterprise agent platform | General agent/workflow runtime |
| Main abstraction | Coordinated business agents | Superagent + specialists | Graph/workflow + agents |
| Shared context | Business context | Org/data context | Workflow/session state |
| Coordination | Explicit coordination system | Primary-agent delegation | Explicit workflow topology |
| Arbitration | Explicit business arbitration | Routing + governance | Workflow/manager decisions |
| Protocol layer | Not publicly specified | MCP + A2A | MCP clients for tools |
| Governance | Built into platform | Agent Gateway | Middleware/policies |
| Domain specificity | Very high | General enterprise | General |
| Best lesson | Global business optimization | Agent platform boundaries | Explicit execution control |

These are not mutually exclusive designs.

A realistic production architecture can combine them:

```text
                   BUSINESS APPLICATION
                          |
                          v
                 +-------------------+
                 | ORCHESTRATOR      |
                 | LangGraph / MAF   |
                 +---------+---------+
                           |
              +------------+------------+
              |            |            |
              v            v            v
           Booking      Dispatch       Sales
            Agent         Agent         Agent
              |            |             |
              +------------+-------------+
                           |
                           v
                     SHARED STATE
                           |
              +------------+------------+
              |            |            |
             MCP          A2A          APIs
```

## 7. What open source teaches us

### LangChain vs. LangGraph

This distinction is important.

**LangChain** is primarily a set of application/agent abstractions:

- models;
- tools;
- structured output;
- middleware;
- retrieval;
- integrations.

**LangGraph** is the lower-level runtime for **stateful, graph-based, long-running agent workflows**.

A useful mental model:

```text
         LANGCHAIN
             |
   models / tools / agents
             |
             v
         LANGGRAPH
             |
   +---------+---------+
   |         |         |
  state     graph   execution
   |         |         |
persistence  routing  durability
```

For this onboarding concept, **LangGraph is the more important technology to study.**

The repository already contains:

- Lab 05 — LangChain agent;
- Lab 06 — LangGraph booking workflow;
- Lab 09 — shared context;
- Lab 10 — coordination and arbitration;
- Lab 11 — learning loop;
- Lab 12 — agent-to-agent booking.

This chapter is therefore a conceptual layer over existing hands-on material, not a replacement for it.

## 8. How LangGraph can implement the coordination layer

The key LangGraph abstraction is explicit state.

A simplified state might contain:

```python
class BusinessState:
    customer_id: str
    intent: str
    urgency: str

    appointment_value: float
    technician_capacity: dict
    demand_forecast: dict

    candidate_actions: list
    approved_actions: list

    agent_observations: list
    selected_action: str | None
```

The graph can then look like:

```text
                     STATE
                       |
                       v
                +-------------+
                | Coordinator |
                +------+------+
                       |
         +-------------+-------------+
         |             |             |
         v             v             v
      Booking       Dispatch       Demand
       Agent          Agent          Agent
         |             |             |
         +-------------+-------------+
                       |
                       v
                 Arbitration
                       |
                 +-----+-----+
                 |           |
                 v           v
              reject      commit
                 |           |
                 +-----+-----+
                       |
                       v
                     STATE
```

The important property is that the agents do not have to communicate by passing entire conversations to each other.

They can communicate through **typed, inspectable state**.

### State is not the same as memory

Use at least two conceptual scopes:

```text
CURRENT WORKFLOW
----------------
checkpoint
pending action
candidate decisions
current agent
temporary facts

LONG-LIVED BUSINESS STATE
------------------------
customer history
equipment
preferences
business policies
historical outcomes
models/features
```

The workflow runtime should not become the system of record.

The agent should not become the system of record.

The **application/business data layer remains authoritative**.

## 9. Model proposes, harness controls: the simplest production agent

This is the single most useful pattern for production agent systems: it lets the model be
probabilistic while keeping side effects bounded and inspectable. Before thinking about thirty
agents, build the smallest useful production agent:

```text
User
  |
  v
+----------------------+
| Agent                |
| model + instructions |
| + tools              |
+----------+-----------+
           |
           | proposed tool call
           v
+----------------------+
| Control layer        |
|                      |
| validate / authorize |
| policy / HITL        |
| rate / budget        |
| idempotency          |
+----------+-----------+
           |
      +----+----+
      |         |
    reject    execute
                |
                v
               API
```

The important claim is that **an agent is not equivalent to an unrestricted LLM with API credentials**.

In a LangChain/LangGraph-style system, the model can decide which tool it wants to call and what arguments it proposes. Production middleware, graph nodes, or an application control layer can then inspect that proposal before a side effect occurs.

A simple booking agent might produce:

```json
{
  "tool": "book_appointment",
  "arguments": {
    "customer_id": "c123",
    "slot": "2026-10-08T10:00:00"
  }
}
```

The control layer should be able to answer:

```text
Is the customer authenticated?
Is this slot still available?
Is this agent allowed to book it?
Does the action exceed an autonomy limit?
Does policy require a human?
Has this exact operation already succeeded?
Is the request within rate/cost limits?
```

This gives a very useful progression:

```text
LLM
  |
  v
structured proposal
  |
  v
policy + state + authority checks
  |
  v
tool execution
  |
  v
observed result
  |
  v
trace + evaluation
```

For onboarding, this is the simplest example to build **before** introducing multi-agent arbitration. The multi-agent system is the same pattern repeated at a larger scale: more proposals, more shared state, more coordination, and more policy.

### LangChain/LangGraph terminology

Do not confuse the framework's abstractions with the production control boundary.

A LangChain agent provides the model/tool loop and agent abstractions. LangGraph provides explicit stateful graph execution and control points around that loop. Application code still owns the business authority boundary.

The engineering principle is:

> **The framework can orchestrate model reasoning; the application must control consequential side effects.**

This is also why a tool should generally be treated as an API with a contract, not as a trusted extension of the model.

## 10. Idempotency and durable execution

Agent workflows fail in ordinary software-engineering ways:

- process crashes;
- network timeout;
- duplicate delivery;
- tool returns slowly;
- human approval takes hours;
- workflow resumes from a checkpoint.

Suppose:

```text
Agent:
    BOOK_APPOINTMENT

API:
    success

Process:
    crashes before recording success
```

A naive retry can create:

```text
BOOK_APPOINTMENT
BOOK_APPOINTMENT
```

Production systems therefore need an idempotency boundary:

```text
             ACTION REQUEST
                    |
                    v
             operation_id
                    |
                    v
             +-------------+
             | Tool/API    |
             | idempotency |
             +------+------+
                    |
              already done?
                 /       \
               yes       no
               |          |
             return     execute
              prior        |
             result        v
                      persist result
```

This is as important as prompt quality.

## 11. Human-in-the-loop is a workflow state

A mature system should not treat human approval as an exception.

For a high-risk action:

```text
Agent proposes
      |
      v
Policy check
      |
      +------ low risk ------> execute
      |
      +------ high risk -----> human approval
                                  |
                           +------+------+
                           |             |
                         reject        approve
                           |             |
                           +------+------+
                                  |
                                resume
```

LangGraph's interrupt/persistence model is useful for this exact pattern.

The workflow can pause with its state intact, wait for external input, and resume.

## 12. Why "shared context" should not mean "share everything"

A tempting architecture is:

```text
Agent A transcript
       |
       v
Agent B receives transcript
       |
       v
Agent C receives transcript
```

This scales poorly.

A better architecture extracts domain facts:

```text
Raw interaction
      |
      v
Extraction / verification
      |
      v
+------------------------+
| Typed context          |
|                        |
| intent                 |
| urgency                |
| constraints            |
| customer preference    |
| equipment              |
| provenance             |
| confidence             |
| version                |
+-----------+------------+
            |
     +------+------+
     |             |
     v             v
  Dispatch      Lead scoring
```

This gives every downstream agent a common representation without requiring every agent to interpret the original conversation independently.

The existing Call Facts contract and Lab 09 are the repository's concrete teaching implementation of this idea.

## 13. Arbitration does not have to be an LLM

This is another important design choice.

Suppose agents produce:

```text
Booking:
  action = book(job_17)
  value = $2,400
  cost = $180

Dispatch:
  action = move(job_12)
  value = $900
  cost = $40

Demand:
  action = buy_leads($500)
  expected_value = $300
```

The arbitration layer might use a deterministic policy:

```text
score =
    expected_value
  - expected_cost
  - risk_penalty
  - capacity_penalty
```

An LLM can still be useful for generating candidates or explaining tradeoffs.

But deterministic policy can decide whether the action is:

- legal;
- permitted;
- economically justified;
- within capacity;
- already executed;
- safe to execute automatically.

This produces a hybrid system:

```text
LLM = reasoning + candidate generation

Code = state + policy + authority + side effects
```

## 14. MCP and A2A are not orchestration

Two protocols come up in every agent-architecture conversation, and they answer different
questions:

- **MCP (Model Context Protocol)** answers *"how does my agent reach a tool or a data
  source?"* It connects an AI application to the systems it uses. [9]
- **A2A (Agent2Agent)** answers *"how does my agent hand work to someone else's agent?"* It
  connects two independent agents that don't share code, memory or an owner. [10]
- **Orchestration** answers *"what should happen next, and who is allowed to do it?"* Neither
  protocol answers that; your application does.

A useful analogy: MCP is how an employee uses the company's software, A2A is how two
companies' staff email each other a work order, and orchestration is the manager deciding
who does what. Better email doesn't replace the manager.

### MCP: an agent's connection to tools and data

MCP uses JSON-RPC 2.0 between three roles [9]:

- **Host:** the AI application the user talks to (for example, the booking agent's runtime).
- **Client:** a connector inside the host, one per server.
- **Server:** a service that offers capabilities, such as a scheduling or CRM integration.

A server can offer three kinds of things [9]:

| MCP feature | What it is | Booking-agent example |
|---|---|---|
| **Tools** | Functions the model can ask to run | `check_availability`, `create_job` |
| **Resources** | Context and data to read | the customer's service history |
| **Prompts** | Templated messages and workflows | a "reschedule" script the user can pick |

Servers can also ask the user for missing information through the client (*elicitation*).
The current revision (2026-07-28) makes requests stateless and self-contained, and adds
opt-in extensions, including **Tasks** for long-running operations and a community working
group on **Skills over MCP**, structured workflow instructions discovered through MCP, which
is the same idea as [chapter 16](16-shared-skills-and-capabilities.md). [9]

```text
           Host (booking agent runtime)
           |-- MCP client --> scheduling server   tools: check_availability, create_job
           |-- MCP client --> CRM server          resources: customer record, history
           '-- MCP client --> knowledge server    resources: pricing, service area
```

**What MCP does not do.** It standardizes the plug, not the policy. The specification is
explicit that tools are arbitrary code execution, that tool descriptions should be treated
as untrusted unless the server is trusted, and that hosts must get the user's consent before
invoking a tool; it also says the protocol itself cannot enforce these principles. [9] In this
repo's terms, the MCP server is just a cleaner way to expose `create_job`. The guarded
dispatcher from lab 02 (ownership checks, offered slots only, grounded confirmations,
idempotency keys) still has to sit between the model's proposal and the call.

### A2A: one agent delegating to another

A2A connects agents across a boundary: a different team, vendor or company. Its design
principle is that agents are **opaque**: they collaborate on declared capabilities and
exchanged results "without needing to share their internal thoughts, plans, or tool
implementations." [10] Its core objects [10]:

| A2A object | What it is | Example |
|---|---|---|
| **Agent Card** | A JSON document an agent publishes (conventionally at `/.well-known/agent-card.json`) describing its identity, skills, endpoint and required authentication | a contractor's booking agent advertising "book a service visit" |
| **Task** | The stateful unit of work, with an ID and a lifecycle | "book an AC repair for Thursday" |
| **Message / Part** | A turn between client and remote agent, made of text, file or structured-data parts | the request and the follow-up question |
| **Artifact** | An output of the task | the booking confirmation |

Task states include working, input-required, auth-required, and the terminal states
completed, failed, canceled and rejected. Updates can stream in real time or arrive by push
notification to a webhook, and the same model is bound to JSON-RPC, gRPC and HTTP+JSON.
Authentication uses the schemes the Agent Card declares (API keys, HTTP auth, OAuth 2.0,
OpenID Connect or mutual TLS). [10]

```text
Homeowner's assistant agent                     Contractor's booking agent
  1. GET /.well-known/agent-card.json  ------->  skills, endpoint, auth schemes
  2. send message: "AC not cooling, Thu?" ---->  task T-17: working
  3.                                     <-----  task T-17: input-required ("8-10 or 1-3?")
  4. send message: "1-3"                ------>  task T-17: working
  5.                                     <-----  task T-17: completed + artifact (confirmation)
```

**What A2A does not do.** It tells the contractor's agent who is calling and what was asked;
it does not decide whether to trust the request. Everything lab 12 teaches still applies on
the receiving side: scopes, signed and non-replayed requests, idempotent retries, booking only
slots that were actually quoted, treating free-text fields as untrusted data, and not leaking
whether a phone number belongs to a customer. A message from another agent is input, never
instructions. (ServiceTitan's public Homh material describes an assistant app or plugin, not
an A2A endpoint; see [Homh and AI-agent booking](../homh-and-agent-booking.md).)

### How they fit together

| | MCP | A2A | Orchestration |
|---|---|---|---|
| Question it answers | How do I use this tool or data? | How do I hand this task to another agent? | What should happen next, and who may do it? |
| Other side | A server you integrate | An agent someone else runs | Your own agents and policies |
| Unit of work | A tool call or a resource read | A task with a lifecycle | A decision, then a commit |
| Who holds state | Your application | Each agent keeps its own | Your application (ledger, workflow) |
| Trust stance | Tool descriptions untrusted; consent before calls | Peer is opaque; authenticate, then validate | Enforces the policy both protocols leave open |
| In this repo | Lab 02's tools, exposed a standard way | Lab 12's gateway, on the receiving end | Labs 09–11 and sections 15–17 |

In one call they stack like this: the voice agent uses **MCP** to read the customer record and
check availability; it uses **A2A** (or an internal equivalent) to ask a separate financing
agent for options; and the **orchestration layer** decides whether to book, records the
decision with its evidence, and commits through the guarded tool.

Salesforce's public architecture uses both protocols in these roles, with an Agent
Gateway for governance [3][4]; Microsoft's Agent Framework documents MCP clients for tools
[5]. Neither vendor treats the protocol as the orchestrator.

### Four mistakes to avoid

1. **Trusting a tool because it's on an MCP server.** Descriptions and results are input.
   Keep allow-lists, argument validation and consent in your harness.
2. **Letting an A2A message act as instructions.** A peer agent's text can carry prompt
   injection just like a caller's. Parse it into typed fields; never let it grant permissions.
3. **Assuming the protocol is the authorization policy.** OAuth tells you who is calling,
   not whether they may book this customer's slot. Scopes and ownership checks are yours.
4. **Exposing write tools without idempotency.** Clients and networks retry. `create_job` needs an
   idempotency key whichever protocol carries it.

Therefore:

> MCP and A2A solve connectivity and interoperability. They make it cheaper to plug things
> together; they do not decide what should happen, and they do not make an action safe.

## 15. Recommended prototype architecture

For a small ServiceTitan-like educational system, use:

```text
                     USER
                       |
                       v
                 Voice/Web UI
                       |
                       v
             +-------------------+
             |    LangGraph      |
             |   Coordinator     |
             +---------+---------+
                       |
         +-------------+-------------+
         |             |             |
         v             v             v
      Voice/         Booking       Dispatch
      Intake          Agent          Agent
         |             |             |
         +-------------+-------------+
                       |
                       v
                 Arbitration
                       |
                       v
                Control Harness
                       |
                +------+------+
                |             |
                v             v
              Tools       Human approval
                |
                v
           Mock backend
```

Back it with:

- **Postgres** for authoritative business state;
- **Redis** only where low-latency ephemeral state is useful;
- **LangGraph** for stateful orchestration;
- **LangChain** for agent/tool/model conveniences;
- **MCP** for tool boundaries where appropriate;
- **OpenTelemetry/LangSmith** for traces and evaluation;
- deterministic mock APIs for booking/dispatch;
- synthetic data only.

Do not start with 30 agents.

Start with:

- one coordinator;
- three specialist agents;
- one shared state model;
- five to ten tools;
- one arbitration function;
- one human-approval boundary.

Then deliberately create conflicts.

## 16. A useful experiment

Create a fictional HVAC company with:

- 20 customers;
- 10 technicians;
- technician skill constraints;
- geographic locations;
- appointment values;
- limited capacity;
- customer preferences;
- demand forecasts.

Then create:

```text
Booking Agent
  "Book the highest-value customer."

Dispatch Agent
  "Protect technician utilization."

Membership Agent
  "Fill open slots with maintenance customers."

Demand Agent
  "Generate more demand."
```

Give the agents conflicting objectives.

Then compare:

### Experiment A

One large agent.

### Experiment B

Three independent agents.

### Experiment C

Three agents + shared state.

### Experiment D

Three agents + shared state + arbitration.

Measure:

- revenue;
- utilization;
- travel;
- customer delay;
- wrong actions;
- number of conflicts;
- human interventions;
- latency;
- model/tool cost.

The interesting question is not:

> "Which agent is smartest?"

It is:

> **Does coordination produce a better business outcome than independent optimization?**

That is the core systems question behind the Pantheon architecture.

## 17. How the existing onboarding labs map to this chapter

The repository already has hands-on material for the concepts in this chapter:

- Lab 05 — LangChain agent
- Lab 06 — LangGraph booking workflow
- Lab 07 — tracing and evaluation
- Lab 09 — shared context
- Lab 10 — coordination and arbitration
- Lab 11 — learning loop
- Lab 12 — agent-to-agent booking
- Lab 13 — end-to-end control-plane capstone
- Lab 14 — earning autonomy

Use the lab index in [labs/README.md](../../labs/README.md) for the canonical filenames and execution order.
Lab 07 (tracing and evaluation) pairs with [chapter 17](17-running-agents-in-production.md), which
covers tracing, failure mining, evaluation and rollout.

The intended progression is:

```text
Single agent
    |
    v
Tool-using agent
    |
    v
Stateful workflow
    |
    v
Shared context
    |
    v
Multiple agents
    |
    v
Arbitration
    |
    v
Learning loop
    |
    v
Agent-to-agent interaction
    |
    v
Measured autonomy
```

The new chapter is therefore the **architecture map** that connects the individual labs.

## 18. What we can and cannot infer about ServiceTitan

This distinction should remain explicit throughout onboarding. The public record is stronger for ServiceTitan's **data platform** than it is for the private implementation of the Pantheon agent runtime.

### Publicly described: Pantheon / Max

ServiceTitan has publicly described:

- 30 agents;
- 18 business drivers;
- shared context;
- shared judgment;
- coordinated action;
- arbitration;
- centralized supervision;
- outcome/decision learning;
- a command center;
- capacity-aware booking;
- voice intelligence as a separate evaluation/judging capability.

These are the public product/architecture claims that motivate the orchestration model in this chapter.

### Publicly evidenced: the data platform

ServiceTitan's public job listings also identify **Kafka, Snowflake, and Airflow** as part of its data platform.

A ServiceTitan job listing for an Engineering Manager, Data Foundations describes owning
"architecture for data ingestion (Kafka, custom ETL Agent), Snowflake, and Airflow", plus data
quality, monitoring and cost management across the data platform [7].

A Staff Product Manager, Communications Intelligence listing describes "communication event
streaming, and the reporting pipeline into Snowflake" so that "reporting products, AI systems,
AgentOS, and downstream product teams" receive trusted data [8].

Job listings are public but short-lived, and they describe the data platform, not the Pantheon
agent runtime. Read them as evidence about the company's data stack as of October 2026.

That suggests a plausible shape (hypothesis):

```text
Agent / product runtime
          |
          | events / outcomes / operational data
          v
       Kafka
          |
   +------+------+
   |             |
   v             v
streaming     data platform
consumers         |
                  v
              Snowflake
                  |
      +-----------+-----------+
      |           |           |
   analytics   evaluation   failure mining
```

**Important:** the public evidence establishes Kafka/Snowflake as ServiceTitan data-platform technologies. It does **not** establish that every Pantheon agent trace follows exactly this path, nor does it reveal the private topic names, schemas, consumers, retention policies, or internal observability implementation.

### What this means for production agents

This makes the production debugging material in
[chapter 17](17-running-agents-in-production.md#2-debugging-production-agents-and-mining-failure-cases)
more concrete.

A useful engineering hypothesis (not a documented ServiceTitan design) is:

```text
Agent runtime
     |
     +--> trace / decision / tool / outcome events
                     |
                     v
                   Kafka
                     |
          +----------+----------+
          |                     |
    real-time systems       durable analytics
                                |
                                v
                            Snowflake
                                |
                     +----------+----------+
                     |          |          |
                   search     evals     dashboards
                     |
                     v
                failure cases
                     |
                     v
              regression suite
                     |
                     v
               canary / A-B
                     |
                     v
                production
```

The key distinction is:

> **A trace explains one execution. The data platform lets you find patterns across millions of executions.**

That is why Kafka and Snowflake matter to an agent engineer even if the agent itself is implemented with a completely different runtime.

Kafka is useful for moving operational events through the system and feeding downstream consumers. Snowflake is useful for durable analytical history: joining outcomes to versions, cohorts, customer/job attributes, evaluator scores, and other dimensions so engineers can identify systematic failure modes.

For example, a production investigation might ask (illustrative):

```text
Why did wrong-booking rate increase?

         |
         v
   Snowflake query
         |
   +-----+-----+----------------+
   |           |                |
model v42   tool v7       evening traffic
   |           |                |
   +-----------+----------------+
               |
               v
      retrieve representative
         trace IDs
               |
               v
          trace system
               |
               v
      inspect exact execution
               |
               v
      create evaluation cases
               |
               v
      regression + canary
```

This is the production learning loop the onboarding material should teach: **stream operational facts, retain analytical history, trace individual executions, mine failures, turn failures into evaluations, and use those evaluations to control releases.**

### Still not publicly established

We should **not** claim that ServiceTitan's Pantheon implementation specifically uses:

- LangGraph;
- LangChain;
- a particular agent graph runtime;
- a particular agent trace schema;
- specific Kafka topics for agent telemetry;
- specific Snowflake tables for agent traces;
- Redis;
- Postgres;
- a particular vector database;
- a particular internal agent protocol;
- a particular LLM.

Those remain implementation details unless ServiceTitan publicly documents them.

The right engineering stance is therefore:

> **Kafka and Snowflake are publicly evidenced ServiceTitan data-platform technologies. Their exact role in Pantheon's private agent runtime is an informed architectural hypothesis, not a public implementation claim.**

The goal of this chapter is to understand the **architecture problem**, then use public ServiceTitan evidence and open-source implementations to develop useful engineering hypotheses.

## 19. The deeper architectural pattern

The most useful synthesis is:

```text
                AI OPERATING SYSTEM
                       |
    +------------------+------------------+
    |                  |                  |
    v                  v                  v
EXPERIENCE          AGENTS            BUSINESS
voice/web/app       reasoning          state/data
    |                  |                  |
    +------------------+------------------+
                       |
                       v
               ORCHESTRATION
                       |
          +------------+------------+
          |            |            |
        routing    arbitration   policy
          |            |            |
          +------------+------------+
                       |
                       v
                 EXECUTION
                       |
                +------+------+
                |             |
              tools         humans
```

This is why the phrase **AI operating system** is useful.

The differentiator is not merely having an LLM.

It is the system around the LLM that lets many probabilistic components operate against a shared, authoritative model of the business.

## 20. Final mental model

If you remember only one diagram, remember this:

```text
                     HUMAN
                       |
                       v
                   AGENTS
              reason / propose
                       |
                       v
                ORCHESTRATION
             route / arbitrate
              / policy / retry
                       |
                       v
                 SHARED STATE
            facts / forecasts /
             history / outcomes
                       |
                       v
                    TOOLS
             APIs / MCP / DBs
                       |
                       v
                 REAL WORLD
```

And remember the boundary:

> **The agent is not the system.**

The model reasons.

The workflow coordinates.

The state records reality.

The harness controls authority.

The tools change the world.

The evaluation system determines whether the decisions were actually good.

That is the conceptual bridge from a voice agent to an **agentic operating system**.

## Check your understanding

Try each question before reading the sketches below it.

1. Every specialist agent's metric improves, yet booked revenue falls. What is the failure
   called, and which of the five coordination capabilities address it?
2. A teammate proposes letting an LLM choose between two agents' conflicting proposals for
   the same technician slot. What would you put in charge instead, and what can the LLM still do?
3. "We adopted MCP and A2A, so orchestration is solved." What do those protocols give you,
   and what do they leave to you?
4. Which statements about ServiceTitan's architecture in this chapter are public facts, and
   which are hypotheses you would need to validate after joining?

**Answer sketches**

1. Local optimization (section 1). Shared context and shared judgment stop agents from
   reasoning from different facts and scores; arbitration and supervision resolve conflicts
   that remain. Lab 10 shows it.
2. Deterministic arbitration over expected value net of cost, with hard constraints
   (consent, emergencies, capacity) that are never traded away (section 13; lab 10). The LLM can
   propose and explain; the harness decides and commits.
3. Connectivity: MCP standardizes tool and data access, A2A standardizes agent-to-agent
   calls. Policy, arbitration, durable state, idempotent side effects and supervision are
   still application code (section 14).
4. Public: the press release and keynote describe 30 agents across 18 business drivers and
   the five coordination capabilities, and job listings name parts of the data platform.
   Hypotheses: how any of it is implemented, including the role of streaming or the
   warehouse in agent telemetry (section 18).

A question on debugging a wrong-technician booking moved with the production material to
[chapter 17](17-running-agents-in-production.md#check-your-understanding).

## Sources

1. ServiceTitan, Pantheon 2026 announcements (press release, October 6, 2026): <https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html>
2. ServiceTitan at Pantheon 2026, keynote summary and transcript (Investing.com): <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>; see also the repo's [Pantheon 2026 brief](../pantheon-2026-ai-roadmap.md) and the [live coverage](https://www.servicetitan.com/blog/pantheon-2026-live-coverage)
3. Salesforce, Agentforce Multi-Agent Orchestration: <https://www.salesforce.com/agentforce/multi-agent-orchestration/>
4. Salesforce Help, Agentforce SOMA (Single Org, Multi Agent) orchestration and MCP: <https://help.salesforce.com/s/articleView?id=005317683&language=en_US&type=1>
5. Microsoft Learn, Microsoft Agent Framework overview ("When to use agents vs workflows"): <https://learn.microsoft.com/agent-framework/overview/>
6. Microsoft Learn, Workflow orchestrations in Agent Framework: <https://learn.microsoft.com/agent-framework/workflows/orchestrations>
7. ServiceTitan job listing, Engineering Manager, Data Foundations (checked October 7, 2026; listings expire): <https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan/job/Manager--Software-Engineering_JR114911>
8. Built In, ServiceTitan Staff Product Manager, Communications Intelligence (checked October 7, 2026; listings expire): <https://builtin.com/job/staff-product-manager-communications-intelligence/10448969>
9. Model Context Protocol specification, revision 2026-07-28 (architecture, features, security principles, extensions): <https://modelcontextprotocol.io/specification/2026-07-28>
10. A2A (Agent2Agent) Protocol specification, version 1.0.0 (Agent Card, tasks, messages, artifacts, bindings, authentication): <https://a2a-protocol.org/latest/specification/>

## Further reading

- [Microsoft Agent Framework on GitHub](https://github.com/microsoft/agent-framework)
- [LangGraph](https://github.com/langchain-ai/langgraph): [overview](https://docs.langchain.com/oss/python/langgraph/overview), [persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [durable execution](https://docs.langchain.com/oss/python/langgraph/checkpointers#durability-modes), [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents)
- Labs: [05 LangChain agent](../../labs/05_langchain_create_agent.ipynb), [06 LangGraph booking workflow](../../labs/06_langgraph_booking_workflow.ipynb), [07 tracing and evaluation](../../labs/07_langsmith_tracing_evals.ipynb), [09 shared context](../../labs/09_shared_context.ipynb), [10 coordination and arbitration](../../labs/10_coordination_and_arbitration.ipynb), [11 learning loop](../../labs/11_learning_loop.ipynb), [12 agent-to-agent booking](../../labs/12_agent_to_agent_booking.ipynb), [13 Mini-Max capstone](../../labs/13_minimax_capstone.ipynb), [14 earning autonomy](../../labs/14_earning_autonomy.ipynb)
- Related in this repo: [call facts contract](../call-facts-contract.md), [tools and guardrails](../tools-and-guardrails.md), [chapter 16: shared skills](16-shared-skills-and-capabilities.md), [chapter 17: running agents in production](17-running-agents-in-production.md)
