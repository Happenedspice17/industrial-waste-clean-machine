# ADR-0010: Ultrasonic level sensors for the liquid tank and the chip basket

- Status: proposed (owner choice 2026-11-22; sensor changed to HC-SR04 at the owner's request, cheapest option)
- Date: 2026-11-22
- Requirements affected: SR-022, SR-016 (replaced as the level source), SR-008 (float shut-off unchanged), SR-023

## Context
ADR-0007 removed the camera container check. The robot needs a continuous fill level to decide when to return home
(SR-023). Floats give only discrete states and stay th## Options considered
| Option | Price (estimate, to quote) | For | Against |
|---|---|---|---|
| **A. HC-SR04 (chosen)** | ≈ MXN 30–60 each | Cheapest, everywhere in student projects, 2 cm blind zone, 3 mm resolution | Open transducers foul with oil mist; 5 V echo needs a divider; 15° cone echoes off tank walls; not waterproof |
| B. DFRobot A02YYUW | ≈ MXN 350–500 each | Sealed probe, UART, 3.3 V | ≈ 10× the price |
| C. JSN-SR04T | ≈ MXN 150–250 each | Waterproof | ≈ 20–25 cm blind zone, too large for a 20 L tank (deduced) |
| D. Load cell under each container | — | Mass, no fouling | Mechanics under the separation module |

## Decision
1. One HC-SR04 above the tank fill zone and one above the chip basket, powered from 5 V; TRIG from a 3.3 V GPIO;
   ECHO through a 15 kΩ / 22 kΩ divider (WCCA `hcsr04_echo`: 2.65–3.15 V worst case, margin 4.6 % to 3.3 V, WARN
   accepted until the UNO Q pin tolerance is checked). Sensors triggered alternately ≥ 60 ms apart (no crosstalk).
2. Fouling control: transducers face down through a short PVC sleeve above the maximum level, outside the inlet
   splash, with a removable splash cap; wipe check in the daily start; a reading stuck for > 60 s with the vacuum
   running is flagged (to add after TP-L01 shows the failure signature).
3. MCU (`firmware/mcu/level.{h,cpp}`): echo time → mm with temperature compensation (DS18B20 already in the BOM),
   echo timeout → no reading, readings outside the valid window discarded, median of 3, state change confirmed on 2
   consecutive reads with a capped counter, hysteresis out of FULL, FAULT after 500 ms without a valid reading
   (rules 5, 6). Empty/full readings measured on the robot; thresholds 40 % / 80 % (release 70 %) are estimates.
4. Linux returns home on FULL (or FAULT: finish the current segment, go home); the float shut-off is never bypassed.

## Consequences
Two GPIO pairs instead of two UARTs. Oil mist is the main risk (DFMEA F-016, occurrence raised); if TP-L01 shows
fouling, move to option B on the tank only. Python mirror `sim/level_model.py` shares test vectors with the firmware
(`tests/test_level.py`).

## Evidence
Host build of the firmware conversion and filter, and its Python mirror (tests pass). No sensor bought or measured.
