import unittest
import numpy as np

from labs.stlab.autonomy import (
    wilson_upper, promotion_policy, sprt, drift_guard, segment_levels,
)


class TestAutonomy(unittest.TestCase):
    def test_wilson_known_value(self):
        self.assertAlmostEqual(wilson_upper(0, 100), 0.03699, places=3)
        self.assertGreater(wilson_upper(10, 100), 0.10)

    def test_sprt_synthetic_streams(self):
        self.assertEqual(sprt(0, 1000, p0=0.02, p1=0.05), "promote")
        self.assertEqual(sprt(200, 200, p0=0.02, p1=0.05), "demote")

    def test_promotion_requires_minimum_sample(self):
        decision = promotion_policy(0, 20, 0, min_samples=100)
        self.assertEqual(decision.decision, "hold")

    def test_demotion_fires_on_drift(self):
        train = np.zeros((100, 4))
        train[:, 0] = np.linspace(0, 1, 100)
        current = np.ones((20, 4)) * 10
        result = drift_guard([0.8, 0.1, 0.08, 0.02], [0.4, 0.3, 0.2, 0.1],
                             train, current)
        self.assertTrue(result["pause"])

    def test_per_segment_levels(self):
        out = segment_levels({"good": (1, 500), "bad": (100, 500)},
                             levels={"good": 3, "bad": 3})
        self.assertEqual(out["good"].decision, "promote")
        self.assertEqual(out["bad"].decision, "demote")


if __name__ == "__main__":
    unittest.main()
