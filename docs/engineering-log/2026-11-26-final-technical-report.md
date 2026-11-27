# Engineering log — 2026-11-26 Final technical report (PROJECT.03)

- **Problem:** PROJECT.03 asks for a technical report (source + PDF) and the presentation in one ZIP; the team asked
  for an extensive report covering every course activity, in English, with the GitHub repository highlighted and a
  guide to use it.
- **Change:** New `docs/final-report/`: 27 Markdown chapters/appendices, cover, CSS, `build.sh` (pandoc → HTML →
  Playwright PDF, plus DOCX) and `gen_appendices.py` (appendices C, D, E generated from `requirements.yaml`, the
  glossary, `CHANGELOG.md` and the engineering log). `report.pdf`: 123 pages, 19 chapters, 80 references, appendices
  A (repository guide) to F. On 2026-11-27, after merging `develop` (#19), the report was updated with TP-S01
  (measured pre-test, photos), ADR-0008 (degreaser), SR-022–SR-025, DFMEA F-010–F-014, PFMEA, SCCAF SC-008–SC-011,
  WCCA dosing branch (52 min at 165 W), economics with degreaser (8.4 months, pessimistic NPV −10,926) and TP-S02;
  the submission uses presentation v4. Figures extracted from the improved proposal.
- **Evidence:** Content from `docs/00-project-context.md`, ADRs, risk registers, test protocols and the semester-1
  deliverables; numbers re-run with `tools/fmea.py`, `tools/wcca.py`, `tools/dfma.py`, `tools/econ.py`. Evidence labels
  kept (estimate / calculation / simulation); no physical test claimed. Inferences marked "(deduced)" (e.g. wheel
  torque with an assumed 35 kg mass, customer-payback reconciliation). Repository visibility checked (public).
- **Result:** Documentation only. Rendered and checked visually. Pending from the team: ACT.01–ACT.03 and PROJECT.01
  files, team member per build team, PROJECT.03 rubric. Presentation v4 is ≈ 10.5 min vs the 15-min oral slot.
