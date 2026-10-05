# Series outline

The running example is one generic home-services booking call: “my AC stopped working.”
Each episode is designed for roughly 3–4 minutes at 140–150 words per minute. The visual
language is a dark field, cyan signal lines, blue system boxes, green verified outcomes,
gold uncertainty, and red blocked actions.

1. **Anatomy of one call** — Follow audio through VAD, STT, LLM, a tool call, TTS, and
   playout. Build a latency waterfall and distinguish real latency from perceived dead air.
   Finish with the lab 08 question: what adds the most latency in your pipeline?
2. **Turn-taking** — Show speech probability, silence timers, semantic end-of-turn decisions,
   a phone number read with pauses, backchannels, interruption cancellation, and the
   difference between generated audio and audio the caller actually heard. Finish with two
   questions linking to lab 03 and lab 01 section 4.
3. **Choosing an architecture** — Compare cascaded, native speech-to-speech, and full-duplex
   backend delegation across latency, naturalness, interruptions, control, inspectability,
   modularity, cost, and debuggability. Keep model/pricing statements dated October 2026.
4. **The control plane** — Show that the model proposes while the application decides:
   identity, ownership, grounded confirmation, idempotent writes, emergency escalation, the
   claim guard, and repeat-trial evaluation. Finish with labs 02 and 07.
