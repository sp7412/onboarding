# Exercise: Voice-Agent Latency Budget

**Time:** 45 minutes · **Builds on:** [latency budget](../docs/voice-agent-architecture.md#latency-budget), lab 08, the site's latency simulation

## Scenario

A caller says:

> "Tuesday afternoon works. Can you book that?"

Assume a target of **900 ms p95** from the end of the caller's turn to the start of useful
agent audio. This is a reasoning exercise, not a claim about any real production system.

## Starting budget

| Stage | Your p95 budget | Observed / simulated | Risk |
|---|---:|---:|---|
| Turn detection / endpointing | | | |
| Audio and network transport (inbound) | | | |
| Model inference to first token or audio | | | |
| Tool dispatch | | | |
| Backend / source-of-truth lookup | | | |
| Response generation | | | |
| Audio generation and transport (outbound) | | | |
| **Total** | **900 ms** | | |

### Questions

1. Which stages can overlap, and which are strictly on the critical path?
2. Does the table's total equal the end-to-end p95? (Hint: think about what happens when you
   add percentiles.)
3. What happens if backend p95 doubles?
4. Which stage would you optimize first, and why?
5. Which optimization could improve latency while making correctness worse?
6. What would you measure at p50, p95 and p99, and on which slices?
7. Where would you put a timeout, and what should happen after it fires?
8. How would you tell model latency from tool or backend latency in a trace?
9. What should the caller hear instead of silence?

## Extensions

- **Two objectives.** Design a *conversational* budget (an acknowledgement while work
  continues) and a *transaction* budget (a verified tool result before claiming success).
  Explain why they differ and which one the 900 ms target should apply to.
- **Full duplex.** Redo the budget for a full-duplex voice model that delegates the booking to
  a backend agent (see [GPT-Live-1](../docs/gpt-live-1.md)). Which stages disappear, which
  move off the critical path, and what new risk appears?

## Deliverable

A one-page budget, one annotated trace (simulated is fine; lab 08 can produce one), and a
paragraph on your largest trade-off. Label every number as hypothetical unless you measured it
locally.

## Self-check

A strong answer:

- Notes that **p95s don't add**: the sum of per-stage p95s overstates the end-to-end p95 if
  stages are independent, and understates it if slowdowns are correlated (for example, load
  slowing the model and the backend together). It budgets end to end and measures end to end.
- Moves work off the critical path (prefetching likely slots while the caller is still talking,
  streaming TTS, overlapping the acknowledgement with the lookup) rather than only shaving
  stages.
- Never uses a preamble to imply success. "Let me check that" is fine; "you're booked" before
  the commit is not.
- Gives the timeout a defined behavior: tell the caller, read state before any retry, and hand
  off or call back if the tool is down.
- Names a correctness risk created by a latency fix, such as a looser endpointing threshold
  cutting callers off mid-number, or a cached slot list going stale.

---

Part of the [senior engineer judgment track](README.md).
