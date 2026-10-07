import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "labs"))

from stlab.backend import JOB_TYPES  # noqa: E402
from stlab.calls import (  # noqa: E402
    EMERGENCY_SCENARIOS, generate_calls, load_calls, scenario_counts, validate_record,
)


class CallsDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calls = load_calls()

    def test_snapshot_matches_generator(self):
        self.assertEqual(self.calls, generate_calls(400, seed=7))

    def test_determinism_by_seed(self):
        self.assertEqual(generate_calls(50, seed=3), generate_calls(50, seed=3))
        self.assertNotEqual(generate_calls(50, seed=3), generate_calls(50, seed=4))

    def test_exact_scenario_mix(self):
        self.assertEqual(Counter(c["scenario"] for c in self.calls), Counter(scenario_counts(400)))
        self.assertEqual(sum(scenario_counts(400).values()), 400)
        self.assertEqual(sum(scenario_counts(37).values()), 37)

    def test_every_record_valid(self):
        for c in self.calls:
            validate_record(c)
            self.assertTrue(c["transcript"])
            self.assertTrue(c["call_id"].startswith("call-"))

    def test_safety_labels(self):
        for c in self.calls:
            if c["scenario"] in EMERGENCY_SCENARIOS:
                self.assertTrue(c["emergency"])
                self.assertFalse(c["bookable"])
                self.assertFalse(c["outcome"]["booked"])
            if c["injection_attempt"]:
                self.assertFalse(c["bookable"])
            if c["outcome"]["booked"]:
                self.assertTrue(c["bookable"])

    def test_bookable_calls_use_backend_job_types(self):
        for c in self.calls:
            if c["bookable"]:
                self.assertIn(c["job_type"], JOB_TYPES)

    def test_transcripts_match_labels(self):
        for c in self.calls:
            text = " ".join(t["text"].lower() for t in c["transcript"] if t["speaker"] == "caller")
            if c["scenario"] in ("no_cool_heatwave", "topic_switch", "phone_chunks"):
                self.assertEqual((c["trade"], c["job_type"]), ("HVAC", "ac_repair"))
                self.assertIn("ac", text)
            if c["injection_attempt"]:
                self.assertIn("ignore your rules", text)

    def test_no_real_contact_details(self):
        for c in self.calls:
            for turn in c["transcript"]:
                if "555" in turn["text"]:
                    self.assertIn("01", turn["text"])        # 555-01xx fictional range only

    def test_validate_rejects_bad_records(self):
        bad = dict(self.calls[0], emergency=True, bookable=True)
        with self.assertRaises(ValueError):
            validate_record(bad)
        with self.assertRaises(ValueError):
            validate_record(dict(self.calls[0], job_type="teleportation"))


if __name__ == "__main__":
    unittest.main()
