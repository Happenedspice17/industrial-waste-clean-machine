# Lessons learned

## Lessons inherited from the team's previous robot

Origin: a maze-solving robot on the same Arduino UNO Q, built by the team for *Microcontroladores 2* at Universidad
Panamericana (sensors: 3 × VL53L0X, TCS34725, MPU-6050, OV9281 camera, no encoders; result: **second place**, best
run 2 min 6.4 s; repository `github.com/Happenedspice17/sumo-v-ia` [77]). These 21 lessons are applied by default in
this project; any decision that goes against one must be flagged.

### Technical

| # | Lesson | How it is applied here |
|:-:|---|---|
| 1 | **Split by timing requirement, not complexity.** The real-time MCU executes each order autonomously and stops by itself; Linux decides with the robot still. If Linux is late, the robot stays still | ADR-0002, SR-007, heartbeat + T_stale |
| 2 | **Time is not distance.** Moving/turning by time drifts with battery, floor and load | References from encoders + IMU + LiDAR; never open-loop timing |
| 3 | **Trust geometry, not estimated millimeters.** Re-anchor position on known features each cycle | Walls, machine footprints, aisle edges in the LiDAR map |
| 4 | **One bad reading never changes anything alone.** Min of 3, confirm jumps on 2 consecutive reads, capped vote counters | Floats, pressure, bumpers, level, RFID (Section 6.6) |
| 5 | **Thresholds at the midpoint between two measured real readings**, not from CAD | Rule 5; the AprilTag mount guess failed exactly this way (Chapter 11) |
| 6 | **Every sensor has a written role and hierarchy** | Sensor hierarchy table (Section 6.6) |
| 7 | **Each sensor only distinguishes what it can really see** | Respect cones, ranges, reflectivity; quantize instead of trusting long distances |
| 8 | **Localizing against a known map beat building it on the fly** | Map once, save, localize every shift |
| 9 | **Simulate before tuning:** the simulator raised arrival rate from 26 % to 98 % | `sim/`; make it reproduce field failures |
| 10 | **Log every run raw** (≈ 20 Hz + every decision) and replay | `run.jsonl` in the AprilTag app; `sim/replay/` planned |
| 11 | **Calibrate from a phone web page, on site, with its light** | Web UI calibration; AprilTag mount-calibration button |
| 12 | **Watch side load:** web queries, display refresh blocking ≈ 25 ms, clock jumps on network sync | Use `time.monotonic()`; model RPC delays in simulation |
| 13 | **Removing code is engineering** (a rewrite removed ≈ 500 lines without losing capability) | Prefer deleting dead paths over adding flags |
| 14 | **Test on the real floor early and often** | Suction rig first; oily-floor tests in P4 |
| 15 | **Measure real parts before CAD** | Rule 8; wheel hub waits for measured shaft and wheel |

### Process and documentation

| # | Lesson | How it is applied here |
|:-:|---|---|
| 16 | **Engineering log per stage:** problem, hypothesis, change, evidence, reasoning, result, commits; mark "(deduced)" | `docs/engineering-log/` (11 entries) |
| 17 | **Single source of truth:** PDFs generated from Markdown; regenerate and cross-check counts and dates on closing | `docs/00-project-context.md`; this report is built from Markdown |
| 18 | **Verify data against code before documenting** (a flag contradicted the README) | Report numbers re-run with the tools |
| 19 | **Parallel agents:** one file per agent, agents never commit, verify their claims | `.claude/agents/` rules |
| 20 | **Diagram syntax details** (e.g. "2 min 6.4 s", not "2:06.4" in Mermaid timelines) | Documentation style |
| 21 | **Mark the final version honestly** with result, video and what remains untested | Project status sections in README and this report |

## Lessons from this semester

| Lesson | What happened | What we do now |
|---|---|---|
| Selection methods must agree | The quality matrix and the pairwise comparison started with a rank correlation of only 0.26 | Correct contradictory answers with an explicit rule; agreement rose to 0.83 |
| Mandatory items need a rule | Weighted scores ranked the chassis 46th and the e-stop 41st | Keep mandatory structural and safety items regardless of score |
| Do not add a third stream | Water/steam outlets would dilute the oil and create more waste | Removed from the concept; no water, steam or chemicals |
| Floor lines fail on oil | Oil fouls floor markings | LiDAR + encoders + IMU |
| Check statistics against the source | The first draft's fall statistics did not match the cited page | Every figure re-checked; evidence labels |
| No absolute claims | "No system exists" and "slip-free floor" could not be proven | Bounded gap statement; benefits as expected results |
| Suction is the critical risk | An 80 W vacuum may not lift steel | Suction-first plan; option B as backup; criteria fixed before testing |
| The calendar was too optimistic | The October plan aimed at a functional demo on 12 December after a seven-week build | Replanned: the full design and risk record this semester, the build next semester, starting with the suction rig |
| Guessed parameters break software | The AprilTag app failed on the bench because the mount height and a tag position were guessed | Measure first; a calibration button; refusals instead of wrong poses |
| Test early, even crudely | A one-afternoon handheld test (TP-S01) changed the concept more than weeks of analysis | Run cheap exploratory tests early; label them exploratory and fix criteria before the real test (TP-S02) |
| A principle can fall to evidence | "No water or chemicals" was a core principle; the pre-test showed dry suction does not move the film | Change it through an ADR with options and consequences (ADR-0008), not silently; update requirements, risks and economics in the same change |
| Write it where a script can check it | Requirements and risks in slides drift | YAML/CSV registers checked by CI on every change |
