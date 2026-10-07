# First-PR Decision Tree

**Time:** 20 minutes now, then use it in weeks 2–4 · **Builds on:** [first 90 days playbook](../docs/first-90-days-playbook.md), [manager alignment](../docs/manager-alignment.md)

The goal is a useful first contribution without manufacturing work before you understand the
system.

## 1. Is there an obvious low-risk defect?

Examples: incorrect documentation, a broken or flaky test, a misleading log message, a stale
dependency, a missing regression case.

**Yes:** fix it, add evidence, and ship it. **No:** continue.

## 2. Is there recurring developer friction?

Look for repeated manual steps, unclear local setup, weak test fixtures, poor debugging
information, or a slow feedback loop. Did you hit it yourself during onboarding? That's
evidence, and onboarding is the only time you'll see it with fresh eyes.

**Yes:** propose the smallest reversible improvement. **No:** continue.

## 3. Is there an evaluation blind spot?

Does an important failure mode lack a deterministic regression test, a trace view, or an
evaluator? Candidates from the [eval exercise](eval-design.md): false confirmations, duplicate
writes after retries, emergencies handled as routine, bookability misjudged.

**Yes:** add the smallest failure-driven eval you can justify. **No:** continue.

## 4. Is there an operational risk with a clear owner?

Don't take ownership just because you noticed it. Confirm the owner and the outcome they want
first.

**Yes:** offer a narrowly scoped contribution. **No:** keep learning, and write down what you
noticed in your [working hypotheses](hypotheses.md).

## Before opening the PR

Confirm:

- the problem and who is affected
- current behavior
- expected behavior
- the owner or stakeholder, and that they want this
- the smallest useful change
- test or evaluation evidence
- a rollback path
- whether the change adds operational burden (alerts, dashboards, on-call)
- the team's norms: PR size, review expectations, how changes are flagged and rolled out

## The rule

A good first PR is not the biggest thing you can build. It is evidence that you can improve the
system **without increasing risk faster than you increase understanding**.

## Self-check

Pick one plausible candidate change (fictional is fine) and fill in "Before opening the PR"
for it. If you can't name the owner, the evidence, or the rollback path, it isn't ready, and
the question to ask in your next 1:1 is whichever one is missing.

---

Part of the [senior engineer judgment track](README.md).
