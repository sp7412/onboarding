# %% [markdown]
# # 08 · Capstone: talker + thinker + control plane + observability
#
# **Goal:** assemble the full architecture and answer the study question with evidence.
#
# ```
#   caller ⇄ [transport] ⇄ TALKER (realtime model)          fast, conversational, no business logic
#                              │ advance_booking(...)
#                              ▼
#                     CONTROL PLANE (this notebook)          identity from caller ID, verbatim transcript,
#                              │                             emergency screening, filler policy, tracing
#                              ▼
#                     THINKER (LangGraph workflow, nb 06)    owns the process + backend calls
# ```
#
# You will:
# 1. wire the realtime talker to the LangGraph thinker through a single tool
# 2. discover why the control plane must pass the **verbatim transcript**, not the model's paraphrase
# 3. hide slow thinking with **control-plane filler** and measure the latency budget
# 4. trace the whole thing (talker spans + graph node spans in one tree)
# 5. write your one-page answer to the study question
#
# Offline on the simulator by default; live with `OPENAI_API_KEY` (and LangSmith traces with `LANGSMITH_API_KEY`).

# %%
import asyncio, json, time, os, warnings, contextlib, logging
warnings.filterwarnings("ignore")
import stlab
from stlab import backend as be
from stlab import booking_graph as bg
from stlab.tools import CallState
from stlab.realtime import connect, EventPrinter

stlab.load_env()
LIVE = None
LS_LIVE = stlab.have("langsmith")
if LS_LIVE:
    os.environ["LANGSMITH_TRACING"] = "true"; os.environ.setdefault("LANGSMITH_PROJECT", "st-voice-labs")
else:
    logging.getLogger("langsmith").setLevel(logging.CRITICAL)

TALKER_INSTRUCTIONS = """You are the voice of Benbrook Comfort Services. You do not make decisions about
scheduling. Every time the caller speaks, call advance_booking with what they said, then say the
returned `say` text naturally and briefly. If the tool says done=true, wrap up politely."""

TALKER_TOOLS = [
    {"type": "function", "name": "advance_booking",
     "description": "Advance the booking workflow with what the caller just said. Returns {say, done, outcome}.",
     "parameters": {"type": "object", "properties": {"caller_said": {"type": "string"}}, "required": ["caller_said"]}},
]

# %% [markdown]
# ## 1. The control plane object
#
# One `Call` per phone call. It owns: identity (caller ID from the transport, never from the model), the workflow thread, the verbatim transcript, and the timing log.

# %%
from dataclasses import dataclass, field

@dataclass
class Call:
    call_id: str
    caller_id: str
    graph: object
    use_verbatim: bool = True            # pass transcript (True) or the model's paraphrase (False) to the thinker
    filler_after_ms: int | None = None   # speak a filler if the thinker is slower than this
    state: CallState = None
    started: bool = False
    timings: list = field(default_factory=list)

    def __post_init__(self):
        self.state = CallState(call_id=self.call_id)

    def think(self, model_arg: str) -> dict:
        """Tool implementation for advance_booking. Runs in a worker thread."""
        if not self.started:
            self.started = True
            return bg.advance(self.graph, self.call_id, caller_phone=self.caller_id)   # identity from caller ID
        words = self.state.last_user_text if self.use_verbatim else model_arg
        return bg.advance(self.graph, self.call_id, caller_said=words)

# %% [markdown]
# ## 2. The talker loop, with filler
#
# Same shape as notebook 02, plus one control-plane policy: if the thinker hasn't answered within `filler_after_ms`, send an **out-of-band** `response.create` (instructions override, no tools) so the caller hears something like "One moment while I check the schedule." Then deliver the real tool output.
#
# Timing marks per caller turn: `t0` = turn committed; `first_audio` = first spoken token of anything; `answer_audio` = first token of the response *after* the thinker returned.

# %%
async def drain_response(conn, on_event, marks, key):
    while True:
        ev = await conn.recv(timeout=30); on_event(ev)
        if ev["type"].endswith("text.delta") or ev["type"].endswith("transcript.delta"):
            marks.setdefault(key, time.perf_counter())
        if ev["type"] == "response.done":
            return ev["response"]

async def talker_turn(conn, call: Call, text: str, on_event=lambda e: None):
    marks = {"t0": time.perf_counter()}
    call.state.last_user_text = text
    if text and be.detect_emergency(text):
        call.state.emergency = True           # the graph will escalate too; this flag is for the app's own policy
    if text:
        await conn.send({"type": "conversation.item.create", "item": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}})
    await conn.send({"type": "response.create"})
    spoken = []
    while True:
        resp = await drain_response(conn, on_event, marks, "first_audio")
        calls = [o for o in resp.get("output", []) if o.get("type") == "function_call"]
        spoken += [c.get("text") or c.get("transcript", "") for o in resp.get("output", [])
                   if o.get("type") == "message" for c in o.get("content", [])]
        if not calls:
            break
        for c in calls:
            model_arg = json.loads(c["arguments"]).get("caller_said", "")
            task = asyncio.create_task(asyncio.to_thread(call.think, model_arg))
            if call.filler_after_ms is not None:
                done, _ = await asyncio.wait({task}, timeout=call.filler_after_ms / 1000)
                if not done:
                    await conn.send({"type": "response.create", "response": {
                        "conversation": "none", "tools": [], "output_modalities": ["text"],
                        "instructions": "Say exactly: One moment while I check that for you."}})
                    await drain_response(conn, on_event, marks, "first_audio")
                    spoken.append("[filler] One moment while I check that for you.")
            result = await task
            marks["thinker_done"] = time.perf_counter()
            await conn.send({"type": "conversation.item.create", "item": {
                "type": "function_call_output", "call_id": c["call_id"], "output": json.dumps(result)}})
        await conn.send({"type": "response.create"})
        resp = await drain_response(conn, on_event, marks, "answer_audio")
        spoken += [c.get("text") or c.get("transcript", "") for o in resp.get("output", [])
                   if o.get("type") == "message" for c in o.get("content", [])]
        if not [o for o in resp.get("output", []) if o.get("type") == "function_call"]:
            break
    if "answer_audio" in marks:   # whichever sound came first is what ended the dead air
        marks["first_audio"] = min(marks.get("first_audio", marks["answer_audio"]), marks["answer_audio"])
    ms = lambda k: round((marks[k] - marks["t0"]) * 1000) if k in marks else None
    call.timings.append({"caller": text, "first_audio_ms": ms("first_audio"),
                         "thinker_ms": ms("thinker_done"), "answer_audio_ms": ms("answer_audio")})
    return " ".join(s for s in spoken if s)

async def run_call(utterances, caller_id="+18175550142", call_id="cap-1", verbose=True, **kw):
    be.reset()
    call = Call(call_id=call_id, caller_id=caller_id, graph=bg.build(), **kw)
    conn = await connect(live=LIVE)
    await conn.recv(timeout=10)
    await conn.send({"type": "session.update", "session": {"type": "realtime", "output_modalities": ["text"],
                     "instructions": TALKER_INSTRUCTIONS, "tools": TALKER_TOOLS}})
    for text in [""] + utterances:
        said = await talker_turn(conn, call, text)
        if verbose:
            if text: print("CALLER:", text)
            print("AGENT: ", said)
    await conn.close()
    return call

call = await run_call(["My furnace is banging and there's no heat", "The first one works", "Yes, that's correct"])
print("\njobs:", [(j["id"], j["job_type"], j["window"]) for j in be.jobs()])

# %% [markdown]
# ## 3. Verbatim vs. paraphrase
#
# The talker model calls `advance_booking(caller_said=...)`. Models paraphrase ("The caller confirmed."). The thinker's yes/no parser, and any audit trail, need **what the caller actually said**, which the control plane has from the transcript. Run the same call trusting the model's argument:

# %%
call_p = await run_call(["My furnace is banging and there's no heat", "The first one works", "Yes, that's correct"],
                        call_id="cap-2", use_verbatim=False)
print("\njobs booked:", len(be.jobs()))

# %% [markdown]
# The paraphrase "The caller confirmed." isn't a yes to the parser, so the workflow escalated a perfectly good booking to a human. (With a live model the failure is subtler: usually fine, occasionally a summarized or "corrected" address.) **Rule:** tool arguments are the model's interpretation; the transcript is evidence. Pass evidence to the thinker and log both.
#
# ## 4. The latency budget
#
# Slow the thinker's slot search down and compare no filler vs. filler after 700 ms. What the caller experiences is `first_audio_ms`; what the business needs is `answer_audio_ms`.

# %%
import pandas as pd
rows = []
for find_ms in [300, 1500, 3000]:
    for filler in [None, 700]:
        be.LATENCY_MS.update({"lookup_customer": 100, "find_slots": find_ms, "create_job": 250})
        c = await run_call(["My AC is blowing warm air"], call_id=f"lat-{find_ms}-{filler}",
                           filler_after_ms=filler, verbose=False)
        t = c.timings[-1]
        rows.append({"find_slots_ms": find_ms, "filler": "on" if filler else "off",
                     "first_audio_ms": t["first_audio_ms"], "answer_audio_ms": t["answer_audio_ms"]})
lat = pd.DataFrame(rows); lat

# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 3.2))
labels = [f"{r.find_slots_ms}ms / filler {r.filler}" for r in lat.itertuples()]
ax.barh(labels, lat.answer_audio_ms, color="#ccc", label="until the answer")
ax.barh(labels, lat.first_audio_ms, color="#4C72B0", label="until first sound (dead air)")
ax.axvline(1000, ls="--", color="red", lw=1); ax.text(1010, -0.4, "~1 s target", color="red", fontsize=8)
ax.invert_yaxis(); ax.set_xlabel("ms after the caller's turn is committed"); ax.legend(fontsize=8)
plt.title("Filler doesn't make the thinker faster; it removes dead air"); plt.show()

# %% [markdown]
# Add transport time on top of these numbers (endpointing ~0.3–0.8 s from notebook 03, network and playout ~0.1–0.2 s) to get what the caller truly feels.
#
# | Stage | Owner | Lever |
# |---|---|---|
# | end of speech → turn committed | transport (LiveKit / server VAD) | endpointing delay, semantic turn detection |
# | turn → first model token | model | reasoning effort, prompt size, preambles |
# | tool call → result | control plane + thinker + backend | caching, parallel calls, precomputing slots at call start |
# | silence while waiting | control plane | filler policy, preambles |
# | token → audio at the caller | transport | TTS/codec, buffering |
#
# ## 5. One trace for the whole call
#
# Wrap each turn in a traced span. Because LangGraph is LangChain-native, its **node executions nest automatically** under the talker span, so one tree shows talker and thinker together.

# %%
from langsmith import traceable, tracing_context
TREES = []

@traceable(run_type="chain", name="voice_turn")
async def traced_turn(conn, call, text):
    return await talker_turn(conn, call, text)

async def run_traced(utterances, call_id="cap-traced"):
    be.reset(); be.LATENCY_MS.update({"lookup_customer": 100, "find_slots": 600, "create_job": 250})
    call = Call(call_id=call_id, caller_id="+18175550101", graph=bg.build(), filler_after_ms=700)
    conn = await connect(live=LIVE)
    await conn.recv(timeout=10)
    await conn.send({"type": "session.update", "session": {"type": "realtime", "output_modalities": ["text"],
                     "instructions": TALKER_INSTRUCTIONS, "tools": TALKER_TOOLS}})
    ctx = contextlib.nullcontext() if LS_LIVE else tracing_context(enabled="local")
    with ctx:
        for text in [""] + utterances:
            await traced_turn(conn, call, text, langsmith_extra={
                "metadata": {"thread_id": call_id, "agent_version": "capstone-v1"}, "on_end": TREES.append})
    await conn.close()
    return call

await run_traced(["The water heater is leaking", "second one", "yes"])

def show(run, depth=0, t0=None):
    t0 = t0 or run.start_time
    s = (run.start_time - t0).total_seconds() * 1000
    d = ((run.end_time or run.start_time) - run.start_time).total_seconds() * 1000
    noise = run.name.startswith(("Runnable", "ChannelWrite"))
    if not noise:
        print(f"{'  '*depth}{run.name:<22} +{s:6.0f}ms {d:6.0f}ms")
    for c in run.child_runs:
        show(c, depth + (0 if noise else 1), t0)

for r in TREES[1:3]:
    print(f"── caller: {r.inputs.get('text')!r}")
    show(r)

# %% [markdown]
# ## 6. Your answer to the study question
#
# > **Where does each component stop, and where does the application's own control plane, business logic, guardrails, and state management begin?**
#
# Fill this in from what you measured and broke in notebooks 01–08. (A starter is provided; rewrite it in your own words.)
#
# | Component | Owns | Stops at | Evidence from the labs |
# |---|---|---|---|
# | **LiveKit** | media transport, rooms, VAD, turn commit, barge-in, telephony, playout/truncation | *what* to say; whether an action is allowed; persistence | nb 03 trade-off curves; nb 04 agents reuse the same tools unchanged |
# | **Realtime model** | understanding speech, conversation, proposing tool calls, speaking | executing tools; authority over facts; memory beyond its items; knowing what was heard | nb 01 truncation; nb 02 early `create_job` attempts; nb 08 paraphrase |
# | **LangChain / LangGraph** | multi-step orchestration, durable workflow state, hooks, HITL | real-time turn-taking; system of record; defining the rules | nb 05 round-trip count; nb 06 structural guarantee + crash/resume |
# | **LangSmith** | traces, datasets, evaluators, experiments, monitoring | runtime enforcement; audio-layer timing (unless you emit it); what "good" means | nb 07 v0 vs v1; waterfall |
# | **Control plane (yours)** | identity, policy at the tool boundary, grounding/evidence, idempotency, emergency screening, phase gating, filler policy, redaction, escalation, success definitions | — | every guard that caught something |
#
# **My one-paragraph answer:**
#
# *…write it here…*
#
# ## 7. Stretch goals
#
# 1. **Live end to end:** make the talker a LiveKit `Agent` whose only tool is `advance_booking`, backed by `Call.think` (notebook 04 pattern). Measure the latency table again with real audio.
# 2. **Precompute:** start `find_slots` in the background as soon as `triage` classifies the job, before the caller finishes talking. What does that do to `answer_audio_ms`, and what does it cost when the caller changes their mind?
# 3. **Evaluate the capstone:** point notebook 07's `aevaluate` at `run_call` and add an evaluator for `first_audio_ms < 1000`.
# 4. **Write the README** for your GitHub capstone repo using the table above plus your measured numbers.
