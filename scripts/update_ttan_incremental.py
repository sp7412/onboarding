#!/usr/bin/env python3
"""Incrementally refresh TTAN daily close/volume data and the chart JSON.

The committed history cache is the source of truth. Each run requests Yahoo
Finance data only from the last cached session (inclusive, to allow corrections),
then rewrites the cache and chart without downloading the full history.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, time as dt_time, timedelta, timezone
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo


def quarter_for(session: date) -> tuple[int, int, str]:
    month = session.month
    quarter = 4 if month in (11, 12, 1) else (month - 1 + 2) // 3
    fiscal_year = session.year if month == 1 else session.year + 1
    return quarter, fiscal_year, f"FY{fiscal_year % 100:02d} Q{quarter}"


def clean_rows(rows: list[dict]) -> list[dict]:
    by_date = {}
    for row in rows:
        close, volume = float(row["close"]), int(row["volume"])
        if math.isfinite(close) and math.isfinite(volume) and volume > 0:
            by_date[row["date"]] = {
                "date": row["date"], "close": round(close, 4), "volume": volume
            }
    return [by_date[key] for key in sorted(by_date)]


def add_rolling(rows: list[dict]) -> list[dict]:
    result = []
    for i, row in enumerate(rows):
        window = rows[max(0, i - 62):i + 1]
        volume = sum(item["volume"] for item in window)
        result.append({
            **row,
            "rollingCloseVwap": round(
                sum(item["close"] * item["volume"] for item in window) / volume, 4
            ),
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=370)
    parser.add_argument("--cache", type=Path,
                        default=Path("site/src/data/ttan-daily-history.json"))
    parser.add_argument("--output", type=Path,
                        default=Path("site/src/data/ttan-vwap.json"))
    args = parser.parse_args()
    if args.days < 95:
        parser.error("--days must be at least 95")

    cache = json.loads(args.cache.read_text(encoding="utf-8"))
    existing = clean_rows(cache.get("data", []))
    if not existing:
        raise RuntimeError(f"No cached TTAN history in {args.cache}")

    import yfinance as yf
    start = date.fromisoformat(existing[-1]["date"])
    history = yf.download(
        "TTAN", start=start.isoformat(), period=None, interval="1d",
        auto_adjust=False, actions=False, progress=False, threads=False,
        multi_level_index=False, timeout=30,
    )
    if history is None or history.empty:
        raise RuntimeError("Yahoo Finance returned no TTAN bars for incremental update")

    now = datetime.now(timezone.utc)
    et_now = datetime.now(ZoneInfo("America/New_York"))
    complete_through = (et_now.date() if et_now.time() >= dt_time(16, 15)
                        else et_now.date() - timedelta(days=1))
    fetched = []
    for session, bar in history.iterrows():
        day = session.date().isoformat()
        close, volume = float(bar["Close"]), float(bar["Volume"])
        if day <= complete_through.isoformat() and math.isfinite(close) and math.isfinite(volume) and volume > 0:
            fetched.append({"date": day, "close": round(close, 4), "volume": int(volume)})
    all_rows = clean_rows(existing + fetched)
    cache.update({
        "symbol": "TTAN",
        "source": "Yahoo Finance daily Close and Volume; incremental refresh",
        "updatedAt": now.isoformat(),
        "updatedThrough": all_rows[-1]["date"],
        "data": all_rows,
    })
    args.cache.parent.mkdir(parents=True, exist_ok=True)
    args.cache.write_text(json.dumps(cache, indent=2) + "\n", encoding="utf-8")

    chart = json.loads(args.output.read_text(encoding="utf-8"))
    previous_last_date = chart.get("lastDate", "")
    existing_chart_rows = chart.get("data", [])
    display_start = (et_now.date() - timedelta(days=args.days)).isoformat()

    # Preserve previously computed rolling values (including hidden warm-up bars).
    # Only calculate rolling values for newly appended sessions.
    additions = [row for row in all_rows if row["date"] > previous_last_date
                 and row["date"] <= complete_through.isoformat()]
    chart_rows = list(existing_chart_rows)
    for row in additions:
        index = next(i for i, item in enumerate(all_rows)
                     if item["date"] == row["date"])
        window = all_rows[max(0, index - 62):index + 1]
        volume = sum(item["volume"] for item in window)
        chart_rows.append({
            **row,
            "rollingCloseVwap": round(
                sum(item["close"] * item["volume"] for item in window) / volume, 4
            ),
        })
    display = [row for row in chart_rows
               if row["date"] >= display_start
               and row["date"] <= complete_through.isoformat()]
    if len(display) < 65:
        raise RuntimeError(f"Only {len(display)} chart sessions available after cache update")

    # Only append sessions later than the published chart end. Repeated runs are
    # idempotent and cannot add a session to a quarter more than once.
    quarters = chart.get("quarterlyClosingVwap", [])
    for row in additions:
        session = date.fromisoformat(row["date"])
        quarter, fiscal_year, label = quarter_for(session)
        item = next((q for q in quarters if q["label"] == label), None)
        if item is None:
            item = {"label": label, "quarter": quarter, "firstDate": row["date"],
                    "lastDate": row["date"], "sessions": 0, "volume": 0,
                    "volumeWeightedClose": 0.0}
            quarters.append(item)
        old_volume = int(item["volume"])
        old_weighted = float(item["volumeWeightedClose"]) * old_volume
        new_volume = old_volume + row["volume"]
        item["firstDate"] = min(item["firstDate"], row["date"])
        item["lastDate"] = max(item["lastDate"], row["date"])
        item["sessions"] += 1
        item["volume"] = new_volume
        item["volumeWeightedClose"] = round(
            (old_weighted + row["close"] * row["volume"]) / new_volume, 4
        )
    chart.update({
        "feed": "yahoo-daily",
        "method": "Daily closing prices and volumes. quarterlyClosingVwap is each fiscal quarter's volume-weighted average of daily closing prices; this is not trade-level VWAP. rollingCloseVwap is a 63-session close-based reference series.",
        "generatedAt": now.isoformat(),
        "firstDate": display[0]["date"],
        "lastDate": display[-1]["date"],
        "sessions": len(display),
        "quarterlyClosingVwap": sorted(quarters, key=lambda q: q["firstDate"]),
        "data": display,
    })
    args.output.write_text(json.dumps(chart, indent=2) + "\n", encoding="utf-8")
    print(f"Updated cache through {all_rows[-1]['date']} ({len(fetched)} fetched rows); "
          f"wrote {len(display)} chart sessions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
