# 02 · Architecture

## Processing split (lesson 1)

| Domain | Runs | Responsibilities | Must never |
|---|---|---|---|
| STM32U585 MCU (Zephyr + Arduino core) | Real time, deterministic loops | Motor PWM + encoder speed loops; brush/vacuum/compactor sequencing; floats, MPX5010DP, HX711, bumpers, e-stop state, battery voltage; stall/current cut; **watchdog: stop all motion if no valid command within T_stale**; execute one motion order autonomously and stop by itself | Wait on Linux to stop; allocate dynamically in control loops; block > 1 ms in ISR |
| QRB2210 MPU (Debian, Python) | Best effort | LiDAR mapping/localization against saved map; coverage route; vision task; web UI (calibration, routes, status); RFID check; raw logging ~20 Hz; replay | Command actuators directly; assume real-time timing; use wall-clock for intervals (use `time.monotonic()`) |
| Hardware | Always | E-stop opens 40 A main relay coil (actuators lose power, logic stays on); fuses per branch; float shut-off at vacuum port; slipping brush belt | Depend on software |

## Command protocol (Bridge RPC) — proposed

- Linux → MCU: `move(segment_id, v, distance_mm | heading_deg, timeout_ms)`, `set_tool(brush, vacuum)`,
  `compact(max_force_n)`, `stop()`, heartbeat every 100 ms.
- MCU → Linux: `status(state, segment_id, odom, faults[], sensors{})` at 20 Hz; `done(segment_id, reason)`.
- MCU stops if: heartbeat lost > 300 ms (T_stale, to be tuned with measured RPC latency), bumper, e-stop, fault,
  segment complete, obstacle flag from Linux. Every stop reason is logged.
- Version the protocol (`proto_version`) and reject mismatches at start.

## States

Idle → Authorized (RFID) → Running (start button) → Compacting (tank/basket full or route done) → Ready to empty.
Paused (obstacle/bumper, auto-resume when clear). Fault/E-stop (any state) → deliberate restart (card + button).

## Sensor roles and hierarchy (lesson 6) — draft, confirm with tests

| Quantity | Authority | Support | Notes |
|---|---|---|---|
| Collision / contact | Bumpers (hard stop on MCU) | LiDAR stop zone | Bumper never overridden |
| Obstacles ahead | LiDAR | — | Reflective metal: validate with field logs |
| Pose | Encoders + IMU (MCU) | LiDAR scan match and AprilTag fixes (single camera, log-only until TP-V02, SR-018) re-anchor | Lesson 2–3; tags never act as obstacle or safety sensor (ADR-0007) |
| Heading | IMU (BNO055 IMU mode, no magnetometer) | Encoders | Magnetometer unreliable near steel |
| Tank level | Float switches (majority filter) | — (camera cross-check SR-016 deferred, ADR-0007) | Float shut-off is hardware |
| Suction / blockage | MPX5010DP | Vacuum current (ACS712, optional) | Thresholds from measured readings |
| Compactor force | Load cell + HX711 | Actuator current | ≤ 100 kgf |
| Battery | Voltage divider (INA226 optional) | — | Cut-off ≈ 50 % DoD |
| Residue on cleaned strip | Operator inspection | — (camera residue check SR-015 deferred, ADR-0007) | One camera is used for AprilTags |

## Safety chain

E-stop (LAY37, NC) in series with main relay coil → switched 12 V bus to M2/M3/M4. E-stop state also wired to an MCU
input for reporting. Logic (5 V) stays powered to report the fault. Restart requires RFID + start button.
