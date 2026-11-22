# ADR-0010: Ultrasonic level sensors for the liquid tank and the chip basket

- Status: proposed (owner choice 2026-11-22; sensor model to confirm)
- Date: 2026-11-22
- Requirements affected: SR-022, SR-016 (replaced as the level source), SR-008 (float shut-off unchanged), SR-023

## Context
ADR-0007 removed the camera container check. The robot needs a continuous fill level to decide when to return home
(SR-023). Floats give only discrete states and stay the hardware overfill protection (rule 1).

## Options considered
- **A. DFRobot A02YYUW (chosen, to confirm):** waterproof probe, UART output, 3.3–5 V, small blind zone (≈3 cm, to
  verify), suits oil mist and a closed tank.
- **B. HC-SR04:** cheap, but open transducers foul with oil mist and the 5 V echo needs a divider.
- **C. JSN-SR04T:** waterproof but ≈20–25 cm blind zone, too large for a 20 L tank (deduced).
- **D. Load cell under each container:** accurate mass, but adds mechanics under the separation module.

## Decision
1. One A02YYUW above the tank fill zone and one above the chip basket, each on its own MCU UART, powered at 3.3 V so
   TX is 3.3 V logic (WCCA `ultrasonic_a02yyuw_tx_to_mcu_rx`: margins 0.49 V high / 0.59 V low).
2. MCU (`firmware/mcu/level.{h,cpp}`): frame checksum, readings outside the valid window discarded, median of 3,
   state change confirmed on 2 consecutive reads with a capped counter, hysteresis out of FULL, FAULT after 500 ms
   without a valid reading (rules 6, 5). Empty and full readings are measured on the robot; thresholds 40 % / 80 %
   (release 70 %) are estimates until TP-L01.
3. Linux returns home when either container reads FULL (or FAULT: treat as unknown, finish the current segment and
   go home); the float shut-off is never bypassed.

## Consequences
Two UARTs needed on the STM32U585 (to verify on the UNO Q pinout); price to quote and add to the M5 BOM. Foam, oil
film on the probe and the irregular chip surface may bias readings: TP-L01 measures them. Python mirror
`sim/level_model.py` is used by the simulator; the same vectors are tested on both (`tests/test_level.py`).

## Evidence
Host build of the firmware filter and its Python mirror (tests pass). No sensor bought or measured yet.
