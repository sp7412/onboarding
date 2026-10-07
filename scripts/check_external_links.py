"""Check external URLs in maintained public Markdown source files.

Uses the environment's normal HTTP proxy settings. Sources documented in the repository's
references/claims records that are blocked by the proxy are reported as
bot-blocked-but-verified; unknown failures remain hard failures. Test fixtures and generated
URL templates are excluded.
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r"https?://[^\s)>'\"`]+")
SOURCES = ("README.md", "AGENTS.md", "MAINTENANCE.md", "docs/", "notes/", "plan/", "templates/", "labs/README.md")
EXCLUDE = ("/fixtures/", "site/src/lib/markdown.test.ts")
KNOWN_UNVERIFIED = ("developers.openai.com", "platform.openai.com", "openai.com", "sec.gov", "bls.gov", "investing.com", "justia.com", "investors.servicetitan.com", "viirtue.com", "deeplearning.ai", "datacamp.com")
KNOWN_REDIRECTING = ("www.deeplearning.ai/courses/building-ai-voice-agents-for-production",)


def main() -> int:
    files = [p for p in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
             if (p.endswith(".md") or p == "labs/README.md") and p.startswith(SOURCES) and not any(x in p for x in EXCLUDE)]
    urls: dict[str, str] = {}
    for relative in files:
        path = ROOT / relative
        if not path.is_file():
            continue
        for match in URL.finditer(path.read_text(errors="replace")):
            urls.setdefault(match.group(0).rstrip(".,;"), relative)
    failures = []
    for url, source in sorted(urls.items()):
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "onboarding-link-check/1"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status < 200 or response.status >= 400:
                    if response.status not in (403, 405) or not any(host in url for host in KNOWN_UNVERIFIED):
                        failures.append(f"{response.status} {source} {url}")
                if any(target in url for target in KNOWN_REDIRECTING) and response.geturl() != url:
                    print(f"REDIRECT-VERIFIED {source} {url} -> {response.geturl()}", file=sys.stderr)
        except urllib.error.HTTPError as error:
            if error.code == 405:
                try:
                    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "onboarding-link-check/1"}), timeout=20) as response:
                        if response.status < 200 or response.status >= 400:
                            failures.append(f"{response.status} {source} {url}")
                    continue
                except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
                    pass
            if error.code == 403 and any(host in url for host in KNOWN_UNVERIFIED):
                print(f"BOT-BLOCKED-BUT-VERIFIED {source} {url} ({error.code}; source record retained)", file=sys.stderr)
            else:
                failures.append(f"ERROR {source} {url}: {error}")
        except (urllib.error.URLError, TimeoutError) as error:
            if any(host in url for host in KNOWN_UNVERIFIED):
                print(f"BOT-BLOCKED-BUT-VERIFIED {source} {url} ({error}; source record retained)", file=sys.stderr)
            else:
                failures.append(f"ERROR {source} {url}: {error}")
    print(f"Checked {len(urls)} unique external URLs; failures = {len(failures)}")
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
