# %% [markdown]
# # 17 · Prompting Jev for typed decisions
#
# **Goal:** turn a vague classification prompt into a bounded, testable decision contract.
# Define state, write discriminative instructions and criteria, inspect labeled fictional
# call turns, and optionally call the live API.
#
# Jev is a decision model, not a chat-completion endpoint. A request contains state and typed
# questions: choice, noul, and score. The question ID is only a response key; put the decision
# in instructions. Criteria define allowed answers. Application code owns thresholds,
# authorization, routing, and side effects.
#
# The notebook runs offline. Live requests are opt-in and may incur usage charges.
# Set JEVMODEL_API_KEY in your environment or Colab Secrets only if you choose live mode.
# Use fictional examples only; never paste customer transcripts or secrets.
#
# **Facts as of: October 14, 2026 · Last reviewed: October 14, 2026**
#
# Primary reference: https://jevmodel.org/docs/
# Companion guide: ../docs/jev-call-intent-classification.md

# %%
import json
import os
import urllib.error
import urllib.request
from collections import Counter
from pprint import pprint

# %% [markdown]
# ## 1. The decision contract
#
# A useful decision prompt answers four questions:
# 1. What state is being judged? Include relevant facts and distinguish caller words from metadata.
# 2. What exact question should Jev answer? Write it in instructions, not just the ID.
# 3. What do the labels mean? Make criteria mutually distinguishable and action-oriented.
# 4. What happens with uncertainty? Define clarification and fallback behavior in code.
#
# Choice selects one label from a fixed set. Noul estimates the probability that a proposition
# is true. Score places the state on an ordered scale. Related questions can share one state.

# %%
INTENT_CRITERIA = {
    "schedule_service": "Caller wants a new service visit; no existing appointment is being changed.",
    "reschedule_service": "Caller wants to change the date or time of an existing appointment.",
    "cancel_service": "Caller explicitly wants to cancel an existing appointment or scheduled visit.",
    "appointment_status": "Caller asks about arrival time or status of an existing appointment.",
    "pricing_or_service_question": "Caller asks about price or service capabilities without requesting an appointment action.",
    "existing_job_followup": "Caller follows up on a prior or ongoing repair or unresolved problem.",
    "emergency_or_safety": "Caller states a potential immediate safety hazard requiring the approved safety workflow.",
    "human_agent_request": "Caller explicitly asks to speak with a human representative.",
    "other_or_unclear": "Intent is unsupported, insufficiently specified, or genuinely ambiguous.",
}

# %% [markdown]
# ## 2. Make the state concrete
#
# Include the committed caller turn and only the context needed to disambiguate the decision.

# %%
example_state = {
    "caller_utterance": "Can you move my appointment to Friday afternoon?",
    "appointment_context": {
        "existing_appointment": True,
        "current_appointment_time": "Tuesday 10:00 AM",
    },
    "workflow_state": "collecting_intent",
}
pprint(example_state)

# %% [markdown]
# ## 3. Write the request
#
# This schema follows the Jev System One HTTP API documentation. The question ID is a response
# key; the instructions must fully define the judgment. The criteria define the answer space.

# %%
intent_question = {
    "type": "choice",
    "instructions": (
        "Classify the caller's current primary intent from caller_utterance, using "
        "appointment_context only to disambiguate whether an appointment already exists. "
        "Choose exactly one label. Prefer the requested next action over incidental details. "
        "Use emergency_or_safety only when a potential immediate hazard is stated. "
        "Use other_or_unclear when evidence is insufficient; do not guess."
    ),
    "criteria": INTENT_CRITERIA,
}
request_body = {
    "model": "jev-latest",
    "state": example_state,
    "questions": {
        "intent": intent_question,
        "needs_clarification": {
            "type": "noul",
            "instructions": (
                "Is the requested next action materially ambiguous or missing a fact that must "
                "be clarified before selecting a workflow? Answer yes if plausible interpretations "
                "would lead to different actions; otherwise no."
            ),
        },
        "human_handoff": {
            "type": "noul",
            "instructions": (
                "Does the caller explicitly request a human representative? Do not infer this "
                "solely from frustration or an unclear request."
            ),
        },
        "urgency": {
            "type": "score",
            "instructions": "Rate urgency explicitly supported by the caller's words; do not infer an emergency from ordinary inconvenience.",
            "criteria": [
                "Routine: ordinary information or scheduling with no time pressure.",
                "Soon: near-term need but no immediate hazard.",
                "Urgent: explicit time-sensitive service problem, no stated immediate hazard.",
                "Critical: plausible immediate safety hazard requiring the approved safety workflow.",
            ],
        },
    },
}
print(json.dumps(request_body, indent=2))

# %% [markdown]
# ## 4. Prompting is taxonomy design, not magic wording
#
# Compare a vague instruction with one that specifies the unit of classification, priority rules,
# and a catch-all. We will not pretend a local keyword heuristic is Jev; it is only a baseline
# to make error analysis tangible before any paid model call.

# %%
weak_instructions = "What is the caller asking for?"
strong_instructions = intent_question["instructions"]
print("WEAK:\n", weak_instructions, "\n\nSTRONG:\n", strong_instructions)

# %% [markdown]
# Prompt review checklist:
# - Is the target decision one clear sentence?
# - Are labels distinct in terms of next workflow action?
# - Does each criterion describe positive evidence?
# - Are safety and human-request cases explicit?
# - Is there an other_or_unclear path?
# - Are response probabilities interpreted according to the actual API schema?
# - Does application code retain final authority to route or execute tools?

# %% [markdown]
# ## 5. Create a small labeled evaluation set
#
# These fictional examples are teaching data, not an authoritative business taxonomy. Real
# evaluation requires reviewed labels, a documented policy, and a held-out test set.

# %%
examples = [
    {"text": "I need someone to look at my AC; it stopped cooling.", "existing": False, "gold": "schedule_service"},
    {"text": "Can you move my appointment to Friday afternoon?", "existing": True, "gold": "reschedule_service"},
    {"text": "Please cancel the visit scheduled for tomorrow.", "existing": True, "gold": "cancel_service"},
    {"text": "What time is the technician supposed to arrive?", "existing": True, "gold": "appointment_status"},
    {"text": "Do you service tankless water heaters?", "existing": False, "gold": "pricing_or_service_question"},
    {"text": "How much does a diagnostic visit cost?", "existing": False, "gold": "pricing_or_service_question"},
    {"text": "The repair from yesterday still isn't working.", "existing": False, "gold": "existing_job_followup"},
    {"text": "I smell gas in the kitchen.", "existing": False, "gold": "emergency_or_safety"},
    {"text": "Let me speak to a person, please.", "existing": False, "gold": "human_agent_request"},
    {"text": "I need help, but I'm not sure what service I need.", "existing": False, "gold": "other_or_unclear"},
    {"text": "Can I get an appointment, and what do you charge?", "existing": False, "gold": "schedule_service"},
    {"text": "The technician is late; is anyone coming today?", "existing": True, "gold": "appointment_status"},
    {"text": "I want to change the time of tomorrow's visit.", "existing": True, "gold": "reschedule_service"},
    {"text": "The drain you cleared is blocked again.", "existing": False, "gold": "existing_job_followup"},
    {"text": "Cancel my appointment, and then let me talk to an agent.", "existing": True, "gold": "human_agent_request"},
    {"text": "There is water spreading across the floor near an outlet.", "existing": False, "gold": "emergency_or_safety"},
    {"text": "Do you install new thermostats?", "existing": False, "gold": "pricing_or_service_question"},
    {"text": "Could someone come out next week to inspect the furnace?", "existing": False, "gold": "schedule_service"},
    {"text": "I don't remember whether I have an appointment.", "existing": False, "gold": "other_or_unclear"},
    {"text": "I'm unhappy with the last repair and need it fixed properly.", "existing": False, "gold": "existing_job_followup"},
]
print(f"{len(examples)} examples | label counts: {dict(Counter(r['gold'] for r in examples))}")

# %% [markdown]
# ## 6. Establish a deliberately simple baseline
#
# This is a teaching comparator, not a Jev implementation or a competitor claim.

# %%
def keyword_baseline(text):
    t = text.lower()
    if any(term in t for term in ("smell gas", "water spreading", "near an outlet")):
        return "emergency_or_safety"
    if any(term in t for term in ("speak to a person", "talk to an agent", "human representative")):
        return "human_agent_request"
    if any(term in t for term in ("cancel", "cancellation")):
        return "cancel_service"
    if any(term in t for term in ("move my appointment", "change the time", "reschedule")):
        return "reschedule_service"
    if any(term in t for term in ("what time", "is anyone coming", "supposed to arrive", "technician is late")):
        return "appointment_status"
    if any(term in t for term in ("repair from yesterday", "still isn't working", "blocked again", "last repair")):
        return "existing_job_followup"
    if any(term in t for term in ("how much", "cost", "do you service", "do you install")):
        return "pricing_or_service_question"
    if any(term in t for term in ("appointment", "come out", "someone to look", "stopped cooling")):
        return "schedule_service"
    return "other_or_unclear"

predictions = [keyword_baseline(r["text"]) for r in examples]
correct = sum(p == r["gold"] for p, r in zip(predictions, examples))
print(f"Baseline accuracy on this tiny teaching set: {correct}/{len(examples)} = {correct / len(examples):.1%}")

# %% [markdown]
# ## 7. Inspect errors by example
#
# Error review helps determine whether the problem is the label policy, prompt, context, or
# model. Do not tune and report performance on the same examples as if they were held out.

# %%
errors = [
    {"text": row["text"], "gold": row["gold"], "predicted": pred}
    for row, pred in zip(examples, predictions) if row["gold"] != pred
]
pprint(errors)
print("Error count:", len(errors))

# %% [markdown]
# ## 8. Optional live Jev request
#
# Uses POST https://jevmodel.org/v1/systemone and Python's standard library. Disabled unless
# you explicitly call run_live_jev after setting JEVMODEL_API_KEY. A successful request may
# incur usage charges. Verify current limits, pricing, model availability, and response
# semantics before production use.

# %%
JEV_ENDPOINT = "https://jevmodel.org/v1/systemone"

def run_live_jev(state, questions=None, timeout_seconds=5):
    api_key = os.environ.get("JEVMODEL_API_KEY")
    if not api_key:
        raise RuntimeError("Set JEVMODEL_API_KEY in your environment or Colab Secrets first.")
    body = {
        "model": "jev-latest",
        "state": state,
        "questions": questions or {"intent": intent_question},
    }
    request = urllib.request.Request(
        JEV_ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"Jev HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Jev request failed or timed out: {exc}") from exc
    if not isinstance(result, dict) or not isinstance(result.get("answers"), dict):
        raise ValueError("Unexpected Jev response: missing answers object")
    return result

# %%
# Opt in by uncommenting after setting JEVMODEL_API_KEY. Do not loop over the dataset casually.
# live_result = run_live_jev(example_state)
# pprint(live_result)

# %% [markdown]
# ## 9. Make routing deterministic
#
# Thresholds below are illustrative policy values, not universal Jev cutoffs. Tune them on a
# validation set using the relative costs of false positives, false negatives, clarification,
# and handoff. A model answer is evidence, not authorization to perform an action.

# %%
def choose_next_step(intent, needs_clarification, human_handoff, urgency):
    if human_handoff >= 0.80:
        return "human_handoff"
    if urgency >= 3.0:
        return "approved_safety_workflow"
    if needs_clarification >= 0.50 or intent == "other_or_unclear":
        return "ask_one_clarifying_question"
    routes = {
        "schedule_service": "booking_workflow",
        "reschedule_service": "appointment_lookup_then_reschedule",
        "cancel_service": "cancellation_workflow_with_policy_checks",
        "appointment_status": "appointment_status_lookup",
        "pricing_or_service_question": "answer_or_information_workflow",
        "existing_job_followup": "existing_job_workflow",
        "emergency_or_safety": "approved_safety_workflow",
        "human_agent_request": "human_handoff",
    }
    return routes.get(intent, "ask_one_clarifying_question")

for demo in [
    ("schedule_service", 0.05, 0.01, 0.0),
    ("other_or_unclear", 0.82, 0.02, 0.0),
    ("emergency_or_safety", 0.01, 0.01, 3.0),
    ("appointment_status", 0.01, 0.91, 0.0),
]:
    print(demo, "->", choose_next_step(*demo))

# %% [markdown]
# ## 10. Evaluation plan and exercises
#
# Before a production pilot:
# - Adjudicate labels using a written inclusion/exclusion policy.
# - Split by call/session into development, validation, and untouched test sets.
# - Report per-class precision/recall, macro-F1, confusion matrix, clarification rate,
#   human-handoff recall, and safety-case false negatives.
# - Inspect errors by language, transcription quality, interruptions, and context type.
# - Compare against the current baseline in shadow mode before routing on outputs.
# - Measure end-to-end p50/p95/p99, timeout rate, cost per decision, and downstream outcomes.
# - Version taxonomy, instructions, criteria, model, and thresholds together.
#
# **Exercise A:** Rewrite instructions to define which action wins when a caller asks to cancel
# and reschedule in the same utterance.
#
# **Exercise B:** Add five overlapping-intent examples and explain the strongest alternative.
#
# **Exercise C:** Change one criterion at a time and test whether the target error decreases
# without increasing a more costly error on a held-out set.
#
# **Exercise D:** Implement and test timeout and invalid-label fallbacks without live API calls.
#
# **Exercise E:** Choose thresholds from a cost matrix, including the cost of missed human
# requests and unnecessary handoffs.
#
# ## Key takeaways
#
# - Ask for a decision, not an essay.
# - Put the complete question in instructions; the question ID is just a key.
# - Define the answer space with explicit criteria and an other/unclear path.
# - Evaluate with reviewed labels and error analysis; prompt quality is empirical.
# - Treat probabilities as model outputs, not authorization.
# - The orchestrator validates, applies policy, and owns tools and side effects.

# %% [markdown]
# ## Check your understanding
#
# 1. Why must the complete decision live in `instructions` rather than the question ID?
# 2. Why is `other_or_unclear` safer than forcing every caller turn into a supported workflow?
# 3. Which routing decision in `choose_next_step` is deliberately deterministic rather than model-owned?
#
# **Graded exercise:** Add an overlapping-intent case and an invalid-label fallback. Show with
# offline assertions that the fallback asks one clarification rather than selecting a booking,
# cancellation, or emergency workflow.
