# TTAN daily closing-price charts

The TTAN plots in the [Company chapter](whitepaper/01-company.md#ttan-vwap-year) use daily closing prices and volume across the full year. The site workflow refreshes the data before every build; no API key is needed.

## What the charts show

- **Daily close:** the reported close for each trading session, without smoothing.
- **63-session close×volume proxy:** the volume-weighted average of those daily closes over the latest 63 sessions. This is useful as a trend reference, but it is not trade-level VWAP. True VWAP needs intraday trades or bars.
- **Inset:** the latest ten trading sessions.

## Refresh locally

```bash
python3 scripts/update_ttan_daily.py --days 370 \
  --output site/src/data/ttan-vwap.json
```

The script uses [`yfinance`](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html) to fetch Yahoo Finance's daily `Close` and `Volume` fields for TTAN. It requests unadjusted daily bars, uses two years of history to warm up the 63-session calculation, then writes the requested display window to `site/src/data/ttan-vwap.json`. The data source is [Yahoo Finance historical data for TTAN](https://finance.yahoo.com/quote/TTAN/history/).
