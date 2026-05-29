# CV build — single source (cv.yaml) → all formats in one shot.

.PHONY: all build docx publish open clean

all: build

# Render the web page + all three PDFs + Markdown + LaTeX source.
# PDFs: cv-singlecol.pdf (Chrome), cv-twocol.pdf (Chrome), cv-latex.pdf (tectonic).
build:
	python3 build.py

# Optional: Markdown → Word, for portals that demand .docx.
docx: build
	pandoc dist/cv.md -o dist/cv.docx

# Refresh the repo-root files that external sites link to (stable URLs):
#   cv.html    -> the modern web page
#   resume.pdf -> the two-column PDF
publish: build
	cp dist/cv.html cv.html
	cp dist/cv.pdf resume.pdf

# Open the web page in the default browser.
open: build
	open dist/cv.html

clean:
	rm -rf dist
