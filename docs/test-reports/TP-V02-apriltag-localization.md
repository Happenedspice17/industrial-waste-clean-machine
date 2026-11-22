# Test protocol and report — TP-V02 AprilTag bench localization

Status: protocol written 2026-11-22; **simulation and bench observations only, physical accuracy test not run**.
Refs: SR-018, SR-019, SR-020, SR-021 · SR-017 (log-only gate) · ADR-0007 · threat model `docs/security/threat-model.md`
(T-01–T-06). App: `linux/apriltag_pose/` (App Lab app on the UNO Q).

## Acceptance criteria (fixed before the physical test)
| Part | Requirement | Pass |
|---|---|---|
| A Accuracy | SR-018 | ≥ 30 tape-measured robot poses at 0.8–3.5 m from 0.20 m tags: p90 position error ≤ 0.10 m and p90 yaw error ≤ 5° |
| B No wrong pose | SR-018 | 0 validated poses published while the logged reason is `ambiguous_no_prior`, `tags_disagree` or `reproj` |
| C Logging | SR-019 | Each plug/unplug gives one `camera_connected` / `camera_disconnected` / `camera_missing` record; ≥ 20 frame records/s while the camera runs |
| D Bridge | SR-019 | MCU Monitor shows pose lines only while the page shows **OK** (never during **TEST ESTIMATE**) |
| E Privacy | SR-020 | `STREAM = False` committed; `GET /frame.jpg` → 404; no image files under `python/logs/` after a run |
| F Mount calibration | SR-021 | CAM_Z within 0.02 m and CAM_PITCH within 1° of tape / inclinometer; values gone after app restart |

## Setup (physical test)
- Tags tag36h11, black square measured with a caliper and written to `TAG_SIZE`; centres and facing directions
  tape-measured into `TAGS`. Matte paper, flat backing, area lights as in the plant.
- Camera intrinsics calibrated first (chessboard, ≥ 15 views, `cv2.calibrateCamera` RMS < 0.5 px) and written to
  `K_CAL`/`D` at the calibration resolution. **The committed `K_CAL` (fx = fy = 600 px) is a placeholder.**
- Camera mount measured (height to lens centre, pitch with an inclinometer). Record git hash, camera model, mode chosen
  by the startup probe, light level.

## Procedure
1. Start the app; save the `camera_modes` and `camera_connected` log lines.
2. Privacy check (E): `curl -i http://<board>:7000/frame.jpg` → 404; after the run list `python/logs/`.
3. Mount calibration (F): camera still at its real height with one tag in view, press **Calibrate mount**; compare
   with step "Setup"; restart the app and confirm `current:` shows the committed values again.
4. Accuracy (A): mark ≥ 30 robot poses on the floor (tape + square) covering 0.8–3.5 m and ± 30° to the tags; hold
   3 s at each; note the true (x, y, yaw). Compute the median logged pose per hold from `run.jsonl` (`kind = frame`,
   `ok = true`) offline.
5. Wrong-pose checks (B): very oblique views, one tag only at > 3 m, and a deliberately wrong `TAGS` entry. Count
   validated poses whose reason is not `ok` (must be 0 by construction; the check guards against regressions).
6. Bridge (D): watch the MCU Monitor while the page alternates OK / TEST ESTIMATE / NO POSE.
7. Logging (C): unplug and replug the camera 5 times; count events; compute frame records per second.

## Results so far

### Simulation (synthetic tag images, no physical camera) — 2026-11-22
| Case | n | Position p50 / p90 | Yaw p50 / p90 | Notes |
|---|---|---|---|---|
| 0.10 m tags, tags at 0.55 m, camera 0.30 m level, no prior | 93 of 163 with tag in view | 0.038 / 0.156 m | 1.3 / 4.2° | rest refused (ambiguous) |
| 0.20 m tags, same geometry, no prior | 132 of 157 | 0.020 / 0.102 m | 0.5 / 2.6° | first solver |
| 0.20 m tags, planar solver v2, camera level | 101 of 300 random poses | 0.020 / 0.112 m | 0.5 / 2.7° | 178 poses saw no tag |
| 0.20 m tags, planar solver v2, camera pitched 7° | 101 of 300 | 0.024 / 0.091 m | 0.7 / 2.2° | |

Simulation is **borderline for criterion A** (p90 0.09–0.11 m); it has no lens distortion, blur or lighting
effects, so the physical result is expected to be worse (deduced). Unit tests `linux/apriltag_pose/python/test_pose.py`
(Jacobian, one-tag pose, unknown ID, wrong map, mount calibration, STREAM off, log without images): 7 passed.

### Bench observations on the UNO Q — 2026-11-22 (team, desk setup, untaped poses)
| Item | Measured | Source |
|---|---|---|
| Camera modes (startup probe, 30 frames each) | 320×240 MJPG req. 120 → 66.9 fps · 640×480 MJPG req. 120 → 45.2 · 320×240 YUYV 60 → 44.1 · 320×240 MJPG 60 → 34.8 · 640×480 MJPG 60 → 30.2 · 320×240 YUYV 30 → 30.2 · 640×480 MJPG 30 → 15.4 | console log 21:10 |
| Delivered rate at 320×240 MJPG | 65–75 fps typical, peaks 110–121 fps | `[1s]` lines |
| Processing time | ~5 ms per frame without tags; 15–30 ms with tags while the planar solve failed (proc 33–60 fps) | `[1s]` lines |
| Pose | every planar solve failed (`reproj` 75–81 px); single-tag fit put the camera at 0.39–0.41 m and 0–1.3° pitch vs configured 0.51 m / 6.5° | `run.jsonl` 21:16 |
| Two tags | per-tag camera positions 0.15–0.21 m and ~14° apart → `TAGS[1]` does not match the real tag | `run.jsonl` 21:16 |

Action taken: `CAM_Z = 0.40`, `CAM_PITCH = 0.5` (deduced from the log, commit 1bf64c5); mount calibration button added
for criterion F. The app has not been re-run on the board since these changes.

## Verdict
| Part | Verdict |
|---|---|
| A Accuracy | NOT RUN (simulation borderline) |
| B No wrong pose | PASS in simulation and unit tests; physical NOT RUN |
| C Logging | PASS in simulation (unplug/replug logged once each); physical NOT RUN |
| D Bridge | NOT RUN (code inspection: `Bridge.notify` with tag count > 0 only on reason `ok`) |
| E Privacy | PASS in simulation (`/frame.jpg` 404); physical NOT RUN |
| F Mount calibration | PASS in simulation (0.448 m / 3.1° vs 0.45 m / 3.0°); physical NOT RUN |

SR-018–SR-021 stay **draft** until the physical run passes.

## Follow-ups
- Calibrate intrinsics (placeholder `K_CAL`), measure `TAG_SIZE`, `TAGS` and the mount, then run steps 1–7.
- Re-run on the board after commit 1bf64c5 and the calibration button to confirm `reproj` is gone.
- Before any use outside the lab network: authentication on the web page (threat model T-03, T-04).
