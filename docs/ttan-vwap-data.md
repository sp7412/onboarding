# TTAN daily closing-price charts

The TTAN plots in the [Company chapter](whitepaper/01-company.md#ttan-vwap-year)
use daily closing prices and volume across the full year.

## What the charts show

- **Daily close:** the reported close for each trading session, without smoothing.
- **63-session close×volume proxy:** the volume-weighted average of those daily closes
  over the latest 63 sessions. This is a trend reference, not trade-level VWAP.
- **Inset:** the latest ten trading sessions.

## Incremental refresh

The committed [daily-history cache](../site/src/data/ttan-daily-history.json)
stores daily date, close, and volume records. The incremental updater reads that
cache and asks Yahoo Finance only for data starting at the last cached session
(inclusive, so a provider correction to the last bar can be picked up).

```bash
python3 -m pip install 'yfinance>=1.7.0'
python3 scripts/update_ttan_incremental.py --days 370
```

The script updates both the cache and the chart JSON at
`site/src/data/ttan-vwap.json`. Commit both files together to preserve the new
checkpoint for the next run. The cache currently contains available chart bars
beginning 2025-10-13; it is not a complete multi-year archive.

## Full refresh

To rebuild the chart from a fresh Yahoo Finance history download, use the original
full-history script:

```bash
python3 scripts/update_ttan_daily.py --days 370 \
  --output site/src/data/ttan-vwap.json
```

That script uses two years of unadjusted daily bars to warm up the 63-session
calculation. Yahoo Finance is the source for daily `Close` and `Volume` fields.
