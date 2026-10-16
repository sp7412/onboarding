# 17 - Running Agents in Production: Traces, Failure Mining, Evaluation and Rollout

**Estimated reading time:** 10 minutes · **Facts as of:** October 7, 2026

Continues [chapter 15](15-agentic-orchestration.md), which covers how agents are coordinated.
This chapter covers how they are run once they are live: tracing each decision, mining
production failures, evaluating changes and rolling them out safely. It was split out of
[Chapter 15](15-agentic-orchestration.md) on October 7, 2026; the content is unchanged apart from section numbers.

It pairs with [Design by Evaluation](../design-by-evaluation.md), which treats evaluation as a
design input. That doc's [section 6, "Finding failures in production"](../design-by-evaluation.md#6-finding-failures-in-production)
and [section 7, "Failure mining creates new evals"](../design-by-evaluation.md#7-failure-mining-creates-new-evals)
overlap with sections 2 and 3 here; read them together rather than twice.

For a symptom-first production response, use the [Voice Agent Production Troubleshooting Runbook](../voice-agent-production-troubleshooting.md), which maps caller-visible failures to telemetry, likely causes, containment, and recovery checks.

As in [Chapter 15](15-agentic-orchestration.md), the architecture below is generic. Nothing here describes ServiceTitan's
internal systems; the only ServiceTitan evidence is public job listings about its data
platform [1][2].

## Five Takeaways

1. Trace the decision, not just the request: every run needs a correlated trace of model calls, tool calls, policy decisions, approvals and the final outcome.
2. Debugging means walking back from a bad outcome to the decision boundary that failed, then saving that case as an evaluation example.
3. A trace explains one execution; an analytical store lets you find patterns across millions, so design the IDs that join them before production.
4. Evaluate at four levels (runtime, agent, policy, business outcome), offline before release and online on sampled production traces.
5. Roll out with canaries judged on guardrail metrics first, stratified A/B tests and shadow mode; for contractor playbooks, treat technician feedback as evidence for a reviewed, versioned learning loop.

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

## 5. Learning from technician feedback: improve the playbook, not just the model

The production learning loop applies to more than conversational agents. A contractor's
operating knowledge also lives in **playbooks** (how work is diagnosed and performed) and a
**pricebook** (the catalog of sellable services, materials, equipment, and their pricing).
These are different assets with different risk profiles:

- A **playbook** guides a decision or procedure: what to inspect, in what order, when to stop,
  and when to escalate.
- A **pricebook** defines what can be quoted or sold: item identity, scope, labor assumptions,
  material compatibility, price, and related terms.

They may share job evidence, but a technician saying a diagnostic step is missing must not
silently change a price, labor allowance, or catalog item. Treat each change type as a separate,
versioned proposal with its own reviewers and acceptance criteria.

This section uses an illustrative **AC-not-cooling** playbook. It is a systems design example,
not an HVAC service procedure or a substitute for manufacturer instructions, company policy,
licensing requirements, or qualified technical judgment.

### The feedback event: preserve what was reported

Suppose a technician chooses **Missing diagnostic step** after working a job. Do not immediately
ask an LLM to rewrite the playbook. First capture a small, structured event tied to the job and
the exact playbook version. The initial report should be lightweight; permitted job evidence can
be linked later.

```json
{
  "feedback_id": "uuid",
  "feedback_type": "playbook_defect",
  "category": "missing_diagnostic_step",
  "status": "needs_evidence",
  "source": {
    "technician_id": null,
    "submitted_at": null,
    "submission_channel": null
  },
  "context": {
    "job_id": null,
    "equipment_id": null,
    "equipment_type": "HVAC",
    "symptom": "AC not cooling",
    "playbook_id": "ac-not-cooling",
    "playbook_version": null,
    "step_id": null
  },
  "observation": {
    "original_text": null,
    "expected_step": null,
    "actual_workflow": null,
    "reason_step_was_needed": null
  },
  "evidence": {
    "measurements": [],
    "diagnostic_findings": [],
    "parts_used": [],
    "labor_minutes": null,
    "attachments": [],
    "repair_outcome": null,
    "callback_within_window": null
  },
  "assessment": {
    "interpreted_issue": null,
    "candidate_revision_id": null,
    "confidence": null,
    "supporting_feedback_ids": [],
    "contradicting_evidence": []
  },
  "review": {
    "technical_approval": null,
    "safety_approval": null,
    "publication_approval": null
  },
  "audit": {
    "created_at": null,
    "published_revision_id": null
  }
}
```

Null means **unknown or not supplied**, not false. In this example, technician details, playbook
version, and the actual missing step are unknown and must remain unknown. Preserve the original
report immutably; store corrections and AI interpretations in linked records so auditors can
distinguish what the technician said from what the system inferred. Use stable IDs and controlled
enums in implementation. Keep sensitive customer/job data behind access controls rather than
copying it into every event.

### Evidence to collect

Use progressive enrichment instead of requiring a long form from a technician in the field.

| Stage | Evidence | Why it matters |
|---|---|---|
| Initial triage | Playbook/version, step if known, technician's description, equipment family | Locate and understand the alleged gap |
| Technical validation | Relevant readings, diagnostic codes, observations, actual sequence, approved reference | Determine whether a step is justified and where it belongs |
| Outcome | Confirmed cause, work performed, parts, labor, verified result, repeat visit/callback | Test whether the step improved the result |
| Pattern validation | Similar reports, workarounds, equipment configuration, season, successful counterexamples | Separate recurring gaps from one-off cases |

Distinguish a genuinely missing step from an existing step that was overlooked, a model-specific
exception, a training/usability problem, or a case outside the playbook's scope. Repeated reports
raise investigation priority but do not prove the suggested change is correct. One credible
safety-critical report may justify immediate expert review even without duplicates.

### Example: AC-not-cooling feedback

The illustrative playbook might guide a technician to confirm the complaint, collect relevant
observations, follow approved diagnostic checks, determine whether evidence supports a diagnosis,
present an estimate, perform authorized work, and verify the outcome. This is a high-level
workflow only; exact checks must come from approved HVAC guidance.

A technician selects **Missing diagnostic step**. With no description or evidence, the system
creates a `needs_evidence` record and asks a short follow-up: *What check did you need that the
current playbook did not include, and what did it help establish?* It should not guess.

After evidence is supplied, an AI assistant may draft a candidate revision containing:

- the proposed step and trigger conditions;
- where it fits in the current sequence;
- the observation or result to record;
- stop conditions and escalation paths;
- supporting and contradicting cases;
- confidence, unresolved questions, and the exact playbook version affected.

The draft remains a **proposal**, not live guidance. If evidence shows that a step applies only
to one equipment family, encode that applicability explicitly rather than adding needless steps
to every job.

### End-to-end learning workflow

```text
Technician feedback
        |
        v
Immutable feedback event + job/playbook IDs
        |
        v
Enrich with permitted job evidence and outcomes
        |
        v
Triage: duplicate, incomplete, safety-sensitive, or actionable?
        |
        v
Cluster similar reports; inspect counterexamples
        |
        v
Draft a versioned candidate playbook revision
        |
        v
Technical review + safety/policy review
        |
        v
Replay historical cases and run regression evaluations
        |
        v
Authorized owner approves a limited pilot
        |
        v
Monitor outcomes, compare with baseline, roll back if needed
        |
        v
Retain feedback, decision, version, and measured outcome
```

Rejection and revision are first-class outcomes. A reviewer may find that the step already
exists, that the issue reflects training or usability trouble, or that evidence is insufficient.
Those decisions are useful labels for improving triage and documentation; they are not failed
automation to discard.

### Evaluation: measure outcomes, not agreement with a suggestion

Define the intended improvement and guardrails before testing a proposed change. Evaluate it
against a fixed, versioned set of historical jobs and expert-authored scenarios.

| Dimension | Evaluation question |
|---|---|
| Diagnostic completeness | Does the candidate cover the confirmed gap? |
| Correctness | Does it distinguish plausible causes without asserting unsupported diagnoses? |
| Safety and compliance | Are required precautions, stop conditions, and escalation preserved? |
| Applicability | Does the step run only for relevant equipment/configurations? |
| Efficiency | Does it reduce avoidable rework without adding needless steps elsewhere? |
| Field outcome | Do verified repairs, callbacks, and first-time-fix performance improve? |
| Usability | Can technicians understand and follow the revised instructions? |
| Regression | Does it degrade other symptom or equipment cohorts? |

Treat safety and policy failures as hard gates, not values that can be traded against an average
score. An LLM judge may help classify feedback or compare text, but it must not be the sole
authority for technical correctness. Use deterministic checks where possible and qualified human
labels for domain-specific judgments. Do not optimize only for revenue, average ticket, or job
duration.

Compare versions on comparable cases. Job difficulty, equipment age, region, season, technician
experience, parts availability, and customer decisions can confound before/after comparisons.
Use randomized pilots where appropriate; otherwise stratify cohorts and document limitations.

### Approval gates and ownership

1. **Triage gate.** Link the report to a real job and playbook version where possible. Request
   missing context; do not treat a signal as a confirmed defect.
2. **Technical gate.** A qualified HVAC subject-matter expert validates the step, applicability,
   expected observation, and authoritative reference.
3. **Safety/policy gate.** Confirm required safety controls, licensing constraints, and escalation
   conditions. Safety-sensitive changes require the designated qualified approver.
4. **Evaluation gate.** Historical replay, scenario tests, and regression checks meet predefined
   acceptance criteria. Critical failures block release.
5. **Publication gate.** An authorized playbook owner approves the exact diff, version, rationale,
   applicability, and rollback plan.
6. **Monitoring gate.** Release to a limited cohort and compare against baseline and guardrails.
   Pause or roll back if safety, correctness, callbacks, or agreed measures regress.

The path depends on change class. A wording clarification may need less review than a new
diagnostic procedure; price, labor, and catalog changes need their own approval policies.
Feedback about a missing diagnostic step never grants authority to change pricebook values.

### What the system learns over time

The learning system is more than a fine-tuned model. Its durable assets are linked feedback,
evidence, approved revisions, evaluation cases, reviewer decisions, and observed outcomes.
Models can assist with extraction, deduplication, clustering, applicability suggestions, and
drafting. Statistical analysis can surface recurring patterns and estimate whether an approved
change helped. Qualified owners remain accountable for operational guidance.

Preserve the lineage:

```text
feedback -> evidence -> proposal -> review decision
         -> published version -> job outcome -> evaluation set
```

This lets the system learn from rejected proposals, false alarms, and regressions as well as
successful changes. Keep company-specific knowledge and cross-customer patterns appropriately
segregated: one contractor's procedures, prices, or customer records must not silently become
another contractor's policy. Cross-business learning requires appropriate data rights, privacy
controls, and evidence that a pattern generalizes.

A strong first release is deliberately modest: capture structured reports, enrich them from
permitted job records, cluster repeated issues, and draft versioned revisions for human review.
Add automated rollout only for narrowly defined change classes after the evaluation and approval
policy is proven. **The AI proposes; evidence tests; authorized people approve; production
outcomes close the loop.**

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
