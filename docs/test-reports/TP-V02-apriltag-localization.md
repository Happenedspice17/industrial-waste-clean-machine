# Test protocol — TP-V02 Single-camera AprilTag localization

Status: written 2026-11-21, **not run**. Refs: SR-018, SR-019, SR-017 · ADR-0007, ADR-0008 · DFMEA F-010–F-012 · SC-008 · TM-V01.
Each run produces a test report from `docs/templates/test-report.md`. `NAV_ENABLED` in `linux/vision/localizer.py`
is switched on only after this protocol passes and its report is committed.

## Acceptance criteria (fixed before testing)
| Part | Pass |
|---|---|
| L1 Static accuracy | ≥ 95 % of accepted fixes within 0.10 m / 3° (tag 0.5–2.5 m) and 0.25 m / 5° (2.5–4.0 m) of the surveyed pose; ≥ 200 fixes at ≥ 20 poses |
| L2 Moving | Robot at 0.15 and 0.38 m/s along a taped lane: same limits against the tape line (cross-track) and lane heading |
| L1b Tag pairs | Multi-tag fixes (both tags of a station in view) accepted in the same frame, within SR-018 limits in ≥ 95 % (SR-019) |
| L3 Robustness | 0 accepted fixes from: an unmapped tag ID, one tag of a pair moved 0.5 m, a tag half covered, a printed tag held by hand and moved; printed copy of a whole pair recorded (expected to pass the pair check: P-15, F-013) |
| L4 Logging | Every frame logged (ok/fail, IDs, corners, status, reasons); no image files written |

## Setup
1. Print tags with `python tools/gen_apriltags.py --ids 0-25 --size-mm 160 --paper LETTER --out build/apriltags` at
   100 % (no "fit to page"). Measure each black square with a steel rule; reject a sheet > 1 mm off; write the measured
   size in the tag map.
2. Glue on rigid, flat, matte board; mount in stations of two (centres 0.60 m apart, same height and facing), vertical, "TOP" up, facing the work area. Survey each tag centre (x, y, z)
   and facing direction with tape + laser distance meter from two cell corners; save `tag_map.json` with the report.
3. Calibrate the camera at its working resolution with a checkerboard (≥ 20 views, OpenCV `calibrateCamera`); fix
   exposure and gain; save intrinsics and the measured mount (x, y, z, yaw, pitch) in `camera.json`.
4. Record floor, lighting (lux at 3 points), temperature, battery voltage, git hash.

## Procedure
1. L1: place the robot at ≥ 20 surveyed poses (taped marks, heading by a square) at 0.5–4.0 m from the tags, with
   1–3 tags in view; log 30 s each with `python -m linux.vision.tag_logger --tags tag_map.json --camera camera.json
   --out L1_<pose>.jsonl --seconds 30`.
2. L2: drive taped lanes at both speeds, 5 runs each, logging tags + odometry at ~20 Hz.
3. L3: run each spoof/move case for 60 s while static and while moving.
4. Repeat L1 at 5 poses with area lights off/on and with a light oil film on one tag (expect "rejected", not wrong).
5. Replay the logs offline (lesson 10): error per fix, rejection reasons, measured corner noise (px) and range at
   which the error passes the limit. Set the gates at the midpoint between passing and failing readings (rule 5).

## Records
Raw logs as release assets (not in git), tag map, camera calibration, photos of each tag mount and the setup, test
report with the gate values chosen, engineering log entry with the decision (enable `NAV_ENABLED` or not).
