# Linux app — QRB2210 (Debian, Python ≥ 3.11)

Decides and observes; never drives actuators except through the protocol.
Planned packages: `nav/` (map, localization against saved map, coverage route), `bridge/` (protocol client),
`web/` (phone calibration page, routes, status — lesson 11), `logging/` (JSON lines ~20 Hz, monotonic timestamps),
`vision/` (single-camera AprilTag localization SR-018, ADR-0007; log-only until TP-V02 passes, SR-017).

### nav/ (implemented, simulation-tested only)
`caution.py` (speed cap near people/obstacles/blind camera, SR-020) · `home.py` (return home and dock on the home
tag pair, SR-023).

### vision/ (implemented, simulation-tested only)
`detector.py` (OpenCV AprilTag 36h11 corners) → `localizer.py` (3-DOF floor pose from all cameras; 2+ agreeing
tags accepted at once, one tag with IMU prior + 2-read confirmation; `NAV_ENABLED = False`) · `people.py` +
`pipeline.py` + `privacy.py` (person summaries only, buffers zeroed, fail-closed hardening, SR-021) · `config.py` (tag map + camera JSON) · `tag_logger.py` (camera → JSON
lines 0600, never saves frames) · `config/*.example.json` (placeholders, replace with surveyed/calibrated values).
Tags: `python tools/gen_apriltags.py`; layout and accuracy: `sim/tag_visibility.py`, `sim/tag_accuracy.py`. Tests live next to code (`linux/**/test_*.py`) and reference SR IDs.
