# Lab 10 Solution Sketch

Track moves per customer across days in a small registry the dispatch rule consults, and
refuse a second move inside the week regardless of the requester's expected value.

```python
moves_this_week: dict[str, int] = {}

def consent_and_limit(job, ask):
    if moves_this_week.get(job.customer, 0) >= 1:
        return False                      # protection rule: no second move this week
    moves_this_week[job.customer] = moves_this_week.get(job.customer, 0) + 1
    return True                           # in production: ask the customer

board = full_board()
ok, _ = request_move(board, board.lowest_value_slot(), consent_and_limit)
assert ok
# Next day: Avery's job is on today's board again and another high-value lead wants the slot.
board2 = full_board()
ok2, why = request_move(board2, board2.lowest_value_slot(), consent_and_limit)
assert not ok2
```

Keep the rule outside the arbiter (a hard rule or the receiver's own policy). If it were a
cost term, a big enough expected value would eventually buy a second move.

## Extension solution sketch: one slot, competing claims

Use a single authoritative reservation function as the linearization point. It must check
slot ownership and the expected schedule version and record the idempotency key in the same
atomic operation. A simplified contract is:

```python
def reserve(slot_id, expected_version, idempotency_key):
    if idempotency_key in results:
        return results[idempotency_key]  # retry returns the original outcome
    if expected_version != schedule.version:
        return Conflict("stale version")
    if schedule.slot_owner(slot_id) is not None:
        return Conflict("slot already claimed")
    result = schedule.commit_reservation(slot_id, idempotency_key)
    results[idempotency_key] = result
    return result
```

In a real implementation, the version check, ownership check, reservation write, and
idempotency record must be one database transaction or equivalent atomic operation; the
pseudocode above is a contract, not thread-safe code. On conflict, refresh and re-evaluate.
On an ambiguous timeout, retry with the same key, then verify authoritative state. Never
interpret a tool timeout as proof that the write failed or succeeded. Keep customer consent
and approval requirements outside expected-value scoring.
