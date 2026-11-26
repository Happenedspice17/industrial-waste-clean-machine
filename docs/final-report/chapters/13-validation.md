# Validation plan and current status

Rule: acceptance criteria are fixed **before** testing, results say "simulation" or "measured (date, conditions)",
and a requirement becomes "verified" only when its test report is committed.

## What is validated and what is pending

| Aspect | Status | Evidence today | Next step |
|---|---|---|---|
| Need and requirements | ✔ Done | Literature, patents, statistics, R1–R10, 21 SR | Customer interviews (P5) |
| Coverage route | ✔ Simulation meets M3 (≥ 100 m²/h) | 167 m²/h, 96 %, 25.6 min (simulation) | Repeat on a real floor (P4) |
| Speed, braking, energy | ✔ Calculations | 0.38 m/s, ≤ 7.4 cm, ≈ 55 min | Measure on the oily floor |
| Circuits | ⚠ WCCA: battery-sense divider margin 4.1 % | `tools/wcca.py` | Retune divider, re-run with measured parts |
| **Vacuum lifts steel chips** | ⏳ **Pending — design gate** | Theory only (pickup velocity) | **Suction rig, weeks 1–3** |
| M1 recovery / M2 purity | ⏳ Pending | Estimates by scenario | Weigh tank and basket, 1 m² patch |
| Safety (e-stop, heartbeat, floats, force) | ⏳ Pending | Design in hardware; DFMEA/SCCAF | Tests linked to SC-002, SC-003, SC-006, SC-007 |
| Vision | ⏳ Log-only | Protocol TP-V01 written | Run TP-V01 on the real robot |
| AprilTag bench localization | ⚠ Simulation p90 0.09–0.11 m vs 0.10 m target | 7 unit tests; bench log | Calibrate camera, run TP-V02 |
| Economics | ✔ Calculations, 3 scenarios + tornado | `tools/econ.py` | Quotes from a real plant |

## Test plan for next semester

| Order | Test | Measure | Pass criterion | Requirements / risks |
|:-:|---|---|---|---|
| 1 | **Suction rig** | Chip lift rate (g/s), liquid recovered per pass, clogging with long chips (count per 10 runs), vacuum motor current and temperature | Decides A or B: A only if chip pickup ≥ 85 % and no clogging in 10 runs | ADR-0004, F-001, SC-001 |
| 2 | M1 recovery | Mass recovered ÷ spilled, 1 m² patch, one pass, mean of 5 runs | ≥ 85 % liquid and chips | SR-001 |
| 3 | M2 purity | Solids > 1 mm in the tank; free oil in compacted chips | ≤ 5 % solids; ≥ 90 % oil-free chips | SR-002, SR-003 |
| 4 | Speed and overspeed | Encoder log; injected overspeed | Max ≤ 0.38 m/s (0.15 cleaning); trip at 0.40 ± 0.02 m/s in 5 tests | SR-004, SR-013 |
| 5 | Braking on oil | Stopping distance from 0.38 m/s, 10 runs on reference oil | Max ≤ 0.10 m | SR-005, F-004, SC-005 |
| 6 | E-stop | Actuator rail voltage after pressing, firmware halted | All rails < 1 V within 100 ms | SR-006, F-003, SC-003 |
| 7 | Heartbeat loss | Kill the Linux app / block RPC during motion | Motion stops ≤ T_stale + 50 ms | SR-007, F-005, SC-006 |
| 8 | Float shut-off | Overfill test, 5 times | No liquid at the vacuum port | SR-008, F-002, SC-002 |
| 9 | Compactor | Load-cell peak; motion with lid open | ≤ 1030 N; no motion with lid open | SR-009, F-006, SC-007 |
| 10 | Authorization | 20 unauthorized start attempts; 10 fault resets | 0 starts without card + button | SR-010, SR-014 |
| 11 | M3 coverage | m²/h on a stored route, 3 runs | ≥ 100 m²/h, 0 incidents | SR-011 |
| 12 | Envelope | Measured dimensions | ≤ 700 × 500 × 520 mm | SR-012 |
| 13 | Vision (TP-V01) | Agreement with operator labels / floats | ≥ 90 % (residue), ≥ 95 % (level) | SR-015–SR-017 |
| 14 | AprilTag (TP-V02) | ≥ 30 taped poses | p90 ≤ 0.10 m and 5° | SR-018–SR-021 |

## Test protocol TP-V01 · Vision validation

**Status:** written 21 Nov 2026, **not run.** Refs: SR-015, SR-016, SR-017 · ADR-0006 · DFMEA F-007–F-009.

| Part | Requirement | Pass |
|---|---|---|
| V1 Residue check | SR-015 | ≥ 90 % agreement with operator labels over ≥ 200 frames; 0 motion or stop commands from vision |
| V2 Container level | SR-016 | ≥ 95 % agreement with float states over ≥ 100 checks per container; 0 stops or tool commands from vision |

**Setup.** Real robot, final camera placement, shroud + LED, exposure and gain fixed from the phone calibration page
and read back; reference lubricant and chip samples; record floor, light, temperature, battery voltage and git hash.

**Procedure.** (1) Calibrate on site and save the calibration JSON with the report. (2) V1: run cleaning strips over
clean floor, oil film and chip patches (≥ 3 of each, randomized order); the operator labels every logged frame region
(residue / clean) without seeing the vision output. (3) V2: fill and drain the tank and the chip basket through low →
half → full → low at least 5 times each; log floats and vision at 20 Hz. (4) Glare check with the area lights on/off
and with fresh oil sheen. (5) Compare logs offline (replay); count agreements, false positives, false negatives and
abstentions.

## Test protocol TP-V02 · AprilTag bench localization

**Status:** protocol written 22 Nov 2026; simulation and bench observations only; physical accuracy test not run.

| Part | Requirement | Pass |
|---|---|---|
| A Accuracy | SR-018 | ≥ 30 tape-measured robot poses at 0.8–3.5 m from 0.20 m tags: p90 position error ≤ 0.10 m and p90 yaw error ≤ 5° |
| B No wrong pose | SR-018 | 0 validated poses published while the logged reason is `ambiguous_no_prior`, `tags_disagree` or `reproj` |
| C Logging | SR-019 | Each plug/unplug gives one camera event record; ≥ 20 frame records/s while the camera runs |
| D Bridge | SR-019 | MCU Monitor shows pose lines only while the page shows OK (never during TEST ESTIMATE) |
| E Privacy | SR-020 | `STREAM = False` committed; `GET /frame.jpg` → 404; no image files after a run |
| F Mount calibration | SR-021 | CAM_Z within 0.02 m and CAM_PITCH within 1° of tape / inclinometer; values gone after restart |

**Setup.** Tags tag36h11, black square measured with a caliper; tag centers and facing directions tape-measured;
matte paper on a flat backing. Camera intrinsics calibrated first (chessboard, ≥ 15 views, `cv2.calibrateCamera`
RMS < 0.5 px). Camera mount measured (height to lens center, pitch with an inclinometer).

**Procedure.** (1) Start the app; save the camera-mode and connection log lines. (2) Privacy check. (3) Mount
calibration and restart check. (4) Accuracy: ≥ 30 poses marked with tape covering 0.8–3.5 m and ± 30° to the tags;
hold 3 s each; compute the median logged pose per hold offline. (5) Wrong-pose checks: very oblique views, one tag at
> 3 m, a deliberately wrong map entry. (6) Bridge check. (7) Logging check: unplug and replug 5 times.

| Part | Verdict today |
|---|---|
| A Accuracy | NOT RUN (simulation borderline) |
| B No wrong pose | PASS in simulation and unit tests; physical NOT RUN |
| C Logging | PASS in simulation; physical NOT RUN |
| D Bridge | NOT RUN (code inspection: Bridge notify with tag count > 0 only on reason `ok`) |
| E Privacy | PASS in simulation (`/frame.jpg` 404); physical NOT RUN |
| F Mount calibration | PASS in simulation (0.448 m / 3.1° vs 0.45 m / 3.0°); physical NOT RUN |

## Test report template

Each future test produces a report from `docs/templates/test-report.md` with: test ID and requirement IDs, date,
place and people; setup (hardware revision, git hash, materials, environment); acceptance criteria copied from the
requirement before the test; raw data location (logs as release assets, not in git); results with units; verdict
(PASS / FAIL / NOT RUN); deviations; follow-ups; and an engineering log entry with the decision.
