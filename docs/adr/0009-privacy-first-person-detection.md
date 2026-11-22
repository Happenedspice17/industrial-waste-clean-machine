# ADR-0009: Person detection that keeps no images (privacy by design)

- Status: proposed (requested by the project owner, 2026-11-22; reviewed by the cybersecurity agent)
- Date: 2026-11-22
- Requirements affected: SR-020, SR-021 · threat model TM-V01 rev 2 · privacy review 2026-11-22

## Context
The owner wants the robot to be more careful near people, and the processing of people and images to be eliminated
or censored, without keeping them in memory. Workers in a machining plant are identifiable; a log of where they
stood is personal data under the Mexican LFPDPPP (privacy review P-06).

## Options considered
- **A. No person detection (camera only for tags).** Most private; caution only from LiDAR obstacles.
- **B. On-robot detection, summaries only (chosen).** HOG on a downscaled grey copy; output only bearing and rough
  distance; pixels zeroed per frame; no image ever stored or sent.
- **C. Blur/black-box people in a stream or recordings.** Rejected: a detector misses people (sitting, occluded,
  close), so a deny-list redaction leaks; no video stream is needed for the task.

## Decision
1. `linux/vision/pipeline.py` + `privacy.FrameScope`: every buffer the pipeline creates (frame, grey copy, downscaled
   copy) is zeroed before the result returns, also on exceptions; only tag corners and `Person(bearing, distance)`
   leave the scope.
2. `privacy.require_hardening()`: no camera opens unless core dumps are off and the process is non-dumpable.
3. No image files, no debug view, no frame server. Any future image view needs a new ADR and an allow-list design
   (show tag regions only).
4. Logs keep only person count and nearest distance in 0.5 m bins (no bearings, so no location track); log files are
   created with mode 0600 and identify configs by hash, not path.
5. Robot image (to do, TP-V03): swap off or encrypted, `fs.suid_dumpable=0`, systemd-coredump storage off,
   dedicated non-root user as the only member of `video`, cameras by stable `/dev/v4l/by-id` paths, pinned OpenCV.
6. The detector is advisory (SR-020); HOG quality is unknown until TP-V03. OpenCV is pinned below 5 because 5.x
   removed HOG.

## Consequences
Python cannot reach kernel V4L2 buffers, OpenCV's internal capture and detector temporaries, or freed allocator
pages: the design reduces residence in RAM, it does not eliminate it (stated in SR-021 and TM-V01). A separate
capture process per run would further limit residence (privacy review P-02, open).

## Evidence
`linux/vision/test_privacy.py` (frame zeroed after processing and on exceptions, views wiped through their base,
non-dumpable, coarse person logging, camera ordering). Nothing tested on the robot image.
