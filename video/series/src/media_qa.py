"""Offline QA report for the rendered explainer media."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RENDERED = ROOT / "video/series/rendered"
CAPTIONS = ROOT / "video/series/captions"
EPISODES = ["voice-agents-01-anatomy", "voice-agents-02-turn-taking", "voice-agents-03-architecture", "voice-agents-04-control-plane"]


def probe(path: Path, entries: str) -> dict:
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", str(path)], text=True)
    return json.loads(raw)


def main() -> int:
    report = []
    for base in EPISODES:
        mp4 = RENDERED / f"{base}-1080p.mp4"
        mp3 = RENDERED / f"{base}.mp3"
        video = probe(mp4, "stream=width,height,r_frame_rate,codec_name:format=duration")
        audio = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp3), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary", "-f", "null", "-"], text=True, capture_output=True, check=False)
        loudness = re.search(r"Input Integrated:\s+([\-\d.]+) LUFS", audio.stderr)
        true_peak = re.search(r"Input True Peak:\s+([\-\d.]+) dBTP", audio.stderr)
        vtt = (CAPTIONS / f"{base}.vtt").read_text()
        stamps = re.findall(r"(\d\d):(\d\d):(\d\d\.\d{3}) --> (\d\d):(\d\d):(\d\d\.\d{3})", vtt)
        end = stamps[-1][3:6] if stamps else None
        caption_end = (int(end[0]) * 3600 + int(end[1]) * 60 + float(end[2])) if end else None
        duration = float(video["format"]["duration"])
        report.append({"episode": base, "video": video, "integrated_lufs": float(loudness.group(1)) if loudness else None, "true_peak_db": float(true_peak.group(1)) if true_peak else None, "caption_cues": len(stamps), "caption_end": caption_end, "caption_drift_seconds": round(caption_end - duration, 3) if caption_end is not None else None})
    out = ROOT / "video/series/media-qa.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
