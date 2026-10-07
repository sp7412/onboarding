# %% [markdown]
# # 14 · Earning autonomy: when should an agent act alone?
#
# **Goal:** turn "trust" into an explicit statistical policy. Promotion requires evidence,
# not a model's self-reported confidence, and autonomy can be different for different segments.
#
# These five level names are original teaching labels inspired by, but not copied from, the
# public Pantheon description.
#
# **Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stlab.calls import load_calls
from stlab.autonomy import (
    AUTONOMY_LEVELS, LEVEL_TARGETS, promotion_policy, cost_threshold,
    expected_cost, calibration, drift_guard, segment_levels, simpsons_paradox,
)

calls = load_calls()
print("Autonomy levels:")
for i, (name, target) in enumerate(zip(AUTONOMY_LEVELS, LEVEL_TARGETS)):
    print(i, name, "target error <", target)

# %% [markdown]
# ## 1. Promotion policy
#
# The promotion rule uses a Wilson upper confidence bound. A point estimate below a target is
# not enough: the upper bound must clear the target after the minimum sample size is reached.

# %%
examples = [
    {"errors": 2, "n": 500, "level": 0},
    {"errors": 6, "n": 500, "level": 1},
    {"errors": 4, "n": 500, "level": 2},
    {"errors": 3, "n": 500, "level": 3},
]
display(pd.DataFrame([promotion_policy(x["errors"], x["n"], x["level"]).__dict__ for x in examples]))

# %% [markdown]
# ## 2. Simulate weeks of traffic
#
# We use the shared call population repeatedly, but inject deterministic segment-specific
# error rates. This keeps the exercise reproducible while showing why aggregate metrics are insufficient.

# %%
def synthetic_week(week, records):
    rows = []
    for i, r in enumerate(records):
        base = {"HVAC": 0.012, "plumbing": 0.028, "electrical": 0.045}[r["trade"]]
        if r["emergency"]:
            base += 0.025
        if r["after_hours"]:
            base += 0.008
        error = ((i * 17 + week * 29) % 1000) / 1000 < base
        rows.append({
            "week": week, "trade": r["trade"], "after_hours": r["after_hours"],
            "emergency": r["emergency"], "error": int(error),
        })
    return pd.DataFrame(rows)

weekly = pd.concat([synthetic_week(w, calls) for w in range(1, 7)], ignore_index=True)
display(weekly.groupby(["week", "trade"]).error.mean().unstack().round(3))

# %%
levels = {"HVAC": 0, "plumbing": 0, "electrical": 0}
history = []
for week in range(1, 7):
    current = weekly[weekly.week == week]
    for trade in levels:
        x = current[current.trade == trade]
        decision = promotion_policy(int(x.error.sum()), len(x), levels[trade], min_samples=100)
        levels[trade] = decision.level
        history.append({"week": week, "trade": trade, "level": decision.level,
                        "decision": decision.decision, "upper_bound": decision.upper_bound})
history_df = pd.DataFrame(history)
display(history_df)

# %% [markdown]
# ## 3. Cost asymmetry
#
# A wrong "booked" claim can create a wasted truck roll and damage trust. A wrong "not
# bookable" decision can lose revenue. The threshold should therefore come from expected cost,
# not accuracy alone.

# %%
threshold = cost_threshold(wrong_book_cost=1500, missed_book_cost=300)
print("P(bookable) threshold:", round(threshold, 3))
for p in (0.50, 0.80, 0.90, 0.98):
    book_cost, decline_cost = expected_cost(p, 1500, 300)
    print(p, "book cost", round(book_cost), "decline cost", round(decline_cost))

# %% [markdown]
# ## 4. Calibration
#
# An overconfident model can have a beautiful confidence histogram and still be unsafe.
# Calibration asks whether a group assigned probability p is actually correct about p of the time.

# %%
probs = [min(0.99, 0.55 + ((i * 7) % 40) / 100) for i in range(200)]
outcomes = [int(((i * 13 + 7) % 100) / 100 < (p * 0.86)) for i, p in enumerate(probs)]
bins, ece = calibration(probs, outcomes)
cal = pd.DataFrame(bins, columns=["mean_confidence", "empirical_rate", "n"])
display(cal)
print("ECE:", round(ece, 3))

# %%
fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1], linestyle="--", label="perfect calibration")
ax.scatter(cal["mean_confidence"], cal["empirical_rate"], s=cal["n"] * 3)
ax.set_xlabel("Mean confidence")
ax.set_ylabel("Empirical success rate")
ax.set_title("Reliability diagram")
ax.legend()
ax.grid(True)
plt.show()

# %% [markdown]
# ## 5. Drift and OOD
#
# The same error rate can mean something different after a heat wave or a new trade launch.
# Combine a population-shift statistic with a simple multivariate OOD score.

# %%
rng = np.random.default_rng(7)
train = rng.normal(0, 1, size=(200, 4))
stable = rng.normal(0, 1, size=(50, 4))
shifted = rng.normal(2.5, 1, size=(50, 4))
expected_mix = [0.70, 0.20, 0.08, 0.02]
stable_mix = [0.69, 0.21, 0.08, 0.02]
shifted_mix = [0.45, 0.25, 0.20, 0.10]
print("stable:", drift_guard(expected_mix, stable_mix, train, stable))
print("shifted:", drift_guard(expected_mix, shifted_mix, train, shifted))

# %% [markdown]
# ## 6. Segment-specific autonomy
#
# Aggregate metrics can hide a weak segment. A classic Simpson's-paradox-style situation can
# occur when the traffic mix changes at the same time as segment performance changes.

# %%
print(simpsons_paradox())
segment = {"HVAC": (4, 500), "plumbing": (12, 500), "electrical": (28, 500)}
display(pd.DataFrame([d.__dict__ | {"segment": name}
                      for name, d in segment_levels(segment).items()]))

# %% [markdown]
# ## 7. Naive promotion vs. bounded, cost-aware promotion
#
# Naive rule: promote when observed accuracy exceeds 95%.
#
# Bounded rule: use a confidence bound, minimum sample size, asymmetric cost, and drift/OOD
# guard. For the synthetic comparison, an "incident" is a wrong autonomous action.

# %%
naive_incidents = 0
bounded_incidents = 0
for _, row in weekly.iterrows():
    if row["error"] and row["week"] >= 2:
        naive_incidents += 1
    if row["error"] and row["week"] >= 5:
        bounded_incidents += 1
print({
    "naive_accuracy_threshold_incidents": naive_incidents,
    "bounded_policy_incidents": bounded_incidents,
})
print("These counts are illustrative simulation outputs, not production estimates.")

# %% [markdown]
# ## Exercises
#
# 1. Write a promotion policy for a new segment. State the target error, minimum n, confidence
#    level, cost asymmetry, and drift guard.
# 2. Explain to a non-technical manager in three sentences why the agent is not fully
#    autonomous yet.
# 3. Design the dashboard a team should watch: include outcome, safety, calibration, drift,
#    segment cuts, and promotion state.
# 4. Replace the naive incident counter with a true decision-by-decision comparison using
#    the bookability agent from lab 13.

# %% [markdown]
# ## Check your understanding
#
# 1. Why does a confidence bound matter when promoting an agent?
# 2. Why can accuracy be the wrong objective when the costs of false booking and missed booking differ?
# 3. Why should autonomy be segmented instead of granted from one aggregate score?
#
# **Graded exercise:** implement an automatic demotion rule that fires when PSI or the OOD
# score crosses its limit, then prove it with a synthetic drift test. See solutions/14.md.
