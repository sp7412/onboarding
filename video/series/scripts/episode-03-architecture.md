# Episode 3 — Choosing an architecture

Target length: 3:45 · Approx. 535 words · Version-specific facts are as of October 2026.

## Cold open — 0:00–0:10

Three agents answer the same caller. One is easier to inspect. One sounds more natural. One
keeps listening while it speaks. Which one should book the AC repair?

*Source: `docs/speech-to-speech-models.md`, section 5; `docs/gpt-live-1.md`, section 2.*

## Scene 1 — Cascaded — 0:10–0:55

The cascaded design is explicit: speech-to-text, then a language model, then text-to-speech.
It has more hops, so streaming and overlap matter. But it leaves a text checkpoint between
what the caller said and what the agent will say. You can inspect it, filter it, swap one
stage, or tune speech recognition for addresses and phone numbers.

For a booking call, that modularity is valuable when the team needs to debug every decision or
use different models for different stages. The cost is extra coordination and another place
for latency to accumulate.

*Source: `docs/speech-to-speech-models.md`, sections 1 and 5; `docs/voice-agent-architecture.md`, “Latency Budget”.*

## Scene 2 — Native speech-to-speech — 0:55–1:40

Native speech-to-speech uses one model to hear audio and produce audio. It can preserve cues
that a transcript loses, such as tone and hesitation. It can make responses feel more
natural, and often reduces the number of model hops.

The trade is inspectability. Audio arrives directly, so it is harder to filter the response
before it is spoken. Audio tokens can also cost more than text tokens. As of October 2026,
the repository describes current Realtime model prices and names as changing vendor facts;
use them only as dated context, not as timeless architecture rules.

*Source: `docs/speech-to-speech-models.md`, sections 1, 3, and 5. The model names and prices are described as of October 2026; no benchmark is used here.*

## Scene 3 — Full duplex with delegation — 1:40–2:35

Full duplex changes the rhythm. The live voice model can listen while speaking, while a
backend handles reasoning and tools. The backend can send three kinds of updates: an
instruction that changes direction, thinking that helps the model without being spoken, and
commentary that can be said aloud.

That last channel needs a hard boundary. “I’m checking Thursday” is progress. “You’re booked”
is a claim. Commentary should contain the claim only after the backend has committed the
booking. If the caller interrupts while the write is in flight, the application decides
whether to finish or cancel it, then reports the actual result.

*Source: `docs/gpt-live-1.md`, sections 2–4; `docs/voice-agent-architecture.md`, “Talker And Thinker”. Version-specific model, endpoint, and pricing facts are as of October 2026.*

## Scene 4 — Trade-off table — 2:35–3:20

Compare the choices across eight dimensions. Cascaded wins modularity, control, and
inspectability. Native speech-to-speech tends to win naturalness and can reduce latency, but
is harder to inspect. Full duplex can win overlapping conversation and interruption handling,
while moving more design work into delegation and backend boundaries. Cost and debuggability
depend on the actual workload.

For a booking call, choose cascaded when inspection and stage-level control dominate. Choose
native speech-to-speech when conversational timing matters and the tool boundary is strong.
Choose full duplex when simultaneous listening and speaking are central, and the team can
operate a backend delegation path. In every case, the control plane stays.

*Source: `docs/speech-to-speech-models.md`, sections 5–6; `docs/gpt-live-1.md`, sections 3–5; `docs/voice-agent-architecture.md`, “Ownership Rules”.*

## Recap and end card — 3:20–3:45

The architecture changes where latency and uncertainty live. It does not change who owns
authorization, grounded evidence, durable state, or evaluation. For the version-specific
details and the questions to validate after joining, read `docs/gpt-live-1.md`.

*Source: `docs/gpt-live-1.md`, “Questions to validate after joining”; `docs/voice-agent-architecture.md`, “Where Each Component Stops”.*
