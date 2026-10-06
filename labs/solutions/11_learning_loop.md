# Lab 11 Solution Sketch

Update in weekly batches and clamp each week's change.

```python
CAP = 250
assumptions = dict(SIGNAL_UPLIFT)
labelled = with_true_type(closed)
for week in range(4):
    batch = labelled[week * 100:(week + 1) * 100]
    est = fit_uplifts(batch, list(assumptions))
    for sig, (obs, n) in est.items():
        proposed = shrink(assumptions[sig], obs, n, k=20)
        step = max(-CAP, min(CAP, proposed - assumptions[sig]))
        assert abs(step) <= CAP
        assumptions[sig] += step
print(assumptions)
```

The cap trades speed for safety: a true shift takes several weeks to absorb, but one odd week
can't swing every decision. Log each step with its evidence so large moves can be reviewed.
