"""Check the release assets referenced by the explainer manifest."""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "video/series/RELEASE.md"
URL_RE = re.compile(r"https://github\.com/sp7412/onboarding/releases/download/explainer-series/[^)]+")


def main() -> int:
    urls = sorted(set(URL_RE.findall(MANIFEST.read_text())))
    failures = []
    for target in urls:
        try:
            request = urllib.request.Request(target, method="HEAD", headers={"User-Agent": "onboarding-release-check/1"})
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status != 200:
                    failures.append(f"{response.status} {target}")
        except Exception as error:  # noqa: BLE001 - report all release failures
            failures.append(f"{target}: {error}")
    print(f"Checked {len(urls)} release assets; failures = {len(failures)}")
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
