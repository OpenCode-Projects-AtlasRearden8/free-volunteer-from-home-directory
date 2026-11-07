# STATUS — Kitchen-Table Volunteering

Project: static directory of at-home volunteering (transcription, citizen
science, crisis lines, tutoring, accessibility testing, craft drives),
targeting the 2026-11-07 request. Owner: Asdale Dynamics, LLC.

## What was built

- `content/` — Markdown source for 8 pages: home (index), six directory
  entries, and the pick-your-first-project worksheet page (including the
  form markup as a raw HTML block). Each entry covers time commitment,
  age notes, and signing-up steps.
- `build.py` — stdlib-only markdown-to-HTML generator (headings, lists with
  wrapped-line continuations and one nesting level, bold/italic/inline
  code/links, raw HTML passthrough). Writes `site/` and copies assets.
- `assets/style.css` — one stylesheet, no external fonts or CDNs.
- `assets/worksheet.js` — client-side scoring of the six entries against
  four questions (time, talking-to-people, hands/head/testing, 18+). No
  network calls, no storage, no tracking.
- `tests.py` — smoke tests (see verification below).
- `README.md`, `LICENSE` (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC").
- `site/` — generated output, committed for convenience (rebuild any time).
- Git initialized; single commit "Initial site: kitchen-table volunteering
  directory with build script, tests, and worksheet". Nothing pushed, no
  remote, nothing published.

## How to run it

```bash
python3 build.py     # regenerate site/ from content/
python3 tests.py     # smoke tests
python3 -m http.server --directory site   # or just open site/index.html
```

## Verification results

- `python3 build.py` — succeeds; writes 8 pages + 2 assets, printout checked.
- `python3 tests.py` — all ~130 checks pass, covering:
  - clean build and expected output files
  - each entry page contains Time commitment / Age notes / Signing-up steps
  - every internal link resolves; all pages have balanced HTML tags
  - no tracking scripts/keywords anywhere in built output; worksheet JS
    makes no network calls and stores nothing
  - no secret-shaped strings in any source or output file
  - LICENSE contains exactly one copyright line, worded exactly
    "Copyright (c) 2026 Asdale Dynamics, LLC"; README credits the LLC
- Worksheet scoring verified in Node with a stubbed DOM across 6 answer
  profiles (each expected winner matched; crisis line never suggested for
  sub-18 or non-"committed" answers).
- Local HTTP serve smoke test: all pages and the stylesheet return 200.

## Known gaps

- Program names (Smithsonian, Zooniverse, Crisis Text Line, 988, UPchieve,
  Project Linus, Knit-a-Square) are cited generically as starting points;
  no direct outbound links were embedded, and requirements (ages, training
  hours, fees) change — the pages say to check each program's own site.
- The worksheet is deliberately simple scoring, not a full quiz; no
  explanations per question beyond the summary text.
- Markdown subset is intentionally small; unsupported syntax renders
  literally rather than erroring (documented in build.py's docstring).
- No dark mode, search, or RSS; not needed at this scope but easy to add.
- site/ is committed as generated output; a future CI could rebuild it.
