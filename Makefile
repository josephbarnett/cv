# CV build — single source (cv.yaml) → all formats.
# `make` regenerates HTML, PDF (via headless Chrome), Markdown, and LaTeX source.

.PHONY: all build pdf-latex open clean

all: build

# Render HTML, Markdown, LaTeX source, and the Chrome-based PDF.
build:
	python3 build.py

# Compile dist/cv.tex to a PDF. Requires a TeX engine (tectonic recommended:
#   brew install tectonic
pdf-latex: build
	cd dist && tectonic cv.tex

# Open the generated HTML page in the default browser.
open: build
	open dist/cv.html

clean:
	rm -rf dist
