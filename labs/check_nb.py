"""Check generated notebooks against their percent-format Python sources.

Notebook cell IDs and execution artifacts are intentionally ignored: they are
not source-controlled teaching content and may vary between nbformat versions.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import nbformat

from build_nb import convert


def comparable(notebook_path: Path) -> dict:
    notebook = nbformat.read(notebook_path, as_version=4)
    data = dict(notebook)
    data["cells"] = []

    for cell in notebook.cells:
        item = dict(cell)
        item.pop("id", None)
        item.pop("execution_count", None)
        item.pop("outputs", None)
        data["cells"].append(item)

    return data


def main() -> int:
    root = Path(__file__).resolve().parent
    source_dir = root / "src"
    failures = []

    with tempfile.TemporaryDirectory(prefix="notebook-check-") as temp_dir:
        temp_root = Path(temp_dir)

        for source in sorted(source_dir.glob("*.py")):
            generated = temp_root / f"{source.stem}.ipynb"
            committed = root / generated.name
            convert(source, generated)

            if not committed.is_file():
                failures.append(f"{committed.relative_to(root)} is missing")
                continue

            if comparable(generated) != comparable(committed):
                failures.append(
                    f"{committed.relative_to(root)} differs from {source.relative_to(root)}"
                )

    if failures:
        print("Generated notebook check failed:")
        print("\n".join(f"  - {failure}" for failure in failures))
        return 1

    print("Generated notebooks match their source files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
