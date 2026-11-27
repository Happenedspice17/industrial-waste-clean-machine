# Scenario analysis

The concept was evaluated in two scenarios that bound the external conditions the team does not control: an
idealist scenario and a pessimist one. Ten protection terms that keep the robot from damaging itself apply in both
scenarios, three metrics measure the main function, and the expected performance is summarized per scenario. Source:
*Scenario Analysis* deliverable and the improved proposal.

## External conditions of use

| # | Idealist scenario | Pessimist scenario |
|:-:|---|---|
| 1 | Sealed, flat concrete floor with no ramps, drains or cracks | Uneven floor with ramps, drains, joints and cracks; wet patches of coolant |
| 2 | Thin film of low-viscosity lubricant at room temperature | Thick grease, high-viscosity or cold oil, water-based coolant emulsions |
| 3 | Short ferrous machining chips (steel, cast iron) | Long, stringy or non-ferrous chips (aluminum, brass) and foreign objects (rags, gloves, bolts) |
| 4 | Shift-change window ≥ 30 min, area clear of people and forklifts | Short window (< 15 min); workers and forklifts cross the area |
| 5 | Aisles and machines match the stored map | Pallets, carts and tools left in aisles; layout differs from the map |
| 6 | Uniform lighting, no direct sunlight | Poor or changing light, glare, reflective metal surfaces |
| 7 | Stable Wi-Fi, low electromagnetic noise | No Wi-Fi; strong EMI from welders, VFDs and motors |
| 8 | Ambient 18–30 °C, low dust and mist | Above 35 °C, dust and oil mist near active machines |
| 9 | Battery fully charged; trained operator empties both streams | Spills larger than tank capacity; battery not recharged between shifts |

## Protection terms (both scenarios)

| Term | Design rule | How the robot enforces it |
|---|---|---|
| 1 · Structural safety factor | n ≥ 2 on the full loaded mass; n ≥ 3 at mounts that take bumps | 2040 aluminum frame, steel brackets, PETG parts sized with margin; Shigley static and fatigue checks |
| 2 · Motor and driver current | Run motors well below the 43 A driver rating; stop on stall | BTS7960 current sense read by the MCU; cut after a stall > ≈ 2 s |
| 3 · Overcurrent | One fuse per branch below wire ampacity; main fuse at the battery | Fuses for drive, collection, separation and logic; 14 AWG power wiring |
| 4 · Battery | Avoid deep discharge and wrong charging | Low-voltage cut-off at ≈ 50 % depth of discharge; BR-600 SLA charger only |
| 5 · Thermal and duty cycle | Respect datasheet duty cycles of vacuum and actuator | Timed runs with rest periods; ventilated electronics bay |
| 6 · Ingress | IP54 target for electronics (IEC 60529); IPX4 below the deck because the degreaser solution conducts | Sealed bay above the liquid path; cable glands, sealed connectors, drip loops |
| 7 · Chemical compatibility | Every part touching oil must resist it | PETG, nitrile hose and gaskets, stainless mesh, aluminum; no PLA or natural rubber |
| 8 · Overflow and blockage | Liquid never reaches the vacuum motor; a blocked hose must not overheat it | Float shut-off at the vacuum port, level cut-off; MPX5010DP detects blockage → vacuum off; low-foam agent and inlet baffle against foam (SR-023) |
| 9 · Mechanical overload | Compactor force ≤ 100 kgf of 150 kgf (n = 1.5); brush jams must not break the drive | Load cell + HX711 force limit; brush belt slips as a mechanical fuse |
| 10 · Impact, vibration, runaway | Limit speed; secure everything that can loosen; stop if control is lost | 0.38 m/s max (0.15 m/s cleaning), bumpers, nyloc nuts, thread-locker, strain relief, MCU watchdog on stale commands |
| 11 · Dose and wet floor (added with ADR-0008) | Spray only what the cleaning needs; never leave a slippery floor | Dose limit; pump only while moving with the brush on; squeegee leaves no standing liquid (SR-022, SR-024) |

## Metrics

| Metric | Definition and test | Pass threshold |
|---|---|---|
| M1 · Recovery efficiency | Mass recovered ÷ mass spilled on a 1 m² patch, one pass; tank and basket weighed before and after | ≥ 85 % liquid and ≥ 85 % chips |
| M2 · Stream purity | Solids > 1 mm in the tank (filtered and weighed) and free oil drained from the compacted chips | ≥ 95 % liquid stream, ≥ 90 % solid stream |
| M3 · Autonomous coverage | Area cleaned per hour on a stored route with zero safety incidents | ≥ 100 m²/h, 0 incidents |

## Expected performance by scenario

Engineering estimates, to be replaced by test results.

| | Idealist scenario | Pessimist scenario |
|---|---|---|
| Behavior | Authorized start, stored route repeated with little drift; chips and thin oil collected, separated and stored; cycle ends on time and the tower turns green | Grease only partly lifted; emulsions fill the tank sooner; long or non-ferrous chips tangle or clog the hose (detected, robot pauses); people and pallets cause frequent stops; offline operation without Wi-Fi |
| Protection terms | Present but rarely triggered; loads within the safety factors | Triggered often (jams, blockage, overflow, heat); the robot stays intact. The cost is productivity, not damage |
| M1 recovery | ≈ 90 % liquid, ≈ 95 % chips → **meets** | ≈ 60–75 % liquid, ≈ 70 % chips → below |
| M2 purity | ≥ 95 % / ≥ 90 % → **meets** | ≈ 85 % liquid (fines, emulsions) → below |
| M3 coverage | ≈ 120–150 m²/h, 0 incidents → **meets** | ≈ 40–70 m²/h, 0 incidents → below, **safe** |
| **Overall** | **Fully functional** | **Partially functional and safe** |
| Strengths | Full cycle without help; separation at the source; repeatable route; quick emptying | Protections stop the robot before it breaks; faults detected and reported; works offline |
| Weaknesses | Vacuum power, battery and tank capacity limit the area per cycle; compaction adds time | Grease and non-ferrous chips; hose clogging; reduced coverage; LiDAR and camera glare |

## Reading

The scenario analysis shows that the design's protection terms turn the pessimist scenario into a productivity
problem, not a safety problem: in every pessimist condition the expected result is "below, but safe" with zero
incidents. The idealist scenario meets all three metrics on paper. The decisive uncertainty is the same in both
columns: whether the 80 W vacuum lifts steel chips. That is why the first test of next semester is the suction rig,
not the robot.
