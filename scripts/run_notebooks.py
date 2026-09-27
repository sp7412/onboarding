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

LABS = Path(__file__).resolve().parents[1] / "labs"
KEY_VARS = ["OPENAI_API_KEY", "LANGSMITH_API_KEY", "LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]


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
        nb = nbformat.read(nb_path, as_version=4)
        client = NotebookClient(nb, timeout=300, kernel_name="python3",
                                resources={"metadata": {"path": str(LABS)}})
        try:
            client.execute()
            print(f"PASS  {nb_path.name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {nb_path.name}\n      {str(e).strip().splitlines()[-1][:300]}")
    print(f"\n{len(nbs) - failed}/{len(nbs)} passed ({'live' if live else 'offline'})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
