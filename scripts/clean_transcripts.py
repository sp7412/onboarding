"""Create readable, local Markdown study transcripts from timestamped captions."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS = ROOT / "build" / "transcripts"
CLEAN = TRANSCRIPTS / "clean"
VIDEO_RE = re.compile(r"https://www\.youtube\.com/watch\?v=([\w-]{11})")
TERM_FIXES = {
    r"\blife\s*kit\b": "LiveKit", r"\blang\s*smith\b": "LangSmith",
    r"\blang\s*chain\b": "LangChain", r"\blang\s*graph\b": "LangGraph",
    r"\bV\s*A\s*D\b": "VAD", r"\bS\s*T\s*T\b": "STT",
    r"\bL\s*L\s*M\b": "LLM", r"\bT\s*T\s*S\b": "TTS", r"\bM\s*C\s*P\b": "MCP",
}


def reading_items() -> dict[str, tuple[str, str]]:
    text = (ROOT / "docs" / "reading-guide.md").read_text()
    current: tuple[str, str] | None = None
    found: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        heading = re.match(r"### (\d+[A-Z]?)\. (.+)$", line)
        if heading:
            current = (heading.group(1), heading.group(2))
        for vid in VIDEO_RE.findall(line):
            if current:
                found[vid] = current
    return found


def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    for pattern, replacement in TERM_FIXES.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def dedupe(segments: list[dict]) -> list[dict]:
    result: list[dict] = []
    previous = ""
    for segment in segments:
        text = clean_text(segment["text"])
        if not text or text.lower() == previous.lower():
            continue
        result.append({**segment, "text": text})
        previous = text
    return result


def paragraphs(segments: list[dict], size: int = 5) -> list[tuple[float, str]]:
    output: list[tuple[float, str]] = []
    for index in range(0, len(segments), size):
        group = segments[index : index + size]
        text = " ".join(segment["text"] for segment in group)
        text = re.sub(r"\s+([,.!?])", r"\1", text)
        text = re.sub(r"([.!?])(?=[A-Z])", r"\1 ", text)
        if text and text[-1] not in ".!?":
            text += "."
        output.append((group[0]["start"], text))
    return output


def stamp(url: str, seconds: float) -> str:
    return f"[{int(seconds // 60)}:{int(seconds % 60):02d}]({url}&t={int(seconds)}s)"


def clean_one(path: Path, items: dict[str, tuple[str, str]]) -> str:
    data = json.loads(path.read_text())
    vid = data["video_id"]
    url = data["url"]
    item_number, item_title = items.get(vid, ("unknown", "Unlisted video"))
    segments = dedupe(data["segments"])
    duration = int((segments[-1]["start"] + segments[-1].get("duration", 0)) // 60) if segments else 0
    lines = [f"# {data.get('title') or item_title}", "", f"- Video: {url}", f"- Reading-guide item: {item_number} — {item_title}", f"- Caption duration: {duration} min", ""]
    for start, text in paragraphs(segments):
        lines.extend([f"## {stamp(url, start)}", "", text, ""])
    lines.extend(["## Terms used", "", "- See the shared [glossary](../../../../notes/glossary.md) for repository terminology.", ""])
    return "\n".join(lines)


def main() -> int:
    CLEAN.mkdir(parents=True, exist_ok=True)
    items = reading_items()
    changes = ["# Local cleanup changes", "", "- Normalized technical terms, removed consecutive duplicate captions, and paragraphized every five caption segments."]
    for path in sorted(TRANSCRIPTS.glob("*.json")):
        (CLEAN / f"{path.stem}.md").write_text(clean_one(path, items))
    (CLEAN / "CHANGES.md").write_text("\n".join(changes) + "\n")
    print(f"Wrote {len(list(TRANSCRIPTS.glob('*.json')))} cleaned transcripts to {CLEAN.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
