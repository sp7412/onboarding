import json
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "labs"))

from stlab.autonomy import (  # noqa: E402
    LEVEL_TARGETS, calibration, cost_threshold, drift_guard, hidden_regression_example, promotion_policy, psi,
    segment_levels, sprt, sprt_stopping_n, wilson_interval, wilson_upper,
)


class AutonomyTests(unittest.TestCase):
    def test_wilson_known_values(self):
        self.assertAlmostEqual(wilson_upper(0, 100), 0.0370, places=4)
        lo, hi = wilson_interval(10, 100)
        self.assertAlmostEqual(lo, 0.0552, places=3)
        self.assertAlmostEqual(hi, 0.1744, places=3)
        self.assertEqual(wilson_interval(0, 0), (0.0, 1.0))

    def test_promotion_needs_samples_and_a_bound(self):
        self.assertEqual(promotion_policy(0, 20, 0, min_samples=100).decision, "hold")
        self.assertEqual(promotion_policy(0, 300, 0).decision, "promote")
        self.assertEqual(promotion_policy(3, 120, 2).decision, "hold")   # 2.5% but too few samples

    def test_no_demotion_for_lack_of_evidence(self):
        # 1.1% observed at level 3 with a small sample: the upper bound is above 2%,
        # but nothing shows the agent is worse than the 5% this level required.
        self.assertEqual(promotion_policy(2, 182, 3).decision, "hold")

    def test_demotion_on_evidence(self):
        d = promotion_policy(50, 600, 3)
        self.assertEqual((d.decision, d.level), ("demote", 2))
        self.assertGreater(d.lower_bound, 0.05)

    def test_shared_cases_match_site_lesson(self):
        # The site's earned-autonomy lesson re-implements this policy in TypeScript and checks
        # itself against the same file, so both must agree with these published numbers.
        path = Path(__file__).resolve().parents[1] / "labs" / "data" / "autonomy-cases.json"
        doc = json.loads(path.read_text())
        for c in doc["cases"]:
            d = promotion_policy(c["errors"], c["n"], c["level"], min_samples=doc["minSamples"])
            self.assertEqual(d.decision, c["decision"], c["name"])
            self.assertAlmostEqual(d.lower_bound, c["lower"], places=5, msg=c["name"])
            self.assertAlmostEqual(d.upper_bound, c["upper"], places=5, msg=c["name"])
            self.assertEqual(LEVEL_TARGETS[c["level"]], c["promoteTarget"])
            self.assertEqual(LEVEL_TARGETS[c["level"] - 1], c["keepTarget"])
        ex = doc["exercise9"]
        self.assertAlmostEqual(cost_threshold(180, 350), ex["costThreshold"], places=5)
        self.assertAlmostEqual(psi([0.5, 0.3, 0.15, 0.05], [0.38, 0.27, 0.15, 0.20]), ex["psi"], places=5)

    def test_sprt(self):
        self.assertEqual(sprt(0, 1000), "promote")
        self.assertEqual(sprt(200, 200), "demote")
        self.assertEqual(sprt(1, 10), "continue")
        decision, n = sprt_stopping_n([0] * 500)
        self.assertEqual(decision, "promote")
        self.assertLess(n, 200)

    def test_cost_threshold(self):
        self.assertAlmostEqual(cost_threshold(1500, 300), 1500 / 1800)
        with self.assertRaises(ValueError):
            cost_threshold(0, 0)

    def test_calibration_bins_partition_the_data(self):
        probs = [0.05, 0.15, 0.55, 0.95, 1.0, 1.0]
        rows, ece = calibration(probs, [0, 0, 1, 1, 1, 1])
        self.assertEqual(sum(n for _, _, n in rows), len(probs))
        perfect, _ = calibration([1.0] * 4, [1] * 4)
        self.assertEqual(perfect, [(1.0, 1.0, 4)])
        self.assertAlmostEqual(calibration([1.0] * 4, [1] * 4)[1], 0.0)
        self.assertGreater(ece, 0)

    def test_drift_guard_stable_does_not_pause(self):
        rng = np.random.default_rng(1)
        train = rng.normal(0, 1, (600, 4))
        mix = [0.55, 0.25, 0.12, 0.08]
        stable = drift_guard(mix, [0.56, 0.24, 0.12, 0.08], train, rng.normal(0, 1, (300, 4)))
        self.assertFalse(stable["pause"], stable)

    def test_drift_guard_pauses_on_shift(self):
        rng = np.random.default_rng(1)
        train = rng.normal(0, 1, (600, 4))
        mix = [0.55, 0.25, 0.12, 0.08]
        ood = drift_guard(mix, mix, train, rng.normal(1.5, 1.3, (300, 4)))
        self.assertTrue(ood["pause"])
        self.assertIn("out of distribution", ood["reason"])
        shifted = drift_guard(mix, [0.30, 0.15, 0.20, 0.35], train, rng.normal(0, 1, (300, 4)))
        self.assertTrue(shifted["pause"])
        self.assertGreater(psi(mix, [0.30, 0.15, 0.20, 0.35]), 0.25)

    def test_per_segment_levels(self):
        out = segment_levels({"good": (1, 500), "bad": (100, 500)}, levels={"good": 3, "bad": 3})
        self.assertEqual(out["good"].decision, "promote")
        self.assertEqual(out["bad"].decision, "demote")

    def test_hidden_regression_example(self):
        ex = hidden_regression_example()
        self.assertGreater(ex["new"]["aggregate"], ex["old"]["aggregate"])
        self.assertLess(ex["new"]["hard"], ex["old"]["hard"])


if __name__ == "__main__":
    unittest.main()
