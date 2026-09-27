# Lab 07 Solution Sketch

For `looked_up_first`, return a boolean based on the first tool name, with an explicit
empty-trajectory case. For a booking-count metric, define the denominator first:

```python
booking_rate = sum(o["outcome"] == "booked" for o in outputs) / len(outputs)
```

Keep invariant evaluators such as emergency-never-booked deterministic. Use an LLM
judge only for qualities such as tone, with a calibrated human-reviewed set.
