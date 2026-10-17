---
name: evidence-first-debugging
description: Diagnose a software failure by testing competing hypotheses before changing code. Use for bugs, flaky tests, unexpected outputs, and production-like incidents.
---

# Evidence-first debugging

## Procedure
1. Restate the observed failure, expected behavior, reproduction conditions, and impact.
2. Separate direct observations from assumptions. Capture logs, stack traces, inputs,
   environment, versions, and a minimal reproduction where possible.
3. List at least two plausible hypotheses when the evidence does not uniquely identify
   the cause. For each, state what evidence would support or falsify it.
4. Choose the cheapest discriminating experiment; change one variable at a time.
5. Reproduce the failure before modifying implementation when practical.
6. Fix the demonstrated mechanism, not merely the visible symptom.
7. Add a regression test that fails before the fix and passes afterward.
8. Run targeted tests, then broader relevant checks. Inspect the final diff for unrelated
   changes and new failure modes.

## Output
- Observations and unresolved unknowns.
- Hypotheses and the evidence that distinguishes them.
- Root cause, or the best-supported explanation if root cause remains uncertain.
- Fix, regression test, verification commands, and residual risks.

## Guardrails
- Never invent log output or claim an experiment was performed when it was not.
- Do not suppress an exception, loosen an assertion, or add a retry without explaining why
  that change addresses the underlying failure.
- Stop and ask before destructive actions or access to sensitive data.
