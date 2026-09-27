"""A toy simulator for voice turn-taking: VAD, endpointing, semantic turn
detection, and interruption (barge-in) policies.

It is deliberately simple so you can *see* the trade-offs that LiveKit's
turn_handling options and the Realtime API's turn_detection options control.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

FRAME_MS = 20


@dataclass
class Seg:
    kind: str                 # "speech" or "pause"
    ms: int
    text: str = ""
    complete: bool = True     # for speech: does the utterance *end* a thought here?


def caller_timeline(segs: list[Seg], noise: float = 0.12, seed: int = 0):
    """Return (t_ms, speech_prob, truth_speaking, speech_segments_with_times)."""
    rng = np.random.default_rng(seed)
    probs, truth, spans, t = [], [], [], 0
    for s in segs:
        n = max(1, s.ms // FRAME_MS)
        if s.kind == "speech":
            base = np.clip(0.85 + rng.normal(0, noise, n), 0, 1)
            # natural dips inside speech (plosives, breaths)
            dips = rng.random(n) < 0.06
            base[dips] = rng.uniform(0.2, 0.5, dips.sum())
            spans.append({"start": t, "end": t + n * FRAME_MS, "text": s.text, "complete": s.complete})
        else:
            base = np.clip(0.08 + np.abs(rng.normal(0, noise, n)), 0, 1)
        probs.append(base)
        truth.append(np.full(n, s.kind == "speech"))
        t += n * FRAME_MS
    p = np.concatenate(probs)
    return np.arange(len(p)) * FRAME_MS, p, np.concatenate(truth), spans


def vad(prob, threshold=0.5, min_speech_ms=100, min_silence_ms=200):
    """Hysteresis VAD: needs `min_speech_ms` above threshold to start, `min_silence_ms` below to stop."""
    on, out, above, below = False, np.zeros(len(prob), bool), 0, 0
    for i, p in enumerate(prob):
        if p >= threshold:
            above, below = above + FRAME_MS, 0
        else:
            below, above = below + FRAME_MS, 0
        if not on and above >= min_speech_ms:
            on = True
        elif on and below >= min_silence_ms:
            on = False
        out[i] = on
    return out


def endpoint(vad_on, spans, min_delay_ms=500, max_delay_ms=3000, semantic=False, eou_accuracy=0.9, seed=1):
    """Decide when the user's turn is committed.

    - fixed endpointing: commit once VAD has been off for `min_delay_ms`.
    - semantic: at each VAD-off, a (simulated) end-of-utterance model looks at
      the transcript so far. If it predicts "not done yet" (e.g. mid phone
      number), we wait up to `max_delay_ms` instead.
    Returns list of commit times (ms).
    """
    rng = random.Random(seed)
    commits, i, n = [], 0, len(vad_on)
    while i < n:
        if vad_on[i] and (i + 1 < n) and not vad_on[i + 1]:
            t_off = (i + 1) * FRAME_MS
            delay = min_delay_ms
            if semantic:
                span = next((s for s in reversed(spans) if s["start"] <= t_off), None)
                truly_complete = span["complete"] if span else True
                predicted = truly_complete if rng.random() < eou_accuracy else not truly_complete
                delay = min_delay_ms if predicted else max_delay_ms
            j, resumed = i + 1, False
            while j < n and (j - i - 1) * FRAME_MS < delay:
                if vad_on[j]:
                    resumed = True
                    break
                j += 1
            if not resumed:
                commits.append(t_off + delay)
            i = j
        else:
            i += 1
    return commits


def score_turns(commits, spans):
    """Count premature commits (mid-thought) and latency after true end-of-turn."""
    ends = [s["end"] for s in spans if s["complete"]]
    premature, latencies = 0, []
    for c in commits:
        # which span's pause did this commit happen in?
        prev = [s for s in spans if s["end"] <= c]
        if prev and not prev[-1]["complete"]:
            premature += 1
        elif prev:
            latencies.append(c - prev[-1]["end"])
    missed = max(0, len(ends) - (len(commits) - premature))
    return {"commits": len(commits), "premature_cutoffs": premature, "missed_turns": missed,
            "mean_response_gap_ms": round(float(np.mean(latencies)), 0) if latencies else None}


def plot(t, prob, vad_on, spans, commits, title=""):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(t / 1000, prob, lw=0.8, label="speech probability")
    ax.fill_between(t / 1000, 0, vad_on * 1.0, alpha=0.2, step="post", label="VAD on")
    for s in spans:
        ax.text(s["start"] / 1000, 1.05, s["text"][:28], fontsize=8, color="green" if s["complete"] else "orange")
    for c in commits:
        ax.axvline(c / 1000, color="red", ls="--", lw=1)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("seconds")
    ax.set_title(title + "   (red dashed = turn committed, orange text = incomplete thought)")
    ax.legend(loc="lower right", fontsize=8)
    plt.show()


# ---------------------------------------------------------------- barge-in
@dataclass
class Sound:
    at_ms: int
    ms: int
    kind: str      # "interrupt" | "backchannel" | "cough" | "tv"
    words: int = 0


def interruptions(sounds: list[Sound], agent_speaking=(0, 8000), mode="vad", min_duration_ms=500,
                  min_words=0, adaptive_accuracy=0.95, resume_false_interruption=True, seed=3):
    """Decide, per caller sound, whether the agent yields the floor.

    mode="vad": any sound longer than min_duration_ms (and >= min_words once STT has words) interrupts.
    mode="adaptive": an acoustic classifier (accuracy `adaptive_accuracy`) separates real barge-ins
                     from backchannels/noise before yielding.
    A *false interruption* = agent stopped but no real words followed. If
    resume_false_interruption, the agent picks up where it left off.
    """
    rng = random.Random(seed)
    rows = []
    for s in sounds:
        if not (agent_speaking[0] <= s.at_ms <= agent_speaking[1]):
            rows.append({**s.__dict__, "agent_stops": False, "note": "agent not speaking"})
            continue
        real = s.kind == "interrupt"
        if mode == "vad":
            stops = s.ms >= min_duration_ms and s.words >= min_words
        else:
            guess = real if rng.random() < adaptive_accuracy else not real
            stops = guess
        if stops and real:
            note = "correct barge-in"
        elif stops and s.words == 0:
            note = "false interruption -> " + ("resumes speaking" if resume_false_interruption else "awkward silence")
        elif stops:
            note = "WRONG: yielded to a backchannel"
        elif real:
            note = "WRONG: talked over the caller"
        else:
            note = "correctly ignored"
        # rough time-to-decision: duration gate (+ waiting for STT words) vs. a fast acoustic model
        decision_ms = (min_duration_ms + (400 if min_words else 0)) if mode == "vad" else 250
        rows.append({**s.__dict__, "agent_stops": stops, "decision_ms": decision_ms if stops else None, "note": note})
    return rows
