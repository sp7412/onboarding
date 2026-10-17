---
name: test-and-evaluate
description: Convert acceptance criteria into executable checks and report verification evidence. Use before declaring a code change ready.
---

# Test and evaluate

## Procedure
1. Extract observable acceptance criteria and identify safety or correctness invariants.
2. Map each criterion to a deterministic test, a manual check, or an explicitly unresolved gap.
3. Select the smallest useful test set first; include regression, boundary, failure-path,
   and negative tests where applicable.
4. Inspect project instructions and use the repository's documented commands and environment.
5. Run checks and preserve their exact command, exit status, and meaningful output.
6. Diagnose failures instead of silently retrying, skipping, or weakening the test.
7. Review whether tests are flaky, environment-dependent, or insufficiently isolated.
8. Summarize what is verified and what remains unverified.

## Output
| Acceptance criterion | Evidence/check | Result | Limitation |
|---|---|---|---|

Include commands run, tests skipped and why, environmental constraints, and any unresolved
risks.

## Guardrails
- Never say tests passed if they were not executed.
- Do not edit expected outputs merely to make a test pass without establishing correctness.
- Distinguish unit tests, integration tests, evaluation datasets, and production telemetry.
