# ADR-0002: Split MCU / Linux by timing requirement

- Status: accepted · Date: 2026-11-21 · Requirements: SR-006, SR-007, SR-013

## Context
Lesson 1 from the previous UNO Q robot.
## Decision
MCU executes each motion order autonomously and stops by itself (obstacle flag, bumper, fault, overspeed, stale
command). Linux plans and decides with the robot stopped or between segments. Heartbeat every 100 ms; T_stale
initially 300 ms, to be set from measured RPC latency + margin.
## Consequences
Protocol must be versioned; every stop reason logged; simulator must model RPC delays and clock jumps.
