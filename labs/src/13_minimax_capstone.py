# %% [markdown]
# # 13 · Mini-Max: the voice agent as the system's sensor
#
# **Goal:** follow calls from the words the caller said, to structured facts, to business
# decisions (book, transfer, decline, call back), to a committed booking, a dispatched
# technician, and finally what the agent is allowed to *say*. Then break it on purpose.
#
# At Pantheon 2026 ServiceTitan described Max as many agents working from shared context, with
# lead scoring that uses what was said on the call and a separate "voice intelligence" judge
# of which calls were bookable (company claims; see
# [`docs/pantheon-2026-ai-roadmap.md`](../docs/pantheon-2026-ai-roadmap.md)). That makes the
# voice agent a *sensor*: its facts drive other agents' decisions. This lab is a small
# synthetic system built on that idea, not ServiceTitan's implementation. The design questions
# behind its facts contract are in [`docs/call-facts-contract.md`](../docs/call-facts-contract.md).
#
# You will:
# 1. trace calls end to end and read the trace as a system, not a transcript
# 2. inject one extraction error at a time and see which ones actually cost money
# 3. find the confidence floor that minimizes error cost for a noisy extractor
# 4. find and fix a consumer that trusts facts it shouldn't
#
# Uses the shared synthetic dataset (`labs/data/calls/`, see its DATASHEET). Offline.
#
# **Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

# %%
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd

from stlab.calls import load_calls
from stlab.minimax import (
    ERROR_TYPES, error_sensitivity, extract_call_facts, facts_to_ledger, floor_sweep,
    gold_action, run_call,
)

calls = load_calls()
print(len(calls), "synthetic calls")
print("what a correct system would do:", dict(Counter(gold_action(c) for c in calls)))

# %% [markdown]
# ## 1. One call, end to end
#
# The extractor turns the transcript into `CallFacts`: each field has a value, a confidence,
# and the caller's words that support it. Downstream agents never see the transcript, only the
# facts, so the facts are a **contract**.

# %%
call = next(c for c in calls if c["scenario"] == "no_cool_heatwave")
for turn in call["transcript"]:
    print(f'{turn["speaker"]:>6}: {turn["text"]}')
facts = extract_call_facts(call)
pd.DataFrame([{"field": k, "value": v.value, "confidence": v.confidence,
               "evidence": v.evidence[0]["quote"]} for k, v in facts.fields.items()])

# %%
result = run_call(call)
for step in result["trace"]:
    print(step)

# %% [markdown]
# Read the trace stage by stage. Bookability decides what's permitted. The commit goes through
# `execute_tool` with grounded confirmations (lab 02). Retrying the same booking returns the
# same job, because the idempotency key belongs to the application. Only *after* the commit
# does the system score the lead and dispatch. The claim guard checks the sentence against
# committed state before it's spoken.

# %%
sample = calls[:40]
rows = [run_call(c) for c in sample]
trace = pd.DataFrame([{
    "call_id": r["call_id"], "scenario": c["scenario"], "action": r["decision"].action,
    "committed": r["committed"], "idempotent_retry": r["idempotent_retry"],
    "tech": r["assigned_tech"], "est_value": r["est_value"], "spoken": r["spoken"],
} for r, c in zip(rows, sample)])
print("false 'you're booked' claims:", sum(r["false_claim"] for r in rows))
trace.head(12)

# %% [markdown]
# ## 2. Error propagation: which mistakes matter?
#
# Take the correct facts for every call, inject one *confident* mistake at a time, and measure
# what changes downstream: decisions, wrong bookings, emergencies booked, missed bookings,
# lead value and technician assignment. Costs are illustrative: a wrong booking costs $1,500
# (wasted truck roll, rework, trust), and a missed booking costs $250.

# %%
sens = pd.DataFrame(error_sensitivity(calls))
sens.sort_values("error_cost", ascending=False)

# %% [markdown]
# Things to notice:
#
# - **Most errors fail safe.** A flipped `bookable` mostly turns bookings into declines, and a
#   low-confidence `intent` or a conflict turns them into callbacks. That's costly in lost
#   bookings and staff time, but nobody gets sent a wrong truck. Layered rules (emergency,
#   injection, service area, job type) catch most of the dangerous flips.
# - **A wrong job type is the expensive one here, and it changes no decision at all.** The
#   call still books, so nothing looks wrong. But it's the wrong work, needing the wrong
#   skills, in the wrong-length slot. Errors that leave the decision unchanged but corrupt
#   *what* was decided are the hardest to catch with decision-level metrics.
# - **Some errors are invisible to booking but not to the business.** A missed replacement
#   signal changes no decision, yet it removes lead value and sends a junior tech to a job the
#   senior tech should take. A sentiment error changes nothing at all *in this system*. Would
#   that still hold if sentiment fed lead scoring, as the public Pantheon material suggests?
# - **`emergency_missed` costs nothing, because of one line of defense.** Turn that defense
#   off and see what happens:

# %%
no_screen = pd.DataFrame(error_sensitivity(calls, transcript_screen=False)).set_index("error_type")
with_screen = sens.set_index("error_type")
pd.DataFrame({"emergencies booked (screen on)": with_screen["emergencies_booked"],
              "emergencies booked (screen off)": no_screen["emergencies_booked"]})

# %% [markdown]
# The control plane screens the caller's raw words for emergency terms, *independently of the
# extractor*. When the extractor confidently says "not an emergency, bookable furnace repair"
# for "I smell gas near the furnace", the screen still transfers. That's defense in depth: the
# most dangerous decision doesn't rest on one model's output.

# %% [markdown]
# ## 3. How much should downstream agents trust the extractor?
#
# Now use a *noisy* extractor (`noise=0.12`): some fields are wrong, and wrong values sometimes
# carry high confidence. A downstream confidence floor decides which facts may be acted on.
# Below the floor, critical facts send the call to a person.

# %%
floors = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
sweep = pd.DataFrame(floor_sweep(calls, floors, noise=0.12))
sweep

# %%
fig, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(sweep["confidence_floor"], sweep["automation_rate"], marker="o", label="automation rate")
ax1.set_xlabel("Downstream confidence floor")
ax1.set_ylabel("Share of bookable calls booked automatically")
ax2 = ax1.twinx()
ax2.plot(sweep["confidence_floor"], sweep["error_cost"], marker="s", color="tab:red", label="error cost")
ax2.set_ylabel("Illustrative error cost ($)")
fig.legend(loc="upper center", ncol=2)
ax1.set_title("Raising the floor trades automation for fewer wrong actions")
plt.show()
best = sweep.loc[sweep["error_cost"].idxmin()]
print(f"lowest-cost floor: {best.confidence_floor} (automation {best.automation_rate:.0%}, "
      f"{int(best.wrong_bookings)} wrong bookings, ${best.error_cost:,.0f})")

# %% [markdown]
# The cost curve has a minimum. Too low a floor lets confident mistakes through as wrong
# bookings. Too high a floor sends good calls to people. Where the minimum sits depends on the
# cost ratio. Rerun the sweep in your head with a wrong booking at $5,000: the best floor
# moves up.

# %% [markdown]
# ## 4. A consumer that trusts too much (seeded bug)
#
# The voice agent *proposes* every fact to the context ledger (lab 09). The control plane
# *verifies* only facts that clear the floor and are grounded in the caller's words. Here is a
# downstream consumer, a lead-priority agent, written carelessly:

# %%
noisy_call = next(c for c in calls if c["scenario"] == "topic_switch")
noisy = extract_call_facts(noisy_call, noise=0.6, seed=3)       # a bad day for the extractor
ledger = facts_to_ledger(noisy, confidence_floor=0.85)


def priority_agent(ledger, call_id):
    """Seeded bug: reads *proposed* facts, so it acts on facts nobody verified."""
    facts = ledger.view(call_id, min_status="proposed")
    return "high" if facts.get("urgency") == "same_day" or facts.get("replacement_interest") else "normal"


print("proposed :", ledger.view(noisy_call["call_id"], min_status="proposed"))
print("verified :", ledger.view(noisy_call["call_id"]))
print("priority (buggy):", priority_agent(ledger, noisy_call["call_id"]))

# %% [markdown]
# Exercise: fix `priority_agent` so it acts only on verified facts, *without* changing the
# extractor or lowering the global floor. Then decide what it should do when a fact it needs
# isn't verified: assume the default, or ask?

# %% [markdown]
# ## 5. Business outcomes from the same data
#
# The dataset carries synthetic outcomes, so you can connect decisions to contractor terms.
# These are teaching numbers, not benchmarks. The dataset contains only answered calls, so it
# can't tell you how many calls were *missed*; that's an input to the value calculator on the
# site, not something this data can measure.

# %%
booked = [c for c in calls if c["outcome"]["booked"]]
pd.Series({
    "calls": len(calls),
    "bookable opportunities (gold)": sum(c["bookable"] for c in calls),
    "booked jobs": len(booked),
    "booking rate, of bookable calls": round(len(booked) / sum(c["bookable"] for c in calls), 3),
    "booking rate, of ALL calls": round(len(booked) / len(calls), 3),
    "after-hours share": round(sum(c["after_hours"] for c in calls) / len(calls), 3),
    "average ticket ($)": round(sum(c["outcome"]["actual_value"] for c in booked) / len(booked), 2),
})

# %% [markdown]
# Notice the two booking rates. The same bookings look like 86% or 50% depending on the
# denominator. That's why the company's public answer to gameable booking rates was a separate
# judge of which calls were bookable.

# %% [markdown]
# ## Capstone acceptance rubric
#
# | Requirement | Pass condition |
# |---|---|
# | Grounded confirmation | A booking needs grounded address and slot confirmations in application state |
# | Emergency safety | Zero emergencies reach a booking, even when the extractor misses them |
# | Idempotency | Retrying a commit returns the original job |
# | Claim guard | Zero "you're booked" without a committed job |
# | Injection handling | Override attempts are transferred, never obeyed |
# | Decision trace | Every call has extract → ledger → bookability → (commit → dispatch) → claim |
# | Evidence contract | Only facts at or above the floor, with evidence, are verified or acted on |
# | Business linkage | Lead value and dispatch happen only after a commit |
#
# ## Check your understanding
#
# 1. Why is an extraction error only expensive when it crosses a decision boundary? Give an example from the sensitivity table of one that doesn't.
# 2. Why does the transcript emergency screen sit in the control plane rather than inside the extractor?
# 3. Why can a *higher* confidence floor reduce automation and still lower total cost?
#
# **Graded exercise:** add a new fact, `callback_window` (when the caller can be reached),
# end to end: extractor, `CallFacts` JSON Schema, ledger permissions, and a consumer that uses
# it only when verified. Then add a test proving that a low-confidence `callback_window` can't
# change any decision. See [`solutions/13_minimax_capstone.md`](../solutions/13_minimax_capstone.md).
