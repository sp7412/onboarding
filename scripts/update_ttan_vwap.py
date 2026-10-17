#!/usr/bin/env python3
"""Fetch TTAN one-minute bars and calculate daily and rolling VWAP.

Requires ALPACA_API_KEY and ALPACA_SECRET_KEY. The default SIP feed is queried as
historical data ending at least 20 minutes before the current time. Set
ALPACA_DATA_FEED=iex only if SIP access is denied;
IEX represents one exchange, not the consolidated US market.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone, time as dt_time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

API_URL = "https://data.alpaca.markets/v2/stocks/TTAN/bars"
ET = ZoneInfo("America/New_York")


def aggregate_bars(bars: list[dict], rolling_sessions: int = 63) -> list[dict]:
    """Aggregate minute-bar VWAPs by New York session date."""
    sessions: dict[str, dict] = defaultdict(
        lambda: {"weighted_value": 0.0, "volume": 0.0, "close": None, "last_ts": ""}
    )
    for bar in sorted(bars, key=lambda item: item["t"]):
        timestamp = datetime.fromisoformat(bar["t"].replace("Z", "+00:00"))
        local_time = timestamp.astimezone(ET)
        outside_session = (local_time.hour, local_time.minute) < (9, 30) or (
            local_time.hour, local_time.minute
        ) >= (16, 0)
        if outside_session:
            continue
        session_date = local_time.date().isoformat()
        volume = float(bar.get("v") or 0)
        if volume <= 0:
            continue
        minute_vwap = bar.get("vw")
        if minute_vwap is None:
            raise ValueError(
                f"Minute bar {bar['t']} has volume but no VWAP field; refusing "
                "to substitute a close-based approximation."
            )
        session = sessions[session_date]
        session["weighted_value"] += float(minute_vwap) * volume
        session["volume"] += volume
        if bar["t"] >= session["last_ts"]:
            session["last_ts"] = bar["t"]
            session["close"] = float(bar["c"])

    rows = []
    for session_date in sorted(sessions):
        item = sessions[session_date]
        if item["volume"] <= 0 or item["close"] is None:
            continue
        rows.append({
            "date": session_date,
            "dailyVwap": round(item["weighted_value"] / item["volume"], 6),
            "close": round(item["close"], 4),
            "volume": int(item["volume"]),
        })

    for i, row in enumerate(rows):
        window = rows[max(0, i - rolling_sessions + 1):i + 1]
        total_volume = sum(item["volume"] for item in window)
        weighted_vwap = sum(item["dailyVwap"] * item["volume"] for item in window)
        row["rollingVwap"] = round(weighted_vwap / total_volume, 6)
    return rows


def fetch_bars(
    api_key: str, secret_key: str, feed: str, start: date, end: str
) -> list[dict]:
    """Fetch every page of one-minute bars for the requested interval."""
    bars: list[dict] = []
    page_token = None
    while True:
        params = {
            "timeframe": "1Min",
            "start": start.isoformat(),
            "end": end,
            "limit": 10000,
            "sort": "asc",
            "feed": feed,
            "adjustment": "raw",
        }
        if page_token:
            params["page_token"] = page_token
        request = Request(
            API_URL + "?" + urlencode(params),
            headers={
                "APCA-API-KEY-ID": api_key,
                "APCA-API-SECRET-KEY": secret_key,
                "Accept": "application/json",
                "User-Agent": "sp7412-onboarding-ttan-vwap/1.0",
            },
        )
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.load(response)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise RuntimeError(
                f"Alpaca API returned HTTP {exc.code}: {detail}"
            ) from exc
        except URLError as exc:
            raise RuntimeError(f"Could not reach Alpaca API: {exc.reason}") from exc
        bars.extend(payload.get("bars", []))
        page_token = payload.get("next_page_token")
        if not page_token:
            break
    return bars


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--days", type=int, default=370,
        help="Calendar-day chart window to output",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("site/src/data/ttan-vwap.json"),
        help="Output JSON consumed by the Astro chart",
    )
    parser.add_argument(
        "--feed", choices=("iex", "sip"),
        default=(os.environ.get("ALPACA_DATA_FEED") or "sip").lower(),
        help="IEX (free tier, venue-only) or SIP (consolidated, subscription required)",
    )
    args = parser.parse_args()
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ALPACA_API_KEY and ALPACA_SECRET_KEY are required.", file=sys.stderr)
        return 2
    if args.days < 95:
        parser.error(
            "--days must be at least 95 to calculate a three-month rolling window"
        )

    now_et = datetime.now(ET)
    today = now_et.date()
    # SIP historical requests are ended 20 minutes in the past. Do not plot a
    # partial current session when the workflow is manually run before close.
    end = (
        (datetime.now(timezone.utc) - timedelta(minutes=20))
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    complete_through = (
        today if now_et.time() >= dt_time(16, 15) else today - timedelta(days=1)
    )
    # Fetch a 100-calendar-day warm-up so the first displayed point has a full
    # 63-session rolling window, then trim the output to the requested chart span.
    fetch_start = today - timedelta(days=args.days + 100)
    display_start = today - timedelta(days=args.days)
    bars = fetch_bars(api_key, secret_key, args.feed, fetch_start, end)
    all_rows = aggregate_bars(bars)
    rows = [
        row for row in all_rows
        if display_start.isoformat() <= row["date"] <= complete_through.isoformat()
    ]
    if len(rows) < 65:
        raise RuntimeError(
            f"Only {len(rows)} sessions returned; expected at least 65. "
            "Check the ticker, feed permissions, and historical-data access."
        )
    payload = {
        "symbol": "TTAN",
        "feed": args.feed,
        "method": "Minute-bar VWAP × minute volume, aggregated by New York session; "
                  "rolling 63-session VWAP is volume-weighted across daily VWAPs.",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "firstDate": rows[0]["date"],
        "lastDate": rows[-1]["date"],
        "sessions": len(rows),
        "data": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(rows)} sessions ({rows[0]['date']} through {rows[-1]['date']}) "
        f"from Alpaca {args.feed.upper()} feed to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
