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

pandoc chapters/*.md \
  --from markdown+pipe_tables+raw_html+implicit_figures+tex_math_dollars \
  --to docx --toc --toc-depth=2 --number-sections --columns=10000 \
  --resource-path=. \
  --metadata title="Autonomous Robot for Industrial Waste Cleaning and Separation — Technical report" \
  --metadata subtitle="Proyecto Mecatrónico I · Universidad Panamericana · 27 November 2026 · github.com/Happenedspice17/industrial-waste-clean-machine" \
  --metadata author="Franco Zavala Morgan; María Ruiz Mejía; Manuel Harari López; Ian Carlo Olivares Chávez; Carlos Emiliano Escamilla Garibay; Luis Roberto Sánchez Salgado; Juan Manuel Vásquez Paniagua" \
  -o report.docx

echo "Built report.html, report.pdf, report.docx"
