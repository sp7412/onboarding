# Exercise: Voice-Agent Latency Budget

## Scenario

A caller says:

> "Tuesday afternoon works. Can you book that?"

Assume a target of **900 ms p95** from the end of the caller's turn to the beginning
of useful agent audio. This is a reasoning exercise, not a claim about any real production system.

## Starting budget

| Stage | Your budget | Observed/simulated | Risk |
|---|---:|---:|---|
| Turn detection / endpointing | | | |
| Audio/network transport | | | |
| Model inference | | | |
| Tool dispatch | | | |
| Backend/source-of-truth lookup | | | |
| Response generation | | | |
| Audio generation/transport | | | |
| **Total** | **900 ms** | | |

### Questions

1. Which stages can overlap?
2. Which stages are on the critical path?
3. What happens if backend p95 doubles?
4. Which stage would you optimize first, and why?
5. Which optimization could improve latency while making correctness worse?
6. What would you measure at p50, p95, and p99?
7. Where would you put a timeout, and what should happen after it?
8. How would you distinguish model latency from tool/backend latency in a trace?
9. What user-visible behavior is preferable to silent waiting?

## Senior-level extension

Design two budgets:
- **fast conversational response:** acknowledgement/backchannel while work continues
- **transaction completion:** verified tool result before claiming success

Explain why these are different latency objectives.

## Evidence

Produce a one-page budget, one annotated trace, and a paragraph explaining your largest
trade-off. Label all numbers as hypothetical unless measured locally.
