# Linux app — QRB2210 (Debian, Python ≥ 3.11)

Decides and observes; never drives actuators except through the protocol.
Planned packages: `nav/` (map, localization against saved map, coverage route), `bridge/` (protocol client),
`web/` (phone calibration page, routes, status — lesson 11), `logging/` (JSON lines ~20 Hz, monotonic timestamps),
`vision/` (residue check SR-015 + container-level cross-check SR-016, log-only until TP-V01 passes, SR-017;
ADR-0006 lists what to reuse from the maze robot). Tests live next to code (`linux/**/test_*.py`) and reference SR IDs.
