# 30/60/90-Day Onboarding Checklist

Theme: **learn the domain → ship something small → own a measurable piece of agent quality.**
Adjust dates once the team's rhythm is clear.

## Pre-start (now → Oct 25)

### Week of Sept 28: Technical warm-up
- [ ] Set up a personal venv and run labs 00–03 offline
- [ ] Create free-tier accounts (OpenAI, LiveKit Cloud, LangSmith) under a personal email
- [ ] Run lab 01 §5 live and hear real Realtime audio
- [ ] Note 3 things that surprised me about the event protocol

### Week of Oct 5: Stack depth
- [ ] Labs 04–06; run `realtime_agent.py console` and talk to it
- [ ] Fill in the latency worksheet in the study guide with real numbers
- [ ] Break the agent 5 ways (interrupt, read a phone number slowly, say "uh-huh," mention gas, confirm the wrong address) and log what happened

### Week of Oct 12: Evaluation + synthesis
- [ ] Labs 07–08; write my answer to the study question in [`notes/study-question.md`](../notes/study-question.md)

### Week of Oct 19: Domain + logistics
- [ ] Watch ServiceTitan's Pantheon 2025 keynote and the Pro Products session
- [ ] Read the Contact Center Pro, Atlas, Scheduling Pro and Dispatch Pro product pages
- [ ] Build out [`notes/glossary.md`](../notes/glossary.md)
- [ ] Finalize [`templates/1on1-questions.md`](../templates/1on1-questions.md) for my manager
- [ ] Home office: second monitor, headset for listening to calls, stable network
- [ ] Take at least 2 days fully off before the 26th

## Days 1–30: Learn and earn trust

### Week 1 (Oct 26–30): Orientation
- [ ] Finish HR, security and compliance onboarding promptly
- [ ] Get access: repos, CI, cloud consoles, observability, ticket tracker, Slack channels, call recordings (per PII policy)
- [ ] First 1:1 with my manager (questions in `templates/1on1-questions.md`)
- [ ] Get the dev environment running locally
- [ ] Read all of the team's architecture docs
- [ ] Start the onboarding log (internal copy, from `templates/onboarding-log.md`); 5 minutes daily

### Week 2 (Nov 2–6): Map the system
- [ ] Trace one real production call end to end: telephony → transport → model → tools → scheduling backend → traces
- [ ] Draw the architecture diagram; have a teammate mark it up
- [ ] List where the real system differs from my lab mental model
- [ ] Identify the owner of each component
- [ ] Ship the first small PR (doc fix, test, logging) to learn review and CI norms
- [ ] 1:1s with my PM and the evals/observability owner

### Week 3 (Nov 9–13): Customer and quality
- [ ] Listen to 20+ recorded agent calls; tag each as success, failure, or awkward
- [ ] Write down the top 5 failure patterns
- [ ] Learn how booking rate, escalation rate, containment and latency are computed; find the dashboards
- [ ] Read recent incident reports or postmortems, if the team keeps them
- [ ] 1:1s with the telephony/infra owner and a support or CSR-facing person
- [ ] Ship a second PR that touches agent behavior

### Week 4 (Nov 16–20): Synthesize
- [ ] Write the 30-day memo (`templates/30-day-memo.md`)
- [ ] Review it with my manager; agree on the 60-day deliverable and its success metric
- [ ] Update and share the architecture diagram

**Day-30 exit criteria**
- [ ] Can explain the production architecture from memory
- [ ] 2+ PRs merged
- [ ] 60-day deliverable agreed in writing

## Days 31–60: Contribute and specialize

### Weeks 5–6: Scope and design
- [ ] Write the design doc (`templates/design-doc.md`)
- [ ] Review with my manager plus one senior engineer
- [ ] Measure the baseline *before* changing anything
- [ ] Candidate deliverables:
  - [ ] **Eval harness:** turn flagged production calls into regression tests with code evaluators
  - [ ] **Guardrails/escalation:** detect calls the agent shouldn't handle (OOD work) and escalate cleanly
  - [ ] **Latency:** waterfall of where dead air comes from, then one targeted fix

### Weeks 7–8: Build
- [ ] Ship in small increments behind a flag or to a test cohort
- [ ] Weekly status (`templates/weekly-status.md`)
- [ ] Shadow on-call or an incident review at least once
- [ ] Pair with a teammate on their task to learn another part of the system

**Day-60 check (with my manager)**
- [ ] Show progress against the baseline
- [ ] Confirm the deliverable is still the right bet, or adjust
- [ ] Ask: "What should I do more of, and less of?"

## Days 61–90: Own and lead

### Weeks 9–10: Ship
- [ ] Roll out to production (or the full target cohort)
- [ ] Measure the before/after change, including what didn't work
- [ ] Add monitoring or an alert for regressions
- [ ] Write a runbook: how it works, how to debug it, who owns it

### Weeks 11–12: Propose and multiply
- [ ] Next-quarter proposal (2 pages): problem, why now, expected impact, rough plan
- [ ] Present it to my manager and PM
- [ ] Run one knowledge-share (brown-bag or wiki page)
- [ ] Review others' PRs in my area of strength

### Week 13: Retro
- [ ] Write the 90-day retro (`templates/90-day-retro.md`) and review it with my manager
- [ ] Update résumé and LinkedIn with the shipped outcome (public-safe wording)

**Day-90 exit criteria**
- [ ] One deliverable in production with a measured impact
- [ ] Next-quarter proposal reviewed
- [ ] Go-to person for at least one area

## Recurring (every week)
- [ ] 5 minutes of onboarding-log notes daily
- [ ] 3-line status to my manager
- [ ] Listen to 5 production calls
- [ ] One coffee chat outside my immediate team
- [ ] Friday: review this checklist and move anything slipping

## Watch-outs
- **Ship small and reversible;** evals are the safety net, not up-front perfection
- **Frame wins in contractor outcomes** (booked jobs, missed calls, CSR time), not model metrics
- **Ask "dumb" questions early;** the window closes around day 45
