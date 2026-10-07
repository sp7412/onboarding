import unittest

from labs.stlab.calls import generate_calls, load_calls


class TestCallsDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calls = load_calls()

    def test_determinism_by_seed(self):
        self.assertEqual(generate_calls(40, seed=7), generate_calls(40, seed=7))
        self.assertNotEqual(generate_calls(40, seed=7), generate_calls(40, seed=8))

    def test_schema_validity(self):
        self.assertEqual(len(self.calls), 400)
        required = {
            "call_id", "channel", "time_of_day", "after_hours", "trade", "season",
            "scenario", "transcript", "intent", "job_type", "urgency", "emergency",
            "bookable", "bookable_reason", "caller_sentiment", "replacement_interest",
            "membership", "price_shopper", "injection_attempt", "outcome",
        }
        for row in self.calls:
            self.assertTrue(required <= row.keys())
            self.assertTrue(row["transcript"])
            self.assertIn(row["outcome"]["booked"], (True, False))

    def test_label_consistency(self):
        for row in self.calls:
            if row["emergency"]:
                self.assertFalse(row["bookable"])
                self.assertFalse(row["outcome"]["booked"])
            if row["outcome"]["booked"]:
                self.assertTrue(row["bookable"])

    def test_class_balance_bounds(self):
        counts = {}
        for row in self.calls:
            counts[row["scenario"]] = counts.get(row["scenario"], 0) + 1
        self.assertGreaterEqual(counts["routine"], 80)
        self.assertGreaterEqual(counts["no_cool_heatwave"], 35)
        self.assertGreaterEqual(counts["member_tuneup"], 20)
        emergency = sum(row["emergency"] for row in self.calls)
        self.assertGreaterEqual(emergency, 25)
        self.assertLessEqual(emergency, 70)
        self.assertGreaterEqual(counts["injection"], 8)

    def test_snapshot_matches_generator(self):
        self.assertEqual(self.calls, generate_calls(400, seed=7))


if __name__ == "__main__":
    unittest.main()
