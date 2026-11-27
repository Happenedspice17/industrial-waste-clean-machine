# Project management

## Team

Seven students of the Faculty of Engineering, Universidad Panamericana (Mexico City):

- Franco Zavala Morgan
- María Ruiz Mejía
- Manuel Harari López
- Ian Carlo Olivares Chávez
- Carlos Emiliano Escamilla Garibay
- Luis Roberto Sánchez Salgado
- Juan Manuel Vásquez Paniagua

**Professor and advisor:** Dr. Hiram Eredín Ponce Espinosa, Faculty of Engineering, Universidad Panamericana.

## Team organization for the build

The build is organized in four module teams after a whole-team suction phase. Each team owns the design, build and a
share of the validation of its modules; for the critical characteristics, validation is done by a different team
(Chapter 9).

| Team | Modules | Headcount | Tasks | Deliverable before integration | Budget (MXN) |
|---|---|:-:|---|---|--:|
| A · Chassis and mobility | M1, M2, M3 (brush mechanics) | 2 | Frame, motor mounts, printed hubs, wheels, brush + belt, suction module mount, manual drive tests on oily floor | Rolling chassis with brush, suction module mounted, manual drive tested | 4,578 |
| B · Separation and storage | M4, M5 | 2 | Separation chamber (mesh + magnets, sealed lid), chip basket and compaction chamber, actuator with load-cell limit, tank cradle, drain valve, leak tray, floats; separation test | Sealed separation chamber, compactor with force limit, tank with drain and leak tray | 1,165 |
| C · Power, safety and HMI | M8, M9, M7 hardware | 1 | Power distribution (battery, fuses, e-stop relay, 5 V buck), 4 × BTS7960 wiring, harness, HMI panel; safety tests | Fused power distribution, hardware e-stop, wired drivers, HMI panel | 4,705.50 |
| D · Control, navigation and vision | M6, M7 software | 2 | UNO Q setup, MCU firmware, sequencing and states, LiDAR + IMU map/save/replay, web UI + RFID, vision (stretch) | Firmware, operating states, route save and replay, web UI; vision as stretch | 4,613 |

Suction phase budget (separate): MXN 1,770 (components 1,426 + tooling 344). Total listed with tooling MXN 17,530.50;
with 15 % contingency ≈ MXN 20,160; with the dosing system of ADR-0008 ≈ MXN 21,310 (estimate).

| Suction-phase role | People | Later team |
|---|:-:|---|
| Suction rig build (tank, vacuum, hose, valve, sealing) | 2 | A |
| Nozzle design and 3D printing (v1–v3), squeegee | 2 | A / B |
| Float shut-off and MPX5010DP reading | 1 | C / D |
| Test protocol and measurements | 1 | D |
| Purchasing, tracking orders, documentation | 1 | C |

## Original calendar (October 2026 proposal)

The improved proposal planned a seven-week build from 12 October to a functional-prototype demonstration on
12 December 2026 (*Prototype_Timeline_Dec2026.xlsx*, Gantt with 35 tasks and dependencies).

| Week | Team A | Team B | Team C | Team D | Milestone |
|---|---|---|---|---|---|
| W1–W3 · 12–30 Oct | **Whole team · suction first:** order parts, reference lubricant and chips, suction rig, nozzle v1–v3, float shut-off and MPX5010DP, suction test protocol | | | | 30 Oct · MS1 suction validated; decision A/B |
| W4 · 2–6 Nov | Cut and assemble frame, covers, motor mounts, printed hubs | Separation chamber: mesh + magnets, sealed lid | Power distribution: battery, fuses, e-stop relay, 5 V buck | UNO Q setup; MCU firmware for motors, encoders, sensors | Frame assembled; power board energized |
| W5 · 9–13 Nov | Wheels and caster; brush with 775 motor and belt | Chip basket and compaction chamber; tank cradle, drain, leak tray, floats | Wire 4 × BTS7960, perfboards, harness | Sequencing and states; start LiDAR + IMU mapping | Rolling chassis; firmware drives the motors |
| W6 · 16–20 Nov | Brush and squeegee mount; suction module on chassis | Linear actuator with load-cell limit (≤ 100 kgf) | HMI panel: RFID, button, LCD, tower | Web UI and RFID; route save/replay | Sequencing demo on the bench |
| W7 · 23–27 Nov | Manual drive tests on oily floor | Separation test (M2) | Safety tests: e-stop, fuses, watchdog | Map, save and replay a route; vision (stretch) | 27 Nov · module deliverables and test sheets |
| W8 · 30 Nov–4 Dec | **Whole team · integration**, first full-cycle run | | | | 4 Dec · feature freeze |
| W9 · 7–11 Dec | **Whole team · validation**: M1–M3 tests, fix list, report, video, rehearsal | | | | Final report and video |
| 12 Dec | | | | | MS2 · functional prototype demo |

Decision gates: 30 Oct (suction results fix the collection architecture); 27 Nov (each module passes its own test
before integration); 4 Dec (features not working are frozen out of the demo, vision and full SLAM first).

## Actual progress and replanning

The design and analysis work was completed this semester, a bench software tool runs on the UNO Q and a first
exploratory suction pre-test was run (TP-S01). The physical build did not start: the suction rig, the module builds and the tests were moved to the next semester (*Proyecto
Mecatrónico II*). Honest status: **initial design, not frozen; no physical prototype; one exploratory pre-test.** The
order of work is unchanged (suction first), because it attacks the biggest risk before spending on the rest.

| Planned this semester | Status at 27 Nov 2026 |
|---|---|
| Requirements, selection, conceptual design, design of models, scenarios | Done |
| Priced BOM, timeline, costs | Done |
| Economics and technological impact | Done |
| Standards, DFMEA, SCCAF, WCCA, DFMA, threat model, ADRs, test protocols | Done (beyond the original plan) |
| Public repository with automatic checks | Done (beyond the original plan) |
| AprilTag bench localization app on the UNO Q | Done (simulation + bench; physical accuracy test pending) |
| First physical evidence | Handheld suction pre-test TP-S01 measured on 24 Nov 2026 (exploratory); degreaser adopted (ADR-0008); rig protocol TP-S02 written |
| Suction rig and A/B decision | Moved to next semester (weeks 1–3), now with brush + degreaser + wet trap (TP-S02) |
| Module builds, integration, M1–M3 tests, demo | Moved to next semester |

## Roadmap for next semester

| Phase | Weeks | Goal | Exit criterion |
|---|---|---|---|
| P1 | 1–3 | **Suction rig TP-S02** (brush + degreaser dose + wet trap) → decide A/B and the dose → freeze the design | ADR-0004 accepted with test report; SC-001, SC-008, SC-009 measured; dose and product chosen |
| P2 | 3–7 | Build modules in 4 teams: chassis + mobility · separation + storage · power + safety + HMI · control + navigation + vision | Each module passes its own test sheet |
| P3 | 7–10 | Integration; map, save and replay a route | Full cycle on the bench and on the floor |
| P4 | 10–13 | Validate M1–M3 and safety on an oily floor | Test reports for SR-001–SR-014 |
| P5 | 13–16 | Plant pilot, customer interviews, final report | Pilot log; interview notes; business model updated |

Stretch goals: vision task with the camera · full SLAM · LiFePO4 battery · coolant emulsions after compatibility tests.

## Open decisions (to close with evidence and record as ADRs)

| # | Decision | Closes with |
|:-:|---|---|
| 1 | Collection architecture A vs B (ADR-0004) | Suction rig: chip lift rate, liquid per pass, clogging |
| 2 | Reference lubricant (type, viscosity) and chip samples | Plant visit / supplier |
| 2b | Cleaning-agent product, dilution and dose (ADR-0008); optional spot dosing only where residue is detected | TP-S02 parts C–F |
| 3 | Mesh aperture, magnet layout, compactor stroke and force path, compaction ratio | Separation tests |
| 4 | IMU: BNO055 vs MPU-6050 (ADR-0005) | I²C test on the STM32U585 |
| 5 | LiDAR supply (out of stock at check), oil-hose price, printed wheel hubs | Purchasing; measured parts |
| 6 | Sensor role hierarchy — confirm before coding | Bench tests |
| 7 | Vision: camera placement (DFMA) and USB hub power (WCCA) | DFMA and WCCA rows |
| 8 | EVR-01–EVR-03 into `requirements.yaml` | Team approval |
| 9 | Who may authorize operation (RFID credentials); start, fault, reset and maintenance sequence | Operating procedure |

## Project risks (management view)

| Risk | Effect | Response |
|---|---|---|
| Vacuum cannot lift chips | Collection concept changes | Option B ready; criteria fixed before test |
| LiDAR out of stock | Navigation delayed | Reserve early; Amazon/Mercado Libre alternatives; AprilTag bench tool meanwhile |
| Integration takes longer than planned | Validation squeezed | Module test sheets before integration; feature freeze; stretch goals first to drop |
| Budget overrun on unpriced items | Contingency used | 15 % contingency; buy in phases by team |
| Knowledge concentrated in few people | Bus factor | Everything in the repository; engineering log; reviews by another team |
