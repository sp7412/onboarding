import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labs"))

import jsonschema  # noqa: E402

from stlab.calls import load_calls  # noqa: E402
from stlab.minimax import (  # noqa: E402
    ERROR_TYPES, Evidence, claim_guard, decide_bookability, error_sensitivity,
    extract_call_facts, facts_to_ledger, floor_sweep, gold_action, inject_error, run_call,
    validate_call_facts,
)

SCHEMA = json.loads((ROOT / "labs/data/schemas/call-facts.schema.json").read_text())


class MiniMaxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calls = load_calls()
        cls.emergencies = [c for c in cls.calls if c["emergency"]]

    def test_facts_match_json_schema(self):
        for c in self.calls[:60]:
            for noise in (0.0, 0.3):
                jsonschema.validate(extract_call_facts(c, noise, seed=1).as_dict(), SCHEMA)

    def test_gold_actions_match_labels(self):
        for c in self.calls:
            self.assertEqual(gold_action(c) == "book", c["bookable"], c["call_id"])

    def test_emergencies_never_booked_even_when_extractor_misses_them(self):
        for c in self.emergencies:
            missed = inject_error(extract_call_facts(c), "emergency_missed")
            self.assertTrue(missed.values()["bookable"])
            result = run_call(c, facts=missed)
            self.assertEqual(result["decision"].action, "transfer")
            self.assertFalse(result["committed"])
        rows = {r["error_type"]: r for r in error_sensitivity(self.calls)}
        self.assertEqual(rows["emergency_missed"]["emergencies_booked"], 0)
        unscreened = {r["error_type"]: r for r in error_sensitivity(self.calls, transcript_screen=False)}
        self.assertEqual(unscreened["emergency_missed"]["emergencies_booked"], len(self.emergencies))

    def test_no_false_booking_claims_and_idempotent_commits(self):
        for c in self.calls[:80]:
            r = run_call(c, noise=0.2, seed=5)
            self.assertFalse(r["false_claim"], c["call_id"])
            if r["committed"]:
                self.assertTrue(r["idempotent_retry"])
                self.assertIsNotNone(r["assigned_tech"])
            else:
                self.assertIsNone(r["assigned_tech"])        # no dispatch without a commit

    def test_injection_is_transferred(self):
        for c in (c for c in self.calls if c["injection_attempt"]):
            self.assertEqual(decide_bookability(extract_call_facts(c), c).action, "transfer")

    def test_claim_guard(self):
        self.assertTrue(claim_guard("You're booked.", committed=True))
        self.assertFalse(claim_guard("You're booked.", committed=False))
        self.assertFalse(claim_guard("You're booked.", committed=True, emergency=True))
        self.assertTrue(claim_guard("I'm transferring you to a person now.", committed=False, transferred=True))
        self.assertFalse(claim_guard("I'm transferring you to a person now.", committed=False))

    def test_low_confidence_critical_field_sends_to_person(self):
        facts = extract_call_facts(self.calls[0])
        facts.fields["intent"] = Evidence("book_service", 0.40, facts.fields["intent"].evidence)
        ok, errors = validate_call_facts(facts, 0.85)
        self.assertFalse(ok)
        self.assertIn("low_confidence:intent", errors)
        self.assertEqual(decide_bookability(facts, self.calls[0]).action, "callback")

    def test_low_confidence_noncritical_field_is_ignored_not_fatal(self):
        c = next(c for c in self.calls if c["bookable"] and c["urgency"] == "same_day")
        facts = extract_call_facts(c)
        facts.fields["urgency"] = Evidence("same_day", 0.40, facts.fields["urgency"].evidence)
        self.assertTrue(validate_call_facts(facts, 0.85)[0])
        self.assertNotIn("urgency", facts.trusted(0.85))

    def test_conflicts_are_rejected(self):
        facts = inject_error(extract_call_facts(self.calls[0]), "conflicting_facts")
        ok, errors = validate_call_facts(facts)
        self.assertFalse(ok)
        self.assertIn("conflict:job_type", errors)

    def test_ledger_verifies_only_trusted_facts(self):
        c = self.calls[0]
        facts = extract_call_facts(c)
        facts.fields["urgency"] = Evidence("same_day", 0.40, facts.fields["urgency"].evidence)
        ledger = facts_to_ledger(facts, 0.85)
        self.assertIn("urgency", ledger.view(c["call_id"], min_status="proposed"))
        self.assertNotIn("urgency", ledger.view(c["call_id"]))

    def test_error_sensitivity_covers_every_error_type(self):
        rows = error_sensitivity(self.calls[:50])
        self.assertEqual([r["error_type"] for r in rows], list(ERROR_TYPES))
        wrong_job = next(r for r in rows if r["error_type"] == "job_type_wrong")
        self.assertEqual(wrong_job["decisions_changed"], 0)
        self.assertGreater(wrong_job["wrong_bookings"], 0)

    def test_floor_sweep_trades_automation_for_errors(self):
        rows = floor_sweep(self.calls, [0.5, 0.7, 0.95])
        self.assertGreater(rows[0]["automation_rate"], rows[-1]["automation_rate"])
        self.assertGreaterEqual(rows[0]["wrong_bookings"], rows[-1]["wrong_bookings"])
        costs = [r["error_cost"] for r in rows]
        self.assertLess(costs[1], costs[0])
        self.assertLess(costs[1], costs[2])


if __name__ == "__main__":
    unittest.main()
