import json
import unittest
from pathlib import Path

from labs.stlab.calls import load_calls
from labs.stlab.minimax import (
    CallFacts, Evidence, extract_call_facts, run_call, validate_call_facts,
    claim_guard, error_sensitivity,
)


class TestMiniMax(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calls = load_calls()

    def test_contract_validation(self):
        facts = extract_call_facts(self.calls[0])
        ok, errors = validate_call_facts(facts)
        self.assertTrue(ok, errors)
        payload = facts.as_dict()
        schema = json.loads(Path("labs/data/schemas/call-facts.schema.json").read_text())
        self.assertIn("schema_version", schema["required"])
        self.assertEqual(payload["schema_version"], schema["properties"]["schema_version"]["const"])
        self.assertTrue(all(v["evidence"] for v in payload["fields"].values()))

    def test_emergency_never_booked(self):
        emergency = next(c for c in self.calls if c["emergency"])
        result = run_call(emergency)
        self.assertFalse(result["committed"])
        self.assertNotEqual(result["decision"].action, "book")
        self.assertFalse(any(t.get("stage") == "commit" and t.get("ok") for t in result["trace"]))

    def test_claim_guard(self):
        self.assertTrue(claim_guard("You're booked.", committed=True))
        self.assertFalse(claim_guard("You're booked.", committed=False))
        self.assertFalse(claim_guard("You're booked.", committed=True, emergency=True))
        self.assertTrue(claim_guard("I am transferring you to a human.", committed=False, transferred=True))

    def test_error_injection_harness(self):
        rows = error_sensitivity(self.calls[:3])
        names = {row["error_type"] for row in rows}
        self.assertEqual(names, {
            "urgency_wrong", "job_type_wrong", "replacement_interest_missed",
            "sentiment_flipped", "stale_fact", "conflicting_facts",
        })
        self.assertTrue(all("value_delta" in row for row in rows))
        self.assertTrue(all(row["false_claims"] >= 0 for row in rows))

    def test_low_confidence_is_rejected(self):
        facts = extract_call_facts(self.calls[0])
        facts.fields["urgency"] = Evidence("same_day", 0.20, facts.fields["urgency"].evidence)
        ok, errors = validate_call_facts(facts, 0.85)
        self.assertFalse(ok)
        self.assertTrue(any("low_confidence:urgency" == e for e in errors))

    def test_conflicting_facts_are_rejected(self):
        facts = extract_call_facts(self.calls[0])
        facts.conflicts = ("job_type",)
        ok, errors = validate_call_facts(facts)
        self.assertFalse(ok)
        self.assertIn("conflict:job_type", errors)


if __name__ == "__main__":
    unittest.main()
