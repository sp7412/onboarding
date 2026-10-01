"""Create NotebookLM podcast episodes from docs/podcast-prompts.md with the unofficial `nlm` CLI.

For each episode block this creates a notebook, adds its sources, and requests an Audio
Overview with the block's format, length and customize prompt (as the focus).

    python scripts/podcasts_to_nlm.py                 # dry run: print the commands (default)
    python scripts/podcasts_to_nlm.py --episodes 1,2  # only some episodes
    python scripts/podcasts_to_nlm.py --run           # actually call nlm (resumable)
    python scripts/podcasts_to_nlm.py --publish       # download finished audio, upload to a
                                                      # GitHub release, add Listen links to the doc

Requirements for --run: `pipx install notebooklm-mcp-cli` (provides `nlm`), then `nlm login`
with a PERSONAL Google account on a PERSONAL machine. `nlm` drives NotebookLM's internal
interface, not a public API, so it can break without notice; consumer NotebookLM has no
official API. Progress is saved in .nlm-podcasts.json (gitignored): reruns reuse each
episode's notebook, add only missing sources, and retry only the audio request. NotebookLM
limits how many Audio Overviews an account can generate per day; when that limit is hit
(RESOURCE_EXHAUSTED), the run stops requesting audio and tells you to try again later.
--publish needs the GitHub CLI (`gh auth login`) and makes the audio public as release assets.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "docs" / "podcast-prompts.md"
STATE = ROOT / ".nlm-podcasts.json"
AUDIO_DIR = ROOT / "build" / "podcasts"
RELEASE_TAG = "podcasts"
QUOTA_MARKERS = ("RESOURCE_EXHAUSTED", "rate limit", "quota")

FORMATS = {"deep dive": "deep_dive", "brief": "brief", "critique": "critique", "debate": "debate"}
LENGTHS = {"default": "default", "longer": "long", "long": "long", "shorter": "short", "short": "short"}


@dataclass
class Episode:
    number: int
    title: str
    format: str
    length: str
    sources: list[str] = field(default_factory=list)
    prompt: str = ""


def parse_episodes(text: str) -> list[Episode]:
    """Parse every ```text block that starts with 'EPISODE <n>:'. Fails loudly on malformed blocks."""
    episodes = []
    titles = {int(n): t.strip() for n, t in re.findall(r"^#{2,3} (?:Coaching )?Episode (\d+): (.+)$", text, flags=re.M)}
    for block in re.findall(r"```text\n(EPISODE .*?)\n```", text, flags=re.S):
        head = re.match(r"EPISODE (\d+): (.+)", block)
        fmt = re.search(r"^Format: (.+?) · Length: (.+)$", block, flags=re.M)
        src = re.search(r"^SOURCES[^\n]*\n(.*?)\n\s*\n", block, flags=re.S | re.M)
        prompt = re.search(r"^CUSTOMIZE PROMPT[^\n]*\n(.+)$", block, flags=re.S | re.M)
        if not (head and fmt and src and prompt):
            raise ValueError(f"Malformed episode block starting: {block[:60]!r}")
        f, ln = fmt.group(1).strip().lower(), fmt.group(2).strip().lower()
        if f not in FORMATS or ln not in LENGTHS:
            raise ValueError(f"Episode {head.group(1)}: unknown format/length {f!r}/{ln!r}")
        episodes.append(Episode(
            number=int(head.group(1)), title=titles.get(int(head.group(1)), head.group(2).strip()), format=FORMATS[f], length=LENGTHS[ln],
            sources=[s.strip() for s in src.group(1).splitlines() if s.strip().startswith("http")],
            prompt=" ".join(prompt.group(1).split()),
        ))
    if not episodes:
        raise ValueError("No episode blocks found")
    return episodes


def source_args(url: str) -> list[str]:
    return ["--youtube", url] if re.search(r"(youtube\.com|youtu\.be)/", url) else ["--url", url]


def commands_for(ep: Episode, nlm: str, profile: list[str]) -> list[list[str]]:
    title = f"Onboarding podcast {ep.number:02d}: {ep.title}"
    cmds = [[nlm, "notebook", "create", title, "--json", *profile]]
    cmds += [[nlm, "source", "add", "<NOTEBOOK_ID>", *source_args(u), "--wait", *profile] for u in ep.sources]
    cmds.append([nlm, "audio", "create", "<NOTEBOOK_ID>", "--format", ep.format, "--length", ep.length,
                 "--focus", ep.prompt, "--confirm", *profile])
    return cmds


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", action="store_true", help="actually call nlm (default is a dry run)")
    ap.add_argument("--episodes", default="", help="comma-separated episode numbers, e.g. 1,2,10")
    ap.add_argument("--nlm", default="nlm", help="path to the nlm executable")
    ap.add_argument("--profile", default="", help="nlm profile name")
    ap.add_argument("--force", action="store_true", help="redo episodes already recorded as done")
    ap.add_argument("--delay", type=int, default=30, help="seconds between audio requests (default 30)")
    ap.add_argument("--publish", action="store_true",
                    help="download finished audio, upload it to a GitHub release, and add Listen links")
    ap.add_argument("--share", action="store_true", help="with --publish: also make each notebook public "
                    "and link it")
    ap.add_argument("--repo", default="sp7412/onboarding", help="GitHub repo for the release (owner/name)")
    args = ap.parse_args(argv)

    episodes = parse_episodes(PROMPTS.read_text())
    if args.episodes:
        wanted = {int(x) for x in args.episodes.split(",") if x.strip()}
        episodes = [e for e in episodes if e.number in wanted]
    profile = ["--profile", args.profile] if args.profile else []

    if not args.run and not args.publish:
        for ep in episodes:
            print(f"\n# Episode {ep.number}: {ep.title}  ({ep.format}, {ep.length}, {len(ep.sources)} sources)")
            for cmd in commands_for(ep, args.nlm, profile):
                print(shlex.join(cmd))
        print("\n# Dry run only. Re-run with --run to execute (after `nlm login`).")
        return 0

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if args.publish:
        return publish(episodes, state, args, profile)

    failures, quota_hit = 0, False
    for i, ep in enumerate(episodes):
        key = str(ep.number)
        record = state.setdefault(key, {})
        if record.get("audio_requested") and not args.force:
            print(f"SKIP episode {ep.number} (audio already requested; use --force to redo)")
            continue
        print(f"\n== Episode {ep.number}: {ep.title}")
        nb_id = None if args.force else record.get("notebook_id")
        if not nb_id:
            created = run(commands_for(ep, args.nlm, profile)[0])
            try:
                nb_id = json.loads(created.stdout)["notebook_id"]
            except (json.JSONDecodeError, KeyError):
                print(f"  FAIL creating notebook: {created.stderr.strip() or created.stdout.strip()}")
                failures += 1
                continue
            record.clear()
            record.update(notebook_id=nb_id, added_sources=[], failed_sources=[])
        else:
            print(f"  reusing notebook {nb_id}")
            if "added_sources" not in record:  # state from an older version of this script
                failed = set(record.get("failed_sources", []))
                record["added_sources"] = [u for u in ep.sources if u not in failed]
        added = set(record.setdefault("added_sources", []))
        record["failed_sources"] = []
        for url in ep.sources:
            if url in added:
                continue
            res = run([args.nlm, "source", "add", nb_id, *source_args(url), "--wait", *profile])
            if res.returncode == 0:
                record["added_sources"].append(url)
                print(f"  added  {url}")
            else:
                record["failed_sources"].append(url)
                print(f"  FAILED {url}")
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        if quota_hit:
            print("  audio not requested (daily limit already hit this run)")
            continue
        if i and args.delay:
            time.sleep(args.delay)
        audio = run([args.nlm, "audio", "create", nb_id, "--format", ep.format, "--length", ep.length,
                     "--focus", ep.prompt, "--confirm", *profile])
        out = f"{audio.stdout}\n{audio.stderr}"
        record["audio_requested"] = audio.returncode == 0 and not any(m in out for m in QUOTA_MARKERS)
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        if record["audio_requested"]:
            print("  audio overview requested (generation takes several minutes)")
        elif any(m in out for m in QUOTA_MARKERS):
            quota_hit = True
            failures += 1
            print("  NotebookLM's Audio Overview limit was hit. Sources are saved; re-run later "
                  "(often the next day) and only the audio request will be retried.")
        else:
            failures += 1
            print(f"  FAIL requesting audio: {audio.stderr.strip() or audio.stdout.strip()}")
        if record["failed_sources"]:
            print("  Some sources failed; save them as PDF in a browser and upload with "
                  f"`{args.nlm} source add {nb_id} --file <file.pdf> --wait`.")
    print(f"\nDone: {len(episodes) - failures} ok, {failures} not finished. State saved to {STATE.name}.")
    return 1 if failures else 0


def release_url(repo: str, filename: str) -> str:
    return f"https://github.com/{repo}/releases/download/{RELEASE_TAG}/{filename}"


def update_listen_lines(text: str, links: dict[int, dict[str, str]]) -> str:
    """Insert or replace a '- **Listen:** …' line under each episode's checkbox line."""
    out, current = [], None
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^#{2,3} (?:Coaching )?Episode (\d+):", line)
        if m:
            current = int(m.group(1))
        out.append(line)
        if current in links and line.startswith("- [") and "Generated" in line and "Listened" in line:
            if i + 1 < len(lines) and lines[i + 1].startswith("- **Listen:**"):
                i += 1  # drop the old Listen line
            info = links[current]
            parts = [f"[Episode {current} audio (m4a)]({info['audio']})"]
            if info.get("notebook"):
                parts.append(f"[NotebookLM notebook]({info['notebook']})")
            out.append("- **Listen:** " + " · ".join(parts))
        i += 1
    return "\n".join(out)


def publish(episodes: list[Episode], state: dict, args, profile: list[str]) -> int:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    if run(["gh", "release", "view", RELEASE_TAG, "--repo", args.repo]).returncode != 0:
        made = run(["gh", "release", "create", RELEASE_TAG, "--repo", args.repo, "--title", "Onboarding podcasts",
                    "--notes", "AI-generated NotebookLM audio overviews of the public onboarding material."])
        if made.returncode != 0:
            print(f"FAIL creating release: {made.stderr.strip()}")
            return 1
    links: dict[int, dict[str, str]] = {}
    for ep in episodes:
        record = state.get(str(ep.number), {})
        nb_id = record.get("notebook_id")
        if not nb_id or not record.get("audio_requested"):
            print(f"SKIP episode {ep.number} (no audio requested yet)")
            continue
        name = f"episode-{ep.number:02d}.m4a"
        path = AUDIO_DIR / name
        if not path.exists() or args.force:
            dl = run([args.nlm, "download", "audio", nb_id, "--output", str(path), "--no-progress", *profile])
            if dl.returncode != 0 or not path.exists():
                print(f"WAIT episode {ep.number}: audio not ready yet ({(dl.stderr or dl.stdout).strip()[:120]})")
                continue
        up = run(["gh", "release", "upload", RELEASE_TAG, str(path), "--clobber", "--repo", args.repo])
        if up.returncode != 0:
            print(f"FAIL uploading episode {ep.number}: {up.stderr.strip()}")
            continue
        info = {"audio": release_url(args.repo, name)}
        if args.share:
            sh = run([args.nlm, "share", "public", nb_id, *profile])
            link = re.search(r"https://notebooklm\.google\.com/\S+", sh.stdout)
            if link:
                info["notebook"] = link.group(0)
        record["audio_url"] = info["audio"]
        links[ep.number] = info
        print(f"OK   episode {ep.number}: {info['audio']}")
    STATE.write_text(json.dumps(state, indent=2) + "\n")
    if links:
        PROMPTS.write_text(update_listen_lines(PROMPTS.read_text(), links))
        print(f"\nAdded Listen links for {len(links)} episode(s) to {PROMPTS.relative_to(ROOT)}. "
              "Review, commit and push to show players on the site.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
