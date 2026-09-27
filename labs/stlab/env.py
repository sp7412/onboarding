"""Tiny .env loader + key checks so every notebook can run offline-first."""
import os
from pathlib import Path

KEYS = {
    "openai": ["OPENAI_API_KEY"],
    "livekit": ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"],
    "langsmith": ["LANGSMITH_API_KEY"],
}


def load_env(path: str | None = None) -> None:
    """Load KEY=VALUE lines from a .env file (searches cwd and parents)."""
    candidates = [Path(path)] if path else [p / ".env" for p in [Path.cwd(), *Path.cwd().parents]]
    for p in candidates:
        if p.is_file():
            for line in p.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


def have(service: str) -> bool:
    """True if every env var needed for `service` is set and non-empty."""
    return all(os.environ.get(k) for k in KEYS[service])


def status() -> None:
    for svc in KEYS:
        mark = "LIVE   " if have(svc) else "offline"
        print(f"  {svc:<10} {mark}  ({', '.join(KEYS[svc])})")
