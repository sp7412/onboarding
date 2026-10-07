# Solution sketch: lab 14 · Earning autonomy

## Graded exercise: stricter re-validation after drift

Track a per-segment state alongside the level:

```python
state = {s: {"paused": False, "stable_weeks": 0, "approved": False} for s in VOLUME}

guard = drift_guard(baseline_mix[seg], mix_now, baseline_feats[seg], feats_now)
st = state[seg]
if guard["pause"] and not st["paused"]:
    bounded[seg] = max(0, bounded[seg] - 1)
    evidence[seg] = [0, 0]
    st.update(paused=True, stable_weeks=0, approved=False)
elif st["paused"]:
    if week == approval_week[seg]:                 # a person signs off on the new baseline
        baseline_mix[seg], baseline_feats[seg] = mix_now, feats_now
        st["approved"] = True
    if st["approved"]:
        st["stable_weeks"] = st["stable_weeks"] + 1 if not drift_guard(
            baseline_mix[seg], mix_now, baseline_feats[seg], feats_now)["pause"] else 0
    if st["stable_weeks"] >= 2:
        st["paused"] = False                       # evidence counts again from next week
else:
    evidence[seg][0] += errors
    evidence[seg][1] += volume
    d = promotion_policy(*evidence[seg], bounded[seg])
    if d.level != bounded[seg]:
        bounded[seg], evidence[seg] = d.level, [0, 0]
```

Assertions to add: plumbing is demoted in week 8; `max(level for plumbing, weeks 8–12) < 3`;
and HVAC and electrical never enter `paused`.

## Exercises

1. **External AI assistant bookings.**
   - *Error:* a booking the homeowner didn't confirm, or the wrong job or slot.
   - *Targets:* tighter than phone, because no person heard the request; for example 10%,
     5%, 1% and 0.5%, with n ≥ 300 per step at 95%.
   - *Cost ratio:* a wrong booking is at least 5× a missed one.
   - *Drift signals:* new client IDs, request-volume spikes, and an unusual mix of job types or
     ZIP codes (lab 12).
2. **For a manager:** "In plumbing the agent makes the right call about 97% of the time on
   ordinary weeks, but we don't yet have enough plumbing calls to be sure it's above our bar
   for acting without review. When we opened the new area, its mistakes tripled, so we
   stepped it back to 'act and notify' until it proves itself on the new traffic. HVAC has
   the evidence and runs on its own."
3. **Dashboard:**
   - per segment: level, decisions this week, errors, n since the last level change, Wilson
     bounds vs. the target
   - safety: wrong bookings, emergencies not transferred
   - coverage (share handed to people)
   - calibration (ECE, and a reliability diagram per month)
   - drift (PSI, OOD rate)
   - a log of every promotion, demotion and pause, with the reason and the owner

## Check your understanding

1. Promotion should require evidence that the agent is good enough; the upper bound says
   "even pessimistically, it clears the bar". Demotion should require evidence that it's bad;
   the lower bound says "even optimistically, it misses the bar". Using the upper bound for
   both demotes agents for having small samples.
2. With asymmetric costs the best threshold isn't 0.5 and the best model isn't the most
   accurate one. Lab 14 section 4 shows booking at P(bookable) = 0.80 costs more than not
   booking when a wrong booking costs five times a missed one.
3. An aggregate can rise while one segment gets worse (section 7). Each segment has its own
   error rate, volume and risk, so each needs its own evidence.
