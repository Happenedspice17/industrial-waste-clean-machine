# Project Brief — Autonomous Robot for Industrial Waste Cleaning and Separation

> Working reference for the team. Draft 6 adds the **conceptual design** results (black box, UI component selection, functional and component white boxes, morphological matrix, priced component list) and the **specific objectives**. The 33-component inventory from Draft 5 remains the working proposal, **pending team confirmation**. The Arduino UNO Q decision is retained.

- **Course:** Proyecto Mecatrónico I — Universidad Panamericana
- **Professor:** Dr. Hiram Eredín Ponce Espinosa
- **Team:** Franco Zavala Morgan · María Ruiz Mejía · Manuel Harari López · Ian Carlo Olivares Chávez · Carlos Emiliano Escamilla Garibay · Luis Roberto Sánchez Salgado · Juan Manuel Vásquez Paniagua
- **Version:** Draft 6 — 9 October 2026
- **Confirmed control platform:** Arduino UNO Q
- **Status:** Conceptual design complete; prototype component list priced at **$15,849.50 MXN** (listed components only, §10). Performance targets remain open.
- **Language:** English. Requirement and component names match the English pairwise-comparison workbook (*Pairwise_Comparison_Corrected.xlsx*).

## 1. Core idea

An autonomous mobile robot that collects lubricants mixed with metal chips and other solid residues from a manufacturing floor, separates the ferrous fraction and coarse solids from the liquid onboard, compacts and drains the solids, and stores liquid and solid waste streams in separate containers. Its intended operating window is a controlled area during shift changes.

## 2. General objective

Develop and validate a compact mobile prototype that collects lubricants and solid residues, separates them by mechanical filtration and magnetic capture, compacts and drains the solid fraction, and stores the two waste streams separately. Integrate safe mobility, a defined vision function, route storage and mapping, and authorized operation using the Arduino UNO Q as the control platform. Demonstrate the functions through measured prototype tests before making claims about floor safety, liquid reuse, unattended deployment or disposal compliance.

The baseline liquid is a lubricant to be specified by the team. Coolants/emulsions may be included after compatibility testing; grease handling is not assumed to be equivalent to pumping liquid oil.

### Specific objectives

| ID | Specific objective | Indicator | Requirements |
|---|---|---|---|
| OE1 | Design and integrate a suction collection system (brushes, squeegee, nozzle, lubricant-resistant hose, vacuum unit with sensor) that picks up lubricant and chips from the floor. | Collected volume, collection time and residual liquid with the reference lubricant. | R1 |
| OE2 | Design a module that retains coarse solids with a filter, captures the ferrous fraction with a magnet into a basket, and compacts and drains the solids with a force-controlled linear actuator. | Captured solids by size and material, volume reduction, drained liquid, actuator force, jamming. | R2, R3 |
| OE3 | Implement separate liquid and solid storage with drain-valve emptying, leak tray and level cut-off. | Useful capacity, no mixing between streams, leaks, level cut-off response. | R9, R5 |
| OE4 | Build an oil-compatible differential-drive platform that localizes with encoders, IMU and LiDAR, saves and repeats mapped routes, and runs the defined vision task with camera and LED lighting. | Traction, stopping distance, loaded stability, route-tracking error, vision-task performance, dimensions. | R4, R6, R7, R8 |
| OE5 | Develop the Arduino UNO Q control architecture (MCU for sensors and actuators; Linux for vision and routes) with RFID and start-button authorization, status indicators and a relay e-stop independent of software. | Authorized and unauthorized start, deliberate restart after a stop, stop time, fault response. | R5, R10 |
| OE6 | Validate the complete prototype in a controlled test area with a protocol that fixes numerical acceptance criteria before testing. | All indicators recorded by lubricant, solids, floor, load and test conditions. | All |

Numerical targets for these indicators are still TBD (§6). Objectives tree: separate team PDF (not archived here).

## 3. Working hypothesis

If an oil-compatible mobile platform integrates brushes and a squeegee that direct residues to a vacuum nozzle, a vacuum unit, a coarse-solids filter, a magnet with a metal basket for the ferrous fraction and a compaction chamber with drainage, then it should be possible to recover a lubricant/solid mixture, retain and compact the solids, and store them separately from the collected liquid in a controlled test area. Arduino UNO Q coordinates sensing, actuator commands, operator controls and route execution; the emergency stop acts through an independent relay circuit. Separation performance, compaction ratio, storage arrangement and navigation capability require validation.

Differential traction with oil-compatible wheels/tracks is the proposed drive; swerve is not pursued. No water, steam or chemical cleaning medium is used, so the recovered lubricant is not diluted or contaminated by a third stream. Filtering does not establish that the lubricant is suitable for reuse.

## 4. Problem and intended contribution

Manufacturing-floor contamination can combine lubricants, metal chips and other residues, creating a collection and handling problem. The project addresses the integration of mobile collection, onboard separation, solids compaction and controlled waste storage into one academic prototype.

The contribution is this integration under the team's operating constraints. The Draft 1 claim that no existing system combines floor cleaning and waste separation is not retained as an established fact: such an absolute novelty claim requires a documented market and patent review. Recycling suitability and disposal procedures depend on the actual collected waste and must be evaluated separately.

## 5. Scope and architecture boundaries

**Proposed component scope (33 items, §9)**
- Mobility: oil-compatible wheels/tracks, chassis, encoders, IMU, LiDAR and bumper.
- Collection: brushes, squeegee, collection nozzle, lubricant-resistant hose, vacuum unit (includes the former "Vacuum cleaner" item) and vacuum sensor.
- Separation and storage: coarse-solids filter, magnet, metal basket, compaction chamber with drainage (includes the pressure plate), linear actuator, pressure/force sensor, storage tank (vacuum-resistant structure), drain valve, leak tray and level cut-off.
- Control and interface: Arduino UNO Q, PCB, fuses and auxiliary electronics, relay circuit, camera with LED lighting, operation/programming control, start button, RFID reader, status indicators and emergency-stop button.

**Removed from the active proposal**
- Pressurized water/heating/steam outlets and the auxiliary-product container (soap, acid): they would add a third waste stream and contaminate the recovered lubricant.
- Line sensor (redundant with LiDAR; oil fouls floor markings), swerve drive, separate Wi‑Fi and logging modules (provided by UNO Q), industrial vibrator and brush-lifting motors (optional; reconsider only if tests show filter clogging or brush-height problems).

**Remaining implementation items**
- Conceptual choices made in §10: differential drive with two 124 mm wheels and a rear caster, 12 V 24 Ah sealed lead-acid battery for the prototype (LiFePO4 as upgrade), 5 V buck regulation.
- Mounting, wiring, connectors, filter mesh size, magnet layout and compactor stroke/force remain to be sized.

**Operating boundaries**
- Supervised commissioning and autonomous-cycle demonstrations in a controlled test area, with shift changes as the intended operating window.
- Remote control supports commissioning, manual recovery and programming.
- Alloy sorting, chemical decomposition of lubricant, mixed operation with people, fleet/cloud analytics and manipulator tasks are not project deliverables.
- Do not claim certified industrial operation, guaranteed slip-free floors or automatic lubricant reusability.

## 6. Project requirements

Importance is an independent relevance score from 1 to 10, not a ranking; repeated values are intentional. The values match the live weighted matrix on 24 September 2026. They do not override mandatory structural or safety functions.

| ID | Requirement | Importance / 10 | Covered by (proposal) | Verification to develop |
|---|---|---:|---|---|
| R1 | Lubricant suction / collection | 10 | C12, C11, C10, C04, C08, C13 | Measure collected volume, collection time and residual liquid for the agreed lubricant. |
| R2 | Solid-chip separation | 10 | C06, C27, C28 | Measure captured solids and residual particle content by size and material. |
| R3 | Compaction system | 6 | C25, C29, C26 | Measure volume reduction, drained liquid and actuator force; evaluate jamming. |
| R4 | Compact size | 2 | C14 (design envelope) | Measure external dimensions, service clearances and loaded mass. |
| R5 | Safety system | 6 | C22, C32, C35, C23, C24, C19, C31 | Test emergency stop, overflow inhibition, compactor access and fault response. |
| R6 | Vision system | 6 | C16, C34 | Demonstrate the defined vision task with controlled lighting; task and accuracy target remain to be specified. |
| R7 | Safe mobility | 10 | C01, C17, C33, C03, C35 | Measure traction, stopping distance and stability on the representative floor. |
| R8 | Route storage and mapping | 6 | C03, C17, C33, C15, C20 | Save, reload and execute a route; demonstrate mapping and localization. |
| R9 | Separate solid and liquid waste containers | 10 | C02, C28, C30, C31, C23 | Verify separation, useful capacity, leak containment and controlled emptying. |
| R10 | Operating authorization | 4 | C36, C18, C20 | Test authorized/unauthorized start and deliberate restart after a stop. |

All 10 requirements have assigned hardware in the proposal. Numerical acceptance thresholds are **TBD**: capacity, collection rate, particle cutoff, compaction ratio, dimensions, autonomy, speed, stopping distance and navigation/vision accuracy are not yet fixed.

## 7. Subsystems and process flow

1. **Mechanical platform and mobility:** oil-compatible wheels/tracks (C01), chassis with supports and maintenance covers (C14), encoders (C17), IMU (C33), LiDAR (C03) and bumper (C35). Differential traction proposed; the IMU compensates wheel slip on oily floors.
2. **Collection:** brushes (C04) and squeegee (C08) direct residues → collection nozzle (C11) → lubricant-resistant hose (C10) → vacuum unit (C12). Vacuum sensor C13 monitors suction.
3. **Separation, compaction and storage:** coarse-solids filter (C06) → magnet (C27) captures the ferrous fraction into the metal basket (C28) → compaction chamber with drainage and pressure plate (C25), driven by the linear actuator (C29) with force sensing (C26). Liquid goes to the storage tank (C02), emptied through the drain valve (C30); leak tray (C31) and level cut-off (C23) protect against spills and overflow.
4. **Perception and control:** Arduino UNO Q (C15), camera (C16) with LED lighting (C34), PCB (C21), fuses and auxiliary electronics (C24) and operation/programming control (C20).
5. **Operator interface and safety:** RFID reader (C36) and start button (C18) for authorization, status indicators (C19), emergency-stop button (C22) acting through the relay circuit (C32).

For the sketch, use the C-codes in §9.

## 8. Confirmed control platform: Arduino UNO Q

**Decision:** C15 (“Microcontroller”) is specified as **Arduino UNO Q**.

Arduino documents two processing domains on UNO Q: a Qualcomm Dragonwing QRB2210 MPU running Debian Linux and an STM32U585 MCU running Arduino sketches over Zephyr. It also documents an inter-processor Arduino Bridge/RPC mechanism and onboard Wi-Fi/Bluetooth. These are board capabilities, not proof that the project's full software workload will meet its timing needs. [Official Arduino UNO Q documentation](https://docs.arduino.cc/hardware/uno-q/). The onboard Wi‑Fi and Linux storage are the reason the separate Wi‑Fi and logging modules were removed from the proposal.

**Proposed task allocation**
- MCU: periodic sensor acquisition (vacuum, level, force, encoders, IMU, bumper), actuator commands through external drivers, compactor sequencing and low-level machine sequencing.
- Linux MPU: vision processing, map/route management, higher-level planning, logs and operator interface.
- Inter-processor link: exchange commands, status and fault information; define a safe response to stale commands, loss of communication and restart.
- Emergency stop and hazardous-motion inhibition: implemented through the relay circuit (C32), independent of application availability; UNO Q is not specified as a safety PLC.

**Integration items still to resolve**
- Board memory/storage variant, mounting and enclosure, power budget and cooling.
- Sensor interfaces, GPIO voltage/current compatibility and any level conversion or isolation.
- Drive, vacuum and compactor interface ratings, supply rails, protection and electromagnetic-noise management.
- Camera compatibility, LiDAR and RFID drivers, software environment and measured runtime performance.

## 9. Proposed component inventory — 33 items

Codes C01–C22 keep their meaning from the previous 22-item list (C05, C07 and C09 are retired). C23–C36 are components restored from the 47-item weighted matrix. "Pos." is the position in that weighted matrix.

| ID | Component | Pos. | Main reason |
|---|---|---:|---|
| C01 | Oil-compatible wheel/track | 28 | Safe mobility (R7) |
| C02 | Storage tank (pressure-resistant structure) | 6 | Liquid container (R9) |
| C03 | LIDAR | 11 | Mapping and obstacles (R7, R8) |
| C04 | Cleaning brushes | 12 | Direct chips to the nozzle |
| C06 | Coarse-solids filter | 15 | Solids separation (R2) |
| C08 | Squeegee | 22 | Pushes oil film to the nozzle |
| C10 | Lubricant-resistant hose | 18 | Suction (R1) |
| C11 | Collection nozzle | 20 | Suction (R1) |
| C12 | Vacuum unit for oil and chips (includes vacuum cleaner) | 2 | Main suction function (R1) |
| C13 | Vacuum sensor | 9 | Detects clogging or suction loss |
| C14 | Chassis (includes support and maintenance covers) | 46 | Mandatory, structural |
| C15 | Microcontroller — **Arduino UNO Q** | 29 | Confirmed controller |
| C16 | Camera | 25 | Vision (R6) |
| C17 | Encoders | 35 | Odometry |
| C18 | Start button | 39 | Authorization and deliberate restart (R10) |
| C19 | Status indicators | 43 | Visible status and faults (R5) |
| C20 | Control to operate or program the robot | 5 | Commissioning, manual recovery, routes (R8) |
| C21 | PCB | 24 | Electrical integration |
| C22 | Emergency-stop button | 41 | Mandatory, safety (duplicate entry merged) |
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

**Integrated into another component (6):** Vacuum cleaner → C12 · Support → C14 · Maintenance covers → C14 · Emergency stop for safety or machine problems → C22 · Pressure-resistant structure → C02 · Pressure plate → C25.

**Discarded (8):** Line sensor · Industrial vibrator · Wi-Fi module · Swerve · Logging modules · Motors to raise or lower the rollers · Extra-products container (former C09) · Pressurized water / steam outlets (former C07).

Summary: 33 keep · 6 integrate · 8 discard = 47.

## 10. Conceptual design (October 2026)

Deck: *Conceptual_Design_Waste_Robot.pptx* (13 slides, English). Prices checked 8 October 2026.

### A. Black box

| UI (input) | Inputs | Outputs | UI (output) |
|---|---|---|---|
| Operator authorization · start/stop command · emergency stop · route programming and manual control · waste emptying and maintenance access | Operator · floor with lubricant and chips · programmed route/area map · obstacle detection · floor surface condition · energy · on/off | Movement go/stop · clean floor area · separated lubricant · separated, compacted chips · noise · status signal | Status indicator (operating/fault/finished) · audible alarm · tank and bin level · battery level · cycle progress |

### B. User-interface components

| UI function | Selected component | Code |
|---|---|---|
| Operator authorization | RC522 RFID reader + 13.56 MHz cards | C36 |
| Start / stop | 22 mm illuminated push button | C18 |
| Emergency stop | Mushroom e-stop + 40 A automotive relay | C22, C32 |
| Route programming and manual control | Web interface over UNO Q Wi-Fi (phone/laptop) | C20 |
| Waste emptying and maintenance | 1/2" ball drain valve + removable chip basket | C30, C28 |
| Status, alarm | 12 V LED signal tower with built-in alarm | C19 |
| Tank/bin level, battery, cycle progress | 20×4 I2C LCD (+ web interface) | C19 |

### C. White boxes

- **Functional:** six modules — Operation (authorize, verify safety, start/stop), Navigation (load route, localize, detect obstacles, drive), Collection (agitate, suck), Separation (filter, capture ferrous, compact and drain), Storage (store liquid, monitor levels), Supervision (manage energy, report status).
- **Components:** based on the team's *robot_components_level_CORRECTED* diagram, updated with the selected parts; adds the e-stop relay circuit that the team diagram did not show.

### D. Morphological matrix — selected concept

| Function | Selected | Alternatives considered |
|---|---|---|
| Traction | Differential drive, rubber wheels | Rubber tracks, mecanum, swerve |
| Drive motors | DC gearmotor + Hall encoder | Stepper NEMA 23, BLDC hub |
| Motor driver | BTS7960 43 A H-bridge | L298N, Cytron MDD10A |
| Floor agitation | Rotary nylon brush (775 motor) | Side discs, squeegee only, microfiber roller |
| Waste suction | 12 V wet/dry vacuum unit | Diaphragm, peristaltic, centrifugal pump |
| Coarse-solids filtering | Stainless mesh basket | Cyclone, settling tank |
| Ferrous separation | Neodymium bar magnets | Electromagnet, magnetic drum |
| Solids compaction | 12 V electric linear actuator | Lead screw + DC motor, pneumatic, hydraulic |
| Localization and mapping | 2D LiDAR + encoders + IMU | Line sensors, ultrasonic array, depth camera |
| Collision detection | Bumper limit switches | ToF, ultrasonic |
| Tank/bin level | Float switches | Capacitive, ultrasonic |
| Vision | USB webcam + LED light | ESP32-CAM, stereo/depth camera |
| Main controller | Arduino UNO Q | Raspberry Pi 5 + Mega, ESP32-S3, STM32 Nucleo |
| Energy source | 12 V SLA 24 Ah (prototype) | LiFePO4, Li-ion 3S/4S |
| Operator authorization | RFID RC522 | Keypad PIN, key switch |
| Status output | LED signal tower + LCD 20×4 | RGB LED + buzzer, touch display |
| Route programming | Web interface over Wi-Fi | RC transmitter, wired pendant |
| Chassis | Aluminum 2040 profile | Welded steel, 3D-printed/acrylic |

### E. Component list — summary

| Subsystem | Items | Subtotal (MXN) |
|---|---:|---:|
| Control, sensing and UI | 13 | $6,687.50 |
| Mobility, collection and separation | 12 | $5,267.00 |
| Power, safety and structure | 7 | $3,895.00 |
| **Total, listed components** | **32** | **$15,849.50** |

Main suppliers: UNIT Electronics, Sandorobotics, Steren, Home Depot México, AG Electrónica, Mikels, Maquinaria y Control, Electrónica Universal, Abasteo. Largest items: RPLIDAR A1M8 ($2,870, Sandorobotics, out of stock at check), Talon 124 mm wheels ($1,520, need a 3D-printed 6 mm → 12 mm hex hub) and SLA battery BR-1224 ($1,290). Not included: oil hose (AutoZone, no online price), wiring, fasteners, 3D-printed parts. The full line-item list with sources is in the deck.

## 11. Evaluation methods and working files

Three evaluations exist and must not be presented as interchangeable results.

### A. Weighted requirements–components matrix — 47 components (unchanged)

[Weighted matrix — 47 components](https://docs.google.com/spreadsheets/d/1MZ2SNzkPxzvO9T-omShws64Tjsg37_WgHSopBQhlQi0/edit)

- 10 requirements, original importance values and 47-component inventory.
- Relationship scale: **0 = none; 1 = weak; 3 = medium; 9 = strong**.
- Component score: **S(j) = Σ importance(i) × relationship(i,j)**.
- Count-based 80% selection: **38 of 47**. The cut is by count, not by score: Start button (position 39, 90 points) ties with RFID reader (position 38, 90 points) but falls outside.
- This matrix underrates mandatory items: Chassis is position 46 and Emergency stop position 41. The proposal in §9 keeps both regardless of score.

### B. Pairwise component comparison — 22 components

[Pairwise comparison (live)](https://docs.google.com/spreadsheets/d/19pLKUD3okLerDdvfoZEJU3ysCDMKe-jNFY9lGN_vhvA/edit)

- Covers the previous 22-item list, upper triangle: **231 unique pairs**.
- **0 = equal importance; Cxx:1 = mild preference; Cxx:2 = strong preference**. Only the winner receives points.
- The team had answered 143 pairs. An offline corrected workbook (*Pairwise_Comparison_Corrected.xlsx*) completes the 88 blank pairs from requirement-based scores and corrects 47 team answers that contradicted those scores by two or more levels, mostly in rows C03 (LiDAR) and C15 (UNO Q), where the column component had been entered as winner. Mandatory components (C14, C15, C22) win :2 against non-mandatory ones.
- Rank correlation between criteria and pairwise results: **0.26 with the original answers, 0.83 after correction**.
- This comparison does not yet include C23–C36; extend it if the team adopts the 33-item proposal.

### C. Agreement between evaluations

- Lowest in both the weighted matrix and the pairwise comparison: Pressurized water outlets (47/47, 22/22), Extra-products container (45/47, 21/22), Status indicators (43/47, 18/22) and Start button (39/47, 15/22).
- The first two are discarded in §9. Indicators and start button are kept because they serve safety (R5) and authorization (R10).

[Project folder](https://drive.google.com/drive/folders/1FUDjoQG8ePsiPn1uzvEDpGwZ0xfaLslv)

## 12. Expected benefits and validation limits

The project aims to reduce manual contact with contaminated residues, improve segregation at collection, reduce solids-storage volume through compaction and recover lubricant without diluting it with water or chemicals. Safe mobility and controlled collection aim to reduce residual floor contamination. These are expected benefits to validate, not measured results.

No injury reduction percentage, recycling uplift, mist-exposure reduction, guaranteed dryness or certified disposal outcome has been established by this project. Report measured prototype results with the lubricant, solids, floor, load and test conditions.

## 13. Open decisions before detailed design

- **Team confirmation of the 33-item proposal** (§9) versus the previous 22-item list.
- Lubricant type, viscosity/temperature range, material compatibility and representative solids.
- Collection volume, flow rate, suction height, filter mesh, magnet type and transfer/clogging behavior.
- Compactor stroke, force, drainage path and jamming behavior.
- Loaded robot mass, envelope, wheel versus track and stopping/obstacle-response targets.
- Vision purpose, mapping method, route format and UNO Q software/compute budget.
- Battery runtime check for the SLA 24 Ah choice; price for the oil hose; LiDAR availability (Sandorobotics out of stock); 3D-printed wheel hubs.
- Extend the pairwise comparison to C23–C36 or document why the weighted matrix is used for them.
- Confirm who may authorize operation (RFID credentials) and the start, fault, reset and maintenance sequence.

## 14. Academic deliverables and terminology

- [ ] Cover: title, team and professor.
- [ ] Motivation: general/social context and a quantitative paragraph with at least 4 checked references.
- [ ] Problem formulation: technical/literature discussion with at least 5 appropriate primary references, plus the specific project problem.
- [ ] Hypothesis and general objective aligned with the current scope.
- [ ] One-page labeled concept sketch and expected benefits.
- [ ] Requirements, evaluation methods, controller architecture and test plan.
- [x] Conceptual design: black box, UI components, functional and component white boxes, morphological matrix, component list with prices and suppliers (October 2026).
- [ ] Consistent bibliography with real, checked sources; distinguish review literature from primary experiments.

Use: **waste streams**, **ferrous fraction**, **mechanical filtration**, **magnetic separation**, **compaction**, **coverage path planning**, **SLAM**, **operating authorization**, **Arduino UNO Q** and **shift change**. Magnetic separation and the compaction assembly are part of the proposed inventory; state that they are pending team confirmation until §13 is closed.

## 15. Evidence and references

**Hardware source**
- Arduino. *UNO Q — official hardware documentation.* https://docs.arduino.cc/hardware/uno-q/ — accessed 24 September 2026.
- Supplier product pages for every priced component are listed on the last slide of *Conceptual_Design_Waste_Robot.pptx* (checked 8 October 2026).

**Inherited research sources from Draft 1 — retained for follow-up verification**

The original bibliography is preserved below for continuity. Its bibliographic details, claim fit and patent relevance have not all been independently revalidated. Draft 1's numerical injury statements (including $1.20 B, 14.4%, $8.32 B, >400,000 cases and 145 deaths) are not treated here as verified evidence; check the original source, year, geography and case definition before using them in a deliverable.

**Motivation/need**
1. Liberty Mutual. *2023 Workplace Safety Index: Manufacturing.* https://business.libertymutual.com/wp-content/uploads/2023/07/WSI_1005_2023.pdf
2. National Safety Council. *Injury Facts — Falls to the Same Level* (BLS data). https://injuryfacts.nsc.org/work/safety-topics/falls-same-level/
3. OSHA. *Metalworking Fluids: Safety and Health Best Practices — Health Effects.* https://www.osha.gov/metalworking-fluids/health-effects
4. NIOSH (1998). *Occupational Exposure to Metalworking Fluids* (Pub. 98-102). https://www.cdc.gov/niosh/docs/98-102/

**Technical literature — inherited bibliography; includes review articles**
5. Cadena et al. (2016). Past, present, and future of SLAM. *IEEE T-RO, 32*(6), 1309–1332. https://doi.org/10.1109/TRO.2016.2624754
6. Le et al. (2019). Energy optimization of path planning in a differential-drive floor-cleaning robot. *Energies, 12*(6), 1136. https://doi.org/10.3390/en12061136
7. Svoboda & Fujita (2003). Recent developments in magnetic methods of material separation. *Minerals Engineering, 16*(9), 785–792. https://doi.org/10.1016/S0892-6875(03)00212-7
8. Lee et al. (2017). Eco-friendly technology for recycling of cutting fluids and metal chips: A review. *Int. J. Precis. Eng. Manuf.-Green Tech., 4*(4), 457–468. https://doi.org/10.1007/s40684-017-0051-9
9. Debnath, Reddy & Yi (2014). Environmental friendly cutting fluids and cooling techniques: A review. *J. Cleaner Production, 83*, 33–47. https://doi.org/10.1016/j.jclepro.2014.07.071

**Patent prior art (Espacenet)**
10. EP2808668A1 · 11. US2007271004A1 · 12. CN112641396A · 13. CN114129101A · 14. CN115319717A

## 16. Revision record

**Draft 6 — 9 October 2026:** added the seventh team member (Juan Manuel Vásquez Paniagua); added specific objectives OE1–OE6; added the conceptual design (black box, UI components, white boxes, morphological matrix with selected concept, priced component list: 32 items, $15,849.50 MXN); recorded prototype drive and battery choices; renumbered sections 11–16.

**Draft 5 — 25 September 2026:** proposed a 33-item inventory from the 47-component weighted matrix (33 keep, 6 integrate, 8 discard); restored compaction, magnetic separation, overflow, leak, relay e-stop, IMU, bumper, LED lighting and RFID hardware; removed water/steam outlets and auxiliary-product container; assigned C23–C36; mapped all 10 requirements to hardware; recorded the corrected pairwise workbook (143 team answers, 88 completed, 47 corrected; rank correlation 0.26 → 0.83) and the low-position agreement between evaluations. Pending team confirmation.

**Draft 4 — 24 September 2026:** synchronized the brief and pairwise spreadsheet to the 22-component list; preserved and remapped 12 pairwise responses; updated formulas, dropdowns and result ranges to 231 pairs. The weighted spreadsheet was restored and verified against its original 47-component data and formulas.

**Draft 3 — 24 September 2026:** replaced the active inventory with the 22 components supplied by the team; retained Arduino UNO Q; retained the conditional camera and consolidated emergency-stop entry; marked requirement-coverage gaps.

**Draft 2 — 24 September 2026 (historical):** incorporated 10 requirements and importance values; retained the 47 candidate IDs and weighted-selection results; specified Arduino UNO Q; documented both evaluation methods; replaced absolute performance/novelty assertions with testable objectives.

---
*Update the version and affected decisions when the team revises the project. Spreadsheet snapshots describe the state read on the revision date; follow the linked live files for later scores.*
