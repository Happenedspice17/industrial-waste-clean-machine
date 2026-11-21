# ADR-0006: Vision assists only — residue check and container-level cross-check, enabled only after validation

- Status: accepted (tasks confirmed by the project owner, 2026-11-21) · Requirements: R6, R9, SR-015, SR-016, SR-017

## Context
R6 (vision, importance 6) has no defined task yet. M6 lists a USB webcam (COM-126) and an LED light; the pessimist
scenario adds glare, reflective metal and oil sheen. The team's previous UNO Q robot (maze solver,
github.com/Happenedspice17/sumo-v-ia, `uno_q_v2/python/main.py`, `docs/historial_cambios.md`) used a
camera; this is what it did and what happened:

| Topic | What the maze robot did | Result |
|---|---|---|
| Hardware | OV9281 mono global-shutter USB camera on the Linux side (OpenCV + V4L2), 320 × 240, buffer 1, 3 frames flushed before each read | Worked |
| Pipeline | Median blur 5 → contrast stretch (2–98 % of the lower half, skipped if the range is < 25 grey levels) → Otsu threshold on the lower half, clamped to 100–220 → binary floor/wall | Worked on a matte floor |
| Geometry | Pixel → floor point (mm) from lens height 162 mm and tilt 40° taken from CAD; tilt recalibrated on site against the front ToF | CAD tilt was wrong (changed 25° → 40°); on-site calibration needed |
| Calibration | Phone web page, saved to JSON: fixed exposure and gain, sensitivity offset, straight-ahead column, rad/pixel, tilt. Reads back what the driver really applied | Auto exposure moved the threshold with light and people; some drivers ignore settings |
| Glare | A wall had to extend ≥ 14 image rows; shorter white blobs were treated as floor reflections | Added after the first track run |
| Role | Camera went from leader → tie-breaker → off. Rule: it never blocks a path; a camera hit only slows the robot and the ToF double-checks | ToF became the authority for walls |
| Simulation | Camera model (pixel noise, missing columns, bad frames, tilt error) plus drawn images through the same code | 99 % correct free cells ahead; 94 % wall/opening when it answered (no answer 30 %); runs 98–100 % with or without camera: **no measurable gain** (simulation) |
| Field | First v2 track run (2026-11-13): glossy black floor reflected the light → false walls. That run also had a clock jump and a gyro-sign bug; total 8 losses, 9 crashes | `CAM_LOC = False`; camera kept logging what it saw (CSV line C) to compare with the map. Never re-validated with real photos |
| Integration | `/dev/video0–1` are internal on the UNO Q → probe only existing `/dev/video*` from index 2; a background thread re-finds the camera every 2 s; a lock shares it between the robot loop and the web page | With the UNO Q powered from VIN its USB-C gives no 5 V to the hub: the hub needs its own PD supply; a "dumb" USB-C → USB-A OTG adapter fixed recognition |

## Options considered (vision task)
- **A. Residue check on the cleaned strip:** a downward camera under a shroud with its own LED looks at the floor just
  behind the squeegee and flags patches of oil film or chips; the planner adds a re-pass. Error cost: a false positive
  adds one pass, a false negative is today's situation.
- **B. Spill detection ahead:** set speed/tools before reaching a patch. Error cost: needless slow-downs; open-floor
  lighting = the maze-robot glare problem on a shinier floor.
- **D. Container-level cross-check:** a camera looks at the liquid tank (translucent wall or sight strip) and the
  chip basket and reports low / half / full. The float switches stay the authority; vision only flags a disagreement
  ("check floats") in the log, LCD and web UI. Error cost: a needless operator check.
- **C. Person / obstacle detection:** rejected. ISO 3691-4 4.8.2 stays with LiDAR + bumpers; a webcam is not a
  safety sensor.

## Decision
1. Vision has two tasks: **A residue check** (SR-015, output = re-pass request) and **D container-level
   cross-check** (SR-016, output = "check floats" warning). It never stops, steers or blocks the robot and never
   feeds a safety function; the float shut-off and level cut-off stay in hardware/MCU.
2. **Validation gate (extra step, SR-017):** both tasks start in log-only mode. Every decision goes to the raw run log
   next to the operator's ground truth. Each action flag (one per task, all off = display + log) is enabled only after
   its validation protocol passes on the real robot (`docs/test-reports/TP-V01-vision-validation.md`) and the test
   report is committed.
3. Controlled lighting: shroud + own LED, fixed exposure and gain set from the phone calibration page on site, values
   read back and logged. Test a cross-polarized LED/lens pair against oil sheen (to verify).
4. Before tuning: capture a labelled photo set on the real floor (clean, oil film, chips) under the robot's LED; the
   simulator and drawn images replay it, never replace it.
5. Reuse the integration fixes above: index ≥ 2, hot-plug thread, camera lock, background open, PD-powered hub.

## Consequences
SR-015, SR-016, SR-017 added (draft); DFMEA rows F-004–F-006. One camera cannot see the floor and both containers
(deduced): placement (second USB camera or mirror) must go through DFMA, and the USB hub power budget through WCCA,
before buying parts. Sensor hierarchy row for vision updated in `docs/02-architecture.md`. Check that the COM-126
accepts manual exposure through V4L2 (`v4l2-ctl --list-ctrls`) before relying on it; if not, reuse the OV9281.
Measure USB bandwidth/power with LiDAR + camera on the same hub (ADR-0001).

## Evidence
Maze-robot code and change log cited above (simulation and one field run; no photo dataset). No tests on this robot
yet; validation protocol TP-V01 written, not run.
