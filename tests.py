#!/usr/bin/env python3
"""Smoke tests for the kitchen-table volunteering site.

Run: python3 tests.py
Rebuilds the site from content/ and checks structure, links, worksheet
scoring, LICENSE wording, and that nothing ships tracking or secrets.
"""

import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"

ENTRIES = [
    "archive-transcription",
    "citizen-science",
    "remote-crisis-line",
    "online-tutoring",
    "accessibility-testing",
    "craft-drives",
]

REQUIRED_SECTIONS = ["Time commitment", "Age notes", "Signing-up steps"]

TRACKING_PATTERNS = [
    "google-analytics", "googletagmanager", "gtag(", "analytics.js",
    "hotjar", "matomo", "segment.io", "mixpanel", "facebook.net",
    "document.cookie", "localStorage", "sessionStorage", "fetch(", "XMLHttpRequest",
]

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

failures = []


def check(label, condition, detail=""):
    if condition:
        print("PASS %s" % label)
    else:
        failures.append(label)
        print("FAIL %s%s" % (label, (" — " + detail) if detail else ""))


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag == "script" and d.get("src"):
            self.scripts.append(d["src"])
        if tag not in ("meta", "link", "br", "hr", "img", "input"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ("meta", "link", "br", "hr", "img", "input"):
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()


def all_site_text():
    return "\n".join(
        p.read_text(encoding="utf-8") for p in sorted(SITE.rglob("*")) if p.is_file()
    )


def main():
    # 1. Rebuild from scratch.
    result = subprocess.run(
        [sys.executable, "build.py"], capture_output=True, text=True
    )
    check("build.py runs cleanly", result.returncode == 0, result.stderr)

    # 2. Expected pages exist (site starts empty to prove the build is hermetic).
    expected = ["index.html"] + [e + ".html" for e in ENTRIES] + ["worksheet.html"]
    for page in expected:
        check("site/%s exists" % page, (SITE / page).is_file())

    # 3. Assets copied.
    for asset in ("style.css", "worksheet.js"):
        check("site/assets/%s exists" % asset, (SITE / "assets" / asset).is_file())

    # 4. Each directory entry has the three required sections.
    for entry in ENTRIES:
        text = (SITE / (entry + ".html")).read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            check(
                "%s.html has '%s'" % (entry, section),
                section in text,
            )

    # 5. Internal links resolve to real files.
    parse_ok = True
    for page in expected:
        html = (SITE / page).read_text(encoding="utf-8")
        parser = LinkParser()
        parser.feed(html)
        if parser.stack:
            parse_ok = False
            print("  note: %s has unbalanced tags left: %s" % (page, parser.stack))
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target, _, _ = href.partition("#")
            check(
                "%s link %s resolves" % (page, href),
                not target or (SITE / target).is_file(),
            )
    check("all pages have balanced tags", parse_ok)

    # 6. No tracking / no network calls anywhere in the built site.
    combined = all_site_text()
    for needle in TRACKING_PATTERNS:
        check("no '%s' in built site" % needle, needle not in combined)
    # worksheet.js must not import or call any network API.
    js = (SITE / "assets" / "worksheet.js").read_text(encoding="utf-8")
    check(
        "worksheet.js has no network calls",
        not re.search(r"\b(fetch|XMLHttpRequest|navigator\.sendBeacon)\b", js),
    )
    check(
        "worksheet.js stores nothing",
        not re.search(r"\b(localStorage|sessionStorage|document\.cookie)\b", js),
    )

    # 7. Worksheet page includes the form and the button wiring.
    ws = (SITE / "worksheet.html").read_text(encoding="utf-8")
    for needle in ('id="worksheet"', 'id="ws-run"', 'id="ws-result"'):
        check("worksheet.html includes %s" % needle, needle in ws)

    # 8. No secrets in source or output.
    for path in [ROOT / f for f in ("build.py", "tests.py", "README.md")] + list(
        (ROOT / "content").glob("*.md")
    ) + list((ROOT / "assets").glob("*")) + list(SITE.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pat in SECRET_PATTERNS:
            check("no secret pattern in %s" % path.name, not pat.search(text))

    # 9. LICENSE wording.
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    check(
        "LICENSE has exact copyright line",
        "Copyright (c) 2026 Asdale Dynamics, LLC" in license_text
        and license_text.count("Copyright (c)") == 1
        and license_text.startswith("MIT License"),
    )

    # 10. README credits the LLC.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("README credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme)

    print()
    if failures:
        print("%d FAILURE(S):" % len(failures))
        for f in failures:
            print(" -", f)
        return 1
    print("All tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
