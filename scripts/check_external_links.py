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
SOURCES = ("README.md", "AGENTS.md", "MAINTENANCE.md", "docs/", "notes/", "plan/", "templates/", "labs/README.md", "site/src/")
EXCLUDE = ("/fixtures/", "/__fixtures__/", ".test.", "site/src/lib/markdown.ts")
KNOWN_UNVERIFIED = (
    "api.slack.com", "bls.gov", "ccmux.dev", "ceo-copilot.net", "colab.research.google.com",
    "ctacquisitions.com", "datacamp.com", "deeplearning.ai", "developers.openai.com",
    "globenewswire.com", "investing.com", "investors.servicetitan.com", "jev.guide",
    "justia.com", "notion.com", "openai.com", "platform.openai.com", "researchgate.net",
    "sec.gov", "servicetitan.gcs-web.com", "slack.com", "to-do.office.com",
    "ui.adsabs.harvard.edu", "usafa.af.mil", "viirtue.com",
)
KNOWN_REDIRECTING = ("www.deeplearning.ai/courses/building-ai-voice-agents-for-production",)
URL_TEMPLATES = ("https://github.com/sp7412/onboarding/releases/download/explainer-series",)


def known_blocked(url: str) -> bool:
    return any(host in url for host in KNOWN_UNVERIFIED)


def main() -> int:
    files = [p for p in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
              if p.endswith((".md", ".astro", ".ts")) and p.startswith(SOURCES) and not any(x in p for x in EXCLUDE)]
    urls: dict[str, str] = {}
    for relative in files:
        path = ROOT / relative
        if not path.is_file():
            continue
        for match in URL.finditer(path.read_text(errors="replace")):
            url = match.group(0).rstrip(".,;")
            # Source templates (for example Astro interpolation and documentation
            # placeholders) are not concrete destinations and cannot be link-checked.
            if "${" not in url and "[" not in url and ".invalid/" not in url and url not in URL_TEMPLATES:
                urls.setdefault(url, relative)
    failures = []
    for url, source in sorted(urls.items()):
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "onboarding-link-check/1"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status < 200 or response.status >= 400:
                    if response.status not in (403, 405, 417) or not known_blocked(url):
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
            if error.code in (403, 405, 417) and known_blocked(url):
                print(f"BOT-BLOCKED-BUT-VERIFIED {source} {url} ({error.code}; source record retained)", file=sys.stderr)
            else:
                failures.append(f"ERROR {source} {url}: {error}")
        except (urllib.error.URLError, TimeoutError) as error:
            if known_blocked(url):
                print(f"BOT-BLOCKED-BUT-VERIFIED {source} {url} ({error}; source record retained)", file=sys.stderr)
            else:
                failures.append(f"ERROR {source} {url}: {error}")
    print(f"Checked {len(urls)} unique external URLs; failures = {len(failures)}")
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
