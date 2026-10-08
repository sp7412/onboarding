# %% [markdown]
# # 11 · The learning loop: tying outcomes back to decisions
#
# **Goal:** make a multi-agent system get better from its own results. Every decision is
# logged with what the agent *knew at the time*, its prediction and its action; when the job
# closes, the outcome is attached. Then you measure and recalibrate two things: the value
# assumptions behind lead scoring, and how far to trust the voice agent's extracted facts.
#
# You will:
# 1. log 400 fictional decisions with ledger snapshots
# 2. attach outcomes and measure prediction error
# 3. estimate what each signal is *really* worth and update the assumptions with shrinkage
# 4. check the improvement on jobs the update never saw
# 5. calibrate the voice agent's confidence, and pick a verification threshold from data
# 6. see how reading today's facts instead of the decision-time snapshot fools you
#
# Leadership described this loop publicly at Pantheon 2026 ("every outcome is tied back to the
# decisions that produced it"). This lab is a generic teaching model. Data is synthetic. Offline.

# %%
from statistics import mean
from stlab.context import ContextLedger
from stlab.coordination import SIGNAL_UPLIFT, lead_score
from stlab.learning import (DecisionLog, DecisionRecord, calibration_table, mean_abs_error,
                            fit_uplifts, shrink, synthetic_jobs)

jobs = synthetic_jobs(n=400, seed=11)
print(len(jobs), "fictional jobs. Example:", jobs[3])
print("Prior assumptions (what lead scoring believes):", SIGNAL_UPLIFT)

# %% [markdown]
# ## 1. Log every decision with a snapshot
#
# For each call, the voice agent proposes `job_type` with a confidence; the control plane
# verifies it at confidence ≥ 0.85. Lead scoring predicts the job's value from the verified
# job type and signals. The decision record stores exactly those inputs, so later we can ask
# "was the decision right *given what we knew*?"

# %%
ledger = ContextLedger()
log = DecisionLog()

def decide(job, uplift, threshold=0.85):
    ledger.propose("voice_agent", job["job_id"], "job_type", job["heard_job_type"], job["confidence"],
                   evidence="(transcript span)")
    if job["confidence"] >= threshold:
        ledger.verify(job["job_id"], "job_type", evidence="confidence threshold")
    jt = ledger.view(job["job_id"]).get("job_type", "unknown")
    pred = lead_score(jt, job["signals"], uplift)
    return DecisionRecord(f"D-{job['job_id']}", job["job_id"], ledger.clock,
                          {"job_type": jt, "signals": list(job["signals"])}, pred, "book")

for job in jobs:
    log.record(decide(job, SIGNAL_UPLIFT))
print(len(log.records), "decisions logged. First:", next(iter(log.records.values())))

# %% [markdown]
# ## 2. Attach outcomes

# %%
for job in jobs:
    log.attach_outcome(job["job_id"], job["actual_value"])
closed = log.closed()
learn, test = closed[:200], closed[200:]
print(f"closed: {len(closed)}  |  mean absolute error of lead scoring: ${mean_abs_error(closed):,.0f}")

# %% [markdown]
# ## 3. What is each signal really worth?
#
# Estimate every signal's value at once with least squares, controlling for job type and the
# other signals. (Simply comparing averages "with vs. without" a signal is biased here: a call
# that mentions `system_down` sometimes also mentions a replacement, and the replacement's
# value would be credited to `system_down`.) Then update each assumption with **shrinkage**: with `n` observations the evidence gets weight `n / (n + k)`,
# so a handful of unusual jobs can't swing a number that drives every decision.

# %%
# Closed jobs reveal the true job type; use it for the comparison so mislabeled calls
# don't masquerade as signal effects.
TRUE_TYPE = {j["job_id"]: j["job_type"] for j in jobs}
def with_true_type(records):
    return [DecisionRecord(r.decision_id, r.job_id, r.at, {**r.inputs, "job_type": TRUE_TYPE[r.job_id]},
                           r.prediction, r.action, r.outcome) for r in records]

updated = dict(SIGNAL_UPLIFT)
print(f"{'signal':22} {'prior':>7} {'observed':>9} {'n':>4} {'updated':>8}")
estimates = fit_uplifts(with_true_type(learn), list(SIGNAL_UPLIFT))
for sig, prior in SIGNAL_UPLIFT.items():
    obs, n = estimates[sig]
    updated[sig] = round(shrink(prior, obs, n, k=20))
    print(f"{sig:22} {prior:7.0f} {obs:9.0f} {n:4d} {updated[sig]:8.0f}")

# %% [markdown]
# All three assumptions were off: `system_down` was assumed to add $300 and adds far less,
# `replacement_interest` adds more than assumed, and `same_day_needed` adds roughly nothing.
# None of this was visible until outcomes were tied back to the decision inputs.
#
# ## 4. Did it help? Check on jobs the update never saw

# %%
def rescore(records, uplift):
    return [DecisionRecord(r.decision_id, r.job_id, r.at, r.inputs,
                           lead_score(r.inputs["job_type"], r.inputs["signals"], uplift),
                           r.action, r.outcome) for r in records]

before, after = mean_abs_error(rescore(test, SIGNAL_UPLIFT)), mean_abs_error(rescore(test, updated))
print(f"held-out error with prior assumptions:   ${before:,.0f}")
print(f"held-out error with updated assumptions: ${after:,.0f}   ({(before - after) / before:.0%} better)")

# %% [markdown]
# Always measure the update on data it didn't learn from. Improvement on the training half
# alone proves little.
#
# ## 5. How much should we trust the voice agent?
#
# Each closed job reveals the true job type. Compare it with what the voice agent heard, by
# the confidence it reported. A well-calibrated agent is right about 90% of the time when it
# says 0.9.

# %%
pairs = [(j["confidence"], j["heard_job_type"] == j["job_type"]) for j in jobs]
for row in calibration_table(pairs):
    print(row)

def precision_at(threshold):
    kept = [ok for c, ok in pairs if c >= threshold]
    return (sum(kept) / len(kept) if kept else 0.0), len(kept)

print()
for t in (0.80, 0.85, 0.90):
    p, n = precision_at(t)
    print(f"verify at >= {t:.2f}: precision {p:.0%} on {n} facts")

# %% [markdown]
# The agent is **overconfident** in the 0.8–0.9 band: facts it rates there are right far less often
# than that. The data says: to verify `job_type` automatically with at least ~90% precision,
# the threshold should be 0.9, not 0.85. Facts below it should be confirmed with the caller
# ("Just to confirm, the AC isn't cooling at all?"), not trusted silently.
#
# ## 6. The hindsight trap
#
# Suppose a job type is corrected after the decision (the technician finds it was a tune-up).
# If you evaluate the decision using *today's* facts, it looks like the agent knew the right
# answer and still predicted badly. Read the ledger **as of the decision**.

# %%
j = jobs[0]
JID = j["job_id"]
decision = log.records[f"D-{JID}"]
ledger.retract(JID, "job_type", reason="technician corrected job type on site")
ledger.propose("control_plane", JID, "job_type", "tune_up", 1.0, evidence="technician note")
ledger.verify(JID, "job_type", evidence="technician note")
print("facts as of the decision :", ledger.view(JID, as_of=decision.at))
print("facts today              :", ledger.view(JID))

# %% [markdown]
# Evaluating with today's view would blame the decision for information it never had, or
# credit it with knowledge it didn't have. The decision record and `as_of` reads keep the
# learning loop honest.
#
# ## Self-check

# %%
assert after < before, "updated assumptions must reduce held-out error"
assert updated["system_down"] < SIGNAL_UPLIFT["system_down"]
assert updated["replacement_interest"] > SIGNAL_UPLIFT["replacement_interest"]
assert precision_at(0.90)[0] >= 0.9 > precision_at(0.80)[0]
assert ledger.view(JID, as_of=decision.at)["job_type"] == decision.inputs["job_type"]
print("All checks passed.")

# %% [markdown]
# ## Where the loop stops
#
# - Outcomes are noisy and delayed (a replacement can close weeks later). Shrinkage and holdout
#   checks keep you from chasing noise; they don't remove the delay.
# - Observed differences aren't causal proof. A signal can correlate with value because of who
#   calls, not because of the signal. Experiments or careful adjustment are the next step.
# - The loop changes behavior automatically, so it needs the same guardrails as any agent:
#   limits on how fast assumptions move, review of large changes, and a rollback path.
#
# ## Exercises
#
# 1. Try `k=0` and `k=200` in `shrink`. What goes wrong at each extreme?
# 2. Recalibrate confidence per job type instead of globally. Does the threshold differ?
# 3. Add a weekly drift check that alerts when held-out error rises by more than 15%.

# %% [markdown]
# ## Check your understanding
#
# 1. Why must the decision record store the inputs *as of* the decision?
# 2. Why shrink the update toward the prior instead of using the observed value directly?
# 3. What does a calibration table tell you that overall accuracy doesn't?
#
# **Graded exercise:** split the 400 jobs into four weekly batches of 100, update the
# assumptions after each batch, and assert that the change applied to any single assumption in
# one week never exceeds a cap you choose (for example $250), even if the evidence says more.
# See [`solutions/11_learning_loop.md`](../solutions/11_learning_loop.md).
