# Architecture decision records

Every decision between options is recorded in `docs/adr/` with its context, the options considered, the decision and
its consequences [73]. A decision cannot be changed silently: a new ADR supersedes the old one.

| ADR | Decision | Status | Date | Requirements |
|---|---|---|---|---|
| 0001 | Arduino UNO Q 2 GB as main controller | Accepted | 24 Sep 2026 | R5, R6, R7, R8, R10 |
| 0002 | Split MCU / Linux by timing requirement | Accepted | 21 Nov 2026 | SR-006, SR-007, SR-013 |
| 0003 | Hardware emergency stop through main relay | Accepted | 9 Oct 2026 | SR-006, SR-014 |
| 0004 | Collection architecture A (vacuum for all) vs B (front hopper for chips) | **Proposed — decide with suction rig** | — | SR-001, SR-002 |
| 0005 | IMU: BNO055 (IMU mode) preferred over MPU-6050 | Proposed | 15 Nov 2026 | R7, R8 |
| 0006 | Vision assists only: residue check and container-level cross-check, enabled only after validation | Accepted | 21 Nov 2026 | R6, R9, SR-015–SR-017 |
| 0007 | AprilTag camera localization as a bench test tool | Accepted | 22 Nov 2026 | R8, R6, SR-017–SR-021 |
| 0008 | Low-dose, low-foam degreaser sprayed ahead of the brush | Accepted (dose and product set by TP-S02) | 25 Nov 2026 | SR-001–SR-003, SR-005, SR-008, SR-022–SR-025 |

## ADR-0001 · Arduino UNO Q 2 GB as main controller

**Context.** The robot needs real-time I/O (motors, encoders, sensors, sequencing) and Linux workloads (LiDAR mapping,
vision, web UI, logs). **Options:** UNO Q · Raspberry Pi 5 + Arduino Mega · ESP32-S3 · STM32 Nucleo · Raspberry Pi 4
+ microcontroller. **Decision:** UNO Q 2 GB (ABX00162, ≈ MXN 1,080, UNIT Electronics). One board covers both domains;
the team already used it in a previous robot (second place). A Pi 4 has a stronger CPU and bigger ROS 2 community but
needs an extra MCU for PWM, encoders and HX711. **Consequences:** single USB-C port → powered USB-C hub needed for
LiDAR + webcam; consider the 4 GB variant if SLAM + web UI saturate RAM; CAN only classic via FDCAN (not needed now);
Bridge RPC latency must be measured (T_stale).

## ADR-0002 · Split MCU / Linux by timing requirement

**Context.** Lesson 1 from the previous UNO Q robot. **Decision:** the MCU executes each motion order autonomously
and stops by itself (obstacle flag, bumper, fault, overspeed, stale command). Linux plans and decides with the robot
stopped or between segments. Heartbeat every 100 ms; T_stale initially 300 ms, to be set from measured RPC latency +
margin. **Consequences:** the protocol must be versioned; every stop reason logged; the simulator must model RPC
delays and clock jumps.

## ADR-0003 · Hardware emergency stop through main relay

**Decision:** LAY37 mushroom e-stop (normally closed) in series with the 40 A main relay coil feeding the switched
12 V bus (drive, collection, separation). Logic stays powered to report. E-stop state also read by the MCU. Restart
requires RFID + start button. **Consequences:** relay inrush and contact welding is a DFMEA item (F-003); the WCCA
must check contact ratings; a certified product would need a safety relay with monitored contacts (ISO 13849-1).

## ADR-0004 · Collection architecture A vs B (open)

**Options.** A: brush + vacuum carry liquid and chips into the sealed chamber (one intake, simplest). B: brush throws
chips into a front hopper with magnets; vacuum handles only liquid (chips never pass through the hose). **Decision
criteria (fixed before the test):** chip lift rate (g/s) for reference chips; liquid recovered per pass; clogging with
long chips (count per 10 runs); current and temperature of the vacuum motor. **Choose A only if chip pickup ≥ 85 % and
no clogging in 10 runs.** **Context:** pickup velocity grows with density (steel ≈ 7,850 kg/m³); the 80 W automotive
vacuum is the main technical risk (F-001, SC-001). **Evidence so far:** TP-S01 (measured 24 Nov 2026, exploratory,
handheld dry vacuum 16 kPa / 40 AW seller data, no brush, no squeegee): dry, 0 of 5 coins lifted and no visible change
on the film; with water + dish soap + baking soda, film mostly removed (visual 85–90 %) and 2 of 5 coins (30 % by
mass). Suction alone fails the option-A criterion with that vacuum; the brush + squeegee concept and the BOM vacuum are
still untested, so the decision stays open and is taken on the TP-S02 rig.

## ADR-0005 · IMU: BNO055 in IMU mode

**Decision (proposed):** BNO055 in IMU mode (no magnetometer: unreliable near steel and motors); on-chip fusion saves
firmware time. MPU-6050 is cheap but end-of-life (mostly clones) and needs its own fusion; acceptable fallback because
LiDAR scan matching corrects heading drift. Test I²C clock stretching on the STM32U585 early. Note: BME280/BMP280 are
barometers, not IMUs.

## ADR-0006 · Vision assists only

**Context.** R6 (vision, importance 6) had no defined task. The team's previous robot used a camera: on a glossy black
floor the light reflected and the camera saw walls that did not exist; it went from leader to tie-breaker to off, and
simulation showed no measurable gain from it.

| Topic | What the maze robot did | Result |
|---|---|---|
| Hardware | OV9281 mono global-shutter USB camera on Linux (OpenCV + V4L2), 320 × 240, buffer 1, 3 frames flushed per read | Worked |
| Pipeline | Median blur → contrast stretch → Otsu threshold on the lower half → binary floor/wall | Worked on a matte floor |
| Geometry | Pixel → floor point from lens height and tilt taken from CAD; tilt recalibrated on site | CAD tilt was wrong (25° → 40°); on-site calibration needed |
| Calibration | Phone web page saved to JSON: fixed exposure and gain, offsets, tilt; reads back what the driver applied | Auto exposure moved the threshold with light and people |
| Glare | A wall had to extend ≥ 14 image rows; shorter white blobs treated as reflections | Added after the first track run |
| Role | Camera: leader → tie-breaker → off. It never blocks a path; a hit only slows the robot | ToF became the authority for walls |
| Field | First v2 track run: glossy floor → false walls (plus a clock jump and a gyro-sign bug) | `CAM_LOC = False`; camera kept logging only |

**Options for the vision task.** A residue check on the cleaned strip (re-pass request); B spill detection ahead;
D container-level cross-check (low/half/full vs floats); C person/obstacle detection — **rejected** (ISO 3691-4 4.8.2
stays with LiDAR + bumpers; a webcam is not a safety sensor).

**Decision.** Vision has two tasks: **A residue check** (SR-015, output = re-pass request) and **D container-level
cross-check** (SR-016, output = "check floats" warning). It never stops, steers or blocks the robot and never feeds a
safety function. **Validation gate (SR-017):** both start in log-only mode and each action flag is enabled only after
TP-V01 passes on the real robot and the report is committed. Controlled lighting: shroud + own LED, fixed exposure and
gain from the phone calibration page, values read back and logged; test a cross-polarized LED/lens pair against oil
sheen. Before tuning: capture a labeled photo set on the real floor.

## ADR-0007 · AprilTag bench localization

**Options.** Detector: `pupil_apriltags` vs `cv2.aruco`. Pose: free 6-DOF per tag vs planar 3-DOF solver. Camera mode:
fastest vs largest image with a minimum frame rate. Web image: stream frames vs numbers only. **Decision:** `cv2.aruco`
with sub-pixel corners; planar Gauss–Newton solver on all corners; publish no pose when ambiguous; largest mode with
≥ 40 fps; `STREAM = False`; bench tool only. **Consequences:** pose quality depends on measured tags, tag size,
intrinsics and mount; wrong values show up as `reproj` or `tags_disagree` instead of a wrong pose; a camera tilt
different from the configured pitch breaks the planar model, so the mount must be rigid; at 0.38 m/s the robot moves
≈ 8 mm per frame at 45 fps (deduced); the web page has no authentication (lab network only).

## ADR-0008 · Low-dose, low-foam degreaser ahead of the brush

**Context.** TP-S01 showed that dry suction does not move the oil film nor the heavier flat pieces, while a simple
degreasing solution removed most of the film. The semester-1 concept assumed oil only (no water or chemicals) to keep
the liquid stream undiluted and avoid a third waste stream.

| Option | For | Against |
|---|---|---|
| 0 Dry: brush + vacuum only | Oil stream undiluted, simplest | Brush + dry suction untested on viscous film; TP-S01 shows suction alone fails |
| 1 Flood with water + detergent (scrubber style, ≈ 60 mL/m², deduced from commercial scrubbers) | Proven in scrubbers | Large tank and mass, lots of oily water, foam, wet slippery floor |
| **2 Low-dose spray (≈ 20 mL/m², estimate) of a low-foam, quick-break alkaline degreaser ahead of the brush** | Breaks the film and the oil seal under chips with little water; quick-break lets oil separate in the tank | Liquid stream becomes oil + water; adds tank, pump, nozzles and a consumable |
| 3 Solvent degreaser | No water | Flammable/VOC exposure (NOM-010-STPS), not acceptable near people |

**Decision.** Option 2: a 5 L clean-solution tank, a 12 V diaphragm pump and a spray bar (2 flat-fan nozzles) wet the
strip just ahead of the brush; brush → squeegee → nozzle → sealed chamber stay as designed. Product (SR-025):
low-foam, quick-break, silicone-free, water-based, SDS per NOM-018-STPS-2015, no flammable solvent. The pump runs only
while the robot moves in cleaning mode with the brush on, from the e-stop-switched bus (rule 1).

**Consequences.** Still two waste streams (the solution tank is a supply); the claim "oil recovered undiluted" is
withdrawn — the oil floats and is decanted, the water phase is oily wastewater for an authorized handler. Foam
(F-010, SR-023), wet floor (F-011, SR-024) and unknown friction on the soapy film (F-004, SR-005) must be measured.
The solution conducts, so IPX4 below the deck (F-013). Wet chips may rust (F-014). Refill exposure → PPE and SDS
(P-001). Estimates: hardware ≈ MXN 1,000, +≈ 5.5 kg full, +≈ 5 W → 165 W and ≈ 52 min per charge, ≈ 1.4 L per cycle,
concentrate ≈ MXN 2,500/yr and extra oily-water disposal ≈ MXN 7,700/yr. The rig needs a wet trap so the vacuum never
ingests liquid (TP-S02).
