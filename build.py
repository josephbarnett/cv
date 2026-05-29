#!/usr/bin/env python3
"""Render cv.yaml into every output format.

Single source of truth: cv.yaml. Templates live in templates/.
Outputs land in dist/:

    dist/cv.html   modern responsive page (also the print-to-PDF source)
    dist/cv.pdf    polished PDF, rendered from cv.html via headless Chrome
    dist/cv.md     ATS / LinkedIn-friendly Markdown
    dist/cv.tex    LaTeX source (compile with `make pdf-latex` once a TeX
                   engine is installed)

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
    # Pull out the emphasis markers before escaping, escape the body,
    # then wrap. Done in one pass so escaping never touches the markers.
    def bold(m: re.Match) -> str:
        return r"\textbf{" + _escape_tex(m.group(1)) + "}"

    def ital(m: re.Match) -> str:
        return r"\emph{" + _escape_tex(m.group(1)) + "}"

    out, last = [], 0
    # Handle bold first, then italics on the remaining plain segments.
    for m in _BOLD.finditer(text):
        out.append(_italic_and_escape(text[last:m.start()]))
        out.append(bold(m))
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


def render(data: dict) -> None:
    DIST.mkdir(exist_ok=True)
    targets = {
        "cv.html.j2": ("cv.html", inline_html, _markup_env()),
        "cv.md.j2": ("cv.md", inline_md, _markup_env()),
        "cv.tex.j2": ("cv.tex", inline_tex, _latex_env()),
    }
    for tpl_name, (out_name, inline, env) in targets.items():
        env.filters["inline"] = inline
        tpl = env.get_template(tpl_name)
        (DIST / out_name).write_text(tpl.render(**data))
        print(f"  rendered dist/{out_name}")


def render_pdf() -> None:
    src = DIST / "cv.html"
    out = DIST / "cv.pdf"
    if not Path(CHROME).exists():
        print("  ! Chrome not found — skipping PDF. Open dist/cv.html and "
              "print to PDF, or install Chrome.")
        return
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={out}", src.resolve().as_uri()],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"  rendered dist/cv.pdf")


def main() -> int:
    data = yaml.safe_load((ROOT / "cv.yaml").read_text())
    print("Building CV from cv.yaml:")
    render(data)
    if "--no-pdf" not in sys.argv:
        render_pdf()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
