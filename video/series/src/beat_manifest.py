from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from kokoro import KPipeline
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "video/series/scripts/episode-01-anatomy.md"
OUT = ROOT / "video/series/build/episode-01"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    body = re.sub(r"^#.*$|^Target length:.*$|^## .*?$", "", SCRIPT.read_text(), flags=re.MULTILINE)
    body = re.sub(r"\n\*Source:.*?\*", "", body)
    beats = [s.strip() for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\n+", " ", body)) if s.strip()]
    pipeline = KPipeline(lang_code="a")
    cursor = 0.0; all_audio=[]; rows=[]
    breath=np.zeros(round(.32*24000),dtype=np.float32)
    for i, beat in enumerate(beats):
        audio=np.concatenate([a for _,_,a in pipeline(beat,voice="af_heart",speed=1.0)]).astype(np.float32)
        duration=len(audio)/24000; path=OUT/f"beat-{i:02d}.wav"; sf.write(path,audio,24000)
        rows.append({"index":i,"text":beat,"audio":str(path.relative_to(ROOT)),"start":round(cursor,3),"duration":round(duration,3),"end":round(cursor+duration,3),"animation_event":f"beat-{i:02d}"})
        all_audio.append(audio); cursor+=duration
        if i<len(beats)-1: all_audio.append(breath); cursor+=.32
    sf.write(OUT/"narration.wav",np.concatenate(all_audio),24000)
    (OUT/"timing.json").write_text(json.dumps({"voice":"af_heart","sample_rate":24000,"duration":round(cursor,3),"beats":rows},indent=2)+"\n")
    print(f"{len(rows)} beats, {cursor:.2f}s")


if __name__ == "__main__": main()
