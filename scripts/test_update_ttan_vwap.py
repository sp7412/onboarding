import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("update_ttan_vwap.py")
SPEC = importlib.util.spec_from_file_location("update_ttan_vwap", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AggregateBarsTests(unittest.TestCase):
    def test_daily_vwap_and_rolling_volume_weighting(self):
        bars = [
            {"t": "2026-10-15T13:00:00Z", "vw": 1.0, "v": 9999, "c": 1.0},  # pre-market, excluded
            {"t": "2026-10-15T14:30:00Z", "vw": 10.0, "v": 100, "c": 10.2},
            {"t": "2026-10-15T14:31:00Z", "vw": 12.0, "v": 300, "c": 11.9},
            {"t": "2026-10-15T20:01:00Z", "vw": 50.0, "v": 9999, "c": 50.0},  # after-hours, excluded
            {"t": "2026-10-16T14:30:00Z", "vw": 20.0, "v": 100, "c": 20.1},
            {"t": "2026-10-16T14:31:00Z", "vw": 22.0, "v": 100, "c": 21.8},
        ]
        rows = MODULE.aggregate_bars(bars, rolling_sessions=63)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["date"], "2026-10-15")
        self.assertAlmostEqual(rows[0]["dailyVwap"], 11.5)
        self.assertAlmostEqual(rows[0]["close"], 11.9)
        self.assertEqual(rows[0]["volume"], 400)
        self.assertAlmostEqual(rows[1]["dailyVwap"], 21.0)
        self.assertAlmostEqual(
            rows[1]["rollingVwap"], (11.5 * 400 + 21.0 * 200) / 600, places=5
        )

    def test_refuses_close_proxy_when_minute_vwap_missing(self):
        bars = [{"t": "2026-10-15T14:30:00Z", "v": 100, "c": 10.2}]
        with self.assertRaisesRegex(ValueError, "refusing to substitute"):
            MODULE.aggregate_bars(bars)


if __name__ == "__main__":
    unittest.main()
