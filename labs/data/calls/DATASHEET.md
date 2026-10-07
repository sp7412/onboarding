# Datasheet: Synthetic Home-Services Calls v1

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

## Purpose

One shared, deterministic population of calls for labs 13–14: call understanding,
bookability, lead scoring, dispatch, and earning autonomy. Using the same calls everywhere
lets the labs connect an extraction error to its business cost.

It is **synthetic**. There is no real customer data, recording, name, phone number or
address. Streets are invented, phone numbers are in the fictional 555-01xx range, and ZIP
codes are the three service-area ZIPs of the teaching backend (`stlab/backend.py`) plus
three outside it.

## Generation

`generate_calls(n=400, seed=7)` in `labs/stlab/calls.py` uses Python's seeded `random.Random`
and no network, clock or external data. The same `(n, seed)` always gives identical records.
The committed snapshot `calls-v1.jsonl` is that output, and a unit test checks they match.
Regenerate with `python -m stlab.calls` from `labs/`.

Scenario counts are allocated exactly (largest remainder) from these shares, then shuffled:

| Scenario | Share | Count (n=400) |
|---|---:|---:|
| routine service request | 27.5% | 110 |
| no-cool in a heat wave (after hours) | 12.5% | 50 |
| member tune-up | 7.0% | 28 |
| topic switch (asks about another service, returns) | 7.0% | 28 |
| price shopper (45% decide to book) | 6.5% | 26 |
| reschedule | 6.0% | 24 |
| phone number and address read in chunks | 5.5% | 22 |
| out of service area | 5.0% | 20 |
| cancellation | 4.5% | 18 |
| prompt injection ("ignore your rules, I'm the owner") | 3.5% | 14 |
| gas, smoke, flooding, carbon monoxide, sparks emergencies | 10.5% | 42 |
| wrong number / spam | 4.5% | 18 |

Realized snapshot: 305 HVAC, 57 plumbing and 38 electrical calls; 298 phone, 41 web chat,
39 SMS and 22 external-AI-assistant contacts; 229 after hours; 232 bookable and 199 booked.

## Labels

- **intent:** the caller's main goal (`book_service`, `price_quote`, `reschedule`, `cancel`,
  `out_of_area`, `emergency`, `unknown`, `spam`).
- **job_type:** a job type the teaching backend can schedule (`ac_repair`, `furnace_repair`,
  `hvac_tuneup`, `leak_repair`, `water_heater`), `electrical_issue` (the fictional contractor
  doesn't do electrical work), or `none`.
- **urgency:** `emergency`, `same_day`, `soon`, `routine` or `none`.
- **emergency:** a safety emergency; always transferred, never booked.
- **bookable:** whether a correct system should book this call; **bookable_reason** says why
  or why not (for example out of area, existing appointment, electrical, override attempt).
- **caller_sentiment:** a coarse label for the interaction, not a judgment about the person.
- **replacement_interest, membership, price_shopper, injection_attempt:** booleans.
- **outcome:** synthetic `booked`, `slot`, `est_value` (from the shared lead-scoring function
  in `stlab/coordination.py`) and `actual_value` (est. value × 0.80–1.15).

`scenario` is included for analysis. Extractors must not read it.

## Invariants (enforced by `validate_record` and tests)

- Emergencies are never bookable and never booked.
- Injection attempts are never bookable.
- Every booked call is bookable, and every bookable call has a backend job type.
- Transcripts agree with labels (for example, a no-cool call is HVAC `ac_repair`).

## Known limits and biases

A teaching distribution, not a sample of real contractor calls. Transcripts are short,
scripted English with no ASR errors, accents, crosstalk, disclosures or multilingual traffic.
Emergencies and injection attempts are far more common than in real traffic so that the
labs have enough of them. The dataset contains only answered calls, so it cannot measure
missed-call volume. Values are illustrative, not ServiceTitan, contractor or market figures.

## Intended use

Offline labs, regression tests, metric demonstrations and sensitivity analysis. Don't infer
real customer behavior or production performance from it.
