# Solution sketch: lab 13 · Mini-Max

## Seeded bug (section 4)

`priority_agent` reads `min_status="proposed"`, so it acts on facts the control plane never
verified. Read the verified view instead, and treat a missing fact as unknown:

```python
def priority_agent(ledger, call_id):
    facts = ledger.view(call_id)                      # verified only (the default)
    if "urgency" not in facts and "replacement_interest" not in facts:
        return "normal"                               # unknown is not "high"; a person can upgrade it
    return "high" if facts.get("urgency") == "same_day" or facts.get("replacement_interest") else "normal"
```

Don't fix it by lowering the floor or changing the extractor. The consumer states the trust
level it needs.

## Graded exercise: add `callback_window`

1. **Labels and extractor.** Add `callback_window` (`morning`, `afternoon`, `evening`,
   `unknown`) to the dataset labels and `FIELD_NAMES`, `ALLOWED` and `CONFIDENCE_SPREAD` in
   `minimax.py`. Keep it out of `CRITICAL_FIELDS`: it shouldn't decide whether to book.
2. **Contract.** Add it to `call-facts.schema.json` with an enum, and to `required`.
3. **Permissions.** `voice_agent` already may write `callback_window` in
   `context.DEFAULT_PERMISSIONS`. Check that no other agent can.
4. **Consumer.** A callback scheduler reads `ledger.view(call_id)` and uses the window only
   if it's verified; otherwise it asks.
5. **Tests.**
   - Schema validation passes with the new field.
   - A `callback_window` at confidence 0.40 doesn't appear in `facts.trusted(0.85)` or the
     verified ledger view.
   - For every call, `decide_bookability` returns the same action with and without the
     low-confidence field (the field can't change a decision).

## Check your understanding

1. `sentiment_flipped` and `urgency_wrong` change no booking decision here, so they cost
   nothing in this system. `job_type_wrong` changes no decision either, but books the wrong
   work. The boundary that matters is "what gets booked", not just "whether".
2. The extractor is the component being guarded against. A screen on the raw words, owned by
   the control plane, still works when the extractor is confidently wrong.
3. Wrong bookings cost much more than missed ones. Rejecting more uncertain facts loses some
   automation but avoids enough expensive mistakes to lower the total, up to the point where
   it starts rejecting mostly correct facts.
