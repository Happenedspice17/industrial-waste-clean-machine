# ADR-0008: Tag pairs per station, immediate trust on agreeing tags, home pair, multi-camera ready

- Status: proposed (requested by the project owner, 2026-11-22; team to confirm)
- Date: 2026-11-22
- Requirements affected: SR-017, SR-018, SR-019, SR-020, SR-023 · extends ADR-0007

## Context
With one tag in view, heading is weakly determined (lateral offset and yaw look alike), so ADR-0007 leaned on the IMU
heading prior. The owner asked for **two tags per position**, to **trust the camera fully when it sees two or more
tags**, to be **more careful when a person or obstacle is seen**, for **two home tags** where the robot goes after
each suction round, and to plan for **at least four cameras** while building with one.

**Conflicts flagged (CLAUDE.md rule 11):** "trust 100 %" vs rule 6 (one reading never changes state alone) and rule 4
(no claims without evidence); "careful near people" vs ADR-0006 option C (a webcam is not a safety sensor).

## Decision
1. **Stations:** every tag location is a pair of tag36h11 on US letter sheets, centres 0.60 m apart, same height
   (0.9 m), same facing. Simulation (`sim/tag_accuracy.py`, 0.5 px noise, no IMU prior): p95 0.05 m / 1.0° at 2.5 m
   with 0.60 m spacing vs 0.09 m / 2.1° with 0.25 m.
2. **Trust rule (SR-019):** two or more tags in the same frame whose individual poses agree within 0.25 m and 8° are a
   cross-check on their own: the joint fix (all corners, no IMU prior) is accepted in that frame, even far from
   odometry. If they disagree, all are rejected (a tag was moved or misread). One tag keeps ADR-0007 rules. This is
   how rule 6 is met: the second tag is the second read. "100 %" is interpreted as *no extra confirmation*, not as
   unchecked: the reprojection, range and agreement gates still apply, `NAV_ENABLED` stays off until TP-V02 passes
   (SR-017), and nothing in the safety chain consumes the fix.
3. **Caution (SR-020):** a person seen by a camera within 3 m, a LiDAR obstacle within 1.5 m, or a blind camera →
   speed request capped at 0.10 m/s for 2 s after the last trigger, and multi-tag jumps need 2 consistent reads.
   It only lowers speed; MCU stops (bumpers, LiDAR stop zone, watchdog) are unchanged.
4. **Home (SR-023):** IDs 100–101, 0.40 m apart on a wall; dock pose 1.0 m in front, robot facing the tags so both
   stay in the 60° view while docked. `linux/nav/home.py`: approach point 1 m out → align → straight-in at 0.08 m/s
   → docked only on a fresh fix that sees both home tags; lost tags → back off and retry (3×) → failed (stopped,
   reported). Triggered after each round or when the ultrasonic level reads full (SR-022, ADR-0010).
5. **Multi-camera:** observations carry a camera index; `Localizer` takes a list of cameras, each with its own
   calibration and measured mount, and solves all corners jointly. One camera now; four planned (to be placed by
   DFMA, USB budget by WCCA before buying).

## Consequences
- Twice the tags per station (26 + 2 home sheets for the example 12 × 8 m cell).
- Two printed tags at the surveyed spacing pass the pair check (privacy review P-15, TM-V01): accepted only while
  log-only; before enabling, bound multi-tag jumps with LiDAR scan agreement and confirm the dock with LiDAR
  geometry or charging contacts.
- Whole-mission simulation over 20 random cells: `docs/sim/plant-sim-20-maps.md`.

## Evidence
Simulation only: `linux/vision/test_vision.py`, `linux/nav/test_home.py`, `sim/tag_accuracy.py`,
`sim/plant_sim.py`. Nothing measured on the robot.
