# Simulation

- `coverage/`: boustrophedon coverage of a plant cell (semester-1 result: 96 %, 25.6 min, 167 m²/h, 68 Wh).
- `sensors/`: noisy sensor models (LiDAR dropouts on reflective metal, float bounce, pressure noise, RPC delay,
  clock jumps) — must reproduce failures seen in field logs (lesson 9).
- `replay/`: run a field log through the decision code as a regression test (lesson 10).
Report success rates with seeds and number of scenarios. Simulation is never physical evidence.
- `plant_sim.py`: whole mission over random plant cells (tag stations, people, occlusion, odometry drift, caution,
  ultrasonic level, return home, docking) using the real Linux code; results in `docs/sim/plant-sim-20-maps.md`.
- `tag_accuracy.py`, `tag_visibility.py`: single-tag / tag-pair error vs range and layout visibility.
- `level_model.py`: Python mirror of the firmware ultrasonic level filter (same test vectors).
