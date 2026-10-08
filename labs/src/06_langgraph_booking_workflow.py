# %% [markdown]
# ## Running this lab in Google Colab
#
# Use the **Open in Colab** badge to run this notebook without setting up the repository locally.
# The setup cell below clones the public repo, installs the same requirements used by the
# local/Codespaces environment, and switches into `labs/`. Outside Colab it is a no-op.

# %%
import os
import subprocess
import sys

if "google.colab" in sys.modules:
    repo = "/content/onboarding"
    if not os.path.isdir(repo):
        subprocess.run(["git", "clone", "-q",
                        "https://github.com/sp7412/onboarding.git", repo],
                       check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "-r", os.path.join(repo, "requirements.txt")],
                   check=True)
    os.chdir(os.path.join(repo, "labs"))
    print("Colab environment ready:", os.getcwd())
else:
    print("Local/Codespaces environment detected; use the normal repository setup.")

# %% [markdown]
# # 06 · LangGraph: a durable, deterministic booking workflow
#
# **Goal:** encode the *business process* as an explicit graph, and let models handle only the fuzzy bits. This is the "deterministic vs. agentic" dial:
#
# - `create_agent` (notebook 05): the model decides the next step every time. Flexible, harder to guarantee.
# - `StateGraph` (this notebook): **you** decide the steps and transitions; models (or simple parsers) fill in classification and extraction.
#
# You will:
# 1. define typed state with reducers
# 2. build nodes + conditional edges for identify → triage → offer → confirm → book / escalate
# 3. use `interrupt()` to pause for the caller and `Command(resume=...)` to continue
# 4. learn the **re-execution rule** for interrupts (and where side effects belong)
# 5. survive a process crash with a checkpointer, and inspect history
# 6. wrap the whole graph as **one tool** a realtime talker can call
#
# Runs fully offline.

# %%
import operator, re, json
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
import stlab
from stlab import backend as be

be.reset(); be.LATENCY_MS.update({k: 0 for k in be.LATENCY_MS})

# %% [markdown]
# ## 1. State
#
# `Annotated[list, operator.add]` is a **reducer**: node updates to that key are appended instead of overwriting. Everything else is last-write-wins.

# %%
class CallGraphState(TypedDict, total=False):
    caller_phone: str
    heard: Annotated[list[str], operator.add]   # caller utterances
    said: Annotated[list[str], operator.add]    # agent prompts
    customer: dict | None
    job_type: str | None
    triage_attempts: int
    emergency: bool
    slots: list[dict]
    chosen_slot: dict | None
    address_confirmed: bool
    job: dict | None
    outcome: str | None

# %% [markdown]
# ## 2. The "fuzzy" functions
#
# These are keyword parsers so the notebook runs offline. In production each could be a small, fast model call with structured output. Crucially, they only **classify**; they don't decide what happens next.

# %%
JOB_WORDS = [("water heater", "water_heater"), ("hot water", "water_heater"), ("leak", "leak_repair"),
             ("tune", "hvac_tuneup"), ("furnace", "furnace_repair"), ("heat", "furnace_repair"),
             ("ac", "ac_repair"), ("air", "ac_repair"), ("cool", "ac_repair")]

def classify_problem(text):
    t = text.lower()
    return next((j for w, j in JOB_WORDS if re.search(rf"\b{re.escape(w)}", t)), None)

def parse_yes_no(text):
    t = text.lower()
    if re.search(r"\b(no|nope|wrong|not)\b", t): return False
    if re.search(r"\b(yes|yeah|yep|correct|right|sure)\b", t): return True
    return None

def parse_choice(text, n):
    t = text.lower()
    for i, w in enumerate(["first", "second", "third"][:n]):
        if w in t: return i
    return 0 if parse_yes_no(t) else None

# Optional: swap in an LLM classifier when a key is present
stlab.load_env()
if stlab.have("openai"):
    from langchain.chat_models import init_chat_model
    from pydantic import BaseModel
    class Problem(BaseModel):
        job_type: str | None  # one of the JOB_TYPES or None
    _clf = init_chat_model("openai:gpt-5.4-mini").with_structured_output(Problem)
    def classify_problem(text):
        return _clf.invoke(f"Classify into one of {list(be.JOB_TYPES)} or null: {text!r}").job_type
print(classify_problem("the furnace is making a banging noise"))

# %% [markdown]
# ## 3. Nodes and edges
#
# `ask()` wraps `interrupt()`. When a node calls `interrupt(value)`, the graph **pauses**, saves a checkpoint, and returns `value` to the caller under `__interrupt__`. Later, `graph.invoke(Command(resume=answer))` continues, and `interrupt()` returns `answer`.

# %%
def ask(prompt):
    return interrupt({"say": prompt})

def identify(state):
    cust = be.lookup_customer(state["caller_phone"])
    if cust:
        return {"customer": cust}
    heard = ask("I couldn't find your account from this number. What's the phone number on the account?")
    return {"heard": [heard], "customer": be.lookup_customer(heard)}

def triage(state):
    name = state["customer"]["name"].split()[0] if state.get("customer") else "there"
    prompt = (f"Thanks, {name}. What's going on with your system?" if not state.get("triage_attempts")
              else "Sorry, is this about heating, cooling, a water heater, or a leak?")
    heard = ask(prompt)
    return {"heard": [heard], "said": [prompt], "job_type": classify_problem(heard),
            "emergency": be.detect_emergency(heard), "triage_attempts": state.get("triage_attempts", 0) + 1}

def route_after_triage(state):
    if state.get("emergency") or not state.get("customer"):
        return "escalate"
    if state.get("job_type"):
        return "find_slots"
    return "triage" if state["triage_attempts"] < 2 else "escalate"

def find_slots(state):
    try:
        return {"slots": be.find_slots(state["job_type"], state["customer"]["zip"], limit=2)}
    except be.PolicyError as e:
        return {"slots": [], "outcome": f"policy:{e.code}"}

def fmt(x):
    h = int(x["start"][:2])
    return f"{x['weekday']} at {h % 12 or 12}{'am' if h < 12 else 'pm'} with {x['tech']}"

def choose_slot(state):
    prompt = "I can do " + " or ".join(fmt(x) for x in state["slots"]) + ". Which works?"
    heard = ask(prompt)
    idx = parse_choice(heard, len(state["slots"]))
    return {"heard": [heard], "said": [prompt], "chosen_slot": state["slots"][idx] if idx is not None else None}

def confirm_address(state):
    prompt = f"Great. Just to confirm, the service address is {state['customer']['address']}?"
    heard = ask(prompt)
    return {"heard": [heard], "said": [prompt], "address_confirmed": parse_yes_no(heard) is True}

def book(state, config):
    c = state["chosen_slot"]
    key = f"{config['configurable']['thread_id']}:{c['id']}"   # idempotency key from the thread
    try:
        job = be.create_job(state["customer"]["id"], c["id"], state["job_type"], state["heard"][-3][:80], key)
    except be.PolicyError as e:
        return {"outcome": f"policy:{e.code}"}
    return {"job": job, "outcome": "booked",
            "said": [f"You're booked for {c['weekday']} {c['start']}–{c['end']} with {c['tech']}. Job {job['id']}."]}

def escalate(state):
    if state.get("emergency"):
        return {"outcome": "emergency_transfer", "said": [
            "If you smell gas, leave the home now and call 911 from outside. Connecting you to our emergency line."]}
    return {"outcome": state.get("outcome") or "transfer", "said": ["Let me connect you with a team member."]}

builder = StateGraph(CallGraphState)
for n, f in [("identify", identify), ("triage", triage), ("find_slots", find_slots), ("choose_slot", choose_slot),
             ("confirm_address", confirm_address), ("book", book), ("escalate", escalate)]:
    builder.add_node(n, f)
builder.add_edge(START, "identify")
builder.add_edge("identify", "triage")
builder.add_conditional_edges("triage", route_after_triage, ["escalate", "find_slots", "triage"])
# the third argument lists possible destinations so the graph can be drawn and validated
builder.add_conditional_edges("find_slots", lambda s: "choose_slot" if s.get("slots") else "escalate",
                              ["choose_slot", "escalate"])
builder.add_conditional_edges("choose_slot", lambda s: "confirm_address" if s.get("chosen_slot") else "escalate",
                              ["confirm_address", "escalate"])
builder.add_conditional_edges("confirm_address", lambda s: "book" if s.get("address_confirmed") else "escalate",
                              ["book", "escalate"])
builder.add_edge("book", END); builder.add_edge("escalate", END)

saver = InMemorySaver()
graph = builder.compile(checkpointer=saver)
print(graph.get_graph().draw_mermaid())

# %% [markdown]
# Paste that Mermaid text into mermaid.live (or a JupyterLab Mermaid cell) to see the diagram. Every path ends in `book` or `escalate`: there is no way to reach `book` without passing `confirm_address`. That's a structural guarantee, not a prompt.
#
# ## 4. Drive a call
#
# A tiny driver: start the thread, then feed caller answers until the graph finishes.

# %%
def run_call(graph, call_id, phone, answers, verbose=True):
    cfg = {"configurable": {"thread_id": call_id}}
    out = graph.invoke({"caller_phone": phone}, cfg)
    for a in answers:
        if "__interrupt__" not in out:
            break
        if verbose:
            print("AGENT: ", out["__interrupt__"][0].value["say"]); print("CALLER:", a)
        out = graph.invoke(Command(resume=a), cfg)
    if "__interrupt__" in out:
        print("AGENT: ", out["__interrupt__"][0].value["say"], " (waiting)")
    else:
        print("AGENT: ", out["said"][-1]); print("→ outcome:", out["outcome"])
    return out

be.reset()
out = run_call(graph, "call-A", "+18175550142",
               ["The furnace is banging and there's no heat", "The second one", "Yes, that's right"])

# %%
print("--- wrong address → human")
run_call(graph, "call-B", "+18175550101", ["AC is out", "first", "No, I moved"]);
print("\n--- two unclear answers → human")
run_call(graph, "call-C", "+18175550101", ["it's making a weird noise", "I'm not sure, just weird"]);
print("\n--- emergency")
run_call(graph, "call-D", "+18175550101", ["There's a gas smell near the furnace"]);
print("\n--- outside service area")
run_call(graph, "call-E", "+18175550199", ["my water heater is leaking"]);

# %% [markdown]
# ## 5. The re-execution rule
#
# **When a graph resumes, the interrupted node runs again from the top**; `interrupt()` then returns the resume value instead of pausing. Any side effect *before* the `interrupt()` in that node happens twice.
#
# That's why `find_slots` (backend call) is its own node, and `choose_slot` only asks. Watch what happens if you merge them:

# %%
CALLS = {"n": 0}
def offer_bad(state):
    CALLS["n"] += 1                                   # side effect before interrupt
    slots = be.find_slots("ac_repair", "76126", limit=2)
    answer = interrupt({"say": "Pick one: " + ", ".join(s["id"] for s in slots)})
    return {"chosen_slot": slots[0], "heard": [answer]}

g = StateGraph(CallGraphState); g.add_node("offer_bad", offer_bad)
g.add_edge(START, "offer_bad"); g.add_edge("offer_bad", END)
bad = g.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "x"}}
bad.invoke({"caller_phone": "x"}, cfg); bad.invoke(Command(resume="first"), cfg)
print("find_slots executed", CALLS["n"], "times for one question")

# %% [markdown]
# Rules of thumb:
# - Put side effects in nodes **without** interrupts, or make them idempotent (like `create_job` with a thread-scoped key).
# - Don't rely on non-deterministic values (timestamps, random IDs) computed before an interrupt.
#
# ## 6. Durability: surviving a crash
#
# The checkpointer saved state at every step. Simulate a worker dying mid-call: throw away the compiled graph, build a **new** one from the same checkpointer, and resume the same thread.

# %%
be.reset()
cfg = {"configurable": {"thread_id": "call-F"}}
graph.invoke({"caller_phone": "+18175550142"}, cfg)
graph.invoke(Command(resume="water heater is leaking"), cfg)
print("before crash, waiting at:", graph.get_state(cfg).next)

del graph                                             # 💥 process restarts
graph = builder.compile(checkpointer=saver)           # new process, same durable store
out = graph.invoke(Command(resume="first one"), cfg)
out = graph.invoke(Command(resume="yes"), cfg)
print("after restart →", out["outcome"], out["job"]["id"])

# %% [markdown]
# `InMemorySaver` only survives within this kernel. For real durability use `SqliteSaver` (local) or `PostgresSaver` (production), same interface:

# %%
try:
    import sqlite3
    from langgraph.checkpoint.sqlite import SqliteSaver
    conn = sqlite3.connect("booking_checkpoints.db", check_same_thread=False)
    durable = builder.compile(checkpointer=SqliteSaver(conn))
    cfg = {"configurable": {"thread_id": "call-G"}}
    durable.invoke({"caller_phone": "+18175550101"}, cfg)
    print("saved to booking_checkpoints.db; restart the kernel and resume thread 'call-G' to prove it")
except ImportError:
    print("pip install langgraph-checkpoint-sqlite to try this")

# %% [markdown]
# ### History and time travel
#
# Every step is a checkpoint you can inspect, which makes debugging a bad call much easier: see exactly what the state was when the agent said something wrong.

# %%
cfg = {"configurable": {"thread_id": "call-A"}}
for snap in list(graph.get_state_history(cfg))[::-1]:
    v = snap.values
    print(f"next={str(snap.next):<22} heard={len(v.get('heard', []))} job_type={v.get('job_type')!s:<15} "
          f"slot={(v.get('chosen_slot') or {}).get('id')!s:<16} outcome={v.get('outcome')}")

# %% [markdown]
# ## 7. The graph as a tool for a realtime talker
#
# The realtime model (notebooks 01–02) is great at conversation and bad at being a reliable state machine. The graph is the opposite. Combine them: the talker calls **one** tool, `advance_booking(caller_said)`, and speaks whatever the graph says next. The graph owns the process; the talker owns the voice.
#
# `stlab.booking_graph` contains this same graph plus an `advance()` helper; notebook 08 plugs it into the realtime loop.

# %%
from stlab import booking_graph as bg
be.reset()
wf = bg.build()
print(bg.advance(wf, "call-H", caller_phone="+18175550142"))
print(bg.advance(wf, "call-H", caller_said="AC is blowing warm"))
print(bg.advance(wf, "call-H", caller_said="the first one"))
print(bg.advance(wf, "call-H", caller_said="yep that's correct"))

ADVANCE_BOOKING_TOOL = {
    "type": "function", "name": "advance_booking",
    "description": ("Advance the booking workflow with what the caller just said. "
                    "Speak the returned `say` text naturally. If done=true, the workflow is finished."),
    "parameters": {"type": "object", "properties": {"caller_said": {"type": "string"}}, "required": ["caller_said"]},
}

# %% [markdown]
# ## Where LangGraph stops
#
# - It guarantees the **shape** of the process (you can't reach `book` without `confirm_address`). It doesn't know whether "yeah I think so?" is a real yes; that's your parser/model and your policy.
# - Checkpoints make the workflow durable, but they aren't your system of record; the job lives in the backend.
# - It's not a turn-taking or audio system. It pauses and resumes; something else (the talker) decides when the caller has finished speaking.
#
# ## Exercises
#
# 1. Add a `reschedule` path: identify → find existing job → offer new slots → confirm → move job. Which new side effects need idempotency keys?
# 2. Replace `parse_yes_no` with an LLM that returns `yes | no | unclear`, and route `unclear` back to `confirm_address` once before escalating.
# 3. Add a node-level timeout policy: if `find_slots` takes > 2 s, return a "we'll text you options" outcome. Where does that timeout belong: graph, tool, or talker?

# %% [markdown]
# ## Check your understanding
#
# 1. Why are side effects before an interrupt dangerous?
# 2. What does a checkpointer preserve, and what does it not replace?
# 3. Which graph edge guarantees that booking requires address confirmation?
#
# **Graded exercise:** add an `unclear` confirmation branch that asks once more before
# escalation, then assert that an unclear answer cannot reach `book`. See
# [`solutions/06_langgraph_booking_workflow.md`](../solutions/06_langgraph_booking_workflow.md).
