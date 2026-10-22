# %% [markdown]
# # Lab 20 — Full-duplex interaction evaluation and regression log
#
# Use this after Lab 19 has a real browser conversation working. This notebook creates a small, repeatable manual test set and a local CSV log.
#
# It does not fabricate model metrics or automate human audio judgments. Record timestamps at defined boundaries, include failures, and separate subjective ratings from measured latency. Do not enter customer/company data or save audio recordings.
#
# For this pilot, collect at least 20 valid observations per latency metric before reporting p50/p95. Keep model revision, environment, browser, and test conditions with each run.

# %%
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import csv, json, platform, sys

WORK_DIR = Path.home() / "moshi-demo"
RESULTS_DIR = WORK_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
print("Results:", RESULTS_DIR)
print("OS:", platform.platform(), "| Python:", sys.version.split()[0])

# %%
SCENARIOS = [
    {"id": "basic-01", "category": "basic_exchange",
     "prompt": "I need to schedule a fictional furnace inspection next Tuesday.",
     "expected": "Intelligible response and relevant follow-up."},
    {"id": "pause-01", "category": "natural_pause",
     "prompt": "Say: I need to check... [pause about 2 seconds] ...whether Tuesday works.",
     "expected": "Does not repeatedly mistake the natural pause for a final turn."},
    {"id": "barge-01", "category": "barge_in",
     "prompt": "Interrupt the assistant mid-sentence with: Actually, stop.",
     "expected": "Assistant yields promptly; no false completion claim."},
    {"id": "overlap-01", "category": "overlap",
     "prompt": "Speak a short correction while the assistant is mid-sentence.",
     "expected": "Correction is noticed; observe confusion or loss."},
    {"id": "noise-01", "category": "false_interrupt",
     "prompt": "Pause briefly, then make a quiet non-speech noise.",
     "expected": "Noise does not consistently trigger an inappropriate turn."},
    {"id": "recover-01", "category": "recovery",
     "prompt": "Reload the local page and start a new short exchange.",
     "expected": "Session recovers or failure is diagnosable."},
]
for item in SCENARIOS:
    print(f"{item['id']} [{item['category']}]: {item['expected']}")

# %%
FIELDS = [
    "timestamp_utc", "run_id", "scenario_id", "model_repo_or_revision",
    "machine_backend", "browser", "network_notes", "outcome",
    "turn_latency_ms", "stop_latency_ms", "intelligibility_1_to_5",
    "interruption_handled", "notes",
]
CSV_PATH = RESULTS_DIR / "full_duplex_observations.csv"
if not CSV_PATH.exists():
    with CSV_PATH.open("w", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writeheader()
print("Observation log:", CSV_PATH)
print("Turn latency: end of user speech to first assistant audio.")
print("Stop latency: user interruption onset to assistant audio stopping.")

# %%
observation = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "run_id": "pilot-001",
    "scenario_id": "basic-01",
    "model_repo_or_revision": "record exact repo/revision or model ID",
    "machine_backend": "record chip + MLX version",
    "browser": "record browser/version",
    "network_notes": "localhost; no tunnel",
    "outcome": "not_run",  # pass / fail / not_run
    "turn_latency_ms": "",
    "stop_latency_ms": "",
    "intelligibility_1_to_5": "",
    "interruption_handled": "",
    "notes": "Replace this template with an actual observation.",
}
APPEND_OBSERVATION = False
if APPEND_OBSERVATION:
    if observation["scenario_id"] not in {s["id"] for s in SCENARIOS}:
        raise ValueError("scenario_id must be in the declared scenario set")
    with CSV_PATH.open("a", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(observation)
    print("Appended observation.")
else:
    print("No row written. Edit the template and set APPEND_OBSERVATION=True.")

# %%
def percentile(values, p):
    values = sorted(values)
    if not values:
        return None
    pos = (len(values) - 1) * p
    lo, hi = int(pos), min(int(pos) + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (pos - lo)

with CSV_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))

for field in ("turn_latency_ms", "stop_latency_ms"):
    values = []
    for row in rows:
        try:
            value = float(row[field])
            if value >= 0:
                values.append(value)
        except (ValueError, TypeError):
            pass
    print(f"\n{field}: n={len(values)}")
    if len(values) < 20:
        print("Insufficient observations for p50/p95 (pilot minimum: 20).")
    else:
        print("p50:", round(percentile(values, 0.50), 1), "ms")
        print("p95:", round(percentile(values, 0.95), 1), "ms")

# %%
with CSV_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))
counts = Counter(row.get("scenario_id", "") + ":" + row.get("outcome", "")
                 for row in rows)
print("Scenario outcome counts:")
for key, count in sorted(counts.items()):
    print(f"  {key}: {count}")

manifest = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "scenario_ids": [s["id"] for s in SCENARIOS],
    "observation_count": len(rows),
    "csv_path": str(CSV_PATH),
    "limitations": [
        "Manual test; browser audio judgments are not automatically graded.",
        "Latency is valid only when timestamps follow the documented boundaries.",
        "No claim of production reliability or concurrent-call capacity.",
    ],
}
manifest_path = RESULTS_DIR / "evaluation-manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
print("Wrote:", manifest_path)

