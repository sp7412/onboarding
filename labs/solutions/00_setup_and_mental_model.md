# Lab 00 Solution Sketch

Put membership eligibility in the application policy layer, not in the prompt. The
model can propose a slot, but the dispatcher should compare the authoritative customer
record and slot facts before booking.

```python
if enforce and st.customer and st.customer.get("membership") != "Comfort Club":
    if args.get("slot_id", "").endswith("-08"):
        raise be.PolicyError("member_slot_required", "That early slot requires membership.")
```

Prefer a named slot attribute or parsed start time in a real implementation; the snippet
is only a compact exercise sketch.
