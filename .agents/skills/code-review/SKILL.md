---
name: code-review
description: Review a proposed code change for correctness, regressions, security, and maintainability. Use when asked to review a diff or pull request.
---

# Code review

## Inputs
- The target diff or pull request.
- Relevant acceptance criteria and surrounding implementation.
- Available test, lint, and static-analysis commands.

## Procedure
1. Read the diff and enough surrounding code to understand the behavior.
2. Identify changed contracts, edge cases, error paths, state transitions, concurrency,
   authorization, data handling, and backward compatibility.
3. Trace important claims to concrete code. Do not infer that a bug exists solely from
   unfamiliar style or an unverified assumption.
4. Run targeted checks when permitted and practical. Record exact commands and outcomes.
5. Report findings first, ordered by severity. Each finding must include the affected file
   and line(s), the failure mechanism, impact, and a minimal correction.
6. Separate confirmed defects from questions, risks, and suggestions.

## Output
- Findings with severity and file/line references.
- Tests/checks run and their outcomes.
- Important residual risks or checks not run.

## Stop conditions
- Do not edit the code as part of a review unless explicitly asked.
- Do not claim a test passed unless it actually ran and passed.
- If no findings are identified, say that explicitly and mention review limitations.
