# 14 - Implications And Open Questions

**Estimated reading time:** 9 minutes · **Facts as of:** October 7, 2026

This chapter turns the paper into a working brief for the first 90 days. It focuses on
options and hypotheses to test.

## Five Takeaways

1. The job, in one sentence: help the voice agent turn more of a contractor's calls into *correct* booked work, safely, and prove it with numbers the business trusts.
2. The highest-leverage engineering is at the boundaries: tool validation, claim grounding, escalation, and evaluation.
3. Evaluation, out-of-distribution detection and latency work are strong entry points for an ML engineer with a rigorous-testing background.
4. Speak in contractor outcomes (booked jobs, recovered revenue, fewer missed calls, CSR hours) because that's how the company measures itself (GTV, share of wallet).
5. Most of what matters (architecture, metrics, incidents, priorities) can only be learned inside. Arrive with sharp questions, not answers.

## What the business cares about (from chapters 01–05, 11)

- **Revenue flowing through the platform (GTV)** and the company's **share of wallet**. [ch. 01]
- **Retention**, which depends on contractors trusting the platform with their customers. [ch. 01, 12]
- **The AI strategy** (Atlas, Max, Virtual Agents), which is company-level. [ch. 01, 06, 13]
- **Peak-day performance**, because demand and call volume spike with weather. [ch. 02, 04]

## Where an ML engineer adds leverage

| Area | Why it matters | First move |
|---|---|---|
| **Evaluation** | Agent quality has to be measured on committed state, repeated trials and real call slices | Map the current eval set and metrics; propose adding claim-grounding and repeat-trial (pass^k) checks (ch. 12; lab 07) |
| **Out-of-distribution and escalation** | Calls the agent shouldn't handle (emergencies, unusual requests, confused callers) must be detected and handed off | Measure escalation correctness; prototype a detector for "outside the rules" calls |
| **Latency** | Dead air and interruptions drive abandonment | Build an end-to-end latency waterfall per call phase (lab 08) |
| **Grounding and guardrails** | False confirmations and wrong bookings are silent, costly failures | Audit tool boundaries: identity, ownership, offered-slot, idempotency checks (lab 02) |
| **Robustness** | Noisy lines, accents, Spanish-speaking callers | Slice metrics by audio condition and language |

## Hypotheses to test after joining

1. Booking rate on *bookable* calls is lower on peak days than on normal days.
2. A meaningful share of escalations are avoidable, and a meaningful share of non-escalations
   should have escalated.
3. Some agent confirmations don't match committed state (measured by comparing transcripts
   and records).
4. Agent-booked jobs have different cancellation or reschedule rates than CSR-booked jobs.
5. Latency spikes cluster in specific call phases (lookups, availability searches).

Each can be checked with data in the first 30–60 days and turned into a scoped project.

## New open questions after Pantheon 2026

ServiceTitan's October 6, 2026 announcements and keynotes described the voice agent as one of
30 coordinated agents in Max, a voice intelligence agent that judges whether each call was a
bookable lead, and Homh, which makes contractors bookable through consumer AI assistants.
[1][2][3] Full notes: [Pantheon 2026 AI roadmap brief](../pantheon-2026-ai-roadmap.md). These
raise questions that only the team can answer:

- **Shared context:** what does the voice agent write for dispatch and lead scoring, with
  what confidence, and who verifies it? (Teaching draft: [call facts contract](../call-facts-contract.md).)
- **Bookability judge:** how is voice intelligence evaluated, and does the voice agent's
  reported booking rate now use its denominator?
- **Arbitration:** when booking, dispatch and demand agents disagree, where does the decision
  live, and how is it tested?
- **New channels:** are Homh and partner AI CSR bookings held to the same identity, capacity
  and policy checks as phone bookings?
- **Earned autonomy:** the CEO said some customers let the voice agent take 100% of calls. [2]
  What evidence gates moving a customer from overflow to all calls, and what triggers a
  step back? (Lab 14 models one approach.)
- **Learning loop:** which downstream outcomes (completed jobs, job value, cancellations) feed
  back to the voice agent, and how quickly?

Analysis: these extend the hypotheses above from one agent to a system of agents;
[chapter 15](15-agentic-orchestration.md) is the background reading.

## Questions to ask, by audience

**Manager:** What does success look like at 30, 60 and 90 days? Which metrics does leadership
watch for voice agents? What's the biggest current risk?

**Product manager:** Which customer pain drives Virtual Agent purchases? What do churned or
unhappy customers say? How do Virtual Agents relate to Atlas and Max?

**Evaluation and observability owner:** How are calls turned into eval data? What's labeled,
by whom, and how is PII handled? What regressions got through recently?

**Telephony and infrastructure:** What happens on peak days? Where are the latency budgets?
What are the fallbacks when a provider degrades?

**Support and CSR partners:** Which agent behaviors frustrate callers or CSRs? What should a
warm transfer carry that it doesn't today?

**Customers (when possible):** What made you trust (or distrust) the agent? What would you
never let it do?

## How to use this paper

- Read the essentials path before day one (see the introduction).
- Revisit chapters 04, 07, 11 and 12 during week 3, when the checklist has you listening to
  calls and learning the metrics.
- Replace this chapter's hypotheses with real answers as you learn them, in private notes, not
  in this public repo.

## Related repo material

- Plan: [30/60/90 checklist](../../plan/30-60-90-checklist.md) and
  [first-90-days playbook](../first-90-days-playbook.md)
- Labs: tool guardrails (02), turn-taking (03), evaluation (07), latency (08)
- Study question: [notes/study-question.md](../../notes/study-question.md)
- Multi-agent labs: shared context (09), arbitration (10), learning loop (11),
  agent-to-agent booking (12), call-facts capstone (13), earning autonomy (14)

## Sources

1. ServiceTitan press release, "ServiceTitan Announcing New and Expanded Capabilities at Pantheon 2026" (October 6, 2026): <https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html>
2. Investing.com, ServiceTitan at Pantheon 2026, keynote summary and transcript (October 6, 2026): <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
3. ServiceTitan, "Pantheon 2026: Live coverage from ServiceTitan" (live blog, read October 7, 2026): <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
