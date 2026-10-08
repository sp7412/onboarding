# %% [markdown]
# # 05 · LangChain `create_agent`: tools, state, context, middleware
#
# **Goal:** use LangChain as the *orchestration* layer: the thing that runs a model ↔ tool loop, carries state, and gives you hooks (middleware) to enforce policy around every model and tool call.
#
# LangChain 1.x in one line: **agent = model + harness**, where the harness is the prompt, the tools, and middleware. `create_agent` builds that loop on the LangGraph runtime (so you get checkpointing, streaming, and interrupts for free).
#
# In a voice system, this loop usually sits **behind** the realtime model (as the implementation of a complex tool, a background "thinker", or post-call processing), not between the caller and the next spoken word. We'll measure why.
#
# **Offline:** uses `ScriptedChatModel`, a rule-based fake that emits tool calls. **Live:** set `OPENAI_API_KEY` and it uses a real model via `init_chat_model`.

# %%
import json, time, os
from dataclasses import dataclass
import stlab
from stlab import backend as be
from stlab.scripted_model import ScriptedChatModel

stlab.load_env()
be.reset(); be.LATENCY_MS.update({"lookup_customer": 50, "find_slots": 150, "create_job": 100})

from langchain.chat_models import init_chat_model
MODEL_NAME = os.environ.get("LC_MODEL", "openai:gpt-5.4-mini")
def make_model():
    return init_chat_model(MODEL_NAME) if stlab.have("openai") else ScriptedChatModel()
print("model:", MODEL_NAME if stlab.have("openai") else "ScriptedChatModel (offline)")

# %% [markdown]
# ## 1. The smallest useful agent
#
# Tools are plain functions with type hints and a docstring (the docstring becomes the description the model sees).

# %%
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def lookup_customer(phone: str) -> dict:
    """Look up a customer by phone number."""
    return {"ok": True, "customer": be.lookup_customer(phone)}

@tool
def find_slots(job_type: str, zip_code: str) -> dict:
    """Find open appointment windows. job_type: ac_repair | furnace_repair | hvac_tuneup | water_heater | leak_repair."""
    try:
        return {"ok": True, "slots": be.find_slots(job_type, zip_code)}
    except be.PolicyError as e:
        return e.as_dict()

SYSTEM = ("You schedule service calls for Benbrook Comfort Services. Look up the customer, "
          "then find slots. Offer the earliest slot. Be brief.")

agent = create_agent(make_model(), tools=[lookup_customer, find_slots], system_prompt=SYSTEM)
result = agent.invoke({"messages": [{"role": "user", "content": "My AC died. Number is 817-555-0142."}]})
for m in result["messages"]:
    m.pretty_print()

# %% [markdown]
# ## 2. Streaming the steps
#
# `stream_mode="updates"` yields one chunk per node (model step, tool step). This is how you'd surface progress to a UI or measure step latency.

# %%
t0 = time.perf_counter()
for chunk in agent.stream({"messages": [{"role": "user", "content": "Water heater's leaking, 817 555 0101"}]},
                          stream_mode="updates"):
    for node, update in chunk.items():
        last = update["messages"][-1]
        what = [c["name"] for c in getattr(last, "tool_calls", [])] or str(last.content)[:70]
        print(f"{(time.perf_counter()-t0)*1000:7.0f} ms  {node:<6} {what}")

# %% [markdown]
# Count the **model round-trips** in that trace. Each one is a full LLM call (hundreds of ms to seconds with a real model). A voice caller hears silence for the sum. That's the core argument for keeping multi-step agent loops *off* the realtime hot path, or masking them with a spoken preamble.
#
# ## 3. Runtime context vs. state
#
# | | **Context** (`context_schema`) | **State** (`state_schema`) |
# |---|---|---|
# | What | per-invocation facts the model shouldn't control | data that evolves during the run |
# | Examples | tenant ID, call ID, caller's verified phone, user permissions | messages, `address_confirmed`, offered slots |
# | Who writes | your application, at invoke time | tools/middleware (via `Command(update=...)`) |
# | Model can change it? | no | only through tools you wrote |
#
# Tools get both via `ToolRuntime`. The model never sees `runtime` as a parameter.

# %%
from langchain.tools import ToolRuntime
from langchain.agents import AgentState
from langchain_core.messages import ToolMessage
from langgraph.types import Command

@dataclass
class CallContext:
    tenant_id: str
    call_id: str
    caller_phone: str   # from SIP headers / caller ID: authoritative, not from the model

class BookingState(AgentState):
    customer_id: str | None
    offered_slot_ids: list[str]
    address_confirmed: bool

@tool
def lookup_caller(runtime: ToolRuntime[CallContext, BookingState]) -> Command:
    """Look up the current caller using their caller ID."""
    cust = be.lookup_customer(runtime.context.caller_phone)
    return Command(update={
        "customer_id": cust["id"] if cust else None,
        "messages": [ToolMessage(json.dumps({"ok": True, "customer": cust}), tool_call_id=runtime.tool_call_id)]})

@tool
def find_open_slots(job_type: str, runtime: ToolRuntime[CallContext, BookingState]) -> Command:
    """Find open slots for the caller's address. job_type: ac_repair | furnace_repair | hvac_tuneup | water_heater | leak_repair."""
    cust = be.lookup_customer(runtime.context.caller_phone)
    try:
        slots = be.find_slots(job_type, cust["zip"])
        payload = {"ok": True, "slots": slots}
    except be.PolicyError as e:
        slots, payload = [], e.as_dict()
    return Command(update={
        "offered_slot_ids": [s["id"] for s in slots],
        "messages": [ToolMessage(json.dumps(payload), tool_call_id=runtime.tool_call_id)]})

@tool
def confirm_address(runtime: ToolRuntime[CallContext, BookingState]) -> Command:
    """Record that the caller confirmed their service address out loud."""
    return Command(update={"address_confirmed": True, "messages": [
        ToolMessage('{"ok": true}', tool_call_id=runtime.tool_call_id)]})

@tool
def create_job(slot_id: str, job_type: str, summary: str, runtime: ToolRuntime[CallContext, BookingState]) -> dict:
    """Book the job in an offered slot."""
    key = f"{runtime.context.call_id}:{slot_id}"   # idempotency key from context, not from the model
    try:
        return {"ok": True, "job": be.create_job(runtime.state["customer_id"], slot_id, job_type, summary, key)}
    except be.PolicyError as e:
        return e.as_dict()

# %% [markdown]
# `create_job` reads `customer_id` from **state** (set by `lookup_caller`), not from a model argument. The model can't book for a different customer, because it's never asked which customer.
#
# ## 4. Middleware: policy around every call
#
# Hooks (decorators or `AgentMiddleware` subclasses):
#
# | Hook | Runs | Use it for |
# |---|---|---|
# | `before_model` / `after_model` | around each model step | inject facts, trim/summarize history, block unsafe outputs |
# | `wrap_model_call` | wraps the model call; can change the request | dynamic tool sets, model routing/fallback |
# | `wrap_tool_call` | wraps each tool execution | **authorization / precondition checks**, retries, auditing |
# | `before_agent` / `after_agent` | once per invocation | setup, final validation |
#
# Three middlewares for our booking agent:

# %%
from langchain.agents.middleware import wrap_tool_call, wrap_model_call, before_model, ToolCallLimitMiddleware

AUDIT = []

@wrap_tool_call
def booking_guard(request, handler):
    """Hard preconditions for create_job, enforced in code."""
    call, state = request.tool_call, request.state
    AUDIT.append((call["name"], call["args"]))
    if call["name"] == "create_job":
        problems = []
        if not state.get("customer_id"):
            problems.append("customer not identified")
        if not state.get("address_confirmed"):
            problems.append("address not confirmed")
        if call["args"].get("slot_id") not in (state.get("offered_slot_ids") or []):
            problems.append("slot was not offered to the caller")
        if problems:
            return ToolMessage(json.dumps({"ok": False, "error": "precondition_failed", "problems": problems}),
                               tool_call_id=call["id"], name=call["name"])
    return handler(request)

@wrap_model_call
def phase_tools(request, handler):
    """Only expose tools that make sense for where the call is."""
    s = request.state
    if not s.get("customer_id"):
        allowed = {"lookup_caller"}
    elif not s.get("offered_slot_ids"):
        allowed = {"find_open_slots"}
    else:
        allowed = {"find_open_slots", "confirm_address", "create_job"}
    tools = [t for t in request.tools if getattr(t, "name", None) in allowed]
    return handler(request.override(tools=tools))

@before_model(can_jump_to=["end"])
def emergency_screen(state, runtime):
    """Stop the loop entirely on emergency language; the application takes over."""
    last = state["messages"][-1]
    if last.type == "human" and be.detect_emergency(str(last.content)):
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage("If you smell gas, leave the home now and call 911 from outside. "
                                       "I'm connecting you to our emergency line.")],
                "jump_to": "end"}

# %% [markdown]
# Build the agent with context, state, middleware, and a checkpointer (so multiple caller turns share one thread).
#
# The offline `ScriptedChatModel` knows only the tool names from section 1, so for this part we give it a small policy that uses the new tool names.

# %%
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage, HumanMessage
import uuid, re

def v2_policy(messages, tool_names):
    last = messages[-1]
    humans = [m for m in messages if isinstance(m, HumanMessage)]
    said = str(humans[-1].content).lower() if humans else ""
    call = lambda n, a: AIMessage("", tool_calls=[{"name": n, "args": a, "id": "c_" + uuid.uuid4().hex[:6]}])
    if isinstance(last, ToolMessage):
        r = json.loads(last.content)
        if last.name in ("lookup_customer", "lookup_caller"):
            return AIMessage(f"Hi {r['customer']['name'].split()[0]}! What's going on?")
        if last.name in ("find_slots", "find_open_slots") and r.get("ok"):
            s = r["slots"][0]
            return AIMessage(f"Earliest is {s['weekday']} {s['start']} with {s['tech']} ({s['id']}). Book it?")
        if last.name == "confirm_address":
            return call("create_job", {"slot_id": LAST_OFFER[0], "job_type": "ac_repair", "summary": "AC not cooling"})
        if last.name == "create_job":
            return AIMessage(f"Result: {last.content[:120]}")
        return AIMessage(f"Tool said: {last.content[:120]}")
    if "lookup_caller" in tool_names:
        return call("lookup_caller", {})
    if "find_open_slots" in tool_names and "create_job" not in tool_names:
        return call("find_open_slots", {"job_type": "ac_repair"})
    m = re.search(r"s-\d{4}-t-\d{2}-\d{2}", said)
    if "yes" in said and "address" in said:
        return call("confirm_address", {})
    if "book" in said or "yes" in said:   # reckless: tries to book right away
        return call("create_job", {"slot_id": LAST_OFFER[0], "job_type": "ac_repair", "summary": "AC not cooling"})
    return AIMessage("Anything else?")
LAST_OFFER = [None]

model = init_chat_model(MODEL_NAME) if stlab.have("openai") else ScriptedChatModel(policy=v2_policy)
booking_agent = create_agent(
    model,
    tools=[lookup_caller, find_open_slots, confirm_address, create_job],
    system_prompt=("You book service for Benbrook Comfort Services. Use lookup_caller first. "
                   "Offer the earliest slot. Before create_job, read the address back and call confirm_address "
                   "only after the caller says yes."),
    context_schema=CallContext,
    state_schema=BookingState,
    middleware=[emergency_screen, phase_tools, booking_guard, ToolCallLimitMiddleware(run_limit=8)],
    checkpointer=InMemorySaver(),
)

be.reset(); AUDIT.clear()
ctx = CallContext(tenant_id="benbrook-comfort", call_id="call-777", caller_phone="+18175550142")
cfg = {"configurable": {"thread_id": ctx.call_id}}

def turn(text):
    out = booking_agent.invoke({"messages": [{"role": "user", "content": text}]}, config=cfg, context=ctx)
    LAST_OFFER[0] = (out.get("offered_slot_ids") or [None])[0]
    print(f"CALLER: {text}\nAGENT:  {out['messages'][-1].content}\n")
    return out

turn("Hi, it's Marcus.")
turn("My AC is blowing warm air.")
out = turn("Yes, book it.")                          # tries to book before address confirmation
out = turn("Yes, the address is right.")
print("state →", {k: out.get(k) for k in ["customer_id", "offered_slot_ids", "address_confirmed"]})
print("audit →", [n for n, _ in AUDIT])

# %%
emergency = booking_agent.invoke({"messages": [{"role": "user", "content": "wait, I smell gas in the kitchen"}]},
                                 config={"configurable": {"thread_id": "call-778"}}, context=ctx)
print(emergency["messages"][-1].content)

# %% [markdown]
# ## 5. Built-in middleware worth knowing
#
# - `SummarizationMiddleware`: compress long histories (long calls, multi-call memory)
# - `PIIMiddleware("email", strategy="redact")` / custom detectors: scrub before the model or before logging
# - `HumanInTheLoopMiddleware`: pause for approval on specific tools (e.g. refunds)
# - `ModelFallbackMiddleware`, `ModelRetryMiddleware`, `ToolRetryMiddleware`: resilience
# - `ModelCallLimitMiddleware`, `ToolCallLimitMiddleware`: budget guards against loops
# - `LLMToolSelectorMiddleware`: let a small model pick relevant tools when you have many
#
# A quick PII example with a custom phone-number detector:

# %%
from langchain.agents.middleware import PIIMiddleware
pii_agent = create_agent(make_model(), tools=[lookup_customer],
                         middleware=[PIIMiddleware("phone", detector=r"\b\d{3}[-. ]?\d{3}[-. ]?\d{4}\b",
                                                   strategy="mask", apply_to_input=True)])
r = pii_agent.invoke({"messages": [{"role": "user", "content": "call me back at 817-555-0199 please"}]})
print("what the model saw:", r["messages"][0].content)

# %% [markdown]
# Note the trade-off you just created: with the number masked, the model can no longer pass it to `lookup_customer`. That's often what you want (the app supplies caller ID via context, as in section 3), but decide deliberately.
#
# ## Where LangChain stops
#
# - It runs the loop and gives you hooks. **Which** rules go in those hooks is product/compliance work.
# - Agent state is a working copy for this run/thread. Bookings, customers, and schedules live in systems of record.
# - It isn't a real-time audio framework. Put it behind the talker: as a tool, a background planner, or post-call work.
#
# ## Exercises
#
# 1. With a live model, time 5 full bookings and count model round-trips per booking. What's the p50 wall-clock? Would you put this between a caller and the next word?
# 2. Move the `slot not offered` check from `booking_guard` into the `create_job` tool itself. Which location is better, and why might you keep both?
# 3. Add a `SummarizationMiddleware` and simulate a 40-turn call. What facts must survive summarization (hint: they should be in *state*, not only in messages)?

# %% [markdown]
# ## Check your understanding
#
# 1. What belongs in runtime context versus agent state?
# 2. Why can middleware be useful but still not define product policy by itself?
# 3. Why is a multi-round agent loop usually a poor direct audio hot path?
#
# **Graded exercise:** add a middleware assertion that blocks `create_job` when the slot
# was not offered, then show the invariant survives a reckless model call. See
# [`solutions/05_langchain_create_agent.md`](../solutions/05_langchain_create_agent.md).
