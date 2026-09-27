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



class AppointmentTests(unittest.TestCase):
    """Reschedule and cancel: identity from state, ownership, confirmation, same-day policy, idempotency."""

    def setUp(self):
        be.reset(seed_booked=False)
        self.state = CallState(call_id="appt-call")
        execute_tool("lookup_customer", {"phone": "817-555-0142"}, self.state)   # Marcus, owns A-2001

    def test_get_appointments_uses_verified_customer(self):
        result = execute_tool("get_appointments", {}, self.state)
        self.assertEqual([a["id"] for a in result["appointments"]], ["A-2001"])
        anon = execute_tool("get_appointments", {}, CallState(call_id="anon"))
        self.assertEqual(anon["error"], "customer_not_verified")

    def test_reschedule_requires_offered_slot_and_is_idempotent(self):
        execute_tool("get_appointments", {}, self.state)
        open_slot = be.find_slots("water_heater", "76126")[0]["id"]
        blocked = execute_tool("reschedule_appointment", {"appointment_id": "A-2001", "new_slot_id": open_slot},
                               self.state)
        self.assertEqual(blocked["error"], "slot_not_offered")
        execute_tool("find_slots", {"job_type": "water_heater", "zip_code": "76126"}, self.state)
        args = {"appointment_id": "A-2001", "new_slot_id": self.state.offered_slot_ids[0]}
        first = execute_tool("reschedule_appointment", args, self.state)
        replay = execute_tool("reschedule_appointment", args, self.state)
        self.assertTrue(first["ok"])
        self.assertTrue(replay["appointment"]["replayed"])
        self.assertEqual(be.appointment("A-2001")["slot_id"], self.state.offered_slot_ids[0])

    def test_cancel_requires_grounded_confirmation(self):
        execute_tool("get_appointments", {}, self.state)
        early = execute_tool("cancel_appointment", {"appointment_id": "A-2001", "reason": "x"}, self.state)
        self.assertEqual(early["error"], "cancel_not_confirmed")
        self.state.last_user_text = "Yes, please cancel it"
        execute_tool("confirm_cancellation", {"caller_said": "yes"}, self.state)
        done = execute_tool("cancel_appointment", {"appointment_id": "A-2001", "reason": "x"}, self.state)
        self.assertTrue(done["ok"])
        self.assertEqual(be.appointment("A-2001")["status"], "cancelled")

    def test_cannot_touch_another_customers_appointment(self):
        execute_tool("get_appointments", {}, self.state)
        self.state.cancel_confirmed = True
        result = execute_tool("cancel_appointment", {"appointment_id": "A-2002", "reason": "x"}, self.state)
        self.assertEqual(result["error"], "appointment_not_owned")
        self.assertEqual(be.appointment("A-2002")["status"], "scheduled")

    def test_same_day_changes_are_refused_by_backend(self):
        dana = CallState(call_id="dana", last_user_text="yes cancel it")
        execute_tool("lookup_customer", {"phone": "817-555-0101"}, dana)
        execute_tool("get_appointments", {}, dana)
        execute_tool("confirm_cancellation", {"caller_said": "yes"}, dana)
        result = execute_tool("cancel_appointment", {"appointment_id": "A-2002", "reason": "x"}, dana)
        self.assertEqual(result["error"], "same_day_change")
        self.assertEqual(dana.changes, [])


if __name__ == "__main__":
    unittest.main()
