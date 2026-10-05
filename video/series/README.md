# Voice Agents from First Principles

This directory contains the source for a four-episode local explainer series. The rendered
MP4, MP3, and PDF release assets are deliberately not committed to git; they belong in the
`explainer-series` GitHub release.

## Local production

Production uses Manim Community Edition 0.21.0, Kokoro 0.9.4 with Torch 2.14.1, and ffmpeg
9.0.2. Run commands from the repository root with the repository `.venv` active:

```bash
python video/series/src/render_series.py --all
```

The renderer creates local working files under `video/series/rendered/` and committed-sized
posters, captions, diagrams, and scripts under this directory. It uses no API keys, cloud
voices, uploads, logos, or third-party footage. The narration is an AI-generated voice made
locally with Kokoro.

Run `python video/series/src/media_qa.py` after downloading the release media locally. It
reports dimensions, frame rate, duration, integrated loudness, true peak, sentence-level
caption cue count, and caption drift. The site accessibility smoke test also checks the four
episode cards at 390px and 1280px static viewport targets, including `preload="none"`, PNG
posters, caption tracks, and watched controls.

## Sources

Claims are paraphrased from the following repository documents and the labs named in each
script. Local transcript files were not available when this series was produced.

- `docs/voice-agent-architecture.md`
- `docs/speech-to-speech-models.md`
- `docs/gpt-live-1.md`
- `docs/whitepaper/08-technology-landscape.md`
- `docs/whitepaper/12-risks-and-failure-modes.md`
- `docs/video-notes.md`
- `docs/evaluating-voice-agents.md`
- `labs/src/01_realtime_protocol.py`, `02_tools_and_guardrails.py`, `03_turn_taking.py`,
  `07_evaluation.py`, and `08_latency_and_scale.py`
- `site/src/pages/simulations.astro`

Model names, prices, and benchmarks are marked as “as of October 2026” in the scripts and
on screen. Vendor benchmark figures are described as OpenAI-reported.

## Files

- `scripts/` — narration in our own words, with a source note after every paragraph
- `storyboards/` — scene timing and visual plans
- `src/` — reusable Manim components and episode scenes
- `captions/` — WebVTT captions
- `posters/` — lightweight PNG posters
- `diagrams/` — cheat-sheet diagrams exported from the same visual vocabulary
