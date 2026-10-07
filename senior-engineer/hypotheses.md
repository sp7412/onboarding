# Working Hypotheses

**Time:** 20 minutes before day 1, then a few minutes a week

A template for separating what you *know* from what you *assume*. Before you start, fill it
with hypotheses drawn from public material. After you start, keep the live version in a
**private** place (company notes, or a local `private/` folder that is never committed). This
file stays a blank template with public examples.

| Hypothesis | Observed evidence | Inference | Confidence | How to test | Status |
|---|---|---|---|---|---|
| | | | | | Open |

## Public examples to start from

Each example is grounded only in public statements from Pantheon 2026, which are company
claims (see the [Pantheon brief](../docs/pantheon-2026-ai-roadmap.md)). They are guesses about
how things might work, not facts about internal systems.

| Hypothesis | Public evidence | How to test after joining |
|---|---|---|
| The booking-rate denominator comes from a separate post-call judge (which calls *were* bookable), so that judge's accuracy bounds every booking metric | The company said in-product booking rates are easy to game, so it built a "voice intelligence" agent that reviews every call to decide whether it was a bookable lead | Ask how the judge is evaluated, how often it disagrees with human reviewers, and whether it is the same model family as the agent it grades |
| Facts from the call (job type, urgency, tone) reach lead scoring and dispatch through shared context | Lead scoring was described as using what was said on the call and the customer's tone; the coordination system was described as sharing context across agents | Trace one call's facts to a downstream decision |
| Customers grant the voice agent autonomy gradually, based on evidence | Voice agents were placed at level 2 of a five-level AI maturity model; some customers reportedly let the agent handle all calls with CSRs on standby | Ask what evidence moves a customer from "after hours only" to "all calls", and who decides |
| Phone, text, web and external AI assistants share one booking control plane | Booking was described as multi-channel, and Homh announced booking by homeowners' AI agents (ChatGPT, Gemini, Claude) | Compare the guardrails on two channels |
| Demand-side agents can change the volume and mix of calls the voice agent receives | Demand forecasting was described as standing ads down when the schedule is forecast full | Ask whether demand changes are annotated on voice-agent dashboards |

## Rules

- **Observed:** directly measured, documented, or demonstrated to you.
- **Inferred:** a conclusion supported by evidence but not directly established.
- **Unknown:** not yet established.
- **Confidence:** your current belief. It doesn't replace evidence.
- **How to test:** the cheapest useful experiment, trace, conversation, or measurement.

## Useful questions

- What do I know because I saw it?
- What do I believe because someone told me?
- What am I assuming because the architecture diagram suggests it?
- What would falsify this?
- Who owns the source of truth?
- What production evidence would settle the question?

Never copy internal architecture, customer data, traces, metrics, incidents, credentials, or
other confidential information into this public repository.

---

Part of the [senior engineer judgment track](README.md).
