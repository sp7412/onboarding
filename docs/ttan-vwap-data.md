# TTAN daily VWAP chart data

The TTAN plots on the [Company chapter](whitepaper/01-company.md#ttan-vwap-year) use intraday data rather than monthly close/volume estimates.

## What the plots calculate

- **Daily VWAP:** each 1-minute bar's volume-weighted average price (`vw`) multiplied by its volume, summed across the New York trading session, then divided by that session's total bar volume.
- **Rolling VWAP:** a volume-weighted aggregation of the daily VWAP values over the latest 63 trading sessions (approximately three months). The one-year line is sampled once per trading day.
- **Raw price:** the last 1-minute bar close for each session, without smoothing.
- **Inset:** the last ten trading sessions, approximately two weeks.

This is exact for the returned bars' VWAP and volume fields, subject to the feed's coverage and bar aggregation. It is not a trade-by-trade calculation from individual executions.

## Configure the data source

The site build refreshes the chart automatically when both credentials are present. After setup, the deployment workflow also runs at 22:30 UTC on weekdays, after the US regular session closes. Historical requests end 20 minutes before the current time, and the script omits an incomplete current-day session. The script never embeds credentials in the repository or generated JSON.

1. Create a free account with [Alpaca](https://app.alpaca.markets/signup) and create an API key pair. The key is used for market-data access; the chart pipeline does not place trades.
2. In this repository, open **Settings → Secrets and variables → Actions → New repository secret**. Add:
   - `ALPACA_API_KEY` — the API key ID.
   - `ALPACA_SECRET_KEY` — the corresponding secret key.
3. Under **Settings → Secrets and variables → Actions → Variables**, optionally add `ALPACA_DATA_FEED`:
   - `sip` (default): requests historical consolidated data from all US exchanges. The script ends the query 20 minutes in the past to use Alpaca’s historical-data access rules.
   - `iex`: use only if SIP history is denied. This is IEX venue data only and is not a market-wide VWAP.

4. Trigger a deployment by pushing a normal site/content update or running **Actions → Deploy site to GitHub Pages → Run workflow**.

If credentials are absent, the site build succeeds but the plots display a setup notice instead of inventing a VWAP line. The workflow refreshes the JSON in the build workspace; it does not commit API data or credentials back to the repository.

## Important coverage limitation

**Feed coverage matters.** SIP consolidates trading across US exchanges and is the intended default for a market-wide VWAP. IEX is a single exchange and must not be presented as the whole-market VWAP. If Alpaca rejects the historical SIP request for the account, the workflow fails clearly; switch to IEX only if a venue-specific series is acceptable. The chart subtitle and caption identify the feed in use.

The implementation fetches one-minute bars with pagination, computes the daily and 63-session rolling values, and refuses to substitute daily closes or typical-price estimates when a volume-bearing minute bar lacks a VWAP field. Unit tests cover volume weighting and the missing-field failure mode.

## Reproduce locally

```bash
export ALPACA_API_KEY="your-key-id"
export ALPACA_SECRET_KEY="your-secret-key"
# Optional: only when entitled to consolidated data
export ALPACA_DATA_FEED="sip"

python3 scripts/update_ttan_vwap.py --days 370 \\
  --output site/src/data/ttan-vwap.json
python3 -m unittest discover -s scripts -p 'test_update_ttan_vwap.py'
```
