# %% [markdown]
# # 13 · Mini-Max: the voice agent as the system's sensor
#
# **Goal:** follow one call from speech-derived facts through bookability, lead scoring,
# dispatch, control-plane commitment, and claim verification.
#
# This is a synthetic teaching system inspired by public Pantheon 2026 descriptions. It is
# not ServiceTitan's implementation. The key engineering question is what downstream agents
# are allowed to trust.
#
# **Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

# %%
import pandas as pd
import matplotlib.pyplot as plt
from stlab.calls import load_calls
from stlab.minimax import run_call, error_sensitivity

calls = load_calls()
sample = calls[:20]
results = [run_call(c) for c in sample]
print("dataset:", len(calls), "calls; capstone sample:", len(sample))

# %% [markdown]
# ## 1. One call, end to end
#
# Read the trace as a system trace, not a model transcript: extraction proposes facts,
# bookability decides what is permitted, scoring values the opportunity, dispatch chooses
# capacity, the control plane commits, and the claim guard checks what can be said.

# %%
trace_rows = []
for result in results:
    trace_rows.append({
        "call_id": result["call_id"],
        "action": result["decision"].action,
        "reason": result["decision"].reason,
        "assigned_tech": result["assigned_tech"],
        "est_value": result["est_value"],
        "committed": result["committed"],
        "idempotent_retry": result["idempotent_retry"],
        "claim_guard_blocked_false_claim": result["false_claim"],
    })
trace = pd.DataFrame(trace_rows)
display(trace)

# %% [markdown]
# ## 2. Error propagation
#
# Inject one extraction error at a time. A useful sensitivity analysis asks not only whether
# the extraction was wrong, but whether the wrong fact crossed a permission/trust boundary and
# changed a business decision.

# %%
sensitivity = pd.DataFrame(error_sensitivity(sample))
display(sensitivity.sort_values("value_delta"))

# %% [markdown]
# The interesting rows are not necessarily the largest extraction errors. A missed replacement
# signal can change lead value without changing booking, while a wrong emergency or job type
# can cross a much more consequential control-plane boundary.

# %% [markdown]
# ## 3. Confidence floors
#
# A downstream consumer should not accept a fact merely because the extractor emitted a value.
# Sweep the minimum confidence required to act and watch automation fall as the evidence bar rises.

# %%
floors = [round(x, 2) for x in [0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95]]
rows = []
for floor in floors:
    decisions = [run_call(c, floor)["decision"].action for c in sample]
    automation = sum(a == "book" for a in decisions) / len(decisions)
    error_cost = 0.0
    for record, action in zip(sample, decisions):
        if action == "book" and not record["bookable"]:
            error_cost += 1500
        elif action != "book" and record["bookable"]:
            error_cost += 250
    rows.append({"confidence_floor": floor, "automation_rate": automation,
                 "error_cost": error_cost})
floor_df = pd.DataFrame(rows)
display(floor_df)

# %%
fig, ax = plt.subplots()
ax.plot(floor_df["confidence_floor"], floor_df["automation_rate"], marker="o")
ax.set_xlabel("Downstream confidence floor")
ax.set_ylabel("Automation rate")
ax.set_title("Automation rate vs. confidence floor")
ax.grid(True)
plt.show()

# %% [markdown]
# ## 4. Business outcomes from the same dataset
#
# The dataset is synthetic, so these are teaching numbers. The point is to connect system
# decisions to contractor outcomes rather than to optimize a model score in isolation.

# %%
bookable_calls = sum(c["bookable"] for c in calls)
booked_calls = sum(c["outcome"]["booked"] for c in calls)
actual_revenue = sum(c["outcome"]["actual_value"] for c in calls)
after_hours = sum(c["after_hours"] for c in calls)
print({
    "calls": len(calls),
    "bookable_opportunities": bookable_calls,
    "booked_jobs": booked_calls,
    "bookable_to_booked_rate": round(booked_calls / bookable_calls, 3),
    "after_hours_share": round(after_hours / len(calls), 3),
    "synthetic_actual_revenue": round(actual_revenue, 2),
})

# %% [markdown]
# ## 5. Exercises
#
# 1. Add a new fact type end to end: add it to the schema, permissions, extractor, consumer,
#    and a regression test. Write down which agents are allowed to consume it.
# 2. Find the seeded contract violation: make a downstream consumer act on a proposed fact
#    below the confidence floor. Fix it without changing the extractor.
# 3. Add a deterministic test proving that an emergency can never reach the booking tool.
# 4. Add a trace field for the exact evidence span that justified the bookability decision.

# %% [markdown]
# ## Capstone acceptance rubric
#
# | Requirement | Pass condition |
# |---|---|
# | Grounded confirmation | Booking requires application state, not model wording |
# | Emergency safety | Zero emergency calls reach a routine booking commit |
# | Idempotency | A repeated commit returns the original job |
# | Claim guard | No uncommitted booking is emitted as "you're booked" |
# | Injection handling | Injection attempts are refused or transferred |
# | Decision trace | Every downstream decision has a trace entry |
# | Evidence contract | Every accepted fact has evidence and clears the floor |
# | Business linkage | Lead value and booking outcomes are visible in the trace |
#
# **Graded exercise:** add one new fact type all the way from schema to consumer and prove with
# a test that a low-confidence version cannot trigger a booking.
#
# ## Check your understanding
#
# 1. Why is a wrong extraction only dangerous when it crosses a downstream trust boundary?
# 2. Which evidence should the claim guard trust: the model's sentence or committed state?
# 3. Why can a higher confidence floor reduce automation while improving expected business value?
