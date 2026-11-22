# Changelog

Every pull request adds one entry under **Unreleased** in the same PR (CI checks it). When `develop` is merged into
`main`, the Unreleased entries move under a dated release heading. Format: PR number · date · type · title, then what
changed, validation and the requirement/risk IDs touched. Stage narratives live in `docs/engineering-log/`.

## Unreleased

### #TBD · 2026-11-22 · feat · HC-SR04 level, front + rear cameras, pose fusion, cameras vs LiDAR study
- ADR-0010 revised: HC-SR04 (cheapest) instead of A02YYUW; firmware echo-to-mm with temperature compensation, host
  test and Python mirror; WCCA echo divider 15 k/22 k (margin 4.6 %, WARN) and TRIG level; DFMEA F-016 occurrence 6.
- SR-024: at least two cameras (front + rear); rear camera example config and camera list; joint multi-camera test.
- Localizer: immediate multi-tag trust only with good geometry (1-sigma ≤ 0.05 m / 1.5°); jump limit grows with
  drift. New `linux/nav/fusion.py` (variance-weighted fusion), used by the simulator.
- `sim/plant_sim.py --rig {front,front_rear,quad,lidar_front}`: 4 rigs × 20 maps; ADR-0011 proposes 2 cameras +
  low-cost ranging ring instead of the 360° LiDAR (team to decide).
- Validation: `python tools/check_all.py` passes; results are simulation only. Refs: SR-018, SR-019, SR-022, SR-024.

### #TBD · 2026-11-22 · feat · Tag pairs, privacy-first person caution, ultrasonic level, home docking, 20-map simulation
- ADR-0008 (tag stations of two, 2+ agreeing tags trusted at once, home pair, multi-camera ready), ADR-0009 (person
  detection keeps no images), ADR-0010 (ultrasonic container level). New SR-019–SR-023.
- Linux: multi-camera joint localizer with agreement gate and caution; single-tag jumps need a different tag;
  `people.py`, `pipeline.py`, `privacy.py` (buffers zeroed, fail-closed hardening, coarse 0600 logs);
  `nav/caution.py`, `nav/home.py`. Firmware: `level.{h,cpp}` (A02YYUW parser + filter) with host test.
- Tags: 26 station sheets + HOME 100–101 (US letter, 160 mm). `sim/plant_sim.py` over 20 maps
  (`docs/sim/plant-sim-20-maps.md`). TP-V03, TP-L01, TP-N01; TP-V02 updated. DFMEA F-013–F-017, SCCAF SC-009/010,
  WCCA ultrasonic UART, TM-V01 rev 2 + privacy review (cybersecurity agent). Traceability check flags undefined SR IDs.
- OpenCV pinned < 5 (HOG removed in 5.x).
- Validation: `python tools/check_all.py` passes; all results are simulation. Refs: SR-017–SR-023.

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
