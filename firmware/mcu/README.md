# Firmware — STM32U585 (Zephyr + Arduino core on UNO Q)

Owns everything with a deadline (ADR-0002): motor PWM + encoder loops, tool sequencing, stop conditions, watchdog,
sensor filtering. Coding rules: `.claude/agents/embedded-safety-reviewer.md`.

Proposed layout (create as code arrives):
```
firmware/mcu/
  config.h          all constants with units and the measurement that justifies each threshold
  safety.*          stop conditions evaluated every cycle (cannot be disabled at runtime)
  motion.*          segment executor: runs one order and stops by itself
  tools.*           brush / vacuum / compactor sequencing with interlocks
  sensors.*         floats, MPX5010DP, HX711, bumpers, battery — min-of-3 + 2-read confirm + capped votes
  level.*           ultrasonic A02YYUW parser + level filter (SR-022, ADR-0010) — implemented, host-tested
  bridge.*          RPC protocol (versioned), heartbeat, T_stale
  main.*            fixed-period loop, watchdog feed only when all checks pass
```
Board facts (pins, voltage tolerance, RPC API) must be checked in the official Arduino UNO Q docs; write
"(to verify)" until confirmed.
