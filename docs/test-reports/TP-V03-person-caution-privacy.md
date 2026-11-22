# Test protocol — TP-V03 Person caution and camera privacy

Status: written 2026-11-22, **not run**. Refs: SR-020, SR-021 · ADR-0009 · TM-V01 rev 2 · privacy review 2026-11-22.

## Acceptance criteria (fixed before testing)
| Part | Requirement | Pass |
|---|---|---|
| P1 Caution | SR-020 | Speed request ≤ 0.10 m/s within 0.5 s of the trigger in ≥ 95 % of ≥ 100 person passes (walk across, walk towards, stand, sit, partly hidden); never above the requested speed |
| P2 Blind camera | SR-020 | Lens covered / camera unplugged → caution on within 0.5 s and held while blind |
| P3 No images | SR-021 | After a 1 h run: 0 image files anywhere (`find / -newer start -type f` filtered by image magic), log mode 0600, logs hold only count + nearest-distance bins |
| P4 Image hardening | SR-021 | Swap off or encrypted (`/proc/swaps`), process non-dumpable (`/proc/<pid>/status`), no core file after `kill -SEGV`, no listening frame server (`ss -ltnp`), app user is the only member of `video` |

## Procedure
1. Volunteers informed and consenting; no video recording of the test. Ground truth by an observer with a clicker
   and a tape grid (person distance bins), not by camera.
2. P1/P2 with `python -m linux.vision.tag_logger` plus the caution log; replay offline (lesson 10).
3. P3/P4 on the robot image right after a run; record commands and outputs in the report.
4. Measure HOG time per frame on the QRB2210 (lesson 12); if over budget, record the frame rate actually reached.

## Records
Test report, observer sheets, command outputs, engineering log entry. No images.
