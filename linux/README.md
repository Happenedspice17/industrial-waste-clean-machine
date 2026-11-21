# Linux app — QRB2210 (Debian, Python ≥ 3.11)

Decides and observes; never drives actuators except through the protocol.
Planned packages: `nav/` (map, localization against saved map, coverage route), `bridge/` (protocol client),
`web/` (phone calibration page, routes, status — lesson 11), `logging/` (JSON lines ~20 Hz, monotonic timestamps),
`vision/` (residue check, log-only until SR-015 passes; ADR-0006 lists what to reuse from the maze robot). Tests live next to code (`linux/**/test_*.py`) and reference SR IDs.
