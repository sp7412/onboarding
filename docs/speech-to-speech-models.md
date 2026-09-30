# Speech-To-Speech Models

How realtime voice models like OpenAI's `gpt-realtime` family work, the current lineup, and
when to use them instead of a cascaded pipeline for a phone agent. Facts as of September 29,
2026; model names and prices change often, so check the [OpenAI models
pages](https://developers.openai.com/api/docs/models/gpt-realtime-2.1) before relying on them.

> **On the name "GPT Live".** OpenAI doesn't sell a model by that name. It most likely
> refers to the Realtime API's speech-to-speech models (`gpt-realtime-*`), which the labs
> use, or to ChatGPT's voice mode, which runs on similar technology. Worth confirming with
> the team.

## Five Takeaways

1. A speech-to-speech model hears audio and speaks audio with **one model**, instead of
   chaining speech-to-text → LLM → text-to-speech. That cuts latency and keeps information
   (tone, emotion, background sound) that a transcript throws away. [1]
2. Current OpenAI options (September 2026): `gpt-realtime-2.1` for complex agent
   workflows, `gpt-realtime-2.1-mini` for cheaper, faster calls, plus specialized
   streaming models for transcription and translation. [2][3][4][5]
3. These are **reasoning models with tool use**: you can set reasoning effort, and the
   model can call your functions mid-conversation. [2][6]
4. Audio is expensive relative to text: for `gpt-realtime-2.1`, audio input costs 8× text
   input per token, and audio output about 2.7× text output. [2]
5. Analysis: speech-to-speech wins on latency and naturalness; cascaded wins on
   inspectability and control. Phone agents often need both, so put deterministic checks
   at the tool boundary regardless of which you choose.

## 1. From pipelines to a single model

Before GPT-4o, ChatGPT's Voice Mode was a pipeline of three models: one transcribed audio to
text, GPT-3.5 or GPT-4 generated a text reply, and a third converted the reply back to
audio. Average latency was 2.8 seconds (GPT-3.5) and 5.4 seconds (GPT-4). OpenAI noted the
main model lost a lot of information that way: it couldn't directly observe tone, multiple
speakers or background noise, and couldn't laugh, sing or express emotion. [1]

With GPT-4o (May 2024), OpenAI trained one model end to end across text, vision and audio,
so the same network processes all inputs and outputs. It could respond to audio in as
little as 232 ms, averaging 320 ms, roughly human conversational timing. [1] Analysis: the Realtime
API's `gpt-realtime` models build on that end-to-end approach.

## 2. How speech-to-speech models work (conceptually)

OpenAI doesn't publish the internals of its realtime models, so the public research
literature is the best way to understand the mechanism. The Moshi paper (Kyutai, 2024) is a
clear, openly documented example: [7]

- **Audio becomes tokens.** A neural audio codec compresses speech into discrete tokens,
  so a language-model backbone can read and generate audio the way it handles text.
- **Text guides speech.** Moshi first predicts time-aligned text tokens, then the audio
  tokens (its "Inner Monologue"), which improves the linguistic quality of the speech and
  yields transcripts for free.
- **Two streams at once.** Moshi models its own speech and the user's speech as parallel
  streams, which removes explicit speaker turns and allows overlaps, interruptions and
  interjections. It reports about 200 ms latency in practice.
- **Why pipelines fall short.** The paper names the same three problems OpenAI did:
  seconds of latency, loss of non-verbal information through the text bottleneck, and rigid
  turn segmentation. [7]

Analysis: production APIs like OpenAI's Realtime API are still largely **turn-based**. Voice
activity detection (server-side or semantic) decides when a caller's turn ends, and the
client handles interruptions by cancelling and truncating responses (lab 01 §4). Fully
duplex, overlap-aware models like Moshi point to where the field may go.

## 3. The current OpenAI lineup

| Model | What it is | Context / max output | Price per 1M tokens (text in / out; audio in / out) | Source |
|---|---|---|---|---|
| `gpt-realtime-2.1` | Reasoning speech-to-speech model with tool use; updates gpt-realtime-2 with better alphanumeric recognition, silence and noise handling, and interruption behavior | 128k / 32k | $4 / $24; $32 / $64 | [2] |
| `gpt-realtime-2.1-mini` | Distilled reasoning model for faster, lower-cost voice interactions; better alphanumeric recognition than gpt-realtime-2 | 128k / 32k | $0.60 / $2.40; $10 / $20 | [3] |
| `gpt-realtime-2` | The May 2026 model the labs target; configurable reasoning effort, stronger instruction following, more reliable tool use | 128k / 32k | $4 / $24; $32 / $64 | [6] |
| `gpt-realtime-whisper` | Streaming speech-to-text for low-latency transcript deltas; priced by audio duration | 16k / 2k | per audio duration | [4] |
| `gpt-realtime-translate` | Streaming speech-to-speech *translation* on a dedicated endpoint; returns translated audio and transcripts while audio is still arriving | 16k / 2k | per audio duration | [5] |

Notes:
- All three conversational models accept text, audio and image input and produce text and
  audio output, and have a September 30, 2024 knowledge cutoff. [2][3][6] Analysis: the
  model knows nothing about your customers, schedule or recent events; everything current
  must come from tools or instructions.
- The July 6, 2026 release also cut p95 latency by at least 25% across Realtime voice
  models through improved caching. [8]
- Aliases like `gpt-realtime-mini` move to newer snapshots over time (OpenAI's changelog
  records these updates), so pin a dated snapshot for production and re-evaluate before
  upgrading. [9]

## 4. What the Realtime API adds around the model

The model is only part of the system. The Realtime API provides the session around it: [10]

- **Connections** over WebRTC (browsers, apps), WebSocket (servers) or SIP (phone calls). [3]
- **Sessions** with instructions, voice, tools and turn-detection settings you can update
  mid-call.
- **Turn detection:** server VAD, semantic VAD, or turn-taking controlled by your app.
- **Events** for streaming audio and text, function calls, cancellation and truncation.
- **Reasoning effort** per session or response. Analysis: start low for voice and raise it
  only for hard turns, since effort trades quality against time to first word. [6]

Lab 01 drives all of this at the level of raw events; lab 02 adds tool calls and guardrails.

## 5. Speech-to-speech vs. cascaded, for a phone agent

| Dimension | Speech-to-speech (realtime model) | Cascaded (STT → LLM → TTS) |
|---|---|---|
| Latency | Lower: one model, streaming | Higher: three hops, though streaming narrows the gap |
| Naturalness | Better prosody, tone, backchannels | Depends on the TTS voice |
| Hears non-verbal cues | Yes (tone, hesitation, noise) [1] | Mostly lost in the transcript |
| Inspect or filter before speaking | Hard: audio is generated directly | Easy: there's a text checkpoint |
| Model choice per stage | One vendor model | Mix and match STT, LLM, TTS |
| Alphanumerics (addresses, phone numbers) | Historically a weak spot; improved in 2.1 [2] | Specialized STT can be tuned |
| Cost | Audio tokens are pricier than text [2] | Varies by stage; often cheaper per call |
| Debuggability | Transcripts arrive alongside audio | Every stage leaves text to inspect |

Analysis for a trades booking call: speech-to-speech fits the conversational parts
(greeting, empathy, clarifying questions, handling interruptions). The parts that change
state (booking, rescheduling, cancelling) need the same guardrails either way: validation
at the tool boundary, grounded confirmations, and a claim guard, because audio can't be
unsaid. That's the pattern lab 02 and lab 07 teach.

## 6. Limits and risks to design around

- **You can't unsay audio.** Filter at the tool boundary and in instructions, and detect
  and correct false claims out loud (lab 07's claim guard).
- **Reasoning costs latency.** Higher effort improves hard turns but delays the first
  word; spoken preambles ("let me check that") cover tool calls. [6]
- **Alphanumerics and noise.** Read back phone numbers, addresses and model numbers before
  acting on them; 2.1 improved these but didn't eliminate the risk. [2]
- **Stale knowledge.** The September 2024 knowledge cutoff means no built-in knowledge of
  anything recent; ground answers in tools. [2]
- **Version drift.** Aliases update; pin snapshots and evaluate upgrades on your scenario
  set before switching. [9]
- **Cost at scale.** Price audio-heavy calls explicitly; per token, the mini model is
  about 3× cheaper for audio and about 7× cheaper for text. [2][3]

## Questions to validate after joining

- Which model and version does the production agent use, and how are upgrades evaluated?
- Speech-to-speech, cascaded, or a hybrid, and why?
- What's the per-call cost, and how does it compare with the value of a booked job?

## Related repo material

- [Voice-agent architecture](voice-agent-architecture.md) and whitepaper [chapter 08](whitepaper/08-technology-landscape.md)
- Labs 01 (realtime protocol), 02 (tools and guardrails), 04 (LiveKit with a realtime model)
- [Reading guide](reading-guide.md) items 5, 7, 8, 13 and 14

## Sources

1. OpenAI, "Hello GPT-4o" (May 13, 2024): <https://openai.com/index/hello-gpt-4o/>
2. OpenAI, GPT-Realtime-2.1 model page: <https://developers.openai.com/api/docs/models/gpt-realtime-2.1>
3. OpenAI, GPT-Realtime-2.1 Mini model page: <https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini>
4. OpenAI, GPT-Realtime-Whisper model page: <https://developers.openai.com/api/docs/models/gpt-realtime-whisper>
5. OpenAI, GPT-Realtime-Translate model page: <https://developers.openai.com/api/docs/models/gpt-realtime-translate>
6. OpenAI, GPT-Realtime-2 model page: <https://developers.openai.com/api/docs/models/gpt-realtime-2>
7. Défossez et al., "Moshi: a speech-text foundation model for real-time dialogue" (2024): <https://arxiv.org/abs/2410.00037>
8. OpenAI Developer Community, "New Realtime models on the API: gpt-realtime-2.1 and gpt-realtime-2.1-mini" (July 6, 2026): <https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896>
9. OpenAI API changelog: <https://developers.openai.com/api/docs/changelog>
10. OpenAI, Realtime API guide: <https://developers.openai.com/api/docs/guides/realtime>
