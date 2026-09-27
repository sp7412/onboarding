# %% [markdown]
# # 04 · LiveKit Agents: the real-time transport
#
# **Goal:** put the pieces from notebooks 01–03 onto a real media stack. LiveKit carries audio between a caller (browser via WebRTC, or phone via SIP) and your agent, runs VAD/turn detection/interruptions, and gives you an `AgentSession` that wires a model to the room.
#
# Voice workers don't run *inside* Jupyter (they need a long-lived process and an audio device), so this notebook:
#
# 1. explains the object model
# 2. **writes** three agent programs into `agents/` with `%%writefile`
# 3. tells you how to run them from a terminal (`console` = your laptop mic/speaker; `dev` = connect to LiveKit Cloud)
# 4. runs LiveKit's **text-mode test harness** in the notebook, which exercises the same Agent class, tools, and handoffs without audio
#
# Requirements: `livekit-agents[openai,silero,turn-detector]` (1.x). For `dev` mode and the cascaded pipeline you need a LiveKit Cloud project (free tier) and `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`. The realtime agent also needs `OPENAI_API_KEY`.
#
# API names below match `livekit-agents` 1.8. LiveKit moves quickly, so check docs.livekit.io/agents if an import fails.

# %% [markdown]
# ## 1. Object model
#
# | Concept | What it is |
# |---|---|
# | **Room** | one call. Participants join it. |
# | **Participant / Track** | the caller (SIP or WebRTC) and the agent each publish/subscribe audio tracks |
# | **AgentServer** | a worker process that registers with LiveKit and gets **dispatched** into rooms |
# | **JobContext** | per-room handle given to your entrypoint (`ctx.room`, `ctx.proc`, …) |
# | **AgentSession** | the voice pipeline for one call: STT/LLM/TTS or a realtime model, VAD, turn handling, interruptions, and `userdata` (your per-call state) |
# | **Agent** | instructions + tools (`@function_tool`) + optional per-agent overrides. A tool can return another Agent to **hand off** control. |
# | **RunContext** | passed to tools; `context.userdata` is your `CallState` |
#
# The Agent/tools are where your control plane plugs in. Everything else is transport.

# %%
import os, sys, pathlib
import stlab
stlab.load_env(); stlab.status()
pathlib.Path("agents").mkdir(exist_ok=True)

# %% [markdown]
# ## 2. Agent #1: realtime (speech-to-speech) booking agent
#
# Note how thin the tools are: each one calls `execute_tool`, the same guarded dispatcher from notebook 02. LiveKit doesn't need to know any business rules.
#
# Two control-plane hooks are wired through session **events**:
# - `user_input_transcribed` → record what the caller actually said (grounding) and screen for emergencies
# - `metrics_collected` → per-turn latency metrics (end-of-utterance delay, time to first token/audio)

# %%
%%writefile agents/realtime_agent.py
"""Realtime (speech-to-speech) booking agent.

    python agents/realtime_agent.py console   # talk to it with your mic/speakers
    python agents/realtime_agent.py dev       # join LiveKit Cloud; use the Agents Playground
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # so `stlab` imports

from livekit.agents import (Agent, AgentServer, AgentSession, JobContext, MetricsCollectedEvent, RunContext,
                            cli, function_tool, metrics)
from livekit.plugins import openai

from stlab import backend as be
from stlab import load_env
from stlab.tools import CallState, execute_tool

load_env()
log = logging.getLogger("booking-agent")

INSTRUCTIONS = """You are the phone assistant for Benbrook Comfort Services (HVAC and plumbing).
Speak in short, warm sentences. Look the caller up first, find out what's wrong, offer at most
two appointment windows, read the address back and get a clear yes, then book.
If you need a moment for a tool, say so briefly. Never quote prices.
If anything suggests gas, smoke, sparks, carbon monoxide, or flooding, give one safety
sentence and transfer to a human."""


class BookingAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)

    async def on_enter(self) -> None:
        # Agent speaks first when it takes control of the session
        await self.session.generate_reply(instructions="Greet the caller and ask how you can help.")

    @function_tool
    async def lookup_customer(self, context: RunContext[CallState], phone: str) -> dict:
        """Look up a customer by phone number."""
        return await asyncio.to_thread(execute_tool, "lookup_customer", {"phone": phone}, context.userdata)

    @function_tool
    async def find_slots(self, context: RunContext[CallState], job_type: str, zip_code: str) -> dict:
        """Find open appointment windows. job_type is one of ac_repair, furnace_repair, hvac_tuneup,
        water_heater, leak_repair."""
        return await asyncio.to_thread(execute_tool, "find_slots",
                                       {"job_type": job_type, "zip_code": zip_code}, context.userdata)

    @function_tool
    async def record_address_confirmation(self, context: RunContext[CallState], caller_said: str) -> dict:
        """Call when the caller confirms the service address you read back. Quote their exact words."""
        return execute_tool("record_address_confirmation", {"caller_said": caller_said}, context.userdata)

    @function_tool
    async def create_job(self, context: RunContext[CallState], customer_id: str, slot_id: str,
                         job_type: str, summary: str) -> dict:
        """Book the job in an offered slot after the address is confirmed."""
        # A booking commit should not be cut off halfway by a barge-in:
        context.disallow_interruptions()
        return await asyncio.to_thread(execute_tool, "create_job", {
            "customer_id": customer_id, "slot_id": slot_id, "job_type": job_type, "summary": summary},
            context.userdata)

    @function_tool
    async def transfer_to_human(self, context: RunContext[CallState], reason: str) -> dict:
        """Transfer the caller to a human customer service rep."""
        # Production: warm transfer via LiveKit SIP (SIP REFER or bridging a CSR into the room).
        return execute_tool("transfer_to_human", {"reason": reason}, context.userdata)


server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    state = CallState(call_id=ctx.room.name)
    session = AgentSession[CallState](
        llm=openai.realtime.RealtimeModel(model="gpt-realtime-2", voice="marin"),
        userdata=state,
    )

    @session.on("user_input_transcribed")
    def _on_transcript(ev):
        if not ev.is_final:
            return
        state.last_user_text = ev.transcript
        if be.detect_emergency(ev.transcript) and not state.emergency:
            state.emergency = True   # execute_tool now blocks everything but transfer_to_human
            log.warning("emergency language detected: %r", ev.transcript)

    usage = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage.collect(ev.metrics)

    async def _summary():
        log.info("call %s done: phase=%s booked=%s usage=%s", state.call_id, state.phase,
                 state.booked_job and state.booked_job["id"], usage.get_summary())
    ctx.add_shutdown_callback(_summary)

    await session.start(agent=BookingAgent(), room=ctx.room)


if __name__ == "__main__":
    cli.run_app(server)

# %% [markdown]
# ## 3. Agent #2: cascaded pipeline (STT → LLM → TTS)
#
# Same Agent class, different session. You gain a **text checkpoint** between hearing and speaking (you can inspect, redact, or filter), a choice of providers per stage, and semantic turn detection. The cost is more hops and usually more latency.
#
# The model strings (`"deepgram/nova-3"`, `"openai/gpt-5.4-mini"`, `"cartesia/sonic-3"`) use **LiveKit Inference**, billed through your LiveKit Cloud project, so no separate provider keys are needed. You can also pass plugin objects (`openai.STT()`, etc.).

# %%
%%writefile agents/cascaded_agent.py
"""Cascaded STT -> LLM -> TTS version of the booking agent, with explicit turn handling.

    python agents/cascaded_agent.py download-files   # first time: VAD + turn-detector weights
    python agents/cascaded_agent.py console
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from livekit.agents import AgentServer, AgentSession, JobContext, JobProcess, cli
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from stlab import load_env
from stlab.tools import CallState

from realtime_agent import BookingAgent  # reuse the exact same Agent + tools

load_env()
server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()   # load once per worker process, not per call


server.setup_fnc = prewarm


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession[CallState](
        stt="deepgram/nova-3",
        llm="openai/gpt-5.4-mini",
        tts="cartesia/sonic-3",
        vad=ctx.proc.userdata["vad"],
        turn_detection=MultilingualModel(),              # semantic end-of-turn (notebook 03 §3)
        turn_handling={
            "endpointing": {"min_delay": 0.5, "max_delay": 3.0},
            "interruption": {"enabled": True, "min_duration": 0.5, "resume_false_interruption": True},
            "preemptive_generation": {"enabled": True},  # start the LLM before the turn is final
        },
        userdata=CallState(call_id=ctx.room.name),
    )
    await session.start(agent=BookingAgent(), room=ctx.room)


if __name__ == "__main__":
    cli.run_app(server)

# %% [markdown]
# ## 4. Agent #3: handoffs (intake → booking)
#
# A tool that **returns an Agent** hands the session to it. Each agent can have narrower instructions and a smaller tool set: phase-based tool gating (notebook 02 §5), expressed as agents.

# %%
%%writefile agents/handoff_agent.py
"""Intake agent that triages, then hands off to the booking agent (or a human)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from livekit.agents import Agent, AgentServer, AgentSession, JobContext, RunContext, cli, function_tool
from livekit.plugins import openai

from stlab import load_env
from stlab.tools import CallState, execute_tool

from realtime_agent import BookingAgent

load_env()


class IntakeAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=(
            "You answer calls for Benbrook Comfort Services. Find out, in one or two questions, whether the "
            "caller needs to book service, has a billing question, or has an emergency. Then call the matching tool."))

    async def on_enter(self):
        await self.session.generate_reply(instructions="Greet the caller and ask what they need today.")

    @function_tool
    async def start_booking(self, context: RunContext[CallState], problem: str):
        """The caller wants to schedule service. `problem` is a short description."""
        context.userdata.phase = "identify"
        return BookingAgent(), f"Handing off to booking. Problem: {problem}"

    @function_tool
    async def billing_question(self, context: RunContext[CallState]):
        """The caller has a billing question (not handled by the voice agent)."""
        return execute_tool("transfer_to_human", {"reason": "billing"}, context.userdata)


server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession[CallState](llm=openai.realtime.RealtimeModel(model="gpt-realtime-2"),
                                      userdata=CallState(call_id=ctx.room.name))
    await session.start(agent=IntakeAgent(), room=ctx.room)


if __name__ == "__main__":
    cli.run_app(server)

# %% [markdown]
# ### Sanity check: do the files import?
#
# This only imports and constructs classes (no network), so it runs without keys.

# %%
import importlib, os
sys.path.insert(0, str(pathlib.Path("agents").resolve()))
os.environ.setdefault("OPENAI_API_KEY", "sk-placeholder-for-import-only") if not stlab.have("openai") else None
for mod in ["realtime_agent", "handoff_agent"]:
    m = importlib.import_module(mod)
    print("imported", mod, "→", [n for n in dir(m) if n.endswith("Agent") and n != "Agent"])
agent = m.BookingAgent()
print("BookingAgent tools:", sorted(t.info.name if hasattr(t, "info") else getattr(t, "name", str(t)) for t in agent.tools))

# %% [markdown]
# ## 5. Run them (terminal)
#
# ```bash
# cd <this folder>
# python agents/cascaded_agent.py download-files   # once
# python agents/realtime_agent.py console          # local mic + speakers, no LiveKit server needed for audio I/O
# python agents/realtime_agent.py dev              # registers with LiveKit Cloud; open the Agents Playground
# ```
#
# Things to try while talking to it, mapped to earlier notebooks:
#
# | Try | Watch for | Notebook |
# |---|---|---|
# | read your phone number slowly with pauses | premature cut-offs; compare realtime vs. cascaded (semantic turn detector) | 03 |
# | say "uh-huh" while it's talking | does it stop? resume? | 03 |
# | interrupt mid-sentence, then ask "what did you just say?" | does it know what you actually heard (truncation)? | 01 |
# | "the first one works" before confirming the address | `address_not_confirmed` in logs, and the agent asks for the address | 02 |
# | mention a gas smell | emergency flag → only transfer allowed | 02 |
# | watch the `metrics` log lines | end-of-utterance delay, TTFT, TTS first byte | 08 |
#
# **Telephony:** in LiveKit Cloud, create an inbound SIP trunk (e.g. from Twilio/Telnyx) and a dispatch rule that routes calls into rooms where your agent is dispatched. The caller then becomes a SIP participant, and your code doesn't change.
#
# ## 6. Test the agent in text mode (in the notebook)
#
# LiveKit ships a test harness: `session.run(user_input=...)` drives one turn through the Agent (tools, handoffs) using a *text* LLM, and `result.expect` makes assertions about the events. This is how you'd unit-test agent behavior in CI. Needs `OPENAI_API_KEY`.

# %%
from livekit.agents import AgentSession
from livekit.plugins import openai as lk_openai
from stlab import backend as be
from stlab.tools import CallState

if stlab.have("openai") and not os.environ["OPENAI_API_KEY"].startswith("sk-placeholder"):
    from realtime_agent import BookingAgent
    be.reset(); be.LATENCY_MS.update({k: 0 for k in be.LATENCY_MS})
    class TestBookingAgent(BookingAgent):
        async def on_enter(self):   # skip the spoken greeting in tests
            pass
    state = CallState(call_id="test-1")
    async with lk_openai.LLM(model="gpt-5.4-mini") as llm, AgentSession(llm=llm, userdata=state) as session:
        await session.start(TestBookingAgent())
        r = await session.run(user_input="Hi, my number is 817-555-0142 and my water heater is leaking.")
        print(r.events)  # inspect everything that happened this turn
        r.expect.contains_function_call(name="lookup_customer")
        text = "I smell gas in the garage!"
        state.emergency = be.detect_emergency(text)   # the app screens before the model's turn
        r2 = await session.run(user_input=text)
        await r2.expect.next_event(type="message").judge(llm, intent="gives a safety instruction")
    print("phase:", state.phase, "| tool calls:", [c["name"] for c in state.tool_calls])
else:
    print("Set OPENAI_API_KEY to run the LiveKit text-mode test harness. (Skipped.)")

# %% [markdown]
# `judge()` uses an LLM to grade intent, a small built-in LLM-as-judge. Notebook 07 does the same thing at dataset scale with LangSmith.
#
# ## Where LiveKit stops
#
# - It moves audio, detects turns, and handles interruptions. It does not know your booking rules.
# - `userdata` holds your per-call state, but LiveKit doesn't persist it. When the call ends it's gone unless your control plane writes it somewhere.
# - Metrics are about the pipeline (EOU delay, TTFT, TTS TTFB). Business outcomes (booked? escalated correctly?) are yours to define and log.
# - When a realtime model with server-side turn detection is used, some LiveKit interruption settings are ignored. Know which layer owns the turn decision.
#
# ## Exercises
#
# 1. Run both `realtime_agent.py` and `cascaded_agent.py` in console mode and log end-of-speech → first-audio for 10 turns each. Fill in the latency worksheet in the study guide.
# 2. Add a `session.say("This call may be recorded for quality.", allow_interruptions=False)` disclosure at the start. Where should the decision to play it live?
# 3. Add a `BillingAgent` handoff with its own tools. What `CallState` should carry across the handoff, and what should not?
