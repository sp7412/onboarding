import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "labs"))

from stlab.calls import load_calls  # noqa: E402
from stlab.judge import (  # noqa: E402
    PAIRWISE_ITEMS, RUBRICS, ScriptedJudge, ScriptedPairwiseJudge, Verdict, abstention_sweep,
    agreement, build_messages, cohen_kappa, errors_by_scenario, evidence_grounded, flip_rate,
    human_labels, judge_all, parse_verdict, position_test, stratified_sample,
)

V3 = RUBRICS["v2"] + "5. Not bookable: electrical work; the contractor does not offer electrical service.\n"


class JudgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calls = load_calls()
        cls.gold = [c["bookable"] for c in cls.calls]

    def test_kappa_known_values(self):
        self.assertEqual(cohen_kappa([True, False] * 5, [True, False] * 5), 1.0)
        self.assertAlmostEqual(cohen_kappa([True, True, False, False], [True, False, True, False]), 0.0)
        with self.assertRaises(ValueError):
            cohen_kappa([True], [])

    def test_parse_verdict_contract(self):
        v = parse_verdict('{"verdict": "bookable", "confidence": 0.8, "evidence": "x", "reason": "y"}')
        self.assertEqual((v.verdict, v.confidence), ("bookable", 0.8))
        self.assertEqual(parse_verdict("not json").verdict, "needs_human")
        self.assertEqual(parse_verdict('{"verdict": "maybe", "confidence": 0.9}').verdict, "needs_human")
        self.assertEqual(parse_verdict('{"verdict": "bookable", "confidence": 3}').verdict, "needs_human")

    def test_prompt_keeps_disposition_out_unless_asked(self):
        call = self.calls[0]
        self.assertNotIn("disposition:", build_messages(call, "v1")[1]["content"])
        self.assertIn("disposition:", build_messages(call, "v1", show_disposition=True)[1]["content"])
        self.assertIn("76109", build_messages(call, "v1")[0]["content"])

    def test_rubric_fixes_raise_agreement_and_v3_touches_only_electrical(self):
        v1 = judge_all(ScriptedJudge("v1"), self.calls)
        v2 = judge_all(ScriptedJudge("v2"), self.calls)
        v3 = judge_all(ScriptedJudge(V3), self.calls)
        k1, k2, k3 = (agreement(v, self.gold)["kappa"] for v in (v1, v2, v3))
        self.assertLess(k1, k2)
        self.assertLess(k2, k3)
        self.assertLess(k3, cohen_kappa(human_labels(self.calls), self.gold) + 0.05)
        worst = next(iter(errors_by_scenario(self.calls, v1)))
        self.assertIn(worst, ("reschedule", "cancellation", "injection"))
        changed = {c["job_type"] for c, a, b in zip(self.calls, v2, v3) if a.verdict != b.verdict}
        self.assertEqual(changed, {"electrical_issue"})
        self.assertGreater(flip_rate(v1, v2), 0.05)

    def test_disposition_hides_missed_leads(self):
        j = ScriptedJudge("v2")
        missed = [c for c in self.calls if c["bookable"] and not c["outcome"]["booked"]]
        clean = sum(j.judge(c).bookable is True for c in missed)
        shown = sum(j.judge(c, show_disposition=True).bookable is True for c in missed)
        self.assertLess(shown, clean / 2)

    def test_evidence_grounding(self):
        call = self.calls[0]
        self.assertTrue(evidence_grounded(call, Verdict("bookable", 0.9, call["transcript"][0]["text"], "")))
        self.assertFalse(evidence_grounded(call, Verdict("bookable", 0.9, "caller said they wanted to book", "")))
        v = judge_all(ScriptedJudge("v2"), self.calls)
        ungrounded = sum(not evidence_grounded(c, x) for c, x in zip(self.calls, v))
        self.assertTrue(0 < ungrounded < len(self.calls) * 0.05)

    def test_abstention_trades_coverage_for_accuracy(self):
        rows = abstention_sweep(judge_all(ScriptedJudge("v2"), self.calls), self.gold)
        cov = [r["coverage"] for r in rows]
        self.assertEqual(cov, sorted(cov, reverse=True))
        self.assertGreaterEqual(rows[1]["accuracy_when_decided"], rows[0]["accuracy_when_decided"])

    def test_position_test_detects_first_position_bias(self):
        rows = position_test(ScriptedPairwiseJudge(), PAIRWISE_ITEMS)
        self.assertTrue(any(r["always_first"] for r in rows))
        for r in rows:
            if r["gold"] != "either":
                self.assertEqual(r["debiased"], r["gold"])

    def test_stratified_sample_covers_every_scenario(self):
        s = stratified_sample(self.calls, 80)
        self.assertEqual(len(s), 80)
        self.assertEqual({c["scenario"] for c in s}, {c["scenario"] for c in self.calls})
        self.assertEqual(s, stratified_sample(self.calls, 80))


if __name__ == "__main__":
    unittest.main()
