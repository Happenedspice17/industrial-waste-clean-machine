# Engineering log — 2026-11-21 Single camera, AprilTag localization

- **Problem:** Owner asked for one camera only, used to locate the robot with AprilTags around the cell. ADR-0006 had
  two other camera tasks and said vision never steers.
- **Hypothesis:** Uniquely identified tags give an absolute pose that complements encoders + IMU + LiDAR; solving only
  (x, y, yaw) on the floor with an IMU heading prior is stable enough for a re-anchor.
- **Change:** ADR-0007 (proposed); SR-018; SR-015/SR-016 deferred; SR-017 covers TP-V02; `linux/vision/` (detector,
  3-DOF localizer with gates and 2-read confirmation, config loader, JSON-lines logger without frames);
  `tools/gen_apriltags.py` and `docs/apriltags/` (20 tags, 220 mm, A3); `sim/tag_visibility.py`, `sim/tag_accuracy.py`;
  TP-V02; DFMEA F-010–F-012, SCCAF SC-008; TM-V01; architecture, glossary, README.
- **Evidence (simulation):** first attempt with full 6-DOF single-tag pose gave fixes > 1 m off at 5 m from 0.5–1 px
  corner error (synthetic images) → switched to the planar solve with IMU prior. p95 error with 0.3 px noise:
  0.02 m at 1.5 m, 0.07 m at 2.5 m, 0.16 m at 3.5 m. Example layout: usable tag in 39 % of poses, longest stretch
  without a fix ≈ 9 m on the coverage route (no occlusion). Nothing measured on the robot.
- **Reasoning:** Tags are support, not authority; MCU stops are independent; output log-only until TP-V02 (rule 1–2,
  lesson 6). Range gate 4 m from the error table (estimate, to be replaced by TP-V02 midpoints).
- **Validation:** `python tools/check_all.py` passes (41 tests incl. synthetic-image detection and spoof/jump cases).
- **Result:** Pending: team confirms ADR-0007, camera calibration, measured mount, surveyed tag map, TP-V02 run.
- **N/A:** WCCA (same single USB camera as the M6 BOM, no wiring change); DFMA (tags are printed sheets on boards,
  no robot part changed; camera bracket goes through DFMA when designed).
