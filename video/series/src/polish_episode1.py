"""Build the approved episode-1 timing, audio, and sentence-driven render."""
# ruff: noqa: E701, E702, F401
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[3]
SERIES = ROOT / "video/series"
BUILD = SERIES / "build/episode-01"
SCRIPT = SERIES / "scripts/episode-01-anatomy.md"


def sentences() -> list[str]:
    body = SCRIPT.read_text()
    body = re.sub(r"^#.*$|^Target length:.*$|^## .*?$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\n\*Source:.*?\*", "", body)
    text = re.sub(r"\n+", " ", body)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    from kokoro import KPipeline

    pipeline = KPipeline(lang_code="a")
    pieces: list[np.ndarray] = []
    timing = []
    cursor = 0.0
    breath = np.zeros(round(0.32 * 24000), dtype=np.float32)
    for index, sentence in enumerate(sentences()):
        audio_parts = [audio for _, _, audio in pipeline(sentence, voice="af_heart", speed=1.0)]
        audio = np.concatenate(audio_parts).astype(np.float32)
        start = cursor
        duration = len(audio) / 24000
        pieces.append(audio)
        cursor += duration
        timing.append({"index": index, "text": sentence, "start": round(start, 3), "duration": round(duration, 3), "event": f"sentence-{index:02d}"})
        if index != len(sentences()) - 1:
            pieces.append(breath)
            cursor += len(breath) / 24000
    narration = np.concatenate(pieces)
    sf.write(BUILD / "narration.wav", narration, 24000)
    (BUILD / "timing.json").write_text(json.dumps({"voice": "af_heart", "sample_rate": 24000, "sentences": timing, "duration": round(cursor, 3)}, indent=2) + "\n")
    # Original locally generated ambient bed: two quiet low sine oscillators, no external asset.
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"aevalsrc=0.025*sin(2*PI*110*t)+0.018*sin(2*PI*165*t):s=48000:d={cursor}", "-ac", "2", str(BUILD / "music-bed.wav")], check=True, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-i", str(BUILD / "narration.wav"), "-i", str(BUILD / "music-bed.wav"), "-filter_complex", "[0:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11[n];[1:a]volume=0.08,aresample=48000[m];[n][m]amix=inputs=2:duration=first:dropout_transition=2[out]", "-map", "[out]", "-ar", "48000", "-ac", "2", str(BUILD / "mix.wav")], check=True, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"wrote {len(timing)} sentence cues and {cursor:.2f}s audio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
