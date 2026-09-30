"""Scan tracked files and commit metadata for locally supplied sensitive patterns."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET_PATTERNS = [
    r"\bsk-(?!placeholder)[A-Za-z0-9_-]{20,}\b",
    r"\blsv2_[A-Za-z0-9_-]{20,}\b",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    # KEY=value on one line ([ \t], not \s, so an empty value can't match the next line);
    # values of 8+ chars without "...", so placeholders like "sk-...", "lsv2_..." and "<key>" pass.
    r"\b(?:OPENAI_API_KEY|LANGSMITH_API_KEY|LIVEKIT_API_SECRET|API_SECRET)[ \t]*=[ \t]*(?!<)(?![^\s#]*\.\.\.)[^\s#]{8,}",
]
FORBIDDEN_PREFIXES = (".opencode/", ".claude/", ".cursor/")


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.STDOUT)


def configured_patterns() -> list[str]:
    values = os.environ.get("SENSITIVE_PATTERNS", "")
    pattern_file = ROOT / ".sensitive-patterns"
    if pattern_file.is_file():
        values += "\n" + pattern_file.read_text()
    return [line.strip() for line in re.split(r"[\n,]", values) if line.strip()]


def matching_patterns(text: str, patterns: list[str]) -> list[str]:
    """Return configured patterns found in text; useful for isolated tests."""
    return [pattern for pattern in patterns if re.search(pattern, text, re.IGNORECASE)]


def main() -> int:
    files = [p for p in run("git", "ls-files", "-z").split("\0") if p]
    configured = configured_patterns()
    if not configured:
        print("warning: SENSITIVE_PATTERNS and .sensitive-patterns are absent; custom scan skipped")
    errors: list[str] = []
    for path in files:
        if path.startswith(FORBIDDEN_PREFIXES):
            errors.append(f"forbidden tracked path: {path}")
        file_path = ROOT / path
        if file_path.suffix == ".ipynb":
            try:
                import nbformat
                notebook = nbformat.read(file_path, as_version=4)
                if any(cell.get("outputs") or cell.get("execution_count") is not None for cell in notebook.cells):
                    errors.append(f"notebook contains outputs: {path}")
            except ImportError:
                errors.append("nbformat is required for notebook checks")
        try:
            text = file_path.read_text(errors="replace")
        except OSError:
            continue
        for pattern in matching_patterns(text, SECRET_PATTERNS + configured):
            errors.append(f"sensitive pattern in {path}: {pattern}")
    metadata = run("git", "log", "--all", "--format=%an%n%ae%n%cn%n%ce%n%s%n%b")
    for pattern in matching_patterns(metadata, SECRET_PATTERNS + configured):
        errors.append(f"sensitive pattern in commit metadata: {pattern}")
    emails = run("git", "log", "--all", "--format=%ae%n%ce").splitlines()
    if any(email and not email.lower().endswith("@users.noreply.github.com") for email in emails):
        print("warning: historical commit metadata contains a non-GitHub-noreply email")
    if errors:
        print("sensitive-content check failed:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("sensitive-content check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
