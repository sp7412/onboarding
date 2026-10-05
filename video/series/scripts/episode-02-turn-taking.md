# Episode 2 — Turn-taking

Target length: 3:35 · Approx. 510 words · Running example: a caller reading a phone number.

## Cold open — 0:00–0:10

“My number is eight one seven…” Pause. “Five five five…” Pause again. If your agent treats
every silence as the end, a phone number becomes three conversations.

*Source: `site/src/pages/simulations.astro`, turn-taking simulation; `labs/src/03_turn_taking.py`.*

## Scene 1 — Speech probability — 0:10–0:55

Turn-taking begins with a probability, not a sentence. Voice activity detection estimates
whether each short audio frame contains speech. A minimum speech duration prevents a cough
from opening a turn. A silence timer waits for enough quiet before closing it. These are
useful signals, but silence inside a thought is still silence.

On the waveform, mark the pauses inside the number in gold. A simple timer sees a possible
endpoint. The caller resumes. If the timer already committed, the system has cut the caller
off and must repair the turn downstream.

*Source: `site/src/pages/simulations.astro`, controls for silence timers, speech probability, and line noise; `docs/video-notes.md`, “Designing Voice Agents for Real Conversations”.*

## Scene 2 — Semantic end-of-turn — 0:55–1:40

Semantic end-of-turn detection asks a different question: does this sound like a complete
thought? It can combine the speech signal with transcript context. “My number is eight one
seven” is grammatically unfinished, even after a pause. “That’s everything I need” is more
likely complete.

This does not replace VAD. VAD says whether audio is active. Semantic detection estimates
whether the idea is finished. Together they trade a little decision time for fewer premature
cutoffs. For a booking call, test this on addresses, phone numbers, model numbers, and
restarts—not just clean sentences.

*Source: `docs/video-notes.md`, “Fix AI Voice Interruptions with Semantic Turn Detection”; `site/src/pages/simulations.astro`; `labs/src/03_turn_taking.py`.*

## Scene 3 — Interruptions and backchannels — 1:40–2:25

An interruption is not the same as a backchannel. “Uh-huh” may mean keep going. “No, the
second floor” means stop and revise. A useful agent needs an interruption policy, not only a
volume threshold.

When the caller interrupts, cancel response generation and stop playout. But cancellation
has two histories: what the model generated, and what the caller actually heard. Truncate
the conversation at the audio boundary the caller reached. Otherwise the model may remember
words that never played and answer as if the caller heard them.

*Source: `docs/speech-to-speech-models.md`, section 4; `labs/src/01_realtime_protocol.py`, section on cancellation and truncation; `docs/video-notes.md`, “Designing Voice Agents for Real Conversations”.*

## Scene 4 — Measure the compromise — 2:25–3:10

Every turn detector makes two kinds of mistake. It can cut off a caller too early, or make a
caller wait too long. Record both. Measure endpointing delay, premature cutoffs, interruption
response time, and the gap after a caller really finishes. Slice the results by utterance
type. A detector that looks good on ordinary sentences can still fail on digits.

*Source: `docs/evaluating-voice-agents.md`, “Metrics” and “Adversarial set”; `site/src/pages/simulations.astro`, turn-taking score; `labs/src/03_turn_taking.py`.*

## Recap and end card — 3:10–3:35

Two questions: **How should uncertainty about turn completion change the agent’s behavior?**
And **which false interruption costs the caller the most?** Explore them in lab 03, then see
how lab 01 section 4 cancels and truncates an interrupted response.

*Source: `docs/video-notes.md`, “Fix AI Voice Interruptions with Semantic Turn Detection”; `labs/src/03_turn_taking.py`; `labs/src/01_realtime_protocol.py`.*
