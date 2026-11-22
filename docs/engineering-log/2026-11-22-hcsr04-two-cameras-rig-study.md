# Engineering log — 2026-11-22 HC-SR04, front + rear cameras, pose fusion, cameras vs LiDAR

- **Problem:** Owner asked for the cheapest ultrasonic (HC-SR04), at least two cameras (front + rear) in the next
  build, and whether 4 cameras or 1 LiDAR + 1 camera is better given the LiDAR price.
- **Change:** ADR-0010 revised (HC-SR04, echo divider, splash sleeve); firmware `level::echo_to_mm`; SR-024 and rear
  camera config; localizer geometry check and drift-scaled jump limit; `linux/nav/fusion.py`; simulator rigs;
  ADR-0011 (proposed).
- **Evidence (simulation):** first 2-camera run looked worse than 1 camera (p95 median 0.178 vs 0.147 m). Cause:
  weak-geometry pair fixes accepted at once, then the robot could not re-anchor; and every fix overwrote the pose.
  After the fixes, 20 maps per rig, p95 median / worst: 1 cam 0.081 / 0.288 m, 2 cams 0.058 / 0.211 m, 4 cams
  0.036 / 0.096 m, LiDAR + 1 cam 0.033 / 0.034 m (optimistic LiDAR model). All rigs 0 contacts, 38/38 dockings,
  coverage ≈ 83 % (route-limited). WCCA: echo divider 2.65–3.15 V.
- **Reasoning:** cameras give no range, so the LiDAR's obstacle role must move to a low-cost ranging ring on the MCU
  if the LiDAR is dropped (rule 1, flagged). 4 cameras localize better but cost more CPU/USB/privacy and still give
  no obstacle range.
- **Validation:** `python tools/check_all.py` passes.
- **Result / next:** team decides ADR-0011; if accepted, write the ranging-ring SR, WCCA, DFMEA and ISO check; run
  TP-V02 with two cameras; measure HC-SR04 fouling in TP-L01.
- **N/A:** DFMA (no part drawn yet).
