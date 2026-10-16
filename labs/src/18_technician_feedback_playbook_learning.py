# %% [markdown]
# # 18 · Technician feedback to safer playbook revisions
#
# **Goal:** build a small, reproducible learning loop for the illustrative *AC not cooling* playbook. A technician reports a missing diagnostic step; the system gathers evidence, proposes a scoped revision, evaluates it on historical cases, and waits for human approval before any release.
#
# This is a **synthetic teaching simulation**, not HVAC service guidance. The simulated “additional check” below is an abstract diagnostic coverage marker—not an instruction to perform a real-world procedure. Real technical steps must come from approved manufacturer documentation and qualified reviewers.
#
# ## You will
#
# 1. create structured technician-feedback events while preserving unknowns;
# 2. distinguish repeated signals from verified evidence;
# 3. draft a versioned, scoped candidate revision;
# 4. compare the current and candidate playbooks on held-out synthetic cases;
# 5. apply hard safety and technical approval gates;
# 6. simulate a limited pilot and define rollback criteria.
#
# **Learning objective:** the model can recommend and prepare changes, but it cannot approve or publish operational guidance.

# %% [markdown]
# ## 1. Imports and reproducibility
#
# Use only the Python standard library so the notebook can run in a basic Codespace or local Python environment.

# %%
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from statistics import mean
import json
import random
import uuid

SEED = 20261015
rng = random.Random(SEED)
print("Seed:", SEED)

# %% [markdown]
# ## 2. Define the feedback contract
#
# The initial report below intentionally has no technician details and no evidence. Missing values remain `None`; the system must not infer the missing diagnostic step from the category alone.

# %%
feedback = {
    "feedback_id": str(uuid.uuid4()),
    "feedback_type": "playbook_defect",
    "category": "missing_diagnostic_step",
    "status": "needs_evidence",
    "source": {
        "technician_id": None,
        "submitted_at": None
    },
    "context": {
        "job_id": None,
        "equipment_id": None,
        "symptom": "AC not cooling",
        "playbook_id": "ac-not-cooling",
        "playbook_version": "1.4",
        "step_id": None
    },
    "observation": {
        "original_text": None,
        "expected_step": None,
        "reason_step_was_needed": None
    },
    "evidence": {
        "diagnostic_findings": [],
        "repair_outcome": None,
        "callback_within_window": None
    }
}
print(json.dumps(feedback, indent=2))
assert feedback["source"]["technician_id"] is None
assert feedback["observation"]["expected_step"] is None

# %% [markdown]
# ### Exercise A — what should happen next?
#
# Before running the next cell, decide what the system may safely do with this report. It may ask a targeted follow-up and link permitted job evidence. It may not name a missing check, assert a root cause, or modify the published playbook.

# %%
def triage_feedback(event):
    required_for_review = [
        event["context"]["playbook_version"],
        event["observation"]["original_text"],
        event["observation"]["expected_step"],
        event["observation"]["reason_step_was_needed"],
    ]
    if not all(required_for_review):
        return {
            "status": "needs_evidence",
            "next_question": (
                "What check was missing, when would it apply, "
                "and what did it help establish?"
            ),
            "may_publish": False,
        }
    return {
        "status": "ready_for_technical_review",
        "next_question": None,
        "may_publish": False,
    }

triage_feedback(feedback)

# %% [markdown]
# ## 3. Generate synthetic cases
#
# We create 240 fictional historical cases. The candidate change is a hypothetical additional diagnostic checkpoint relevant only to one equipment/configuration cohort. A latent label indicates whether the checkpoint would have helped clarify the diagnosis. These labels are synthetic ground truth for evaluation—not real HVAC rules.
#
# We deliberately split cases into a **proposal-development set** and a **held-out evaluation set**. Never tune the candidate on the held-out results and then report those same results as independent validation.

# %%
cases = []
for i in range(240):
    cohort = "configuration_B" if rng.random() < 0.35 else "other"
    # Synthetic label: whether the abstract checkpoint is relevant.
    useful = cohort == "configuration_B" and rng.random() < 0.70
    baseline_covered = not useful
    cases.append({
        "case_id": f"case-{i:03d}",
        "cohort": cohort,
        "baseline_covered": baseline_covered,
        "candidate_would_cover": useful,
        "safe": True,
        "outcome_observed": rng.random() < 0.92,
    })

rng.shuffle(cases)
development = cases[:120]
heldout = cases[120:]
print("Development cases:", len(development))
print("Held-out cases:", len(heldout))
print("Held-out cohort counts:", dict(Counter(c["cohort"] for c in heldout)))

# %% [markdown]
# ## 4. Cluster feedback, but do not confuse frequency with proof
#
# Create synthetic reports about the same possible gap plus counterexamples. In production, clustering would use structured attributes and possibly semantic similarity; each cluster still needs evidence review. The purpose here is to show how recurrence prioritizes investigation, not automatically validates the proposal.

# %%
reports = [
    {"id": "fb-001", "cohort": "configuration_B", "category": "missing_diagnostic_step", "evidence_complete": True, "supports_candidate": True},
    {"id": "fb-002", "cohort": "configuration_B", "category": "missing_diagnostic_step", "evidence_complete": True, "supports_candidate": True},
    {"id": "fb-003", "cohort": "configuration_B", "category": "missing_diagnostic_step", "evidence_complete": False, "supports_candidate": None},
    {"id": "fb-004", "cohort": "other", "category": "missing_diagnostic_step", "evidence_complete": True, "supports_candidate": False},
    {"id": "fb-005", "cohort": "configuration_B", "category": "missing_diagnostic_step", "evidence_complete": True, "supports_candidate": True},
]

clusters = defaultdict(list)
for report in reports:
    clusters[(report["category"], report["cohort"])].append(report)

for key, items in clusters.items():
    complete = [r for r in items if r["evidence_complete"]]
    support = sum(r["supports_candidate"] is True for r in complete)
    contradict = sum(r["supports_candidate"] is False for r in complete)
    print(key, {
        "reports": len(items),
        "evidence_complete": len(complete),
        "supporting": support,
        "contradicting": contradict,
        "disposition": "review evidence" if complete else "request evidence",
    })

# %% [markdown]
# ## 5. Draft a revision proposal
#
# A proposal must specify applicability, rationale, evidence, counterevidence, and the exact base version. This simulation's proposed step is intentionally abstract. Replace it with real, approved technical wording only in a production workflow after subject-matter review.

# %%
proposal = {
    "revision_id": "ac-not-cooling-v1.5-candidate",
    "base_version": "1.4",
    "candidate_version": "1.5-candidate",
    "change_type": "diagnostic_step",
    "proposed_text": (
        "[PLACEHOLDER] Add an approved diagnostic checkpoint "
        "for the applicable equipment/configuration cohort."
    ),
    "applicability": {"cohort": "configuration_B"},
    "rationale": "Recurring evidence-linked reports suggest a scoped coverage gap.",
    "supporting_feedback_ids": ["fb-001", "fb-002", "fb-005"],
    "contradicting_feedback_ids": ["fb-004"],
    "evidence_reviewed": False,
    "technical_approval": False,
    "safety_approval": False,
    "publication_approval": False,
}
print(json.dumps(proposal, indent=2))

# %% [markdown]
# ## 6. Evaluate the candidate on held-out cases
#
# We measure whether the abstract candidate covers cases that the baseline missed. This is only a **coverage metric**; it does not establish real diagnostic correctness, safety, reduced callbacks, or better repairs. Those require expert-labelled scenarios and field outcome data.
#
# A candidate must also pass hard gates. A strong score cannot compensate for a safety failure or missing required approval.

# %%
def coverage_rate(rows, use_candidate=False):
    if not rows:
        return 0.0
    covered = 0
    for row in rows:
        baseline = row["baseline_covered"]
        candidate_applies = (
            use_candidate
            and row["cohort"] == proposal["applicability"]["cohort"]
        )
        covered += bool(baseline or (candidate_applies and row["candidate_would_cover"]))
    return covered / len(rows)

baseline = coverage_rate(heldout)
candidate = coverage_rate(heldout, use_candidate=True)
improvement_pp = (candidate - baseline) * 100
print(f"Baseline coverage:  {baseline:.1%}")
print(f"Candidate coverage: {candidate:.1%}")
print(f"Change:              {improvement_pp:+.1f} percentage points")

# Inspect cohort-specific results to ensure the change is scoped.
for cohort in sorted({r["cohort"] for r in heldout}):
    subset = [r for r in heldout if r["cohort"] == cohort]
    print(cohort, {
        "n": len(subset),
        "baseline": round(coverage_rate(subset), 3),
        "candidate": round(coverage_rate(subset, use_candidate=True), 3),
    })

# %% [markdown]
# ### Exercise B — add negative and safety tests
#
# Add at least three cases where the candidate must **not** apply: an unrelated equipment cohort, insufficient evidence, and a scenario where the proposed step conflicts with approved guidance. The final scenario should fail a hard gate regardless of coverage improvement.

# %%
test_cases = [
    {"name": "unrelated cohort", "applies": False, "evidence_sufficient": True, "safety_ok": True},
    {"name": "insufficient evidence", "applies": True, "evidence_sufficient": False, "safety_ok": True},
    {"name": "conflicts with approved guidance", "applies": True, "evidence_sufficient": True, "safety_ok": False},
]

for case in test_cases:
    eligible = case["applies"] and case["evidence_sufficient"] and case["safety_ok"]
    print(case["name"], "eligible_for_pilot =", eligible)

# %% [markdown]
# ## 7. Enforce approval gates
#
# The approval function should fail closed. The candidate is not publishable just because the evaluation metric improved. All required gates must pass and the exact proposed diff must be approved by an authorized owner.

# %%
def release_decision(proposal, evaluation_passed):
    gates = {
        "evidence_reviewed": proposal["evidence_reviewed"],
        "technical_approval": proposal["technical_approval"],
        "safety_approval": proposal["safety_approval"],
        "evaluation_passed": evaluation_passed,
        "publication_approval": proposal["publication_approval"],
    }
    return {
        "decision": "pilot_eligible" if all(gates.values()) else "blocked",
        "gates": gates,
        "failed_gates": [name for name, passed in gates.items() if not passed],
    }

release_decision(proposal, evaluation_passed=(candidate >= baseline))

# %% [markdown]
# ## 8. Simulate the authorized pilot and rollback policy
#
# Only after reviewers approve the exact revision should a limited pilot begin. In a real deployment, define sample size, duration, minimum detectable effect, segmentation, and guardrails before rollout. Roll back on safety incidents or material regression; do not wait for statistical significance to respond to a credible safety concern.

# %%
pilot_policy = {
    "max_initial_traffic_fraction": 0.05,
    "minimum_reviewed_cases": 30,
    "rollback_on_safety_incident": True,
    "rollback_if_callback_rate_worsens": True,
    "owner": "designated_playbook_owner",
    "rollback_target": "1.4",
}
print(json.dumps(pilot_policy, indent=2))

# %% [markdown]
# ## 9. Export a review packet
#
# A reviewer should receive the proposal, exact base version, feedback links, supporting and contradicting evidence, evaluation results, unresolved questions, and rollout/rollback plan. This cell creates a compact in-memory packet; a production system would persist it with access controls and an audit trail.

# %%
review_packet = {
    "proposal": proposal,
    "evaluation": {
        "heldout_n": len(heldout),
        "baseline_coverage": round(baseline, 4),
        "candidate_coverage": round(candidate, 4),
        "coverage_change_percentage_points": round(improvement_pp, 2),
        "warning": "Synthetic coverage metric only; not proof of HVAC correctness or safety."
    },
    "approval_gates": release_decision(
        proposal, evaluation_passed=(candidate >= baseline)
    ),
    "pilot_policy": pilot_policy,
}
print(json.dumps(review_packet, indent=2))

# %% [markdown]
# ## 10. Debrief and acceptance checklist
#
# Mark the simulation complete only when you can explain and demonstrate:
#
# - [ ] Unknown technician details remain unknown; the model does not invent the missing step.
# - [ ] Every report is linked to a job and exact playbook version when available.
# - [ ] Similar reports are clustered, and counterexamples remain visible.
# - [ ] The candidate revision is scoped to an explicit applicability condition.
# - [ ] Evaluation uses held-out cases and reports limitations of the synthetic metric.
# - [ ] Safety and technical approval are hard gates, not weighted score components.
# - [ ] Publication is blocked until the exact revision is approved.
# - [ ] The pilot has predefined guardrails, monitoring, and rollback criteria.
# - [ ] Rejected proposals and observed outcomes are retained for future evaluation.
#
# **Stretch goals:** replace the synthetic records with a richer fixture; add a false-positive feedback cluster; simulate callback outcomes with confounders; add a reviewer decision schema; or compare two candidate revisions while keeping the evaluation set fixed.
#
# **Takeaway:** this is a controlled data-and-evaluation loop, not automatic self-editing. The AI proposes; evidence tests; authorized people approve; field outcomes close the loop.

# %% [markdown]
# ## Check your understanding
#
# 1. Why is a technician's report a signal rather than proof that a proposed step is correct?
# 2. Which evaluation and approval gates must pass before a candidate playbook revision can be released?
# 3. Why should a pilot define rollback criteria before rollout?
#
# **Graded exercise:** produce a review packet for the synthetic missing-step report, including preserved unknowns, evidence requirements, evaluation results, explicit approval gates, and pilot rollback criteria.
