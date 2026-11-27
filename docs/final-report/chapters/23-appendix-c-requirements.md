# Appendix C · Requirements: full text {.unnumbered}

Generated from `requirements/requirements.yaml` (single source of truth). Status values: draft → approved → verified; a requirement is verified only when its test report is committed.

## C.1 Stakeholder requirements {.unnumbered}

| ID | Requirement | Importance (1-10) |
|---|---|:-:|
| R1 | Lubricant suction / collection | 10 |
| R2 | Solid-chip separation | 10 |
| R3 | Compaction system | 6 |
| R4 | Compact size | 2 |
| R5 | Safety system | 6 |
| R6 | Vision system | 6 |
| R7 | Safe mobility | 10 |
| R8 | Route storage and mapping | 6 |
| R9 | Separate solid and liquid containers | 10 |
| R10 | Operating authorization | 4 |

## C.2 System requirements {.unnumbered}

### SR-001 · parent R1 · module M3 · must {.unnumbered}

> The collection system shall recover at least 85 % of the spilled liquid mass in one pass over a 1 m2 test patch with the reference lubricant.

| Field | Value |
|---|---|
| Rationale | Metric M1 (liquid). |
| Verification | Test |
| Acceptance | >= 85 % mass recovered, mean of 5 runs |
| Status | draft |
| Verified by | — |

### SR-002 · parent R2 · module M4 · must {.unnumbered}

> The separation module shall deliver a solid stream with at least 90 % mass free of drainable oil after compaction.

| Field | Value |
|---|---|
| Rationale | Metric M2 (solids). |
| Verification | Test |
| Acceptance | >= 90 % |
| Status | draft |
| Verified by | — |

### SR-003 · parent R9 · module M5 · must {.unnumbered}

> The liquid stream in the storage tank shall contain no more than 5 % by mass of solids larger than 1 mm.

| Field | Value |
|---|---|
| Rationale | Metric M2 (liquid). |
| Verification | Test |
| Acceptance | <= 5 % solids > 1 mm (filtered and weighed) |
| Status | draft |
| Verified by | — |

### SR-004 · parent R7 · module M2 · must {.unnumbered}

> The robot shall limit its commanded speed to 0.38 m/s in any mode and to 0.15 m/s while cleaning.

| Field | Value |
|---|---|
| Rationale | Speed limit (ISO 3691-4 4.3). |
| Standard | ISO 3691-4:2023 4.3 |
| Verification | Test |
| Acceptance | Encoder log max <= 0.38 m/s (0.15 m/s cleaning) |
| Status | draft |
| Verified by | — |

### SR-005 · parent R7 · module M2 · must {.unnumbered}

> The robot shall stop within 0.10 m from 0.38 m/s on a floor contaminated with the reference lubricant.

| Field | Value |
|---|---|
| Rationale | Braking on oil; calculation gives <= 7.4 cm at mu = 0.1. |
| Standard | ISO 3691-4:2023 4.2 |
| Verification | Test |
| Acceptance | Max of 10 runs <= 0.10 m |
| Status | draft |
| Verified by | — |

### SR-006 · parent R5 · module M8 · must {.unnumbered}

> Actuating the emergency stop shall remove power from all actuators through a hardware relay independent of software within 100 ms.

| Field | Value |
|---|---|
| Rationale | Safety does not depend on software. |
| Standard | ISO 3691-4:2023 4.8.1; ISO 13850 |
| Verification | Test |
| Acceptance | All actuator rails < 1 V within 100 ms with firmware halted |
| Status | draft |
| Verified by | — |

### SR-007 · parent R5 · module M7 · must {.unnumbered}

> The MCU shall stop all motion if no valid command or heartbeat is received from Linux for longer than T_stale.

| Field | Value |
|---|---|
| Rationale | Lesson 1 — if Linux is late the robot stops. T_stale TBD (measure RPC latency; initial 300 ms). |
| Verification | Test |
| Acceptance | Motion stops <= T_stale + 50 ms after heartbeat loss |
| Status | draft |
| Verified by | — |

### SR-008 · parent R5 · module M5 · must {.unnumbered}

> The vacuum unit shall be switched off before liquid reaches the vacuum port, by a float shut-off acting in hardware.

| Field | Value |
|---|---|
| Rationale | Protection term 8. |
| Verification | Test |
| Acceptance | No liquid at port in 5 overfill tests |
| Status | draft |
| Verified by | — |

### SR-009 · parent R3 · module M4 · must {.unnumbered}

> The compactor shall limit pressing force to 100 kgf (981 N) +/- 5 % and run only with the chamber lid closed.

| Field | Value |
|---|---|
| Rationale | Protection term 9; NOM-004-STPS interlock. |
| Verification | Test |
| Acceptance | Load-cell peak <= 1030 N; no motion with lid open |
| Status | draft |
| Verified by | — |

### SR-010 · parent R10 · module M9 · must {.unnumbered}

> The robot shall start a cleaning cycle only after a valid RFID card is read and the start button is pressed.

| Field | Value |
|---|---|
| Rationale | Authorized operation (R10). |
| Verification | Test |
| Acceptance | 0 starts in 20 unauthorized attempts |
| Status | draft |
| Verified by | — |

### SR-011 · parent R8 · module M6 · should {.unnumbered}

> The robot shall save a map and a cleaning route and repeat the route with a coverage rate of at least 100 m2/h and zero safety incidents.

| Field | Value |
|---|---|
| Rationale | Metric M3. Simulation estimate 167 m2/h (12 x 8 m cell). |
| Verification | Test |
| Acceptance | >= 100 m2/h on stored route, 0 incidents, 3 runs |
| Status | draft |
| Verified by | — |

### SR-012 · parent R4 · module M1 · should {.unnumbered}

> The robot envelope shall not exceed 700 x 500 x 520 mm (L x W x H to LiDAR top).

| Field | Value |
|---|---|
| Rationale | Compact size; fits plant aisles. |
| Verification | Inspection |
| Acceptance | Measured envelope within limits |
| Status | draft |
| Verified by | — |

### SR-013 · parent SR-004 · module M2 · must {.unnumbered}

> The MCU shall stop all motion when the speed measured by the encoders exceeds 0.40 m/s.

| Field | Value |
|---|---|
| Rationale | Overspeed detection independent of the speed command. |
| Standard | ISO 3691-4:2023 4.3.1 |
| Verification | Test |
| Acceptance | Stop triggered at 0.40 m/s +/- 0.02 m/s in 5 injected-overspeed tests |
| Status | draft |
| Verified by | — |

### SR-014 · parent R5 · module M9 · must {.unnumbered}

> After any stop caused by a fault or the emergency stop, the robot shall require a new valid RFID card read and a start-button press before moving again.

| Field | Value |
|---|---|
| Rationale | No automatic restart. |
| Standard | ISO 3691-4:2023 4.1.14 |
| Verification | Test |
| Acceptance | No motion after fault reset without card + button in 10 tests |
| Status | draft |
| Verified by | — |

### SR-015 · parent R6 · module M6 · should {.unnumbered}

> The vision function shall flag residue patches of at least 50 x 50 mm (oil film or chips) left on the cleaned strip, agreeing with operator inspection in at least 90 % of logged frames.

| Field | Value |
|---|---|
| Rationale | R6 task proposed in ADR-0006 (option A, team to confirm). Output is only a re-pass request; vision never stops, steers or blocks the robot. |
| Verification | Test |
| Acceptance | >= 90 % agreement with operator labels over >= 200 frames on the real floor under the robot LED; 0 motion or stop commands issued by vision |
| Status | draft |
| Verified by | — |

### SR-016 · parent R9 · module M6 · should {.unnumbered}

> The vision function shall classify the fill level of the liquid tank and of the chip basket as low, half or full, agreeing with the float switches in at least 95 % of logged checks.

| Field | Value |
|---|---|
| Rationale | Container-level cross-check (ADR-0006 option D). Floats stay the authority; a disagreement only raises a "check floats" warning. |
| Verification | Test |
| Acceptance | >= 95 % agreement with float states over >= 100 checks per container (fill and drain cycles); 0 stops or tool commands issued by vision |
| Status | draft |
| Verified by | — |

### SR-017 · parent R6 · module M6 · must {.unnumbered}

> Each vision output shall remain in log-only mode until its validation protocol TP-V01 passes on the real robot and the test report is committed.

| Field | Value |
|---|---|
| Rationale | Validation gate (ADR-0006); camera was untrustworthy on a glossy floor in the maze robot. |
| Verification | Inspection |
| Acceptance | Action flags default to off in code; each enabled flag cites a committed TP-V01 report |
| Status | draft |
| Verified by | — |

### SR-018 · parent R8 · module M6 · should {.unnumbered}

> The AprilTag bench localization app shall estimate the robot planar pose (x, y, yaw) from one USB camera and tag36h11 markers at measured positions with a 90th-percentile error of at most 0.10 m and 5 deg at 0.8-3.5 m from 0.20 m tags, and report no pose instead of an ambiguous or inconsistent one.

| Field | Value |
|---|---|
| Rationale | Test tool for the localization of R8 (ADR-0007). LiDAR + encoders + IMU stay the localization authority; this app only measures and logs. |
| Verification | Test |
| Acceptance | Physical run per TP-V02: p90 position error <= 0.10 m and p90 yaw error <= 5 deg against tape-measured robot poses, >= 30 poses; 0 poses published when the reason is ambiguous, tags_disagree or reproj |
| Status | draft |
| Verified by | TP-V02 |

### SR-019 · parent R6 · module M6 · must {.unnumbered}

> The AprilTag bench localization app shall log every camera connect, disconnect and outage and at least 20 frame records per second with the decision reason, sending to the MCU only validated poses.

| Field | Value |
|---|---|
| Rationale | Lessons 7 and 10 (log raw, replay failures); SR-017 log-only gate. Test-mode estimates are for the page and log only. |
| Verification | Test |
| Acceptance | run.jsonl holds camera_connected / camera_disconnected / camera_missing for each plug event and >= 20 frame records/s while the camera runs; Bridge pose messages with tag count > 0 occur only for frames with reason ok (TP-V02 step 6) |
| Status | draft |
| Verified by | TP-V02 |

### SR-020 · parent R6 · module M6 · must {.unnumbered}

> The AprilTag bench localization app shall keep camera images on the robot by default, writing no image to disk and serving no image over the network unless the STREAM flag is set in code.

| Field | Value |
|---|---|
| Rationale | Privacy of plant staff in view of the camera (threat model T-01). |
| Verification | Inspection |
| Acceptance | STREAM = False in the committed web.py; GET /frame.jpg returns 404; no image files under python/logs after a run |
| Status | draft |
| Verified by | TP-V02 |

### SR-021 · parent R6 · module M6 · should {.unnumbered}

> The mount calibration of the AprilTag bench localization app shall measure camera height and pitch from at least 20 single-tag views within 2 s and apply them only to the running session.

| Field | Value |
|---|---|
| Rationale | CAM_Z/CAM_PITCH guesses broke every pose in the field log of 2026-11-22; values must come from measurement (rule 5). Session-only so a web request cannot change the committed configuration (threat model T-03). |
| Verification | Test |
| Acceptance | TP-V02 step 3: calibrated CAM_Z within 0.02 m and CAM_PITCH within 1 deg of the tape/inclinometer measurement; values revert on app restart |
| Status | draft |
| Verified by | TP-V02 |

### SR-022 · parent R1 · module M3 · must {.unnumbered}

> The dosing system shall spray cleaning solution ahead of the brush at the dose set by TP-S02 (estimate 20 mL/m2, within +/- 25 %) only while the robot moves in cleaning mode with the brush running, and stop within 1 s when either condition ends or the e-stop opens.

| Field | Value |
|---|---|
| Rationale | ADR-0008. TP-S01 showed suction alone does not detach the oil film; a puddle from a pump left running is a slip hazard (F-012). |
| Verification | Test |
| Acceptance | Dose within +/- 25 % of target over 5 runs (solution tank weighed before/after, area from the log); pump off <= 1 s after stop, brush off or e-stop in 10 of 10 trials |
| Status | draft |
| Verified by | TP-S02 |

### SR-023 · parent R5 · module M4 · must {.unnumbered}

> Foam generated in the sealed chamber shall not reach the vacuum port during a full 20 L tank fill with the selected cleaning solution and the reference lubricant.

| Field | Value |
|---|---|
| Rationale | ADR-0008; foam can bypass the float shut-off (SR-008) and wet the vacuum motor (F-010). |
| Verification | Test |
| Acceptance | 0 foam at the port (inspection window) and 0 early float trips in 5 full fills; foam height logged per run |
| Status | draft |
| Verified by | TP-S02 |

### SR-024 · parent R7 · module M3 · must {.unnumbered}

> After one cleaning pass the floor shall show no standing liquid and a measured slip resistance at least equal to the clean dry floor minus 10 %.

| Field | Value |
|---|---|
| Rationale | NOM-001-STPS-2008 7.4 b (liquids on floors must not be a slip hazard); the degreaser leaves a wet film (TP-S01, F-011). |
| Verification | Test |
| Acceptance | Inclined-plane or drag-sled friction coefficient on 5 cleaned strips >= 0.9 x clean dry value; no standing liquid by inspection 1 min after the pass |
| Status | draft |
| Verified by | TP-S02 |

### SR-025 · parent R5 · module M3 · must {.unnumbered}

> The cleaning agent shall be a water-based, low-foam, quick-break, silicone-free degreaser without flammable solvents, delivered with a safety data sheet under NOM-018-STPS-2015.

| Field | Value |
|---|---|
| Rationale | ADR-0008; worker exposure (NOM-010-STPS), foam (SR-023), oil separation in the tank and no silicone residue in machining plants. |
| Verification | Inspection |
| Acceptance | SDS and label on file; SDS shows no flammable classification; supplier states low-foam and quick-break; dilution recorded in the operating sheet |
| Status | draft |
| Verified by | TP-S02 |

