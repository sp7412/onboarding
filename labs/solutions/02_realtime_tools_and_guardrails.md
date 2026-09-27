# Lab 02 Solution Sketch

Keep the counter in `CallState`, because the application owns the policy and it must
survive model retries. A minimal shape is:

```python
if enforce and len(st.offered_slot_ids) >= 2:
    raise be.PolicyError("slot_offer_limit", "Only two windows may be offered.")
```

In production, count offers separately from returned slot IDs and record the policy
decision in the audit log.
