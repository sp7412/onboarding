# First-90-Days Question Bank

**Last reviewed:** October 2026

## Purpose

The first 90 days are not only about learning the system. They are an opportunity to
exchange information with people who have context that is not written down.

Do **not** use this as a questionnaire. Pick two to four questions that fit the person and
conversation. Follow interesting answers instead of trying to get through the list.

The highest-value questions usually expose one of four things:

- **strategy** — where the team is actually going;
- **reality** — how production differs from the architecture diagrams;
- **judgment** — how experienced people make tradeoffs;
- **learning** — what the team has learned from success and failure.

## A simple conversation loop

Use:

> **Question → answer → concrete example → implication → follow-up**

For example:

> **Question:** What breaks most often in production?  
> **Answer:** Transfers after long pauses.  
> **Example:** Two recent incidents involved turn timing.  
> **Implication:** The apparent "model quality" problem may actually be a realtime
> control-loop problem.  
> **Follow-up:** Who owns turn-taking, and what metric catches it?

The goal is not to collect answers. It is to discover useful mental models and evidence.

---

## Strategy and vision

Use these with managers, staff engineers, product leaders, and people who have broad context.

- What do you think we're trying to become that isn't obvious from the product today?
- What is the most important technical problem we need to solve over the next 6–12 months?
- Which part of the Pantheon/agent vision do you think matters most?
- Which part of that vision is hardest to make real?
- If we execute exceptionally well over the next year, what becomes possible that isn't
  possible today?
- What do you think we are under-investing in?
- What assumption about the future of agents do you think the team is betting on?

### A particularly high-value question

> **If you could change one thing about the technical strategy today, what would it be?**

---

## Reality versus the architecture

These questions are designed to uncover the gap between a clean system diagram and a
production system.

- What part of the system looks great in a diagram but is still painful in production?
- Where does the agent most often do something technically reasonable but operationally
  wrong?
- Which component causes the most downstream problems?
- What is harder than it initially appears?
- What have we deliberately made deterministic because agents were not reliable enough?
- Where are we relying on a human process because the software isn't ready yet?
- Which abstraction in the system has held up particularly well?
- Which abstraction have we already started regretting?

### Especially useful

> **If I understand the architecture from the docs, what important thing am I still likely
> to misunderstand?**

---

## Reliability and failure

These should become routine questions for engineers, evaluation, infrastructure, and support.

- What breaks most often?
- What failure mode do you worry about that our normal metrics don't capture?
- What works 95% of the time, but the remaining 5% is extremely difficult?
- What is the most expensive or consequential failure we've seen?
- What failures routinely escape the evaluation suite?
- When something goes wrong, what usually turns out to be the actual root cause?
- How do we distinguish a model failure from an orchestration, state, tool, policy, or
  integration failure?
- How do we discover that an agent has gotten worse before customers tell us?
- What is the hardest failure to reproduce?
- What failure mode would make you uncomfortable increasing autonomy?

### Ask for a story

> **Tell me about the worst agent failure you've seen. What actually caused it?**

Then ask:

> **What changed afterward?**

---

## Evaluation and learning

The important question is not merely whether the team has evaluations. It is whether
production experience reliably changes what gets evaluated.

- What is the most trusted signal that an agent is improving?
- Which metrics do people look at but not really trust?
- How does a production failure become a regression test?
- Who decides which failures become evaluation cases?
- How do we know an evaluation set is representative?
- How do we detect regressions that only appear in a particular customer, job type, region,
  channel, or time of day?
- How do we evaluate improvements when business outcomes take days or weeks to observe?
- What does a good canary look like here?
- How do we know when an agent is ready for more autonomy?

### Strong follow-up

> **What's an example where offline evaluation said we improved something, but production
> disagreed?**

---

## Autonomy and control

These questions connect the agent architecture to the real authority boundary.

- Which actions can agents take without approval today?
- Which actions are recommendation-only?
- What determines when a capability earns more autonomy?
- Where do we intentionally keep a human in the loop?
- What is the most important guardrail around consequential actions?
- What happens when an agent proposes something that is technically valid but economically
  undesirable?
- Where should deterministic code have authority over an LLM?
- What would have to become true before you would trust this system to take action
  automatically?

A useful framing is:

> **Where has the system earned trust, and where has it not?**

---

## Shared context, skills, and reusable capabilities

These questions are especially relevant after the Pantheon/shared-capability work.

- What capabilities do multiple agents need to share today?
- Where are we duplicating the same capability across agents?
- Do we think of capabilities as reusable platform assets, or does each agent mostly own
  its own behavior?
- How do we know when a capability is good enough to reuse broadly?
- When we improve a capability, how do we make sure we don't improve one agent while
  silently hurting another?
- How are shared capabilities versioned and rolled out?
- Is there a capability or skill that you wish every agent could use today?
- What should be centralized, and what should remain agent-specific?

### Important distinction

Do not assume that "skills marketplace" is the team's terminology or implementation.
Use neutral language first:

> **How do you think about reusable capabilities or skills across agents?**

Then follow their terminology.

---

## Production operations

Ask these of infrastructure, platform, SRE, and engineers who operate the system.

- What is the most common source of production incidents?
- What signals do you look at first when an agent starts behaving differently?
- How do you trace a bad customer outcome back to the exact agent/model/tool decision?
- What is difficult to observe today?
- Where do latency spikes usually come from?
- What causes the most expensive operations?
- What is hardest to roll back?
- Which dependencies are most fragile?
- What happens when a downstream tool is slow or unavailable?
- What does a good incident review look like here?

### Very high-value question

> **If the wrong technician gets booked tomorrow morning, how would we investigate it?**

This forces the conversation across state, orchestration, model behavior, tools, telemetry,
evaluation, and business data rather than staying at the component level.

---

## Success stories

New engineers often spend too much time asking about problems and not enough time learning
what good looks like.

Ask:

- What recent AI/agent improvement are you most proud of?
- What actually made that improvement successful?
- Tell me about a capability that went from experimental to genuinely useful.
- What's the best example you've seen of an agent improving a customer or contractor
  outcome?
- What is an example where a small engineering change had a surprisingly large impact?
- What did the team learn from that success that we now apply elsewhere?
- What is a project that looked risky but worked?

### The key follow-up

> **What do you think was the real reason that worked?**

This often produces more useful information than the success story itself.

---

## Failure stories

Ask for stories, not just lists of failure modes.

- Tell me about the worst production failure you've seen.
- Tell me about a failure that initially looked like a model problem but wasn't.
- Tell me about a time we had to roll something back.
- Tell me about something that looked promising offline but failed in production.
- Tell me about the most surprising agent behavior you've seen.
- Tell me about a customer interaction that changed how the team thought about the product.
- Tell me about a problem that took much longer to diagnose than expected.
- What did the team change after that?

A particularly revealing question:

> **What painful lesson does the team already know that isn't written down anywhere?**

---

## Technical judgment and tradeoffs

Use these with senior engineers and architects.

- What tradeoffs does the team make repeatedly?
- Where do we sacrifice model quality for latency, reliability, cost, or controllability?
- What should be deterministic today that could eventually become agentic?
- What looks like an AI problem but should actually be solved with conventional software?
- Where are we being unnecessarily conservative?
- Where are we being too aggressive?
- Which technical decision has aged particularly well?
- Which technical decision would you make differently today?
- What is the most important constraint that newcomers tend to overlook?

### The reset question

> **If you were starting this system over today, what would you build differently?**

---

## Organizational knowledge

Technical systems are also shaped by ownership and decision-making.

- Who owns the customer outcome, rather than just the component?
- Which decisions are centralized and which are intentionally distributed?
- Where do technical decisions actually get made?
- Who is the person I should talk to when I hit a problem in this area?
- Which teams do we depend on most?
- Where do handoffs between teams tend to break down?
- What does the team wish other teams understood better?
- What decision tends to take longer than it should?

---

## Future bets

Once you have enough context to ask informed questions:

- What do you think will matter most six months from now?
- What technology are we experimenting with that could become important?
- Which current architecture decision is likely to be revisited?
- What capability do you think will unlock the next major step?
- What are we building now that you suspect will eventually be replaced?
- What would you bet on if you had to pick one technical direction for the next year?
- What do you think the team will be surprised by?

---

## Role-specific picks

### Manager

Pick from:

1. What is the most important outcome for the team this quarter?
2. What gap do you most need this role to fill?
3. What would make you worried about my ramp at day 30 or 60?
4. What technical problem do you most want someone to own?
5. What does a great first six months look like?

### Senior/staff engineer

1. What part of the architecture is hardest to get right?
2. What failure mode worries you most?
3. What decision would you make differently today?
4. Where should deterministic software have authority over the model?
5. What does the architecture diagram leave out?

### Product / PM

1. Which customer outcome matters most?
2. Which metric do you trust most, and which do you distrust?
3. What customer behavior surprised the team?
4. What capability would create the most value if it became reliable?
5. What is the biggest gap between what customers want and what the system can safely do?

### Evaluation / quality

1. What failures escape our evals?
2. How does a production failure become a regression case?
3. Which metric is most predictive of real customer quality?
4. What does a good eval set look like here?
5. Where do offline and production results disagree?

### Infrastructure / platform

1. What fails most often?
2. Where does latency come from?
3. How do we trace a bad outcome end-to-end?
4. What is hardest to roll back?
5. Which dependency would you worry about during a major traffic spike?

### Support / operations

1. What do customers complain about that our metrics don't capture?
2. What failures create the most repeated customer effort?
3. What work do humans still do because the agent isn't trustworthy enough?
4. What is the most common reason an agent interaction gets escalated?
5. What does a genuinely great interaction look like to you?

---

## Questions that should probably be retired or de-emphasized

The repository already has manager-alignment questions covering:

- priorities;
- success at 30/60/90;
- stakeholders;
- ramp;
- communication preferences;
- decision rights;
- feedback;
- working norms.

Those are still important, but they belong in the **manager alignment** conversation rather than
the general question bank.

The new question bank should focus more heavily on information that is difficult to obtain
from documentation.

In particular, avoid spending valuable peer time asking:

> "What are the team's top priorities?"

when you could ask:

> **"What do you think we're getting wrong about the problem we're trying to solve?"**

The second question is much more likely to produce information you could not have obtained
from the onboarding docs.

---

## The first-week minimum set

If time is limited, ask these eight questions across different people:

1. **What are we trying to become that isn't obvious from the product today?**
2. **What part of the architecture looks better on paper than it works in production?**
3. **What breaks most often?**
4. **Tell me about the worst agent failure you've seen.**
5. **Tell me about the best agent improvement you've seen.**
6. **How do we discover that an agent got worse before customers tell us?**
7. **If you were starting this system over today, what would you build differently?**
8. **What painful lesson does the team already know that isn't written down anywhere?**

That set deliberately spans **vision → architecture → reliability → failure → success →
evaluation → technical judgment → tribal knowledge**.

---

## Capture the answer, not just the question

For important conversations, maintain a private evidence log:

| Question | Answer | Evidence/example | Implication | Follow-up |
|---|---|---|---|---|
| What breaks most often? | … | … | … | … |
| What are we trying to become? | … | … | … | … |
| What failure worries you? | … | … | … | … |

Do not put confidential answers or internal implementation details into this public repository.
Keep the real notes in an approved company system.

The goal after 30 days should be more than knowing the architecture.

You should be able to say:

> **Here is what the team says the system is trying to accomplish, here is how it actually
> behaves, here are the highest-value failure modes, here are examples of genuine success,
> here are the assumptions I still need to validate, and here is where I think I can contribute.**
