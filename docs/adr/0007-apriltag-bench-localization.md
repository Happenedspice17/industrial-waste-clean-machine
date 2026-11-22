# ADR-0007: AprilTag camera localization as a bench test tool

- Status: accepted (requested by the project owner, 2026-11-22)
- Date: 2026-11-22
- Requirements affected: R8, R6, SR-017, SR-018, SR-019, SR-020, SR-021

## Context
The team wanted to test pose estimation now, with one USB camera on the UNO Q and printed AprilTags, before the LiDAR
stack exists. ADR-0006 gives the camera only advisory tasks (residue check, container level) and keeps localization on
LiDAR + encoders + IMU. Two friends' repositories (AR overlays with `cv2.aruco`) were reviewed: both estimate tag
pose relative to the camera only, use an approximate camera matrix, plain `solvePnP` and run on Windows only.

## Options considered
1. **Detector:** `pupil_apriltags` vs `cv2.aruco` (`DICT_APRILTAG_36h11`). App Lab's Python image ships OpenCV; the
   `pupil_apriltags` import failed on the board and the `requirements.txt` install did not run (uv "no virtual
   environment" error).
2. **Pose:** free 6-DOF pose per tag (`solvePnP`) vs a planar 3-DOF solver (x, y, yaw) with the mount height and
   pitch fixed. In simulation a single small or oblique tag gave mirror-image poses with sub-pixel error (6-DOF).
3. **Camera mode:** fastest mode vs largest image that still meets a minimum frame rate.
4. **Web image:** stream camera frames to the page vs page with map and numbers only.

## Decision
- `cv2.aruco` detector with sub-pixel corners; IPPE square solutions only as seeds.
- Planar Gauss-Newton solver with an analytic Jacobian on all corners of all known tags. When two distinct solutions
  fit, use the one nearest a pose less than 1 s old; without one, publish **no pose** (`ambiguous_no_prior`).
  Per-tag camera positions further apart than 0.5 m → `tags_disagree` (map error), never averaged.
- Camera probe at start: choose the largest image with ≥ 40 fps measured (640×480 MJPG ≈ 45 fps on the bench camera);
  exposure from the delivered rate.
- `STREAM = False` by default; images never written to disk.
- The app stays a **bench test tool**: LiDAR + encoders + IMU remain the localization authority (ADR-0006 unchanged).
  Only validated poses go to the MCU, and the MCU sketch only prints them (SR-017, SR-019). `TEST_MODE` single-tag
  estimates are page/log only.

## Consequences
- Pose quality depends on measured `TAGS`, `TAG_SIZE`, intrinsics and mount; wrong values show up as `reproj` or
  `tags_disagree` instead of a wrong pose. A mount calibration button measures CAM_Z/CAM_PITCH (SR-021).
- A camera tilt different from the configured pitch breaks the planar model; the mount must be rigid.
- 640×480 at ~45 fps gives longer range than 320×240 at ~70 fps; at 0.38 m/s the robot moves ~8 mm per frame (deduced).
- The web page has no authentication; acceptable only on an isolated lab network (threat model T-03, T-04).

## Evidence (tests, calculations, sources)
- Simulation and bench observations: `docs/test-reports/TP-V02-apriltag-localization.md`.
- Unit tests: `linux/apriltag_pose/python/test_pose.py` (7 passed, simulation).
- Field log 2026-11-22: camera mode rates and the `reproj` diagnosis (TP-V02, "Bench observations").
