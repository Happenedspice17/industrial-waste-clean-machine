"""Build an editable Word version of the report (report.docx) from chapters/*.md.

Word cannot show the inline SVG diagrams, the cover HTML or the styled boxes, so this script:
renders each inline <svg> to a PNG (Chromium via render_svg.js), turns the GitHub box, tiles and notes into plain
Markdown, adds a title page, and runs pandoc to DOCX. Run from docs/final-report/ (build.sh does it).
"""

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
TMP = HERE / "build-docx"
REPO = "https://github.com/Happenedspice17/industrial-waste-clean-machine"

TITLE_PAGE = f"""---
title: "Autonomous Robot for Industrial Waste Cleaning and Separation"
subtitle: "Final capstone project · Technical report · Proyecto Mecatrónico I · Universidad Panamericana"
author:
  - Franco Zavala Morgan
  - María Ruiz Mejía
  - Manuel Harari López
  - Ian Carlo Olivares Chávez
  - Carlos Emiliano Escamilla Garibay
  - Luis Roberto Sánchez Salgado
  - Juan Manuel Vásquez Paniagua
date: "Professor: Dr. Hiram Eredín Ponce Espinosa · 27 November 2026 · Repository: {REPO}"
lang: en
---

![Final concept, side cutaway](img/final_concept.png)

![Scan to open the GitHub repository](img/repo_qr.png){{width=35mm}}

**GitHub repository: [{REPO.removeprefix("https://")}]({REPO})**

"""


def svg_to_png(svgs: list[str]) -> list[str]:
    TMP.mkdir(exist_ok=True)
    paths = []
    for i, svg in enumerate(svgs):
        src = TMP / f"svg_{i}.svg"
        src.write_text(svg, encoding="utf-8")
        paths.append(f"build-docx/svg_{i}.png")
    subprocess.run(["node", "render_svg.js", str(TMP), str(len(svgs))], check=True, cwd=HERE)
    return paths


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def convert(md: str, svg_paths: list[str], counter: list[int]) -> str:
    def fig(m: re.Match) -> str:
        cap = strip_tags(m.group(2)) if m.group(2) else ""
        path = svg_paths[counter[0]]
        counter[0] += 1
        return f"\n![{cap}]({path})\n"

    md = re.sub(r"<figure>\s*(<svg.*?</svg>)\s*(?:<figcaption>(.*?)</figcaption>)?\s*</figure>", fig, md, flags=re.S)

    # GitHub box → highlighted block
    def ghbox(m: re.Match) -> str:
        inner = m.group(0)
        body = re.search(r"<div>\s*\n(.*?)\n</div>\s*\n</div>\s*\n</div>", inner, flags=re.S)
        text = body.group(1) if body else ""
        text = re.sub(r'<span class="badge">(.*?)</span>', r"**[\1]**", text)
        return (
            f"> **GITHUB REPOSITORY: [{REPO.removeprefix('https://')}]({REPO})**\n>\n"
            + "\n".join("> " + line for line in text.strip().splitlines())
            + "\n\n![Scan to open the repository](img/repo_qr.png){width=30mm}\n"
        )

    md = re.sub(r'<div class="gh-box">.*?\n</div>\s*\n</div>\s*\n</div>', ghbox, md, flags=re.S)

    # tiles → bullet list
    def tiles(m: re.Match) -> str:
        items = re.findall(r'<div class="n">(.*?)</div><div class="d">(.*?)</div>', m.group(0))
        return "\n" + "\n".join(f"- **{strip_tags(n)}** — {strip_tags(d)}" for n, d in items) + "\n"

    md = re.sub(r'<div class="tiles">.*?\n</div>', tiles, md, flags=re.S)

    # notes → blockquote
    md = re.sub(
        r'<div class="note">\s*\n(.*?)\n</div>',
        lambda m: "\n".join("> " + line for line in m.group(1).strip().splitlines()),
        md,
        flags=re.S,
    )
    md = re.sub(r'<span class="badge">(.*?)</span>', r"**[\1]**", md)
    return md


def main() -> None:
    files = sorted((HERE / "chapters").glob("*.md"))
    texts = [f.read_text(encoding="utf-8") for f in files]
    svgs = [s for t in texts for s in re.findall(r"<svg.*?</svg>", t, flags=re.S)]
    svg_paths = svg_to_png(svgs)
    counter = [0]
    body = "\n\n".join(convert(t, svg_paths, counter) for t in texts)
    src = TMP / "report-docx.md"
    src.write_text(TITLE_PAGE + body, encoding="utf-8")
    subprocess.run(
        [
            "pandoc",
            str(src),
            "--from",
            "markdown+pipe_tables+raw_html+implicit_figures+tex_math_dollars",
            "--to",
            "docx",
            "--toc",
            "--toc-depth=2",
            "--number-sections",
            "--columns=10000",
            "--resource-path=.",
            "--reference-doc=reference.docx",
            "-o",
            "report.docx",
        ],
        check=True,
        cwd=HERE,
    )
    print(f"report.docx built ({len(svgs)} diagrams rendered)")


if __name__ == "__main__":
    main()
