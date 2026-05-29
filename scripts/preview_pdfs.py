#!/usr/bin/env python3
"""Render the three candidate PDF styles for side-by-side comparison.

Throwaway preview tool. Once a style is chosen, the winner gets wired into
build.py and this script + the losing templates are deleted.

Outputs:
    dist/cv-singlecol.pdf   Chrome, polished single column
    dist/cv-twocol.pdf      Chrome, dark fixed sidebar + experience
    dist/cv-latex.pdf       tectonic (built separately from dist/cv.tex)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import build  # reuse the data loader, filters, env helpers

DIST = ROOT / "dist"
CHROME = build.CHROME


def chrome_pdf(html: Path, pdf: Path) -> None:
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf}", html.resolve().as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"  {pdf.name}")


def main() -> None:
    import yaml
    data = yaml.safe_load((ROOT / "cv.yaml").read_text())
    env = build._markup_env()
    env.filters["inline"] = build.inline_html
    DIST.mkdir(exist_ok=True)
    for tpl, html_name, pdf_name in [
        ("cv-singlecol.html.j2", "cv-singlecol.html", "cv-singlecol.pdf"),
        ("cv-twocol.html.j2", "cv-twocol.html", "cv-twocol.pdf"),
    ]:
        html = DIST / html_name
        html.write_text(env.get_template(tpl).render(**data))
        chrome_pdf(html, DIST / pdf_name)


if __name__ == "__main__":
    main()
