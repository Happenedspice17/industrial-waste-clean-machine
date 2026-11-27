# Final technical report — source files

Technical report of the final capstone project (*Proyecto Mecatrónico I*, PROJECT.03, 27 Nov 2026).
Repository: https://github.com/Happenedspice17/industrial-waste-clean-machine

| File | Content |
|---|---|
| `chapters/*.md` | One Markdown file per chapter (00 front matter … 19 conclusions, 20 references, 21–26 appendices) |
| `cover.html` | Cover page |
| `style.css` | Page layout and styles (A4) |
| `img/` | Figures (from the improved proposal, the README and the coverage simulation) |
| `gen_appendices.py` | Generates appendices C (requirements), D (glossary) and E (history) from the repository files |
| `render.js` | Prints the HTML to PDF with Chromium (Playwright), with header, footer and page numbers |
| `build.sh` | Runs everything: appendices → HTML → PDF → DOCX |
| `report.pdf` | Built report (deliverable) |
| `report.html` | Built report as one self-contained web page |
| `report.docx` | Editable Word version (inline SVG diagrams and the cover box are not included in Word) |

Build (from a clone of the repository): `cd docs/final-report && ./build.sh`. Needs pandoc ≥ 3, Python 3 with PyYAML,
and Node.js with Playwright/Chromium. `gen_appendices.py` reads `requirements/requirements.yaml`,
`docs/07-glossary.md`, `CHANGELOG.md` and `docs/engineering-log/`, so it must run inside the repository.
