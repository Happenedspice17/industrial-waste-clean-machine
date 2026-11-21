# Test protocol — TP-V01 Vision validation (residue check + container level)

Status: written 2026-11-21, **not run**. Refs: SR-015, SR-016, SR-017 · ADR-0006 · DFMEA F-007–F-009.
Each run produces a test report from `docs/templates/test-report.md`; an action flag is enabled only after its part passes.

## Acceptance criteria (fixed before testing)
| Part | Requirement | Pass |
|---|---|---|
| V1 Residue check | SR-015 | ≥ 90 % agreement with operator labels over ≥ 200 frames; 0 motion or stop commands from vision |
| V2 Container level | SR-016 | ≥ 95 % agreement with float states over ≥ 100 checks per container; 0 stops or tool commands from vision |

## Setup
Real robot, final camera placement, shroud + LED, exposure/gain fixed from the phone calibration page and read back.
Reference lubricant and chip samples (ADR-0004). Record floor, light, temperature, battery voltage, git hash.

## Procedure
1. Calibrate on site (lesson 11); save the calibration JSON with the report.
2. V1: run cleaning strips over clean floor, oil film and chip patches (≥ 3 of each, randomized order). The operator
   labels every logged frame region (residue / clean) without seeing the vision output.
3. V2: fill and drain the tank and the chip basket through low → half → full → low at least 5 times each; log
   floats and vision at 20 Hz.
4. Glare check: repeat a subset with the area lights on/off and with fresh oil sheen.
5. Compare logs offline (replay, lesson 10); count agreements, false positives, false negatives, abstentions.

## Records
Raw logs as release assets (not in git), labels CSV, calibration JSON, photos of the setup, test report, and an
engineering log entry with the decision (enable flag or not).
