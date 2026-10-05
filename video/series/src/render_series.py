from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SERIES = HERE.parent
SCRIPTS = SERIES / "scripts"
CAPTIONS = SERIES / "captions"
POSTERS = SERIES / "posters"
RENDERED = SERIES / "rendered"

EPISODES = {
    "01": ("Anatomy of one call", "episode-01-anatomy.md", "Episode01", "voice-agents-01-anatomy"),
    "02": ("Turn-taking", "episode-02-turn-taking.md", "Episode02", "voice-agents-02-turn-taking"),
    "03": ("Choosing an architecture", "episode-03-architecture.md", "Episode03", "voice-agents-03-architecture"),
    "04": ("The control plane", "episode-04-control-plane.md", "Episode04", "voice-agents-04-control-plane"),
}


def narration(markdown: str) -> str:
    body = re.sub(r"^#.*$", "", markdown, flags=re.MULTILINE)
    body = re.sub(r"^Target length:.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^## .*?$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\n\*Source:.*?\*", "", body)
    body = re.sub(r"\n\n+", "\n\n", body)
    return body.strip()


def make_audio(ep: str, script: Path) -> Path:
    out = RENDERED / f"{EPISODES[ep][3]}.wav"
    code = f'''
from pathlib import Path
from kokoro import KPipeline
import soundfile as sf
text = Path(r"{script}").read_text()
import re
text = re.sub(r"^#.*$", "", text, flags=re.MULTILINE)
text = re.sub(r"^Target length:.*$", "", text, flags=re.MULTILINE)
text = re.sub(r"^## .*?$", "", text, flags=re.MULTILINE)
text = re.sub(r"\\n\\*Source:.*?\\*", "", text)
pipeline = KPipeline(lang_code="a")
chunks = []
for _, _, audio in pipeline(text, voice="af_heart", speed=1.0):
    chunks.append(audio)
import numpy as np
sf.write(r"{out}", np.concatenate(chunks), 24000)
'''
    subprocess.run([sys.executable, "-c", code], check=True, cwd=ROOT)
    return out


def make_vtt(ep: str, script: Path, duration: float) -> Path:
    text = narration(script.read_text())
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    # Sentence-level cues are easier to read and keep caption drift bounded. The renderer
    # does not have a word-level alignment API, so distribute each paragraph's share by
    # sentence word count rather than displaying whole multi-sentence paragraphs.
    cues: list[str] = []
    for paragraph in paragraphs:
        cues.extend(s.strip() for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip())
    words = [len(p.split()) for p in cues]
    total = sum(words) or 1
    cursor = 0.0
    lines = ["WEBVTT", ""]
    for i, (cue, count) in enumerate(zip(cues, words), 1):
        end = duration if i == len(cues) else cursor + duration * count / total
        def ts(value: float) -> str:
            h = int(value // 3600); m = int(value % 3600 // 60); s = value % 60
            return f"{h:02d}:{m:02d}:{s:06.3f}"
        lines.extend([str(i), f"{ts(cursor)} --> {ts(end)}", cue, ""])
        cursor = end
    path = CAPTIONS / f"{EPISODES[ep][3]}.vtt"
    path.write_text("\n".join(lines))
    return path


def render_visual(ep: str) -> Path:
    scene = EPISODES[ep][2]
    subprocess.run([str(ROOT / ".venv/bin/manim"), "-qh", "--disable_caching", str(HERE / "series_scenes.py"), scene], check=True, cwd=ROOT)
    source = ROOT / "media" / "videos" / "series_scenes" / "1080p60" / f"{scene}.mp4"
    target = RENDERED / f"{EPISODES[ep][3]}-visual.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(source), "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(target)], check=True, cwd=ROOT)
    return target


def make_poster(ep: str, visual: Path) -> Path:
    path = POSTERS / f"{EPISODES[ep][3]}.png"
    subprocess.run(["ffmpeg", "-y", "-i", str(visual), "-frames:v", "1", "-vf", "scale=960:-1", str(path)], check=True, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return path


def mux(ep: str, visual: Path, audio: Path) -> tuple[Path, Path]:
    base = EPISODES[ep][3]
    mp4 = RENDERED / f"{base}-1080p.mp4"
    mp4_720 = RENDERED / f"{base}-720p.mp4"
    mp3 = RENDERED / f"{base}.mp3"
    normalized = RENDERED / f"{base}-normalized.wav"
    subprocess.run(["ffmpeg", "-y", "-i", str(audio), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "24000", str(normalized)], check=True, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    video_filter = "tpad=stop_mode=clone:stop_duration=300"
    subprocess.run(["ffmpeg", "-y", "-i", str(visual), "-i", str(normalized), "-map", "0:v", "-map", "1:a", "-vf", video_filter, "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-c:a", "aac", "-b:a", "128k", "-shortest", str(mp4)], check=True, cwd=ROOT)
    subprocess.run(["ffmpeg", "-y", "-i", str(mp4), "-vf", "scale=-2:720", "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "96k", str(mp4_720)], check=True, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-i", str(normalized), "-codec:a", "libmp3lame", "-q:a", "4", str(mp3)], check=True, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return mp4, mp3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", choices=EPISODES)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    RENDERED.mkdir(parents=True, exist_ok=True); CAPTIONS.mkdir(exist_ok=True); POSTERS.mkdir(exist_ok=True)
    eps = list(EPISODES) if args.all or not args.episode else [args.episode]
    for ep in eps:
        script = SCRIPTS / EPISODES[ep][1]
        audio = make_audio(ep, script)
        visual = render_visual(ep)
        mp4, mp3 = mux(ep, visual, audio)
        probe = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(mp4)], text=True)
        make_vtt(ep, script, float(probe))
        make_poster(ep, mp4)
        print(f"{ep}: {mp4} {mp3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
