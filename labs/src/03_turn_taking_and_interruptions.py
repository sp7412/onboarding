# %% [markdown]
# # 03 · Turn-taking: VAD, endpointing, and barge-in
#
# **Goal:** build intuition for the knobs that decide *when the agent talks*. These live in the transport layer (LiveKit `turn_handling`) or in the model's server-side VAD (Realtime `turn_detection`), and they are the single biggest lever on how "natural" a voice agent feels.
#
# Everything here runs on a toy simulator (`stlab.turn_sim`), so you can sweep parameters in seconds. The numbers are illustrative; the *trade-off shapes* are real.
#
# Three separate decisions:
#
# | Decision | Question | Typical mechanism |
# |---|---|---|
# | **VAD** | Is someone speaking *right now*? | Silero VAD, server VAD (energy/ML per 20 ms frame) |
# | **Endpointing** | Is the caller *done* with their turn? | silence timer (`min_delay`), plus a semantic end-of-turn model |
# | **Interruption** | Caller made a sound while the agent talks: should the agent stop? | VAD duration/word thresholds, or an acoustic barge-in classifier |

# %%
import numpy as np, pandas as pd
from stlab.turn_sim import Seg, Sound, caller_timeline, vad, endpoint, score_turns, plot, interruptions

# %% [markdown]
# ## 1. A caller reading a phone number
#
# The hardest moments for endpointing are pauses *inside* a thought: reading a phone number, an address, a model number off the furnace label. Orange text = a pause where the caller isn't done.

# %%
call = [
    Seg("speech", 1600, "Yeah my number is 817 555", complete=False),
    Seg("pause",   800),                                        # looking at the fridge magnet...
    Seg("speech",  900, "0142", complete=True),
    Seg("pause",  1800),
    Seg("speech", 1400, "and the unit is a Trane, model", complete=False),
    Seg("pause",   950),
    Seg("speech", 1200, "XR14 I think", complete=True),
    Seg("pause",  2000),
]
t, prob, truth, spans = caller_timeline(call, seed=0)
v = vad(prob, threshold=0.5, min_speech_ms=100, min_silence_ms=200)
commits = endpoint(v, spans, min_delay_ms=500)
plot(t, prob, v, spans, commits, "Fixed endpointing, min_delay=500 ms")
score_turns(commits, spans)

# %% [markdown]
# With a 500 ms silence timer, the agent jumps in while the caller is mid-number. The obvious fix is a longer silence timer, so let's see what that costs.
#
# ## 2. The endpointing trade-off
#
# Sweep `min_delay_ms`. Short delays = snappy but rude; long delays = polite but sluggish on *every* turn.

# %%
rows = []
for d in [200, 300, 500, 700, 900, 1200, 1500]:
    s = score_turns(endpoint(v, spans, min_delay_ms=d), spans)
    rows.append({"min_delay_ms": d, **s})
df = pd.DataFrame(rows); df

# %%
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots(figsize=(7, 3))
ax1.plot(df.min_delay_ms, df.premature_cutoffs, "o-", color="tab:red", label="premature cut-offs")
ax1.set_xlabel("min_delay_ms"); ax1.set_ylabel("cut-offs", color="tab:red")
ax2 = ax1.twinx()
ax2.plot(df.min_delay_ms, df.mean_response_gap_ms, "s--", color="tab:blue", label="response gap")
ax2.set_ylabel("gap after real end (ms)", color="tab:blue")
plt.title("Fixed endpointing: you can't win both"); plt.show()

# %% [markdown]
# ## 3. Semantic turn detection
#
# A semantic end-of-turn model looks at the *words so far* ("my number is 817 555…") and predicts whether the thought is complete. If not, the agent waits longer (`max_delay`); if yes, it can respond after a short `min_delay`. LiveKit's turn-detector plugin is a small distilled LLM that does this on CPU; the Realtime API offers `semantic_vad` with an `eagerness` setting.
#
# The simulator models this as a classifier with some accuracy. Try lowering `eou_accuracy`.

# %%
for acc in [1.0, 0.9, 0.7]:
    c = endpoint(v, spans, min_delay_ms=400, max_delay_ms=2500, semantic=True, eou_accuracy=acc)
    print(f"eou_accuracy={acc:.1f}", score_turns(c, spans))
c = endpoint(v, spans, min_delay_ms=400, max_delay_ms=2500, semantic=True, eou_accuracy=0.95)
plot(t, prob, v, spans, c, "Semantic endpointing, min 400 / max 2500 ms")

# %% [markdown]
# ## 4. VAD sensitivity and noisy lines
#
# Phone audio is noisy (road noise, TV, speakerphone). Raise the noise and watch VAD flicker. `min_silence_ms` smooths dips inside words; `threshold` trades missed speech against false triggers.

# %%
t2, prob2, _, spans2 = caller_timeline(call, noise=0.3, seed=4)
for thr, sil in [(0.5, 100), (0.5, 250), (0.65, 250)]:
    v2 = vad(prob2, threshold=thr, min_silence_ms=sil)
    flips = int(np.abs(np.diff(v2.astype(int))).sum())
    print(f"threshold={thr} min_silence_ms={sil}: VAD on/off transitions={flips}",
          score_turns(endpoint(v2, spans2, 500), spans2))

# %% [markdown]
# ## 5. Interruptions (barge-in)
#
# While the agent is speaking (0–8 s), the caller makes four sounds: an "uh-huh" backchannel, a cough, a TV in the background, and a real interruption ("wait, that's the wrong address").

# %%
sounds = [Sound(1200, 350, "backchannel", words=1),   # "uh-huh"
          Sound(2600, 180, "cough"),
          Sound(3800, 900, "tv"),
          Sound(5600, 1300, "interrupt", words=5)]

def compare(**kw):
    return pd.DataFrame(interruptions(sounds, **kw))[["at_ms", "kind", "agent_stops", "decision_ms", "note"]]

print("VAD-based, min_duration 250 ms");            display(compare(mode="vad", min_duration_ms=250))
print("VAD-based, min_duration 500 ms + 2 words");  display(compare(mode="vad", min_duration_ms=500, min_words=2))
print("Adaptive (acoustic barge-in classifier)");   display(compare(mode="adaptive", adaptive_accuracy=0.95))

# %% [markdown]
# Things to notice:
#
# - Pure duration thresholds treat a loud TV like a caller. Requiring words helps, but you only have words after STT catches up; look at `decision_ms`. Meanwhile the agent keeps talking over the caller.
# - **False interruptions**: the agent stopped but no real words followed. LiveKit can resume speaking where it left off (`resume_false_interruption`) after a `false_interruption_timeout`.
# - LiveKit's adaptive interruption handling (LiveKit Cloud) is a trained acoustic model that separates true barge-ins from backchannels *before* transcripts arrive.
#
# ## 6. When the agent must NOT be interruptible
#
# Some utterances are policy: a recording-consent notice, a payment confirmation read-back, the final "you're booked for…" summary. These are decided by the **application**, not the transport:
#
# - LiveKit: `session.say(text, allow_interruptions=False)` or `turn_handling={"interruption": {"enabled": False}}` on a specific Agent
# - Realtime API: temporarily set `interrupt_response: false`, or turn off server VAD and manage turns yourself (`create_response: false`)
#
# ## 7. Mapping the knobs to real configs
#
# **LiveKit Agents (Python, 1.x)**
# ```python
# AgentSession(
#     vad=silero.VAD.load(),
#     turn_detection=MultilingualModel(),               # semantic end-of-turn
#     turn_handling={
#         "endpointing":  {"min_delay": 0.5, "max_delay": 3.0},
#         "interruption": {"enabled": True, "mode": "adaptive",   # or "vad"
#                          "min_duration": 0.5, "min_words": 0,
#                          "resume_false_interruption": True},
#         "preemptive_generation": {"enabled": True},
#     },
#     ...)
# ```
#
# **OpenAI Realtime session**
# ```python
# {"audio": {"input": {"turn_detection": {
#     "type": "server_vad", "threshold": 0.5, "prefix_padding_ms": 300,
#     "silence_duration_ms": 500, "create_response": True, "interrupt_response": True}}}}
# # or {"type": "semantic_vad", "eagerness": "low" | "medium" | "high" | "auto"}
# ```
#
# **Important:** when LiveKit drives a realtime model that has *its own* server-side turn detection, some LiveKit interruption settings are ignored. Always know which layer is actually making the turn decision in your configuration.
#
# ## Where turn-taking stops
#
# The transport decides **when** a turn starts/ends and **whether** to yield. It does not know **what** the caller meant, whether this is a moment that must not be interrupted, or whether a pause means "I'm reading a number" vs. "I'm confused". Semantic models narrow that gap; policy closes it.
#
# ## Exercises
#
# 1. Build a caller who spells an email address letter by letter with long pauses. Find settings with zero cut-offs and a response gap < 800 ms.
# 2. Change `Sound(3800, 900, "tv")` to 2500 ms. Which modes fail? What would you log to detect this in production (notebook 07)?
# 3. Suppose the *agent* is reading a 4-item list and the caller says "the second one": is that an interruption you want to honor instantly? Sketch the policy.

# %% [markdown]
# ## Check your understanding
#
# 1. How do VAD and endpointing differ?
# 2. What is the cost of increasing a fixed silence timer?
# 3. Why can a duration-only interruption detector mistake a TV for a caller?
#
# **Graded exercise:** sweep endpointing delays and choose the shortest setting with zero
# premature cutoffs for the phone-number example. Record the tradeoff in one sentence.
# See [`solutions/03_turn_taking_and_interruptions.md`](../solutions/03_turn_taking_and_interruptions.md).
