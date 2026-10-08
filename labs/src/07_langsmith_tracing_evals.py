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
# # 07 · LangSmith: tracing, debugging, and evaluation
#
# **Goal:** make the voice agent observable and measurable.
#
# 1. **Trace** a call: one tree per caller turn, with spans for the model response and each tool, tagged with call ID, versions, and latency
# 2. **Visualize** a latency waterfall from those spans
# 3. **Redact** before anything leaves your process
# 4. **Evaluate**: run a scenario dataset against two versions of the agent and compare with code evaluators (and an LLM judge, if you have a key)
# 5. Turn a production failure into a regression test
#
# **Offline:** LangSmith supports `tracing_context(enabled="local")`, which builds the exact same run trees but doesn't upload them. We capture them with an `on_end` hook and print them. `evaluate(..., upload_results=False)` runs experiments locally. **Live:** with `LANGSMITH_API_KEY`, the same code sends traces/experiments to your LangSmith project.

# %%
import asyncio, json, time, os, re, warnings, contextlib
warnings.filterwarnings("ignore", message=".*API key.*")
import stlab
from stlab import backend as be
from stlab.tools import TOOL_SCHEMAS, CallState, execute_tool
from stlab.realtime import connect

stlab.load_env()
LS_LIVE = stlab.have("langsmith")
if LS_LIVE:
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ.setdefault("LANGSMITH_PROJECT", "st-voice-labs")
print("LangSmith:", "LIVE → project " + os.environ.get("LANGSMITH_PROJECT", "") if LS_LIVE else "local (nothing uploaded)")
be.LATENCY_MS.update({"lookup_customer": 80, "find_slots": 350, "create_job": 200})

# %% [markdown]
# ## 1. Instrumenting the voice loop
#
# LangChain/LangGraph code is traced automatically. Our realtime loop is plain Python, so we instrument it by hand:
#
# - `@traceable` on functions (sync or async), with `run_type` = `chain` | `llm` | `tool` | `retriever`
# - `with trace(...) as run:` for spans that don't map to one function call (e.g. "model response", from `response.create` to `response.done`)
# - **metadata** on the root: `thread_id` groups all turns of one call into a LangSmith *Thread*; add `agent_version`, `prompt_version`, `model`, and tenant so you can slice later

# %%
from langsmith import traceable, trace, tracing_context
from langsmith.run_helpers import get_current_run_tree

INSTRUCTIONS = ("You are the phone assistant for Benbrook Comfort Services. Caller ID: {caller_id}. "
                "Look the caller up, diagnose, offer two slots, confirm the address before booking, "
                "confirm before cancelling, never say a change is done unless the tool confirms it, "
                "and transfer emergencies immediately.")

@traceable(run_type="tool", name="tool")
def traced_tool(name, args, state, enforce=True):
    rt = get_current_run_tree()
    if rt:
        rt.name = f"tool:{name}"
    return execute_tool(name, args, state, enforce=enforce)

async def model_response(conn, state, enforce):
    """One response.create → response.done, as an llm span; then run any tool calls."""
    with trace("realtime_response", run_type="llm", inputs={"n_items": "…"}) as run:
        t0, ttft, text, calls = time.perf_counter(), None, [], []
        while True:
            ev = await conn.recv(timeout=30)
            if ev["type"].endswith("text.delta") or ev["type"].endswith("transcript.delta"):
                ttft = ttft or (time.perf_counter() - t0) * 1000
                text.append(ev["delta"])
            if ev["type"] == "response.done":
                resp = ev["response"]
                calls = [o for o in resp.get("output", []) if o.get("type") == "function_call"]
                break
        run.metadata.update({"ttft_ms": round(ttft) if ttft else None, "status": resp["status"]})
        run.end(outputs={"text": "".join(text), "tool_calls": [c["name"] for c in calls]})
    for c in calls:
        result = await asyncio.to_thread(traced_tool, c["name"], c["arguments"], state, enforce)
        await conn.send({"type": "conversation.item.create", "item": {
            "type": "function_call_output", "call_id": c["call_id"], "output": json.dumps(result)}})
    return "".join(text), bool(calls)

CLAIM = re.compile(r"\b(all set|taken care of|is cancelled|is moved|moved to|you're booked|is booked)\b", re.I)

@traceable(run_type="chain", name="caller_turn")
async def caller_turn(conn, state, text, *, enforce=True, screen=True, claim_guard=False):
    state.last_user_text = text
    changes_before = len(state.changes)
    if screen and be.detect_emergency(text) and not state.emergency:
        state.emergency = True
        await conn.send({"type": "session.update", "session": {"type": "realtime",
            "tools": [t for t in TOOL_SCHEMAS if t["name"] == "transfer_to_human"]}})
    if text:
        await conn.send({"type": "conversation.item.create", "item": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}})
    await conn.send({"type": "response.create"})
    spoken = []
    for _ in range(6):                       # model → tools → model … until it just talks
        said, had_calls = await model_response(conn, state, enforce)
        spoken.append(said)
        if not had_calls:
            break
        await conn.send({"type": "response.create"})
    said_all = " ".join(s for s in spoken if s).strip()
    claimed = bool(CLAIM.search(said_all))
    changed = len(state.changes) > changes_before
    corrected = False
    if claim_guard and claimed and not changed:
        # The agent said something happened that the backend never confirmed. Audio can't be un-said,
        # so the control plane corrects out loud and hands off.
        corrected = True
        execute_tool("transfer_to_human", {"reason": "agent claimed an unconfirmed change"}, state)
        await conn.send({"type": "response.create", "response": {
            "conversation": "none", "tools": [], "output_modalities": ["text"],
            "instructions": "Say exactly: Correction, that change did not go through. "
                            "I'm connecting you with a team member who can finish it."}})
        fix, _ = await model_response(conn, state, enforce)
        said_all = f"{said_all} {fix}".strip()
    state.claim_log.append({"claimed": claimed, "changed": changed, "corrected": corrected})
    return {"agent_said": said_all, "phase": state.phase}

# %% [markdown]
# A small harness that runs a whole call. Every turn becomes its own trace, and the shared `thread_id` stitches them into one conversation.

# %%
CAPTURED = []   # local-mode run trees

async def run_call(caller_id, utterances, *, call_id, enforce=True, screen=True, claim_guard=False,
                   overclaim=False, version="v1", live_model=None):
    be.reset()
    conn = await connect(live=live_model, speed=5)
    await conn.recv(timeout=10)
    session = {"type": "realtime", "output_modalities": ["text"],
               "tools": TOOL_SCHEMAS, "instructions": INSTRUCTIONS.format(caller_id=caller_id)}
    if overclaim and not getattr(conn, "is_live", False):
        session["x_sim"] = {"overclaim": True}   # simulator-only: a model that overstates success on tool errors
    await conn.send({"type": "session.update", "session": session})
    state = CallState(call_id=call_id)
    state.claim_log = []
    meta = {"thread_id": call_id, "agent_version": version, "enforce": enforce, "screen": screen,
            "model": "gpt-realtime-2" if getattr(conn, "is_live", False) else "simulator", "tenant": "benbrook-demo"}
    transcript = []
    ctx = contextlib.nullcontext() if LS_LIVE else tracing_context(enabled="local")
    with ctx:
        for text in [""] + utterances:                 # "" = agent opens the call
            out = await caller_turn(conn, state, text, enforce=enforce, screen=screen, claim_guard=claim_guard,
                                    langsmith_extra={"metadata": meta, "on_end": CAPTURED.append,
                                                     "tags": [version]})
            transcript.append((text, out["agent_said"]))
    await conn.close()
    return state, transcript

state, transcript = await run_call("+18175550142",
    ["Hi, my furnace isn't heating", "The first one works", "Yes, that's correct"], call_id="trace-demo-1")
for caller, agent in transcript:
    if caller: print("CALLER:", caller)
    print("AGENT: ", agent)

# %% [markdown]
# ## 2. Reading the trace
#
# In the LangSmith UI you'd click into the thread. Locally, print the trees:

# %%
def show(run, depth=0, t0=None):
    t0 = t0 or run.start_time
    start = (run.start_time - t0).total_seconds() * 1000
    dur = ((run.end_time or run.start_time) - run.start_time).total_seconds() * 1000
    extra = ""
    md = (run.extra or {}).get("metadata", {})
    if md.get("ttft_ms"): extra += f" first-token={md['ttft_ms']}ms"
    if run.run_type == "tool": extra += " → " + json.dumps(run.outputs or {})[:70]
    if run.error: extra += f" ERROR {run.error}"
    print(f"{'  '*depth}{run.name:<34}{run.run_type:<6} +{start:6.0f}ms {dur:6.0f}ms{extra}")
    for c in run.child_runs:
        show(c, depth + 1, t0)

for r in CAPTURED[-4:]:
    print(f"── turn: {r.inputs.get('text')!r}")
    show(r)

# %% [markdown]
# ## 3. Latency waterfall
#
# The same spans, drawn on a timeline. This is how you find *where* dead air comes from: model time-to-first-token, tool latency, or a second model round-trip after the tool.

# %%
import matplotlib.pyplot as plt

def waterfall(root, title):
    rows = []
    def walk(r, d=0):
        rows.append((r, d))
        for c in r.child_runs: walk(c, d + 1)
    walk(root)
    t0 = root.start_time
    fig, ax = plt.subplots(figsize=(10, 0.35 * len(rows) + 1))
    colors = {"chain": "#999", "llm": "#4C72B0", "tool": "#DD8452"}
    for i, (r, d) in enumerate(rows):
        s = (r.start_time - t0).total_seconds() * 1000
        e = ((r.end_time or r.start_time) - t0).total_seconds() * 1000
        ax.barh(i, e - s, left=s, color=colors.get(r.run_type, "#55A868"))
        ttft = (r.extra or {}).get("metadata", {}).get("ttft_ms")
        if ttft: ax.plot([s + ttft], [i], "k|", ms=14)
        ax.text(e + 10, i, f"{'  '*d}{r.name}", va="center", fontsize=8)
    ax.invert_yaxis(); ax.set_yticks([]); ax.set_xlabel("ms since caller turn committed")
    ax.set_title(title + "   (| = first token)"); plt.show()

turn2 = next(r for r in CAPTURED if r.inputs.get("text") == "Hi, my furnace isn't heating")
waterfall(turn2, "Turn: 'my furnace isn't heating'")

# %% [markdown]
# Note what LangSmith **doesn't** see here: endpointing delay, network, and audio playout. Those live in the transport (LiveKit metrics). A full picture joins both on `call_id`. You can emit transport metrics as spans too (e.g. a `turn_detection` span whose duration is the EOU delay).
#
# ## 4. Redaction before upload
#
# Call audio and transcripts contain PII. The LangSmith client accepts `hide_inputs` / `hide_outputs` callables that run **before** data leaves your process.

# %%
import re
from langsmith import Client

PHONE = re.compile(r"\+?1?[\s\-.(]*\d{3}[\s\-.)]*\d{3}[\s\-.]*\d{4}")
ADDRESS = re.compile(r"\d+\s+[A-Z][a-z]+(\s[A-Z][a-z]+)*\s(Dr|St|Ct|Ave|Rd|Ln|Blvd|Pkwy|Trace)\b[^\"]*")

def redact(data: dict) -> dict:
    s = json.dumps(data)
    s = PHONE.sub("[PHONE]", s)
    s = ADDRESS.sub("[ADDRESS]", s)
    return json.loads(s)

sample = {"text": "Call me at 817-555-0142", "customer": {"address": "9 Pecan Ridge Ct, Benbrook, TX 76126"}}
print(redact(sample))
redacting_client = Client(hide_inputs=redact, hide_outputs=redact) if LS_LIVE else None
# Use it with: with tracing_context(client=redacting_client): ...

# %% [markdown]
# ## 5. Evaluation
#
# ### The dataset
# Eleven scripted callers in `stlab.scenarios` (booking, reschedule, cancel, emergencies, edge cases), each with the **reference outcome** (`booked`, `rescheduled`, `cancelled`, `transfer`, `emergency_transfer`, `no_booking`). In real life you'd build this from redacted production calls plus hand-written edge cases.

# %%
from stlab.scenarios import SCENARIOS
import pandas as pd
pd.DataFrame([{"id": s["id"], "caller": s["inputs"]["caller_id"][-4:], "turns": len(s["inputs"]["utterances"]),
               "expected": s["outputs"]["outcome"]} for s in SCENARIOS])

# %% [markdown]
# ### The target
# A function `inputs → outputs`. Here: run the scripted call through the agent with a given configuration and summarize what happened. We'll compare two versions:
#
# - **v0-trusting**: no tool-boundary enforcement, no app-side emergency screening (prompt only)
# - **v1-guarded**: the control plane from notebook 02, plus a **claim guard** that catches the agent saying a change happened when the backend didn't record one
#
# Both versions run the same simulated model, configured to overstate success when a reschedule or cancel fails.

# %%
def outcome_of(st: CallState):
    actions = [c["action"] for c in st.changes]
    if "rescheduled" in actions: return "rescheduled"
    if "cancelled" in actions: return "cancelled"
    if st.booked_job: return "booked"
    if st.transferred:
        reasons = " ".join(str(c["args"]) for c in st.tool_calls if c["name"] == "transfer_to_human")
        return "emergency_transfer" if st.emergency or re.search(r"gas|smoke|emergency", reasons) else "transfer"
    return "no_booking"

def make_target(version, enforce, screen, claim_guard):
    async def target(inputs: dict) -> dict:
        st, transcript = await run_call(inputs["caller_id"], inputs["utterances"], enforce=enforce, screen=screen,
                                        claim_guard=claim_guard, overclaim=True,
                                        call_id=f"eval-{version}-{time.perf_counter_ns()}", version=version)
        return {"outcome": outcome_of(st), "job_type": (st.booked_job or {}).get("job_type"),
                "address_confirmed": st.address_confirmed,
                "tools": [c["name"] for c in st.tool_calls],
                "tool_errors": [c["result"].get("error") for c in st.tool_calls if not c["result"].get("ok", True)],
                "last_agent_line": transcript[-1][1],
                "changes": [c["action"] for c in st.changes],
                "false_claims": sum(1 for t in st.claim_log if t["claimed"] and not t["changed"] and not t["corrected"])}
    return target

# %% [markdown]
# ### Evaluators
# Evaluators are functions that receive `inputs`, `outputs`, `reference_outputs` (any subset, by parameter name) and return a bool/number or a dict with `key` and `score`. Mix:
#
# - **correctness** vs. the reference
# - **invariants** that must hold regardless of reference ("never book without a confirmed address")
# - **trajectory** checks on tool usage
# - **LLM-as-judge** for things code can't check (tone), live only

# %%
def outcome_correct(outputs, reference_outputs):
    return outputs["outcome"] == reference_outputs["outcome"]

def job_type_correct(outputs, reference_outputs):
    if reference_outputs.get("job_type") is None:
        return {"key": "job_type_correct", "score": None}   # not applicable
    return outputs["job_type"] == reference_outputs["job_type"]

def no_unsafe_booking(outputs):
    """Invariant: a booking implies a grounded address confirmation."""
    return not (outputs["outcome"] == "booked" and not outputs["address_confirmed"])

def emergency_never_booked(inputs, outputs):
    said = " ".join(inputs["utterances"]).lower()
    risky = be.detect_emergency(said)
    return not (risky and outputs["outcome"] == "booked")

def looked_up_first(outputs):
    t = outputs["tools"]
    return (not t) or t[0] in ("lookup_customer", "transfer_to_human")

def claims_grounded(outputs):
    """Invariant: every "it's done" the agent says is backed by a backend change (or corrected out loud)."""
    return outputs["false_claims"] == 0

EVALUATORS = [outcome_correct, job_type_correct, no_unsafe_booking, emergency_never_booked, looked_up_first,
              claims_grounded]

if stlab.have("openai"):
    from langchain.chat_models import init_chat_model
    judge_llm = init_chat_model("openai:gpt-5.4-mini")
    def tone_ok(outputs):
        v = judge_llm.invoke("Answer only yes or no. Is this phone-agent line brief, polite, and clear? "
                             f"LINE: {outputs['last_agent_line']!r}").content.strip().lower()
        return v.startswith("y")
    EVALUATORS.append(tone_ok)

# %% [markdown]
# ### Run the experiments
#
# Offline, we pass examples directly and don't upload. Live, we create (or reuse) a LangSmith dataset and results appear as comparable experiments in the UI.

# %%
from langsmith import aevaluate
from langsmith.schemas import Example
import uuid, datetime

if LS_LIVE:
    client = Client()
    DS = "st-voice-booking-scenarios"
    if not client.has_dataset(dataset_name=DS):
        ds = client.create_dataset(DS, description="Scripted booking calls (ServiceTitan onboarding labs)")
        client.create_examples(dataset_id=ds.id, examples=[
            {"inputs": s["inputs"], "outputs": s["outputs"], "metadata": {"scenario": s["id"]}} for s in SCENARIOS])
    DATA, UPLOAD = DS, True
else:
    # evaluate() still tries to flush its own run trees without a key; silence those auth warnings
    import logging; logging.getLogger("langsmith").setLevel(logging.CRITICAL)
    _ds = uuid.uuid4()
    DATA = [Example(id=uuid.uuid4(), dataset_id=_ds, inputs=s["inputs"], outputs=s["outputs"],
                    metadata={"scenario": s["id"]}, created_at=datetime.datetime.now()) for s in SCENARIOS]
    UPLOAD = False

results = {}
for version, enforce, screen, guard in [("v0-trusting", False, False, False), ("v1-guarded", True, True, True)]:
    res = await aevaluate(make_target(version, enforce, screen, guard), data=DATA, evaluators=EVALUATORS,
                          experiment_prefix=version, upload_results=UPLOAD, max_concurrency=1)
    results[version] = res.to_pandas()

# %%
def summarize(df):
    cols = [c for c in df.columns if c.startswith("feedback.")]
    return df[cols].apply(lambda s: pd.to_numeric(s, errors="coerce").mean()).rename(lambda c: c.replace("feedback.", ""))

pd.DataFrame({v: summarize(df) for v, df in results.items()}).round(2)

# %% [markdown]
# And the per-scenario view: this is where you debug.

# %%
def per_scenario(df):
    out = df[["inputs.utterances", "outputs.outcome", "reference.outcome", "feedback.outcome_correct",
              "feedback.no_unsafe_booking", "feedback.claims_grounded", "outputs.tool_errors"]].copy()
    out.insert(0, "scenario", [s["id"] for s in SCENARIOS][:len(out)])
    return out.drop(columns=["inputs.utterances"])
display(per_scenario(results["v0-trusting"]))
display(per_scenario(results["v1-guarded"]))

# %% [markdown]
# Read the two tables together:
#
# - `books_before_confirm`: v0 books with no confirmed address (violates the invariant). v1's tool boundary blocks it.
# - `gas_mid_booking`: the model's own emergency handling depends on its keyword sense ("smoke"), and v0 may keep booking. v1 screens every utterance before the model responds.
# - `cancel_same_day`: both versions run the *same* simulated model, which overstates success when a
#   reschedule or cancel fails ("All set, that's taken care of"). The backend refused the same-day change,
#   so v0 leaves the caller believing it was cancelled, failing `claims_grounded` and `outcome_correct`.
#   v1's **claim guard** compares what the agent said with what the backend recorded, corrects out loud,
#   and transfers. With speech-to-speech you can't un-say audio, so detect-and-correct plus an eval is the
#   realistic defense; in a cascaded pipeline you could block the sentence before TTS.
# - Where v1 *still* fails, that's your next piece of work, and now it's measurable. (The simulator's "model" is intentionally naive; with a live model you'll see different, subtler failures.)
#
# > In `aevaluate`, the evaluated target runs inside its own trace, so each experiment row links to the full call trace in the LangSmith UI.
#
# ## 6. From production failure to regression test
#
# The loop you want in production:
#
# 1. **Online evaluators** / monitors sample live traces (e.g. `no_unsafe_booking`, transfer rate, p95 TTFT) and alert.
# 2. A bad call gets flagged (by an evaluator, a CSR, or `client.create_feedback(run_id, key="csr_flag", score=0)`).
# 3. Someone reviews it in an **annotation queue** and writes the expected outcome.
# 4. It's **added to the dataset** (redacted), and every future version is evaluated against it before shipping.

# %%
new_case = {"inputs": {"caller_id": "+18175550142",
                       "utterances": ["The AC is out", "the second one works", "yeah, that's the right address"]},
            "outputs": {"outcome": "booked", "job_type": "ac_repair"}, "metadata": {"source": "fictional-regression-001"}}
if LS_LIVE:
    Client().create_examples(dataset_name="st-voice-booking-scenarios", examples=[new_case])
    print("added to LangSmith dataset")
else:
    SCENARIOS.append({"id": "prod_regression_1", **new_case})
    print("added locally; re-run section 5 to include it")

# %% [markdown]
# ## Where LangSmith stops
#
# - It records and scores; it doesn't **enforce** anything at runtime.
# - It sees what you instrument. Audio-layer latency needs transport metrics joined on call ID.
# - Evaluators encode *your* definition of success. Writing good ones (and good datasets) for a home-services contractor's customers is the domain work, and it's where a senior engineer adds the most value.
#
# ## Exercises
#
# 1. Add a `turns_to_book` evaluator (fewer is better) and a summary evaluator that reports the booking rate across the dataset.
# 2. Add span metadata for `phase` at each turn and build a chart of where calls end (phase funnel).
# 3. With a live realtime model, run v1 three times (`num_repetitions=3`). Which scenarios are flaky? What does flakiness tell you about where to add structure (notebook 06)?

# %% [markdown]
# ## Check your understanding
#
# 1. Which latency components are invisible to a basic model/tool trace?
# 2. Which invariants should be code evaluators rather than LLM-judge criteria?
# 3. How does a reviewed production failure become a regression case?
#
# **Graded exercise:** add an evaluator for `looked_up_first` or `turns_to_book`, run it
# on the fictional scenarios, and report the denominator. See
# [`solutions/07_langsmith_tracing_evals.md`](../solutions/07_langsmith_tracing_evals.md).
