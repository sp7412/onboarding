import importlib.util
import math
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

SCRIPT = Path(__file__).with_name("update_ttan_daily.py")
SPEC = importlib.util.spec_from_file_location("update_ttan_daily", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FakeHistory:
    def __init__(self, rows):
        self.rows = rows

    def iterrows(self):
        yield from self.rows


class BuildRowsTests(unittest.TestCase):
    def test_rolling_proxy_uses_63_sessions_and_warmup_before_display_window(self):
        start = datetime(2026, 1, 1)
        rows = [
            (start + timedelta(days=i), {"Close": i + 10, "Volume": i + 1})
            for i in range(65)
        ]

        result = MODULE.build_rows(
            FakeHistory(rows), date(2026, 12, 31), (start + timedelta(days=63)).date().isoformat()
        )

        self.assertEqual([row["date"] for row in result], [
            (start + timedelta(days=63)).date().isoformat(),
            (start + timedelta(days=64)).date().isoformat(),
        ])
        expected_64 = sum((k + 9) * k for k in range(2, 65)) / sum(range(2, 65))
        expected_65 = sum((k + 9) * k for k in range(3, 66)) / sum(range(3, 66))
        self.assertAlmostEqual(result[0]["rollingCloseVwap"], expected_64, places=4)
        self.assertAlmostEqual(result[1]["rollingCloseVwap"], expected_65, places=4)

    def test_excludes_future_nonfinite_and_zero_volume_rows(self):
        start = datetime(2026, 1, 1)
        rows = [
            (start, {"Close": 10, "Volume": 100}),
            (start + timedelta(days=1), {"Close": 20, "Volume": 0}),
            (start + timedelta(days=2), {"Close": 30, "Volume": 100}),
            (start + timedelta(days=3), {"Close": 40, "Volume": 100}),
            (start + timedelta(days=4), {"Close": math.nan, "Volume": 100}),
        ]

        result = MODULE.build_rows(FakeHistory(rows), date(2026, 1, 3), "2026-01-03")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["date"], "2026-01-03")
        self.assertEqual(result[0]["rollingCloseVwap"], 20.0)


if __name__ == "__main__":
    unittest.main()
