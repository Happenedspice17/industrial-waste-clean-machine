#!/usr/bin/env bash
# Build the technical report: chapters/*.md -> report.html (pandoc) -> report.pdf (Playwright/Chromium)
# and an editable report.docx (pandoc). Run from any directory.
set -euo pipefail
cd "$(dirname "$0")"

python3 gen_appendices.py

pandoc chapters/*.md \
  --from markdown+pipe_tables+raw_html+implicit_figures+tex_math_dollars \
  --to html5 --mathml --include-before-body=cover.html --standalone --embed-resources \
  --toc --toc-depth=2 --number-sections --columns=10000 \
  --css style.css \
  --metadata title="Autonomous Robot for Industrial Waste Cleaning and Separation" \
  --metadata lang=en \
  -o report.html

node render.js report.html report.pdf

python3 build_docx.py

echo "Built report.html, report.pdf, report.docx"
