# %% [markdown]
# # 01 · The OpenAI Realtime protocol
#
# **Goal:** understand the Realtime API at the level of raw JSON events so that SDKs and frameworks (LiveKit's OpenAI plugin, the Agents SDK) stop being magic.
#
# You will:
# 1. open a session and configure it with `session.update`
# 2. send a turn and read every event that comes back
# 3. measure time-to-first-token vs. reasoning effort
# 4. see barge-in (cancellation) and **truncation**, the thing most homegrown voice loops get wrong
# 5. (live only) get audio back and play it
#
# **Live vs. offline.** If `OPENAI_API_KEY` is set, `connect()` opens a WebSocket to `wss://api.openai.com/v1/realtime?model=gpt-realtime-2`. Otherwise it returns `FakeRealtime`, a simulator that speaks the same event protocol with a scripted "brain". Force either with `LIVE = True/False`.
#
# Reference: OpenAI Realtime API guide and client/server event reference (developers.openai.com). Model names change; check the models page.

# %%
import asyncio, json, time
import stlab
from stlab.realtime import connect, EventPrinter

stlab.load_env()
LIVE = None          # None = auto (live if OPENAI_API_KEY), or force True / False
MODEL = "gpt-realtime-2"

# %% [markdown]
# ## 1. Open a session
#
# A Realtime connection is a long-lived WebSocket. The server immediately sends `session.created`. You then send `session.update` to set instructions, output modality, tools, voice, turn detection, and (for reasoning models) reasoning effort.
#
# In the GA API the session object has `"type": "realtime"`, audio config nested under `audio.input` / `audio.output`, and `output_modalities` of `["text"]` or `["audio"]`.

# %%
conn = await connect(live=LIVE, model=MODEL)
print("LIVE" if conn.is_live else "SIMULATED", "connection")
first = await conn.recv(timeout=10)
print(first["type"])

await conn.send({
    "type": "session.update",
    "session": {
        "type": "realtime",
        "instructions": ("You are the phone assistant for Benbrook Comfort Services, an HVAC and plumbing "
                         "contractor. Be brief and warm. Never quote prices."),
        "output_modalities": ["text"],         # text first; audio in section 5
        "reasoning": {"effort": "low"},
    },
})
ev = await conn.recv(timeout=10)
while ev["type"] != "session.updated":
    ev = await conn.recv(timeout=10)
print(ev["type"], "→ instructions:", ev["session"]["instructions"][:60], "...")

# %% [markdown]
# ## 2. One turn, raw events
#
# A conversation is a list of **items** (messages, function calls, function outputs). A **response** is the model generating new items. The client:
#
# 1. `conversation.item.create`: add the caller's message (here typed text; with audio you'd `input_audio_buffer.append` and let VAD commit it)
# 2. `response.create`: ask the model to respond
#
# Then reads server events until `response.done`. Below, no helper hides anything: we print each event type and key fields.

# %%
async def send_text_turn(conn, text):
    await conn.send({"type": "conversation.item.create", "item": {
        "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}})
    await conn.send({"type": "response.create"})

await send_text_turn(conn, "Hi, my AC stopped blowing cold air this morning.")

t0 = time.perf_counter()
reply = []
while True:
    ev = await conn.recv(timeout=30)
    ms = (time.perf_counter() - t0) * 1000
    typ = ev["type"]
    if typ == "response.output_text.delta":
        reply.append(ev["delta"])
        if len(reply) == 1:
            print(f"{ms:7.0f} ms  {typ}  (first token; further deltas hidden)")
        continue
    print(f"{ms:7.0f} ms  {typ}")
    if typ == "response.done":
        r = ev["response"]
        print("\nstatus:", r["status"], "| usage:", r.get("usage"))
        break
print("\nAssistant:", "".join(reply))

# %% [markdown]
# **Event anatomy to memorize**
#
# | Event | Meaning |
# |---|---|
# | `response.created` | model started; the response id is here |
# | `response.output_item.added` | a new output item (message or function_call) began |
# | `conversation.item.added` | that item now exists in the conversation |
# | `response.output_text.delta` / `response.output_audio_transcript.delta` / `response.output_audio.delta` | streaming content |
# | `response.function_call_arguments.done` | a complete tool call proposal: `name`, `arguments`, `call_id` |
# | `response.done` | final status: `completed`, `cancelled`, `incomplete`, `failed` (+ usage) |
# | `input_audio_buffer.speech_started` / `speech_stopped` / `committed` | server VAD saw the caller start/stop talking |
#
# From here on we use `EventPrinter`, which prints the same thing more compactly.

# %% [markdown]
# ## 3. Reasoning effort vs. time-to-first-token
#
# `gpt-realtime-2` exposes `reasoning.effort` (`minimal` … `xhigh`). More reasoning can mean better handling of messy requests, but it delays the first word. In voice, **time to first audio** is the metric callers feel.
#
# Measure `response.created` → first delta for each effort. (Simulated numbers are made up to illustrate the shape; live numbers are real.)

# %%
async def ttft(conn, effort, text="Can someone come out tomorrow afternoon instead of Thursday?"):
    await conn.send({"type": "session.update", "session": {"type": "realtime", "reasoning": {"effort": effort}}})
    await send_text_turn(conn, text)
    t_created = t_first = None
    while True:
        ev = await conn.recv(timeout=60)
        now = time.perf_counter()
        if ev["type"] == "response.created":
            t_created = now
        elif ev["type"].endswith(".delta") and t_first is None and "text" in ev["type"]:
            t_first = now
        elif ev["type"] == "response.done":
            return (t_first - t_created) * 1000 if t_first and t_created else None

results = {}
for effort in ["minimal", "low", "medium", "high"]:
    results[effort] = await ttft(conn, effort)
    print(f"{effort:<8} first token after {results[effort]:6.0f} ms")

# %% [markdown]
# **Design question:** should effort be fixed per session? A common pattern is low effort for small talk and slot-filling, and a higher effort (or a separate "thinker", see notebook 08) only for hard turns such as rescheduling conflicts or billing disputes. You can change it with `session.update` mid-call, or pass overrides on a single `response.create`.

# %%
await conn.send({"type": "session.update", "session": {"type": "realtime", "reasoning": {"effort": "low"}}})
await conn.close()

# %% [markdown]
# ## 4. Barge-in and truncation
#
# With server VAD (`audio.input.turn_detection` with `interrupt_response: true`), when the caller starts talking while the model is speaking, the server cancels the in-flight response (`response.done` with `status: cancelled`).
#
# But the model **generated** more text/audio than the caller **heard**. Audio is streamed to the client faster than real time and buffered for playout. If you don't fix this, the conversation history says the agent said things the caller never heard, and the model will later refer to them.
#
# The fix: the client tracks how many milliseconds of the assistant's audio were actually played, then sends `conversation.item.truncate` with `audio_end_ms`. The server trims the item (and its transcript) to match.
#
# The simulator supports a non-standard client event, `x_sim.user_speech`, to emulate the caller talking into a mic. With a live key you need real audio input to trigger VAD, so this section always runs on the simulator.

# %%
from stlab.fake_realtime import FakeRealtime, MS_PER_WORD_AUDIO

sim = await connect(live=False)
p = EventPrinter()
await sim.send({"type": "session.update", "session": {
    "type": "realtime", "output_modalities": ["audio"],
    "audio": {"input": {"turn_detection": {"type": "server_vad", "silence_duration_ms": 500,
                                            "create_response": True, "interrupt_response": True}}}}})

# Agent starts a long greeting...
await sim.send({"type": "response.create"})

played_ms, assistant_item = 0, None
async def pump_until(pred, timeout=5):
    global played_ms, assistant_item
    while True:
        ev = await sim.recv(timeout=timeout)
        p(ev)
        if ev["type"] == "response.output_audio.delta":
            assistant_item = ev["item_id"]
        if pred(ev):
            return ev

# Let 6 words stream to the client, then the caller barges in.
# Audio arrives faster than real time, so the speaker has only *played* ~3 of them.
n = {"words": 0}
def six_words(e):
    if e["type"] == "response.output_audio_transcript.delta":
        n["words"] += 1
    return n["words"] >= 6
await pump_until(six_words)
played_ms = 3 * MS_PER_WORD_AUDIO   # what our (pretend) speaker actually played
await sim.send({"type": "x_sim.user_speech", "text": "Sorry, I need someone for my water heater", "duration_ms": 1500})
await pump_until(lambda e: e["type"] == "response.done")
print(f"\nCaller heard ~{played_ms} ms of the greeting; truncating item {assistant_item}")

# %%
await sim.send({"type": "conversation.item.truncate", "item_id": assistant_item,
                "content_index": 0, "audio_end_ms": played_ms})
await pump_until(lambda e: e["type"] == "conversation.item.truncated")
item = next(i for i in sim.items if i["id"] == assistant_item)
print("History now says the agent said:", repr(item["content"][0]["transcript"]))
# drain the auto-response to the caller's new turn
await pump_until(lambda e: e["type"] == "response.done")

# %% [markdown]
# Two things to notice in the log above:
#
# - The cancelled response ends with `response.done` / `status=cancelled`. Your client must also **stop local playout immediately** and flush its audio buffer; the server can't reach into your speaker.
# - After the caller stopped, the server waited `silence_duration_ms` before `speech_stopped`, then auto-created a response (`create_response: true`). That wait is endpointing; notebook 03 is all about tuning it.
#
# **Who owns what here?** The model owns generating speech. The transport (LiveKit, or your WebRTC client) owns knowing what was played and doing the truncation; LiveKit's agent framework does this for you. The application owns *policy*: e.g. "this disclosure must be heard in full: disable interruptions while it plays."

# %%
await sim.close()

# %% [markdown]
# ## 5. (Live only) Audio output
#
# Switch to `output_modalities: ["audio"]`, pick a voice, collect `response.output_audio.delta` chunks (base64 PCM16, 24 kHz mono), and play them.

# %%
import base64, io, wave, os
from IPython.display import Audio, display

if os.environ.get("OPENAI_API_KEY"):
    live = await connect(live=True, model=MODEL)
    await live.recv(timeout=10)
    await live.send({"type": "session.update", "session": {
        "type": "realtime", "output_modalities": ["audio"],
        "audio": {"output": {"voice": "marin", "format": {"type": "audio/pcm", "rate": 24000}}},
        "instructions": "You are a friendly HVAC dispatcher. One sentence answers."}})
    await send_text_turn(live, "Greet a caller who just phoned about a broken furnace.")
    pcm, transcript = bytearray(), []
    while True:
        ev = await live.recv(timeout=60)
        if ev["type"] == "response.output_audio.delta":
            pcm += base64.b64decode(ev["delta"])
        elif ev["type"] == "response.output_audio_transcript.delta":
            transcript.append(ev["delta"])
        elif ev["type"] == "response.done":
            break
    await live.close()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(bytes(pcm))
    print("".join(transcript), f"\n{len(pcm)/48000:.1f} s of audio")
    display(Audio(buf.getvalue(), rate=24000))
else:
    print("Set OPENAI_API_KEY to hear real audio. (Skipped.)")

# %% [markdown]
# ## Where the Realtime model stops
#
# - It **proposes** tool calls; it never executes them (next notebook).
# - It has **no durable memory**: everything it knows is in the item list you (or the framework) maintain.
# - Instructions are **soft**. Anything that must never be said or done needs enforcement outside the model.
# - It doesn't know what the caller actually **heard**. The client must truncate.
# - It can't un-say audio. Policies about speech must act *before* generation.
#
# ## Exercises
#
# 1. Re-run section 3 with a longer, messier caller utterance. Does the effort/latency curve change shape?
# 2. In section 4, set `interrupt_response: False` and re-run. What happens to the greeting? When would you want that?
# 3. Set `create_response: False`. Now *your* code must decide when to call `response.create`. Why might a control plane want that power (hint: emergency screening before the model replies)?

# %% [markdown]
# ## Check your understanding
#
# 1. What is the difference between a conversation item and a response?
# 2. Why must local audio playout be stopped on cancellation?
# 3. What does `conversation.item.truncate` reconcile?
#
# **Graded exercise:** modify the simulator turn so the caller interrupts after a
# different number of words, then assert that the stored assistant transcript contains
# no more words than were actually played. See [`solutions/01_realtime_protocol.md`](../solutions/01_realtime_protocol.md).
