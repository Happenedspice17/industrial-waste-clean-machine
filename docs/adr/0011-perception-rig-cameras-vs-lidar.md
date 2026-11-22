# ADR-0011: Perception rig — two cameras + low-cost ranging instead of a 360° LiDAR (for now)

- Status: proposed (owner question 2026-11-22: "4 cameras or 1 LiDAR + 1 camera? the 360° LiDAR is expensive")
- Date: 2026-11-22
- Requirements affected: SR-018, SR-019, SR-020, SR-024, SR-005, R7 · ADR-0001, ADR-0002, ADR-0007, ADR-0008

## Context
The design has an RPLIDAR A1M8 for two jobs: (1) **obstacle detection** — "Obstacles ahead: authority LiDAR" and the
LiDAR stop zone in `docs/02-architecture.md` — and (2) **localization** by scan matching. AprilTag stations now give
localization, and the owner wants at least two cameras (front + rear, SR-024). The question is which rig to buy.

**Conflict flagged (CLAUDE.md rules 1 and 11):** dropping the LiDAR removes the current obstacle-detection authority.
Cameras cannot replace it (no reliable range, not a safety sensor, ADR-0006 option C). Whatever replaces it must
measure distance and act on the MCU without Linux.

## Options and evidence
Simulation over the same 20 cells (`docs/sim/plant-sim-20-maps.md`, real `Localizer`, `PoseFusion`, `Docking`).
Costs are **estimates to quote** (Mexican retail, Nov 2026), not checked prices.

| Rig | Pose p95, median of maps | Pose p95, worst map | Frames with a fix | Longest stretch without fix (median / worst) | Obstacle sensing | Hardware cost (estimate) |
|---|---|---|---|---|---|---|
| 1 front camera | 0.081 m | 0.288 m | 26 % | 13.4 / 20.6 m | none | ≈ 300–450 |
| **2 cameras front + rear** | **0.058 m** | **0.211 m** | 47 % | 7.9 / 10.9 m | none | ≈ 600–900 |
| 4 cameras | 0.036 m | 0.096 m | 78 % | 7.1 / 9.9 m | none | ≈ 1,200–1,800 + powered hub ≈ 400 |
| LiDAR + 1 camera | 0.033 m | 0.034 m | 26 % tags + scan match | 0.4 / 0.6 m | 360° range, 0.15–12 m | ≈ 2,300–2,900 |

All rigs: 0 person contacts, 0 machine hits, 38/38 dockings, coverage 83 % (coverage is limited by the route model,
not by localization). The LiDAR model is **optimistic** (Gaussian 3 cm / 0.5°, 10 % failures, no symmetric-cell
aliasing or reflective-metal dropouts).

Other factors (deduced, to measure):
- **Compute and USB:** the UNO Q has one USB-C port; 4 USB cameras need a powered hub and four decode + AprilTag +
  person-detection pipelines on a 4-core Cortex-A53 with 2 GB. Two cameras are within reach; four need a frame-rate
  budget measured on the QRB2210 (lesson 12) and a WCCA of the hub supply.
- **Obstacles:** 4 cameras still see no distance. A ring of low-cost ranging sensors read by the MCU gives a real
  stop zone: e.g. 4–6 HC-SR04 (≈ 40 each) or VL53L1X ToF (≈ 150 each; check glare on shiny metal). Bumpers stay.
- **Privacy:** every extra camera is more people in view (ADR-0009); the LiDAR sees no faces.

## Decision (proposed)
1. **Next build: 2 cameras (front + rear) for AprilTags and caution + a low-cost ranging ring on the MCU for the
   obstacle stop zone + bumpers.** No 360° LiDAR for now: two cameras with tag pairs give ≈ 6 cm p95 in simulation,
   enough for 0.35 m lanes with 5 cm overlap only if TP-V02 confirms it.
2. The ranging ring becomes the obstacle authority on the MCU (stop and slow zones, min-of-3, 2-read confirm,
   thresholds from measured readings). It needs its own SR, WCCA (5 V echo dividers, 6 more GPIO pairs), DFMEA and
   ISO 3691-4 check before it replaces the LiDAR in the sensor hierarchy. Until then the hierarchy is unchanged.
3. **Do not buy 4 cameras yet:** better localization than 2 (3.6 vs 5.8 cm), but ≈ 2× cost, much more CPU and USB
   load, more privacy exposure, and still no obstacle range. Revisit if TP-V02 shows 2 cameras miss the limits.
4. **Keep a LiDAR mount and cable path** in the chassis (520 mm height already planned). Buy the LiDAR if: TP-V02
   fails with 2 cameras, the ranging ring fails the obstacle tests (reflective metal, chairs, thin legs), or the
   customer requires a 360° stop zone.

## Consequences
Saves ≈ MXN 1,500–2,000 against the LiDAR rig (estimate). Localization depends on keeping tags clean and in place
(F-010, F-011); between stations the robot relies on odometry + IMU (≈ 8–11 m without a fix). The obstacle function
must be re-specified and re-verified (definition of done: SR + DFMEA + ISO + WCCA + test).

## Evidence
Simulation only (`sim/plant_sim.py --rig {front,front_rear,quad,lidar_front}`), 20 maps each, seed 0. No hardware
bought or measured.
