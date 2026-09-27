"""Convert percent-format .py sources (# %% / # %% [markdown]) into .ipynb."""
import sys, re, nbformat
from pathlib import Path

def convert(src: Path, dst: Path):
    cells, kind, buf = [], None, []
    def flush():
        if kind is None: return
        text = "\n".join(buf).strip("\n")
        if kind == "md":
            text = "\n".join(l[2:] if l.startswith("# ") else ("" if l == "#" else l) for l in text.splitlines())
            cells.append(nbformat.v4.new_markdown_cell(text))
        elif text:
            cells.append(nbformat.v4.new_code_cell(text))
    for line in src.read_text().splitlines():
        if line.startswith("# %% [markdown]"):
            flush(); kind, buf = "md", []
        elif line.startswith("# %%"):
            flush(); kind, buf = "code", []
        else:
            buf.append(line)
    flush()
    nb = nbformat.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
        "language_info": {"name": "python"}})
    nbformat.write(nb, dst)

if __name__ == "__main__":
    for s in sorted(Path("src").glob("*.py")):
        convert(s, Path(s.stem + ".ipynb")); print("built", s.stem)
