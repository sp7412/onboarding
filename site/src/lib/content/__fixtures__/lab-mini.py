# %% [markdown]
# # 03 · Turn-taking: VAD, endpointing, and barge-in
#
# **Goal:** build intuition for the knobs that decide *when the agent talks*. These
# live in the transport layer, and they are the single biggest lever on how
# "natural" a voice agent feels.
#
# Everything here runs on a toy simulator, so you can sweep parameters in seconds.

# %%
import numpy as np

# %% [markdown]
# ## 1. A caller reading a phone number
#
# The hardest moments for endpointing are pauses *inside* a thought.

# %%
call = []

# %% [markdown]
# ## 2. The endpointing trade-off
#
# Sweep the delay. Short = snappy but rude; long = polite but sluggish.

# %%
rows = []

# %% [markdown]
# ## Check your understanding
#
# 1. Why does a longer silence timer hurt every turn?
# 2. When would you turn semantic turn detection off?
#
# **Graded exercise:** sweep endpointing delays and choose the shortest setting
# with zero premature cut-offs, then record the response gap.
