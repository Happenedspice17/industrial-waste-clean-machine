# Firmware — STM32U585 (Zephyr + Arduino core on UNO Q)

Owns everything with a deadline (ADR-0002): motor PWM + encoder loops, tool sequencing, stop conditions, watchdog,
sensor filtering. Coding rules: `.claude/agents/embedded-safety-reviewer.md`.

**Status (Nov 2026):** no robot firmware yet — it starts after the suction gate (ADR-0004). The only MCU code today is
the AprilTag bench sketch in [`linux/apriltag_pose/sketch/`](../../linux/apriltag_pose/sketch/), which only prints
validated poses. CI runs clang-format + cppcheck once C/C++ sources appear here.

Non-negotiable: the e-stop opens the main relay in hardware; firmware never replaces it. The MCU stops by itself on
obstacle, bumper, stale command (heartbeat 100 ms) or fault.

Proposed layout (create as code arrives):
```
firmware/mcu/
  config.h          all constants with units and the measurement that justifies each threshold
  safety.*          stop conditions evaluated every cycle (cannot be disabled at runtime)
  motion.*          segment executor: runs one order and stops by itself
  tools.*           brush / vacuum / compactor sequencing with interlocks
  sensors.*         floats, MPX5010DP, HX711, bumpers, battery — min-of-3 + 2-read confirm + capped votes
  bridge.*          RPC protocol (versioned), heartbeat, T_stale
  main.*            fixed-period loop, watchdog feed only when all checks pass
```
Board facts (pins, voltage tolerance, RPC API) must be checked in the official Arduino UNO Q docs; write
"(to verify)" until confirmed.
