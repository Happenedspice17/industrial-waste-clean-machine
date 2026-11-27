# Test report — TP-S01 Handheld suction pre-test (suction only, with and without degreaser)

Status: **measured 2026-11-24, exploratory**. Not the suction rig of ADR-0004 and not the robot's vacuum.
Refs: SR-001 · SR-002 (context) · ADR-0004 · DFMEA F-001, F-002 · SCCAF SC-001

- Date: 2026-11-24 · Operator: María Ruiz Mejía · Home setup (not the UP lab) · No firmware involved.
- Source: test log by the operator, in Spanish, `evidence/TP-S01/Bitacora_Pruebas_Modulo_Succion_2026-11-24.pdf`
  (photos re-encoded as JPEG q85 to stay under the 5 MB repo limit; original 5,949,909 bytes,
  SHA-256 `8bb196f5773981e46691dcfbfc33429aa48c36330d9a2fb2b4f733791ee1eeb8`, kept by the team).
  Photos extracted to `evidence/TP-S01/01–09_*.jpg`; vacuum listing `00_vacuum_fanttik_x200_listing.jpg`.

## Purpose
Check whether suction alone (no brush, no rollers, no squeegee) removes an oily film, an oil–dust sludge and heavy
flat "chips", and whether a degreasing solution changes the result.

## Acceptance criteria
Not fixed before testing (exploratory). For reference only, the results are compared afterwards with the ADR-0004
criterion for option A (chip pickup ≥ 85 %). SR-001 (≥ 85 % liquid **mass** recovered) cannot be evaluated: no
mass was weighed.

## Setup
| Item | Value | Source |
|---|---|---|
| Vacuum | Fanttik X200 handheld cordless (dry type), direct nozzle, no brush, no squeegee | operator; listing photo |
| Vacuum rating | 16 kPa static, 40 AW | **seller data, not measured** |
| Oil simulant | 70 % cooking oil + 30 % liquid paraffin (vaselina líquida) | operator |
| Viscosity | claimed equivalent to ISO VG 150–320 | **not measured** (deduced by operator) |
| Dust | fine particulate mixed into the oil to form sludge | operator; type and amount not recorded |
| "Chips" | 5 Mexican coins: 1 × $0.50 (3.103 g), 2 × $1 (3.95 g), 1 × $2 (5.19 g), 1 × $5 (7.07 g) = 23.263 g | official masses, **not weighed** |
| Degreaser (test 4) | 300 mL water + 5 mL dish soap + 5 g baking soda | operator, photo `01_solution_prep.jpg` |
| Not recorded | floor type, patch area, oil volume, passes per test, nozzle height/speed, temperature, battery level | — |

## Results (measured 2026-11-24, visual comparison of before/after photos)
The source log numbers the tests inconsistently (table: 1, 3, 4, 5; sections: 1, 2, 3, 5; text says both "4" and
"5" tests). Four tests were run; they are renumbered T1–T4 here.

| ID | Source label | Floor | Agent | Liquid film | Coins lifted | Photos |
|---|---|---|---|---|---|---|
| T1 | Prueba 1 | oil | none | no visible change | — | 02, 03 |
| T2 | Prueba 2 / 3 | oil + dust | none | no visible change | — | 04, 05 |
| T3 | Prueba 3 / 4 | oil + dust + 5 coins | none | no visible change | 0 of 5 | 06, 07 |
| T4 | Prueba 5 | oil + dust + 5 coins | degreaser | ≈ 85–90 % of the film gone (visual estimate), light wet film left | 2 of 5: $1 (3.95 g) + $0.50 (3.103 g) | 08, 09 |

T4 coins: 40 % by count, 7.053 / 23.263 g = **30.3 % by mass** (arithmetic checked). The heavier coins ($2, $5 and
the second $1) stayed in place. The T1 "after" photo has a different framing and light than the "before" photo, so
T1 is weak evidence.

## Verdict
| Item | Verdict |
|---|---|
| SR-001 liquid recovery ≥ 85 % by mass | NOT EVALUATED (no mass measured) |
| ADR-0004 option A, chip pickup ≥ 85 % — suction only | FAIL for this vacuum: 0 % dry, 30 % by mass with degreaser |
| Robot concept (brush + squeegee + wet/dry vacuum) | NOT TESTED — brush and squeegee were absent |

## What it shows and what it does not
- Shows: with this vacuum and no agitation, suction does not detach a viscous film nor lift flat 3–7 g pieces sealed
  to the floor by oil. A wetting agent breaks the film and frees the lightest pieces. This supports the brush that
  the design already has (M3) and the ADR-0004 concern (F-001).
- Does not show: the performance of the BOM vacuum (Mikels AA-12, 80 W wet/dry), of the brush + squeegee concept, or
  of real chips. Coins are flat discs (worst case for the oil seal); real chips are curled, have edges and usually
  weigh less per piece (deduced). Kitchen oil + paraffin is not a machining lubricant.

## Design observations → decided in [ADR-0008](../adr/0008-cleaning-agent-dosing.md) (2026-11-25)
1. **Degreaser conflicts with a core principle.** The concept recovers lubricant *without water or chemicals* so
   the liquid stream stays oil (presentation slides 2 and 5; water/steam outlets were discarded as a third waste
   stream, `docs/00-project-context.md`). A water + detergent solution
   would emulsify the oil, add a third stream or dilute the liquid stream (M2 purity ≥ 95 %), add a clean-water tank
   and dosing (mass, power, BOM) and may change the hazardous-waste class (NOM-052-SEMARNAT-2005). Needs an ADR
   with rig data before any change. → **Team decision 2026-11-25: use a low-dose, low-foam, quick-break degreaser
   (ADR-0008); still two waste streams; dose and product from TP-S02.**
2. **Foam.** If any detergent is used, foam can trip the float shut-off early or reach the vacuum motor (F-002).
   Only low-foam agents or an antifoam in the tank → SR-023, DFMEA F-010, SCCAF SC-008.
3. **Do not vacuum liquids with the X200.** It is a dry handheld vacuum; T4 pulled soapy liquid through it
   (risk of motor damage, deduced). For the rig, a wet trap goes between nozzle and vacuum (TP-S02).
4. **Integrating the X200 in the robot is not recommended** (deduced): dry-only, internal battery, small bin, rating
   unverified. It can still serve on the rig as a dry-chip reference if its air flow is measured.

## Follow-ups → protocol [TP-S02](TP-S02-suction-rig-wet-trap.md)
- Use the BOM wet/dry vacuum (or the candidate), with and without the brush, and the squeegee.
- Fix acceptance criteria before testing; weigh oil before/after (SR-001) and chips lifted (g/s, SC-001).
- Real steel chips from a machining shop (mass, length, shape recorded) plus coins as a repeatable reference.
- Record floor type, area, volume, passes, speed, nozzle height, vacuum current and pressure (MPX5010DP).
- Same camera position and light for before/after photos; 5 runs per case.
