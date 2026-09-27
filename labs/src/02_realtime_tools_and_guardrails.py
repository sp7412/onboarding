# %% [markdown]
# # 02 · Tool calling and the control-plane boundary
#
# **Goal:** build the loop that sits between a realtime model and your backend, and put the guardrails where they actually hold: in code, at the tool boundary, keyed off state the application owns.
#
# You will:
# 1. declare tools in the session and watch the model propose calls
# 2. write the tool loop by hand (then reuse `stlab.loop`)
# 3. run a full booking call
# 4. break things on purpose: guardrails off vs. on, ungrounded confirmations, emergencies, retries, slow tools
# 5. gate tools by call phase with `session.update`
#
# Works live (`gpt-realtime-2`) or on the simulator. The simulator's "model" is deliberately a bit reckless so the guardrails have something to catch. A real model will be more careful *most* of the time, and "most of the time" is the problem guardrails solve.

# %%
import asyncio, json, time
import stlab
from stlab import backend as be
from stlab.tools import TOOL_SCHEMAS, CallState, execute_tool
from stlab.realtime import connect, EventPrinter

stlab.load_env()
LIVE = None
be.LATENCY_MS.update({"lookup_customer": 120, "find_slots": 450, "create_job": 300})

INSTRUCTIONS = """You are the phone assistant for Benbrook Comfort Services (HVAC + plumbing).
Caller ID: {caller_id}
- Look the caller up by caller ID first.
- Find out what's wrong, then offer at most two appointment windows.
- Before booking, read the service address back and get an explicit yes; then call
  record_address_confirmation with the caller's exact words, then create_job.
- If anything suggests gas, smoke, sparks, CO, or flooding: give a one-sentence safety
  instruction and transfer_to_human immediately.
- Keep every reply to one or two short sentences. Never quote prices."""

# %% [markdown]
# ## 1. Tools are just JSON schemas in the session

# %%
print(json.dumps(TOOL_SCHEMAS[2], indent=2))

# %% [markdown]
# ## 2. The tool loop, by hand
#
# When a response finishes (`response.done`) and its `output` contains `function_call` items, the model is waiting on you. For each call:
#
# 1. parse `arguments` (a JSON *string*, possibly malformed)
# 2. **decide** whether to run it: this is the control plane
# 3. run it, then send a `function_call_output` item with the same `call_id`
#
# Then send `response.create` so the model can speak about the result. The model may emit several calls in one response (parallel tool calls); here we execute them in order.

# %%
async def tool_loop(conn, state, printer, enforce=True, idle_timeout=30):
    while True:
        ev = await conn.recv(timeout=idle_timeout)
        printer(ev)
        if ev["type"] == "conversation.item.input_audio_transcription.completed":
            state.last_user_text = ev["transcript"]
        if ev["type"] != "response.done":
            continue
        resp = ev["response"]
        calls = [o for o in resp.get("output", []) if o.get("type") == "function_call"]
        if resp["status"] != "completed" or not calls:
            return
        for c in calls:
            result = await asyncio.to_thread(execute_tool, c["name"], c["arguments"], state, enforce=enforce)
            if printer.__class__ is EventPrinter:
                print(f"           ↳ app executed {c['name']} → {json.dumps(result)[:110]}")
            await conn.send({"type": "conversation.item.create", "item": {
                "type": "function_call_output", "call_id": c["call_id"], "output": json.dumps(result)}})
        await conn.send({"type": "response.create"})

async def caller(conn, state, text, printer, **kw):
    print(f"\n📞 CALLER: {text}")
    state.last_user_text = text           # the app records what was actually said
    await conn.send({"type": "conversation.item.create", "item": {
        "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}})
    await conn.send({"type": "response.create"})
    await tool_loop(conn, state, printer, **kw)

async def new_call(caller_id="+18175550142", call_id="call-001", enforce=True, printer=None):
    conn = await connect(live=LIVE)
    await conn.recv(timeout=10)                      # session.created
    printer = printer or EventPrinter()
    await conn.send({"type": "session.update", "session": {
        "type": "realtime", "output_modalities": ["text"], "tools": TOOL_SCHEMAS, "tool_choice": "auto",
        "instructions": INSTRUCTIONS.format(caller_id=caller_id)}})
    state = CallState(call_id=call_id)
    # have the agent open the call (it should look up the caller ID)
    await conn.send({"type": "response.create"})
    await tool_loop(conn, state, printer, enforce=enforce)
    return conn, state, printer

# %% [markdown]
# ## 3. A complete booking call

# %%
be.reset()
conn, st, p = await new_call()
await caller(conn, st, "Hi, my furnace isn't putting out any heat.", p)
await caller(conn, st, "The first one works.", p)
await caller(conn, st, "Yes, that's correct.", p)
await conn.close()
print("\nphase:", st.phase, "| booked:", st.booked_job and st.booked_job["id"])

# %% [markdown]
# Scroll up and find the moment the model tried `create_job` right after "The first one works", **before** confirming the address. The control plane returned `address_not_confirmed`, and the model turned that into the right question. That is the pattern:
#
# > Prompt = how the agent *should* behave. Tool boundary = what the agent *can* do.

# %%
for c in st.tool_calls:
    ok = c["result"].get("ok")
    print(f"{'✓' if ok else '✗'} {c['name']:<28} {c['result'].get('error', '')}")

# %% [markdown]
# ## 4. Break it on purpose
#
# ### 4a. Guardrails off
#
# Same conversation with `enforce=False`: the application trusts the model.

# %%
be.reset()
conn, st_off, p = await new_call(enforce=False, call_id="call-002")
await caller(conn, st_off, "Hi, my furnace isn't putting out any heat.", p, enforce=False)
await caller(conn, st_off, "The first one works.", p, enforce=False)
await conn.close()
print("\nBooked without address confirmation?", bool(st_off.booked_job), "| address_confirmed =", st_off.address_confirmed)

# %% [markdown]
# ### 4b. Ungrounded confirmations
#
# `record_address_confirmation` requires a quote from the caller. The control plane checks that the quote appears in what the caller *actually said* (`state.last_user_text`, which comes from the transcript, not from the model). This catches a model that "remembers" a yes that never happened.

# %%
st4 = CallState(last_user_text="Hmm, actually I moved last month.")
print(execute_tool("record_address_confirmation", {"caller_said": "yes that's right"}, st4))
st4.last_user_text = "Yes, that's right."
print(execute_tool("record_address_confirmation", {"caller_said": "yes, that's right"}, st4))

# %% [markdown]
# ### 4c. Emergencies: the application screens *before* the model replies
#
# You can't rely on instructions for life-safety. Here the app checks each caller utterance with `be.detect_emergency` **before** asking the model to respond, flips `state.emergency`, and swaps the tool set down to `transfer_to_human` only. Then even a model that ignores the instruction can't book a routine visit.

# %%
TOOLS_BY_NAME = {t["name"]: t for t in TOOL_SCHEMAS}

async def screened_caller(conn, state, text, printer):
    if be.detect_emergency(text) and not state.emergency:
        state.emergency = True
        print("🚨 control plane: emergency detected → restricting tools")
        await conn.send({"type": "session.update", "session": {"type": "realtime",
            "tools": [TOOLS_BY_NAME["transfer_to_human"]],
            "instructions": "Possible emergency. Tell the caller to leave the home if they smell gas and call 911 "
                            "from outside, then call transfer_to_human. Say nothing else."}})
    await caller(conn, state, text, printer)

be.reset()
conn, st_e, p = await new_call(call_id="call-003")
await screened_caller(conn, st_e, "My AC is out, and also there's kind of a gas smell by the furnace.", p)
await conn.close()
print("\ntransferred:", st_e.transferred, "| booked:", bool(st_e.booked_job))

# %% [markdown]
# ### 4d. Retries and idempotency
#
# The tool call times out on your side, but the backend committed. Your loop retries. Because the idempotency key is `call_id + slot_id` (built by the app in `_dispatch`), the retry returns the same job.

# %%
be.reset()
st5 = CallState(call_id="call-004")
execute_tool("lookup_customer", {"phone": "8175550142"}, st5)
execute_tool("find_slots", {"job_type": "water_heater", "zip_code": "76126"}, st5)
st5.address_confirmed = True
args = {"customer_id": "C-1002", "slot_id": st5.offered_slot_ids[0], "job_type": "water_heater", "summary": "no hot water"}
a = execute_tool("create_job", args, st5)
b = execute_tool("create_job", args, st5)   # retry
print(a["job"]["id"], b["job"]["id"], "replayed:", b["job"].get("replayed"), "| jobs:", len(be.jobs()))

# %% [markdown]
# ### 4e. Slow tools and dead air
#
# Crank `find_slots` to 2.5 s and measure two gaps after the caller's turn ends:
#
# - **first words:** when the caller first hears *anything*
# - **useful words:** when they hear the actual answer
#
# A spoken **preamble** ("One moment while I check…") keeps the first gap small even when the second is large. `gpt-realtime-2` can emit preambles while tools run; the simulator does it too.

# %%
async def measure(latency_ms):
    be.reset(); be.LATENCY_MS["find_slots"] = latency_ms
    conn, st, _ = await new_call(call_id=f"lat-{latency_ms}", printer=lambda ev: None)
    quiet = EventPrinter(); quiet_print = lambda ev: quiet.events.append((time.perf_counter(), ev))
    t0 = time.perf_counter()
    await caller(conn, st, "My AC is blowing warm air.", quiet_print)
    await conn.close()
    deltas = [t for t, e in quiet.events if e["type"].endswith("text.delta")]
    first = (deltas[0] - t0) * 1000
    after_tool = [t for t, e in quiet.events if e["type"] == "response.created"]
    useful = (after_tool[-1] - t0) * 1000 if len(after_tool) > 1 else first
    return first, useful

for ms in [200, 1000, 2500]:
    f, u = await measure(ms)
    print(f"find_slots={ms:>5} ms   first words after {f:6.0f} ms   useful answer starts after {u:6.0f} ms")
be.LATENCY_MS["find_slots"] = 450

# %% [markdown]
# ## 5. Phase-based tool gating
#
# Fewer tools = fewer wrong calls. The application knows the call phase (`state.phase`) and can expose only the tools that make sense. Here's a policy you might run after every tool result:

# %%
PHASE_TOOLS = {
    "identify": ["lookup_customer", "transfer_to_human"],
    "diagnose": ["find_slots", "transfer_to_human"],
    "schedule": ["find_slots", "record_address_confirmation", "create_job", "transfer_to_human"],
    "done":     ["transfer_to_human"],
}

def session_tools_for(state):
    return [TOOLS_BY_NAME[n] for n in PHASE_TOOLS[state.phase]]

for ph in PHASE_TOOLS:
    print(f"{ph:<9}", [t["name"] for t in session_tools_for(CallState(phase=ph))])

# %% [markdown]
# **Exercise:** wire `session_tools_for` into `tool_loop` so that after each batch of tool results the loop sends a `session.update` with the new tool list before `response.create`. What breaks if the model still has a pending plan that uses a tool you just removed?
#
# ## Where the model stops and the control plane begins
#
# | The model decides | The control plane decides |
# |---|---|
# | which tool to *ask* for and with what args | whether the call is allowed right now |
# | how to phrase things | which facts are authoritative (record beats model guess) |
# | when it thinks the caller confirmed | whether the confirmation is grounded in the transcript |
# | that it wants to retry | how retries stay idempotent |
# | (nothing about emergencies, reliably) | screening, tool lock-down, escalation |
#
# ## Exercises
#
# 1. Add a `max 2 slot offers per call` rule. Where does the counter live?
# 2. Make `create_job` fail randomly 20% of the time (`be.create_job` raising). What should the agent say, and after how many failures should the control plane force `transfer_to_human`?
# 3. With a live key, remove the address-confirmation sentence from `INSTRUCTIONS` and run section 3 five times. How often does the model try to book early? That count is exactly what an evaluator in notebook 07 should measure.

# %% [markdown]
# ## Check your understanding
#
# 1. Which facts should come from the backend rather than the model?
# 2. Why is transcript grounding stronger than a model's paraphrase?
# 3. What should happen when a tool times out after committing its side effect?
#
# **Graded exercise:** add a maximum-offered-slots policy and assert that a request for
# more slots returns a structured policy error. Solution: [`solutions/02_realtime_tools_and_guardrails.md`](../solutions/02_realtime_tools_and_guardrails.md).
