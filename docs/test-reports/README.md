# Test protocols and reports

One file per test from [`docs/templates/test-report.md`](../templates/test-report.md). Acceptance criteria are fixed
**before** testing; results say "simulation" or "measured (date, conditions)". Reference requirement IDs
(`Refs: SR-005`) so `tools/check_traceability.py` can find them.

| ID | Test | Refs | Status |
|---|---|---|---|
| [TP-V01](TP-V01-vision-validation.md) | Vision: residue check + container level vs floats | SR-015–SR-017, ADR-0006 | Protocol written, not run |
| [TP-V02](TP-V02-apriltag-localization.md) | AprilTag bench localization: accuracy, no wrong pose, logging, privacy, mount calibration | SR-017–SR-021, ADR-0007 | Simulation + 7 unit tests; physical test pending |

Next: suction rig (ADR-0004, SC-001), then M1–M3 and safety tests (SC-002, SC-003, SC-005–SC-007).
