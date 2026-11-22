# Engineering log — 2026-11-22 AprilTag bench localization app

- **Problem:** The team wanted to see the robot pose now, with one USB camera on the UNO Q and printed AprilTags,
  before the LiDAR stack exists; there was no firmware or Linux code in the repo.
- **Hypothesis:** A planar (x, y, yaw) solver with the camera height and pitch fixed avoids the mirror-pose ambiguity
  of single small tags and can run at camera rate on the QRB2210 with OpenCV already in the App Lab image.
- **Change:** App Lab app `linux/apriltag_pose/` (Python `main.py`, `web.py`, `logbook.py`; MCU sketch that prints the
  pose): `cv2.aruco` detection, planar solver with analytic Jacobian, ambiguity and tag-map checks, threaded capture,
  startup camera-mode probe (largest image with ≥ 40 fps), JSONL log with decision reasons and camera
  connect/disconnect events, web page on port 7000 (map, test estimate, mount calibration; camera stream off by
  default). SR-018–SR-021, ADR-0007, threat model rev 1, TP-V02, unit tests.
- **Evidence:** Simulation only for accuracy (TP-V02 tables: p90 0.09–0.11 m, 2.2–2.7° with 0.20 m tags). Bench
  observations on the board (2026-11-22, desk, untaped): camera mode rates, 5 ms/frame without tags, every planar
  solve failing with 75–81 px reprojection because the configured mount (0.51 m / 6.5°) did not match the fitted one
  (0.39–0.41 m / 0–1.3°). Unit tests 7 passed. `python tools/check_all.py` result in the PR.
- **Reasoning:** Applied lessons: thresholds from data (mount taken from the log fit, then a calibration button),
  log every decision, one bad reading never becomes a pose (refuse ambiguous/inconsistent views), simulate before
  tuning. Vision stays log-only (SR-017); LiDAR + encoders + IMU remain the localization authority (ADR-0006/0007).
  Not applicable this time: DFMA/DFMEA (no new part), PFMEA (no process step), WCCA (no wiring change; camera on the
  existing USB port), safety-function checks (no actuator command), SCCAF (no YC/YS row).
- **Result:** The camera delivers 640×480 ≈ 45 fps or 320×240 ≈ 70 fps (probe on the board); the app now picks
  640×480, not yet run on the board in that mode. Pose not yet validated
  on the board: intrinsics are a placeholder, tag map and mount must be measured, then TP-V02 run.
- **Commits:** 33c693a, cbd67a0, 5af5410, 6d7114e, 1bf64c5, 1ce109c and the documentation commit on branch
  `claude/funny-hopper-ikvbpt`.
