# LiveKit Hands-On Track: from no-code prototype to a guarded scheduling agent

This track follows the plan in [`notes/conversation-notes.md`](../notes/conversation-notes.md):
prototype in the browser, rebuild in Python with LiveKit's official starter, then add fake
ServiceTitan tools behind the same control plane the labs use. It complements
[lab 04](../labs/04_livekit_agents.ipynb), which writes agent files by hand. Here you use LiveKit's
own project template and CLI, which is closer to how a team would start a real service.

**Time:** about 4–6 hours across three sessions. **Needs:** a free LiveKit Cloud account. Phase 2
onward also needs Python 3.11+ and [`uv`](https://docs.astral.sh/uv/).

> Public-safe: every "ServiceTitan" tool here is a mock from `labs/stlab`. Don't connect anything to
> real ServiceTitan systems or data.

---

## Phase 1: Prototype in Agent Builder (no code, ~45 min)

Agent Builder lets you prototype and deploy simple voice agents in the browser; it produces Python
code using the Agents SDK, and you can convert to code at any time.
Docs: <https://docs.livekit.io/agents/start/builder/>

- [ ] In LiveKit Cloud, open your project's **Agents** dashboard and choose **Deploy new agent**.
- [ ] Name it `scheduling-assistant` and paste these instructions:
  ```text
  You are a scheduling assistant for Benbrook Comfort Services, a fictional HVAC and plumbing company.
  Help customers schedule, reschedule, or cancel service appointments.
  Be concise and conversational.
  Never claim that an appointment was changed unless the scheduling tool confirms the change.
  ```
- [ ] Pick models. Start with the default cascaded STT → LLM → TTS pipeline; note which realtime
      models the builder offers today.
- [ ] Preview in the browser and try all five:
  1. "Hi, I need someone to look at my AC."
  2. "Move my appointment to tomorrow afternoon."
  3. "Cancel my appointment." Then answer "yes".
  4. Read a phone number slowly with pauses: "eight one seven … five five five … zero one four two."
  5. Interrupt it mid-sentence.

**What to notice**
- Prompts 2–3: it has **no tools**, so it can't actually change anything. Does it honor the "never
  claim" instruction, or does it say "Done"? Either way, you've just seen why that rule has to be
  enforced in code (Phase 3 and lab 07's claim guard), not just asked for in the prompt.
- Prompt 4: did it cut you off? That's endpointing ([lab 03](../labs/03_turn_taking_and_interruptions.ipynb)).
- Prompt 5: how quickly did it stop, and did it remember what you actually heard? ([lab 01](../labs/01_realtime_protocol.ipynb) §4)

- [ ] Write 3 observations in your onboarding log.
- [ ] Optional: use **Convert to code** and compare the generated Python with Phase 2's starter.

---

## Phase 2: The official Python starter (~1.5 h)

The LiveKit CLI can clone the `agent-starter-python` template and configure your environment. The
starter README documents version **2.18.8 or later**.
Starter: <https://github.com/livekit-examples/agent-starter-python>

```bash
brew install livekit-cli        # Linux: curl -sSL https://get.livekit.io/cli | bash
lk --version                    # 2.18.8+
lk cloud auth                   # link the CLI to your LiveKit Cloud project
lk agent init servicetitan-agent --template agent-starter-python
cd servicetitan-agent
uv sync
uv run python src/agent.py download-files   # VAD + turn-detector weights, first run only
```

Three ways to run it:

| Command | What it does | Use it for |
|---|---|---|
| `lk agent console` | talk to the agent in your terminal (mic + speakers) | quick voice checks |
| `lk agent dev` | connects to LiveKit Cloud so the Agent Console, a frontend, or a phone call can reach it | realistic testing |
| `lk agent debugger start` / `say "…"` / `stop` | one **text** turn at a time; prints the reply plus the tool calls and handoffs behind it | fast, scriptable behavior checks |

- [ ] Run `lk agent console` and hold a short conversation.
- [ ] Run `lk agent dev`, open the Agent Console in the dashboard, and talk to it from the browser.
- [ ] Run the debugger:
  ```bash
  lk agent debugger start
  lk agent debugger say "Hi, what can you do?"
  lk agent debugger stop
  ```
- [ ] Read `src/agent.py`. Find the `AgentSession(...)` call (the pipeline) and the `Agent` subclass
      (instructions and tools). These are the same two objects as lab 04 §1.
- [ ] Run the included tests with `uv run pytest`.

**Swap to speech-to-speech.** The starter defaults to a cascaded pipeline. To try the OpenAI Realtime
model (needs `OPENAI_API_KEY` in `.env.local`), replace the pipeline arguments in `AgentSession(...)`:

```python
from livekit.plugins import openai
session = AgentSession(llm=openai.realtime.RealtimeModel(model="gpt-realtime-2", voice="marin"))
```

(Install the plugin with `uv add "livekit-agents[openai]"` if it isn't already there. Check which
realtime model version your team uses; `gpt-realtime-2.1` shipped in July 2026.)

- [ ] Compare cascaded vs realtime on the five Phase 1 prompts. Record end-of-speech → first-audio
      for each in the latency worksheet (`study-guide/`).

---

## Phase 3: Fake ServiceTitan tools behind a control plane (~2 h)

Now give the agent real (mock) actions: the scheduling tools from `labs/stlab`, including
**get_appointments**, **reschedule_appointment** and **cancel_appointment**. Every tool goes through
`execute_tool`, so the policy checks from [lab 02](../labs/02_realtime_tools_and_guardrails.ipynb) §6
apply: identity from state, ownership of appointments, offered slots only, grounded cancel
confirmation, same-day changes refused, idempotent writes.

**1. Copy the mock backend into the starter:**

```bash
cp -r ../onboarding/labs/stlab src/stlab      # adjust the path to your clone of this repo
```

**2. In `src/agent.py`, add tools to the `Agent` subclass.** Keep the starter's structure and add
these methods. Rename the class to match the starter's if needed.

```python
import asyncio
from livekit.agents import Agent, RunContext, function_tool
from stlab.tools import CallState, execute_tool

INSTRUCTIONS = """You are the scheduling assistant for Benbrook Comfort Services (fictional).
Look the caller up first. To book, find slots, offer at most two, record which one the caller picks (record_slot_choice),
confirm the address, then book.
To reschedule or cancel, call get_appointments first; only move to a slot you offered.
Before cancelling, get an explicit yes and call confirm_cancellation with the caller's exact words.
Never say a change is done unless the tool result confirms it. Keep replies short."""


async def run(name: str, args: dict, ctx: RunContext[CallState]) -> dict:
    return await asyncio.to_thread(execute_tool, name, args, ctx.userdata)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)

    @function_tool
    async def lookup_customer(self, context: RunContext[CallState], phone: str) -> dict:
        """Look up a customer by phone number."""
        return await run("lookup_customer", {"phone": phone}, context)

    @function_tool
    async def find_slots(self, context: RunContext[CallState], job_type: str, zip_code: str) -> dict:
        """Find open windows. job_type: ac_repair, furnace_repair, hvac_tuneup, water_heater, leak_repair."""
        return await run("find_slots", {"job_type": job_type, "zip_code": zip_code}, context)

    @function_tool
    async def get_appointments(self, context: RunContext[CallState]) -> dict:
        """List the verified caller's upcoming appointments."""
        return await run("get_appointments", {}, context)

    @function_tool
    async def reschedule_appointment(self, context: RunContext[CallState], appointment_id: str,
                                     new_slot_id: str) -> dict:
        """Move one of the caller's appointments to a slot you offered."""
        context.disallow_interruptions()   # don't let a barge-in cut a write in half
        return await run("reschedule_appointment",
                         {"appointment_id": appointment_id, "new_slot_id": new_slot_id}, context)

    @function_tool
    async def confirm_cancellation(self, context: RunContext[CallState], caller_said: str) -> dict:
        """Call when the caller explicitly confirms a cancellation. Quote their exact words."""
        return await run("confirm_cancellation", {"caller_said": caller_said}, context)

    @function_tool
    async def cancel_appointment(self, context: RunContext[CallState], appointment_id: str, reason: str) -> dict:
        """Cancel one of the caller's appointments, only after confirm_cancellation succeeded."""
        context.disallow_interruptions()
        return await run("cancel_appointment", {"appointment_id": appointment_id, "reason": reason}, context)

    @function_tool
    async def transfer_to_human(self, context: RunContext[CallState], reason: str) -> dict:
        """Transfer the caller to a human customer service rep."""
        return await run("transfer_to_human", {"reason": reason}, context)
```

(Booking tools `record_slot_choice`, `record_address_confirmation` and `create_job` follow the same
pattern, as in lab 04. `create_job` is refused until the caller's chosen window and address are both
recorded in their own words.)

**3. Give the session your per-call state, and record what the caller actually said.** In the
entrypoint, add `userdata` to the existing `AgentSession(...)` call and register two hooks:

```python
import re
from stlab import backend as be

state = CallState(call_id=ctx.room.name)
session = AgentSession[CallState](
    # ...keep the starter's existing pipeline arguments here...
    userdata=state,
)

@session.on("user_input_transcribed")
def _heard(ev):
    if ev.is_final:
        state.last_user_text = ev.transcript          # grounding for confirmations
        if be.detect_emergency(ev.transcript):
            state.emergency = True                     # execute_tool now allows only transfer_to_human

CLAIM = re.compile(r"\b(all set|taken care of|is cancelled|is moved|moved to|you're booked|is booked)\b", re.I)
changes_seen = {"n": 0}

@session.on("conversation_item_added")
def _claim_guard(ev):
    item = ev.item
    if getattr(item, "role", None) != "assistant":
        return
    text = item.text_content or ""
    if CLAIM.search(text) and len(state.changes) == changes_seen["n"]:
        print(f"CLAIM GUARD: agent claimed a change the backend never recorded: {text!r}")
    changes_seen["n"] = len(state.changes)
```

The claim guard here only logs. Lab 07 shows the stronger version: correct out loud and transfer.

**4. Exercise it with the debugger.** Callers are Marcus (`817-555-0142`, water heater appointment
on Wednesday) and Dana (`817-555-0101`, tune-up **today**):

```bash
lk agent debugger start
lk agent debugger say "Hi, this is Marcus, 817-555-0142. I need to move my water heater appointment."
lk agent debugger say "The second option works."
lk agent debugger say "Actually, cancel it instead."
lk agent debugger say "Yes, please cancel it."
lk agent debugger stop
```

- [ ] Reschedule: you should see `get_appointments` → `find_slots` → `reschedule_appointment`.
- [ ] Cancel: `confirm_cancellation` must come before `cancel_appointment`. If the model skips it,
      you should see `cancel_not_confirmed` in the tool result.
- [ ] Same-day: as Dana (`817-555-0101`), cancel today's tune-up. Expect `same_day_change`, then a
      transfer. Watch for the agent saying "all set" anyway, and for the claim-guard log line.
- [ ] Cross-customer: as Marcus, ask to cancel appointment `A-2002` (Dana's). Expect `appointment_not_owned`.
- [ ] Emergency: "there's a gas smell by the water heater". Only `transfer_to_human` should succeed.
- [ ] Repeat two of these by voice with `lk agent console`, and compare cascaded vs realtime.

**5. Lock it in with a test.** Add a pytest case using the starter's test harness (the same
`session.run(user_input=...)` and `result.expect` API as lab 04 §6) asserting that a same-day cancel
never produces `cancel_appointment` success.

---

## Phase 4: Connect it to the rest of the repo

- [ ] Trace a debugger session in LangSmith with `@traceable` around `run()` ([lab 07](../labs/07_langsmith_tracing_evals.ipynb) §1).
- [ ] Add your worst debugger transcript as a scenario in `labs/stlab/scenarios.py`, then re-run lab 07.
- [ ] Update [`notes/study-question.md`](../notes/study-question.md): what did LiveKit handle, and
      what did *you* have to build?

## How this maps to the labs

| Your notes | Here | Labs |
|---|---|---|
| Phase 1: Agent Builder | Phase 1 | lab 03 (turn-taking) |
| Phase 2: `lk` CLI starter | Phase 2 | lab 04 |
| Phase 3: fake ServiceTitan tools | Phase 3 | lab 02 §6 (reschedule/cancel), lab 00 (backend) |
| "Model proposes, harness controls" | Phase 3 steps 2–3 | lab 02 |
| "Never claim a change unless confirmed" | Phase 3 step 3 | lab 07 (`claims_grounded`, claim guard) |
| LangSmith: what the agent did and why | Phase 4 | lab 07 |
