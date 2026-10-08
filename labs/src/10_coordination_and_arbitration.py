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
        subprocess.run(["git", "clone", "-q",
                        "https://github.com/sp7412/onboarding.git", repo],
                       check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "-r", os.path.join(repo, "requirements.txt")],
                   check=True)
    os.chdir(os.path.join(repo, "labs"))
    print("Colab environment ready:", os.getcwd())
else:
    print("Local/Codespaces environment detected; use the normal repository setup.")

# %% [markdown]
# # 10 · Coordination: when good agents make bad decisions together
#
# **Goal:** see why several agents, each optimizing its own metric, can still make the
# business worse, and build the pieces that make them act as a team: **shared judgment**,
# **coordinated action** with the receiver's rules, **arbitration** by expected value, and
# **hard constraints** that arbitration can never trade away.
#
# You will:
# 1. run four independent agents on a full board and measure the damage
# 2. give them one shared lead-scoring and demand-forecast function
# 3. let the booking agent *request* that dispatch free a slot, with the customer's consent
# 4. arbitrate competing proposals on a light board
# 5. add hard rules (consent, emergencies, no repeat moves) the arbiter must obey
#
# The scenarios mirror the failure modes described publicly at Pantheon 2026 (ads spending on
# a full board, a high-value job getting the wrong tech, a strong lead offered tomorrow). The
# code is a teaching model, not ServiceTitan's design. All numbers are illustrative. Offline.

# %%
import copy
from stlab.coordination import (Board, Job, Proposal, arbitrate, assign_tech, demand_forecast,
                                lead_score, request_move)

def full_board():
    techs = {"S1": "Kara", "S2": "Luis", "S3": "Mo", "S4": "Luis"}
    jobs = [Job("J-1", "Avery", "tune_up", 150), Job("J-2", "Blake", "ac_repair", 450),
            Job("J-3", "Casey", "tune_up", 150), Job("J-4", "Drew", "ac_repair", 500)]
    return Board(slots=dict(zip(techs, jobs)), techs=techs,
                 tech_level={"Kara": "senior", "Luis": "junior", "Mo": "junior"})

NEW_LEAD = Job("J-9", "Elena", "no_cool_diagnostic", 0,
               signals=["system_down", "replacement_interest", "same_day_needed"])

board = full_board()
print("Open slots today:", board.open_slots(), "| booked value:", board.booked_value())

# %% [markdown]
# ## 1. Independent agents
#
# Each agent sees only its own job:
# - **Ads agent:** maximizes leads, so it keeps spending ($300 today).
# - **Email agent:** maximizes bookings from campaigns, so it sends a tune-up promotion.
# - **Speed-to-lead agent:** answers Elena instantly but can't create capacity, so it offers
#   tomorrow. She has no cooling and wants today, so assume she calls a competitor.
# - **Dispatch agent:** fills slots in order and assigns whichever tech is free.

# %%
def run_independent(board, lead):
    waste = 300                                    # ad spend for leads nobody can serve today
    emails_sent = 1200                             # customer attention spent on a full board
    if board.open_slots():
        slot = board.open_slots()[0]
        board.slots[slot] = lead
        captured = lead_score(lead.job_type, lead.signals)
    else:
        captured = 0                               # offered tomorrow; lost to a competitor
    return {"captured_value": captured, "wasted_spend": waste, "emails_sent": emails_sent,
            "credits": 0}

independent = run_independent(full_board(), copy.deepcopy(NEW_LEAD))
print(independent)

# %% [markdown]
# Every agent did its job well and the business still lost: money spent on leads it couldn't
# serve, customer attention spent on promotions, and the most valuable lead of the day gone.
# Keynote language for this: an **effectiveness tax** (value left on the table) and an
# **overhead tax** (people untangling conflicts).
#
# ## 2. Shared judgment
#
# Give every agent the same two functions. Now ads and email can see there's no capacity to
# sell, and everyone values Elena's call the same way.

# %%
board = full_board()
gap = demand_forecast(open_slots=len(board.open_slots()), expected_new_calls=6)
elena_value = lead_score(NEW_LEAD.job_type, NEW_LEAD.signals)
print("forecast gap (negative = more demand than capacity):", gap)
print("Elena's expected value:", elena_value)
print("lowest-value job on the board:", board.slots[board.lowest_value_slot()])

# %% [markdown]
# ## 3. Coordinated action: request, don't reach in
#
# The booking agent doesn't move anyone's appointment itself. It **requests** a move from
# dispatch, and dispatch applies its own rules: the moved customer must consent, gets a credit,
# and can't be moved more than once. Consent is simulated here; in production it's a real
# call or text.

# %%
def run_coordinated(board, lead, consent):
    lead = copy.deepcopy(lead)
    lead.est_value = lead_score(lead.job_type, lead.signals)
    result = {"captured_value": 0, "wasted_spend": 0, "emails_sent": 0}
    gap = demand_forecast(len(board.open_slots()), expected_new_calls=6)
    if gap < 0:
        board.log.append("ads and email stand down: forecast says capacity is full")
    slot = board.open_slots()[0] if board.open_slots() else board.lowest_value_slot()
    if board.slots.get(slot) is not None:
        moved, why = request_move(board, slot, consent)
        board.log.append(f"request_move({slot}) -> {why}")
        if not moved:
            board.log.append("fallback: offer Elena the earliest slot tomorrow and a callback if one opens")
            return result | {"credits": board.credits_issued}
    tech = assign_tech(board, slot, lead)
    result["captured_value"] = lead.est_value
    board.log.append(f"booked {lead.job_id} today with {tech}")
    return result | {"credits": board.credits_issued}

board = full_board()
coordinated = run_coordinated(board, NEW_LEAD, consent=lambda job, ask: True)
print(coordinated)
print(*board.log, sep="\n")

# %% [markdown]
# Elena is booked today with the senior tech, Avery's tune-up moves to tomorrow with a credit
# she agreed to, and no money was spent chasing leads the board couldn't serve.
#
# Now the case that matters most: **the customer says no**.

# %%
board_no = full_board()
declined = run_coordinated(board_no, NEW_LEAD, consent=lambda job, ask: False)
print(declined)
print(*board_no.log, sep="\n")

# %% [markdown]
# The booking agent wanted the slot and had a higher-value job, but consent is a **hard
# rule**: expected value can't buy it. The system falls back honestly instead of overbooking
# or moving someone without asking.
#
# ## 4. Arbitration on a light board
#
# Thursday is forecast light. Three agents each want to fill the gap.

# %%
light = Board(slots={"S1": None, "S2": None, "S3": Job("J-5", "Fran", "ac_repair", 450), "S4": None},
              techs={"S1": "Kara", "S2": "Luis", "S3": "Mo", "S4": "Luis"},
              tech_level={"Kara": "senior", "Luis": "junior", "Mo": "junior"})
capacity = len(light.open_slots())
proposals = [
    Proposal("ads", "increase_ads", expected_value=0.35 * 2 * 450, cost=200, params={"slots": 2},
             reason="2 leads expected, 35% book, avg $450"),
    Proposal("memberships", "book_tune_ups", expected_value=2 * 150, cost=20, params={"slots": 2},
             reason="2 members due for tune-ups"),
    Proposal("dispatch", "pull_forward", expected_value=450, cost=25, params={"slots": 1},
             needs_consent=True, reason="pull Friday's repair into Thursday"),
]
for d in arbitrate(proposals, capacity):
    print(f"{'ACCEPT' if d.accepted else 'reject':6} {d.proposal.agent:12} net={d.proposal.net:6.0f}  {d.reason}")

# %% [markdown]
# The arbiter ranks by **net expected value** and stops at capacity. Ads lose here: on this
# board, $200 of spend for an expected $315 nets less than free tune-ups and a pull-forward.
#
# ## 5. Hard rules the arbiter can't trade away
#
# Expected value is the tiebreaker, not the authority. Some rules veto a proposal outright,
# whatever it's worth.

# %%
def no_consent_no_move(p):
    if p.needs_consent and not p.params.get("consent_obtained"):
        return "needs the customer's consent first"
def emergencies_first(p):
    if p.params.get("emergency_waiting") and p.action != "book_emergency":
        return "an emergency is waiting; only emergency booking may take capacity"

for d in arbitrate(proposals, capacity, hard_rules=[no_consent_no_move]):
    print(f"{'ACCEPT' if d.accepted else 'reject':6} {d.proposal.agent:12} {d.reason}")

emergency = Proposal("voice_agent", "book_emergency", expected_value=600, cost=0,
                     params={"slots": 1}, reason="gas smell reported; safety script given")
blocked = [Proposal(p.agent, p.action, p.expected_value, p.cost, {**p.params, "emergency_waiting": True},
                    p.needs_consent, p.reason) for p in proposals]
print()
round1 = arbitrate(blocked + [emergency], capacity, hard_rules=[emergencies_first])
for d in round1:
    print(f"{'ACCEPT' if d.accepted else 'reject':6} {d.proposal.agent:12} {d.reason}")

# %% [markdown]
# Nothing else takes capacity while the emergency is unhandled. Once it's booked, the flag
# clears and the remaining capacity is arbitrated again under the normal rules.

# %%
left = capacity - sum(d.proposal.params.get("slots", 1) for d in round1 if d.accepted)
round2 = arbitrate(proposals, left, hard_rules=[no_consent_no_move])
for d in round2:
    print(f"{'ACCEPT' if d.accepted else 'reject':6} {d.proposal.agent:12} {d.reason}")

# %% [markdown]
# ## Self-check

# %%
assert independent["captured_value"] == 0 and independent["wasted_spend"] > 0
assert coordinated["captured_value"] == lead_score(NEW_LEAD.job_type, NEW_LEAD.signals)
assert coordinated["wasted_spend"] == 0 and coordinated["credits"] == 25
assert declined["captured_value"] == 0 and all(j is not None for j in board_no.slots.values())
assert board.slots[[s for s, t in board.techs.items() if t == "Kara"][0]].job_id == "J-9", "senior tech takes the high-value job"
consented = [d for d in arbitrate(proposals, capacity, hard_rules=[no_consent_no_move]) if d.proposal.agent == "dispatch"][0]
assert not consented.accepted
assert [d.proposal.agent for d in round1 if d.accepted] == ["voice_agent"]
assert any(d.accepted and d.proposal.agent == "memberships" for d in round2)
print("All checks passed.")

# %% [markdown]
# ## Where coordination stops
#
# - Arbitration needs **comparable** value estimates. If two agents score value differently,
#   the arbiter is comparing apples and guesses; that's why shared judgment comes first.
# - Expected values are predictions. Lab 11 closes the loop so they get better.
# - Coordination doesn't replace the control plane. Moves and bookings still go through the
#   backend's checks, and consent is a fact the control plane verifies, not a flag an agent sets.
#
# ## Exercises
#
# 1. Make the ads agent's expected value depend on the forecast gap. At what gap does
#    `increase_ads` start winning?
# 2. Add a `max_credit_per_day` budget to `request_move`. What should happen when it's spent?
# 3. Two leads arrive at once and there's one movable slot. Write the arbitration rule, and
#    decide what each caller is told.

# %% [markdown]
# ## Check your understanding
#
# 1. Why can independent agents that each do their job well still produce a worse outcome?
# 2. Why does the booking agent *request* a move instead of moving the job itself?
# 3. Which decisions should never be made by expected value alone?
#
# **Graded exercise:** add a customer-protection rule so nobody is moved twice in the same
# week (track moves across days), then assert that a second `request_move` for the same
# customer is refused even when the requester's job is worth more. See
# [`solutions/10_coordination_and_arbitration.md`](../solutions/10_coordination_and_arbitration.md).
