# First PR Decision Tree

The objective is to make a useful contribution without manufacturing work before you
understand the system.

## 1. Is there an obvious low-risk defect?

Examples: incorrect documentation, broken test, misleading log message, stale dependency,
missing regression case.

**Yes:** fix it, add evidence, and ship it.

**No:** continue.

## 2. Is there recurring developer friction?

Look for repeated manual steps, unclear local setup, weak test fixtures, poor debugging
information, or an expensive feedback loop.

**Yes:** propose the smallest reversible improvement.

**No:** continue.

## 3. Is there an evaluation blind spot?

Ask whether an important failure mode lacks a deterministic regression test, trace view,
or evaluator.

**Yes:** add the smallest failure-driven eval you can justify.

**No:** continue.

## 4. Is there an operational risk with a clear owner?

Do not take ownership merely because you noticed it. Confirm ownership and desired outcome first.

**Yes:** offer a narrowly scoped contribution.

**No:** keep learning.

## Before opening the PR

Confirm:
- problem and affected users
- current behavior
- expected behavior
- owner/stakeholder
- smallest useful change
- test/evaluation evidence
- rollback path
- whether the change creates operational burden

## Senior-level rule

A good first PR is not the biggest thing you can build.

It is evidence that you can improve the system **without increasing risk faster than you
increase understanding**.
