# Joseph Barnett — CV

Single-source CV. Edit **`cv.yaml`**, run **`make`**, get every format.

## Build

```sh
make            # → dist/cv.html, dist/cv.pdf, dist/cv.md, dist/cv.tex
make open       # build, then open the HTML page in your browser
make pdf-latex  # compile dist/cv.tex → PDF (needs tectonic; see below)
make clean      # remove dist/
```

## Outputs (`dist/`)

| File | What it is |
|------|------------|
| `cv.html` | Modern responsive page. Host on GitHub Pages; print to PDF from the browser. |
| `cv.pdf`  | Polished PDF, rendered from `cv.html` via headless Chrome — matches the page exactly. |
| `cv.md`   | Plain Markdown for ATS, LinkedIn, and web forms. |
| `cv.tex`  | LaTeX source for the "looks great on paper" route. |

## How it works

`build.py` loads `cv.yaml` and renders three Jinja2 templates in `templates/`
(`cv.html.j2`, `cv.md.j2`, `cv.tex.j2`), then drives headless Chrome to produce
the PDF. Inline `**bold**` / `*italic*` in `cv.yaml` is converted to the right
markup per format, so the content stays format-agnostic.

## Dependencies

- **HTML, PDF, Markdown, LaTeX source:** Python 3 with `pyyaml` + `jinja2`,
  and Google Chrome (for the PDF). No other installs.
- **LaTeX → PDF (`make pdf-latex`):** a TeX engine. Recommended:
  `brew install tectonic` (single binary, fetches packages on demand).
  Not required for the Chrome PDF above.
