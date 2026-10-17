#!/usr/bin/env python3
"""Refresh TTAN daily closes and volume-weighted closing-price estimates."""
from __future__ import annotations

import argparse
from datetime import date, datetime, time as dt_time, timedelta, timezone
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo


def build_rows(history, complete_through: date, display_start: str) -> list[dict]:
    """Filter daily bars, calculate the rolling close-volume proxy, and trim output."""
    all_rows = []
    for session, bar in history.iterrows():
        date = session.date().isoformat()
        close, volume = float(bar["Close"]), float(bar["Volume"])
        if (
            date > complete_through.isoformat()
            or not math.isfinite(close)
            or not math.isfinite(volume)
            or volume <= 0
        ):
            continue
        all_rows.append({"date": date, "close": round(close, 4), "volume": int(volume)})

    for i, row in enumerate(all_rows):
        window = all_rows[max(0, i - 62):i + 1]
        total_volume = sum(item["volume"] for item in window)
        row["rollingCloseVwap"] = round(
            sum(item["close"] * item["volume"] for item in window) / total_volume, 4
        )
    return [row for row in all_rows if row["date"] >= display_start]


def fetch(days: int = 370) -> dict:
    import yfinance as yf

    now = datetime.now(timezone.utc)
    history = yf.download(
        "TTAN",
        period="2y",  # Enough history to warm up the rolling 63-session window.
        interval="1d",
        auto_adjust=False,
        actions=False,
        progress=False,
        threads=False,
        multi_level_index=False,
        timeout=30,
    )
    if history is None or history.empty:
        raise RuntimeError("yfinance returned no TTAN daily history")

    et_now = datetime.now(ZoneInfo("America/New_York"))
    complete_through = (
        et_now.date()
        if et_now.time() >= dt_time(16, 15)
        else et_now.date() - timedelta(days=1)
    )
    display_start = (et_now.date() - timedelta(days=days)).isoformat()
    rows = build_rows(history, complete_through, display_start)
    if len(rows) < 65:
        raise RuntimeError(f"Only {len(rows)} complete daily bars returned")

    return {
        "symbol": "TTAN",
        "feed": "yahoo-daily",
        "method": "Daily closing prices and volumes. RollingCloseVwap is a 63-session volume-weighted average of daily closes; it is a proxy, not trade VWAP.",
        "generatedAt": now.isoformat(),
        "firstDate": rows[0]["date"],
        "lastDate": rows[-1]["date"],
        "sessions": len(rows),
        "data": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=370)
    parser.add_argument("--output", type=Path, default=Path("site/src/data/ttan-vwap.json"))
    args = parser.parse_args()
    payload = fetch(args.days)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {payload['sessions']} TTAN daily closes through {payload['lastDate']}")


if __name__ == "__main__":
    main()
