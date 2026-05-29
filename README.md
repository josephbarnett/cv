# Joseph Barnett — CV

Single-source CV. Edit **`cv.yaml`**, run **`make`**, get every format.

## Build

```sh
make            # render the web page + all 3 PDFs + Markdown + LaTeX source
make open       # build, then open the HTML page in your browser
make docx       # also produce dist/cv.docx (Markdown → Word, for ATS portals)
make clean      # remove dist/
```

## Outputs (`dist/`)

| File | What it is | Use for |
|------|------------|---------|
| `cv.html` | Modern responsive two-column page | View / host on Pages; share with humans |
| `cv-singlecol.pdf` | Modern single-column PDF | **Upload to job portals (ATS-clean)** |
| `cv-latex.pdf` | Classic LaTeX-typeset PDF | Upload (ATS-clean); the "on paper" look |
| `cv-twocol.pdf` | Two-column sidebar PDF | Share with humans — **not** for ATS |
| `cv.md` | Plain Markdown | ATS, LinkedIn, web forms |
| `cv.tex` | LaTeX source | Compiled into `cv-latex.pdf` |

See `docs/design/ats-review.md` for why the two-column layout is web/human-only:
parsers read its sidebar out of order. Single-column and LaTeX parse cleanly.

## How it works

`build.py` loads `cv.yaml` and renders the Jinja2 templates in `templates/`,
then drives headless Chrome (single- and two-column PDFs) and tectonic (LaTeX
PDF). Inline `**bold**` / `*italic*` in `cv.yaml` is converted to the right
markup per format, so the content stays format-agnostic.

## Dependencies

- **HTML, single/two-column PDF, Markdown:** Python 3 with `pyyaml` + `jinja2`,
  and Google Chrome.
- **LaTeX PDF:** `tectonic` (`brew install tectonic`). If absent, `make` builds
  everything else and skips `cv-latex.pdf`.
- **`make docx`:** `pandoc`.
