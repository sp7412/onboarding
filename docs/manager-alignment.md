# Setting Goals With Your New Manager

**Last reviewed: October 6, 2026**

The first few conversations with a new manager set the trajectory for everything after them.
The aim is simple: by the end of week two, you and your manager should agree, in writing, on
what success looks like at 30, 60 and 90 days, how it will be judged, and how you'll work
together. This guide keeps those conversations natural while making sure the basics aren't
missed.

> Use this page to prepare. Keep the real notes and the written agreement in company systems
> (your notes app, a shared doc your manager can see), not in this public repo.

## The plan in one view

| When | Conversation | What you leave with |
|---|---|---|
| Before day 1 | Prepare (below) | Your hypotheses, questions and constraints |
| Week 1, first 1:1 | **Getting aligned**: their world, expectations, how you'll work | Notes, and agreement that you'll draft goals |
| End of week 2 | **Turning it into goals**: review your draft, plus a 15-minute pre-mortem | A written 30/60/90 agreement with named risks |
| Day 30 | **Calibration**: you and your manager rate progress separately, then compare | Gaps surfaced early; adjusted goals |
| Day 60, 90 | **Check-ins**: progress against the agreement | Adjusted goals; see the [playbook](first-90-days-playbook.md) contracts |
| Weekly | Three-line status | No surprises in either direction |

## Before the first 1:1

Spend 20 minutes on three things:

1. **Your hypotheses.** From the whitepaper and labs: what you think the team's problems are,
   and where you could help (evaluation, guardrails, latency, out-of-distribution detection).
   Hold them loosely; the point is to test them, not to pitch them.
2. **What you bring and what you're new to.** Be ready to say both plainly: deep evaluation
   and ML experience; new to SaaS release pace, the trades and production voice agents.
3. **Your constraints.** Anything your manager should know early: planned time off, working
   hours and time zone, anything that affects availability.

Two more things to start before day one:

4. **A one-page "working with me" doc** ([template](../templates/working-with-me.md)): how
   you communicate, when you focus, how you like feedback, what you're strong at and new to.
   Share it in your first 1:1. It answers the questions a good manager would ask anyway (see
   Lara Hogan's first-1:1 questions under Further reading), so the meeting can focus on them.
5. **A brag document** ([template](../templates/brag-document.md)): a running record of what
   you did and its impact, updated every Friday and linked to your goals. You'll use it at
   every check-in and your first review.

## Conversation 1: Getting aligned (week 1)

Before this conversation, review the [Pantheon hypothesis map](hypothesis-map.md). Bring a short list of public-grounded hypotheses and ask which ones are most important to validate first. Keep answers learned after day one in company systems, not this public repo.

Let it be a conversation, not an interview. Start broad, follow their energy, and come back
to anything you didn't cover. Rough flow, with phrasing you can adapt:

**1. Their world first** (about 10 minutes)
- "What are the team's top priorities this quarter, and why those?"
- "What's going well right now, and what's keeping you up at night?"
- "How does the team's work show up for customers and in the metrics leadership watches?"

**2. Why this role exists** (5 minutes)
- "What gap were you hoping this hire would fill?"
- "Where do you see me adding the most value in the first six months?"

**3. What success looks like** (10–15 minutes)
- "At 30, 60 and 90 days, what would make you say this is going well?"
- "How will we know? What would you look at?" (ask for something observable: a merged
  change, a design reviewed, a metric moved, a person who'd vouch for it)
- "Who else will form an opinion of my work, and what matters to them?"
- "What will *your* manager judge this team on this quarter?" (Your goals should help your
  manager's goals. Senior engineers keep their influence by staying aligned with the people
  who sponsor their work; see "Staying aligned with authority" under Further reading.)
- "What would make you worried at day 30 or 60?"

**4. Time frames and pace** (5 minutes)
- "What's a realistic ramp here? When do people usually ship their first change?"
- "Are there dates I should plan around: releases, planning cycles, reviews, freezes?"
- "When is the next performance review or calibration, and what does the level expect?"
- "Is there a written career ladder or rubric for my level? Can we map my goals to it?"

**5. How we'll work together** (10 minutes)
- "How do you like updates: Slack, a doc, the 1:1? How often?"
- "Which decisions can I make on my own, which should I run by you, and which need others?"
- "When something's going wrong, how early do you want to hear about it?"
- "How often should we meet, and what should the 1:1 be for?"
- "What are the working norms I should know: hours, on-call, response times?"

**6. Feedback** (5 minutes)
- "How do you prefer to give feedback, and how often?"
- "I'd rather hear things early and directly. Is that how you like to work too?"
- "Is there anything from how past hires ramped up that I should do differently?"

**7. Close** (5 minutes)
- Play back what you heard in two or three sentences.
- "I'll draft 30/60/90 goals from this and send them by <day>. Can we review them next week?"

### When answers are vague

Vague answers are normal early on. Don't push for precision in the moment; offer to do the
work: "That's helpful. Let me take a first pass at what that could look like and you can
react to it." A concrete draft is easier for a busy manager to correct than to invent.

## Conversation 2: Turning it into goals (end of week 2)

Draft before the meeting, and send it a day ahead. Aim for three to five goals across these
kinds:

| Kind | Purpose | Fictional example |
|---|---|---|
| **Learning** | Prove you understand the system and the business | "By day 30, walk the team through an end-to-end call trace and a system map, corrected by a senior engineer." |
| **Delivery** | Ship something real, small at first | "By day 30, two merged changes; by day 60, one scoped improvement behind a flag with a baseline measured." |
| **Impact** | Move an outcome the business cares about | "By day 90, a measured improvement in <agreed metric> for <agreed call type>, with an evaluation that guards it." |
| **Relationships** | Earn trust across the people you depend on | "By day 30, 1:1s with PM, evals owner, infra and a support partner; one shared next step with each." |

For each goal, agree on: **what** (the outcome), **how it's measured**, **by when**, **who
else is involved**, and **what's out of scope**. Ask directly: "If I hit these, would you
consider the first 90 days a success?" If the answer is anything but yes, adjust now.

### The pre-mortem (15 minutes, same meeting)

Ask: "Imagine it's day 90 and my first three months went badly. What most likely happened?"
List every answer without arguing, then turn the top two or three into goals, check-in
questions or early warning signs in the agreement. It surfaces your manager's real worries
faster than "what does success look like?" Use the [pre-mortem template](../templates/pre-mortem.md).

## The written agreement (send within a day)

Keep it to one page, in a doc your manager can comment on:

```text
30/60/90 agreement — <your name> / <manager>, <date>

Team priorities this quarter: …
Why this role exists: …

Goals
1. <goal> — measure: … — by: … — involves: …
2. …
Out of scope for now: …

How we work
- Updates: <format>, <cadence>
- 1:1: <cadence>, used for …
- Decisions: mine / run by you / need others: …
- Escalate early when: …
- Feedback: …

Top risks (from the pre-mortem) and early warning signs: …
Level expectations this maps to: …

Key dates: <reviews, releases, planning>
Check-ins: day 30 <date>, day 60 <date>, day 90 <date>
```

## Don't-miss checklist

By the end of week two, make sure you know:

- [ ] The team's top priorities, and the one metric or outcome that matters most
- [ ] What success looks like at 30, 60 and 90 days, and how each will be judged
- [ ] Who else's opinion matters (peers, PM, skip-level) and what they care about
- [ ] Your decision rights: what you can decide, what to run by your manager, what needs others
- [ ] Update format and cadence, and how early to raise problems
- [ ] 1:1 cadence and purpose
- [ ] How and when feedback will be given, in both directions
- [ ] Review cycle, level expectations, and key dates
- [ ] Working norms: hours, on-call, response times
- [ ] Your first project and what's explicitly out of scope
- [ ] What your manager is worried about (the pre-mortem's top risks)
- [ ] What your manager will be judged on this quarter, and how your goals help
- [ ] The career ladder or rubric for your level, mapped to your goals
- [ ] Access you still need, and who to meet next

## Keeping the trajectory

- **Weekly:** a three-line update (done, next, blocked or decision needed). See the
  [weekly status template](../templates/weekly-status.md).
- **Monthly:** revisit the agreement in a 1:1. Mark goals on track, at risk or changed, and
  say why. Changing a goal is fine; changing it silently isn't.
- **Fridays:** five minutes on the brag document; link each entry to a goal.
- **Day 30 calibration:** before the check-in, you and your manager each rate every goal
  (on track, at risk, off track) and write one sentence why. Compare. Where the ratings
  differ is the most useful conversation you'll have all month.
- **Day 30, 60, 90:** use the agreement as the agenda, alongside the
  [30-day memo](../templates/30-day-memo.md) and [90-day retro](../templates/90-day-retro.md).
- **Watch for misalignment:** surprises in feedback, priorities shifting without discussion,
  or work you thought mattered getting little attention. Raise it early: "I want to make sure
  I'm focused on the right things. Is <X> still the priority?"

## Repair conversations

Misalignment is normal; letting it sit is what hurts. A few scripts:

- **Checking focus:** "Last week I prioritized X over Y. Would you have chosen differently?"
- **After a surprise in feedback:** "That's helpful, and I didn't see it coming. What would
  have told me earlier, so I can watch for it?"
- **Asking for specific feedback:** "What's one thing I should do more of, and one thing less
  of?" Ask every couple of weeks; it's easier to answer than "any feedback?"
- **When priorities shift without discussion:** "I noticed <change>. Is that the new priority,
  and should I adjust the agreement?"
- **When you need more support than you're getting:** say what you need concretely, and build
  a wider support crew (below) rather than waiting.

## Working remotely

Visibility doesn't happen by default when you're fully remote. Agree on these in week 1:

- **Overlap hours** when you're reliably available for quick questions.
- **Written-first updates:** the weekly status, plus a short note whenever you finish or
  unblock something, so progress is visible without meetings.
- **When to use what:** Slack for quick questions, a doc for anything needing feedback, a call
  when a thread goes past three back-and-forths.
- **Camera and meetings:** team norms for video, and which meetings matter most to attend live.
- **In-person time:** ask early whether there are offsites or visits, and plan to attend one in
  the first 90 days if possible.

## Build your support crew

No single manager can give you every kind of support. In the first month, find on purpose:

- **A mentor** outside your direct line, for perspective and career advice.
- **A peer buddy** on the team, for "how do we actually do this here?" questions.
- **A senior engineer or staff partner**, for technical judgment and context.
- **A sponsor**, over time: someone who'll speak up for your work where you're not in the room.

Lara Hogan calls this building a "Voltron" (see Further reading).

## Coming from a defense program

A few habits worth adjusting deliberately:

- **Ask about the pace.** "How finished should something be before I share it?" Product teams
  often want an early, rough draft rather than a polished one.
- **Make uncertainty easy to act on.** Instead of "it depends," say "I'd bet on A; here's
  what would change my mind; I'll know by Friday."
- **Name your strengths as offers, not credentials.** "I've built evaluation and
  out-of-distribution checks for high-stakes systems; happy to apply that here if useful."

## Further reading

- **Lara Hogan, "Questions for our first 1:1":** <https://larahogan.me/blog/first-one-on-one-questions/>.
  The questions a good manager asks a new report; read it to volunteer the answers.
- **Julia Evans, "Get your work recognized: write a brag document":** <https://jvns.ca/blog/brag-documents/>.
  Why and how to keep a running record of your work and share it with your manager.
- **Will Larson, "Staying aligned with authority":** <https://staffeng.com/guides/staying-aligned-with-authority/>.
  How senior engineers keep their influence by staying aligned with their sponsor.
- **Will Larson, "Work on what matters":** <https://staffeng.com/guides/work-on-what-matters/>.
  Choosing work, and pacing yourself, as expectations rise.
- **Lara Hogan, "When your manager isn't supporting you, build a Voltron":** <https://larahogan.me/blog/manager-voltron/>.
  Why to build a wider support crew.
- **Kim Scott, Radical Candor:** <https://www.radicalcandor.com/our-approach/>. A shared
  vocabulary for direct feedback in both directions.
- **Camille Fournier, *The Manager's Path* (O'Reilly, 2017):** the early chapters on being
  managed and on senior technical roles explain what good management looks like from the inside.

## Related

- [First 90 days playbook](first-90-days-playbook.md)
- [1:1 questions](../templates/1on1-questions.md)
- Templates: [working with me](../templates/working-with-me.md), [pre-mortem](../templates/pre-mortem.md), [brag document](../templates/brag-document.md)
- [30/60/90 checklist](../plan/30-60-90-checklist.md)
