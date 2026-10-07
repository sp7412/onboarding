"""Sentence-timed local production for the four approved explainer episodes."""
# ruff: noqa: E701, E702
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = Path(__file__).resolve().parents[3]
SERIES = ROOT / "video/series"
SCRIPT_DIR = SERIES / "scripts"
BUILD = SERIES / "build"
EPISODES = {
    "01": "episode-01-anatomy.md",
    "02": "episode-02-turn-taking.md",
    "03": "episode-03-architecture.md",
    "04": "episode-04-control-plane.md",
}


def sentences(path: Path) -> list[str]:
    body = re.sub(r"^#.*$|^Target length:.*$|^## .*?$", "", path.read_text(), flags=re.MULTILINE)
    body = re.sub(r"\n\*Source:.*?\*", "", body)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\n+", " ", body)) if s.strip()]


def make_vtt(cues: list[dict], path: Path) -> None:
    def stamp(value: float) -> str:
        return f"{int(value//3600):02d}:{int(value%3600//60):02d}:{value%60:06.3f}"
    lines = ["WEBVTT", ""]
    for i, cue in enumerate(cues, 1):
        lines += [str(i), f"{stamp(cue['start'])} --> {stamp(cue['end'])}", cue["text"], ""]
    path.write_text("\n".join(lines))


def main() -> int:
    pipeline = KPipeline(lang_code="a")
    for number, filename in EPISODES.items():
        base = f"voice-agents-{number}-" + {"01":"anatomy", "02":"turn-taking", "03":"architecture", "04":"control-plane"}[number]
        out = BUILD / base
        out.mkdir(parents=True, exist_ok=True)
        chunks: list[np.ndarray] = []
        cues = []
        cursor = 0.0
        for index, sentence in enumerate(sentences(SCRIPT_DIR / filename)):
            audio = np.concatenate([a for _, _, a in pipeline(sentence, voice="af_heart", speed=1.0)]).astype(np.float32)
            start = cursor; duration = len(audio) / 24000; end = start + duration
            chunks.append(audio); cues.append({"index": index, "event": f"sentence-{index:02d}", "text": sentence, "start": round(start, 3), "end": round(end, 3), "duration": round(duration, 3)})
            cursor = end
            if index < len(sentences(SCRIPT_DIR / filename)) - 1:
                chunks.append(np.zeros(round(.32 * 24000), dtype=np.float32)); cursor += .32
        sf.write(out / "narration.wav", np.concatenate(chunks), 24000)
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"aevalsrc=0.025*sin(2*PI*110*t)+0.018*sin(2*PI*165*t):s=48000:d={cursor}", "-ac", "2", str(out / "music.wav")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ffmpeg", "-y", "-i", str(out/"narration.wav"), "-i", str(out/"music.wav"), "-filter_complex", "[0:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11[n];[1:a]volume=0.08,aresample=48000[m];[n][m]amix=inputs=2:duration=first:dropout_transition=2[out]", "-map", "[out]", "-ar", "48000", "-ac", "2", str(out/"mix.wav")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (out / "timing.json").write_text(json.dumps({"voice":"af_heart", "sample_rate":24000, "duration":round(cursor,3), "sentences":cues}, indent=2)+"\n")
        make_vtt(cues, SERIES / "captions" / f"{base}.vtt")
        print(number, base, round(cursor, 2), len(cues))
    return 0


if __name__ == "__main__": raise SystemExit(main())
