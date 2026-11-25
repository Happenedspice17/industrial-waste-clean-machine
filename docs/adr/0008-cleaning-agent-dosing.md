# ADR-0008: Low-dose, low-foam degreaser sprayed ahead of the brush

- Status: **accepted** (team decision 2026-11-25; dose and product set by TP-S02)
- Date: 2026-11-25
- Requirements affected: SR-001, SR-002, SR-003, SR-005, SR-008 · new SR-022–SR-025 · supersedes the "no water or
  chemicals" principle of the semester-1 deliverables (brief draft 6, presentation v1–v3)

## Context
TP-S01 (measured 2026-11-24, exploratory, handheld vacuum, no brush): dry suction left the oil film and oil–dust
sludge unchanged and lifted 0 of 5 coins; after a water + dish soap + baking soda solution the film was mostly
removed (visual estimate 85–90 %) and 2 of 5 coins (30 % by mass) were lifted. The semester-1 concept assumed oil only
(no water or chemicals) to keep the liquid stream undiluted and avoid a third waste stream.

## Options considered
| Option | For | Against |
|---|---|---|
| 0 Dry: brush + vacuum only | Oil stream undiluted, simplest | Brush + dry suction untested on viscous film; TP-S01 shows suction alone fails |
| 1 Flood with water + detergent (scrubber style, ≈ 60 mL/m², deduced from commercial scrubbers) | Proven in scrubbers | Large tank and mass, lots of oily water, foam, wet slippery floor |
| 2 **Low-dose spray (≈ 20 mL/m², estimate) of a low-foam, quick-break alkaline degreaser ahead of the brush** | Breaks the film and the oil seal under chips with little water; quick-break lets oil separate in the tank | Liquid stream becomes oil + water; adds tank, pump, nozzles and a consumable |
| 3 Solvent degreaser | No water | Flammable/VOC exposure (NOM-010-STPS), not acceptable near people |

## Decision
Option 2. A 5 L clean-solution tank, a 12 V diaphragm pump and a spray bar (2 flat-fan nozzles) wet the strip just
ahead of the brush; brush → squeegee → nozzle → sealed chamber stay as designed. Product requirements (SR-025):
low-foam, quick-break (demulsifying), silicone-free, water-based, SDS per NOM-018-STPS-2015, no flammable solvent.
Pump runs only while the robot is moving in cleaning mode and the brush runs; it is fed from the e-stop-switched
12 V bus, so the e-stop stops it in hardware (rule 1).

## Consequences
- **Still two waste streams.** The clean-solution tank is a supply, not a waste stream. Liquid stream = oil + spent
  solution in the 20 L tank; chips stream unchanged. With a quick-break product the oil floats and can be decanted;
  the water phase is oily wastewater for an authorized handler (NOM-052-SEMARNAT-2005). The claim "oil recovered
  undiluted" is withdrawn.
- **Foam** can reach the vacuum port or trip the float early → low-foam product, baffle at the chamber inlet,
  silicone-free antifoam in the tank as backup, float shut-off unchanged (SR-008, SR-023, F-010).
- **Wet floor after the pass** is a slip hazard (NOM-001-STPS-2008 7.4 b) → squeegee recovers the strip, dose limited,
  residual-film check (SR-024, F-011). Braking on a soapy film (SR-005) must be measured, not assumed μ = 0.1 (F-004).
- **Conductive liquid** (oil was insulating) → IP54 electronics bay kept, IPX4 splash target for parts below the
  deck, drip loops, sealed connectors (F-014).
- **Wet chips** may rust in the basket → product with corrosion inhibitor, empty basket every shift (F-015).
- **Worker exposure** at refill → PPE and SDS at the station (PFMEA P-001, NOM-010/017/018-STPS).
- Cost, mass and energy (estimates, not quoted): hardware ≈ MXN 1,000; +≈ 5.5 kg full; +≈ 5 W average → 165 W,
  ≈ 52 min per charge; ≈ 1.4 L solution per 12 × 8 m cycle (5 L tank ≈ 3 cycles); concentrate ≈ MXN 2,500/yr and
  extra oily-water disposal ≈ MXN 7,700/yr (`tools/econ.py`, scenario `degreaser`).
- Test rig: the vacuum must never ingest liquid directly → wet trap between nozzle and vacuum (TP-S02).

## Evidence (tests, calculations, sources)
- TP-S01 (measured 2026-11-24, exploratory). Dose, concentration, foam and slip numbers above are estimates until
  TP-S02 measures them. `python tools/econ.py` for the economics.
