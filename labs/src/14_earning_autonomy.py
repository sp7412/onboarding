# %% [markdown]
# ## Running this lab in Google Colab
#
# Use the **Open in Colab** badge to run this notebook without setting up the repository locally.
# The setup cell below clones the public repo, installs the same requirements used by the
# local/Codespaces environment, and switches into `labs/`. Outside Colab it is a no-op.

# %%
import os
import subprocess
import sys

if "google.colab" in sys.modules:
    repo = "/content/onboarding"
    if not os.path.isdir(repo):
        subprocess.run(["git", "clone", "-q", "https://github.com/sp7412/onboarding.git", repo], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", os.path.join(repo, "requirements.txt")], check=True)
    os.chdir(os.path.join(repo, "labs"))
    print("Colab environment ready:", os.getcwd())
else:
    print("Local/Codespaces environment detected; use the normal repository setup.")

# %% [markdown]
# # 14 · Earning autonomy: when should an agent act alone?
#
# **Goal:** turn "the system earns trust" into an explicit, statistical policy for promoting,
# holding and demoting an agent, one segment at a time.
#
# At Pantheon 2026 ServiceTitan placed voice agents at level 2 of a five-level AI maturity
# model, and said some customers let the agent take every call with CSRs on standby (company
# claims; see [`docs/pantheon-2026-ai-roadmap.md`](../docs/pantheon-2026-ai-roadmap.md)). So
# autonomy is granted gradually. This lab asks what evidence should justify each step. The
# five level names below are our own teaching labels, not ServiceTitan's.
#
# You will:
# 1. measure each segment's real error rate from lab 13's decision pipeline
# 2. promote and demote with confidence bounds instead of point estimates
# 3. stop early with a sequential test
# 4. set a decision threshold from costs, not accuracy
# 5. check whether confidence means what it says (calibration)
# 6. pause autonomy when traffic shifts (PSI and OOD)
# 7. compare a naive promotion rule with the bounded one under a traffic shift
#
# Offline and deterministic. See also [`docs/earning-autonomy.md`](../docs/earning-autonomy.md).
#
# **Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

# %%
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from stlab.autonomy import (
    AUTONOMY_LEVELS, LEVEL_TARGETS, calibration, cost_threshold, drift_guard, expected_cost,
    hidden_regression_example, promotion_policy, segment_levels, sprt_stopping_n, wilson_interval,
)
from stlab.calls import load_calls
from stlab.minimax import FIELD_NAMES, decide_bookability, extract_call_facts, gold_action

calls = load_calls()
gold = {c["call_id"]: gold_action(c) for c in calls}
pd.DataFrame({"level": AUTONOMY_LEVELS,
              "error rate needed to reach the next level": list(LEVEL_TARGETS)})

# %% [markdown]
# ## 1. What counts as an error, per segment
#
# Run lab 13's pipeline with a mildly noisy extractor over every call, five times with
# different seeds. An **autonomous error** is a call the system *acted on* (book, transfer,
# decline, workflow) with the wrong action. A callback isn't an error: it's the system asking
# for help. That cost shows up as lower coverage instead.

# %%
rows = []
for seed in range(1, 6):
    for c in calls:
        action = decide_bookability(extract_call_facts(c, noise=0.04, seed=seed), c, 0.75).action
        rows.append({"trade": c["trade"], "acted": action != "callback",
                     "error": action != "callback" and action != gold[c["call_id"]]})
runs = pd.DataFrame(rows)
by_trade = runs[runs.acted].groupby("trade").error.agg(["sum", "count", "mean"])
by_trade["coverage"] = runs.groupby("trade").acted.mean()
by_trade["wilson_95"] = [tuple(round(x, 3) for x in wilson_interval(int(s), int(n)))
                         for s, n in zip(by_trade["sum"], by_trade["count"])]
TRUE_RATE = by_trade["mean"].round(4).to_dict()
by_trade

# %% [markdown]
# These rates become the "true" error rates for the simulation below. Notice the interval
# widths. With a few hundred decisions, plumbing and electrical each span about four
# percentage points, while HVAC's interval is much tighter. Smaller segments need longer to
# earn anything.

# %% [markdown]
# ## 2. Promote on the upper bound, demote on the lower bound
#
# - **Promote** when the *upper* 95% Wilson bound on the error rate is below the next level's
#   target, after a minimum sample.
# - **Demote** when the *lower* bound is above the target the current level was earned
#   against. That's evidence the agent is worse than required, not just a small sample.
# - Otherwise, **hold**. Evidence resets after every level change.

# %%
examples = [(0, 300, 0), (12, 300, 1), (8, 600, 2), (50, 600, 3), (3, 120, 2)]
table = []
for e, n, lvl in examples:
    d = promotion_policy(e, n, lvl)
    table.append({"errors": e, "n": n, "at level": lvl, "decision": d.decision, "new level": d.level,
                  "wilson 95%": f"[{d.lower_bound:.3f}, {d.upper_bound:.3f}]", "reason": d.reason})
pd.DataFrame(table)

# %% [markdown]
# Row 4 is a demotion: 50 errors in 600 at level 3 puts even the *lower* bound above the 5%
# this level was earned against. The last row is a hold, not a promotion. Three errors in 120
# looks like 2.5%, below the 5% target, but 120 samples can't rule out a much worse true rate.

# %% [markdown]
# ## 3. Stop early with a sequential test (SPRT)
#
# Waiting for a fixed 200 samples wastes time when the evidence is already decisive. Wald's
# SPRT tests "error rate is 2% (fine)" against "error rate is 5% (not fine)" after every
# decision. It stops as soon as the likelihood ratio crosses a boundary, with the false-promote
# and false-demote rates fixed in advance (α = 5%, β = 10%).

# %%
rng = np.random.default_rng(14)
sprt_rows = []
for true_rate in (0.005, 0.02, 0.05, 0.10):
    stops = [sprt_stopping_n(list((rng.random(2000) < true_rate).astype(int))) for _ in range(200)]
    sprt_rows.append({"true error rate": true_rate,
                      "promoted": np.mean([d == "promote" for d, _ in stops]),
                      "demoted": np.mean([d == "demote" for d, _ in stops]),
                      "median samples to decide": int(np.median([n for _, n in stops]))})
pd.DataFrame(sprt_rows)

# %% [markdown]
# Clearly good and clearly bad agents are decided quickly. Agents near the boundary take the
# longest, which is exactly where you want more evidence.

# %% [markdown]
# ## 4. Thresholds come from costs, not accuracy
#
# Booking a call that isn't bookable wastes a truck roll and trust (say $1,500). Failing to
# book a bookable call loses a job (say $300). Book only when P(bookable) clears the
# break-even point.

# %%
threshold = cost_threshold(wrong_book_cost=1500, missed_book_cost=300)
print(f"book only when P(bookable) >= {threshold:.3f}")
pd.DataFrame([{"P(bookable)": p, **dict(zip(("cost if we book", "cost if we don't"),
                                             (round(x) for x in expected_cost(p, 1500, 300))))}
              for p in (0.50, 0.80, 0.83, 0.90, 0.98)])

# %% [markdown]
# ## 5. Does confidence mean what it says?
#
# Use the lab 13 extractor's own confidences. For each field it reports, was the value right?
# A well-calibrated extractor is right about 90% of the time when it says 0.9.

# %%
probs, correct = [], []
for c in calls:
    facts = extract_call_facts(c, noise=0.12, seed=7)
    for key in FIELD_NAMES:
        probs.append(facts.fields[key].confidence)
        correct.append(int(facts.fields[key].value == c[key]))
bins, ece = calibration(probs, correct)
cal = pd.DataFrame(bins, columns=["mean confidence", "observed accuracy", "n"])
print(f"expected calibration error: {ece:.3f}")
cal

# %%
fig, ax = plt.subplots(figsize=(5, 5))
ax.plot([0, 1], [0, 1], linestyle="--", color="grey", label="perfect calibration")
ax.scatter(cal["mean confidence"], cal["observed accuracy"], s=np.sqrt(cal["n"]) * 12)
ax.set_xlabel("Mean confidence")
ax.set_ylabel("Observed accuracy")
ax.set_title("Reliability diagram (lab 13 extractor)")
ax.legend()
plt.show()

# %% [markdown]
# Low-confidence bins are *overconfident*: values the extractor rates 0.6 are right far less
# than 60% of the time. That's why a promotion policy uses observed outcomes, not the agent's
# self-reported confidence.

# %% [markdown]
# ## 6. Pause when the traffic changes
#
# A policy validated on last month's traffic may not hold after a heat wave or a new service
# launch. The drift guard combines a **PSI** on the call-type mix with an **OOD rate**: the
# share of calls whose features fall beyond the 99th percentile of the validation data.

# %%
feat_rng = np.random.default_rng(7)
train = feat_rng.normal(0, 1, size=(600, 4))          # e.g. turns, words, after-hours, channel
normal_week = feat_rng.normal(0, 1, size=(300, 4))
launch_week = feat_rng.normal(1.2, 1.3, size=(300, 4))
base_mix = [0.55, 0.25, 0.12, 0.08]                    # routine, no-cool, price, hard calls
pd.DataFrame({
    "normal week": drift_guard(base_mix, [0.56, 0.24, 0.12, 0.08], train, normal_week),
    "new-service launch": drift_guard(base_mix, [0.30, 0.15, 0.20, 0.35], train, launch_week),
})

# %% [markdown]
# ## 7. Aggregates hide weak segments
#
# Here the aggregate improves while the hard segment gets worse, because the mix shifted toward
# easy calls. Grant autonomy per segment.

# %%
pd.DataFrame(hidden_regression_example())

# %%
pd.DataFrame({name: d.__dict__ for name, d in segment_levels(
    {"HVAC": (6, 900), "plumbing": (9, 300), "electrical": (2, 60)},
    levels={"HVAC": 2, "plumbing": 2, "electrical": 2}).items()}).T

# %% [markdown]
# ## 8. Naive vs. bounded promotion under a traffic shift
#
# Simulate 12 weeks. Weekly decision volumes per segment are scaled up to a multi-contractor
# view, and errors are drawn at the segment rates measured in section 1. In week 8 plumbing
# launches in a new area: its error rate triples and its traffic mix shifts.
#
# - **Naive:** jump to level 3 ("act autonomously") once a week's observed error rate is
#   under 5%. Never look back.
# - **Bounded:** one level at a time with `promotion_policy` on evidence gathered at the
#   current level, plus a weekly drift guard. When it fires, drop one level, reset the
#   evidence, and re-baseline the guard on the new traffic. From then on the agent has to
#   re-earn trust at the new error rate.
#
# An **incident** is an autonomous error made at level 3 or higher, where no person reviews
# the action.

# %%
VOLUME = {"HVAC": 1500, "plumbing": 400, "electrical": 150}
sim = random.Random(2026)
naive = {s: 0 for s in VOLUME}
bounded = {s: 0 for s in VOLUME}
evidence = {s: [0, 0] for s in VOLUME}           # errors, n at the current bounded level
baseline = {s: (base_mix, train) for s in VOLUME}  # what the drift guard compares against
incidents = {"naive": 0, "bounded": 0}
history = []
for week in range(1, 13):
    for seg, volume in VOLUME.items():
        launched = seg == "plumbing" and week >= 8
        rate = TRUE_RATE[seg] * (3 if launched else 1)
        errors = sum(sim.random() < rate for _ in range(volume))
        if naive[seg] < 3 and errors / volume < 0.05:
            naive[seg] = 3
        incidents["naive"] += errors if naive[seg] >= 3 else 0
        incidents["bounded"] += errors if bounded[seg] >= 3 else 0
        mix_now = [0.30, 0.15, 0.20, 0.35] if launched else base_mix
        features_now = launch_week if launched else normal_week
        guard = drift_guard(*baseline[seg][:1], mix_now, baseline[seg][1], features_now)
        if guard["pause"]:
            bounded[seg] = max(0, bounded[seg] - 1)
            evidence[seg] = [0, 0]
            baseline[seg] = (mix_now, features_now)          # re-validated on the new traffic
            decision = "pause: " + guard["reason"]
        else:
            evidence[seg][0] += errors
            evidence[seg][1] += volume
            d = promotion_policy(*evidence[seg], bounded[seg])
            decision = d.decision
            if d.level != bounded[seg]:
                bounded[seg], evidence[seg] = d.level, [0, 0]
        history.append({"week": week, "segment": seg, "observed_error": round(errors / volume, 4),
                        "naive_level": naive[seg], "bounded_level": bounded[seg],
                        "bounded_decision": decision})
hist = pd.DataFrame(history)
hist.pivot(index="week", columns="segment", values="bounded_level")

# %%
fig, axes = plt.subplots(1, 3, figsize=(12, 3), sharey=True)
for ax, seg in zip(axes, VOLUME):
    h = hist[hist.segment == seg]
    ax.step(h.week, h.naive_level, where="post", label="naive", linestyle="--")
    ax.step(h.week, h.bounded_level, where="post", label="bounded")
    ax.axvline(8, color="grey", linewidth=0.8)
    ax.set_title(seg)
    ax.set_xlabel("week")
axes[0].set_ylabel("autonomy level")
axes[0].legend()
plt.tight_layout()
plt.show()
print(incidents, "(synthetic; autonomous errors at level >= 3)")
print(f"bounded policy: {1 - incidents['bounded'] / incidents['naive']:.0%} fewer unreviewed errors")

# %% [markdown]
# The naive rule reaches "act autonomously" after the first week under 5%, and keeps acting
# alone after the plumbing launch. The bounded rule climbs one level at a time, makes the small
# electrical segment wait the longest for enough evidence, and backs plumbing off as soon as
# the drift guard fires. Plumbing can't climb back, because its new error rate doesn't clear
# the bar. The price of that caution is slower automation; the benefit is fewer unreviewed
# mistakes, printed above. Errors at level 3 still happen under both rules, because "act
# autonomously within limits" accepts a small error rate by design.

# %% [markdown]
# ## Exercises
#
# 1. Write a promotion policy for a new segment, "external AI assistant bookings" (lab 12):
#    the error definition, target per level, minimum n, confidence level, cost ratio and drift
#    signals.
# 2. Explain to a non-technical manager, in three sentences, why the agent isn't fully
#    autonomous yet in plumbing.
# 3. Sketch the dashboard a team would watch: outcome, safety, evidence (n and bounds),
#    calibration, drift, segments, and the promotion log.
#
# ## Check your understanding
#
# 1. Why promote on the upper confidence bound but demote on the lower one?
# 2. Why can accuracy be the wrong objective when false bookings and missed bookings cost different amounts?
# 3. Why should autonomy be granted per segment instead of from one aggregate score?
#
# **Graded exercise:** the simulation re-baselines the drift guard the moment it fires. Make it
# stricter: after a pause, hold the segment at its lower level and count no evidence until a
# person approves the new baseline *and* two consecutive weeks are stable. Show that plumbing
# never regains level 3 before week 12, and that HVAC and electrical are never paused. See
# [`solutions/14_earning_autonomy.md`](../solutions/14_earning_autonomy.md).
