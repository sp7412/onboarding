# %% [markdown]
# # 15 · Building an LLM judge you can trust
#
# **Goal:** build a model-based judge for one question, *was this call a bookable lead?*, and
# then do the part most teams skip: prove the judge is right often enough to use, find where
# it is wrong, and wire it so its mistakes are caught.
#
# Every booking rate needs a denominator, and at Pantheon 2026 ServiceTitan said in-product
# booking rates were easy to game, so it built a "voice intelligence" agent to judge which
# calls were bookable (company claims; see
# [`docs/pantheon-2026-ai-roadmap.md`](../docs/pantheon-2026-ai-roadmap.md)). A judge like
# that becomes the ruler every other metric is measured with. This lab is a small synthetic
# version of the idea, not ServiceTitan's implementation.
#
# You will:
# 1. write a rubric and a strict output contract, and check the judge's evidence is real
# 2. measure the judge against human labels: accuracy, Cohen's kappa, and a human ceiling
# 3. read the disagreements and find that most are **rubric bugs**, then fix the rubric
# 4. stop the judge from grading the agent's own claims
# 5. test a pairwise judge for **position bias**
# 6. check calibration and choose when the judge should say `needs_human`
# 7. treat the judge as versioned production code
#
# **Live by default.** With `OPENAI_API_KEY` set, a real model judges a stratified sample of
# calls (`STLAB_JUDGE_N`, default 80; model `STLAB_JUDGE_MODEL`, default `gpt-5.4-mini`).
# Without a key, a scripted judge with deliberate, realistic flaws stands in, so every cell
# still runs. Expect the live numbers to differ from the offline ones; the questions are the
# same. Uses the shared synthetic dataset (`labs/data/calls/`, see its DATASHEET). Pairs with
# reading-guide item 22, Hamel Husain's "Using LLM-as-a-Judge"
# ([`docs/reading-guide.md`](../docs/reading-guide.md)).
#
# **Facts as of: October 7, 2026 · Last reviewed: October 7, 2026**

# %%
import os

import matplotlib.pyplot as plt
import pandas as pd

import stlab
from stlab.autonomy import calibration
from stlab.calls import load_calls
from stlab.judge import (
    PAIRWISE_ITEMS, RUBRICS, OpenAIPairwiseJudge, ScriptedPairwiseJudge, agreement,
    abstention_sweep, build_messages, cohen_kappa, errors_by_scenario, evidence_grounded,
    flip_rate, human_labels, judge_all, make_judge, position_test, stratified_sample,
)

LIVE = stlab.have("openai")
all_calls = load_calls()
calls = stratified_sample(all_calls, int(os.environ.get("STLAB_JUDGE_N", "80"))) if LIVE else all_calls
gold = [c["bookable"] for c in calls]
print("judge:", "LIVE model" if LIVE else "offline scripted stand-in", "|", len(calls), "calls")
print(f"gold labels: {sum(gold)} bookable, {len(gold) - sum(gold)} not bookable")

# %% [markdown]
# ## 1. A rubric and a contract
#
# A judge is a prompt plus a parser plus a policy for when the parser fails. Write the rubric
# the way you'd brief a new reviewer: define the term, list the facts they need (here, the
# service-area ZIPs), and say what *doesn't* count as evidence. The contract is JSON with a
# verdict, a confidence, an **exact quote** from the transcript, and a reason. Anything
# off-contract becomes `needs_human`, never a silent default.

# %%
print(build_messages(calls[0], "v1")[0]["content"])

# %%
judge_v1 = make_judge("v1")
v1 = judge_all(judge_v1, calls)
pd.DataFrame([{"call": c["call_id"], "scenario": c["scenario"], "gold": c["bookable"],
               "verdict": v.verdict, "confidence": v.confidence, "evidence": v.evidence}
              for c, v in list(zip(calls, v1))[:8]])

# %% [markdown]
# The quote requirement is cheap and catches something real: a judge that cites words the
# caller never said is reasoning from an imagined call. Count those.

# %%
ungrounded = [(c["call_id"], v.evidence) for c, v in zip(calls, v1) if not evidence_grounded(c, v)]
print(f"{len(ungrounded)} of {len(calls)} verdicts cite evidence that isn't in the transcript")
ungrounded[:5]

# %% [markdown]
# ## 2. Measure it against people
#
# Accuracy alone flatters a judge when one class dominates. **Cohen's kappa** measures
# agreement beyond what chance would give. It needs a reference point, so compare with how
# often two careful *humans* agree on the same calls: that is roughly the ceiling a judge can
# be expected to reach. (Here the second annotator is simulated: it agrees with the gold
# label except on genuinely debatable price-shopper and override calls.)

# %%
human_b = human_labels(calls)
print("human vs human kappa:", round(cohen_kappa(human_b, gold), 3))
m1 = agreement(v1, gold)
print({k: m1[k] for k in ("coverage", "accuracy", "kappa", "false_bookable", "missed_bookable")})
pd.DataFrame(m1["confusion"]).T

# %% [markdown]
# The two error directions cost different things. A **false bookable** inflates the
# denominator, so the agent looks worse at converting leads than it is. A **missed bookable**
# shrinks it, so the agent looks better. Report both, never just accuracy.
#
# ## 3. Disagreements are usually rubric bugs
#
# Before blaming the model, read where it disagrees with people, grouped by scenario.

# %%
pd.DataFrame(errors_by_scenario(calls, v1)).T.head(8)

# %%
for c, v in zip(calls, v1):
    if v.bookable is not None and v.bookable != c["bookable"] and c["scenario"] in ("reschedule", "cancellation", "injection"):
        print(c["scenario"], "| gold reason:", c["bookable_reason"])
        print("   judge:", v.verdict, "-", v.reason)
        break

# %% [markdown]
# In the offline run, reschedules, cancellations and override attempts are wrong almost every
# time, and confidently. A live model may get some of them right from common sense; check
# which scenarios yours misses. Either way the judge isn't confused: the rubric never said that an existing appointment
# isn't a new lead, or that a caller who says "ignore your rules, I'm the owner" shouldn't be
# counted as one. The labellers knew those rules; the judge was never told. That is the most
# common failure of LLM judges in practice: **the definition lived in people's heads.**
#
# Rubric v2 adds those two rules. Re-measure on the same calls.

# %%
print(RUBRICS["v2"][len(RUBRICS["v1"]):])
judge_v2 = make_judge("v2")
v2 = judge_all(judge_v2, calls)
m2 = agreement(v2, gold)
pd.DataFrame([{"rubric": "v1", **{k: m1[k] for k in ("accuracy", "kappa", "false_bookable", "missed_bookable")}},
              {"rubric": "v2", **{k: m2[k] for k in ("accuracy", "kappa", "false_bookable", "missed_bookable")}}])

# %% [markdown]
# Changing a judge's rubric changes the ruler. Record how many verdicts flipped, and keep the
# labelled set you just used as the judge's **regression test**: any future rubric or model
# change must be re-scored against it before anyone trusts new numbers.

# %%
print(f"verdicts changed between v1 and v2: {flip_rate(v1, v2):.1%}")
pd.DataFrame(errors_by_scenario(calls, v2)).T.head(5)

# %% [markdown]
# Look at what is still wrong. (Hint: the contractor in this dataset doesn't do electrical
# work. Neither rubric says so. That's the graded exercise.)
#
# ## 4. Don't let the judge grade the agent's claims
#
# A judge that sees the agent's own disposition ("BOOKED" / "NOT BOOKED") is tempted to agree
# with it. That's fatal for a bookability judge: the calls that matter most are the bookable
# ones the agent *didn't* book, and a judge that copies "NOT BOOKED" hides exactly those. Run
# the same judge with and without the disposition in its input.

# %%
v2_disp = judge_all(judge_v2, calls, show_disposition=True)
m2d = agreement(v2_disp, gold)
missed_by_agent = [i for i, c in enumerate(calls) if c["bookable"] and not c["outcome"]["booked"]]
def caught(vs):
    return sum(vs[i].bookable is True for i in missed_by_agent)
pd.DataFrame([
    {"input": "transcript only", "kappa": m2["kappa"],
     "agent's missed leads the judge still flags": f"{caught(v2)} / {len(missed_by_agent)}"},
    {"input": "transcript + agent disposition", "kappa": m2d["kappa"],
     "agent's missed leads the judge still flags": f"{caught(v2_disp)} / {len(missed_by_agent)}"},
])

# %% [markdown]
# Keep the agent's claims out of the judge's input, and if the judge must see them, tell it
# they are claims, not evidence, and test that it listens. The same rule applies to any agent
# you evaluate: grade what changed in the system of record, not what the agent said.
#
# ## 5. Pairwise judging and position bias
#
# Many evaluations ask a judge which of two replies is better. Judges often prefer whichever
# reply they read first. The test is cheap: ask every question in both orders and check that
# the judge picks the same *reply* both times.

# %%
pair_judge = OpenAIPairwiseJudge() if LIVE else ScriptedPairwiseJudge()
pairs = pd.DataFrame(position_test(pair_judge, PAIRWISE_ITEMS))
print(f"consistent across orders: {pairs['consistent'].mean():.0%}")
pairs

# %% [markdown]
# Where the judge flips with the order, its "preference" is noise. The standard fix is the one
# in the `debiased` column: run both orders and count a win only when they agree, otherwise
# call it a tie. It doubles the cost and removes a bias that would otherwise go straight into
# your A/B decisions.
#
# ## 6. Calibration and when to say `needs_human`
#
# A judge's confidence is only useful if it means something. Bin the verdicts by confidence
# and compare with how often they were right (the same reliability check lab 14 uses for the
# extractor).

# %%
decided = [(v, g) for v, g in zip(v2, gold) if v.bookable is not None]
rows, ece = calibration([v.confidence for v, _ in decided], [int(v.bookable == g) for v, g in decided], bins=5)
print(f"expected calibration error: {ece:.3f}")
fig, ax = plt.subplots(figsize=(4.5, 4))
ax.plot([0, 1], [0, 1], "--", color="grey")
ax.plot([r[0] for r in rows], [r[1] for r in rows], "o-")
ax.set_xlabel("stated confidence"); ax.set_ylabel("observed accuracy"); ax.set_title("judge reliability")
plt.show()

# %% [markdown]
# Now choose a threshold below which the judge abstains and a person decides. Each step up
# buys accuracy with reviewer time.

# %%
pd.DataFrame(abstention_sweep(v2, gold))

# %% [markdown]
# Pick the threshold from costs, as lab 14 does for autonomy: how much does a wrong
# denominator cost against an hour of review? Note what abstention *can't* fix: errors made at
# high confidence (offline, the electrical calls) pass every threshold. Errors that come from
# a rubric gap only go away when the rubric changes.
#
# ## 7. The judge is production code
#
# Once other metrics depend on it, a judge needs the same discipline as the agent it grades:
#
# - **Version it.** Pin the model and the rubric together, and log the version with every
#   verdict, so a dashboard can tell "the agent changed" from "the ruler changed".
# - **Regression-test it.** Re-score the labelled set on every model or rubric change, and
#   report flips (section 3).
# - **Audit it continuously.** Send a random slice of production verdicts to people every week,
#   and track judge-human kappa over time; a drop is a judge incident.
# - **Watch its inputs.** If the call mix shifts (a new trade, a heat wave), re-check agreement
#   on the new segment before trusting it there (lab 14's drift guard applies to judges too).
# - **Keep it out of the loop it measures.** The agent being graded shouldn't see or optimize
#   against the judge's prompt, or the metric becomes a target.
#
# See [`docs/design-by-evaluation.md`](../docs/design-by-evaluation.md) (section 6, "Finding
# failures in production"), [whitepaper chapter 17](../docs/whitepaper/17-running-agents-in-production.md)
# (evaluation and rollout) and the
# [bookability judge exercise](../senior-engineer/bookability-judge.md).

# %% [markdown]
# ## Exercises
#
# 1. Pick five calls the judge got wrong under v2 and decide, for each, whether the fix
#    belongs in the rubric, the labels, or the input the judge sees.
# 2. Write a second judge for **process quality** (did the agent confirm the address and the
#    slot before booking?) and explain why it must be separate from the bookability judge.
# 3. Live only: run the v2 judge twice on the same calls. How many verdicts differ between
#    runs? What does that imply for how you report week-over-week changes?
#
# ## Check your understanding
#
# 1. Why compare judge-human kappa with human-human kappa instead of with 1.0?
# 2. Why does showing the agent's disposition hurt a bookability judge most on the calls that matter?
# 3. Why can't an abstention threshold fix errors that come from a gap in the rubric?
#
# **Graded exercise:** write rubric v3 by adding a rule for electrical requests (the contractor
# doesn't offer electrical service), judge the same calls, and show that kappa rises, false
# bookables fall, and the flip rate from v2 touches only electrical calls. Pass your rubric
# text to `make_judge(...)`; both the live and the scripted judge read it. See
# [`solutions/15_llm_judge.md`](../solutions/15_llm_judge.md).
