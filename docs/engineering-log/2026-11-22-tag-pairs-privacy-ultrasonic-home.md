# Engineering log — 2026-11-22 Tag pairs, privacy-first person caution, ultrasonic level, home docking, 20-map sim

- **Problem:** Owner asked for two AprilTags per position with full trust when 2+ tags are seen, more care near
  people and obstacles, no retention of person images (cybersecurity agent to review), one camera now and ≥ 4 later,
  container level by ultrasonic sensor, two home tags to return to after each suction round, and simulation over
  20 maps.
- **Conflicts flagged (rule 11):** "trust 100 %" vs rule 6 → two agreeing tags count as the second read, gates
  stay, log-only until TP-V02; camera person detection vs ADR-0006 option C → advisory speed cap only; ultrasonic
  never replaces the float shut-off (rule 1).
- **Change:** ADR-0008/0009/0010; SR-019–SR-023; localizer (multi-camera, joint multi-tag solve, agreement gate,
  caution, single-tag jumps confirmed only by a different tag); `people.py`, `pipeline.py`, `privacy.py`
  (FrameScope, fail-closed hardening); `nav/caution.py`, `nav/home.py`; `firmware/mcu/level.{h,cpp}` + host test +
  Python mirror; tag sheets 0–25 and HOME 100–101; `sim/plant_sim.py`; TP-V03, TP-L01, TP-N01, TP-V02 update; DFMEA
  F-013–F-017, SCCAF SC-009/SC-010; WCCA ultrasonic UART; TM-V01 rev 2 and privacy review (cybersecurity agent;
  its findings verified and dispositioned in the review file); traceability check now fails on undefined SR IDs.
- **Evidence (simulation):** tag pair 0.60 m apart, 0.5 px noise, no IMU prior: p95 0.05 m / 1.0° at 2.5 m. 20 maps:
  0 contacts, 0 machine hits, 38/38 dockings (worst 0.055 m), coverage 77–83 %, pose p95 median 0.147 m, 0 bad fixes
  from moved tags after the fix (31 before). OpenCV 5 removed HOG → pinned < 5.
- **Validation:** `python tools/check_all.py` passes (pytest incl. firmware host build, privacy, docking, sim smoke).
- **Result / next:** team confirms ADRs; quote A02YYUW ×2 and add to BOM; harden robot image (swap, coredump, video
  group); run TP-V02/V03/L01/N01; simulate LiDAR scan matching and 4 cameras; DFMA for camera mounts, WCCA for USB.
- **N/A:** DFMA (no robot part designed yet; ultrasonic and camera brackets go through DFMA when drawn).
