# Voice Agents from First Principles — cheat sheet

Use this one-page summary with the four-episode explainer series. It is intentionally
vendor-neutral except where a dated fact is labeled. The running example is a generic
home-services call: “my AC stopped working.”

## 1. One call, end to end

```text
caller audio → VAD / endpointing → STT or speech model → LLM proposal
             → control-plane checks → tool / workflow → authoritative write
             → response generation → TTS / audio → playout
```

Measure endpointing, first model sound, tool/workflow time, response generation, network,
and playout separately. A spoken preamble can cover dead air; it cannot make the tool faster.

## 2. Turn-taking

```text
speech probability ── silence timer ── possible endpoint
          ╲──────── semantic end-of-turn ────────╱
                         turn commit
```

Silence inside a phone number is not necessarily completion. Track premature cutoffs,
unnecessary waits, interruption response time, and the difference between generated audio and
audio the caller actually heard. Cancel, stop playout, and truncate at the heard boundary.

## 3. Architecture choice

| | Cascaded | Speech-to-speech | Full duplex + backend |
|---|---|---|---|
| Latency | more hops | fewer hops | overlap |
| Naturalness | tunable TTS | strong prosody | conversational |
| Control / inspectability | high text checkpoint | lower | backend checkpoint |
| Modularity | high | lower | medium |
| Cost | varies by stage | audio-heavy | voice + backend |
| Debuggability | stage-by-stage | harder | trace delegation |

Choose the architecture for the use case. The control plane does not disappear when the
model changes. Version-specific model names, prices, and vendor benchmarks are as of October
2026; OpenAI benchmark numbers are OpenAI-reported.

## 4. Control-plane checklist

- [ ] Identity comes from the transport/session, not model invention.
- [ ] Customer ownership and current workflow phase are checked.
- [ ] Slot and address confirmations are grounded in offered/current evidence.
- [ ] Writes are idempotent under retries and interruptions.
- [ ] Emergency, restricted, out-of-distribution, and human requests route safely.
- [ ] Never say “booked” before the authoritative write commits.
- [ ] Hard invariants are deterministic; tone and clarity can use review or judges.
- [ ] Repeat trials cover happy paths, adversarial calls, and redacted regressions.

### Sources

`docs/voice-agent-architecture.md` · `docs/speech-to-speech-models.md` · `docs/gpt-live-1.md` ·
`docs/whitepaper/08-technology-landscape.md` · `docs/whitepaper/12-risks-and-failure-modes.md` ·
`docs/evaluating-voice-agents.md` · labs 01, 02, 03, 07, 08 · site simulations.
