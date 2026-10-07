# Shared Skills and Capability Libraries

**Purpose:** Extend the agentic-orchestration model with a reusable capability layer.

## The distinction

An **agent** is a role in the system: booking, dispatch, voice intake, follow-up, and so on.

A **skill** is a reusable capability that can be applied by multiple agents:

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

## A shared registry

The library can look like a private marketplace:

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

"Marketplace" is a useful architectural metaphor, but it should not be confused with a public product marketplace. A private registry can provide discoverability, versioning, ownership, evaluation, and controlled rollout without allowing arbitrary third-party publication.

## What the public ServiceTitan record supports

ServiceTitan currently documents **Skills & Capabilities** as a real Voice Agent product concept. The settings include independently configurable scheduling capabilities such as booking, confirming/rescheduling, cancellation, and after-hours booking. ServiceTitan also describes an ongoing tuning process in which teams review unbooked calls and identify capability gaps.

That is evidence for modular capabilities, but it does **not** prove that Pantheon internally has a centralized cross-agent "skills marketplace" or repository of optimized skills.

Therefore the safe onboarding statement is:

> ServiceTitan publicly demonstrates modular agent skills/capabilities. A shared, versioned capability library used across Pantheon agents is a plausible architectural extension, but its internal existence and implementation are not publicly established.

## Why this matters for the AI operating system

The skill layer fits between agents and orchestration:

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

This changes the unit of reuse from a prompt to a managed capability.

A booking skill can have its own regression suite, business metrics, version history, canary policy, and autonomy boundary while being consumed by several agents.

## Skills and the learning loop

A mature production loop can continuously improve reusable capabilities:

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
