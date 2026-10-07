# Episode 1 — Why averages lie

Target length: 3–5 minutes · Beat-timed proof rebuild · Running example: “my AC stopped working.”

## Cold open — the puzzle

Imagine saying, “My AC stopped working.” Every stage of the agent is fast on average. So why
does one call in twenty feel broken?

*Source: `docs/voice-agent-architecture.md`, “Latency Budget”.*

Let’s make the question concrete. The caller stops speaking. The system must decide that the
turn is complete, produce the first model sound, check availability, synthesize a response,
and play it. What should we add: the typical time of each stage, or the slow cases?

*Source: `docs/voice-agent-architecture.md`, “Latency Budget” and “Latency Worksheet”.*

## Chapter 1 — One stage has a shape

Start with endpointing. Most turns commit near the middle of the curve, but some pauses are
ambiguous. Mark the middle of the distribution. That is p50: half the turns are faster, half
slower. Now mark p95: only five in one hundred turns are slower than this point.

*Source: `docs/voice-agent-architecture.md`, “Latency Budget”.*

Do the same for the model’s first audio, the tool round trip, and response playout. These are
illustrative shapes, not production measurements. The point is not the exact number. The point
is that a stage has a distribution, not one duration.

*Source: `docs/voice-agent-architecture.md`, “Latency Budget”; `labs/src/08_latency_and_scale.py`.*

## Chapter 2 — Add the stages

Here is the surprising move: the caller experiences the sum. Slide the endpointing curve
across the model curve. Every possible pair makes a new total. Add the tool curve and the total
spreads again. This is convolution: the distribution of a sum is built from all the ways the
parts can add up.

*Source: `docs/voice-agent-architecture.md`, “Latency Budget”; `docs/whitepaper/08-technology-landscape.md`, “Turn-taking and latency”.*

Notice what happens to the tail. The typical total may still feel acceptable. But the p95 of
the whole pipeline can be much worse than adding a few typical values. A slow endpoint plus a
slow lookup plus buffering is one call that feels broken, even when each team reports a healthy
average.

*Source: `docs/voice-agent-architecture.md`, “Latency Budget”; `docs/evaluating-voice-agents.md`, “Metrics”; `labs/src/08_latency_and_scale.py`.*

## Chapter 3 — Perception is not latency

Suppose the tool is slow. The agent can say, “Let me check that.” The preamble moves the first
sound earlier, so perceived silence shrinks. But the tool distribution did not move. The caller
hears activity; the backend still takes the same time.

*Source: `docs/voice-agent-architecture.md`, “Latency Budget”; `site/src/pages/simulations.astro`, “Latency budget”.*

Keep two measurements: time to first sound, and time to the useful answer. A preamble can help
the first one. It cannot improve the second one. If you optimize only what sounds better, you can
hide the tail without removing it.

*Source: `docs/video-notes.md`, “Deploy Voice AI Agents to Production with Full Observability”; `labs/src/08_latency_and_scale.py`.*

## Recap — ask the lab

Return to the opening picture. The agent was not slow because one box was always slow. It was
slow because random delays added along a serial path. Measure p50 and p95 for every boundary,
then measure the total. What adds the most latency in your pipeline?

*Source: `docs/voice-agent-architecture.md`, “Latency Worksheet”; `labs/src/08_latency_and_scale.py`.*
