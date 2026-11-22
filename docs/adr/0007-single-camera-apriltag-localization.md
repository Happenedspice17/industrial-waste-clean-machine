# ADR-0007: One camera only, used for AprilTag localization

- Status: proposed (requested by the project owner, 2026-11-21; team to confirm)
- Date: 2026-11-21
- Requirements affected: R6, R8, SR-015, SR-016, SR-017, SR-018 · supersedes the task list of ADR-0006

## Context
ADR-0006 gave vision two tasks (residue check behind the squeegee, container-level cross-check) and noted that one
camera cannot see the floor and both containers. The owner asked to keep **one camera only** and use it to locate the
robot with AprilTags placed around the cell. Pose today comes from encoders + IMU, re-anchored by LiDAR scan match
(`docs/02-architecture.md`). LiDAR matching can be ambiguous in a symmetric cell and needs a start pose; a tag has a
unique ID, so one sighting gives an absolute pose with no prior (deduced).

**Conflict flagged (CLAUDE.md rule 11):** ADR-0006 says vision "never stops, steers or blocks the robot". A pose
correction steers indirectly (the route follows the corrected pose). Mitigations below keep the safety chain as is.

## Options considered
- **A. One forward camera, tilted up 15°, AprilTag 36h11 on walls/columns (chosen).** Same USB camera (M6 BOM),
  no extra hardware, printed tags. Loses the residue check and container check.
- **B. Keep ADR-0006 tasks, no tags.** Needs a second camera or mirror (ADR-0006 consequences); no absolute pose.
- **C. Two cameras (tags + residue).** More USB load and cost; contradicts "one camera only".
- **D. Floor tags.** Rejected: oil, chips and the squeegee would cover or wear them; the camera would look down.

## Decision
1. One USB camera on the Linux side, facing forward, ~0.45 m high, tilted up ~15° (to measure on the real mount).
2. AprilTag family **tag36h11**, printed at true scale by `tools/gen_apriltags.py` (default 0.16 m black square on US letter, the largest that fits with its white border),
   placed on walls, columns and machine sides at a measured height, positions in a tag map JSON
   (`linux/vision/config/tag_map.example.json`; the real one is measured on site, rule 8).
3. Pose solver: the robot is on the floor and the mount is known, so only (x, y, yaw) is solved from the tag corners
   (Levenberg-Marquardt), with the IMU heading as a prior; several tags in view are solved together. A single tag's
   6-DOF orientation is not trusted (simulation: lateral/yaw ambiguity grows with range).
4. Gates (initial estimates, replace with TP-V02 midpoints, rule 5): black square ≥ 20 px, range ≤ 4 m, view angle
   ≤ 60°, reprojection RMS ≤ 1.5 px, unknown IDs rejected. A fix > 0.30 m or > 10° from odometry needs **2 consecutive
   consistent reads** (capped vote counter, rule 6).
5. Role: **support** for pose (re-anchor next to LiDAR), never authority for obstacles or safety. The MCU keeps its own
   stops (bumpers, LiDAR stop zone, stale-command watchdog; ADR-0002, ADR-0003). `NAV_ENABLED = False` until TP-V02
   passes and its report is committed (SR-017).
6. Residue check (SR-015) and container cross-check (SR-016) are **deferred**: floats stay the only level authority;
   residue is checked by the operator.
7. Frames are never written to disk; logs hold tag IDs, corners and fixes only (threat model TM-V01).

## Consequences
- New SR-018 and protocol TP-V02; SR-015/SR-016 deferred; DFMEA F-010–F-012 and SCCAF SC-008; TM-V01.
- Lower USB load than two cameras (WCCA unchanged: same single camera as the M6 BOM).
- Example layout (12 × 8 m cell, 20 tags every 2 m on the walls, 0.9 m high) gives a usable tag in 40 % of poses and
  a longest stretch of ≈9 m without a fix along the coverage route (simulation, no occlusion). Odometry + IMU + LiDAR
  carry the pose between fixes; add tags on interior columns/machines if TP-V02 shows the drift is too large.
- Error grows with range: p95 position ≈ 0.09 m at 2.5 m and ≈ 0.17 m at 3.5 m (160 mm tag) with 0.3 px corner noise (simulation,
  `sim/tag_accuracy.py`). Real corner noise is unknown until TP-V02.
- Tags must stay clean and in place; a moved tag gives a confident wrong fix unless the gates catch it (F-010).

## Evidence
Simulation only: `linux/vision/test_vision.py` (synthetic images through the real detector), `sim/tag_accuracy.py`,
`sim/tag_visibility.py`. Nothing measured on this robot yet.
