# CV Modernization — Value Cadence Plan

**Goal (gating criterion):** One `cv.yaml` edit regenerates a modern responsive HTML page, a polished PDF, a LaTeX-compiled PDF, and an ATS-friendly Markdown/text file — with content brought current.

## Where the current source is telling us what matters

The corpus is thin: the existing `cv.html` plus the decisions locked in this session. No prior design doc exists to self-quote, so the two concrete problems in the source stand in:

- `cv.html:602` — `NOV 2020 - PRESENT` for Slim.AI. As of 2026-05-28 this is almost certainly stale; the content-currency pass gates "done."
- `cv.html:489-841` — entire CV is one `<table>` of Google-Docs-export cells with ~50 inline `.cNN` classes. Unmaintainable; this is *why* we move to a YAML source of truth, not why we pick any particular renderer.

## Evidence tracks (zero substrate dependency, hours)

These de-risk the two renderers we haven't built before, *before* we invest in the data model around them:

- **E1 — LaTeX toolchain spike.** Compile a one-page sample CV PDF with dummy data using a chosen class (e.g. `moderncv` / `altacv`) via `tectonic` or `latexmk`. Confirms the build works locally and the output looks good before we commit to a LaTeX renderer.
- **E2 — HTML design-direction mock.** Hand-code one static modern HTML page (no renderer, real content) to lock the visual direction with Joe. The renderer in 003 then targets an approved look instead of guessing.

## Cadence table

| # | Slice | What it demonstrates | Dep | ETA |
|---|---|---|---|---|
| E1 | LaTeX toolchain spike | A sample CV PDF compiles locally; class looks good | — | 0.5d |
| E2 | HTML design mock | Joe approves the modern visual direction | — | 0.5d |
| 001 | `cv.yaml` schema + port all current content | Every fact from `cv.html` lives in one schema-validated YAML file | — | 0.5–1d |
| 002 | Content-currency + wording pass | Roles, dates (Slim.AI end), accomplishments current and tightened | 001 | 0.5d* |
| 003 | HTML renderer + modern stylesheet | `cv.yaml` → the approved responsive HTML page | 001, E2 | 1–2d |
| 004 | PDF from HTML | A polished PDF generated headlessly from the HTML | 003 | 0.5d |
| 005 | LaTeX renderer + compiled PDF | `cv.yaml` → `.tex` → professional PDF | 001, E1 | 1d |
| 006 | Markdown/text renderer | `cv.yaml` → ATS/LinkedIn-friendly Markdown | 001 | 0.5d |
| 007 | One build command + GitHub Pages/CI | `make all` regenerates all four formats; page is live | 003,004,005,006 | 0.5–1d |

\* 002 ETA depends on Joe's input turnaround, not engineering time.

## Parallelism + proof point

- **E1, E2, and 001 are parallelizable** — no dependencies between them.
- **003, 005, 006 are parallelizable** once 001 lands — each reads `cv.yaml` independently. 004 waits on 003.
- **Proof point: 007** is the moment the fundamental goal is demonstrated — a single source edit producing all four formats with one command. (The *first* proof that the source-of-truth approach holds arrives earlier, the moment the second renderer reads the same `cv.yaml` and produces correct output.)

## Delta from prior plan

No prior plan exists. This is the initial cadence.

## First move

**E2 — the HTML design mock.** Highest information per unit time: it's zero-dependency, it's the format you most want (hostable page + print-to-PDF covers two of four outputs), and locking the visual direction now prevents rebuilding the renderer in 003 against a guessed design. E1 can run in parallel if we want LaTeX de-risked the same day. 001 (the YAML port) is foundational but mechanical — it doesn't need to gate the design decision.
