# Appendix E · Change history and engineering log {.unnumbered}

## E.1 Engineering log entries {.unnumbered}

One entry per stage in `docs/engineering-log/` (problem, hypothesis, change, evidence, reasoning, result, commits).

| Date | Entry |
|---|---|
| 2026-11-21 | Credits and AI-use statement |
| 2026-11-21 | Design phase close (semester 1) |
| 2026-11-21 | Glossary and internal SCCAF |
| 2026-11-21 | Status "initial design" and cybersecurity agent |
| 2026-11-21 | README showcase (sumo-v-ia style) |
| 2026-11-21 | Professional README |
| 2026-11-21 | Repository bootstrap and vision role |
| 2026-11-22 | AprilTag bench localization app |
| 2026-11-22 | CI workflow parse fix |
| 2026-11-22 | Final presentation v2 (10 slides, IEEE 7000 EVRs) |
| 2026-11-24 | Final presentation v3 (Business Model Canvas diagram) |
| 2026-11-25 | Degreaser adopted (ADR-0008) and suction rig with wet trap (TP-S02) |
| 2026-11-25 | Handheld suction pre-test (TP-S01) and presentation v4 |
| 2026-11-26 | Final technical report (PROJECT.03) |

## E.2 Changelog {.unnumbered}

From `CHANGELOG.md`.

Every pull request adds one entry under **Unreleased** in the same PR (CI checks it). When `develop` is merged into
`main`, the Unreleased entries move under a dated release heading. Format: PR number · date · type · title, then what
changed, validation and the requirement/risk IDs touched. Stage narratives live in `docs/engineering-log/`.

### Unreleased {.unnumbered}

#### #22 · 2026-11-27 · docs · Final report cites presentation v4 {.unnumbered}
- `docs/final-report/chapters/02-methodology.md` and the engineering log: the PROJECT.03 submission uses
  `Final_Presentation_Waste_Robot_v4.pdf`; `report.pdf` rebuilt. Also merges `main`
  back into `develop` (v0.3.0 release heading and version). New `docs/final-report/build_docx.py` + `render_svg.js` +
  `reference.docx`: the Word version keeps the diagrams (SVG → PNG), title page, GitHub box and bordered tables.
- Validation: `python tools/check_all.py` passes; report rebuilt. Refs: N/A (documentation).

### v0.3.0 · 2026-11-27 · Final technical report, first suction pre-test and degreaser decision {.unnumbered}

Still initial design (not frozen), waiting on the suction rig (TP-S02: brush + degreaser + wet trap, ADR-0004). No
prototype yet; one exploratory pre-test (TP-S01) led to the low-dose degreaser (ADR-0008).

#### #21 · 2026-11-27 · release · v0.3.0 to main {.unnumbered}
- Merged `develop` into `main` through `release/v0.3.0`; Unreleased entries #19 and #20 moved under this heading;
  `pyproject.toml` version 0.3.0.
- Validation: `python tools/check_all.py` passes. Refs: N/A (tooling).

#### #20 · 2026-11-27 · docs · Final technical report (PROJECT.03) {.unnumbered}
- New `docs/final-report/`: chapter sources (Markdown), cover, styles, build script and generated appendices; built
  `report.pdf` (123 pages) with the repository highlighted on the cover, a "Read this first" section and a full
  repository guide (Appendix A). Includes #19: TP-S01 (with photos), ADR-0008, SR-022–SR-025, PFMEA, SCCAF
  SC-008–SC-011, economics with degreaser and TP-S02.
- Engineering log `docs/engineering-log/2026-11-26-final-technical-report.md`; `.gitignore` excludes the HTML/DOCX
  build outputs and the local submission bundle.
- Validation: `python tools/check_all.py`; report rendered to PDF and checked visually. Refs: R1–R10 (documentation only).

#### #19 · 2026-11-25 · feat · Low-dose degreaser adopted (ADR-0008) and suction rig protocol with wet trap (TP-S02) {.unnumbered}
- ADR-0008 accepted: low-foam, quick-break degreaser sprayed ahead of the brush (≈ 20 mL/m², estimate); still two
  waste streams. New SR-022–SR-025; DFMEA F-010–F-014 (F-004 updated); new PFMEA `risk/pfmea.csv` (P-001–P-003),
  checked by `tools/fmea.py` (process_step accepted as item) and `check_all.py`; SCCAF SC-008–SC-011; WCCA dosing
  pump branch, runtime 52 min at 165 W.
- `tools/econ.py`: `DEGREASER` scenario is the base (net 46,731/yr, payback 8.4 months, NPV 79,529; pessimistic NPV
  −10,926); `activity06` keeps the old numbers; tests added.
- TP-S02 protocol: wet trap between nozzle and vacuum, brush + dose sweep, foam, slip and A/B criteria fixed before
  testing. TP-S01 and ADR-0004 point to it.
- Context, architecture, standards (NOM-018-STPS-2015), business/BMC, SDG, glossary, README, CLAUDE.md key numbers
  and `Final_Presentation_Waste_Robot_v4` (slides 5, 7, 8, 10, 11, 12 + notes) updated.
- Validation: `python tools/check_all.py` passes; pptx validator passes, changed slides rendered and checked.
  Refs: SR-001, SR-005, SR-022–SR-025, ADR-0004, ADR-0008, F-004, F-010–F-014, P-001–P-003, SC-008–SC-011.

#### #19 · 2026-11-25 · test · Handheld suction pre-test evidence (TP-S01) and presentation v4 {.unnumbered}
- New `docs/test-reports/TP-S01-handheld-suction-pretest.md` + `docs/test-reports/evidence/TP-S01/` (operator log
  PDF with photos re-encoded under 5 MB, original SHA-256 recorded; extracted before/after photos; vacuum listing).
  Measured 2026-11-24 (María Ruiz Mejía, exploratory, home setup): suction only, no brush — dry 0 % visible removal and
  0 of 5 coins; with degreaser ≈ 85–90 % film removed (visual) and 2 of 5 coins (30.3 % by mass).
- ADR-0004 "Evidence so far" (still open); test-reports index, README status, engineering log.
- `Final_Presentation_Waste_Robot_v4.pptx/.pdf`: v3 + slide 10 "First suction test"; slide 9 and next-steps notes.
- Validation: pptx validator passes, slide rendered and checked; `python tools/check_all.py` passes.
  Refs: SR-001, ADR-0004, F-001, F-002, SC-001.

### v0.2.1 · 2026-11-24 · Final presentation v3 with Business Model Canvas {.unnumbered}

Still initial design (not frozen), waiting on the suction rig test (ADR-0004). No physical test results yet.

#### #18 · 2026-11-24 · release · v0.2.1 to main {.unnumbered}
- Merged `develop` into `main` through `release/v0.2.1`; Unreleased entry #17 moved under this heading;
  `pyproject.toml` version 0.2.1.
- Validation: `python tools/check_all.py` passes. Refs: N/A (tooling).

#### #17 · 2026-11-24 · docs · Final presentation v3 with Business Model Canvas diagram {.unnumbered}
- New `docs/semester-1-deliverables/Final_Presentation_Waste_Robot_v3.pptx` + `.pdf`: v2 plus slide 10
  "Business Model Canvas" in the 9-block diagram layout (content from `docs/04-business.md`, costs from
  `tools/econ.py`, labelled as estimates); notes trimmed to ≈ 10 min total; cover says "Final capstone presentation".
- Validation: pptx schema validator passes; rendered to PDF and checked visually. Refs: N/A (documentation).

### v0.2.0 · 2026-11-22 · AprilTag bench app and final presentation v2 {.unnumbered}

Still initial design (not frozen), waiting on the suction rig test (ADR-0004). No physical test results yet.

#### #15 · 2026-11-22 · release · v0.2.0 to main {.unnumbered}
- Merged `develop` into `main` through `release/v0.2.0`; Unreleased entries #11–#14 moved under this heading;
  `pyproject.toml` version 0.2.0.
- Validation: `python tools/check_all.py` passes. Refs: N/A (tooling).

#### #14 · 2026-11-22 · docs · Lighter final presentation v2 and updated READMEs {.unnumbered}
- Presentation: GitHub link and QR code on the cover and the closing slide (`docs/img/repo_qr.png`).
- README refreshed with current facts: 21 SR, 7 ADRs, threat model rev 1, AprilTag bench app (ADR-0007, TP-V02),
  IEEE 7000 EVRs, links to the 10-slide presentation. Folder READMEs updated (`requirements/`, `linux/`, `sim/`,
  `firmware/mcu/`, `cad/`, `docs/test-reports/`, `docs/engineering-log/` index, `docs/semester-1-deliverables/`);
  new `risk/README.md` and `tools/README.md`.
- `Final_Presentation_Waste_Robot_v2.pptx` simplified as a reference deck: short phrases per slide; goal tree and
  black/white boxes redrawn as simple diagrams; detail moved to speaker notes. Same 10 slides and IEEE 7000 EVRs.
- Validation: pptx schema check passes, visual QA of every slide; `python tools/check_all.py` passes.
  Refs: R1–R10 (presentation only).

#### #13 · 2026-11-22 · docs · Final presentation v2 with IEEE 7000 EVRs {.unnumbered}
- New `docs/semester-1-deliverables/Final_Presentation_Waste_Robot_v2.pptx`: 19 → 10 slides (≤ 10 min) following
  the proposal structure, with speaker notes; requirements slide adds EVR-01–EVR-03 (IEEE 7000-2021).
- Engineering log `docs/engineering-log/2026-11-22-final-presentation-v2.md`.
- Validation: pptx schema check passes, visual QA of every slide; `python tools/check_all.py` passes.
  Refs: R1–R10 (presentation only; EVRs not yet in requirements.yaml).

#### #12 · 2026-11-22 · fix · CI workflow rejected at parse time {.unnumbered}
- `ci.yml`: `hashFiles()` in the `firmware` job-level `if:` is not allowed there, so GitHub rejected the whole
  workflow with zero jobs on every run (e.g. `develop` at f07284c). The job now runs always; a first step detects
  firmware sources (`find … | grep -q .` → `found` output) and guards the apt install, clang-format and cppcheck steps.
- Validation: `actionlint` reproduces the error on the old file and passes on the new one; clean venv
  `pip install -e ".[dev]"` OK; ruff, traceability, DFMEA, WCCA and pytest (24 passed, 1 skipped: no `cv2`) pass;
  `python tools/check_all.py` passes. Refs: N/A (tooling).

#### #11 · 2026-11-22 · feat · AprilTag bench localization app (App Lab) {.unnumbered}
- New `linux/apriltag_pose/`: one USB camera + tag36h11 tags → planar pose (x, y, yaw) on the UNO Q; refuses
  ambiguous or inconsistent views; startup camera-mode probe (largest image with ≥ 40 fps); JSONL log with decision
  reasons and camera connect/disconnect events; web page on port 7000 (map, test estimate, mount calibration, camera
  stream off by default); MCU sketch prints validated poses only.
- SR-018–SR-021 (draft), ADR-0007, threat model rev 1 (`docs/security/threat-model.md`), protocol/report TP-V02,
  engineering log, unit tests; ruff per-file ignores for the App Lab script.
- Validation: simulation and unit tests (7 passed); bench observations on the board 2026-11-22 (camera mode rates,
  mount mismatch found in the log). Physical accuracy test not run. Refs: SR-017–SR-021, ADR-0007.

### v0.1.0 · 2026-11-21 · Initial design baseline {.unnumbered}

First release to `main`: initial design (not frozen), waiting on the vacuum (suction rig) test (ADR-0004).

#### #9 · 2026-11-21 · release · v0.1.0 to main {.unnumbered}
- Merged `develop` into `main` through `release/v0.1.0`; Unreleased entries #1–#8 moved under this heading.
- Validation: `python tools/check_all.py` passes. Refs: N/A (tooling).

#### #8 · 2026-11-21 · chore · Changelog for every PR {.unnumbered}
- Added this changelog with entries for PRs #1–#7.
- CI (`branch-policy` → `policy`) fails if a PR does not change `CHANGELOG.md`; PR template and definition of done
  (`CLAUDE.md` rule 12) ask for the entry.
- Validation: `python tools/check_all.py` passes. Refs: N/A (tooling).

#### #7 · 2026-11-21 · docs · README showcase with the validation toolkit {.unnumbered}
- README restyled after the sumo-v-ia README: badges, concept image, flow/state/architecture diagrams, modules.
- New "Engineering validation toolkit": DFMEA top risks, SCCAF rule and register, WCCA results, DFMA, economics.
- Images `docs/img/robot_side_view.jpg` and `docs/img/coverage_simulation.png` taken from the final presentation.
- Validation: numbers copied from tool outputs with evidence labels; links checked.

#### #6 · 2026-11-21 · docs · AI-use dates {.unnumbered}
- README credits: Claude (chat) since August 2026; Claude Code on this repository since November 2026.

#### #5 · 2026-11-21 · docs · Credits, prior work and AI-use statement {.unnumbered}
- README section with team authorship, advisor, prior work (sumo-v-ia), AI contributions, review rules for AI output
  and APA-style references for the AI tools.

#### #4 · 2026-11-21 · chore · Status "initial design" and cybersecurity agent {.unnumbered}
- Status in README and `CLAUDE.md`: initial design, not frozen; waiting on the vacuum (suction rig) test (ADR-0004).
- New `cybersecurity-engineer` agent and `/security` command (vision, web UI, RPC, RFID, Linux, Wi-Fi, logs,
  firmware, supply chain; security never weakens safety); threat-model template; glossary terms; PR checklist item.

#### #3 · 2026-11-21 · docs · Professional README {.unnumbered}
- First structured README: problem, solution, architecture, key figures with evidence level, safety, setup, workflow,
  documentation index, roadmap.

#### #2 · 2026-11-21 · docs · Glossary and internal SCCAF {.unnumbered}
- `docs/07-glossary.md` (IDs, method, robot, plant, git, Spanish ↔ English).
- `docs/08-sccaf.md` + `risk/sccaf.csv` (SC-001–SC-007): YC = S 9–10, YS = S 5–8 and O 4–10 → CC/SC.
- `tools/fmea.py` computes the class, checks the SCCAF register and rejects duplicate IDs; tests added.
- Fix: duplicate DFMEA IDs from #1 — vision rows renumbered F-007–F-009.
- Refs: SR-001, SR-005–SR-009, SR-016.

#### #1 · 2026-11-21 · chore · Repository bootstrap in English with vision role {.unnumbered}
- Imported the project kit (context, ADRs, requirements, risk files, tools, CI, Claude Code agents and commands,
  semester-1 deliverables); `develop` created from `main` after merge.
- Translated the Spanish deliverables: standards table PDF rebuilt, pairwise workbook translated in place (formulas
  and formatting kept), brief and file names in English; "bitácora" → engineering log, "ODS" → SDG.
- ADR-0006 accepted: vision is advisory — residue check (SR-015) and container-level cross-check (SR-016), log-only
  until protocol TP-V01 passes (SR-017); DFMEA rows added.
- Definition of done in `CLAUDE.md` (DFMA, DFMEA/PFMEA, WCCA, ADR, test report, log entry per task); solo-owner
  GitHub setup.
- Fixes: `pip install -e` package discovery; `claude/*` session branches accepted by `check_branch.py`.
- Validation: `python tools/check_all.py` passes. Refs: SR-015, SR-016, SR-017.

