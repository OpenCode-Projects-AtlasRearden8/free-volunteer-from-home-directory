#!/usr/bin/env python3
"""Build the kitchen-table volunteering site: markdown source -> static HTML.

No third-party packages, no network access. Run:

    python3 build.py

Writes the site into site/ (index.html plus one page per content/*.md file
other than index.md).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SITE = ROOT / "site"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<meta name="referrer" content="no-referrer">
<title>{title} — Kitchen-Table Volunteering</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="site">
<header class="site-header">
  <p class="site-title"><a href="index.html">Kitchen-Table Volunteering</a></p>
  <p class="site-tagline">Free volunteering you can do from a kitchen table — no accounts, no tracking.</p>
  <nav class="site-nav">
    <a href="index.html">Home</a>
    <a href="worksheet.html">Find your first project</a>
  </nav>
</header>
<main>
{content}
</main>
<footer class="site-footer">
  <p>Made by Asdale Dynamics, LLC. Free to copy and share under the MIT License — see LICENSE.</p>
  <p>This site is static text about volunteering ideas; every program's own pages have the official requirements. No accounts, no cookies, no analytics, no tracking.</p>
</footer>
</div>
<script src="assets/worksheet.js" defer></script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Minimal markdown -> HTML. Supports the subset used by content/:
# headings (#..####), paragraphs, bullet lists (-/*), ordered lists (1.),
# bold, italics, inline code, links, and --- rules. Blank lines separate
# blocks. Lists must be physically grouped (no blank lines between items).
# ---------------------------------------------------------------------------

BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITAL_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text: str) -> str:
    text = escape(text)
    text = CODE_RE.sub(r"<code>\1</code>", text)
    text = LINK_RE.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), text)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = ITAL_RE.sub(r"<em>\1</em>", text)
    return text


def strip_marker(text: str, item_re: re.Pattern) -> str:
    return item_re.sub("", text, count=1)


def collect_items(lines, i, item_re, continue_re, allow_nested=True):
    """Collect list items starting at index i.

    Returns (next_index, html_items). An item is its marker line plus any
    continuation lines, joined with spaces before inline() runs so bold and
    links may span wrapped lines. Bullets nested (indented) under an item
    become a <ul> inside that item, one level deep.
    """
    n = len(lines)
    nested_bullet = re.compile(r"^\s+[-*]\s+")
    nested_bullet_cont = re.compile(r"^(?:\s+[-*]\s+|\s)")
    html_items = []
    while i < n and item_re.match(lines[i]):
        text_parts = [strip_marker(lines[i].rstrip(), item_re)]
        html_parts = []  # nested <ul> blocks, kept raw (never escaped)
        i += 1
        while (
            i < n
            and lines[i].strip()
            and continue_re.match(lines[i])
            and not item_re.match(lines[i])
        ):
            if allow_nested and nested_bullet.match(lines[i]):
                i, sub_items = collect_items(
                    lines, i, nested_bullet, nested_bullet_cont, allow_nested=False
                )
                html_parts.append("<ul>" + "".join(sub_items) + "</ul>")
            else:
                text_parts.append(lines[i].strip())
                i += 1
        item_html = inline(" ".join(text_parts))
        for block in html_parts:
            item_html += block
        html_items.append("<li>%s</li>" % item_html)
    return i, html_items


def md_to_html(md: str) -> str:
    out = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if line.startswith("---") and line.strip("---") == "":
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level))
            i += 1
            continue

        if re.match(r"^[-*]\s+", line):
            items = collect_items(lines, i, re.compile(r"^[-*]\s+"), re.compile(r"^(?:[-*]\s+|\s)"))
            i = items[0]
            out.append("<ul>" + "".join(items[1]) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", line):
            items = collect_items(lines, i, re.compile(r"^\d+\.\s+"), re.compile(r"^(?:\d+\.\s+|\s)"))
            i = items[0]
            out.append("<ol>" + "".join(items[1]) + "</ol>")
            continue

        if line.lstrip().startswith("<"):
            # Raw HTML block: pass consecutive non-blank lines through
            # untouched (used by the worksheet form in worksheet.md).
            raw = []
            while i < len(lines) and lines[i].strip():
                raw.append(lines[i])
                i += 1
            out.append("\n".join(raw))
            continue

        # Paragraph: gather consecutive plain lines.
        para = []
        while i < len(lines) and lines[i].strip():
            stripped = lines[i].strip()
            if (
                re.match(r"^(#{1,4})\s+", stripped)
                or re.match(r"^[-*]\s+", stripped)
                or re.match(r"^\d+\.\s+", stripped)
                or stripped == "---"
            ):
                break
            para.append(stripped)
            i += 1
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
        else:
            i += 1

    return "\n".join(out)


def first_heading(md: str) -> str:
    for line in md.splitlines():
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1)
    return "Untitled"


def summary(md: str) -> str:
    """First paragraph after the H1, as plain text (no markup)."""
    lines = md.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if re.match(r"^#\s+", line):
            start = idx + 1
            break
    if start is None:
        return ""
    para = []
    for line in lines[start:]:
        if not line.strip():
            if para:
                break
            continue
        para.append(line.strip())
    text = " ".join(para)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    cut = text[:240].rsplit(" ", 1)[0]
    return text if len(text) <= 240 else cut + "…"


def build() -> None:
    SITE.mkdir(exist_ok=True)
    (SITE / "assets").mkdir(exist_ok=True)

    for name in ("style.css", "worksheet.js"):
        (SITE / "assets" / name).write_text(
            (ROOT / "assets" / name).read_text(encoding="utf-8"), encoding="utf-8"
        )

    md_files = sorted(CONTENT.glob("*.md"))
    if not md_files:
        raise SystemExit("No markdown files found in content/")

    pages = []
    for md_path in md_files:
        md = md_path.read_text(encoding="utf-8")
        title = first_heading(md)
        stem = md_path.stem
        html_body = md_to_html(md)
        is_index = stem == "index"
        filename = "index.html" if is_index else stem + ".html"
        html = TEMPLATE.format(
            title=title,
            description=escape(summary(md)[:150]),
            content=html_body,
        )
        (SITE / filename).write_text(html, encoding="utf-8")
        pages.append((title, filename, md))
        print("built %s <- %s" % (filename, md_path.name))

    print("wrote %d pages to %s" % (len(pages), SITE))


if __name__ == "__main__":
    build()
