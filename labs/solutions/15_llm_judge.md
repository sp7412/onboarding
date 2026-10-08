# Solution sketch: lab 15 · Building an LLM judge you can trust

## Graded exercise: rubric v3

Add one rule to v2 and pass the text to the same factory; both the live and the scripted
judge read it.

```python
from stlab.judge import RUBRICS, make_judge, judge_all, agreement, flip_rate

RUBRIC_V3 = RUBRICS["v2"] + """5. Not bookable: requests for electrical work (outlets, wiring,
   panels). The contractor does not offer electrical service.
"""
judge_v3 = make_judge(RUBRIC_V3)
v3 = judge_all(judge_v3, calls)
m3 = agreement(v3, gold)
print(m2["kappa"], "->", m3["kappa"], "| false bookable:", m2["false_bookable"], "->", m3["false_bookable"])
print("flip rate v2 -> v3:", flip_rate(v2, v3))
print({c["job_type"] for c, a, b in zip(calls, v2, v3) if a.verdict != b.verdict})
```

Offline, kappa rises from about 0.87 to about 0.95, false bookables fall from 18 to 3, and
every flipped verdict is an `electrical_issue` call (about 4% of calls). With a live model,
check the same three things; if anything other than electrical calls flipped, the new rule
changed the judge's behavior elsewhere, and that needs reading before you accept v3.

What a good answer also says:

- The rule names the fact the judge was missing (the business's service list), not the
  label you wanted it to produce.
- The labelled set is now the judge's regression test; v3 ships with its kappa, flip rate and
  version recorded next to every verdict it produces.
- Remaining errors are mostly low-confidence noise, which the abstention threshold from
  section 6 can route to people; rubric gaps were not.
