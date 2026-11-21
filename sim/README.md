# Simulation

- `coverage/`: boustrophedon coverage of a plant cell (semester-1 result: 96 %, 25.6 min, 167 m²/h, 68 Wh).
- `sensors/`: noisy sensor models (LiDAR dropouts on reflective metal, float bounce, pressure noise, RPC delay,
  clock jumps) — must reproduce failures seen in field logs (lesson 9).
- `replay/`: run a field log through the decision code as a regression test (lesson 10).
Report success rates with seeds and number of scenarios. Simulation is never physical evidence.
