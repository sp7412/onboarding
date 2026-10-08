# 17 - Running Agents in Production: Traces, Failure Mining, Evaluation and Rollout

**Estimated reading time:** 10 minutes · **Facts as of:** October 7, 2026

Continues [chapter 15](15-agentic-orchestration.md), which covers how agents are coordinated.
This chapter covers how they are run once they are live: tracing each decision, mining
production failures, evaluating changes and rolling them out safely. It was split out of
chapter 15 on October 7, 2026; the content is unchanged apart from section numbers.

It pairs with [Design by Evaluation](../design-by-evaluation.md), which treats evaluation as a
design input. That doc's [section 6, "Finding failures in production"](../design-by-evaluation.md#6-finding-failures-in-production)
and [section 7, "Failure mining creates new evals"](../design-by-evaluation.md#7-failure-mining-creates-new-evals)
overlap with sections 2 and 3 here; read them together rather than twice.

As in chapter 15, the architecture below is generic. Nothing here describes ServiceTitan's
internal systems; the only ServiceTitan evidence is public job listings about its data
platform [1][2].

## Five Takeaways

1. Trace the decision, not just the request: every run needs a correlated trace of model calls, tool calls, policy decisions, approvals and the final outcome.
2. Debugging means walking back from a bad outcome to the decision boundary that failed, then saving that case as an evaluation example.
3. A trace explains one execution; an analytical store lets you find patterns across millions, so design the IDs that join them before production.
4. Evaluate at four levels (runtime, agent, policy, business outcome), offline before release and online on sampled production traces.
5. Roll out with canaries judged on guardrail metrics first, stratified A/B tests and shadow mode; release, trace and evaluation form one loop.

## 1. Production observability: trace the decision, not just the request

A production agent that cannot be traced is extremely difficult to debug.

For every meaningful agent run, capture a correlated trace such as:

```text
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
```

For a multi-agent system, extend the same trace across the graph:

```text
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
```

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

```text
"The agent booked the wrong technician."
```

The trace should let an engineer walk backward:

```text
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
```

This is much more useful than looking only at the final answer.

LangSmith is one example of a tracing/evaluation platform that can provide this kind of agent run visibility. OpenTelemetry is the broader vendor-neutral instrumentation model. The exact production stack is an implementation choice.

## 2. Debugging production agents and mining failure cases

Tracing is only useful if engineers can go from a production symptom to the exact decision path that caused it.

A practical incident workflow is:

```text
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
```

### Example: "the agent booked the wrong technician"

An engineer should be able to search production telemetry for:

```text
outcome = "wrong_technician"
agent = "booking"
date >= yesterday
policy_result = "allowed"
```

Then drill into the individual traces:

```text
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
```

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

```text
Find all traces where:
  - booking agent
  - candidate version = v42
  - tool = availability
  - latency > 2 seconds
  - outcome = failed
```

or:

```text
Find the top 100 traces where:
  - evaluator_score < threshold
  - policy = allowed
  - no human intervention
```

or:

```text
Compare:
  v41 vs v42
  for the same job classes
  by:
    task success
    wrong-action rate
    escalation
    p95 latency
    cost
```

### Turn production failures into the eval set

This is one of the most important production-agent practices:

```text
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
```

Do not simply collect the worst examples. Also sample successful traces so the evaluation set does not become a collection of pathological cases. Maintain slices for important cohorts and failure modes.

### Event streaming vs long-term analytical storage

**Generic pattern, not a description of ServiceTitan's agent architecture.** A common production
architecture separates **operational event transport** from **durable analytical storage**:

```text
Agent runtime
    |
    | OpenTelemetry/events
    v
+----------------+
| Event stream   |
| (e.g. Kafka)   |
|                |
+-------+--------+
        |
   +----+----+
   |         |
   v         v
real-time  durable
consumers  data platform
              |
              v
  warehouse (e.g. Snowflake)
              |
      +-------+-------+
      |               |
   analytics       evaluation
   / dashboards    / failure mining
```

An event stream such as Kafka is well suited to moving high-volume events to many consumers; a warehouse such as Snowflake is well suited to retaining and querying history: outcomes, versions, cohorts and evaluator scores. ServiceTitan's public job listings name both in its data platform [1][2] (see [chapter 15, "What we can and cannot infer about ServiceTitan"](15-agentic-orchestration.md#18-what-we-can-and-cannot-infer-about-servicetitan)), but how its agents use them is not public.

For an agent team, the important distinction is:

> **The trace system explains one execution; the analytical system lets you find patterns across millions of executions.**

For example, a trace can explain one bad booking. A warehouse query can show that a rise in booking failures is concentrated in one combination, say model v42 with tool v7 on evening traffic (a made-up example), which no single trace would reveal.

### What to persist for failure mining

A useful durable event schema includes:

```text
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
```

Keep large payloads such as transcripts and tool bodies separately governed when appropriate. The analytical event should contain enough identifiers and structured metadata to find the detailed trace without making every warehouse row a copy of sensitive conversation data.

### Debugging is a join across systems

In a mature production environment, the engineer often needs to correlate:

```text
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
```

That correlation should be designed **before** production. A trace ID that disappears when the request crosses an agent, tool, queue, or service boundary makes distributed debugging dramatically harder.

## 3. Evaluation: define success before changing the agent

An agent can be technically successful while being operationally bad.

```text
"Tool call succeeded"
         !=
"Business outcome was good"
```

For example:

```text
Booking API: 200 OK
Agent run: SUCCESS

But:
- wrong technician;
- poor route;
- customer unhappy;
- margin below threshold.
```

Production evaluation therefore needs multiple levels:

```text
Level 1: runtime correctness
  Did the workflow complete?

Level 2: agent correctness
  Did it choose an appropriate action?

Level 3: policy correctness
  Was the action permitted?

Level 4: business outcome
  Did the action improve the target metric?
```

A useful evaluation record is:

```json
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
```

This allows offline regression tests and online production evaluation to use the same conceptual schema.

### Offline evaluation

Before deployment, maintain a representative evaluation set:

```text
scenario
   |
   +--> expected facts
   +--> expected constraints
   +--> acceptable actions
   +--> unacceptable actions
   +--> expected outcome
```

Run the candidate agent against the set and compare:

```text
baseline agent
      vs.
candidate agent
```

Do not rely on one aggregate score. Track safety/policy failures separately from quality metrics. A small average improvement is not worth a large increase in dangerous or unauthorized actions.

### Online evaluation

Production evaluation can sample real traces and score them asynchronously:

```text
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
```

This closes the loop between what the model *said* and what the system *actually did*.

## 4. Canary releases and A/B testing for agents

Agent changes should be treated like production software changes, not just prompt edits.

A practical rollout looks like:

```text
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
```

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

```text
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
```

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

```text
real request
     |
     +----------> current agent --> real action
     |
     +----------> candidate agent --> proposal only
                                  |
                                  v
                               compare
```

The candidate observes production-like inputs and generates decisions, but its proposed side effects are not executed.

This is especially valuable for consequential agents because it measures real-distribution behavior without giving an unproven model authority.

### Canary + trace + evaluation form one system

These are not separate DevOps features:

```text
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
```

That is the production learning loop around the agent.

## Check your understanding

Try the question before reading the sketch below it.

1. A customer reports that the wrong technician was booked. Which three systems do you need
   to join to explain it, and what must have been captured at decision time?

**Answer sketch**

1. The agent trace (what it saw and proposed), the source of truth (what was committed and
   when) and the analytical history (similar cases and outcomes), joined on stable IDs
   captured when the decision was made (sections 1–2).

## Sources

1. ServiceTitan job listing, Engineering Manager, Data Foundations (checked October 7, 2026; listings expire): <https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan/job/Manager--Software-Engineering_JR114911>
2. Built In, ServiceTitan Staff Product Manager, Communications Intelligence (checked October 7, 2026; listings expire): <https://builtin.com/job/staff-product-manager-communications-intelligence/10448969>

## Further reading

- [Chapter 15: agentic orchestration](15-agentic-orchestration.md), especially section 18 on what can and cannot be inferred about ServiceTitan's data platform
- [Design by Evaluation](../design-by-evaluation.md) and [Earning autonomy](../earning-autonomy.md)
- Labs: [07 tracing and evaluation](../../labs/07_langsmith_tracing_evals.ipynb), [11 learning loop](../../labs/11_learning_loop.ipynb), [14 earning autonomy](../../labs/14_earning_autonomy.ipynb)
