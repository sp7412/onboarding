# Agentic Orchestration: From Single Agents to an AI Operating System

**Audience:** Engineers and technical leaders who understand ML/LLMs but are new to multi-agent production systems.

**Status:** Public-source onboarding material. ServiceTitan-specific implementation details below are explicitly separated into **public claim** and **analysis/hypothesis**. No internal ServiceTitan architecture is asserted.

## 1. Why orchestration matters

A single agent is easy to understand:

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

    BUSINESS
       |
       +------------+------------+
       |            |            |
       v            v            v
     Sales       Booking      Dispatch
     Agent        Agent        Agent
       |            |            |
      tools        tools       tools

That creates a second problem: **local optimization**.

A booking agent can make a good booking decision while a dispatch agent makes a good dispatch decision, yet the combination can be bad for the business.

For example:

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

The engineering problem therefore becomes:

> **How do multiple specialized agents share enough context and judgment to optimize the system rather than merely their individual tasks?**

That is the orchestration problem.

## 2. The five building blocks

A useful production mental model is:

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

ServiceTitan publicly describes Max as a coordinated system of **30 agents across 18 business drivers**. The opening keynote described five coordination capabilities:

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

**This diagram is an architectural interpretation, not a claim about ServiceTitan's internal database schema.**

The repo already teaches this distinction in [Call Facts](../call-facts-contract.md): proposed facts, verification, permissions, versions, and state transitions matter more than simply copying a transcript between agents.

### Public claim: shared judgment

ServiceTitan describes common lead-scoring and demand-forecasting models that agents can use.

That is different from shared data:

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

Two agents can see exactly the same facts and still disagree if they have different definitions of "valuable."

### Public claim: arbitration

ServiceTitan describes choosing among competing actions using estimated value and expected cost.

A conceptual implementation is:

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

The important lesson is:

> **A model can propose an action without owning the authority to execute it.**

### Public claim: centralized supervision

ServiceTitan describes a command-center experience for configuring and monitoring agents.

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

The official Salesforce documentation describes a primary orchestrator that delegates to specialized agents within one Salesforce org.

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

Salesforce also draws an important boundary between:

- **SOMA/MOMA** — architectures for organizing agents;
- **MCP/A2A** — protocols for agents/tools and agents/agents;
- **Agent Gateway** — governance and control.

That separation is useful well beyond Salesforce.

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

This is a somewhat different emphasis from ServiceTitan.

**Salesforce is exposing a reusable enterprise agent platform. ServiceTitan is applying the same general ideas to a domain-specific operating system for the trades.**

## 5. Microsoft: workflows and an explicit runtime

Microsoft's current **Microsoft Agent Framework (MAF)** is especially useful as an open-source engineering reference.

MAF supports graph-based workflows and explicit orchestration patterns including:

- sequential;
- concurrent;
- handoff;
- group chat;
- Magentic/manager-driven orchestration.

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

This is valuable because it exposes a principle that is easy to miss in agent demos:

> **Not every part of an agentic system should be left to an LLM.**

Microsoft's workflow documentation explicitly recommends workflows when guaranteed execution order or explicit control is required.

For example:

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

That division is closely related to the **model proposes, harness controls** pattern.

## 6. The three approaches compared

| Dimension | ServiceTitan | Salesforce | Microsoft |
|---|---|---|---|
| Primary goal | Run a trades business | Enterprise agent platform | General agent/workflow runtime |
| Main abstraction | Coordinated business agents | Superagent + specialists | Graph/workflow + agents |
| Shared context | Business context | Org/data context | Workflow/session state |
| Coordination | Explicit coordination system | Primary-agent delegation | Explicit workflow topology |
| Arbitration | Explicit business arbitration | Routing + governance | Workflow/manager decisions |
| Protocol layer | Platform-specific + integrations | MCP + A2A | MCP/A2A ecosystem |
| Governance | Built into platform | Agent Gateway | Middleware/policies |
| Domain specificity | Very high | General enterprise | General |
| Best lesson | Global business optimization | Agent platform boundaries | Explicit execution control |

These are not mutually exclusive designs.

A realistic production architecture can combine them:

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

The graph can then look like:

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

The important property is that the agents do not have to communicate by passing entire conversations to each other.

They can communicate through **typed, inspectable state**.

### State is not the same as memory

Use at least two conceptual scopes:

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

The workflow runtime should not become the system of record.

The agent should not become the system of record.

The **application/business data layer remains authoritative**.

## 9. Model proposes, harness controls

This is the single most useful pattern for production agent systems.

Bad:

    LLM ---> API

Better:

                     LLM
                      |
                      | proposed action
                      v
              +---------------+
              | CONTROL       |
              | HARNESS       |
              |               |
              | state         |
              | policy        |
              | permissions   |
              | risk          |
              | arbitration   |
              | idempotency   |
              +-------+-------+
                      |
                 +----+----+
                 |         |
               reject    execute
                           |
                           v
                          API

This pattern lets the model be probabilistic while keeping side effects bounded and inspectable.

## 10. The simplest production agent: model proposes, control layer decides

Before thinking about thirty agents, build the smallest useful production agent:

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

The important claim is that **an agent is not equivalent to an unrestricted LLM with API credentials**.

In a LangChain/LangGraph-style system, the model can decide which tool it wants to call and what arguments it proposes. Production middleware, graph nodes, or an application control layer can then inspect that proposal before a side effect occurs.

A simple booking agent might produce:

    {
      "tool": "book_appointment",
      "arguments": {
        "customer_id": "c123",
        "slot": "2026-10-08T10:00:00"
      }
    }

The control layer should be able to answer:

    Is the customer authenticated?
    Is this slot still available?
    Is this agent allowed to book it?
    Does the action exceed an autonomy limit?
    Does policy require a human?
    Has this exact operation already succeeded?
    Is the request within rate/cost limits?

This gives a very useful progression:

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

For onboarding, this is the simplest example to build **before** introducing multi-agent arbitration. The multi-agent system is the same pattern repeated at a larger scale: more proposals, more shared state, more coordination, and more policy.

### LangChain/LangGraph terminology

Do not confuse the framework's abstractions with the production control boundary.

A LangChain agent provides the model/tool loop and agent abstractions. LangGraph provides explicit stateful graph execution and control points around that loop. Application code still owns the business authority boundary.

The engineering principle is:

> **The framework can orchestrate model reasoning; the application must control consequential side effects.**

This is also why a tool should generally be treated as an API with a contract, not as a trusted extension of the model.

## 11. Production observability: trace the decision, not just the request

A production agent that cannot be traced is extremely difficult to debug.

For every meaningful agent run, capture a correlated trace such as:

    trace_id
       |
       +-- user request
       |
       +-- agent invocation
       |     +-- model
       |     +-- prompt/version
       |     +-- latency
       |     +-- tokens/cost
       |
       +-- tool call
       |     +-- tool name
       |     +-- arguments
       |     +-- latency
       |     +-- result/status
       |
       +-- policy decision
       |
       +-- human approval (if any)
       |
       +-- final outcome

For a multi-agent system, extend the same trace across the graph:

    trace_id = 8f2...

      Coordinator
          |
          +-- Booking Agent
          |      +-- LLM call
          |      +-- availability tool
          |
          +-- Dispatch Agent
          |      +-- capacity tool
          |
          +-- Arbitration
          |      +-- candidates
          |      +-- selected action
          |
          +-- Control Harness
                 +-- policy result
                 +-- booking API

Every child operation should retain the parent trace/span relationship. Otherwise a production incident becomes a pile of unrelated log lines.

### What to capture

At minimum, capture:

- trace/run ID and correlation IDs;
- agent and graph version;
- prompt/instruction version;
- model/provider/version;
- tool name and structured arguments;
- tool result status and latency;
- policy/control decisions;
- retries and exceptions;
- human approvals/rejections;
- final business outcome;
- token usage and model/tool cost where available.

Be deliberate about data handling. Customer PII, call transcripts, secrets, authentication material, and sensitive tool payloads should not automatically be copied into every trace. Redaction, access control, retention, and sampling are production requirements.

### Debugging with traces

When a customer reports:

    "The agent booked the wrong technician."

The trace should let an engineer walk backward:

    wrong outcome
         ^
    wrong action selected
         ^
    arbitration decision
         ^
    agent proposal
         ^
    model/tool result
         ^
    shared state at that point in time
         ^
    original user facts

This is much more useful than looking only at the final answer.

LangSmith is one example of a tracing/evaluation platform that can provide this kind of agent run visibility. OpenTelemetry is the broader vendor-neutral instrumentation model. The exact production stack is an implementation choice.

## 13. Debugging production agents and mining failure cases

Tracing is only useful if engineers can go from a production symptom to the exact decision path that caused it.

A practical incident workflow is:

    1. Detect a bad outcome
             |
             v
    2. Find the trace_id / conversation_id
             |
             v
    3. Reconstruct the trace
             |
             +--> input/context
             +--> model calls
             +--> tool calls
             +--> intermediate state
             +--> policy decisions
             +--> retries
             +--> final action
             |
             v
    4. Identify the failure mode
             |
             +--> bad facts
             +--> bad retrieval
             +--> bad reasoning
             +--> wrong tool
             +--> bad arguments
             +--> policy failure
             +--> stale state
             +--> integration failure
             |
             v
    5. Save the case as an evaluation example
             |
             v
    6. Fix / evaluate / canary

### Example: "the agent booked the wrong technician"

An engineer should be able to search production telemetry for:

    outcome = "wrong_technician"
    agent = "booking"
    date >= yesterday
    policy_result = "allowed"

Then drill into the individual traces:

    Trace 8f2...
       |
       +-- customer facts
       +-- availability lookup
       +-- dispatch recommendation
       +-- model proposal
       +-- arbitration
       +-- authorization
       +-- booking API
       +-- observed result

The goal is not merely to find the bad response. It is to determine **which decision boundary failed**.

### Searching for interesting failures

Production telemetry should be queryable as structured data, not only as text logs.

Useful dimensions include:

- agent/version;
- model/version;
- prompt/instruction version;
- tool name;
- tool error/status;
- policy decision;
- autonomy level;
- latency bucket;
- retry count;
- escalation/HITL;
- user feedback;
- business outcome;
- evaluator score;
- experiment/canary cohort;
- geography/job type/customer segment where appropriate.

That enables queries such as:

    Find all traces where:
      - booking agent
      - candidate version = v42
      - tool = availability
      - latency > 2 seconds
      - outcome = failed

or:

    Find the top 100 traces where:
      - evaluator_score < threshold
      - policy = allowed
      - no human intervention

or:

    Compare:
      v41 vs v42
      for the same job classes
      by:
        task success
        wrong-action rate
        escalation
        p95 latency
        cost

### Turn production failures into the eval set

This is one of the most important production-agent practices:

    Production
       |
       v
    traces
       |
       v
    failure mining
       |
       +--> representative failures
       +--> rare edge cases
       +--> policy violations
       +--> expensive failures
       +--> high-confidence user complaints
       |
       v
    curated evaluation set
       |
       v
    candidate agent
       |
       v
    regression evaluation
       |
       v
    canary
       |
       v
    production

Do not simply collect the worst examples. Also sample successful traces so the evaluation set does not become a collection of pathological cases. Maintain slices for important cohorts and failure modes.

### Event streaming vs long-term analytical storage

A common production architecture separates **operational event transport** from **durable analytical storage**:

    Agent runtime
        |
        | OpenTelemetry/events
        v
    +----------------+
    | Event stream   |
    | Kafka-like     |
    | transport      |
    +-------+--------+
            |
       +----+----+
       |         |
       v         v
    real-time  durable
    consumers  data platform
                  |
                  v
              Snowflake
                  |
          +-------+-------+
          |               |
       analytics       evaluation
       / dashboards    / failure mining

Kafka is well suited to transporting high-volume events to multiple consumers; a warehouse such as Snowflake is well suited to retaining and querying historical events, outcomes, and evaluation data. The exact architecture is an implementation choice.

For an agent team, the important distinction is:

> **The trace system explains one execution; the analytical system lets you find patterns across millions of executions.**

For example, a trace can explain one bad booking. A warehouse query can reveal that **2.7% of booking failures occur only when model v42, tool version v7, and evening availability checks coincide**.

### What to persist for failure mining

A useful durable event schema includes:

    trace_id
    parent_span_id
    timestamp
    agent_name
    agent_version
    model_name
    model_version
    prompt_version
    experiment_id
    cohort
    input_class
    tool_name
    tool_version
    policy_result
    proposed_action
    executed_action
    outcome
    evaluator_score
    latency_ms
    token_usage
    cost
    retry_count
    human_intervention
    error_code

Keep large payloads such as transcripts and tool bodies separately governed when appropriate. The analytical event should contain enough identifiers and structured metadata to find the detailed trace without making every warehouse row a copy of sensitive conversation data.

### Debugging is a join across systems

In a mature production environment, the engineer often needs to correlate:

    customer/job ID
          |
          +--> application database
          |
          +--> trace ID
          |
          +--> event stream
          |
          +--> warehouse history
          |
          +--> evaluation result
          |
          +--> deployment/experiment version

That correlation should be designed **before** production. A trace ID that disappears when the request crosses an agent, tool, queue, or service boundary makes distributed debugging dramatically harder.

## 12. Evaluation: define success before changing the agent

An agent can be technically successful while being operationally bad.

    "Tool call succeeded"
             !=
    "Business outcome was good"

For example:

    Booking API: 200 OK
    Agent run: SUCCESS

    But:
    - wrong technician;
    - poor route;
    - customer unhappy;
    - margin below threshold.

Production evaluation therefore needs multiple levels:

    Level 1: runtime correctness
      Did the workflow complete?

    Level 2: agent correctness
      Did it choose an appropriate action?

    Level 3: policy correctness
      Was the action permitted?

    Level 4: business outcome
      Did the action improve the target metric?

A useful evaluation record is:

    {
      "trace_id": "...",
      "agent_version": "...",
      "scenario": "...",
      "expected": "...",
      "proposed_action": "...",
      "policy_result": "...",
      "actual_outcome": "...",
      "human_label": "...",
      "business_metrics": {
        "revenue": 0,
        "travel_minutes": 0,
        "customer_delay_minutes": 0
      }
    }

This allows offline regression tests and online production evaluation to use the same conceptual schema.

### Offline evaluation

Before deployment, maintain a representative evaluation set:

    scenario
       |
       +--> expected facts
       +--> expected constraints
       +--> acceptable actions
       +--> unacceptable actions
       +--> expected outcome

Run the candidate agent against the set and compare:

    baseline agent
          vs.
    candidate agent

Do not rely on one aggregate score. Track safety/policy failures separately from quality metrics. A small average improvement is not worth a large increase in dangerous or unauthorized actions.

### Online evaluation

Production evaluation can sample real traces and score them asynchronously:

    production traffic
          |
          v
       traces
          |
          +-----------> dashboards
          |
          +-----------> online evaluators
                           |
                     +-----+------+
                     |            |
                   quality      policy
                   score        violations
                     |
                     v
                  outcomes

This closes the loop between what the model *said* and what the system *actually did*.

## 14. Canary releases and A/B testing for agents

Agent changes should be treated like production software changes, not just prompt edits.

A practical rollout looks like:

    100% current version
              |
              v
          1% canary
              |
        +-----+-----+
        |           |
      healthy     regressions
        |           |
        v           v
      10%         rollback
        |
        v
      25%
        |
        v
      50%
        |
        v
     100%

The canary should be evaluated on **guardrail metrics first**, not just aggregate quality:

- tool/policy violation rate;
- wrong-action rate;
- escalation rate;
- task success;
- latency/p95/p99;
- error rate;
- cost per interaction;
- human intervention rate;
- customer/business outcome metrics.

### A/B testing

For a controlled experiment, route comparable traffic to two versions:

    request
       |
       v
    experiment router
       |
       +--------+--------+
       |                 |
       v                 v
    Agent A           Agent B
    control           treatment
       |                 |
       +--------+--------+
                |
                v
        common evaluation
                |
                v
        business outcomes

The key is to keep the evaluation and routing layer outside the agent being tested.

For voice and scheduling systems, random assignment may not be sufficient. Stratify or balance on factors such as:

- customer segment;
- job type;
- geography;
- time of day;
- technician availability;
- language/channel;
- traffic source.

Otherwise a treatment can appear better simply because it received easier cases.

### Shadow mode

Before allowing a new agent to take real actions, use shadow mode:

    real request
         |
         +----------> current agent --> real action
         |
         +----------> candidate agent --> proposal only
                                      |
                                      v
                                   compare

The candidate observes production-like inputs and generates decisions, but its proposed side effects are not executed.

This is especially valuable for consequential agents because it measures real-distribution behavior without giving an unproven model authority.

### Canary + trace + evaluation form one system

These are not separate DevOps features:

    RELEASE
       |
       v
    ROUTING
       |
       v
    AGENT
       |
       v
    TRACE
       |
       v
    EVALUATION
       |
       +------> guardrail breach --> rollback
       |
       +------> healthy ----------> increase traffic
       |
       +------> business improvement -> promote

That is the production learning loop around the agent.

## 15. Idempotency and durable execution

Agent workflows fail in ordinary software-engineering ways:

- process crashes;
- network timeout;
- duplicate delivery;
- tool returns slowly;
- human approval takes hours;
- workflow resumes from a checkpoint.

Suppose:

    Agent:
        BOOK_APPOINTMENT

    API:
        success

    Process:
        crashes before recording success

A naive retry can create:

    BOOK_APPOINTMENT
    BOOK_APPOINTMENT

Production systems therefore need an idempotency boundary:

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

This is as important as prompt quality.

## 16. Human-in-the-loop is a workflow state

A mature system should not treat human approval as an exception.

For a high-risk action:

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

LangGraph's interrupt/persistence model is useful for this exact pattern.

The workflow can pause with its state intact, wait for external input, and resume.

## 17. Why "shared context" should not mean "share everything"

A tempting architecture is:

    Agent A transcript
           |
           v
    Agent B receives transcript
           |
           v
    Agent C receives transcript

This scales poorly.

A better architecture extracts domain facts:

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

This gives every downstream agent a common representation without requiring every agent to interpret the original conversation independently.

The existing Call Facts contract and Lab 09 are the repository's concrete teaching implementation of this idea.

## 18. Arbitration does not have to be an LLM

This is another important design choice.

Suppose agents produce:

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

The arbitration layer might use a deterministic policy:

    score =
        expected_value
      - expected_cost
      - risk_penalty
      - capacity_penalty

An LLM can still be useful for generating candidates or explaining tradeoffs.

But deterministic policy can decide whether the action is:

- legal;
- permitted;
- economically justified;
- within capacity;
- already executed;
- safe to execute automatically.

This produces a hybrid system:

    LLM = reasoning + candidate generation

    Code = state + policy + authority + side effects

## 19. MCP and A2A are not orchestration

These terms are easy to mix up.

### MCP

**Agent <-> tool/data**

    Agent
      |
     MCP
      |
      +--> CRM
      +--> database
      +--> scheduling API
      +--> search

### A2A

**Agent <-> agent**

    Agent A
       |
      A2A
       |
    Agent B

### Orchestration

**What should happen next?**

                 ORCHESTRATOR
                      |
           +----------+----------+
           |          |          |
           v          v          v
         Agent      Agent      Agent
           |          |          |
           +----------+----------+
                      |
                      v
                   decision

Therefore:

> MCP and A2A solve connectivity/interoperability problems. They do not eliminate the need for an application-level coordination strategy.

## 20. Recommended prototype architecture

For a small ServiceTitan-like educational system, use:

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

## 21. A useful experiment

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

    Booking Agent
      "Book the highest-value customer."

    Dispatch Agent
      "Protect technician utilization."

    Membership Agent
      "Fill open slots with maintenance customers."

    Demand Agent
      "Generate more demand."

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

## 22. How the existing onboarding labs map to this chapter

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

The intended progression is:

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

The new chapter is therefore the **architecture map** that connects the individual labs.

## 23. What we can and cannot infer about ServiceTitan

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

ServiceTitan's current public engineering material also explicitly identifies **Kafka, Snowflake, and Airflow** as part of its data-platform architecture.

The ServiceTitan Engineering Manager, Data Foundations role describes responsibility for data ingestion using **Kafka and a custom ETL agent**, **Snowflake**, and **Airflow**, along with data quality, monitoring, incident response, and cost management. The same posting lists hands-on experience with Kafka, Snowflake, Iceberg/Delta/Hudi, Airflow, Kubernetes, and distributed systems as relevant technical depth. [ServiceTitan Engineering Manager, Data Foundations](https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan/job/Manager--Software-Engineering_JR114911)

A separate ServiceTitan Senior Software Engineer, Data Platform role reinforces this picture: it calls out batch and real-time pipelines, Kafka or other streaming platforms, Snowflake, Airflow, production monitoring, incident response, and AI-powered agents for operational tasks. [ServiceTitan Senior Software Engineer, Data Platform](https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan/job/Senior-Software-Engineer--Data-Platform_JR114910)

ServiceTitan's communications-data platform is also publicly described as having **communication event streaming** and a reporting pipeline into **Snowflake** so that reporting products, AI systems, AgentOS, and downstream teams receive trusted communication data. [ServiceTitan Staff Product Manager, Communications Intelligence](https://builtin.com/job/staff-product-manager-communications-intelligence/10448969)

That gives us a useful and defensible production mental model:

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

**Important:** the public evidence establishes Kafka/Snowflake as ServiceTitan data-platform technologies. It does **not** establish that every Pantheon agent trace follows exactly this path, nor does it reveal the private topic names, schemas, consumers, retention policies, or internal observability implementation.

### What this means for production agents

This makes the production debugging section earlier in the chapter more concrete.

A useful engineering hypothesis is:

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

The key distinction is:

> **A trace explains one execution. The data platform lets you find patterns across millions of executions.**

That is why Kafka and Snowflake matter to an agent engineer even if the agent itself is implemented with a completely different runtime.

Kafka is useful for moving operational events through the system and feeding downstream consumers. Snowflake is useful for durable analytical history: joining outcomes to versions, cohorts, customer/job attributes, evaluator scores, and other dimensions so engineers can identify systematic failure modes.

For example, a production investigation might ask:

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

## 24. The deeper architectural pattern

The most useful synthesis is:

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

This is why the phrase **AI operating system** is useful.

The differentiator is not merely having an LLM.

It is the system around the LLM that lets many probabilistic components operate against a shared, authoritative model of the business.

## 25. Final mental model

If you remember only one diagram, remember this:

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

And remember the boundary:

> **The agent is not the system.**

The model reasons.

The workflow coordinates.

The state records reality.

The harness controls authority.

The tools change the world.

The evaluation system determines whether the decisions were actually good.

That is the conceptual bridge from a voice agent to an **agentic operating system**.

## References and further reading

### ServiceTitan

- [Pantheon 2026 AI roadmap in this repository](../pantheon-2026-ai-roadmap.md)
- [ServiceTitan: Pantheon 2026 live coverage](https://www.servicetitan.com/blog/pantheon-2026-live-coverage)
- [ServiceTitan: Pantheon 2026 announcements](https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html)

### Salesforce

- [Agentforce Multi-Agent Orchestration](https://www.salesforce.com/agentforce/multi-agent-orchestration/)
- [SOMA, MOMA, MCP, A2A and Agent Gateway](https://help.salesforce.com/s/articleView?id=005317683&language=en_US&type=1)

### Microsoft

- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Agent Framework orchestration samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/orchestrations)
- [Microsoft workflow concepts](https://learn.microsoft.com/azure/ai-services/agents/concepts/workflows)

### LangChain / LangGraph

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents)

### Repository labs

- [Lab 05 — LangChain agent](../../labs/05_langchain_create_agent.ipynb)
- [Lab 06 — LangGraph booking workflow](../../labs/06_langgraph_booking_workflow.ipynb)
- [Lab 09 — Shared context](../../labs/09_shared_context.ipynb)
- [Lab 10 — Coordination and arbitration](../../labs/10_coordination_and_arbitration.ipynb)
- [Lab 11 — Learning loop](../../labs/11_learning_loop.ipynb)
- [Lab 12 — Agent-to-agent booking](../../labs/12_agent_to_agent_booking.ipynb)
