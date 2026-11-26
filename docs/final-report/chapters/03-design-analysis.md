# Design analysis

The design analysis translates the need into weighted requirements, evaluates the candidate components against them
with two independent methods (a quality matrix and a pairwise comparison), adds ethical value requirements, positions
the project with a SWOT analysis, and organizes the objectives in a goal tree. The methods follow standard
product-development practice [17], [18].

## Stakeholders

| Stakeholder | Interest | How the design responds |
|---|---|---|
| Shop-floor operators and cleaners | Safe floor, no contact with fluids, job security | Robot works in the shift-change window; human-in-the-loop emptying; Spanish, color-based HMI; retraining as operators |
| Maintenance technicians | Easy service, clear faults | Nine removable modules on T-slot rails; fault messages and logs; lockable e-stop |
| EHS (environment, health and safety) manager | Fewer incidents, compliance (NOM-001, NOM-052) | Logs of area cleaned and waste recovered; two labeled streams for authorized handlers |
| Plant / production manager | Cost, no downtime | Cleans between shifts; 6.6-month payback (base case, estimate) |
| Bystanders (other workers, forklift drivers) | Not be hurt by the robot | Speed limit, LiDAR + bumpers, cleared-zone operation, hardware e-stop |
| Environment and community | No illegal dumping, recycling | Segregated streams, chips to scrap recycling, battery returned for recycling |
| Union representatives | Employment terms | Robot reassigns rather than eliminates work (Chapter 14) |

## Stakeholder requirements

The team defined ten requirements. Importance is an independent relevance score from 1 to 10, not a ranking, so
repeated values are intentional. Importance does not override mandatory structural and safety functions (chassis,
controller and emergency stop). The values match the live weighted matrix on 24 September 2026.

| ID | Requirement (original Spanish name) | Imp. | Verification | Objective | Covered by (components) |
|---|---|:-:|---|---|---|
| R1 | Lubricant suction / collection (*Absorción o succión de lubricantes*) | 10 | Collected volume, collection time and residual liquid with the reference lubricant | OE1 | C12, C11, C10, C04, C08, C13 |
| R2 | Solid-chip separation (*Separación de viruta*) | 10 | Captured solids and residual particle content by size and material | OE2 | C06, C27, C28 |
| R3 | Compaction system (*Sistema de compactación*) | 6 | Volume reduction, drained liquid, actuator force, jamming | OE2 | C25, C29, C26 |
| R4 | Compact size (*Tamaño compacto*) | 2 | External dimensions, service clearances and loaded mass | OE4 | C14 |
| R5 | Safety system (*Sistema de seguridad*) | 6 | E-stop, overflow inhibition, compactor access and fault response | OE3, OE5 | C22, C32, C35, C23, C24, C19, C31 |
| R6 | Vision system (*Sistema de visión*) | 6 | Defined vision task under controlled lighting | OE4 | C16, C34 |
| R7 | Safe mobility (*Movilidad segura*) | 10 | Traction, stopping distance and stability on the representative floor | OE4 | C01, C17, C33, C03, C35 |
| R8 | Route storage and mapping (*Guardado y mapeo de rutas*) | 6 | Save, reload and execute a route; mapping and localization | OE4 | C03, C17, C33, C15, C20 |
| R9 | Separate solid and liquid containers (*Contenedor de residuos sólidos y líquidos*) | 10 | Separation, useful capacity, leak containment and controlled emptying | OE3 | C02, C28, C30, C31, C23 |
| R10 | Operating authorization (*Autorización de funcionamiento*) | 4 | Authorized/unauthorized start and deliberate restart after a stop | OE5 | C36, C18, C20 |

## System requirements

Each stakeholder requirement was decomposed into verifiable system requirements (SR) with exactly one "shall", a
verification method and an acceptance criterion fixed before testing. They live in
`requirements/requirements.yaml`, and `tools/check_traceability.py` fails the CI if a requirement loses its parent,
its verification or its test link. The full text is in Appendix C.

| ID | Parent | Module | Priority | Summary | Acceptance (fixed before testing) | Standard |
|---|---|---|---|---|---|---|
| SR-001 | R1 | M3 | must | Recover ≥ 85 % of spilled liquid in one pass on 1 m² | ≥ 85 %, mean of 5 runs | — |
| SR-002 | R2 | M4 | must | Solid stream ≥ 90 % free of drainable oil after compaction | ≥ 90 % | — |
| SR-003 | R9 | M5 | must | Liquid stream ≤ 5 % solids > 1 mm | ≤ 5 % (filtered and weighed) | — |
| SR-004 | R7 | M2 | must | Speed ≤ 0.38 m/s any mode, ≤ 0.15 m/s cleaning | Encoder log max | ISO 3691-4 4.3 |
| SR-005 | R7 | M2 | must | Stop within 0.10 m from 0.38 m/s on oiled floor | Max of 10 runs ≤ 0.10 m | ISO 3691-4 4.2 |
| SR-006 | R5 | M8 | must | E-stop removes actuator power in hardware within 100 ms | Rails < 1 V in 100 ms, firmware halted | ISO 3691-4 4.8.1; ISO 13850 |
| SR-007 | R5 | M7 | must | MCU stops all motion if no heartbeat for > T_stale | Stop ≤ T_stale + 50 ms | — |
| SR-008 | R5 | M5 | must | Float shut-off stops vacuum before liquid reaches the port (hardware) | No liquid at port in 5 overfill tests | — |
| SR-009 | R3 | M4 | must | Compactor force ≤ 100 kgf ± 5 %; only with lid closed | Peak ≤ 1030 N; no motion with lid open | NOM-004-STPS |
| SR-010 | R10 | M9 | must | Start only after valid RFID + start button | 0 starts in 20 unauthorized attempts | — |
| SR-011 | R8 | M6 | should | Save map + route; repeat at ≥ 100 m²/h, 0 incidents | 3 runs on stored route | — |
| SR-012 | R4 | M1 | should | Envelope ≤ 700 × 500 × 520 mm | Measured envelope | — |
| SR-013 | SR-004 | M2 | must | Stop when encoder speed > 0.40 m/s (overspeed) | Trip at 0.40 ± 0.02 m/s in 5 tests | ISO 3691-4 4.3.1 |
| SR-014 | R5 | M9 | must | After fault/e-stop, need new RFID + button to move | 0 restarts without card + button in 10 tests | ISO 3691-4 4.1.14 |
| SR-015 | R6 | M6 | should | Vision flags residue ≥ 50 × 50 mm, ≥ 90 % agreement with operator | ≥ 200 labeled frames; 0 motion commands from vision | — |
| SR-016 | R9 | M6 | should | Vision reads tank/basket level low/half/full, ≥ 95 % agreement with floats | ≥ 100 checks per container | — |
| SR-017 | R6 | M6 | must | Vision outputs log-only until TP-V01 passes and the report is committed | Flags default off; each enabled flag cites a report | — |
| SR-018 | R8 | M6 | should | AprilTag bench app: p90 error ≤ 0.10 m and 5° at 0.8–3.5 m; no pose if ambiguous | TP-V02, ≥ 30 taped poses | — |
| SR-019 | R6 | M6 | must | AprilTag app logs camera events and ≥ 20 frame records/s; only validated poses to MCU | TP-V02 step 6 | — |
| SR-020 | R6 | M6 | must | AprilTag app keeps images on the robot (no disk, no network) unless STREAM is set in code | `/frame.jpg` → 404; no image files | Privacy (LFPDPPP) |
| SR-021 | R6 | M6 | should | Mount calibration measures camera height and pitch from ≥ 20 views in 2 s, session-only | Within 0.02 m and 1° | — |

All 21 SRs are in status **draft**: none can be "verified" until its physical test passes. SR-018–SR-021 already
point to test protocol TP-V02.

## Ethical value requirements (IEEE 7000-2021)

Following the IEEE 7000-2021 value-based engineering process [58] (course template *Ethical Design Evidence*), the
team identified the stakeholders above, elicited the values at stake and translated them into ethical value
requirements (EVRs) that can be verified like any other requirement.

| ID | Value | Ethical value requirement | Measurable criterion | Traces to |
|---|---|---|---|---|
| EVR-01 | **Worker safety** | The robot shall never put a person at risk to gain cleaning speed | Speed ≤ 0.38 m/s (0.15 m/s cleaning); stop ≤ 7.4 cm on oil (calculation) / ≤ 0.10 m (test); e-stop cuts every actuator in hardware; no automatic restart | SR-004, SR-005, SR-006, SR-013, SR-014 |
| EVR-02 | **Environmental responsibility** | The two waste streams shall never mix and shall never overflow | Liquid stream ≤ 5 % solids; float cuts suction before overflow; streams delivered only to authorized handlers | SR-002, SR-003, SR-008 |
| EVR-03 | **Privacy and accountability** | Camera data shall stay on board and no image of a person shall be stored; each run shall be tied to an authorized operator | No images to disk or network by default; RFID card per cycle; log keeps operator ID and time with a privacy notice and limited retention | SR-010, SR-020 |

**Value conflict and priority.** Coverage speed (productivity, M3) conflicts with worker safety. The rule adopted:
**when coverage speed and safety conflict, safety wins.** Concretely, the speed limit and the stop conditions are
fixed first and M3 is evaluated within them; if M3 fails, the response is a better route or a wider tool, never a
faster robot.

**Status.** The EVRs are a team draft (deduced from the existing system requirements and protection terms); they
are not yet in `requirements/requirements.yaml` and will be added once the team approves them.

## Quality matrix

The quality matrix relates each requirement to each candidate component with the house-of-quality scale 0 (none),
1 (weak), 3 (medium) and 9 (strong) [19]. The weighted score of a component is

$$S(j) = \sum_{i} \text{importance}_i \times \text{relationship}_{ij}$$

![Quality matrix: requirements R1–R10 (rows, with importance) against components C01–C22 (columns). Bottom row: weighted score S(j) and rank.](img/quality_matrix.png)

The Arduino UNO Q (C15, S = 204), LiDAR (C03, 168), encoders (C17, 144) and storage tank (C02, 142) score highest
because they serve several requirements at once. The water/steam outlets (C07, 20) and extra-products container (C09,
10) score lowest and were removed, since they would add a third waste stream and dilute the recovered lubricant.

The same scale applied to the team's wider 47-component inventory places 38 components inside a count-based 80 % cut.
The cut is by count, not by score: the start button (position 39, 90 points) ties with the RFID reader (position 38,
90 points) but falls outside. Because that matrix underrates mandatory items (the chassis ranks 46th and the
emergency stop 41st), the final proposal keeps them regardless of score.

## Pairwise comparison matrix

Each pair of the 22 components was compared once (231 pairs, upper triangle): 0 = equal importance, Cxx:1 = mild
preference and Cxx:2 = strong preference for component Cxx; only the winner receives points. This is a simplified
form of the pairwise logic of the analytic hierarchy process [20].

The team answered 143 pairs. The remaining 88 were completed with a rule derived from S(j), and 47 team answers that
contradicted S(j) by two or more levels were corrected; most were in rows C03 (LiDAR) and C15 (UNO Q), where the
column component had been entered as the winner. Mandatory components (C14, C15, C22) win :2 against non-mandatory
ones.

![Corrected pairwise comparison matrix. Amber: row component wins; blue: column component wins; darker = strong preference (:2). Right: points and rank.](img/pairwise_matrix.png)

The Spearman rank correlation between the quality matrix and the pairwise comparison rose from **0.26** with the
original answers to **0.83** after correction, so both methods now point to the same priorities. The remaining
differences come from the mandatory-component rule and from a one-level tolerance that respects the team's judgment.

| Code | Component | Quality matrix | Pairwise (original) | Pairwise (corrected) | Combined |
|---|---|:-:|:-:|:-:|:-:|
| C01 | Oil-compatible wheel/track | 10 | 4 | 13 | 13 |
| C02 | Storage tank | 4 | 5 | 6 | 6 |
| C03 | LiDAR | 2 | 11 | 4 | 3 |
| C04 | Cleaning brushes | 15 | 5 | 14 | 15 |
| C05 | Vacuum cleaner | 7 | 19 | 7 | 9 |
| C06 | Coarse-solids filter | 5 | 14 | 9 | 8 |
| C07 | Pressurized water / steam outlets | 21 | 21 | 20 | 21 |
| C08 | Squeegee | 18 | 17 | 19 | 19 |
| C09 | Extra-products container (soap, acid) | 22 | 19 | 20 | 22 |
| C10 | Lubricant-resistant hose | 11 | 21 | 11 | 11 |
| C11 | Collection nozzle | 8 | 17 | 9 | 10 |
| C12 | Vacuum unit for oil and chips | 5 | 14 | 7 | 7 |
| C13 | Vacuum sensor | 16 | 14 | 16 | 16 |
| C14 | Chassis (mandatory) | 12 | 2 | 3 | 4 |
| C15 | Arduino UNO Q (mandatory) | 1 | 2 | 2 | 1 |
| C16 | Camera | 14 | 9 | 15 | 14 |
| C17 | Encoders | 3 | 11 | 5 | 5 |
| C18 | Start button | 17 | 10 | 18 | 18 |
| C19 | Status indicators | 20 | 11 | 20 | 20 |
| C20 | Operation / programming control | 18 | 8 | 17 | 17 |
| C21 | PCB | 9 | 5 | 12 | 12 |
| C22 | Emergency-stop button (mandatory) | 13 | 1 | 1 | 2 |

Rank of each component by method (1 = most important). Combined = 50 % quality matrix + 50 % corrected pairwise,
both normalized.

**Agreement between evaluations.** Both methods place the controller, LiDAR, encoders, tank, vacuum unit and filter
at the top, and the water/steam outlets, extra-products container, status indicators and start button at the bottom.
The first two were discarded. The indicators and start button are kept because they serve safety (R5) and operating
authorization (R10), which are functions rather than performance drivers.

## Component inventory (33 items)

Codes C01–C22 keep their meaning from the 22-item list (C05, C07 and C09 are retired). C23–C36 were restored from the
47-item weighted matrix. "Pos." is the position in that matrix.

| ID | Component | Pos. | Main reason |
|---|---|:-:|---|
| C01 | Oil-compatible wheel/track | 28 | Safe mobility (R7) |
| C02 | Storage tank (pressure-resistant structure) | 6 | Liquid container (R9) |
| C03 | LiDAR | 11 | Mapping and obstacles (R7, R8) |
| C04 | Cleaning brushes | 12 | Direct chips to the nozzle |
| C06 | Coarse-solids filter | 15 | Solids separation (R2) |
| C08 | Squeegee | 22 | Pushes oil film to the nozzle |
| C10 | Lubricant-resistant hose | 18 | Suction (R1) |
| C11 | Collection nozzle | 20 | Suction (R1) |
| C12 | Vacuum unit for oil and chips (includes vacuum cleaner) | 2 | Main suction function (R1) |
| C13 | Vacuum sensor | 9 | Detects clogging or suction loss |
| C14 | Chassis (includes support and maintenance covers) | 46 | Mandatory, structural |
| C15 | Microcontroller — Arduino UNO Q | 29 | Confirmed controller |
| C16 | Camera | 25 | Vision (R6) |
| C17 | Encoders | 35 | Odometry |
| C18 | Start button | 39 | Authorization and deliberate restart (R10) |
| C19 | Status indicators | 43 | Visible status and faults (R5) |
| C20 | Control to operate or program the robot | 5 | Commissioning, manual recovery, routes (R8) |
| C21 | PCB | 24 | Electrical integration |
| C22 | Emergency-stop button | 41 | Mandatory, safety |
| C23 | Level cut-off (material quantity) | 1 | Overflow prevention (R5, R9) |
| C24 | Fuses, actuators and additional electronic components | 3 | Electrical protection |
| C25 | Compaction chamber with drainage (includes pressure plate) | 8 | Compaction (R3) |
| C26 | Pressure/force sensor | 13 | Compactor force limit and measurement (R3, R5) |
| C27 | Magnet | 17 | Ferrous fraction (R2) |
| C28 | Metal basket | 19 | Separate solids container (R9) |
| C29 | Linear actuator (piston) | 21 | Drives the compactor (R3) |
| C30 | Drain valve | 23 | Controlled emptying (R9) |
| C31 | Leak tray | 27 | Internal leak containment |
| C32 | Relay circuit | 31 | Hardware e-stop cut independent of software |
| C33 | Inertial measurement unit (IMU) | 32 | Odometry under wheel slip on oil |
| C34 | LED lighting | 34 | Controlled lighting for vision |
| C35 | Bumper | 37 | Contact backup for LiDAR (R5) |
| C36 | RFID reader | 38 | Operating authorization (R10) |

**Integrated into another component (6):** vacuum cleaner → C12 · support → C14 · maintenance covers → C14 ·
emergency stop for safety or machine problems → C22 · pressure-resistant structure → C02 · pressure plate → C25.

**Discarded (8):** line sensor · industrial vibrator · Wi-Fi module · swerve · logging modules · motors to raise or
lower the rollers · extra-products container (former C09) · pressurized water / steam outlets (former C07).

Summary: 33 keep · 6 integrate · 8 discard = 47.

## SWOT analysis

| Strengths (internal) | Weaknesses (internal) |
|---|---|
| Collection, separation and separate storage on one platform | An 80 W automotive wet/dry vacuum may not lift dense steel chips |
| No water, steam or chemicals: the recovered lubricant is not diluted | 12 V 24 Ah lead-acid battery: ≈ 144 Wh usable, roughly one hour of operation |
| Nine-module design on a T-slot frame; each team can build and replace a module on its own | 20 L tank sets a ceiling per cycle |
| Arduino UNO Q combines real-time control and Linux navigation on one board | Magnets do not capture non-ferrous chips (aluminum, brass) |
| Hardware e-stop and layered protections (fuses, current limits, float shut-off, force limit, watchdog) | Several numerical targets (particle cut-off, compaction ratio) still to fix |
| Listed cost ≈ MXN 17,500 including tooling; most parts available in Mexico | SLAM performance on the UNO Q not yet benchmarked |

| Opportunities (external) | Threats (external) |
|---|---|
| Segregated oil and chips have higher recycling value and simpler disposal [11] | Real plant conditions: thick grease, emulsions, long chips, people and forklifts crossing the area |
| Shift changes offer a window when no one is on the floor | Industrial deployment would require compliance with mobile-robot and hazardous-waste regulations beyond prototype scope |
| Upgrade paths: LiFePO4 battery, stronger vacuum, ROS 2 navigation stack | Supply delays (the LiDAR was out of stock at the price check) |
| Extension to coolant emulsions after compatibility tests | Existing industrial floor scrubbers and manual cleaning are cheaper, known alternatives |
| Operating data (area cleaned, volumes recovered) useful for plant maintenance planning | Limited build time within an academic semester |

## Goal tree

The goal tree is read from the bottom up: the means (components and actions) achieve the specific objectives, the
specific objectives achieve the general objective, and the general objective contributes to the ends, following the
logical-framework approach [21].

![Goal tree. Codes C refer to the 33-component proposal; R1–R10 are the project requirements.](img/goal_tree.png)
