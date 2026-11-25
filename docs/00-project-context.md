# 00 · Project context (single source of truth for project facts)

Last consolidated: 2026-11-25 (ADR-0008 cleaning agent; first physical pre-test TP-S01). Source: team deliverables Sep–Nov 2026 (proposal, brief draft 6, pairwise
matrices, conceptual design, design of models, scenario analysis, Activity 06, final presentation).
Anything not in a deliverable is marked "(deduced)".

## 1. Problem and need

- Machining shops, foundries and metal-forming lines accumulate oil, grease, coolant and metal chips on floors.
  Cleaning during production is unsafe, so contamination stays until a stoppage.
- Evidence used: Liberty Mutual 2023 WSI Manufacturing — falls on same level USD 1.20 B/yr, 14.4 % of USD 8.32 B,
  2nd most costly cause. NSC/BLS — 264,920 same-level-fall cases with days away from work (2023–2024) and 134 deaths
  (2024). STPS/IMSS — 290,527 work accidents and 340 deaths in Mexico, 2023. Manufacturing ≈ 20 % of Mexico GDP.
  OSHA/NIOSH — metalworking fluids → dermatitis, respiratory disease. NOM-001-STPS-2008 7.4 b: liquids on floors must
  not be a slip/fall hazard.
- Gap (bounded claim): in the literature and patents reviewed (US2007271004A1, CN112641396A, CN114129101A,
  CN115319717A, EP2808668A1) no system combines autonomous floor collection with on-board separation of liquid and
  ferrous fractions into independent containers. Commercial autonomous scrubbers (Kärcher KIRA B 50 ≈ MXN 2.0 M;
  Tennant T380AMR ≈ USD 75,000) clean with water and do not separate waste.

## 2. Hypothesis and objectives

**Hypothesis.** A differential-drive oil-compatible platform with low-dose degreaser spray + brush + squeegee →
vacuum nozzle → sealed
separation chamber (mesh basket, neodymium magnets, force-limited compactor) → independent liquid tank, controlled by
UNO Q with LiDAR/IMU/encoder localization and a hardware e-stop, will on a controlled floor with reference lubricant
and ferrous chips meet M1, M2 and M3. Rejected per function if its metric fails under idealist conditions.

**General objective.** Develop and validate a compact autonomous mobile prototype that collects lubricant and metal
chips during shift changes, separates the ferrous fraction and coarse solids, compacts and drains the solids, and
stores both streams separately, with safe mobility, route mapping, a defined vision function and authorized
operation, controlled by an Arduino UNO Q.

| ID | Specific objective | Indicator / target | Req. |
|---|---|---|---|
| OE1 | Collection system (degreaser dosing, brush, squeegee, nozzle, hose, vacuum + sensor) | M1 ≥ 85 %; dry, non-slip floor after pass | R1 |
| OE2 | Separation: mesh filter, magnets → basket, force-limited compactor | M2 solids ≥ 90 %, force ≤ 100 kgf | R2, R3 |
| OE3 | Separate storage, drain valve, leak tray, level cut-off | no mixing, no leaks, cut-off before overflow; M2 liquid ≥ 95 % | R9, R5 |
| OE4 | Oil-compatible diff-drive, encoders + IMU + LiDAR, routes, vision | speed ≤ 0.38 m/s, M3 ≥ 100 m²/h | R4, R6, R7, R8 |
| OE5 | UNO Q architecture, RFID + start button, indicators, relay e-stop | authorized start, deliberate restart, e-stop cuts all actuators | R5, R10 |
| OE6 | Validation protocol with acceptance criteria fixed before tests | all indicators recorded with conditions | All |

## 3. Metrics (pass thresholds, team proposal)

| Metric | Definition | Pass |
|---|---|---|
| M1 Recovery | mass recovered ÷ mass spilled on 1 m² patch, one pass (weigh tank and basket) | ≥ 85 % liquid and ≥ 85 % chips |
| M2 Purity | solids > 1 mm in tank; free oil drained from compacted chips | ≥ 95 % liquid stream, ≥ 90 % solid stream |
| M3 Coverage | m²/h on a stored route, zero safety incidents | ≥ 100 m²/h, 0 incidents |

## 4. Stakeholder requirements (importance 1–10, independent score, not a ranking)

| ID | Requirement | Imp. |
|---|---|---|
| R1 | Lubricant suction / collection | 10 |
| R2 | Solid-chip separation | 10 |
| R3 | Compaction system | 6 |
| R4 | Compact size | 2 |
| R5 | Safety system | 6 |
| R6 | Vision system | 6 |
| R7 | Safe mobility | 10 |
| R8 | Route storage and mapping | 6 |
| R9 | Separate solid and liquid containers | 10 |
| R10 | Operating authorization | 4 |

Selection methods used: quality matrix (0/1/3/9, S(j) = Σ importance × relationship) over 22 and 47 components;
pairwise comparison of 22 components (231 pairs, 0 / Cxx:1 / Cxx:2; 143 answered, 88 completed, 47 corrected;
Spearman agreement 0.26 → 0.83). Mandatory items (chassis, controller, e-stop) are kept regardless of score.
Discarded: water/steam outlets and extra-products container (third waste stream; superseded in part by ADR-0008:
low-dose degreaser spray from a supply tank, still two waste streams), line sensor (oil fouls marks),
swerve, separate Wi-Fi/logging modules (UNO Q has them), industrial vibrator, brush-lift motors.

## 5. Architecture — nine modules (≈ 700 × 500 × 450 mm, 520 mm to LiDAR)

| Module | Function | Main components | Listed cost MXN |
|---|---|---|---|
| M1 Chassis | Carries modules | 2040 aluminum profile ×4 m, panels, bumper bar, leak tray | 1,276.00 |
| M2 Mobility | Moves on routes | 2× JGB37-3530 12 V 59 rpm w/ encoder, Talon 124 mm wheels (needs printed 6→12 mm hex hub), 3" caster, 2× BTS7960 | 3,011.00 |
| M3 Collection | Wet + loosen + pick up | 775 motor + belt, nylon brush (HDX), squeegee, printed nozzle, 3/8" oil hose, Mikels AA-12 12 V 80 W wet/dry vacuum, MPX5010DP, BTS7960 · **dosing (ADR-0008):** 5 L solution tank, 12 V diaphragm pump, spray bar with 2 flat-fan nozzles, tubing, MOSFET channel | 1,472.00 + ≈ 1,000 dosing (estimate, not quoted) |
| M4 Separation | Retain solids | stainless strainer basket, 10× neodymium 28×4×2 mm, chip basket, compaction chamber, 12 V 150 kgf 100 mm actuator, 50 kg load cell + HX711, BTS7960 | 1,087.00 |
| M5 Storage | Hold liquid | 20 L container, ½" brass ball valve, 2× float, float shut-off at vacuum port | 369.00 |
| M6 Perception | Localize, detect | RPLIDAR A1M8, BNO055 IMU, USB webcam COM-126, LED light, 4× ME-8108 bumpers | 4,232.00 |
| M7 Control | Compute | Arduino UNO Q 2 GB, perfboards, MOSFETs/level shifting | 1,122.00 |
| M8 Power + safety | Energy + hard stop | 12 V 24 Ah SLA BR-1224, BR-600 charger, 2× XL4015 buck, fuse holders, 2× 40 A relay, LAY37 e-stop | 2,619.00 |
| M9 Operator interface | Authorize, show | RC522 RFID, 22 mm lit button, LCD 20×4 I2C, 12 V signal tower w/ alarm, web UI | 661.50 |
| **Total (32 items)** | | | **15,849.50** listed + ≈ 1,000 dosing = **≈ 16,850** |

Tooling/consumables: 3× PETG 1 kg, T-nuts, hose clamps, 14 AWG duplex, 22 AWG wire, heat-shrink, crimper HER-266
→ total 17,530.50 (≈ 18,530 with dosing). 15 % contingency for unpriced items (oil hose, gaskets, fasteners, LED
light, squeegee, nozzle, leak tray, panels, printed hubs, MOSFET board) → ≈ 20,160 (≈ 21,310 with dosing). Prices checked 8–9 Oct 2026 (UNIT Electronics,
Sandorobotics, Steren, Home Depot MX, AG Electrónica, Mikels, Maquinaria y Control, Electrónica Universal, Abasteo).

**Material flow:** solution tank → pump → spray bar wets the strip → brush + squeegee → nozzle + hose → sealed chamber: mesh basket (coarse) → magnet bars
(ferrous) → chip basket + compactor → compacted chips (removable basket). Liquid → 20 L tank by gravity → drain
valve. Vacuum motor pulls clean air from the sealed chamber + tank (wet-vac principle); float shut-off protects it.
Oil drained during compaction returns to the tank. Liquid stream = oil + spent solution; with a quick-break agent the
oil floats and is decanted, the water phase goes to an authorized handler as oily wastewater (ADR-0008). Still two
waste streams; the solution tank is a supply.

**Interfaces:** I1 switched 12 V bus via e-stop relay, fuse per branch (M8→M2/M3/M4) · I2 5 V logic (M8→M6/M7/M9) ·
I3 e-stop state to MCU input · I4 PWM+DIR to BTS7960, encoder A/B · I5 brush PWM, vacuum relay, MPX5010DP analog ·
I6 actuator PWM+DIR, HX711 · I7 floats to DI · I8 LiDAR + webcam USB (Linux), IMU I2C, bumpers DI · I9 RFID SPI,
button, LCD I2C, tower via MOSFETs, web UI over Wi-Fi · I10 hose M3→M4 · I11 liquid by gravity M4→M5 ·
I12 vacuum port with float shut-off M5→M3 · I13 2040 T-slot rails, M5 T-nuts, each module removable ·
I14 dosing pump MOSFET (MCU gate = motion AND brush) on the e-stop-switched bus, fused 3 A.

**Operating states:** Idle → (RFID card) Authorized → (start button) Running → (tank/basket full or route done)
Compacting → Ready to empty. Paused on obstacle/bumper, resumes when clear. Fault / E-stop from any state →
deliberate restart.

## 6. Protection terms (both scenarios)

1 Structural n ≥ 2 on full loaded mass, n ≥ 3 at bump mounts (Shigley) · 2 Motor/driver current limit, stall cut
> ≈ 2 s · 3 Fuse per branch below wire ampacity, main fuse · 4 Battery low-voltage cut-off ≈ 50 % DoD, SLA charger
only · 5 Thermal/duty cycle timed runs · 6 IP54 electronics bay, IPX4 below the deck — the solution conducts (IEC 60529) · 7 Oil compatibility: PETG, nitrile,
stainless, aluminum; no PLA, no natural rubber · 8 Overflow/blockage: float shut-off, level cut-off, MPX5010DP →
vacuum off; low-foam agent + inlet baffle · 9 Compactor ≤ 100 kgf (load cell), slipping brush belt as mechanical fuse · 10 Speed ≤ 0.38 m/s,
bumpers, nyloc + thread-locker, strain relief, MCU watchdog on stale commands · 11 Dose limit and pump only while moving + brushing; squeegee leaves no standing
liquid (SR-022, SR-024).

## 7. Scenarios

Idealist: sealed flat floor, thin low-viscosity oil, short ferrous chips, ≥ 30 min window, layout matches map,
uniform light, Wi-Fi, 18–30 °C, full battery. Pessimist: ramps/drains/cracks, coolant patches, thick/cold grease,
emulsions, long/non-ferrous chips and foreign objects, < 15 min window with people and forklifts, moved pallets,
glare/reflective metal, no Wi-Fi + EMI, > 35 °C + mist, spills larger than tank, partial charge. Expected: idealist
fully functional (M1 ≈ 90/95 %, M3 ≈ 120–150 m²/h); pessimist partially functional and safe (M1 ≈ 60–75 %,
M3 ≈ 40–70 m²/h). Expected values are estimates.

## 8. Simulations and calculations done (not physical tests)

- Coverage (boustrophedon cells + BFS transits), 12 × 8 m cell, 3 machines: 96 % of 74.5 m² free floor, 25.6 min,
  167 m²/h, 68 Wh/cycle (≈ 2.1 cycles per charge). Assumptions: 0.40 m width, 5 cm overlap, 0.15 m/s, 6 s/turn, 160 W.
  With the dosing pump (165 W): ≈ 70 Wh/cycle, ≈ 2.0 cycles per charge (deduced, scaled from 160 W).
- Power budget ≈ 165 W (vacuum 80, brush ≈ 40, drive ≈ 30, electronics ≈ 12, dosing pump ≈ 5 average) → ≈ 52 min
  (was 160 W → 54–55 min before ADR-0008).
- Dosing (estimate, ADR-0008): 20 mL/m² × 71.5 m² ≈ 1.4 L solution per cycle; 5 L tank ≈ 3 cycles; +≈ 5.5 kg full.
- Top speed π·0.124·59/60 ≈ 0.38 m/s; braking on oil (μ = 0.1) ≤ 7.4 cm from 0.38 m/s. μ on the soapy film is not
  known yet (TP-S02 part G).

## 9. Economics (reference case: 1 robot, 3 shifts, 300 days, 900 cycles/yr)

Parameters: labor MXN 63.40/h (min wage 2026 315.04 × 1.15 × 1.40 burden / 8 h); manual cleaning 3 h/day → robot
needs 1 h/day (2 h/day saved); waste/cycle 1.5 kg chips + 1 L oil; disposal MXN 6/kg (assumption, range 2–10);
absorbent 0.5 kg/cycle at MXN 20/kg; used-oil collection MXN 2/kg; scrap MXN 2.50/kg; electricity MXN 1.347/kWh
(CFE GDMTO Jul 2026); SLA replacement 2/yr; consumables 1,200/yr; maintenance 24 h × 120.
**Current (ADR-0008, `tools/econ.py` scenario `base`):** adds 0.020 L/m² solution (1,287 L/yr), 3 % concentrate at
MXN 65/L (≈ 2,510/yr, estimate), spent solution disposed as hazardous at MXN 6/kg (≈ 7,720/yr), hardware 21,310.
Investment per robot 32,710 (hardware 21,310 + assembly 9,000 + commissioning 2,400). Results: labor saved
38,041/yr; waste benefit 18,047/yr; opex 9,358/yr; **net 46,731/yr; payback 8.4 months; NPV(3 yr, 12 %) 79,529**.
Pessimistic (1 h/day, waste −50 %, opex +30 %, investment +50 %): 15,879/yr, 3.1 yr, **NPV −10,926 (not viable)**.
Most sensitive after hours saved: the dose (40 mL/m² → NPV −24,575), so the dose must be measured (TP-S02).
**Activity 06 (dry concept, scenario `activity06`, kept for reference):** investment 31,560; net 56,968/yr; payback
6.6 months; NPV 105,269; pessimistic NPV 7,928; + NRE share 7,560 → NPV 368. Academic prototype cost ≈ 97,260 (incl. 504 engineering h).
Business model (proposed): robot ≈ MXN 60,000 (45 % margin over 32,700; was 47 % over 31,600), service plan
≈ MXN 1,500/month, customer pays the concentrate (≈ 2,500/yr), customer payback ≈ 1.7 yr (was 1.3 yr), ≈ 1/30 the
price of a commercial autonomous scrubber.

## 10. Standards in scope

See `docs/03-standards-matrix.md`. Core: ISO 3691-4:2023 (4.2 braking, 4.3 speed, 4.8.1 e-stop, 4.8.2 person
detection, 5.2 tests, Annex A zones, Clause 6 information for use) and NOM-001-STPS-2008 (7.1.1 order and
cleanliness, 7.4 a/b floors, 7.1.2 delimitation, 5.2/5.3 records). Also NOM-004/010/011/017/018/026/029/035-STPS,
NOM-052-SEMARNAT-2005 + LGPGIR, ISO 12100, ISO 13849-1, ISO 13850, IEC 60204-1, IEC 60529, ISO 45001.

## 11. Open decisions (must be closed with evidence, record as ADR)

1. **Collection architecture (ADR-0004):** A = brush + vacuum carry liquid and chips; B = brush throws chips into a
   front hopper with magnets, vacuum handles only liquid. Decide with the suction rig (chip lift rate g/s, liquid per
   pass, clogging with long chips). Risk: 80 W automotive vacuum may not lift steel (ρ ≈ 7,850 kg/m³). TP-S01
   (handheld vacuum, no brush): suction alone lifted 0 of 5 coins dry, 2 of 5 (30 % by mass) with degreaser.
   Next: TP-S02 rig with brush, degreaser and a wet trap.
2. Reference lubricant (type, viscosity) and chip samples.
2b. Cleaning agent product, dilution and dose (ADR-0008 accepted; numbers from TP-S02). Optional later: spot dosing
   only where residue is detected, to cut solution use.
3. Mesh aperture, magnet layout, compactor stroke/force path, compaction ratio target.
4. IMU: BNO055 (recommended; fusion on chip, use IMU mode — magnetometer unreliable near steel) vs MPU-6050 (cheap,
   EOL, needs own fusion).
5. LiDAR supply (Sandorobotics out of stock at check), oil hose price, printed wheel hubs.
6. Sensor role hierarchy (write it before coding, lesson 6).
7. Vision (ADR-0006, accepted): residue check (SR-015) + container-level cross-check (SR-016), log-only until TP-V01
   passes (SR-017). Open: camera placement (DFMA) and USB hub power (WCCA).

## 12. Next-semester plan (priorities)

P1 weeks 1–3 suction rig (TP-S02: brush + degreaser dose + wet trap) + A/B decision · P2 weeks 3–7 modules in 4 teams (A chassis+mobility, B separation+storage,
C power+safety+HMI, D control+navigation+vision) · P3 weeks 7–10 integration + map/save/replay route · P4 weeks 10–13
validation M1–M3 + safety tests on oily floor · P5 weeks 13–16 plant pilot, customer interviews, final report.
Stretch: vision task, full SLAM, LiFePO4, coolant emulsions.

## 13. Sensor shopping priority

Must: MPX5010DP, 3 floats, dosing pump + spray nozzles, 6 limit switches (4 bumpers + 2 lid interlock), 50 kg load cell + HX711, battery voltage
divider, RPLIDAR A1M8 (buy last, reserve early). Should: BNO055, RC522, INA219/INA226, ACS712 (vacuum), 2× DS18B20.
Nice: webcam + LED, 2× VL53L0X downward (drains/edges), capacitive level, IR reflectance (residual film).
Encoders come with the JGB37 motors; BTS7960 has current sense.
