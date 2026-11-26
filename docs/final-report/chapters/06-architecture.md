# System architecture

This chapter details the design of models: where each module sits, what it contains, how the modules connect
(material, power, signals, mechanics) and how control and safety are split. Source: *Design of Models* deck and
`docs/02-architecture.md`.

## Layout

| View | Arrangement (front of the robot on the left) |
|---|---|
| Side | Front: M3 brush and nozzle, then M3 vacuum unit. Center: M4 separation chamber and compactor, M8 battery low just ahead of the drive axle. Rear: M5 20 L tank, drain valve on the rear face. Top: M7 electronics bay under the lid, M9 HMI panel at the rear, M6 LiDAR on a mast at the highest point (520 mm). M2 drive wheels Ø124 mm at mid-length, caster under the rear |
| Top | M3 brush + nozzle across the full front width; M7 electronics bay over M4; M5 tank at the rear; M9 HMI panel rear-top; signal tower on the side, below the LiDAR scan plane |
| Envelope | ≈ 700 × 500 × 450 mm (520 mm to LiDAR top), to be verified in detailed design (SR-012) |
| Mass distribution | Heaviest masses (battery, tank) low and near the drive axle; nothing rises above the LiDAR scan plane |

## The nine modules in detail

Every component of the conceptual design belongs to exactly one module. Coherence checks passed: each requirement
R1–R10 is served by at least one module; no component appears in two modules; every module has defined power, data
and mechanical interfaces.

### M1 · Chassis and structure

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| Aluminum 2040 profile, 1 m | C14 | 4 | 1,276.00 |
| T-nuts, brackets, fasteners | C14 | — | TBD |
| Side panels and maintenance covers | C14 | — | TBD |
| Front bumper bar | C35 | 1 | TBD |
| Internal leak tray | C31 | 1 | TBD |

Interfaces: 20×40 T-slot rails, M5 T-nuts for every module, removable top lid and rear panel (mechanical); common
chassis ground point (power); leak tray drains toward the tank M5 (fluid). Each module bolts to the rails and can be
removed on its own.

### M2 · Mobility

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| JGB37-3530 12 V gearmotor, 59 rpm, encoder | C01, C17 | 2 | 960.00 |
| Talon 124 mm wheels (pair) + 3D-printed hubs | C01 | 1 | 1,520.00 |
| Heavy-duty 3" swivel caster | C01 | 1 | 289.00 |
| BTS7960 43 A H-bridge driver | C24 | 2 | 242.00 |

Interfaces: motor brackets on lower rails at mid-length, caster under the rear; 12 V switched bus (cut by the
e-stop); PWM + DIR from the MCU, encoder A/B back to the MCU. Notes: 59 rpm × Ø124 mm ≈ 0.38 m/s top speed;
differential steering turns in place inside aisles; torque with a full tank still to verify (limit test fill until
then). The Talon wheels need a printed 6 mm → 12 mm hex hub (`cad/parts/wheel_hub_hex.scad`).

### M3 · Collection

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| Motor 775 12 V + belt reduction | C04 | 1 | 139.00 |
| Rotary nylon brush (from HDX floor brush) | C04 | 1 | 155.00 |
| Rubber squeegee strip | C08 | 1 | TBD |
| Collection nozzle (3D-printed PETG) | C11 | 1 | TBD |
| Oil-resistant hose 3/8" | C10 | 2 m | TBD |
| 12 V wet/dry vacuum unit, Mikels AA-12 (80 W) | C12 | 1 | 522.00 |
| MPX5010DP vacuum sensor | C13 | 1 | 535.00 |
| BTS7960 driver (brush) | C24 | 1 | 121.00 |

Interfaces: front sub-frame on the lower rails, quick-release hose clamp; 12 V switched, vacuum motor through a 40 A
relay; brush PWM, vacuum on/off, sensor analog; hose → M4 inlet. Notes: the brush throws waste toward the nozzle and
the squeegee behind it leaves the floor dry; the vacuum motor pulls air from the sealed M4/M5 volume (wet-vac
principle). The slipping brush belt acts as a mechanical fuse on jams.

### M4 · Separation and compaction

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| Stainless mesh strainer basket | C06 | 1 | 82.00 |
| Neodymium magnet bars 28 × 4 × 2 mm | C27 | 10 | 130.00 |
| Removable perforated chip basket | C28 | 1 | TBD |
| Compaction chamber with drain | C25 | 1 | TBD |
| 12 V linear actuator 150 kgf, 100 mm | C29 | 1 | 711.00 |
| Load cell 50 kg + HX711 | C26 | 1 | 43.00 |
| BTS7960 driver (actuator) | C24 | 1 | 121.00 |

Interfaces: sealed chamber on the center rails with gasketed lid; 12 V switched (actuator); actuator PWM/DIR, HX711
clock/data; inlet from M3, liquid out by gravity to M5. Notes: compaction runs with suction stopped and the lid
closed; the load cell limits the pressing force to 100 kgf; drained oil returns to the tank.

### M5 · Storage

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| 20 L multipurpose container | C02 | 1 | 199.00 |
| ½" brass ball drain valve | C30 | 1 | 76.00 |
| Horizontal float level sensors | C23 | 2 | 94.00 |
| Float shut-off at the vacuum port | C23 | 1 | TBD |

Interfaces: tank cradle on the rear rails, valve on the rear face; float switches → MCU; inlet from M4, air port to
vacuum, drain outlet. Notes: the tank is part of the vacuum volume, so it must hold suction; the shut-off float keeps
liquid out of the vacuum motor in hardware.

### M6 · Perception

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| RPLIDAR A1M8 360° LiDAR | C03 | 1 | 2,870.00 |
| BNO055 + BMP280 IMU | C33 | 1 | 439.00 |
| USB Full HD webcam COM-126 | C16 | 1 | 699.00 |
| LED light for the camera | C34 | 1 | TBD |
| ME-8108 bumper limit switches | C35 | 4 | 224.00 |

Interfaces: LiDAR mast at the highest point, camera front-top, IMU near the turning center; 5 V logic bus; LiDAR and
camera USB to Linux, IMU I2C, bumpers digital inputs. Notes: nothing rises above the LiDAR scan plane; bumpers stop
the motors and back up the LiDAR.

### M7 · Control and electronics

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| Arduino UNO Q 2 GB (ABX00162) | C15 | 1 | 1,080.00 |
| Perforated PCB 9 × 15 cm | C21 | 2 | 42.00 |
| MOSFETs, level shifting, connectors | C24 | — | TBD |

Interfaces: ventilated bay under the top lid, above and away from liquid; 5 V logic from M8; every module's signals;
Wi-Fi to the operator. A powered USB-C hub is needed for LiDAR + webcam (single USB-C port, ADR-0001).

### M8 · Power and safety

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| 12 V 24 Ah SLA battery BR-1224 | — | 1 | 1,290.00 |
| SLA battery charger BR-600 | — | 1 | 999.00 |
| XL4015 buck 12 → 5 V, 5 A | — | 2 | 104.00 |
| Automotive bayonet fuse holders | C24 | 4 | 76.00 |
| 40 A relays (main + vacuum) | C32 | 2 | 98.00 |
| LAY37 emergency stop | C22 | 1 | 52.00 |

Interfaces: battery low, just ahead of the drive axle, charge port on the rear panel; switched 12 V to M2/M3/M4,
fused 12 V → 5 V for M6/M7/M9; e-stop state to the MCU.

### M9 · Operator interface

| Component | Code | Qty | Cost (MXN) |
|---|---|:-:|--:|
| RC522 RFID reader + cards | C36 | 1 | 39.00 |
| 22 mm illuminated start button | C18 | 1 | 122.50 |
| LCD 20 × 4 with I2C | C19 | 1 | 105.00 |
| 12 V signal tower with alarm | C19 | 1 | 395.00 |
| Web interface (software) | C20 | — | TBD |

Interfaces: rear top panel next to the e-stop, tower on the side below the LiDAR plane; 5 V logic, tower 12 V through
MOSFETs; RFID SPI, button input, LCD I2C, tower outputs, web UI over Wi-Fi. Tower colors follow NOM-026-STPS: green
running, amber paused/full, red fault/e-stop.

## Material flow

The vacuum motor pulls air from the sealed separation chamber and tank, so waste never passes through the motor.

<figure>
<svg viewBox="0 0 760 250" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif" font-size="11">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#5d6670"/></marker>
<marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2b6cb0"/></marker></defs>
<g stroke="#22313f" stroke-width="1.2">
<rect x="5" y="20" width="95" height="46" rx="5" fill="#f3e3b5"/><rect x="125" y="20" width="95" height="46" rx="5" fill="#fff"/>
<rect x="245" y="20" width="95" height="46" rx="5" fill="#fff"/><rect x="365" y="20" width="110" height="46" rx="5" fill="#fbeed6"/>
<rect x="500" y="20" width="110" height="46" rx="5" fill="#fbeed6"/><rect x="635" y="20" width="118" height="46" rx="5" fill="#fbeed6"/>
<rect x="635" y="110" width="118" height="40" rx="5" fill="#e6e9ee"/>
<rect x="365" y="110" width="110" height="46" rx="5" fill="#dcebf7"/><rect x="365" y="190" width="110" height="40" rx="5" fill="#dcebf7"/>
<rect x="125" y="110" width="140" height="46" rx="5" fill="#eef5ea"/><rect x="125" y="190" width="140" height="40" rx="5" fill="#fff"/>
</g>
<g text-anchor="middle" fill="#1d2329">
<text x="52" y="40">Floor</text><text x="52" y="55" font-size="9.5">oil + chips</text>
<text x="172" y="40">Brush +</text><text x="172" y="55">squeegee</text>
<text x="292" y="40">Nozzle +</text><text x="292" y="55">oil hose</text>
<text x="420" y="40">Mesh basket</text><text x="420" y="55" font-size="9.5">coarse solids</text>
<text x="555" y="40">Magnet bars</text><text x="555" y="55" font-size="9.5">ferrous chips</text>
<text x="694" y="40">Chip basket</text><text x="694" y="55" font-size="9.5">+ compactor ≤100 kgf</text>
<text x="694" y="128">Compacted chips</text><text x="694" y="142" font-size="9.5">removable basket</text>
<text x="420" y="130">20 L sealed tank</text><text x="420" y="145" font-size="9.5">+ floats</text>
<text x="420" y="207">Drain valve</text><text x="420" y="221" font-size="9.5">separated lubricant</text>
<text x="195" y="130">12 V vacuum motor</text><text x="195" y="145" font-size="9.5">clean air only</text>
<text x="195" y="207">Float shut-off</text><text x="195" y="221" font-size="9.5">at the vacuum port</text>
</g>
<g stroke="#5d6670" stroke-width="1.6" fill="none" marker-end="url(#ar)">
<path d="M100,43 H123"/><path d="M220,43 H243"/><path d="M340,43 H363"/><path d="M475,43 H498"/><path d="M610,43 H633"/><path d="M694,66 V108"/>
</g>
<g stroke="#2b6cb0" stroke-width="1.6" fill="none" marker-end="url(#ab)">
<path d="M420,66 V108"/><path d="M420,156 V188"/><path d="M660,66 C620,95 520,110 477,128"/>
</g>
<g stroke="#8a929c" stroke-width="1.4" stroke-dasharray="5 4" fill="none" marker-end="url(#ar)">
<path d="M365,133 H267"/><path d="M195,188 V158"/>
</g>
<text x="300" y="125" font-size="9.5" fill="#5d6670" text-anchor="middle">air</text>
<text x="560" y="100" font-size="9.5" fill="#2b6cb0" text-anchor="middle">drained oil</text>
<text x="430" y="85" font-size="9.5" fill="#2b6cb0">liquid (gravity)</text>
</svg>
<figcaption>Material flow from the floor to two separate streams. Grey: solids · blue: liquid · dashed: air.</figcaption>
</figure>

## Power and safety architecture

<figure>
<svg viewBox="0 0 760 270" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif" font-size="11">
<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#22313f"/></marker></defs>
<g stroke="#22313f" stroke-width="1.2">
<rect x="5" y="95" width="105" height="50" rx="5" fill="#f6d2cf"/><rect x="135" y="95" width="80" height="50" rx="5" fill="#fff"/>
<rect x="240" y="60" width="120" height="50" rx="5" fill="#fff4d6"/><rect x="240" y="150" width="120" height="50" rx="5" fill="#fff"/>
<rect x="250" y="5" width="100" height="36" rx="18" fill="#d64545"/>
<rect x="400" y="10" width="350" height="30" rx="4" fill="#fff"/><rect x="400" y="46" width="350" height="30" rx="4" fill="#fff"/>
<rect x="400" y="82" width="350" height="30" rx="4" fill="#fff"/><rect x="400" y="118" width="350" height="30" rx="4" fill="#fff"/>
<rect x="400" y="160" width="350" height="44" rx="4" fill="#eef5ea"/>
</g>
<g text-anchor="middle" fill="#1d2329">
<text x="57" y="117">12 V 24 Ah</text><text x="57" y="131">SLA battery</text>
<text x="175" y="124">Main fuse</text>
<text x="300" y="80">40 A main relay</text><text x="300" y="94" font-size="9.5">(e-stop contactor)</text>
<text x="300" y="170">Fuse → XL4015</text><text x="300" y="184" font-size="9.5">12 → 5 V (permanent)</text>
<text x="300" y="27" fill="#fff" font-weight="700">LAY37 e-stop</text>
</g>
<g fill="#1d2329">
<text x="410" y="30">Fuse 15 A → 2 × BTS7960 → drive motors</text>
<text x="410" y="66">Fuse 20 A → BTS7960 → brush · 40 A relay → vacuum</text>
<text x="410" y="102">Fuse 10 A → BTS7960 → linear actuator</text>
<text x="410" y="138">MOSFET → signal tower (12 V)</text>
<text x="410" y="178">Fuse 5 A · 5 V logic: UNO Q, LiDAR, IMU, camera,</text>
<text x="410" y="194">RFID, LCD, sensors (stays on to report faults)</text>
</g>
<g stroke="#22313f" stroke-width="1.5" fill="none" marker-end="url(#a2)">
<path d="M110,120 H133"/><path d="M215,112 L238,90"/><path d="M215,128 L238,170"/>
<path d="M360,78 L398,25"/><path d="M360,82 L398,61"/><path d="M360,86 L398,97"/><path d="M360,90 L398,133"/><path d="M360,175 H398"/>
</g>
<path d="M300,41 V58" stroke="#d64545" stroke-width="2" stroke-dasharray="4 3"/>
<text x="20" y="235" font-size="10" fill="#5d6670">The e-stop (NC) is in series with the main relay coil: pressing it opens the switched 12 V bus to every actuator.</text>
<text x="20" y="251" font-size="10" fill="#5d6670">The e-stop state is also wired to an MCU input for reporting. Restart requires RFID card + start button. Charger at the rear panel.</text>
</svg>
<figcaption>Power distribution and hardware safety chain (fuse values from the WCCA, Chapter 9).</figcaption>
</figure>

## Interface list

| ID | From → To | Type | Specification |
|---|---|---|---|
| I1 | M8 → M2, M3, M4 | Power | Switched 12 V bus through the e-stop relay, one fuse per branch |
| I2 | M8 → M6, M7, M9 | Power | 5 V logic from XL4015 buck converters |
| I3 | M8 → M7 | Safety | E-stop state to an MCU digital input |
| I4 | M7 ↔ M2 | Data | PWM + DIR to BTS7960 drivers; encoder A/B to MCU |
| I5 | M7 ↔ M3 | Data | Brush PWM, vacuum relay on/off, MPX5010DP analog |
| I6 | M7 ↔ M4 | Data | Actuator PWM + DIR; HX711 clock/data |
| I7 | M7 ↔ M5 | Data | Float switches (tank level, shut-off) to digital inputs |
| I8 | M7 ↔ M6 | Data | LiDAR and webcam USB (Linux); IMU I2C; bumpers digital |
| I9 | M7 ↔ M9 | Data | RFID SPI, start button, LCD I2C, tower via MOSFETs; web UI over Wi-Fi |
| I10 | M3 → M4 | Fluid | Oil-resistant hose: lubricant + chips mixture |
| I11 | M4 → M5 | Fluid | Liquid by gravity; compactor drain to the tank |
| I12 | M5 → M3 | Air | Vacuum port with float shut-off to the vacuum motor |
| I13 | M1 ↔ all | Mechanical | 2040 T-slot rails, M5 T-nuts; each module removable on its own |

## Control and software architecture

The Arduino UNO Q splits the work between its real-time MCU and its Linux processor, linked by the Arduino Bridge
(RPC). The split follows lesson 1 of the team's previous robot: **split by timing requirement, not by complexity.**

| Domain | Runs | Responsibilities | Must never |
|---|---|---|---|
| **STM32U585 MCU** (Zephyr + Arduino core) | Real time, deterministic loops | Motor PWM + encoder speed loops; brush/vacuum/compactor sequencing; floats, MPX5010DP, HX711, bumpers, e-stop state, battery voltage; stall/current cut; watchdog: stop all motion if no valid command within T_stale; execute one motion order autonomously and stop by itself | Wait on Linux to stop; allocate memory dynamically in control loops; block > 1 ms in an interrupt |
| **QRB2210 MPU** (Debian, Python) | Best effort | LiDAR mapping and localization against the saved map; coverage route; vision task; web UI (calibration, routes, status); RFID check; raw logging ≈ 20 Hz; replay | Command actuators directly; assume real-time timing; use wall-clock time for intervals (use `time.monotonic()`) |
| **Hardware** | Always | E-stop opens the 40 A main relay coil (actuators lose power, logic stays on); fuses per branch; float shut-off at the vacuum port; slipping brush belt | Depend on software |

### Command protocol (Bridge RPC, proposed)

- Linux → MCU: `move(segment_id, v, distance_mm | heading_deg, timeout_ms)`, `set_tool(brush, vacuum)`,
  `compact(max_force_n)`, `stop()`, heartbeat every 100 ms.
- MCU → Linux: `status(state, segment_id, odom, faults[], sensors{})` at 20 Hz; `done(segment_id, reason)`.
- The MCU stops if: heartbeat lost > 300 ms (T_stale, to be tuned with the measured RPC latency), bumper, e-stop,
  fault, segment complete or obstacle flag from Linux. Every stop reason is logged.
- The protocol is versioned (`proto_version`) and mismatches are rejected at start.

### Operating states

<figure>
<svg viewBox="0 0 760 175" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif" font-size="11">
<defs><marker id="a3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#22313f"/></marker></defs>
<g stroke="#22313f" stroke-width="1.2">
<rect x="5" y="40" width="90" height="36" rx="18" fill="#e6e9ee"/><rect x="150" y="40" width="100" height="36" rx="18" fill="#fff4d6"/>
<rect x="310" y="40" width="100" height="36" rx="18" fill="#d9f0dd"/><rect x="470" y="40" width="110" height="36" rx="18" fill="#fff4d6"/>
<rect x="640" y="40" width="115" height="36" rx="18" fill="#dcebf7"/>
<rect x="310" y="120" width="100" height="34" rx="17" fill="#fff4d6"/><rect x="5" y="120" width="160" height="34" rx="17" fill="#f6d2cf"/>
</g>
<g text-anchor="middle" fill="#1d2329">
<text x="50" y="62">Idle</text><text x="200" y="62">Authorized</text><text x="360" y="62">Running</text>
<text x="525" y="62">Compacting</text><text x="697" y="62">Ready to empty</text>
<text x="360" y="141">Paused</text><text x="85" y="141">Fault / E-stop</text>
</g>
<g stroke="#22313f" stroke-width="1.4" fill="none" marker-end="url(#a3)">
<path d="M95,58 H148"/><path d="M250,58 H308"/><path d="M410,58 H468"/><path d="M580,58 H638"/>
<path d="M350,76 V118"/><path d="M372,118 V78"/><path d="M50,118 V78"/>
</g>
<g font-size="9.5" fill="#5d6670" text-anchor="middle">
<text x="121" y="50">RFID card</text><text x="279" y="50">start button</text><text x="439" y="34">tank/basket full</text><text x="439" y="46">or route done</text>
<text x="609" y="50">done</text><text x="315" y="100">obstacle /</text><text x="315" y="111">bumper</text><text x="405" y="100">clear</text>
<text x="130" y="100">deliberate restart (card + button)</text><text x="200" y="170">from any state: e-stop or fault</text>
</g>
</svg>
<figcaption>Operating state machine. No automatic restart after a fault or e-stop (ISO 3691-4 4.1.14, SR-014).</figcaption>
</figure>

### Sensor roles and hierarchy

Every sensor has a written role, and only one sensor is the authority for each quantity (lesson 6). Draft, to be
confirmed with tests.

| Quantity | Authority | Support | Notes |
|---|---|---|---|
| Collision / contact | Bumpers (hard stop on MCU) | LiDAR stop zone | Bumper never overridden |
| Obstacles ahead | LiDAR | — | Reflective metal: validate with field logs |
| Pose | Encoders + IMU (MCU) | LiDAR scan match (Linux) re-anchors | Lessons 2–3 |
| Heading | IMU (BNO055 IMU mode, no magnetometer) | Encoders | Magnetometer unreliable near steel |
| Tank level | Float switches (majority filter) | Camera cross-check (SR-016, warning only) | Float shut-off is hardware |
| Suction / blockage | MPX5010DP | Vacuum current (ACS712, optional) | Thresholds from measured readings |
| Compactor force | Load cell + HX711 | Actuator current | ≤ 100 kgf |
| Battery | Voltage divider (INA226 optional) | — | Cut-off ≈ 50 % DoD |
| Residue on cleaned strip | Camera (log-only until SR-015 passes) | Operator inspection | Only adds a re-pass; never stops, steers or blocks (ADR-0006) |

### Filtering rules for every sensor

- **One bad reading never changes state alone:** minimum of 3 readings, confirm jumps on 2 consecutive reads, capped
  vote counters (majority filter with hysteresis). Applies to floats, pressure, bumpers, level and RFID.
- **Thresholds at the midpoint between two measured real readings**, never from CAD or a datasheet alone.
- **Log every run raw** (≈ 20 Hz readings + every decision) for replay in the simulator.

### Proposed firmware layout

```
firmware/mcu/
  config.h          all constants with units and the measurement that justifies each threshold
  safety.*          stop conditions evaluated every cycle (cannot be disabled at runtime)
  motion.*          segment executor: runs one order and stops by itself
  tools.*           brush / vacuum / compactor sequencing with interlocks
  sensors.*         floats, MPX5010DP, HX711, bumpers, battery — min-of-3 + 2-read confirm + capped votes
  bridge.*          RPC protocol (versioned), heartbeat, T_stale
  main.*            fixed-period loop, watchdog fed only when all checks pass
```

## Sensor shopping priority

| Priority | Items |
|---|---|
| Must | MPX5010DP, 3 floats, 6 limit switches (4 bumpers + 2 lid interlock), 50 kg load cell + HX711, battery voltage divider, RPLIDAR A1M8 (buy last, reserve early) |
| Should | BNO055, RC522, INA219/INA226, ACS712 (vacuum), 2 × DS18B20 |
| Nice | Webcam + LED, 2 × VL53L0X downward (drains/edges), capacitive level, IR reflectance (residual film) |

Encoders come with the JGB37 motors; the BTS7960 has current sense.
