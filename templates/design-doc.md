# Design Doc: <title>

**Author:** · **Reviewers:** · **Status:** draft

## Problem
## Success metric and baseline
## Approach
## Alternatives considered
## Rollout plan (flag, cohort, rollback)
## Monitoring and evaluation
## Risks and open questions

## Fictional example

**Title:** Block routine booking when address confirmation is not grounded

**Problem:** An invented agent sometimes books after a caller chooses a slot but before
the caller confirms the service address.

**Success metric and baseline:** In a fictional eight-case regression set, unsafe booking
rate is 2/8. Target is 0/8 while keeping happy-path booking correctness unchanged.

**Approach:** Store the caller transcript in application state and reject `create_job`
unless the verified customer, offered slot, and grounded confirmation are present.

**Rollout:** Run offline first, then a fictional canary behind a flag with rollback to
the prior tool policy.
