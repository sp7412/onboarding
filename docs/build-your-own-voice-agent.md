# Build Your Own Voice Agent: Chained vs Full-Duplex

**Facts as of: October 4, 2026 · Last reviewed: October 4, 2026**

A hands-on guide to building the same home-services booking agent two ways with OpenAI's
tools, and to the implementation differences that actually matter:

- **Chained:** speech-to-text → your agent → text-to-speech, using the Agents SDK's
  `VoicePipeline`.
- **Full-duplex:** GPT-Live handles the live conversation and *delegates* reasoning and tools
  to a backend your application runs (client delegation).

Both versions reuse this repo's mock backend and control plane (`labs/stlab`), so the
guardrails from lab 02 carry over unchanged: identity from state, offered and chosen slots,
grounded confirmations, idempotent writes, same-day rules, emergency lock-down.

> **Status:** the code below was checked against `openai` 2.54 and `openai-agents` 0.23 (types,
> method names and offline logic tests), but not run against the live API. You need your own
> OpenAI key for the first real run. Use a personal machine and account, and headphones
> (speaker audio leaking into the microphone causes the agent to interrupt itself).

## 1. Pick the architecture first

OpenAI's voice-agents guide frames three options: [6]

| Architecture | Best for | Why choose it |
|---|---|---|
| **GPT-Live** (full duplex) | Continuous conversation with a separate backend | Keep your existing text workflow and choose its backend independently while the conversation continues |
| **Realtime API** (speech-to-speech) | Speech, reasoning and tool use in one session | One model interprets audio, decides and responds; covered by labs 01–02 |
| **Chained pipeline** | Control over each speech and text stage | Inspect or transform intermediate text; replace each component independently |

The guide's rule of thumb: choose the audio architecture first, then design the rest of the
agent workflow (tools, handoffs, guardrails, observability) the same way you would for text. [6]

## 2. The shared foundation

Both builds wrap the same guarded tools. Run everything from the repo root.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install "openai-agents[voice]" "openai[realtime]" sounddevice soundfile numpy
export OPENAI_API_KEY=sk-...        # personal key; never commit it
export BACKEND_MODEL=gpt-6-luna     # any text model you have access to
```

`voice_tools.py` (repo root) exposes the control-plane tools to the Agents SDK. The model only
ever *proposes* a call; `execute_tool` decides, using the per-call `CallState`:

```python
# voice_tools.py
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "labs"))

from agents import Agent, RunContextWrapper, function_tool  # noqa: E402
from stlab.tools import CallState, execute_tool  # noqa: E402

BACKEND_MODEL = os.environ.get("BACKEND_MODEL", "gpt-6-luna")


def _run(ctx: RunContextWrapper[CallState], name: str, args: dict) -> str:
    return json.dumps(execute_tool(name, args, ctx.context))


@function_tool
def lookup_customer(ctx: RunContextWrapper[CallState], phone: str) -> str:
    """Look up the caller by phone number."""
    return _run(ctx, "lookup_customer", {"phone": phone})


@function_tool
def find_slots(ctx: RunContextWrapper[CallState], job_type: str, zip_code: str) -> str:
    """Find open windows. job_type: ac_repair, furnace_repair, hvac_tuneup, water_heater, leak_repair."""
    return _run(ctx, "find_slots", {"job_type": job_type, "zip_code": zip_code})


@function_tool
def record_slot_choice(ctx: RunContextWrapper[CallState], slot_id: str, caller_said: str) -> str:
    """Record which offered window the caller picked. Quote their exact words."""
    return _run(ctx, "record_slot_choice", {"slot_id": slot_id, "caller_said": caller_said})


@function_tool
def record_address_confirmation(ctx: RunContextWrapper[CallState], caller_said: str) -> str:
    """Record that the caller confirmed the service address. Quote their exact words."""
    return _run(ctx, "record_address_confirmation", {"caller_said": caller_said})


@function_tool
def create_job(ctx: RunContextWrapper[CallState], customer_id: str, slot_id: str,
               job_type: str, summary: str) -> str:
    """Book the job in the slot the caller chose, after the address is confirmed."""
    return _run(ctx, "create_job", {"customer_id": customer_id, "slot_id": slot_id,
                                    "job_type": job_type, "summary": summary})


@function_tool
def transfer_to_human(ctx: RunContextWrapper[CallState], reason: str) -> str:
    """Transfer the caller to a human customer service rep."""
    return _run(ctx, "transfer_to_human", {"reason": reason})


TOOLS = [lookup_customer, find_slots, record_slot_choice, record_address_confirmation,
         create_job, transfer_to_human]

BOOKING_RULES = """You schedule service visits for a fictional HVAC and plumbing company.
Look the caller up first. Find out what's wrong. Offer at most two windows.
When the caller picks one, call record_slot_choice with their exact words.
Read the address back; after a clear yes, call record_address_confirmation, then create_job.
Report an action as complete only after the tool result confirms success.
If anything suggests gas, smoke, sparks, carbon monoxide or flooding, call transfer_to_human."""


def booking_agent(extra_instructions: str = "") -> Agent[CallState]:
    return Agent[CallState](
        name="Booking backend",
        instructions=BOOKING_RULES + extra_instructions,
        model=BACKEND_MODEL,
        tools=TOOLS,
    )
```

## 3. Build A: the chained pipeline

### How it works

The `VoicePipeline` runs three stages per turn: speech-to-text on the caller's audio, your
**workflow** on the transcript, and text-to-speech on whatever text your workflow yields. [6][7]
The workflow is a class with one method, `run(transcription) -> AsyncIterator[str]`, so you
control everything between hearing and speaking. [7] By default the SDK uses OpenAI's
`gpt-transcribe` for speech-to-text and `gpt-4o-mini-tts` for speech (as of `openai-agents`
0.23); you can pass other models.

That's the chained pipeline's superpower: **the full reply exists as text before any audio is
generated**, so you can check it.

### The guarded workflow

```python
# chained_agent.py
import asyncio
import re

import numpy as np
import sounddevice as sd
from agents import Runner
from agents.voice import (AudioInput, TTSModelSettings, VoicePipeline, VoicePipelineConfig,
                          VoiceWorkflowBase)

from voice_tools import booking_agent, execute_tool
from stlab import backend as be
from stlab.tools import CallState

RATE = 24000
CLAIM = re.compile(r"\b(all set|you're booked|is booked|is cancelled|moved to|rescheduled)\b", re.I)
EMERGENCY_LINE = ("If you smell gas, leave the home now and call 911 from outside. "
                  "I'm connecting you to our emergency line.")


class GuardedBookingWorkflow(VoiceWorkflowBase):
    """Transcript in, approved text out. Nothing is spoken until this code yields it."""

    def __init__(self, state: CallState):
        self.state = state
        self.agent = booking_agent("\nCaller ID: " + state.call_id)
        self.history: list = []

    async def run(self, transcription: str):
        # 1. Evidence: the transcript, not a model paraphrase, grounds confirmations.
        self.state.last_user_text = transcription
        # 2. Screen before the model replies.
        if be.detect_emergency(transcription):
            self.state.emergency = True
            execute_tool("transfer_to_human", {"reason": "possible emergency"}, self.state)
            yield EMERGENCY_LINE
            return
        # 3. Run the agent to completion (tools run through the control plane).
        changes_before = len(self.state.changes)
        self.history.append({"role": "user", "content": transcription})
        result = await Runner.run(self.agent, self.history, context=self.state)
        self.history = result.to_input_list()
        reply = str(result.final_output)
        # 4. Claim guard: block "you're booked" unless the backend recorded a change.
        if CLAIM.search(reply) and len(self.state.changes) == changes_before:
            execute_tool("transfer_to_human", {"reason": "unconfirmed claim"}, self.state)
            reply = "I couldn't confirm that change, so I'm connecting you with a team member."
        yield reply


async def main() -> None:
    state = CallState(call_id="+18175550142")   # caller ID comes from telephony in production
    pipeline = VoicePipeline(
        workflow=GuardedBookingWorkflow(state),
        config=VoicePipelineConfig(tts_settings=TTSModelSettings(voice="marin")),
    )
    with sd.OutputStream(samplerate=RATE, channels=1, dtype=np.int16) as speaker:
        while not state.transferred and state.phase != "done":
            input("Press Enter, then speak for up to 6 seconds...")
            audio = sd.rec(int(6 * RATE), samplerate=RATE, channels=1, dtype=np.int16)
            sd.wait()
            result = await pipeline.run(AudioInput(buffer=audio.flatten(), frame_rate=RATE))
            async for event in result.stream():
                if event.type == "voice_stream_event_audio" and event.data is not None:
                    speaker.write(event.data)
    print("phase:", state.phase, "| changes:", state.changes, "| transferred:", state.transferred)


if __name__ == "__main__":
    asyncio.run(main())
```

Run it with `python chained_agent.py`. It's push-to-talk on purpose: each turn is a fixed
recording, which keeps the example short. For hands-free audio, feed a `StreamedAudioInput`,
which lets the pipeline detect turns itself. [7]

### Trade-offs you just made

- **Latency:** `Runner.run` waits for the whole reply (including tool calls) before speech
  starts. Streaming text into TTS (`VoiceWorkflowHelper.stream_text_from(...)`) cuts time to
  first audio, but then audio can start before the claim guard sees the full reply. Choose per
  turn: stream small talk, buffer anything that confirms an action.
- **Turn-taking is yours:** push-to-talk avoids it here; real calls need voice activity
  detection and end-of-turn logic (lab 03), plus interruption handling in your audio layer.
- **Everything is inspectable:** you have the transcript, the agent's tool calls and the final
  text for every turn, which makes logging, redaction and evaluation straightforward.

## 4. Build B: full duplex with GPT-Live (client delegation)

### How it works

GPT-Live listens and speaks at the same time. When it needs help it emits a
**delegation**; your application does the work and sends results back. [1][2] With **client
delegation** your app owns the backend's model, context and execution, and can validate,
redact or discard results before GPT-Live hears them. [2] Key protocol facts:

- Connect to `wss://api.openai.com/v1/live/sessions` (the Python SDK's `client.live.connect()`),
  send `session.start` with the full configuration, and wait for `session.started` before
  sending audio. [3]
- The model, initial instructions, audio format, voice and delegation mode are **fixed at
  startup**; switching delegation modes means a new session. [2][3]
- Stream input with `session.input_audio.append` (base64 raw PCM16, 24 kHz by default; G.711
  is available for telephony); play `session.output_audio.delta`. [3]
- `session.delegation.created` carries only an ID and metadata, **not the user's words**. Your
  app must build context from `session.input_transcript.delta` and
  `session.output_transcript.delta` events. [2]
- Send results back with one of three events (each up to 500 tokens), keyed by the
  delegation ID: [2]
  - `session.thinking.append`: facts or progress the model can use, not spoken on arrival
  - `session.commentary.append`: content the model says aloud (paraphrased)
  - `session.instructions.append`: system-level direction; can interrupt current speech
- Interrupting the conversation does **not** cancel backend work. Your app decides whether to
  finish or cancel, and should ignore results from superseded requests. [1][2]
- End with `session.close`, then wait for `session.closed` to collect final usage. [3]

### The delegation router

```python
# full_duplex_agent.py
import asyncio
import base64
import re

import numpy as np
import sounddevice as sd
from agents import Runner
from openai import AsyncOpenAI

from voice_tools import booking_agent, execute_tool
from stlab import backend as be
from stlab.tools import CallState

RATE = 24000
CLAIM = re.compile(r"\b(all set|you're booked|is booked|is cancelled|moved to|rescheduled)\b", re.I)

LIVE_PROMPT = """You're the friendly phone voice for a fictional HVAC and plumbing company.
Backchannels: brief acknowledgments are fine; don't talk over the caller.
Interruptions: if the caller interrupts, stop and listen.
Delegation: delegate every request that needs customer records, availability, booking,
rescheduling or cancellation. Never say an action is done unless the backend told you so.
While waiting, say you're checking. If you hear about gas, smoke, sparks, carbon monoxide or
flooding, tell the caller to leave the home and call 911, and wait for further instruction."""

BACKEND_VOICE_NOTE = """
You are helping an assistant in a live voice conversation. Transcripts can contain mistakes,
unfinished phrases and later corrections. Use the latest context and verified records. If a
detail is unclear, return a question to ask. Return the relevant facts, the task's status and
the next step, in one or two short sentences."""


class DelegationRouter:
    """Owns conversation context, runs the backend, and decides what GPT-Live may hear."""

    def __init__(self, conn, state: CallState):
        self.conn, self.state = conn, state
        self.agent = booking_agent(BACKEND_VOICE_NOTE + "\nCaller ID: " + state.call_id)
        self.history: list = []
        self.heard = ""               # caller words since the last delegation
        self.active: str | None = None

    async def on_input_transcript(self, delta: str) -> None:
        self.heard += delta
        if be.detect_emergency(self.heard) and not self.state.emergency:
            self.state.emergency = True   # execute_tool now allows only transfer_to_human
            execute_tool("transfer_to_human", {"reason": "possible emergency"}, self.state)
            await self.conn.session.instructions.append(
                delegation_id=None,
                content="Possible emergency. Tell the caller to leave the home now and call 911 "
                        "from outside, then say a team member is joining. Say nothing else.")

    def on_delegation(self, delegation_id: str) -> None:
        said, self.heard = self.heard.strip(), ""
        self.active = delegation_id      # newer requests supersede older ones
        asyncio.create_task(self.handle(delegation_id, said))

    async def handle(self, delegation_id: str, said: str) -> None:
        self.state.last_user_text = said or self.state.last_user_text
        await self.conn.session.thinking.append(
            delegation_id=delegation_id,
            content="Working on it. Nothing has been booked or changed yet.")
        changes_before = len(self.state.changes)
        self.history.append({"role": "user", "content": said or "(continue)"})
        try:
            result = await Runner.run(self.agent, self.history, context=self.state)
        except Exception:
            await self.conn.session.commentary.append(
                delegation_id=delegation_id,
                content="I couldn't finish that just now. A team member can help.")
            return
        self.history = result.to_input_list()
        if delegation_id != self.active:
            return                       # the caller changed the request; drop the stale result
        reply = str(result.final_output)
        if CLAIM.search(reply) and len(self.state.changes) == changes_before:
            reply = "That change isn't confirmed yet. Let me connect you with a team member."
            execute_tool("transfer_to_human", {"reason": "unconfirmed claim"}, self.state)
        await self.conn.session.commentary.append(delegation_id=delegation_id, content=reply[:1500])


async def main() -> None:
    state = CallState(call_id="+18175550142")
    loop = asyncio.get_running_loop()
    mic: asyncio.Queue[bytes] = asyncio.Queue()
    session = {
        "model": "gpt-live-1",
        "instructions": LIVE_PROMPT,
        "audio": {"format": {"type": "audio/pcm", "rate": RATE}, "output": {"voice": "marin"}},
        "delegation": {"type": "client"},
    }

    def on_mic(indata, frames, time, status):  # runs on the audio thread
        loop.call_soon_threadsafe(mic.put_nowait, bytes(indata))

    async with AsyncOpenAI() as client, client.live.connect() as conn:
        router = DelegationRouter(conn, state)
        await conn.session.start(session=session)

        async def pump_mic():
            while True:
                chunk = await mic.get()
                await conn.session.input_audio.append(audio=base64.b64encode(chunk).decode("ascii"))

        with sd.RawInputStream(samplerate=RATE, channels=1, dtype="int16", blocksize=2400,
                               callback=on_mic), \
             sd.RawOutputStream(samplerate=RATE, channels=1, dtype="int16") as speaker:
            sender = None
            try:
                async for event in conn:
                    if event.type == "session.started":
                        sender = asyncio.create_task(pump_mic())
                        print("Session ready. Speak (Ctrl+C to end).")
                    elif event.type == "session.output_audio.delta":
                        speaker.write(np.frombuffer(base64.b64decode(event.delta), dtype=np.int16))
                    elif event.type == "session.input_transcript.delta":
                        await router.on_input_transcript(event.delta)
                    elif event.type == "session.delegation.created" and event.delegation.target == "client":
                        router.on_delegation(event.delegation.id)
                    elif event.type == "session.closed":
                        print("usage:", event.usage)
                        break
                    elif event.type == "error":
                        print("error:", event)
            except (KeyboardInterrupt, asyncio.CancelledError):
                await conn.session.close()      # then keep reading until session.closed
            finally:
                if sender:
                    sender.cancel()
    print("phase:", state.phase, "| changes:", state.changes, "| transferred:", state.transferred)


if __name__ == "__main__":
    asyncio.run(main())
```

Run it with `python full_duplex_agent.py` and headphones. It's deliberately compact; a
production version adds reconnects, resampling, a graceful-close timeout, a sideband
connection for monitoring, and playback controls if your app must decide when audio plays. [3][4]

### What changed compared with the chained build

- **You stop owning turn-taking.** No push-to-talk, no end-of-turn logic: GPT-Live decides
  when to speak, handles interruptions and backchannels, and keeps talking while your backend
  works. [1]
- **You start owning context.** Delegation events don't include the caller's words, so the
  router keeps the transcript and task state itself. [2]
- **The claim guard moves upstream.** You can't inspect the live model's speech before it's
  spoken, so the guard sits on what you *send*: `thinking.append` for progress ("Nothing has
  been booked yet"), `commentary.append` only for verified results. [2]
- **Interruptions and backend work are decoupled.** Stale results must be detected and
  dropped by your app (the `active` check above), and writes must be idempotent because the
  caller can interrupt mid-booking. [2]
- **Emergencies need two actions:** an `instructions.append` to redirect the conversation *and*
  a block in application state, because the instruction doesn't cancel backend work. [2]

## 5. Implementation differences at a glance

| Concern | Chained (`VoicePipeline`) | Full-duplex (GPT-Live, client delegation) |
|---|---|---|
| Conversation model | Turn-based; your app (or the streamed input's detector) decides when a turn ends | Full duplex: listens while speaking; handles interruptions and backchannels itself [1] |
| Where reasoning and tools run | Your workflow, between transcription and speech | Your backend, triggered by `session.delegation.created` [2] |
| What your code sees | Full transcript per turn, all tool calls, the final text | Transcript deltas, delegation IDs, your backend's results; not the live model's reasoning [2] |
| Inspect before speaking | Yes: the whole reply exists as text before TTS | No for live speech; you control only what you append [2] |
| How results are spoken | Your text goes straight to TTS | You append `commentary` and GPT-Live paraphrases it [2] |
| Progress while working | Silence or a scripted filler you yield first | `thinking.append` for quiet progress; the live model can keep talking [2] |
| Interruptions | Yours to detect and handle in the audio layer | Handled by GPT-Live; backend work keeps running until your app cancels it [1][2] |
| Context ownership | Your workflow's message history | Your app, rebuilt from transcript events; delegation events carry no task text [2] |
| Model choice | Any STT, agent model and TTS, per stage [6] | `gpt-live-1` for voice; any backend model or service you run [2][5] |
| Fixed at startup | Nothing; swap stages anytime | Model, instructions, audio format, voice, delegation mode [3] |
| Transport | Whatever carries your audio (files, LiveKit, telephony) | WebRTC, WebSockets or SIP; optional server-side sideband [1][3] |
| Cost model | STT + model tokens + TTS, per stage | $0.05 per minute of voice, billed per second, plus backend usage (as of Oct 2026) [5] |
| Typical latency profile | Adds per-stage hops; streaming narrows it | One live model; OpenAI reports ~0.80 s turn-taking latency in its benchmark (vendor-reported) [8] |
| Main failure modes | Dead air, cut-offs from bad endpointing, talking over callers | Stale backend results, unverified commentary, context drift between transcript and task state |

## 6. Evaluate both the same way

OpenAI's guide recommends testing **both the conversation and the completed task**: for a
booking assistant, listen to the confirmation *and* check the right appointment was saved. [6]
Its staged approach maps cleanly onto this repo:

1. **Crawl:** fixed synthetic speech for single-turn requests (generate audio for the lines in
   `labs/stlab/scenarios.py` with any local TTS) and fixed expected outcomes.
2. **Walk:** replay real recordings of single-turn requests (record your own) to test voices,
   microphones, pauses and noise.
3. **Run:** an independent simulated caller for multi-turn conversations with interruptions
   and changing requirements. [6]

Score each run on: task outcome (`state.changes`, `state.transferred`), tool correctness, claim
grounding (did anything spoken claim a change the backend didn't record?), and latency to a
*useful* answer, comparing median and 95th percentile across repeated calls, with
acknowledgments like "I'm checking" measured separately. [6] Lab 07's evaluators already
encode the grounding and outcome checks.

## 7. Which one for a trades booking call?

Analysis, not vendor guidance:

- **Chained** fits when every spoken confirmation must be checked before it's said, when you
  need a specific STT for addresses and phone numbers, or when you already have a
  transport stack (LiveKit, telephony) and want full control per stage.
- **Full-duplex** fits when natural conversation matters most: callers who interrupt, think
  aloud, or keep talking while the agent looks something up. Your existing text agent becomes
  the backend almost unchanged.
- **Either way, the control plane is the same code.** That's why both builds above share
  `voice_tools.py` and `stlab`: the architecture changes the audio loop, not the rules.

## Sources

1. OpenAI, Getting started with GPT-Live: <https://developers.openai.com/api/docs/guides/live>
2. OpenAI, Delegation and tools in GPT-Live: <https://developers.openai.com/api/docs/guides/live-delegation>
3. OpenAI, WebSockets (GPT-Live section): <https://developers.openai.com/api/docs/guides/voice-websockets?api=live>
4. OpenAI, Managing GPT-Live sessions: <https://developers.openai.com/api/docs/guides/live-conversations>
5. OpenAI, GPT-Live 1 model page: <https://developers.openai.com/api/docs/models/gpt-live-1>
6. OpenAI, Voice agents: <https://developers.openai.com/api/docs/guides/voice-agents>
7. OpenAI Agents SDK (Python), voice pipeline (`agents.voice`), checked against `openai-agents` 0.23: <https://openai.github.io/openai-agents-python/voice/pipeline/>
8. OpenAI, "Build more natural voice experiences with GPT-Live-1 in the API" (September 10, 2026): <https://openai.com/index/introducing-gpt-live-1-in-the-api/>
