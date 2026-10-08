# Real-Time Voice Agent Labs (ServiceTitan onboarding)

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

Sixteen hands-on Jupyter tutorials that build a phone agent for a fictional HVAC/plumbing
contractor, one architecture layer at a time. Labs 09–12 extend it to several agents working
together (shared context, coordination, learning, agent-to-agent booking). Labs 13–14 are
capstones on a shared synthetic call dataset: extracting and committing call facts, and
deciding when an agent has earned more autonomy. Lab 15 builds and validates an LLM judge for
the same calls (live with an OpenAI key, with a scripted stand-in offline). The
[capstone rubric](../docs/capstone-rubric.md) ends with optional pass criteria for labs 09–14.

| # | Notebook | Layer | Keys needed | Time | Run |
|---|---|---|---|---|---|
| 00 | setup_and_mental_model | architecture + mock backend | none | 30–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/00_setup_and_mental_model.ipynb) |
| 01 | realtime_protocol | OpenAI Realtime events, effort vs latency, barge-in, truncation | optional OpenAI | 30–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/01_realtime_protocol.ipynb) |
| 02 | realtime_tools_and_guardrails | tool loop + control-plane boundary | optional OpenAI | 30–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/02_realtime_tools_and_guardrails.ipynb) |
| 03 | turn_taking_and_interruptions | VAD, endpointing, barge-in (simulator) | none | 30–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/03_turn_taking_and_interruptions.ipynb) |
| 04 | livekit_agents | LiveKit agents (writes runnable programs to `agents/`) | OpenAI + LiveKit to run live | 60–90 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/04_livekit_agents.ipynb) |
| 05 | langchain_create_agent | tools, state, context, middleware | optional OpenAI | 30–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/05_langchain_create_agent.ipynb) |
| 06 | langgraph_booking_workflow | durable workflow, interrupts, crash/resume | none | 30–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/06_langgraph_booking_workflow.ipynb) |
| 07 | langsmith_tracing_evals | tracing, waterfall, redaction, evaluation | optional LangSmith/OpenAI | 60–90 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/07_langsmith_tracing_evals.ipynb) |
| 08 | capstone_talker_thinker | talker + thinker + latency budget + study-question answer | optional | 60–90 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/08_capstone_talker_thinker.ipynb) |
| 09 | shared_context | context ledger: proposed vs verified facts, permissions, versions | none | 45–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/09_shared_context.ipynb) |
| 10 | coordination_and_arbitration | shared judgment, requests with consent, arbitration, hard rules | none | 45–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/10_coordination_and_arbitration.ipynb) |
| 11 | learning_loop | decision log, outcomes, recalibration, confidence calibration | none | 45–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/11_learning_loop.ipynb) |
| 12 | agent_to_agent_booking | booking API for other AI agents: auth, scopes, idempotency, injection | none | 45–60 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/12_agent_to_agent_booking.ipynb) |
| 13 | minimax_capstone | call facts → bookability → lead scoring → dispatch → commit → claim guard | none | 90–120 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/13_minimax_capstone.ipynb) |
| 14 | earning_autonomy | promotion policy, SPRT, calibration, drift/OOD, segment-specific autonomy | none | 90–120 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/14_earning_autonomy.ipynb) |
| 15 | llm_judge | LLM-as-judge: rubric, JSON contract, kappa vs. humans, rubric bugs, self-grading and position bias, calibration, abstention | OpenAI (scripted judge offline) | 60–90 minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sp7412/onboarding/blob/main/labs/15_llm_judge.ipynb) |

## Lab environments

- **Full environment:** open the repo in [Codespaces or the dev container](../docs/lab-environments.md#codespaces-and-the-dev-container).
- **Quick single-lab run:** use a lab's **Open in Colab** badge in the table above. The
  notebook's setup cell fetches the repo and that lab's packages, and reads keys from Colab
  Secrets. See [lab environments](../docs/lab-environments.md#google-colab).

## Learning Path

The final acceptance test is [`docs/capstone-rubric.md`](../docs/capstone-rubric.md). Read it
before lab 08 so the capstone evidence you collect is deliberate rather than retrospective.

For each notebook, follow this loop:

1. Read the objective and the "Where it stops" summary.
2. Run the cells offline and inspect the event/state transitions, not just the final output.
3. Answer the check-your-understanding questions from memory.
4. Attempt the graded exercise and run its self-check.
5. Compare with the matching note in [`solutions/`](solutions/) only after attempting it.

The exercises are deliberately small and deterministic. A complete lab is usually 30–60
minutes; labs 04, 07 and 08 can take 60–90 minutes if you do the optional live work, and the
capstone labs 13 and 14 take 90–120 minutes offline.

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
LangChain chat model, a turn-taking simulator, the booking graph, and eval scenarios. The
multi-agent labs add `context.py`, `coordination.py`, `learning.py` and `agent_gateway.py`
(labs 09–12), `calls.py` and `minimax.py` (lab 13), `autonomy.py` (lab 14) and `judge.py` (lab 15).
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

- Model names and SDK APIs change quickly; verified against livekit-agents 1.8.3,
  langchain 1.4, langsmith 0.14, and the GA Realtime event protocol (gpt-realtime-2).
- Use personal/free-tier accounts; never put employer or customer data in these labs.
- `src/` holds the percent-format sources; `python build_nb.py` regenerates the notebooks.
- Edit `src/*.py`, never the generated `.ipynb` files. The repository check verifies that
  generated notebooks contain no outputs.
- `solutions/` contains answer sketches, not a substitute for running the exercises.
