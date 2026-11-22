# Changelog

Every pull request adds one entry under **Unreleased** in the same PR (CI checks it). When `develop` is merged into
`main`, the Unreleased entries move under a dated release heading. Format: PR number · date · type · title, then what
changed, validation and the requirement/risk IDs touched. Stage narratives live in `docs/engineering-log/`.

## Unreleased

### #14 · 2026-11-22 · docs · Lighter final presentation v2 and updated READMEs
- Presentation: GitHub link on the cover and the closing slide.
- README refreshed with current facts: 21 SR, 7 ADRs, threat model rev 1, AprilTag bench app (ADR-0007, TP-V02),
  IEEE 7000 EVRs, links to the 10-slide presentation. Folder READMEs updated (`requirements/`, `linux/`, `sim/`,
  `firmware/mcu/`, `cad/`, `docs/test-reports/`, `docs/engineering-log/` index, `docs/semester-1-deliverables/`);
  new `risk/README.md` and `tools/README.md`.
- `Final_Presentation_Waste_Robot_v2.pptx` simplified as a reference deck: short phrases per slide; goal tree and
  black/white boxes redrawn as simple diagrams; detail moved to speaker notes. Same 10 slides and IEEE 7000 EVRs.
- Validation: pptx schema check passes, visual QA of every slide; `python tools/check_all.py` passes.
  Refs: R1–R10 (presentation only).

### #13 · 2026-11-22 · docs · Final presentation v2 with IEEE 7000 EVRs
- New `docs/semester-1-deliverables/Final_Presentation_Waste_Robot_v2.pptx`: 19 → 10 slides (≤ 10 min) following
  the proposal structure, with speaker notes; requirements slide adds EVR-01–EVR-03 (IEEE 7000-2021).
- Engineering log `docs/engineering-log/2026-11-22-final-presentation-v2.md`.
- Validation: pptx schema check passes, visual QA of every slide; `python tools/check_all.py` passes.
  Refs: R1–R10 (presentation only; EVRs not yet in requirements.yaml).

### #12 · 2026-11-22 · fix · CI workflow rejected at parse time
- `ci.yml`: `hashFiles()` in the `firmware` job-level `if:` is not allowed there, so GitHub rejected the whole
  workflow with zero jobs on every run (e.g. `develop` at f07284c). The job now runs always; a first step detects
  firmware sources (`find … | grep -q .` → `found` output) and guards the apt install, clang-format and cppcheck steps.
- Validation: `actionlint` reproduces the error on the old file and passes on the new one; clean venv
  `pip install -e ".[dev]"` OK; ruff, traceability, DFMEA, WCCA and pytest (24 passed, 1 skipped: no `cv2`) pass;
  `python tools/check_all.py` passes. Refs: N/A (tooling).

### #11 · 2026-11-22 · feat · AprilTag bench localization app (App Lab)
- New `linux/apriltag_pose/`: one USB camera + tag36h11 tags → planar pose (x, y, yaw) on the UNO Q; refuses
  ambiguous or inconsistent views; startup camera-mode probe (largest image with ≥ 40 fps); JSONL log with decision
  reasons and camera connect/disconnect events; web page on port 7000 (map, test estimate, mount calibration, camera
  stream off by default); MCU sketch prints validated poses only.
- SR-018–SR-021 (draft), ADR-0007, threat model rev 1 (`docs/security/threat-model.md`), protocol/report TP-V02,
  engineering log, unit tests; ruff per-file ignores for the App Lab script.
- Validation: simulation and unit tests (7 passed); bench observations on the board 2026-11-22 (camera mode rates,
  mount mismatch found in the log). Physical accuracy test not run. Refs: SR-017–SR-021, ADR-0007.

## v0.1.0 · 2026-11-21 · Initial design baseline

First release to `main`: initial design (not frozen), waiting on the vacuum (suction rig) test (ADR-0004).

### #9 · 2026-11-21 · release · v0.1.0 to main
- Merged `develop` into `main` through `release/v0.1.0`; Unreleased entries #1–#8 moved under this heading.
- Validation: `python tools/check_all.py` passes. Refs: N/A (tooling).

### #8 · 2026-11-21 · chore · Changelog for every PR
- Added this changelog with entries for PRs #1–#7.
- CI (`branch-policy` → `policy`) fails if a PR does not change `CHANGELOG.md`; PR template and definition of done
  (`CLAUDE.md` rule 12) ask for the entry.
- Validation: `python tools/check_all.py` passes. Refs: N/A (tooling).

### #7 · 2026-11-21 · docs · README showcase with the validation toolkit
- README restyled after the sumo-v-ia README: badges, concept image, flow/state/architecture diagrams, modules.
- New "Engineering validation toolkit": DFMEA top risks, SCCAF rule and register, WCCA results, DFMA, economics.
- Images `docs/img/robot_side_view.jpg` and `docs/img/coverage_simulation.png` taken from the final presentation.
- Validation: numbers copied from tool outputs with evidence labels; links checked.

### #6 · 2026-11-21 · docs · AI-use dates
- README credits: Claude (chat) since August 2026; Claude Code on this repository since November 2026.

### #5 · 2026-11-21 · docs · Credits, prior work and AI-use statement
- README section with team authorship, advisor, prior work (sumo-v-ia), AI contributions, review rules for AI output
  and APA-style references for the AI tools.

### #4 · 2026-11-21 · chore · Status "initial design" and cybersecurity agent
- Status in README and `CLAUDE.md`: initial design, not frozen; waiting on the vacuum (suction rig) test (ADR-0004).
- New `cybersecurity-engineer` agent and `/security` command (vision, web UI, RPC, RFID, Linux, Wi-Fi, logs,
  firmware, supply chain; security never weakens safety); threat-model template; glossary terms; PR checklist item.

### #3 · 2026-11-21 · docs · Professional README
- First structured README: problem, solution, architecture, key figures with evidence level, safety, setup, workflow,
  documentation index, roadmap.

### #2 · 2026-11-21 · docs · Glossary and internal SCCAF
- `docs/07-glossary.md` (IDs, method, robot, plant, git, Spanish ↔ English).
- `docs/08-sccaf.md` + `risk/sccaf.csv` (SC-001–SC-007): YC = S 9–10, YS = S 5–8 and O 4–10 → CC/SC.
- `tools/fmea.py` computes the class, checks the SCCAF register and rejects duplicate IDs; tests added.
- Fix: duplicate DFMEA IDs from #1 — vision rows renumbered F-007–F-009.
- Refs: SR-001, SR-005–SR-009, SR-016.

### #1 · 2026-11-21 · chore · Repository bootstrap in English with vision role
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
