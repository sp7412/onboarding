# 30-Day Memo

**Audience:** my manager. **Length:** one page.

## How the system works (my understanding)
## Top risks I see
1.
2.
3.

## Where I think I can contribute
1.
2.
3.

## Open questions
## Proposed 60-day deliverable and success metric

## Fictional example

> **Context:** The example below describes an invented voice-agent team and fictional
> measurements. It is not a ServiceTitan status report.

### How the system works (example)

The transport handles audio and turn boundaries; the talker proposes language and tools;
the application validates identity, confirmations, and escalation; a workflow owns the
booking sequence; the scheduling backend remains the source of truth.

### Top risks (example)

1. A retry could create a duplicate job if the commit is not idempotent.
2. Endpointing could cut off phone numbers or addresses.
3. An OOD billing request could be contained instead of transferred.

### Proposed deliverable (example)

Add a regression evaluator for unsafe booking attempts. Success means 100% of the
fictional safety cases remain unbooked, with no increase in appropriate transfer misses.
