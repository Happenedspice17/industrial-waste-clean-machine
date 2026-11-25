# Test protocol — TP-S02 Suction rig: brush + degreaser + wet trap

Status: **protocol written 2026-11-25, not run**. Acceptance criteria below are fixed before testing.
Refs: SR-001, SR-005, SR-022, SR-023, SR-024, SR-025 · ADR-0004 (A vs B) · ADR-0008 (dose, product) · DFMEA F-001,
F-004, F-010–F-012 · SCCAF SC-001 · follows TP-S01.

## Wet trap ("adapter"): the vacuum never sucks liquid directly
Same principle as the robot's sealed chamber (wet-vac): the vacuum pulls air from a sealed jar; liquid and chips
drop out inside the jar.

```
floor nozzle ──clear hose──▶ INLET (lid) ── tube ends at mid-height, aimed at the wall
                                   │
                         sealed rigid jar 3–4 L  ── mesh basket inside (chips, like M4)
                                   │
           OUTLET (lid) ◀── sponge/mesh demister ◀── ball float cage (closes outlet if level rises)
                                   │
                         printed PETG sleeve ──▶ vacuum inlet (X200 or wet/dry vacuum)
                         tee on the outlet line ──▶ MPX5010DP or water U-tube (vacuum at the trap)
```

- Jar: rigid HDPE or a paint bucket with a gasketed lid (thin PET bottles collapse under vacuum).
- Ports: two tight cable glands or bulkhead fittings for the hoses; silicone sealant only outside the wet zone.
- Float: a ping-pong ball in a printed cage under the outlet seals it before liquid reaches the vacuum (same idea as
  SR-008, F-002).
- Sleeve: PETG, printed after measuring the vacuum inlet (rule 8). **To measure (caliper):** X200 inlet outer and
  inner diameter and usable length, hose inner/outer diameter, jar lid thickness and port positions.
- The trap is weighed empty, before and after each run → liquid and solids recovered by mass (SR-001).
- Expect less air flow than with the bare nozzle; the vacuum reading at the trap records it.
- Preferred vacuum for the rig: the BOM wet/dry unit (Mikels AA-12) or another wet/dry candidate; the X200 (dry
  type) only behind the trap, and only for comparison.

## Acceptance criteria (fixed before the test)
| Part | Requirement | Pass |
|---|---|---|
| A Liquid recovery | SR-001 | ≥ 85 % of spilled liquid mass in the trap, mean of 5 runs, 1 m² patch, one pass |
| B Chips | ADR-0004 | Option A only if chip pickup ≥ 85 % by mass and 0 clogs in 10 runs; else option B (front hopper) |
| C Dose | SR-022 | Dose within ± 25 % of target over 5 runs; pump off ≤ 1 s after stop in 10 of 10 trials (when the pump is on the rig) |
| D Foam | SR-023 | 0 foam at the trap outlet and 0 early float closures in 5 fills with the selected product |
| E Slip | SR-024 | Friction ≥ 0.9 × clean dry floor on 5 strips; no standing liquid 1 min after the pass |
| F Product | SR-025 | SDS on file, not flammable, low-foam, quick-break, silicone-free |
| G Braking input | SR-005 | Friction on the soapy film measured and used to recompute stopping distance (no μ assumed) |

## Setup
- Floor: same tile/concrete as the plant target, 1 m² taped patch; photos from a fixed tripod, same light.
- Lubricant: reference lubricant if available (open decision 2), else TP-S01 simulant; weighed volume.
- Chips: real steel chips from a machining shop (mass, length, shape recorded) + the TP-S01 coins as a repeatable
  reference.
- Brush: the M3 nylon brush driven by the 775 motor (or a drill at a recorded rpm); rubber squeegee behind it.
- Solution: candidate product per SR-025 at the supplier dilution; TP-S01 home mix only as a baseline.

## Procedure (5 runs per case)
1. Dry: brush + squeegee + suction (answers option 0 of ADR-0008).
2. Solution at 10, 20 and 40 mL/m² (spray bottle or pump, tank weighed): brush + squeegee + suction.
3. Per run: weigh patch inputs, trap before/after, basket; count/weigh chips left; vacuum reading; foam height in
   the trap; time; photos before/after.
4. Slip (E/G): drag sled or inclined plane on clean dry floor, oily floor and cleaned strip.
5. Clogging (B): 10 runs with long chips.
6. Log raw values in a sheet (one row per run) and attach it; compute mean, min, max, n.

## Results
Not run.
