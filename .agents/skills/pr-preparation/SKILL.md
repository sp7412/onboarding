---
name: pr-preparation
description: Prepare a code change for pull-request review by checking scope, tests, documentation, and risk. Use when asked to prepare or update a PR.
---

# Pull-request preparation

## Procedure
1. Confirm the task, intended base branch, and the branch/worktree being modified.
2. Inspect repository instructions, status, diff, and changed-file list.
3. Check for accidental generated files, secrets, unrelated edits, debugging leftovers,
   and unreviewed dependency changes.
4. Map the change to acceptance criteria. Run relevant tests, lint, type checks, and builds
   that the project documents and environment supports.
5. Update documentation and examples when user-visible behavior or setup changes.
6. Draft a concise PR summary: problem, implementation, risks, verification, and rollout notes.
7. Report exact branch, commit, PR URL, and CI state when available.

## Guardrails
- Do not commit, push, merge, release, or deploy unless the user or surrounding workflow
  explicitly authorizes that action.
- Do not report a clean working tree or successful CI without checking it.
- Treat passing tests as evidence, not a guarantee; disclose skipped checks and limitations.
