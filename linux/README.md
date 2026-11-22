# Linux side — QRB2210 (Debian, Python ≥ 3.11)

Decides and observes; never drives actuators except through the Bridge protocol (ADR-0002). If Linux is late, the
MCU stops the robot.

## Today: `apriltag_pose/` — bench localization (ADR-0007)

App Lab app: one USB camera + printed tag36h11 tags → planar pose (x, y, yaw) of the robot. A bench tool to test pose
estimation before the LiDAR stack exists; it does not drive the robot.

| File | What it does |
|---|---|
| `app.yaml` | App Lab manifest (web UI brick) |
| `python/main.py` | Camera-mode probe (largest image with ≥ 40 fps), `cv2.aruco` detection, planar solver, ambiguity refusal, Bridge `pose` |
| `python/web.py` | Page on port 7000: map, pose, test estimate, mount calibration; camera stream **off** by default |
| `python/logbook.py` | `run.jsonl`: frame records (≈ 30 Hz), decision reasons, camera connect/disconnect — no images |
| `python/test_pose.py` | Unit tests (Jacobian, one-tag pose, unknown ID, wrong map, mount calibration, privacy) |
| `sketch/sketch.ino` | MCU side: prints validated poses only |

Requirements SR-018–SR-021 · protocol [TP-V02](../docs/test-reports/TP-V02-apriltag-localization.md) (simulation and
unit tests only; physical accuracy test pending, camera intrinsics `K_CAL` still a placeholder) · threat model
[`docs/security/threat-model.md`](../docs/security/threat-model.md).

```bash
pytest -q linux/apriltag_pose/python/test_pose.py   # needs OpenCV (cv2); skipped without it
```

## Planned (after the suction gate)

`nav/` (map, localization against a saved map, coverage route) · `bridge/` (protocol client) · `web/` (phone
calibration, routes, status — lesson 11) · `logging/` (JSON lines ≈ 20 Hz, monotonic timestamps) · `vision/` (residue
check SR-015 + container-level cross-check SR-016, log-only until TP-V01 passes, SR-017; ADR-0006). Tests live next to
the code (`linux/**/test_*.py`) and reference SR IDs.
