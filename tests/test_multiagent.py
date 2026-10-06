import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "labs"))

from stlab import backend as be  # noqa: E402
from stlab.agent_gateway import Gateway, make_request  # noqa: E402
from stlab.context import ContextError, ContextLedger, context_tools  # noqa: E402
from stlab.coordination import Board, Job, Proposal, arbitrate, request_move  # noqa: E402
from stlab.learning import DecisionRecord, calibration_table, fit_uplifts, shrink, synthetic_jobs  # noqa: E402


class ContextLedgerTests(unittest.TestCase):
    def setUp(self):
        self.L = ContextLedger()

    def test_proposed_facts_are_hidden_until_verified(self):
        self.L.propose("voice_agent", "J", "urgency", "same_day", 0.9, "today please")
        self.assertEqual(self.L.view("J"), {})
        self.assertEqual(self.L.view("J", min_status="proposed"), {"urgency": "same_day"})
        self.L.verify("J", "urgency", evidence="caller confirmed")
        self.assertEqual(self.L.view("J"), {"urgency": "same_day"})

    def test_permissions_and_verification_rules(self):
        with self.assertRaises(ContextError) as e:
            self.L.propose("voice_agent", "J", "assigned_tech", "Kara", 1.0)
        self.assertEqual(e.exception.code, "not_permitted")
        self.L.propose("voice_agent", "J", "urgency", "same_day", 0.9)
        with self.assertRaises(ContextError):
            self.L.verify("J", "urgency", evidence="x", by="voice_agent")
        with self.assertRaises(ContextError):
            self.L.verify("J", "urgency", evidence="")
        with self.assertRaises(ContextError):
            self.L.propose("voice_agent", "J", "urgency", "same_day", 1.5)

    def test_optimistic_concurrency(self):
        self.L.propose("dispatch", "J", "assigned_tech", "Kara", 1.0, expected_version=0)
        with self.assertRaises(ContextError) as e:
            self.L.propose("dispatch", "J", "assigned_tech", "Luis", 1.0, expected_version=0)
        self.assertEqual(e.exception.code, "version_conflict")

    def test_retract_ttl_and_as_of(self):
        self.L.propose("voice_agent", "J", "callback_window", "today", 0.9, ttl=3)
        self.L.verify("J", "callback_window", evidence="said so")
        t = self.L.clock
        self.L.tick(5)
        self.assertNotIn("callback_window", self.L.view("J"))
        self.assertEqual(self.L.view("J", as_of=t)["callback_window"], "today")
        self.L.propose("voice_agent", "J", "job_type", "ac_repair", 0.95)
        self.L.verify("J", "job_type", evidence="x")
        self.L.retract("J", "job_type", reason="wrong")
        self.assertNotIn("job_type", self.L.view("J", min_status="proposed"))

    def test_subscriptions_and_tools(self):
        seen = []
        self.L.subscribe("urgency", lambda f: seen.append(f.status))
        tools = context_tools(self.L, "voice_agent")
        self.assertTrue(tools["propose_fact"]("J", "urgency", "same_day", 0.9, "now")["ok"])
        self.assertFalse(tools["propose_fact"]("J", "est_value", 9999, 0.9)["ok"])
        self.L.verify("J", "urgency", evidence="ok")
        self.assertEqual(seen, ["proposed", "verified"])
        self.assertEqual(tools["get_context"]("J"), {"urgency": "same_day"})


class CoordinationTests(unittest.TestCase):
    def board(self):
        techs = {"S1": "Kara", "S2": "Luis"}
        return Board({"S1": Job("J1", "Avery", "tune_up", 150), "S2": Job("J2", "Blake", "ac_repair", 450)},
                     techs, {"Kara": "senior", "Luis": "junior"})

    def test_move_requires_consent_and_limits_repeats(self):
        b = self.board()
        ok, why = request_move(b, "S1", lambda j, a: False)
        self.assertFalse(ok)
        self.assertIsNotNone(b.slots["S1"])
        ok, _ = request_move(b, "S1", lambda j, a: True)
        self.assertTrue(ok)
        self.assertEqual(b.credits_issued, 25)
        b.slots["S1"] = b.tomorrow[0]
        ok, why = request_move(b, "S1", lambda j, a: True)
        self.assertFalse(ok)
        self.assertIn("already been moved", why)

    def test_arbitration_respects_capacity_net_value_and_vetoes(self):
        ps = [Proposal("a", "x", 500, 100), Proposal("b", "y", 300, 10), Proposal("c", "z", 50, 100)]
        d = {x.proposal.agent: x.accepted for x in arbitrate(ps, capacity=1)}
        self.assertEqual(d, {"a": True, "b": False, "c": False})
        veto = arbitrate(ps, capacity=3, hard_rules=[lambda p: "no" if p.agent == "a" else None])
        self.assertFalse(next(x for x in veto if x.proposal.agent == "a").accepted)


class LearningTests(unittest.TestCase):
    def test_fit_recovers_true_effects_and_shrink(self):
        jobs = synthetic_jobs(n=400, seed=11)
        recs = [DecisionRecord(j["job_id"], j["job_id"], 0, {"job_type": j["job_type"], "signals": j["signals"]},
                               0, "book", j["actual_value"]) for j in jobs]
        est = fit_uplifts(recs, ["system_down", "replacement_interest", "same_day_needed"])
        self.assertAlmostEqual(est["system_down"][0], 120, delta=60)
        self.assertAlmostEqual(est["replacement_interest"][0], 2600, delta=150)
        self.assertAlmostEqual(shrink(100, 200, 20, k=20), 150)
        rows = calibration_table([(0.95, True), (0.95, True), (0.85, False), (0.85, True)])
        self.assertEqual([r["accuracy"] for r in rows], [0.5, 1.0])


class GatewayTests(unittest.TestCase):
    def setUp(self):
        be.reset()
        be.LATENCY_MS.update({k: 0 for k in be.LATENCY_MS})
        self.gw = Gateway()
        self.c = self.gw.register("a", {"availability:read", "booking:create"})

    def quote(self):
        return self.gw.handle(make_request(self.c, "POST", "/availability",
                                           {"job_type": "ac_repair", "zip_code": "76126"}, ts=self.gw.now))[1]

    def test_happy_path_and_idempotency(self):
        q = self.quote()
        body = {"quote_id": q["quote_id"], "slot_id": q["windows"][0]["slot_id"],
                "homeowner": {"name": "A", "phone": "+15550001111"}}
        s1, r1 = self.gw.handle(make_request(self.c, "POST", "/bookings", body, ts=self.gw.now, idempotency_key="k"))
        s2, r2 = self.gw.handle(make_request(self.c, "POST", "/bookings", body, ts=self.gw.now, idempotency_key="k"))
        self.assertEqual((s1, s2), (200, 200))
        self.assertEqual(r1["booking_id"], r2["booking_id"])
        self.assertEqual(len(be.jobs()), 0)
        self.assertEqual(self.gw.homeowner_confirms(r1["booking_id"], True)["status"], "confirmed")
        self.assertEqual(len(be.jobs()), 1)

    def test_refusals(self):
        req = make_request(self.c, "POST", "/availability", {"job_type": "ac_repair", "zip_code": "76126"},
                           ts=self.gw.now)
        req.body = {"job_type": "ac_repair", "zip_code": "76109"}
        self.assertEqual(self.gw.handle(req)[1]["error"], "bad_signature")
        stale = make_request(self.c, "POST", "/availability", {"job_type": "ac_repair", "zip_code": "76126"},
                             ts=self.gw.now - 1000)
        self.assertEqual(self.gw.handle(stale)[1]["error"], "stale_request")
        q = self.quote()
        body = {"quote_id": q["quote_id"], "slot_id": "S-NOPE", "homeowner": {"name": "A", "phone": "+1"}}
        self.assertEqual(self.gw.handle(make_request(self.c, "POST", "/bookings", body,
                                                     ts=self.gw.now))[1]["error"], "slot_not_quoted")

    def test_no_customer_enumeration(self):
        q = self.quote()
        known = {"quote_id": q["quote_id"], "slot_id": q["windows"][0]["slot_id"],
                 "homeowner": {"name": "M", "phone": "+18175550142"}}
        unknown = {**known, "slot_id": q["windows"][1]["slot_id"], "homeowner": {"name": "M", "phone": "+19999999999"}}
        a = self.gw.handle(make_request(self.c, "POST", "/bookings", known, ts=self.gw.now))
        b = self.gw.handle(make_request(self.c, "POST", "/bookings", unknown, ts=self.gw.now))
        self.assertEqual((a[0], set(a[1])), (b[0], set(b[1])))


if __name__ == "__main__":
    unittest.main()
