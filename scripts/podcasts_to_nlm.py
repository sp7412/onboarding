"""Create NotebookLM podcast episodes from docs/podcast-prompts.md with the unofficial `nlm` CLI.

For each episode block this creates a notebook, adds its sources, and requests an Audio
Overview with the block's format, length and customize prompt (as the focus).

    python scripts/podcasts_to_nlm.py                 # dry run: print the commands (default)
    python scripts/podcasts_to_nlm.py --episodes 1,2  # only some episodes
    python scripts/podcasts_to_nlm.py --run           # actually call nlm

Requirements for --run: `pipx install notebooklm-mcp-cli` (provides `nlm`), then `nlm login`
with a PERSONAL Google account on a PERSONAL machine. `nlm` drives NotebookLM's internal
interface, not a public API, so it can break without notice; consumer NotebookLM has no
official API. Progress is saved in .nlm-podcasts.json (gitignored) so reruns skip finished
episodes; pass --force to redo them.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "docs" / "podcast-prompts.md"
STATE = ROOT / ".nlm-podcasts.json"

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
    args = ap.parse_args(argv)

    episodes = parse_episodes(PROMPTS.read_text())
    if args.episodes:
        wanted = {int(x) for x in args.episodes.split(",") if x.strip()}
        episodes = [e for e in episodes if e.number in wanted]
    profile = ["--profile", args.profile] if args.profile else []

    if not args.run:
        for ep in episodes:
            print(f"\n# Episode {ep.number}: {ep.title}  ({ep.format}, {ep.length}, {len(ep.sources)} sources)")
            for cmd in commands_for(ep, args.nlm, profile):
                print(shlex.join(cmd))
        print("\n# Dry run only. Re-run with --run to execute (after `nlm login`).")
        return 0

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    failures = 0
    for ep in episodes:
        key = str(ep.number)
        if state.get(key, {}).get("audio_requested") and not args.force:
            print(f"SKIP episode {ep.number} (already requested; use --force to redo)")
            continue
        print(f"\n== Episode {ep.number}: {ep.title}")
        created = run(commands_for(ep, args.nlm, profile)[0])
        try:
            nb_id = json.loads(created.stdout)["notebook_id"]
        except (json.JSONDecodeError, KeyError):
            print(f"  FAIL creating notebook: {created.stderr.strip() or created.stdout.strip()}")
            failures += 1
            continue
        record = state.setdefault(key, {})
        record.update(notebook_id=nb_id, failed_sources=[])
        for url in ep.sources:
            res = run([args.nlm, "source", "add", nb_id, *source_args(url), "--wait", *profile])
            ok = res.returncode == 0
            print(f"  {'added ' if ok else 'FAILED'} {url}")
            if not ok:
                record["failed_sources"].append(url)
        audio = run([args.nlm, "audio", "create", nb_id, "--format", ep.format, "--length", ep.length,
                     "--focus", ep.prompt, "--confirm", *profile])
        record["audio_requested"] = audio.returncode == 0
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        if audio.returncode == 0:
            print("  audio overview requested (generation takes several minutes)")
        else:
            failures += 1
            print(f"  FAIL requesting audio: {audio.stderr.strip() or audio.stdout.strip()}")
        if record["failed_sources"]:
            print("  Some sources failed; save them as PDF in a browser and upload with "
                  f"`{args.nlm} source add {nb_id} --file <file.pdf> --wait`.")
    print(f"\nDone: {len(episodes) - failures} ok, {failures} failed. State saved to {STATE.name}.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
