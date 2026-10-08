# %% [markdown]
# # 09 · Shared context: how agents tell each other what they know
#
# **Goal:** when several agents work the same call (voice, lead scoring, dispatch), they need
# to share what they've learned without trusting each other blindly. You'll build that on a
# **context ledger**: an append-only log of typed facts with provenance and a trust level.
#
# You will:
# 1. see why passing the transcript around doesn't work
# 2. have the voice agent *propose* facts with confidence and evidence
# 3. let the control plane *verify* facts, and dispatch act only on verified ones
# 4. watch a misheard fact send the wrong technician, then fix it with trust rules
# 5. enforce who may write what, and handle two agents writing at once
# 6. react to changes with subscriptions instead of polling
#
# This is a teaching model of a general multi-agent pattern. Companies don't publish their
# internal designs; ServiceTitan has only described "shared context" at a high level
# (see [`docs/pantheon-2026-ai-roadmap.md`](../docs/pantheon-2026-ai-roadmap.md)).
# Runs fully offline.

# %%
import stlab
from stlab.context import ContextLedger, ContextError, context_tools

TRANSCRIPT = [
    ("caller", "Hi, my AC stopped blowing cold air this morning."),
    ("agent", "I'm sorry to hear that. Is anyone at home with health concerns in the heat?"),
    ("caller", "My mom's staying with us, she's 82. And honestly the unit is 19 years old,"
               " I'm wondering if it's time to replace it."),
    ("agent", "Understood. Would today work if we have an opening?"),
    ("caller", "Today would be great. I can't do tomorrow, I'm at work all day."),
]
for who, text in TRANSCRIPT:
    print(f"{who:>6}: {text}")

# %% [markdown]
# ## 1. Why not just share the transcript?
#
# Dispatch could read the transcript and work it out. But every downstream agent would then
# re-interpret free text its own way, nobody could tell which interpretation was trusted, and
# there'd be no record of *what we believed when we decided*. Instead, the agent closest to
# the evidence writes **facts**: typed, small, with a confidence and the span that supports them.

# %%
ledger = ContextLedger()
JOB = "J-5001"
voice = context_tools(ledger, "voice_agent")

proposals = [
    ("job_type", "no_cool_diagnostic", 0.93, "my AC stopped blowing cold air this morning"),
    ("urgency", "same_day", 0.88, "Today would be great"),
    ("constraint", "vulnerable_occupant", 0.85, "My mom's staying with us, she's 82"),
    ("constraint_note", "unavailable tomorrow", 0.80, "I can't do tomorrow"),
    ("intent", "replacement_interest", 0.74, "wondering if it's time to replace it"),
]
for key, value, conf, evidence in proposals:
    print(key, voice["propose_fact"](JOB, key, value, conf, evidence))

# %% [markdown]
# One proposal was refused: `constraint_note` isn't a key the voice agent may write. That's
# deliberate: the ledger has a schema, and an agent can't invent new fields other agents will
# start depending on. Write it as a valid key instead:

# %%
print(voice["propose_fact"](JOB, "callback_window", "today_only", 0.80, "I can't do tomorrow"))
print("\nWhat dispatch can see (verified only):", ledger.view(JOB))
print("What exists, including unverified    :", ledger.view(JOB, min_status="proposed"))

# %% [markdown]
# ## 2. Verification belongs to the control plane
#
# Agents only *propose*. The control plane promotes a fact to **verified** when it has
# evidence it trusts: the supporting words really appear in what the caller said, and the
# agent's confidence clears a threshold for that key (or the caller explicitly confirmed it).
# High-impact keys get a higher bar.

# %%
CALLER_TEXT = " ".join(t for who, t in TRANSCRIPT if who == "caller").lower()
THRESHOLD = {"job_type": 0.85, "urgency": 0.85, "constraint": 0.80, "callback_window": 0.75, "intent": 0.80}

def control_plane_verify(ledger, job_id, caller_text, confirmed_by_caller=()):
    results = {}
    for key in sorted({f.key for f in ledger.history(job_id)}):
        f = ledger.get(job_id, key, min_status="proposed")
        if f is None or f.status != "proposed":
            continue
        grounded = bool(f.evidence) and f.evidence.lower() in caller_text
        confident = f.confidence >= THRESHOLD.get(key, 0.9)
        if grounded and (confident or key in confirmed_by_caller):
            why = "caller confirmed" if key in confirmed_by_caller and not confident else "grounded + confident"
            ledger.verify(job_id, key, evidence=f"{why}: '{f.evidence}'")
            results[key] = "verified"
        else:
            results[key] = "left proposed" + ("" if grounded else " (evidence not in transcript)")
    return results

print(control_plane_verify(ledger, JOB, CALLER_TEXT))
print("\nVerified view:", ledger.view(JOB))

# %% [markdown]
# `intent=replacement_interest` stays proposed (0.74 < 0.80). Downstream agents can still
# *see* it if they explicitly ask for proposed facts, for example lead scoring might use it as
# a weak signal, but nobody can act on it as if it were confirmed. A good next move for the
# voice agent is to ask: "Would you like us to bring replacement options too?"

# %%
ledger.verify(JOB, "intent", evidence="caller said yes to replacement options")
print(ledger.view(JOB))

# %% [markdown]
# ## 3. Dispatch reads only what it may trust
#
# Dispatch picks a technician from verified facts. Lead scoring proposes `est_value` (its own
# key); the control plane verifies it because it's computed from verified inputs.

# %%
from stlab.coordination import lead_score

def score_job(ledger, job_id):
    v = ledger.view(job_id)
    signals = []
    if v.get("intent") == "replacement_interest": signals.append("replacement_interest")
    if v.get("urgency") == "same_day": signals.append("same_day_needed")
    value = lead_score(v.get("job_type", "unknown"), signals)
    ledger.propose("lead_scoring", job_id, "est_value", value, 0.9, evidence=f"lead_score({signals})")
    ledger.verify(job_id, "est_value", evidence="computed from verified facts only")
    return value

TECHS = {"Kara": "senior", "Luis": "junior"}

def dispatch_pick(ledger, job_id, min_status="verified"):
    v = ledger.view(job_id, min_status=min_status)
    high_value = v.get("est_value", 0) >= 1000
    urgent = v.get("urgency") == "same_day" or v.get("constraint") == "vulnerable_occupant"
    tech = "Kara" if (high_value or urgent) else "Luis"
    return tech, {"high_value": high_value, "urgent": urgent}

print("est_value:", score_job(ledger, JOB))
print("dispatch :", dispatch_pick(ledger, JOB))

# %% [markdown]
# ## 4. Break it: a misheard fact
#
# A second call. The caller says "**no** rush, any day **next** week is fine", but noise eats
# "no" and the voice agent proposes `urgency=same_day` at 0.62. The extraction is wrong, but
# its evidence span ("rush") *is* in the transcript, so a lazy grounding check would pass it.

# %%
JOB2 = "J-5002"
caller2 = "no rush, any day next week is fine. it's just a tune-up."
voice["propose_fact"](JOB2, "job_type", "hvac_tuneup", 0.95, "it's just a tune-up")
voice["propose_fact"](JOB2, "urgency", "same_day", 0.62, "rush")

print("Dispatch trusting *proposed* facts :", dispatch_pick(ledger, JOB2, min_status="proposed"))
print("Control plane:", control_plane_verify(ledger, JOB2, caller2))
print("Dispatch trusting *verified* facts :", dispatch_pick(ledger, JOB2))

# %% [markdown]
# Trusting proposed facts sends the senior tech to a routine tune-up; on a busy day that's the
# "effectiveness tax": a high-value job elsewhere gets the junior tech. With the trust rule,
# the low-confidence urgency never becomes verified, so dispatch ignores it.
#
# The fix wasn't a smarter dispatch agent. It was a **contract**: which status and confidence
# a consumer may act on, per key.

# %% [markdown]
# ## 5. Who may write what, and two writers at once

# %%
print(voice["propose_fact"](JOB, "assigned_tech", "Kara", 0.99, "I'd like Kara"))   # not the voice agent's key

try:
    ledger.propose("dispatch", JOB, "assigned_tech", "Kara", 1.0, expected_version=0)
    ledger.propose("dispatch", JOB, "assigned_tech", "Luis", 1.0, expected_version=0)   # stale read
except ContextError as e:
    print("second writer:", e.code, "->", e)
    current = ledger.version(JOB, "assigned_tech")
    print("re-read version", current, "; re-decide with the latest facts, then write with expected_version")

# %% [markdown]
# `expected_version` is **optimistic concurrency**: a writer says which version it based its
# decision on. If someone wrote in between, the write fails instead of silently overwriting.
#
# ## 6. Subscriptions instead of polling

# %%
events = []
ledger.subscribe("urgency", lambda f: events.append((f.job_id, f.value, f.status)))
JOB3 = "J-5003"
voice["propose_fact"](JOB3, "urgency", "same_day", 0.91, "water everywhere")
ledger.verify(JOB3, "urgency", evidence="grounded + confident")
print(events)

# %% [markdown]
# ## 7. Corrections and history
#
# The caller changes their mind: "Actually, tomorrow afternoon is fine." Facts are never edited.
# The control plane retracts the old one and the voice agent proposes the new value; the
# history keeps both, which the learning loop (lab 11) will need.

# %%
ledger.retract(JOB, "callback_window", reason="caller changed availability")
voice["propose_fact"](JOB, "callback_window", "tomorrow_pm", 0.9, "tomorrow afternoon is fine")
ledger.verify(JOB, "callback_window", evidence="caller said it directly")
for f in ledger.history(JOB, "callback_window"):
    print(f.version, f.status, f.value, "|", f.evidence)

# %% [markdown]
# ## Self-check

# %%
assert ledger.view(JOB2).get("urgency") is None, "misheard urgency must never be verified"
assert dispatch_pick(ledger, JOB2)[0] == "Luis"
assert dispatch_pick(ledger, JOB)[0] == "Kara"
assert ledger.view(JOB)["callback_window"] == "tomorrow_pm"
assert not voice["propose_fact"](JOB, "assigned_tech", "Kara", 0.99)["ok"]
print("All checks passed.")

# %% [markdown]
# ## Where the ledger stops
#
# - It records what agents believe and how much to trust it; it isn't the system of record.
#   A job is booked only when the backend says so (status `committed`, lab 10).
# - It doesn't make extraction accurate. It makes inaccuracy *visible* and *contained*, so you
#   can measure it (lab 11).
# - In production this is usually a database table plus an event stream; the logic (schema,
#   permissions, trust levels, versions) is the part that matters.
#
# ## Exercises
#
# 1. Lower the `urgency` threshold to 0.6 and rerun section 4. What breaks, and how would you
#    pick the threshold from data instead of intuition?
# 2. Add a per-consumer policy: lead scoring may use proposed `intent` at confidence ≥ 0.7, but
#    dispatch may not. Where should that policy live?
# 3. Two voice agents (phone and text) propose different `job_type` values for the same job.
#    Which one should win, and who decides?

# %% [markdown]
# ## Check your understanding
#
# 1. Why do agents propose facts instead of writing them directly as true?
# 2. What does `expected_version` protect against, and what should a writer do when it fails?
# 3. Why keep retracted facts in the history instead of deleting them?
#
# **Graded exercise:** give `callback_window` facts a time-to-live (`ttl=`) so a stale
# availability can't be used after it expires, then assert that `ledger.view()` no longer
# returns it once the clock passes the expiry. See
# [`solutions/09_shared_context.md`](../solutions/09_shared_context.md).
