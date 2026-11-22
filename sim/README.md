# Simulation

Simulation is never physical evidence: label results "simulation" with seeds and number of scenarios.

| Folder | Purpose | Status |
|---|---|---|
| `coverage/` | Boustrophedon coverage of a plant cell | Semester-1 result (12 × 8 m, 3 machines): 96 %, 25.6 min, 167 m²/h, 68 Wh/cycle — code to be ported here |
| `sensors/` | Noisy sensor models: LiDAR dropouts on reflective metal, float bounce, pressure noise, RPC delay, clock jumps | Planned — must reproduce failures seen in field logs (lesson 9) |
| `replay/` | Run a field log through the decision code as a regression test (lesson 10) | Planned |

The AprilTag pose simulation (synthetic tag images) is reported in
[TP-V02](../docs/test-reports/TP-V02-apriltag-localization.md).
