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
