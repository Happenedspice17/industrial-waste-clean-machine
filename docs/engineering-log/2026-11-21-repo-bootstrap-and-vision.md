# Engineering log — 2026-11-21 Repository bootstrap and vision role

- **Problem:** Project kit and semester-1 deliverables were not in GitHub; some deliverables were in Spanish; the vision
  function (R6) had no defined task.
- **Hypothesis:** Applying the maze-robot camera lessons (assist only, log first, calibrate on site) avoids repeating
  its false-wall failure on a glossy floor.
- **Change:** Kit imported; standards table and pairwise workbook translated to English; ADR-0006 accepted (residue
  check + container-level cross-check, validation gate); SR-015–SR-017; DFMEA F-007–F-009; protocol TP-V01;
  `pip install -e` fix; `claude/*` branches allowed; definition of done added to `CLAUDE.md`.
- **Evidence:** `python tools/check_all.py` passes. Vision numbers are from the maze robot's simulation and one field
  run (sumo-v-ia); nothing measured on this robot.
- **Reasoning:** Floats and LiDAR/bumpers keep authority; vision errors only cost an extra pass or an operator check.
- **Result:** Pending: camera placement (DFMA), USB hub power budget (WCCA), TP-V01 run.
- **Commits:** 8d376b0 (bootstrap) and the vision follow-up on branch `claude/magical-mendel-rphq63`.
