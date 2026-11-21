# ADR-0001: Arduino UNO Q 2 GB as main controller

- Status: accepted · Date: 2026-09-24 · Requirements: R5, R6, R7, R8, R10

## Context
Needs real-time I/O (motors, encoders, sensors, sequencing) and Linux workloads (LiDAR mapping, vision, web UI, logs).
## Options considered
UNO Q · Raspberry Pi 5 + Arduino Mega · ESP32-S3 · STM32 Nucleo · Raspberry Pi 4 + microcontroller.
## Decision
UNO Q 2 GB (ABX00162, ≈ MXN 1,080, UNIT Electronics). One board covers both domains; the team already used it in a
previous robot (2nd place). Pi 4 has a stronger CPU and bigger ROS 2 community but needs an extra MCU for PWM,
encoders and HX711.
## Consequences
Single USB-C port → powered USB-C hub needed for LiDAR + webcam. Consider 4 GB variant if SLAM + web UI saturate RAM.
CAN only classic via FDCAN on D4/D5 with Zephyr API (not needed now). Bridge RPC latency must be measured (T_stale).
