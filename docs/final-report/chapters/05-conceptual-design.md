# Conceptual design

## General description

The robot is a low, aluminum-framed differential-drive vehicle of about 700 × 500 × 450 mm that works in a cleared
area during shift changes. A rotary nylon brush and a rubber squeegee gather lubricant and metal chips toward a
nozzle. A 12 V wet/dry vacuum lowers the pressure in a sealed separation chamber, so the mixture is drawn in through
an oil-resistant hose. Inside the chamber, a stainless mesh basket retains coarse solids, neodymium magnets capture
the ferrous chips and a linear actuator compacts and drains them into a removable basket. The liquid flows by gravity
into a separate 20 L tank with float level sensors, a leak tray and a ball drain valve. An Arduino UNO Q controls the
robot: its MCU handles motors, sensors and sequencing, and its Linux side runs LiDAR mapping, routes, vision and a web
interface. An RFID card authorizes each cycle, a signal tower and LCD report status, and a hardware emergency stop
cuts every actuator through a relay.

## Black box

The black box defines the robot only by its inputs, outputs and user interfaces (UI).

![Black box of the robot: user-interface inputs, inputs, outputs and user-interface outputs.](img/black_box.png)

| UI (input) | Inputs | Outputs | UI (output) |
|---|---|---|---|
| Operator authorization · start/stop command · emergency stop · route programming and manual control · waste emptying and maintenance access | Operator · floor with lubricant and chips · programmed route/area map · obstacle detection · floor surface condition · energy · on/off | Movement go/stop · clean floor area · separated lubricant · separated, compacted chips · noise · status signal | Status indicator (operating/fault/finished) · audible alarm · tank and bin level · battery level · cycle progress |

### User-interface components

| UI function | Selected component | Code | Reason |
|---|---|---|---|
| **Input UI (operator → robot)** | | | |
| Operator authorization | RC522 RFID reader + 13.56 MHz cards | C36 | Only trained staff can start a cycle (R10) |
| Start / stop command | 22 mm illuminated push button | C18 | Industrial format; lit when ready |
| Emergency stop | Mushroom e-stop + 40 A relay | C22, C32 | Cuts motor power without software (R5) |
| Route programming, manual control | Web interface over UNO Q Wi-Fi (phone/laptop) | C20 | No extra hardware; saves and loads routes (R8) |
| Waste emptying, maintenance | ½" ball drain valve + removable chip basket | C30, C28 | Controlled emptying of each stream (R9) |
| **Output UI (robot → operator)** | | | |
| Status (operating / fault / finished) and audible alarm | 12 V LED signal tower (green / amber / red) with built-in alarm | C19 | Visible across the plant floor; alarm on faults, full tank, e-stop |
| Tank, bin and battery level; cycle progress | 20×4 I2C LCD + web interface | C19 | Local reading at the robot; recharge planning |

## White box A: functional structure

White box A opens the black box into six functional modules: operation, navigation, collection, separation, storage
and supervision. The material flow runs from collection through separation to storage; the liquid leaves the
separation module after filtering.

![White box A: functions inside the system boundary, grouped into six modules.](img/white_box_a.png)

| Functional module | Functions | Input flows | Output flows |
|---|---|---|---|
| Operation | Authorize operator · verify safety state · start/stop cycle | Operator authorization, start/stop, e-stop | — |
| Navigation | Load route and map · localize robot · detect obstacles · drive (go/stop) | Route program, obstacles, surface | Movement go/stop |
| Collection | Agitate and gather waste · suck lubricant + chips | Floor with lubricant and chips | Clean floor, noise |
| Separation | Filter coarse solids · capture ferrous chips · compact and drain solids | Mixture from collection | Compacted chips; liquid to storage |
| Storage | Store liquid · monitor tank/bin levels | Liquid | Separated lubricant |
| Supervision | Manage energy · report status | Energy, on/off | Status signal, alarm |

## White box B: components

White box B replaces each function with the selected component. The Arduino UNO Q sits at the center, with the
sensors and operator inputs on the left and the actuators and process equipment on the right. The power path
(battery, fuses and relay, 12 → 5 V converter) and the hardware e-stop relay appear at the bottom. It is based on the
team's *robot_components_level_CORRECTED* diagram, updated with the selected parts, and adds the e-stop relay circuit
that the team diagram did not show.

![White box B: selected components inside the system boundary.](img/white_box_b.png)

## Morphological matrix

The matrix lists three or more technological alternatives for each function; the **bold** option forms the selected
concept. Selection followed the requirement weights of Chapter 3 and three practical rules: compatibility with oil,
availability in Mexico within the budget, and manageable complexity for a student build.

| Function | Option 1 | Option 2 | Option 3 | Option 4 |
|---|---|---|---|---|
| Traction | Rubber tracks | **Differential drive, rubber wheels** | Mecanum wheels | Swerve modules |
| Drive motors | **DC gearmotor + Hall encoder** | Stepper NEMA 23 | BLDC hub motors | — |
| Motor driver | L298N dual H-bridge | Cytron MDD10A | **BTS7960 43 A H-bridge** | — |
| Floor agitation | Side disc brushes | **Rotary nylon brush (775 motor)** | Squeegee only | Microfiber roller |
| Waste suction | **12 V wet/dry vacuum unit** | Diaphragm pump | Peristaltic pump | Centrifugal pump |
| Coarse-solids filtering | Cyclone separator | Settling (decantation) tank | **Stainless mesh basket** | — |
| Ferrous separation | **Neodymium bar magnets** | Electromagnet | Magnetic drum | — |
| Solids compaction | Lead screw + DC motor | **12 V electric linear actuator** | Pneumatic cylinder | Hydraulic press |
| Localization and mapping | Floor line sensors | Ultrasonic array | **2D LiDAR + encoders + IMU** | Depth camera |
| Collision detection | **Bumper limit switches** | ToF sensors (VL53L0X) | Ultrasonic sensors | — |
| Tank / bin level | Capacitive non-contact | **Float switches** | Ultrasonic level sensor | — |
| Vision | ESP32-CAM | **USB webcam + LED light** | Stereo / depth camera | — |
| Main controller | **Arduino UNO Q** | Raspberry Pi 5 + Arduino Mega | ESP32-S3 | STM32 Nucleo |
| Energy source | 12 V LiFePO4 | Li-ion 3S / 4S pack | **12 V SLA 24 Ah (prototype)** | — |
| Operator authorization | Keypad PIN | Key switch | **RFID reader RC522** | — |
| Status output | **LED signal tower + LCD 20×4** | Single RGB LED + buzzer | Touch display | — |
| Route programming | RC transmitter | **Web interface over Wi-Fi** | Wired joystick pendant | — |
| Chassis / frame | **Aluminum 2040 profile** | Welded steel sheet | 3D-printed / acrylic panels | — |

**Justification of the key choices.**

- **Differential drive with rubber wheels** rather than tracks or mecanum: in-place turning with simple odometry, and
  mecanum rollers lose traction quickly on oil.
- **12 V wet/dry vacuum** rather than pumps: one device moves liquid and solids into a sealed chamber; pumps clog with
  chips or need a separate solids path.
- **Mesh basket + neodymium magnets** rather than a cyclone or magnetic drum: passive, cheap, no extra power; a cyclone
  needs high, steady air flow that a 12 V unit cannot guarantee.
- **LiDAR + encoders + IMU** rather than floor lines: oil fouls floor markings, and the line sensor was discarded in
  both selection methods.
- **Arduino UNO Q** rather than a Raspberry Pi + microcontroller: one board covers real-time I/O and Linux workloads,
  and the team already won second place with it (ADR-0001).
- **12 V SLA battery** for the prototype: cost, availability and a simple charger; LiFePO4 is the planned upgrade for
  lower weight and longer life.

## Final concept

The final concept is the combination highlighted in the morphological matrix, organized into nine modules mounted on
a common 2040 T-slot frame.

![Final concept, side cutaway (front of the robot on the left). Numbers match the legend below.](img/final_concept.png)

| # | Part | # | Part | # | Part |
|:-:|---|:-:|---|:-:|---|
| 1 | Rotary nylon brush (775 motor) | 7 | Chip basket + linear-actuator compactor | 13 | RPLIDAR A1M8 360° LiDAR |
| 2 | Rubber squeegee | 8 | 20 L sealed lubricant tank + floats | 14 | Webcam + LED light |
| 3 | Collection nozzle + oil-resistant hose | 9 | Ball drain valve | 15 | Bumper with limit switches |
| 4 | 12 V wet/dry vacuum unit | 10 | Drive wheel Ø124 mm + gearmotor | 16 | HMI: RFID, start button, LCD |
| 5 | Stainless mesh basket (coarse solids) | 11 | 12 V 24 Ah battery, fuses, relays | 17 | Emergency stop (hardware relay) |
| 6 | Neodymium magnet bars (ferrous chips) | 12 | Arduino UNO Q + BTS7960 drivers | 18 | Signal tower with alarm |

| Module | Function | Main components | Listed cost (MXN) |
|---|---|---|--:|
| M1 Chassis and structure | Carries every module; defines the envelope | 2040 aluminum profile, panels, bumper bar, leak tray | 1,276.00 |
| M2 Mobility | Moves along stored routes with odometry | 2 × JGB37-3530 59 rpm gearmotors with encoders, Talon 124 mm wheels, caster, BTS7960 | 3,011.00 |
| M3 Collection | Loosens and picks up lubricant and chips | 775 brush motor, nylon brush, squeegee, nozzle, hose, Mikels AA-12 vacuum, MPX5010DP | 1,472.00 |
| M4 Separation and compaction | Retains solids and ferrous chips; liquid passes | Mesh basket, 10 neodymium magnets, chip basket, 150 kgf actuator, load cell + HX711 | 1,087.00 |
| M5 Storage | Keeps the liquid sealed, measured, easy to empty | 20 L container, ½" ball valve, float sensors, float shut-off | 369.00 |
| M6 Perception | Knows where the robot is and what is around it | RPLIDAR A1M8, BNO055 IMU, USB webcam, LED light, 4 bumper switches | 4,232.00 |
| M7 Control and electronics | Real-time control and high-level navigation | Arduino UNO Q 2 GB, perforated PCBs, MOSFETs | 1,122.00 |
| M8 Power and safety | Supplies energy; guarantees a hardware stop | 12 V 24 Ah SLA, charger, 2 × XL4015, fuses, 2 × 40 A relays, LAY37 e-stop | 2,619.00 |
| M9 Operator interface | Authorized start, status, stop | RC522 RFID, 22 mm button, LCD 20×4, signal tower, web UI | 661.50 |
| **Listed components (32 items)** | | | **15,849.50** |
| With tooling and consumables (filament, cable, clamps, crimper) | | | 17,530.50 |
| With 15 % contingency for unpriced items (hose, gaskets, fasteners) | | | ≈ 20,160 |

Prices checked 8–9 October 2026. Full line-item list with suppliers in Appendix B.

## Operating cycle

Idle → RFID card → **Authorized** → start button → **Running** along the stored route → (tank or basket full, or
route done) → **Compacting** → **Ready to empty**. An obstacle or bumper contact **pauses** the robot until the path
is clear; a **fault or e-stop** from any state requires a deliberate restart (new card + start button).

## Main design risk and contingency

Suction of dense steel chips with an 80 W vacuum is the critical uncertainty (Section 4.7). The suction rig decides
between two collection architectures; the rest of the architecture is the same in both cases.

| | **A · Baseline** | **B · Contingency** |
|---|---|---|
| Principle | Brush + vacuum carry liquid and chips into the sealed chamber | Brush throws chips into a front hopper with magnets; vacuum handles only liquid |
| Pros | One intake, simplest mechanism; everything enters the sealed chamber | Chips never pass through the hose; vacuum works on its easiest load |
| Cons | The 80 W vacuum may not lift dense steel chips; long chips can clog the hose | Two collection points; more mechanism at the front |
| Decision criteria (fixed before the test) | Choose A only if chip pickup ≥ 85 % and no clogging in 10 runs | Otherwise B |
