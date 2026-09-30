"""Execute lab notebooks headlessly (offline by default) and report pass/fail.

    python scripts/run_notebooks.py            # all notebooks in labs/
    python scripts/run_notebooks.py 02 06      # only notebooks whose name starts with these prefixes
    python scripts/run_notebooks.py --live     # keep API keys from the environment/.env

Notebooks are executed in memory; outputs are NOT written back to the .ipynb files.
"""
import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import DeadKernelError

LABS = Path(__file__).resolve().parents[1] / "labs"
KEY_VARS = ["OPENAI_API_KEY", "LANGSMITH_API_KEY", "LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]


def _summary(exc: BaseException) -> str:
    """One readable line for any failure, including kernel deaths and empty messages."""
    lines = [ln for ln in str(exc).strip().splitlines() if ln.strip()]
    msg = lines[-1] if lines else ""
    return f"{type(exc).__name__}: {msg}"[:300] if msg else type(exc).__name__


def run_one(nb_path: Path) -> tuple[bool, str]:
    """Execute one notebook in memory. Never raises; returns (passed, detail)."""
    try:
        nb = nbformat.read(nb_path, as_version=4)
        client = NotebookClient(nb, timeout=int(os.environ.get("NB_TIMEOUT", "300")), kernel_name="python3",
                                resources={"metadata": {"path": str(LABS)}})
        client.execute()
        return True, ""
    except DeadKernelError as exc:
        return False, f"kernel died ({_summary(exc)}); check memory and installed packages"
    except Exception as exc:  # noqa: BLE001
        return False, _summary(exc)


def main(argv):
    live = "--live" in argv
    prefixes = [a for a in argv if not a.startswith("--")]
    if not live:
        for k in KEY_VARS:
            os.environ.pop(k, None)
        os.environ["STLAB_NO_DOTENV"] = "1"
    nbs = sorted(p for p in LABS.glob("[0-9][0-9]_*.ipynb")
                 if not prefixes or any(p.name.startswith(x) for x in prefixes))
    failed = 0
    for nb_path in nbs:
        ok, detail = run_one(nb_path)
        if not ok and "kernel died" in detail.lower():
            print(f"RETRY {nb_path.name} (kernel died; retrying once)")
            ok, detail = run_one(nb_path)
        if ok:
            print(f"PASS  {nb_path.name}")
        else:
            failed += 1
            print(f"FAIL  {nb_path.name}\n      {detail}")
    print(f"\n{len(nbs) - failed}/{len(nbs)} passed ({'live' if live else 'offline'})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
