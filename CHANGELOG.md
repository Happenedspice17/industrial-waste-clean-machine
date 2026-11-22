# Changelog

Every pull request adds one entry under **Unreleased** in the same PR (CI checks it). When `develop` is merged into
`main`, the Unreleased entries move under a dated release heading. Format: PR number · date · type · title, then what
changed, validation and the requirement/risk IDs touched. Stage narratives live in `docs/engineering-log/`.

## Unreleased

### #TBD · 2026-11-21 · feat · Single-camera AprilTag localization
- ADR-0007 (proposed): one camera, AprilTag 36h11 re-anchors the pose; residue and container checks (SR-015, SR-016)
  deferred. New SR-018; SR-017 covers TP-V02.
- `linux/vision/`: detector, 3-DOF floor-pose localizer (IMU heading prior, gates, 2-read confirmation, log-only),
  config loader, JSON-lines logger that never saves frames. `tools/gen_apriltags.py` + `docs/apriltags/` (IDs 0–19,
  160 mm, US letter). `sim/tag_visibility.py`, `sim/tag_accuracy.py`. Optional dependency group `vision` (OpenCV, NumPy).
- TP-V02, DFMEA F-010–F-012, SCCAF SC-008, threat model TM-V01, architecture, glossary, README, engineering log.
- Validation: `python tools/check_all.py` passes; results are simulation only. Refs: SR-015, SR-016, SR-017, SR-018.

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
