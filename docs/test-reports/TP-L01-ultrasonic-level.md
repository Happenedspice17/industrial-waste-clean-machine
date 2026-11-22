# Test protocol — TP-L01 Ultrasonic container level

Status: written 2026-11-22, **not run**. Refs: SR-022, SR-008 · ADR-0010 · WCCA `hcsr04_echo`, `hcsr04_echo_via_divider_to_mcu`, `mcu_trig_to_hcsr04`.

## Acceptance criteria (fixed before testing)
Level error ≤ 10 % of usable height at 5 fill points (0, 25, 50, 75, 100 %) per container, 3 runs each, with the
reference oil (tank) and real chips (basket); state reported every ≤ 200 ms; FAULT within 0.5 s of unplugging a
sensor; float shut-off still trips at its mark with the sensor fitted.

## Procedure
1. Measure the empty and full readings on the robot (rule 5); write them in `level::Config` with the date.
2. Fill in steps by mass (scale, ±10 g); log raw distance, filtered %, state at 20 Hz (rule 7).
3. Repeat with vacuum running (vibration, foam, oil mist) for ≥ 2 h and log how the reading drifts as the open
   HC-SR04 transducers foul; repeat with the splash cap off and on; measure the echo high level at the divider.
4. Unplug each sensor while running; check FAULT time. Overfill past the float mark; check the hardware shut-off.

## Records
Raw logs (release assets), config values, photos of the mounts, test report, engineering log entry.
