# Kitchen-Table Volunteering

A free, static directory of volunteering you can do from home: archive
transcription, citizen science, remote crisis-line volunteering, online
tutoring, accessibility testing, and craft drives. Every entry lists a
realistic time commitment, age notes, and plain-English signing-up steps —
plus a pick-your-first-project worksheet that runs entirely in your browser.

Free to use, copy, and share under the [MIT License](LICENSE). © 2026
Asdale Dynamics, LLC. Built in the plain-English, beginner-friendly spirit of
[The Massive AI Manual](https://dylanasdale.github.io) by Dylan Asdale.

## Run it

You need Python 3 (nothing else — no packages, no network access to build).

```bash
python3 build.py      # regenerates site/ from content/
python3 tests.py      # runs the smoke tests
```

Then open `site/index.html` in any browser (double-click it, or serve the
folder with `python3 -m http.server` if you prefer).

## Layout

```
content/   Markdown source — edit these to change the site
build.py   Minimal stdlib markdown -> HTML generator (writes site/)
tests.py   Smoke tests: build, links, headings, no-tracking checks
assets/    One stylesheet and one small script (worksheet scoring)
site/      Generated output — safe to delete and rebuild
```

## How it works

- Each `content/*.md` file becomes one HTML page; `content/index.md` becomes
  `site/index.html`. The markdown subset (headings, lists, bold/italic,
  links, fenced raw HTML blocks like the worksheet form) is deliberately
  small and covered by `tests.py`.
- The worksheet is a tiny script that scores the six entries against your
  answers using the same plain-language guidance the entries give. It makes
  no network requests and stores nothing.
- No accounts, cookies, analytics, fonts-from-CDNs, or tracking of any kind.

## Editing the content

Edit a file in `content/`, run `python3 build.py`, refresh the page. For
worksheets, the form HTML lives in `content/worksheet.md` and the scoring
lives in `assets/worksheet.js` — change answers wording, re-run
`python3 tests.py` to make sure the scoring entries still line up.

## Credits

Made by **Asdale Dynamics, LLC** — beginner-friendly AI education, books,
guides, and practical tools. This project is standalone and pairs well with
its siblings: a volunteer **shift** board (for scheduling) and a local
in-person help directory (for town-level resources).

This directory is general information about volunteering, not legal, medical,
or crisis advice. Volunteer requirements (ages, background checks, training
hours) change — always check the program's own site before signing up.
