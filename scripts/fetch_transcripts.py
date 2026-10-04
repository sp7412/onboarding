"""Download YouTube transcripts for every video linked in the onboarding guide.

Reads docs/reading-guide.md and docs/podcast-prompts.md, finds every YouTube video ID
(playlists are skipped; their videos are listed individually in the podcast prompts), and
saves one plain-text transcript per video to build/transcripts/ (gitignored).

    pip install youtube-transcript-api
    python scripts/fetch_transcripts.py            # fetch everything not yet saved
    python scripts/fetch_transcripts.py --force    # re-download all
    python scripts/fetch_transcripts.py --json-only  # refresh timestamped caption JSON

Run this on a home internet connection. YouTube often blocks cloud servers and some
corporate networks. Transcripts are for personal study: don't commit them to the public repo.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [ROOT / "docs" / "reading-guide.md", ROOT / "docs" / "podcast-prompts.md"]
OUT = ROOT / "build" / "transcripts"
VIDEO = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})")


def video_ids() -> list[str]:
    seen: dict[str, None] = {}
    for path in SOURCES:
        for vid in VIDEO.findall(path.read_text()):
            seen.setdefault(vid, None)
    return list(seen)


def title_for(vid: str) -> str | None:
    request = Request(
        f"https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D{quote(vid)}&format=json",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        with urlopen(request, timeout=15) as response:  # noqa: S310 - fixed public endpoint
            return json.load(response).get("title")
    except Exception:  # noqa: BLE001 - optional metadata
        return None


def save_json(vid: str, fetched: object) -> None:
    payload = {
        "video_id": vid,
        "url": f"https://www.youtube.com/watch?v={vid}",
        "title": title_for(vid),
        "segments": [
            {"start": float(segment.start), "duration": float(segment.duration), "text": segment.text}
            for segment in fetched
        ],
    }
    (OUT / f"{vid}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Download transcripts for the guide's YouTube videos.")
    ap.add_argument("--force", action="store_true", help="re-download transcripts that already exist")
    ap.add_argument("--json-only", action="store_true", help="refresh timestamped JSON without replacing TXT files")
    ap.add_argument("--delay", type=float, default=2.0, help="seconds between requests (default 2)")
    args = ap.parse_args(argv)
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("Install it first: pip install youtube-transcript-api")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    api = YouTubeTranscriptApi()
    ids = video_ids()
    ok, failed = 0, []
    for i, vid in enumerate(ids, 1):
        path = OUT / f"{vid}.txt"
        json_path = OUT / f"{vid}.json"
        if path.exists() and json_path.exists() and not args.force and not args.json_only:
            print(f"[{i}/{len(ids)}] skip  {vid} (already saved)")
            ok += 1
            continue
        try:
            fetched = api.fetch(vid, languages=["en", "en-US", "en-GB"])
            save_json(vid, fetched)
            if not args.json_only:
                text = " ".join(s.text.replace("\n", " ") for s in fetched)
                path.write_text(f"https://www.youtube.com/watch?v={vid}\n\n{text}\n")
            print(f"[{i}/{len(ids)}] saved {vid} ({len(fetched)} caption segments)")
            ok += 1
        except Exception as exc:  # noqa: BLE001 - report and keep going
            reason = type(exc).__name__
            print(f"[{i}/{len(ids)}] FAIL  {vid}: {reason}")
            failed.append((vid, reason))
            if reason in ("IpBlocked", "RequestBlocked"):
                print("YouTube is blocking this network. Try a home connection, then re-run.")
                break
        time.sleep(args.delay)

    print(f"\n{ok} saved, {len(failed)} failed. Files are in {OUT.relative_to(ROOT)}/")
    for vid, reason in failed:
        print(f"  {vid}: {reason} (some videos have no transcript or have captions turned off)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
