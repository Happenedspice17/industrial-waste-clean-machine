"""Caution mode (SR-020): a person seen by a camera or an obstacle near the LiDAR lowers the speed request.

Advisory only: it can lower the speed Linux requests, never raise it, and it never replaces the MCU stops (bumpers,
LiDAR stop zone, watchdog). Values are estimates until TP-V03.
"""

from __future__ import annotations

from dataclasses import dataclass

from linux.vision.people import Person


@dataclass(frozen=True)
class CautionLimits:
    person_range_m: float = 3.0
    obstacle_range_m: float = 1.5
    speed_mps: float = 0.10
    hold_s: float = 2.0
    """Stay cautious this long after the last trigger (no flicker, rule 6)."""


class Caution:
    def __init__(self, limits: CautionLimits | None = None) -> None:
        self.lim = limits or CautionLimits()
        self._last = -1e9

    def update(self, t: float, persons: list[Person], lidar_min_m: float | None, *, blind: bool = False) -> bool:
        """``blind``: the camera gave no usable frame; caution then stays on (fail-safe for an advisory function)."""
        near_person = any(p.distance_m <= self.lim.person_range_m for p in persons)
        near_obstacle = lidar_min_m is not None and lidar_min_m <= self.lim.obstacle_range_m
        if near_person or near_obstacle or blind:
            self._last = t
        return t - self._last <= self.lim.hold_s

    def speed(self, requested: float, active: bool) -> float:
        return min(requested, self.lim.speed_mps) if active else requested
