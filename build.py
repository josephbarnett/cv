#!/usr/bin/env python3
"""Render cv.yaml into every output format.

Single source of truth: cv.yaml. Templates live in templates/.
Outputs land in dist/:

    dist/cv.html            modern responsive web page (host / view; the look
                            you keep — not meant for ATS upload)
    dist/cv-singlecol.pdf   modern single-column PDF — ATS-clean, upload this
    dist/cv-twocol.pdf      two-column sidebar PDF — matches the web page, for
                            sharing with humans (sidebar scrambles in ATS)
    dist/cv-latex.pdf       classic LaTeX-typeset PDF — ATS-clean
    dist/cv.md              ATS / LinkedIn-friendly Markdown
    dist/cv.tex             LaTeX source (compiled to cv-latex.pdf)

Inline emphasis in cv.yaml uses **bold** / *italic*; this script converts
those markers to the correct markup for each format so the YAML stays
format-agnostic.
"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
TEMPLATES = ROOT / "templates"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITAL = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")

# Characters that must be escaped in LaTeX text.
_TEX_ESCAPE = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def inline_html(text: str) -> str:
    text = html.escape(text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITAL.sub(r"<em>\1</em>", text)
    return text


def inline_md(text: str) -> str:
    # Markdown markers are already native; leave them as-is.
    return text


def inline_tex(text: str) -> str:
    out, last = [], 0
    for m in _BOLD.finditer(text):
        out.append(_italic_and_escape(text[last:m.start()]))
        out.append(r"\textbf{" + _escape_tex(m.group(1)) + "}")
        last = m.end()
    out.append(_italic_and_escape(text[last:]))
    return "".join(out)


def _italic_and_escape(text: str) -> str:
    out, last = [], 0
    for m in _ITAL.finditer(text):
        out.append(_escape_tex(text[last:m.start()]))
        out.append(r"\emph{" + _escape_tex(m.group(1)) + "}")
        last = m.end()
    out.append(_escape_tex(text[last:]))
    return "".join(out)


def _escape_tex(text: str) -> str:
    return "".join(_TEX_ESCAPE.get(c, c) for c in text)


def _markup_env() -> Environment:
    """Default Jinja env for HTML/Markdown (standard {{ }} / {% %} syntax)."""
    return Environment(
        loader=FileSystemLoader(TEMPLATES),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )


def _latex_env() -> Environment:
    """LaTeX-safe Jinja env. LaTeX uses {, }, %, # heavily, so the template
    delimiters are remapped to \\VAR{} / \\BLOCK{} to avoid collisions."""
    return Environment(
        loader=FileSystemLoader(TEMPLATES),
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )


# (template, output, inline filter, env factory)
TEXT_TARGETS = [
    ("cv.html.j2", "cv.html", inline_html, _markup_env),
    ("cv-singlecol.html.j2", "cv-singlecol.html", inline_html, _markup_env),
    ("cv-twocol.html.j2", "cv-twocol.html", inline_html, _markup_env),
    ("cv.md.j2", "cv.md", inline_md, _markup_env),
    ("cv.tex.j2", "cv.tex", inline_tex, _latex_env),
]


def render_text(data: dict) -> None:
    DIST.mkdir(exist_ok=True)
    for tpl_name, out_name, inline, env_factory in TEXT_TARGETS:
        env = env_factory()
        env.filters["inline"] = inline
        (DIST / out_name).write_text(env.get_template(tpl_name).render(**data))
        print(f"  rendered dist/{out_name}")


def _chrome_pdf(html_name: str, pdf_name: str) -> None:
    if not Path(CHROME).exists():
        print(f"  ! Chrome not found — skipping dist/{pdf_name}")
        return
    src = (DIST / html_name).resolve().as_uri()
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={DIST / pdf_name}", src],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"  rendered dist/{pdf_name}")


def _latex_pdf() -> None:
    if shutil.which("tectonic") is None:
        print("  ! tectonic not found — skipping dist/cv-latex.pdf "
              "(install: brew install tectonic)")
        return
    subprocess.run(["tectonic", "cv.tex"], cwd=DIST, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (DIST / "cv.pdf").replace(DIST / "cv-latex.pdf")
    print("  rendered dist/cv-latex.pdf")


def build_pdfs() -> None:
    _chrome_pdf("cv-singlecol.html", "cv-singlecol.pdf")
    _chrome_pdf("cv-twocol.html", "cv-twocol.pdf")
    _latex_pdf()
    # Primary deliverable: the two-column layout (cv.pdf). Single-column and
    # LaTeX remain as ATS-clean alternatives for portals that need them.
    if (DIST / "cv-twocol.pdf").exists():
        shutil.copyfile(DIST / "cv-twocol.pdf", DIST / "cv.pdf")
        print("  cv.pdf -> two-column (primary)")


def main() -> int:
    data = yaml.safe_load((ROOT / "cv.yaml").read_text())
    print("Building CV from cv.yaml:")
    render_text(data)
    if "--no-pdf" not in sys.argv:
        build_pdfs()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
