# %% [markdown]
# # 00 · Setup and the mental model
#
# **Series:** ServiceTitan voice-agent onboarding labs
#
# This lab series teaches the architecture of a production real-time voice agent by building a small one: a phone agent for a fictional HVAC/plumbing contractor, *Benbrook Comfort Services*.
#
# | Notebook | Layer | Needs keys? |
# |---|---|---|
# | 00 Setup & mental model | the whole picture + the mock backend | no |
# | 01 Realtime protocol | OpenAI Realtime events, sessions, cancellation, truncation | optional (OpenAI) |
# | 02 Tools & guardrails | the control-plane boundary | optional (OpenAI) |
# | 03 Turn-taking & interruptions | VAD, endpointing, barge-in (simulator) | no |
# | 04 LiveKit Agents | real-time transport + agent sessions | yes, to run live (OpenAI + LiveKit) |
# | 05 LangChain `create_agent` | tools, state, context, middleware | optional (OpenAI) |
# | 06 LangGraph booking workflow | durable, deterministic orchestration | no |
# | 07 LangSmith tracing & evals | observability + evaluation | optional (LangSmith) |
# | 08 Capstone | talker/thinker, latency budget, full stack | optional |
#
# **Offline-first.** Every notebook runs without API keys using simulators in the `stlab/` package (a rule-based Realtime API simulator, a scripted chat model, a turn-taking simulator, and a mock backend). When a key is present, the same cells switch to the real service. The simulators are *not* smart; they exist so you can see event flows and control-plane behavior deterministically.
#
# ## The study question
#
# > **Where does each component stop, and where does the application's own control plane, business logic, guardrails, and state management begin?**
#
# Keep a running answer in the last cell of notebook 08.

# %% [markdown]
# ## 1. Install
#
# Run once (in a fresh virtualenv, Python 3.11+ recommended):
#
# ```bash
# pip install -r requirements.txt
# ```
#
# The cell below just checks what's importable.

# %%
import importlib, sys
print(sys.version.split()[0])
for mod in ["numpy", "matplotlib", "pandas", "websockets", "langchain", "langgraph", "langsmith",
            "langchain_openai", "livekit.agents"]:
    try:
        m = importlib.import_module(mod)
        print(f"  ok   {mod:<18} {getattr(m, '__version__', '')}")
    except Exception as e:
        print(f"  --   {mod:<18} missing ({type(e).__name__})")

# %% [markdown]
# ## 2. Keys (optional)
#
# Create a `.env` file next to the notebooks (a template is in `.env.example`):
#
# ```
# OPENAI_API_KEY=sk-...
# LIVEKIT_URL=wss://<your-project>.livekit.cloud
# LIVEKIT_API_KEY=...
# LIVEKIT_API_SECRET=...
# LANGSMITH_API_KEY=lsv2_...
# LANGSMITH_PROJECT=st-voice-labs
# ```
#
# Use personal/free-tier accounts for these labs, and never put employer or customer data in them.

# %%
import stlab
stlab.load_env()
stlab.status()

# %% [markdown]
# ## 3. The reference architecture
#
# ```
#  Caller (PSTN / browser)
#       │  audio (SIP / WebRTC)
#       ▼
#  ┌──────────────────────────┐   LiveKit: rooms, tracks, VAD, turn detection,
#  │  TRANSPORT (LiveKit)     │   interruptions, telephony, agent dispatch
#  └──────────┬───────────────┘
#             │ audio frames + turn events
#             ▼
#  ┌──────────────────────────┐   OpenAI Realtime: understands speech, reasons,
#  │  CONVERSATION (Realtime) │   speaks, *proposes* tool calls
#  └──────────┬───────────────┘
#             │ function_call(name, args)
#             ▼
#  ┌──────────────────────────────────────────────────────────┐
#  │  CONTROL PLANE (your application)                         │
#  │   identity · policy checks · call state · idempotency     │
#  │   phase-based tool gating · escalation · redaction        │
#  │        │                         │                        │
#  │        ▼                         ▼                        │
#  │  ORCHESTRATION (LangChain /   SYSTEMS OF RECORD           │
#  │  LangGraph): multi-step work  (customers, schedule, jobs) │
#  └──────────────────────────────────────────────────────────┘
#             ▲ spans from every layer
#  ┌──────────┴───────────────┐
#  │  OBSERVABILITY (LangSmith)│  traces, datasets, evaluators, experiments
#  └──────────────────────────┘
# ```
#
# Vendors supply **mechanism**. The application supplies **policy**.

# %% [markdown]
# ## 4. Meet the mock backend (the "system of record")
#
# `stlab.backend` fakes the systems an agent would call: customers, a technician schedule, and job booking. It has simulated latency (`LATENCY_MS`) so you can feel what slow tools do to a voice call.

# %%
from stlab import backend as be
from pprint import pprint

be.reset()
print("Service ZIPs:", sorted(be.SERVICE_ZIPS))
print("Job types:  ", list(be.JOB_TYPES))
print("Latency ms: ", be.LATENCY_MS)
pprint(be.lookup_customer("817-555-0142"))

# %%
slots = be.find_slots("furnace_repair", "76126")
for s in slots:
    print(s["id"], s["weekday"], s["date"], s["start"], "-", s["end"], s["tech"])

# %% [markdown]
# Business rules live **in the backend and control plane**, and show up as structured errors the model can talk about:

# %%
for args in [("ac_repair", "76244"),      # Keller: out of area
             ("pool_cleaning", "76109")]: # not a service we sell
    try:
        be.find_slots(*args)
    except be.PolicyError as e:
        print(e.code, "→", e.message)

# %% [markdown]
# ### Idempotency: the network *will* retry
#
# A tool call can time out after the backend already booked the job. If the agent retries, you must not double-book. The idempotency key is owned by the application (not the model).

# %%
be.reset()
key = "call-001:" + slots[0]["id"]
j1 = be.create_job("C-1002", slots[0]["id"], "furnace_repair", "No heat", idempotency_key=key)
j2 = be.create_job("C-1002", slots[0]["id"], "furnace_repair", "No heat", idempotency_key=key)  # retry
print(j1["id"], j2["id"], "replayed:", j2.get("replayed"))
print("jobs in system:", len(be.jobs()))

# %% [markdown]
# ## 5. The control-plane boundary: `CallState` + `execute_tool`
#
# `stlab.tools` holds (a) the JSON tool schemas the model sees, and (b) `execute_tool`, the guarded dispatcher. The model can only *ask*; `execute_tool` decides.
#
# `CallState` is the per-call state **the application owns**: who the caller is, what phase the call is in, what was confirmed out loud. The model's context window is not your source of truth.

# %%
from stlab.tools import TOOL_SCHEMAS, CallState, execute_tool
print([t["name"] for t in TOOL_SCHEMAS])

be.reset()
st = CallState(call_id="demo-1")
print(execute_tool("lookup_customer", {"phone": "8175550142"}, st)["customer"]["name"], "| phase:", st.phase)
res = execute_tool("find_slots", {"job_type": "furnace_repair", "zip_code": "99999"}, st)  # model guessed a ZIP
print("ZIP overridden by record ->", res["slots"][0]["id"])

# The model tries to book before confirming the address:
print(execute_tool("create_job", {"customer_id": "C-1002", "slot_id": st.offered_slot_ids[0],
                                  "job_type": "furnace_repair", "summary": "no heat"}, st))

# %% [markdown]
# Notice three different kinds of control-plane behavior in that cell:
#
# 1. **Correcting** model input with authoritative data (the ZIP comes from the customer record).
# 2. **Blocking** an action whose preconditions aren't met (`address_not_confirmed`).
# 3. **Returning a structured error** that the model can turn into a natural next question.
#
# ## Exercises
#
# 1. Add a rule to `_dispatch` in `stlab/tools.py`: members (`membership == "Comfort Club"`) get the first slot of the day; non-members can't book 8am slots. Where should this rule live, and why not in the prompt?
# 2. Change `LATENCY_MS["find_slots"]` to 2500 and re-run section 4. In notebook 02 you'll see what that does to a live conversation.
# 3. Write down your first-draft answer to the study question in one paragraph. You'll revise it in notebook 08.
