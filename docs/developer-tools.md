# Developer tools: the working engineer's toolkit

A living, task-oriented catalog of small tools that reduce friction while building,
debugging, testing, and documenting software. Start with tools that remove repeated
context switches; add complexity only when a tool solves a real workflow problem.

This page is deliberately broader than the voice-agent stack. It covers the local
developer workstation and the practical utilities around an AI-assisted coding loop.
Prefer tools with clear data-flow, predictable shortcuts, and easy removal. Re-check
pricing, release status, platform support, and privacy claims before adopting a tool;
these change faster than the rest of this guide.

## Quick-start shortlist

| Need | Start here | Why |
|---|---|---|
| Dictate prompts into any focused Mac text field | [MacParakeet](https://www.macparakeet.com/) | Free, open-source, system-wide push-to-talk; also handles files, media URLs, and meeting transcription |
| Minimal local voice-to-text | [OpenWispr](https://open-wispr.com/) | Free, open-source, on-device Whisper transcription with a configurable global hotkey |
| No-install fallback | [Apple Dictation](https://support.apple.com/guide/mac-help/dictate-messages-and-documents-mh40584/mac) | Built into macOS; try it before adding another background app |
| Cross-platform local/cloud voice workflows | [OpenWhispr](https://github.com/openwhispr/openwhispr) | Open-source desktop dictation and transcription with local model choices, including Parakeet and Whisper |
| Polished commercial dictation | [Wispr Flow](https://wisprflow.ai/) | A managed option if its editing workflow is worth the subscription and cloud-processing trade-off |

## Mac dictation for AI-assisted coding

The goal is simple: place the cursor in OpenCode, VS Code, a terminal prompt, an issue,
or a document; press and hold a shortcut; speak a complete instruction; release; review
the inserted text; then submit it. This avoids switching to a separate transcription
window and makes longer prompts less tedious.

### MacParakeet

- **Best fit:** a general-purpose, local-first Mac dictation and transcription utility.
- **Trigger:** Fn/Globe by default; configurable hotkeys are supported.
- **Workflows:** system-wide dictation, audio/video and URL transcription, meeting
  recording, custom vocabulary, and a CLI for automation.
- **Cost and license:** free and open source under GPL-3.0, according to the project.
- **Platform:** Apple Silicon Mac; the project currently documents macOS 14.2 or later.
- **Privacy boundary:** core speech recognition runs locally. URL transcription still
  downloads the source media, and optional external AI providers can introduce network
  data flows. Review settings before using it with sensitive material.
- **Links:** [Website and downloads](https://www.macparakeet.com/) ·
  [Source repository](https://github.com/moona3k/macparakeet) ·
  [Agent/CLI integration guide](https://macparakeet.com/agents/)

### OpenWispr

- **Best fit:** lightweight push-to-talk dictation when local transcription is the main
  requirement.
- **Trigger:** hold the Globe/Fn key, speak, release to transcribe; the project documents
  configurable shortcuts, including F5.
- **Speech engine:** local Whisper via whisper.cpp with Metal acceleration on Apple
  Silicon.
- **Cost and license:** free and open source under MIT, according to the project.
- **Platform:** Apple Silicon and a recent macOS version; check the current repository
  for exact requirements.
- **Trade-off:** more focused than MacParakeet; MacParakeet is the broader choice if
  file/URL transcription, meeting recording, or its CLI are also useful.
- **Links:** [Website and installation](https://open-wispr.com/) ·
  [Source repository](https://github.com/human37/open-wispr)

### Apple Dictation

- **Best fit:** trying voice input without installing or maintaining another app.
- **Trigger:** configure the Dictation shortcut in macOS Keyboard settings; exact behavior
  depends on macOS version and settings.
- **Trade-off:** fewer app-specific controls than dedicated push-to-talk tools. Test
  recognition quality, insertion behavior, and privacy requirements on your own Mac
  before deciding it is insufficient.
- **Link:** [Apple's Dictation guide](https://support.apple.com/guide/mac-help/dictate-messages-and-documents-mh40584/mac)

### Other options to evaluate

| Tool | When to consider it | Check before adopting |
|---|---|---|
| [OpenWhispr](https://github.com/openwhispr/openwhispr) | You want a cross-platform workflow or selectable local models such as NVIDIA Parakeet and Whisper | Model/runtime setup, platform-specific hotkeys, and whether any optional cloud path is enabled |
| [Wispr Flow](https://wisprflow.ai/) | You value polished cleanup and a managed user experience | Current free-tier limits, subscription price, and cloud data handling |
| [Superwhisper](https://superwhisper.com/) | You want configurable modes and multiple transcription workflows | Current plan limits, supported models, and which modes process data locally |

## How to choose a dictation tool

1. **Shortcut ergonomics:** can you hold one key, speak, release, and continue typing
   without changing windows? Check whether the key conflicts with IDE or macOS shortcuts.
2. **Insertion reliability:** does text land at the active cursor in your editor, terminal,
   browser, and remote-desktop session? Some secure or elevated fields may behave
   differently.
3. **Recognition quality:** test actual coding vocabulary, acronyms, filenames, class
   names, punctuation, and commands. Compare the raw transcript rather than judging from
   a marketing demo.
4. **Latency:** measure the time from key release to usable inserted text, not only the
   model's claimed real-time factor.
5. **Privacy and retention:** distinguish local speech recognition from optional cloud
   cleanup, telemetry, saved transcripts, crash reports, media downloads, and update checks.
   Do not dictate secrets or company-sensitive content into an unapproved tool.
6. **Correction cost:** a fast transcript that mangles identifiers can be slower overall
   than a slightly slower, more accurate one. Maintain a short test script of representative
   prompts and repeat it after updates.
7. **Operational footprint:** check login-item/background behavior, accessibility and
   microphone permissions, CPU/memory use, updates, and uninstall steps.

## Starter evaluation

Run the same five prompts through each candidate and record the results:

- A normal prose instruction to an AI coding agent.
- A prompt containing acronyms and product names.
- A code-oriented prompt with identifiers, paths, and punctuation.
- A multi-sentence debugging hypothesis with explicit acceptance criteria.
- A prompt spoken in a realistic environment with keyboard/fan noise.

Record word error rate if you have a reference transcript, but also track identifier
accuracy, manual correction time, end-to-end latency, insertion failures, and whether audio
or text leaves the device. Use fictional or public-safe examples.

## Growing the developer-tools catalog

Keep entries task-oriented rather than collecting tools for their own sake. Useful future
categories include:

- **AI coding:** terminal agents, editor integrations, code review, and repository-aware
  workflows.
- **Navigation and automation:** launchers, clipboard history, window management, and
  repeatable shell workflows.
- **Debugging and observability:** structured logs, trace viewers, profilers, and local
  inspection tools.
- **API and data work:** HTTP clients, database explorers, JSON/JSONL viewers, and event
  stream inspection.
- **Knowledge capture:** Markdown notes, screenshots, screen recording, and local search.
- **Testing:** request replay, fixtures, mock services, load generation, and diffable
  evaluation reports.

For each new entry, capture: problem solved, supported platforms, install method, price and
license, local/cloud data path, keyboard workflow, maintenance status, and one concrete
reason to use it. Treat vendor claims as claims until verified with a small hands-on test.
