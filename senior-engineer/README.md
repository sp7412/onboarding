# Senior Engineer Judgment Track

The labs teach the stack. This track practices the judgment a senior engineer is hired for:
deciding what a number really means, where an incident probably started, which responsibility
belongs to which layer, and what to build first. Each exercise is a short written problem with
a fictional scenario, a deliverable, and a self-check.

The central pattern, used throughout:

**The model proposes → the application controls → the source of truth verifies.**

## Order and time

| # | Exercise | Time | Builds on | You produce |
|---|---|---|---|---|
| 1 | [What I need to know before day 1](what-i-need-to-know.md) | 20 min | the whole repo | a red/amber/green self-assessment |
| 2 | [Architecture review: model vs. control plane](architecture-review.md) | 45 min | [lab 02](../labs/README.md), [tools and guardrails](../docs/tools-and-guardrails.md) | a responsibility table and a one-page architecture |
| 3 | [Latency budget](latency-budget.md) | 45 min | [latency budget](../docs/voice-agent-architecture.md#latency-budget), lab 08 | two budgets and an annotated trace |
| 4 | [Evaluation and denominator design](eval-design.md) | 60 min | [evaluating voice agents](../docs/evaluating-voice-agents.md), lab 07 | a funnel, metric definitions, ten test cases |
| 5 | [Production incident simulation](production-incident.md) | 60 min | labs 07–08, 09–10 | ranked hypotheses and an incident plan |
| 6 | [First-PR decision tree](first-pr-decision-tree.md) | 20 min | [first 90 days playbook](../docs/first-90-days-playbook.md) | a filled-in "before opening the PR" checklist for one candidate change |
| 7 | [Working hypotheses](hypotheses.md) | 20 min, then ongoing | [Pantheon 2026 brief](../docs/pantheon-2026-ai-roadmap.md) | your pre-start hypotheses, each with a test |
| 8 | [Bookability judge](bookability-judge.md) | 60 min | [Pantheon 2026 brief](../docs/pantheon-2026-ai-roadmap.md), [eval design](eval-design.md), labs 07–08 | a bookability definition, gaming paths, and audit plan |
| 9 | [Autonomy promotion review](autonomy-promotion.md) | 45 min | [earning autonomy](../docs/earning-autonomy.md), [lab 14](../labs/14_earning_autonomy.ipynb) | a per-segment promote/hold decision memo |

About six and a quarter hours in total. Exercises 2–5 are the core; if you only have two hours, do 3 and 4.
After Pantheon 2026 reading (item 7B), do exercise 8 before or with the eval design exercise.
Do exercise 9 after lab 14.

## How to use it

1. **Attempt the exercise before reading its self-check.** The self-check lists what a strong
   answer covers. It is not an answer key; you still have to make the calls.
2. **Write your answers in a private copy** (a personal notes app, or a local `private/`
   folder that is never committed), not in this public repo. That keeps the exercises reusable
   and keeps anything you learn after joining out of public view.
3. **Bring one artifact to a 1:1.** The latency budget, the funnel, the bookability definition,
   or the hypotheses list makes a good concrete prompt for the
   [manager alignment](../docs/manager-alignment.md) conversations.

Every scenario, number and system here is fictional and public-safe. None of it describes a
real production system.
