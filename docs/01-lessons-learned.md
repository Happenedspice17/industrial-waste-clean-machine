# 01 · Lessons learned (apply by default)

Origin: maze-solving robot on the same Arduino UNO Q (STM32U585 Zephyr + QRB2210 Debian/Python), Microcontroladores 2,
Universidad Panamericana. Sensors: 3× VL53L0X, TCS34725, MPU-6050, OV9281 camera, no encoders.
Repo: github.com/Happenedspice17/sumo-v-ia. Result: 2nd place, best run 2 min 6.4 s.

**Rule for every agent:** apply these without being reminded and warn the user when a decision goes against one.

## Technical

1. **Split by timing requirement, not complexity.** The real-time MCU executes each order autonomously and safely and
   stops by itself on a wall/goal (here: obstacle, bumper, fault, stale command). Linux decides with the robot still.
   If Linux is late, the robot stays still instead of crashing.
2. **Time is not distance.** Moving/turning by time drifts with battery, floor and load. References come from an
   absolute sensor (here: encoders + IMU + LiDAR scan matching; never open-loop timing).
3. **Trust geometry, not estimated millimeters.** Re-anchor position on known features each cycle (here: walls, machine
   footprints, aisle edges in the LiDAR map).
4. **One bad reading never changes anything alone.** Min of 3 readings, confirm jumps on 2 consecutive reads, capped
   vote counters (majority filter with hysteresis). Applies to floats, pressure, bumpers, level, RFID.
5. **Thresholds at the midpoint between two measured real readings**, not glued to one or taken from CAD. A geometric
   number the sensor cannot reach is useless.
6. **Every sensor has a written role and hierarchy.** (Previous: camera went from leading to tie-breaker to off; floor
   reflections looked like walls. ToF became authority for walls, color sensor the only source for goal.)
7. **Each sensor only distinguishes what it can really see.** Respect cones, ranges and reflectivity limits; quantize
   ("0, 1, 2+ free cells") instead of trusting long distances.
8. **Localizing against a known map beat building the map on the fly** (Bayesian, 16 corner/heading hypotheses).
   Here: map once, save, localize against it every shift.
9. **Simulate before tuning:** same code against hundreds of noisy scenarios. The simulator found real bugs and raised
   arrival rate 26 % → 98 %. Make the simulator reproduce field failures; otherwise it lies.
10. **Log every run raw** (~20 Hz readings + every decision) and replay against the map. Field logs → concrete fixes.
11. **Calibrate from a phone web page, on site, with its light, without reprogramming.** Color mis-calibration cost
    points. Calibration on site is not optional.
12. **Watch side load:** Bridge RPC web queries, OLED refresh blocking ~25 ms, system clock jumping on network sync
    (use `time.monotonic()`) cause failures that are not the algorithm.
13. **Removing code is engineering.** A rewrite removed ~500 lines without losing capability.
14. **Test on the real floor early and often.** Ideas failing due to battery or mechanics were discarded fast.
15. **Measure real parts before CAD.** Saves prints.

## Process and documentation

16. **Engineering log per stage**: problem, hypothesis, change, evidence, reasoning, result, commits. Mark "(deduced)"
    whatever is not written in commits or code. Template: `docs/templates/engineering-log.md`.
17. **Single source of truth:** PDFs are generated from `.md` (pandoc + Playwright, Mermaid). On closing, regenerate
    everything and cross-check counts, dates and versions across README, manuals and log.
18. **Verify data against code before documenting** (a flag like `CAM_LOC = False` contradicted the README).
19. **Parallel agents:** one file per agent, agents never commit, key facts in the prompt, verify their claims (dates,
    order of events, assumed commands like `adb pull`) before integrating.
20. **Mermaid timeline:** `:` separates events; write "2 min 6.4 s", not "2:06.4".
21. **The version that competed is marked final in the README** with result, video and what remains untested, honestly.

## Open items inherited (for reference)

Camera v2 untested with real photos; `cuadrar()` and motor balance tested only in simulation; colors logged but not
used to correct position; map not shown in web UI; power test without PD module pending.
