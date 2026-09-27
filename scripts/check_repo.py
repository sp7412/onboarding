"""Check generated notebooks and repository hygiene without executing notebooks."""
from __future__ import annotations

import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "labs"


def check_notebook_outputs() -> list[str]:
    errors = []
    for path in sorted(LABS.glob("[0-9][0-9]_*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        for index, cell in enumerate(notebook.cells):
            if cell.cell_type == "code" and (cell.get("outputs") or cell.get("execution_count") is not None):
                errors.append(f"{path.relative_to(ROOT)} cell {index} contains execution output")
    return errors


def check_generated_notebooks() -> list[str]:
    errors = []
    source_dir = LABS / "src"
    builder = LABS / "build_nb.py"
    if not builder.is_file():
        return ["labs/build_nb.py is missing"]
    for source in sorted(source_dir.glob("*.py")):
        notebook = LABS / f"{source.stem}.ipynb"
        if not notebook.is_file():
            errors.append(f"missing generated notebook for {source.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = check_notebook_outputs() + check_generated_notebooks()
    if errors:
        print("Repository checks failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Repository checks passed: notebooks are present and output-free.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
