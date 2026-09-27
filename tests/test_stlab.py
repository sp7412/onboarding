"""Focused tests for deterministic teaching fixtures."""
from __future__ import annotations

import unittest

from labs.stlab import backend as be
from labs.stlab.tools import CallState, execute_tool


class BackendTests(unittest.TestCase):
    def setUp(self):
        be.reset(seed_booked=False)

    def test_create_job_is_idempotent(self):
        slot = be.find_slots("furnace_repair", "76126")[0]
        first = be.create_job("C-1002", slot["id"], "furnace_repair", "No heat", "test-key")
        replay = be.create_job("C-1002", slot["id"], "furnace_repair", "No heat", "test-key")
        self.assertEqual(first["id"], replay["id"])
        self.assertTrue(replay["replayed"])
        self.assertEqual(len(be.jobs()), 1)

    def test_unknown_job_and_out_of_area_are_policy_errors(self):
        with self.assertRaises(be.PolicyError) as unknown:
            be.find_slots("pool_cleaning", "76126")
        self.assertEqual(unknown.exception.code, "unknown_job_type")
        with self.assertRaises(be.PolicyError) as area:
            be.find_slots("ac_repair", "99999")
        self.assertEqual(area.exception.code, "out_of_service_area")


class ToolBoundaryTests(unittest.TestCase):
    def setUp(self):
        be.reset(seed_booked=False)
        self.state = CallState(call_id="test-call")
        execute_tool("lookup_customer", {"phone": "817-555-0142"}, self.state)
        execute_tool("find_slots", {"job_type": "furnace_repair", "zip_code": "76126"}, self.state)

    def test_booking_requires_grounded_address_confirmation(self):
        args = {"customer_id": "C-1002", "slot_id": self.state.offered_slot_ids[0],
                "job_type": "furnace_repair", "summary": "No heat"}
        result = execute_tool("create_job", args, self.state)
        self.assertEqual(result["error"], "address_not_confirmed")
        self.assertEqual(be.jobs(), [])

    def test_emergency_blocks_routine_tools(self):
        self.state.emergency = True
        result = execute_tool("find_slots", {"job_type": "furnace_repair", "zip_code": "76126"}, self.state)
        self.assertEqual(result["error"], "emergency_escalation_required")
        transferred = execute_tool("transfer_to_human", {"reason": "possible emergency"}, self.state)
        self.assertTrue(transferred["ok"])
        self.assertTrue(self.state.transferred)

    def test_confirmation_must_match_last_user_text(self):
        self.state.last_user_text = "I am not sure about that."
        result = execute_tool("record_address_confirmation", {"caller_said": "yes, that's right"}, self.state)
        self.assertEqual(result["error"], "confirmation_not_grounded")
        self.state.last_user_text = "Yes, that's right."
        result = execute_tool("record_address_confirmation", {"caller_said": "Yes, that's right."}, self.state)
        self.assertTrue(result["address_confirmed"])


if __name__ == "__main__":
    unittest.main()
