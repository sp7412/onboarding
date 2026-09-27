# Real-Time Voice Agent Labs (ServiceTitan onboarding)

Nine hands-on Jupyter tutorials that build a phone agent for a fictional HVAC/plumbing
contractor, one architecture layer at a time:

| # | Notebook | Layer | Keys needed |
|---|---|---|---|
| 00 | setup_and_mental_model | architecture + mock backend | none |
| 01 | realtime_protocol | OpenAI Realtime events, effort vs latency, barge-in, truncation | optional OpenAI |
| 02 | realtime_tools_and_guardrails | tool loop + control-plane boundary | optional OpenAI |
| 03 | turn_taking_and_interruptions | VAD, endpointing, barge-in (simulator) | none |
| 04 | livekit_agents | LiveKit agents (writes runnable programs to `agents/`) | OpenAI + LiveKit to run live |
| 05 | langchain_create_agent | tools, state, context, middleware | optional OpenAI |
| 06 | langgraph_booking_workflow | durable workflow, interrupts, crash/resume | none |
| 07 | langsmith_tracing_evals | tracing, waterfall, redaction, evaluation | optional LangSmith/OpenAI |
| 08 | capstone_talker_thinker | talker + thinker + latency budget + study-question answer | optional |

## Learning Path

For each notebook, follow this loop:

1. Read the objective and the "Where it stops" summary.
2. Run the cells offline and inspect the event/state transitions, not just the final output.
3. Answer the check-your-understanding questions from memory.
4. Attempt the graded exercise and run its self-check.
5. Compare with the matching note in [`solutions/`](solutions/) only after attempting it.

The exercises are deliberately small and deterministic. A complete lab is usually 30–60
minutes; labs 04, 07, and 08 can take 60–90 minutes if you do the optional live work.

## Quick Start

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
cp ../.env.example .env        # optional: add keys
jupyter lab
```

Run the notebooks in order from this folder (they import the local `stlab/` package).

## Offline-first

`stlab/` contains teaching fixtures: a mock backend (`backend.py`), the guarded tool
dispatcher (`tools.py`), an offline Realtime API simulator (`fake_realtime.py`), a scripted
LangChain chat model, a turn-taking simulator, the booking graph, and eval scenarios.
The simulated "models" are rule-based scripts, not LLMs. They exist to make event flows
and control-plane behavior visible and deterministic. With keys, the same cells hit the
real services.

## Running the LiveKit agents (notebook 04)

```bash
python agents/cascaded_agent.py download-files   # once
python agents/realtime_agent.py console          # mic + speakers
python agents/realtime_agent.py dev              # connect to LiveKit Cloud
```

## Notes

- Model names and SDK APIs change quickly; verified against livekit-agents 1.8.2,
  langchain 1.4, langsmith 0.14, and the GA Realtime event protocol (gpt-realtime-2).
- Use personal/free-tier accounts; never put employer or customer data in these labs.
- `src/` holds the percent-format sources; `python build_nb.py` regenerates the notebooks.
- Edit `src/*.py`, never the generated `.ipynb` files. The repository check verifies that
  generated notebooks contain no outputs.
- `solutions/` contains answer sketches, not a substitute for running the exercises.
