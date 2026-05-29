# CV build — single source (cv.yaml) → all formats in one shot.

.PHONY: all build docx open clean

all: build

# Render the web page + all three PDFs + Markdown + LaTeX source.
# PDFs: cv-singlecol.pdf (Chrome), cv-twocol.pdf (Chrome), cv-latex.pdf (tectonic).
build:
	python3 build.py

# Optional: Markdown → Word, for portals that demand .docx.
docx: build
	pandoc dist/cv.md -o dist/cv.docx

# Open the web page in the default browser.
open: build
	open dist/cv.html

clean:
	rm -rf dist
