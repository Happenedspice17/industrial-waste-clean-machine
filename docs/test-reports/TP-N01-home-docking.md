# Test protocol — TP-N01 Return home and docking on the home tag pair

Status: written 2026-11-22, **not run**. Refs: SR-023, SR-019, SR-022 · ADR-0008.

## Acceptance criteria (fixed before testing)
≥ 19 of 20 dockings within 0.05 m and 3° of the surveyed dock pose (5 start poses × 4 runs, 1–4 m from the dock,
headings ±90°); every failed docking ends stopped and reported (no forced contact); return triggered by end of round
and by a FULL level in at least 3 runs each.

## Procedure
1. Mount home tags 100–101 (0.40 m apart, 0.9 m high), survey the dock pose (tape + square), save in the tag map.
2. Run with `NAV_ENABLED` only after TP-V02 passes; until then run the docking logic in log-only mode while an
   operator drives, and compare its decisions with the measured pose.
3. Measure the final pose with a tape grid and a square after each docking; log fixes and commands at 20 Hz.
4. Fault cases: cover one home tag, a person standing between robot and tags, a printed copy of tag 100 elsewhere.

## Records
Logs (release assets), measurements sheet, test report, engineering log entry.
