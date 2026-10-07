# Datasheet: Synthetic Home-Services Calls v1

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

## Purpose

This dataset gives labs 13–14 one deterministic, shared population for studying call
understanding, bookability, lead scoring, dispatch, and earned autonomy.

It is **synthetic**. It contains no real customer data, recordings, names, phone numbers,
or addresses.

## Generation

The generate_calls(n=400, seed=7) function in labs/stlab/calls.py creates short multi-turn
transcripts and gold labels. The generator is deterministic and has no network, clock,
Faker, or external-data dependency. The committed JSONL snapshot is the 400-call seed=7
population used by the notebooks.

The scenario mix is intentionally weighted rather than uniform:

| Scenario family | Target share |
|---|---:|
| routine service | 27.5% |
| no-cool heat wave | 12.5% |
| member tune-up | 7.0% |
| topic switch | 7.0% |
| price shopper | 6.5% |
| reschedule | 6.0% |
| out of area | 5.0% |
| cancellation | 4.5% |
| phone/address chunks | 5.5% |
| prompt injection | 3.5% |
| gas/smoke/CO/sparks/flooding emergencies | 10.5% |
| wrong number / spam | 4.5% |

The realized snapshot can differ slightly because 400 records sample the deterministic
population.

## Labels

- **intent:** primary caller goal.
- **job_type:** normalized service type or 'none'.
- **urgency:** 'emergency', 'same_day', 'soon', 'routine', or 'none'.
- **emergency:** a safety-sensitive emergency requiring transfer.
- **bookable:** whether this call may enter the autonomous booking workflow.
- **bookable_reason:** human-readable gold rationale.
- **caller_sentiment:** coarse interaction state, not a psychological diagnosis.
- **replacement_interest:** whether the caller signals interest in replacement.
- **membership:** whether the caller is a member.
- **price_shopper:** explicit comparison/price-shopping behavior.
- **injection_attempt:** attempt to override the agent's rules.
- **outcome:** synthetic booked/slot/value fields for downstream learning-loop exercises.

## Deliberate edge cases

The population contains after-hours no-cool calls during a heat wave; phone numbers and
addresses spoken in chunks; price shoppers; member tune-ups; reschedules/cancellations;
out-of-area callers; gas, smoke, carbon-monoxide, sparks, and flooding emergencies;
prompt-injection attempts; wrong numbers; spam; and topic-switching calls.

Emergency calls are never labeled bookable and never receive a booked outcome.

## Known limits and biases

This is a teaching distribution, not a representative sample of real contractor calls.
The transcripts are short, written in English, and do not model real ASR errors, accents,
prosody, legal disclosures, caller demographics, multilingual traffic, or actual contractor
policies. Scenario frequencies are intentionally exaggerated for teaching.

Values are illustrative and should not be treated as ServiceTitan, contractor, or market
benchmarks. The dataset is designed to expose failure modes, not estimate production rates.

## Intended use

Use it for offline labs, regression tests, metric demonstrations, and synthetic sensitivity
analysis. Do not infer real customer behavior or production performance from it.
