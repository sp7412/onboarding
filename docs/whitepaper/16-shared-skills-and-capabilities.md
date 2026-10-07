# 16 - Shared Skills and Capability Libraries

**Estimated reading time:** 8 minutes · **Facts as of:** October 7, 2026

Extends [chapter 15](15-agentic-orchestration.md) with a reusable capability layer between agents
and orchestration. The registry and marketplace ideas below are architecture analysis, not a
description of ServiceTitan's internal systems.

## Five Takeaways

1. An **agent** is a role (booking, dispatch, intake); a **skill** is a reusable capability several agents can apply (identify customer, check capacity, book, escalate).
2. A production skill is a versioned artifact: applicability, required state, tools, policy, autonomy level, examples, evaluation cases, owner and history.
3. ServiceTitan's Voice Agent has a documented "Skills and Capabilities" settings area that controls which scheduling actions the agent may perform [1]. That is evidence of modular capabilities, not of a cross-agent skills marketplace.
4. Skills are not tools: the tool performs the side effect; the skill encodes when and how to use it, so procedure, reasoning and side effects stay separately testable.
5. Versioned skills let the learning loop work at two levels: is this agent deciding well, and is this capability good across every agent that uses it?

## The distinction

An **agent** is a role in the system: booking, dispatch, voice intake, follow-up, and so on.

A **skill** is a reusable capability that can be applied by multiple agents:

```text
Agents
  |
  +--> Voice Agent
  +--> Booking Agent
  +--> Dispatch Agent
  |
  v
Shared skill library
  |
  +--> identify customer
  +--> classify intent
  +--> check capacity
  +--> book appointment
  +--> reschedule
  +--> confirm appointment
  +--> escalate
  +--> collect payment
```

This avoids implementing the same business capability independently inside every agent.

## What belongs in a skill?

A production skill can be treated as a versioned engineering artifact containing:

- applicability conditions;
- required context/state;
- tools it may invoke;
- procedural instructions;
- policy and constraints;
- autonomy level;
- examples;
- evaluation cases;
- known failure modes;
- performance history;
- owner and lifecycle state.

Conceptually:

```text
Skill
  |
  +-- applicability
  +-- required state
  +-- instructions
  +-- tools
  +-- policy
  +-- autonomy
  +-- examples
  +-- evals
  +-- version
  |
  v
Agent proposes use
  |
  v
Control harness validates
  |
  v
Workflow/tool executes
```

## A shared registry

The library can look like a private marketplace:

```text
discover
   |
   v
validate
   |
   v
evaluate
   |
   v
approve
   |
   v
skill registry
   |
   +--------+--------+
   |                 |
   v                 v
Agent A           Agent B
```

"Marketplace" is a useful architectural metaphor, but it should not be confused with a public product marketplace. A private registry can provide discoverability, versioning, ownership, evaluation, and controlled rollout without allowing arbitrary third-party publication.

## What the public ServiceTitan record supports

ServiceTitan's help center documents a **Skills and Capabilities** settings area for the Voice
Agent that "control[s] which scheduling actions the agent can perform"; use cases such as
appointment cancellation are switched on there [1]. The same page says the agent classifies call
types and assigns AI-generated call reasons to unbooked calls from the transcript [1], which gives
a team a way to spot missing capabilities (that use is our inference).

That is evidence for modular capabilities, but it does **not** prove that Pantheon internally has a centralized cross-agent "skills marketplace" or repository of optimized skills.

Therefore the safe onboarding statement is:

> ServiceTitan publicly demonstrates modular agent skills/capabilities. A shared, versioned capability library used across Pantheon agents is a plausible architectural extension, but its internal existence and implementation are not publicly established.

## Why this matters for the AI operating system

The skill layer fits between agents and orchestration:

```text
EXPERIENCE
    |
    v
AGENTS
    |
    v
SKILLS / CAPABILITIES
    |
    v
ORCHESTRATION
  routing
  arbitration
  policy
    |
    v
SHARED STATE
    |
    v
TOOLS / SYSTEMS
```

This changes the unit of reuse from a prompt to a managed capability.

A booking skill can have its own regression suite, business metrics, version history, canary policy, and autonomy boundary while being consumed by several agents.

## Skills and the learning loop

A mature production loop can continuously improve reusable capabilities:

```text
Skill v42
   |
   v
Agents
   |
   v
Production traffic
   |
   v
traces / outcomes
   |
   v
event stream / analytics
   |
   v
failure mining
   |
   v
evaluation cases
   |
   v
Skill v43
   |
   v
canary
   |
   +----> eligible agents
```

This makes the learning loop operate at two levels:

1. **Agent level:** Is this particular agent making good decisions?
2. **Skill level:** Is this reusable capability good across every agent and workflow that consumes it?

The second question is especially important for an operating system built from many agents.

## Skills versus tools

Do not confuse a skill with a tool.

- **Tool:** a system boundary that performs an operation, such as book_appointment.
- **Skill:** the reusable business capability that determines when and how that operation should be used.
- **Agent:** the reasoning role that decides whether the skill is relevant.
- **Orchestrator:** the runtime that coordinates competing agents and controls execution.

For example:

```text
Booking skill
   |
   +--> check eligibility
   +--> check capacity
   +--> select candidate slot
   +--> validate policy
   +--> propose booking
                |
                v
          book_appointment tool
```

This separation keeps business procedure, reasoning, and side effects independently testable.

## Recommended onboarding exercise

Build one shared booking skill and make both a Voice Agent and a Booking Agent consume it.

Then introduce a new version with an intentional behavioral change.

Measure:

- task success;
- wrong-action rate;
- escalation rate;
- latency;
- tool errors;
- cost;
- business outcome.

Roll the new skill through a canary and compare the two agents separately.

The lesson should be:

> **Reusable skills turn agent improvement into a platform capability rather than a one-agent prompt change.**

## Check your understanding

1. In one sentence each, what separates a tool, a skill and an agent in this chapter?
2. You improve a shared "confirm address" skill and one agent's booking errors fall while
   another agent's rise. What should have caught that before rollout?
3. What does ServiceTitan's public help center actually establish about "Skills and
   Capabilities", and what would be an inference?

**Answer sketches**

1. A tool is a system boundary that performs one operation (`book_appointment`); a skill is
   the reusable business capability that decides when and how to use it, versioned with its
   policy, examples and evaluation cases; an agent is the reasoning role that decides whether
   a skill is relevant (see "Skills versus tools").
2. Versioned skills with per-consumer evaluations and a staged rollout, so each agent that
   depends on the skill is re-evaluated before the new version reaches it.
3. The help center documents Voice Agent settings that control which scheduling actions
   the agent may perform [1]. A cross-agent skills registry or marketplace is a hypothesis
   with no public evidence.

## Sources

1. ServiceTitan Help, Configure your Voice Agent settings in Contact Center Pro (checked October 7, 2026): <https://help.servicetitan.com/docs/configure-your-voice-agent-settings>
