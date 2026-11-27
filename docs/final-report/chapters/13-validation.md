# Validation plan and current status

Rule: acceptance criteria are fixed **before** testing, results say "simulation" or "measured (date, conditions)",
and a requirement becomes "verified" only when its test report is committed.

## What is validated and what is pending

| Aspect | Status | Evidence today | Next step |
|---|---|---|---|
| Need and requirements | ✔ Done | Literature, patents, statistics, R1–R10, 25 SR | Customer interviews (P5) |
| Coverage route | ✔ Simulation meets M3 (≥ 100 m²/h) | 167 m²/h, 96 %, 25.6 min (simulation) | Repeat on a real floor (P4) |
| Speed, braking, energy | ✔ Calculations | 0.38 m/s, ≤ 7.4 cm, ≈ 52 min (165 W with dosing) | Measure on the oily floor |
| Circuits | ⚠ WCCA: battery-sense divider margin 4.1 % | `tools/wcca.py` | Retune divider, re-run with measured parts |
| **Vacuum lifts chips / removes the film** | ⚠ **Pre-test only — design gate open** | TP-S01 measured 24 Nov 2026: suction alone 0 % dry; with degreaser ≈ 85–90 % film (visual), 30 % coin mass | **TP-S02 rig with brush + degreaser + wet trap, weeks 1–3** |
| Degreaser dose, foam, slip | ⏳ Pending (ADR-0008 accepted) | Estimates (20 mL/m²) | TP-S02 parts C–G |
| M1 recovery / M2 purity | ⏳ Pending | Estimates by scenario | Weigh tank and basket, 1 m² patch |
| Safety (e-stop, heartbeat, floats, force) | ⏳ Pending | Design in hardware; DFMEA/SCCAF | Tests linked to SC-002, SC-003, SC-006, SC-007 |
| Vision | ⏳ Log-only | Protocol TP-V01 written | Run TP-V01 on the real robot |
| AprilTag bench localization | ⚠ Simulation p90 0.09–0.11 m vs 0.10 m target | 7 unit tests; bench log | Calibrate camera, run TP-V02 |
| Economics | ✔ Calculations, scenarios + tornado (dry and degreaser) | `tools/econ.py` | Measured dose; quotes from a real plant |

## Test plan for next semester

| Order | Test | Measure | Pass criterion | Requirements / risks |
|:-:|---|---|---|---|
| 1 | **Suction rig TP-S02** (brush + degreaser + wet trap) | Liquid recovered by mass, chip pickup and clogging with long chips (10 runs), dose, foam, slip, friction on the soapy film, vacuum reading | A only if chip pickup ≥ 85 % by mass and 0 clogs in 10 runs; dose ± 25 %; 0 foam at outlet; friction ≥ 0.9 × dry | ADR-0004, ADR-0008, SR-001, SR-022–SR-025, F-001, F-010, F-011, SC-001, SC-008, SC-009 |
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
| 15 | Dosing pump stop | Pump state after stop, brush off, e-stop | Off ≤ 1 s in 10 of 10 | SR-022, F-012 |
| 16 | Spray / ingress | Spray test on the assembled robot | No water inside the bay; connectors dry | F-013, SC-010 |
| 17 | Emptying procedure | Delivery log of oily water and oil | 100 % of deliveries logged, none to drain | SR-003, P-003, SC-011 |

## Test report TP-S01 · Handheld suction pre-test (measured)

**Status:** measured 24 November 2026, **exploratory** (acceptance criteria were not fixed before testing). Not the
suction rig of ADR-0004 and not the robot's vacuum. Operator: María Ruiz Mejía, home setup (not the UP lab). Source:
the operator's log in Spanish with photos (`docs/test-reports/evidence/TP-S01/`).

| Item | Value | Source |
|---|---|---|
| Vacuum | Fanttik X200 handheld cordless (dry type), direct nozzle, no brush, no squeegee | operator; listing photo |
| Vacuum rating | 16 kPa static, 40 AW | seller data, not measured |
| Oil simulant | 70 % cooking oil + 30 % liquid paraffin | operator |
| Viscosity | claimed equivalent to ISO VG 150–320 | not measured |
| "Chips" | 5 Mexican coins: $0.50 (3.103 g), 2 × $1 (3.95 g), $2 (5.19 g), $5 (7.07 g) = 23.263 g | official masses, not weighed |
| Degreaser (T4) | 300 mL water + 5 mL dish soap + 5 g baking soda | operator, photo |
| Not recorded | floor type, patch area, oil volume, passes, nozzle height and speed, temperature, battery | — |

| Test | Floor | Agent | Liquid film | Coins lifted |
|---|---|---|---|---|
| T1 | oil | none | no visible change | — |
| T2 | oil + dust | none | no visible change | — |
| T3 | oil + dust + 5 coins | none | no visible change | 0 of 5 |
| T4 | oil + dust + 5 coins | degreaser | ≈ 85–90 % of the film gone (visual estimate), light wet film left | 2 of 5: $1 + $0.50 |

![TP-S01, from left: T3 before and after (dry suction, oil + dust + 5 coins), T4 before and after (with degreaser). Photos by the operator, 24 Nov 2026.](img/tp_s01_before_after.jpg)

T4 coins: 40 % by count, 7.053 / 23.263 g = **30.3 % by mass**. The heavier coins stayed in place. The T1 "after" photo
has a different framing and light, so T1 is weak evidence.

| Item | Verdict |
|---|---|
| SR-001 liquid recovery ≥ 85 % by mass | NOT EVALUATED (no mass measured) |
| ADR-0004 option A, chip pickup ≥ 85 % — suction only | FAIL for this vacuum: 0 % dry, 30 % by mass with degreaser |
| Robot concept (brush + squeegee + wet/dry vacuum) | NOT TESTED |

**What it shows:** with this vacuum and no agitation, suction does not detach a viscous film nor lift flat 3–7 g pieces
sealed by oil; a wetting agent breaks the film and frees the lightest pieces. This supports the brush that the design
already has and led to ADR-0008. **What it does not show:** the performance of the BOM vacuum (Mikels AA-12, 80 W
wet/dry), of the brush + squeegee concept or of real chips (coins are flat discs, a worst case for the oil seal;
deduced). The X200 is a dry vacuum and should not ingest liquid; the rig uses a wet trap.

## Test protocol TP-S02 · Suction rig with brush, degreaser and wet trap

**Status:** protocol written 25 November 2026, **not run**; acceptance criteria fixed before testing. A wet trap
(a sealed rigid 3–4 L jar with a mesh basket, a ping-pong-ball float under the outlet and a demister) sits between the
nozzle and the vacuum, so the vacuum never sucks liquid and the trap can be weighed before and after each run.

| Part | Requirement | Pass |
|---|---|---|
| A Liquid recovery | SR-001 | ≥ 85 % of spilled liquid mass in the trap, mean of 5 runs, 1 m² patch, one pass |
| B Chips | ADR-0004 | Option A only if chip pickup ≥ 85 % by mass and 0 clogs in 10 runs; else option B |
| C Dose | SR-022 | Dose within ± 25 % of target over 5 runs; pump off ≤ 1 s after stop in 10 of 10 trials |
| D Foam | SR-023 | 0 foam at the trap outlet and 0 early float closures in 5 fills |
| E Slip | SR-024 | Friction ≥ 0.9 × clean dry floor on 5 strips; no standing liquid 1 min after the pass |
| F Product | SR-025 | SDS on file, not flammable, low-foam, quick-break, silicone-free |
| G Braking input | SR-005 | Friction on the soapy film measured and used to recompute stopping distance |

**Procedure (5 runs per case):** (1) dry: brush + squeegee + suction; (2) solution at 10, 20 and 40 mL/m²; (3) per run,
weigh patch inputs, trap and basket, count and weigh chips left, record vacuum reading, foam height, time and photos
from a fixed tripod; (4) slip by drag sled or inclined plane on dry, oily and cleaned floor; (5) 10 runs with long
real steel chips for clogging; (6) one row per run in a raw sheet with mean, min, max and n.

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
