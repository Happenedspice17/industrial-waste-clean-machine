"""Navigator-side pose fusion (SR-018, SR-019): blend each accepted fix with dead reckoning by variance.

Overwriting the pose with every accepted fix made the pose worse in simulation (a one-tag fix has weak heading and
~0.1 m position noise); weighting by variance cut the p95 pose error by about half (docs/sim/plant-sim-20-maps.md).
Odometry variance grows with distance (position, estimate 3 %) and time (IMU heading, estimate 0.3 deg/sqrt(min)).
Decides only; the MCU executes and stops by itself (ADR-0002).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from linux.vision.geometry import wrap


@dataclass(frozen=True)
class FusionNoise:
    pos_per_m: float = 0.03
    yaw_deg_per_sqrt_min: float = 0.3
    min_fix_sigma_m: float = 0.01
    min_fix_sigma_deg: float = 0.2


class PoseFusion:
    def __init__(self, pose: tuple[float, float, float], noise: FusionNoise | None = None) -> None:
        self.x, self.y, self.yaw = pose
        self.n = noise or FusionNoise()
        self.pos_var = 0.0
        self.yaw_var = 0.0

    @property
    def pose(self) -> tuple[float, float, float]:
        return self.x, self.y, self.yaw

    def predict(self, dx: float, dy: float, dyaw: float, dt: float) -> None:
        """Dead-reckoning step in the world frame."""
        self.x += dx
        self.y += dy
        self.yaw = wrap(self.yaw + dyaw)
        ds = math.hypot(dx, dy)
        self.pos_var += (self.n.pos_per_m * ds) ** 2 + 0.002 * ds
        self.yaw_var += math.radians(self.n.yaw_deg_per_sqrt_min) ** 2 * dt / 60

    def correct(self, pose: tuple[float, float, float], sigma_m: float, sigma_deg: float) -> None:
        fix_pos = max(sigma_m, self.n.min_fix_sigma_m) ** 2 if math.isfinite(sigma_m) else 0.25**2
        k = self.pos_var / (self.pos_var + fix_pos) if self.pos_var + fix_pos > 0 else 1.0
        self.x += k * (pose[0] - self.x)
        self.y += k * (pose[1] - self.y)
        self.pos_var *= 1 - k
        if math.isfinite(sigma_deg):
            fix_yaw = math.radians(max(sigma_deg, self.n.min_fix_sigma_deg)) ** 2
            ky = self.yaw_var / (self.yaw_var + fix_yaw) if self.yaw_var + fix_yaw > 0 else 1.0
            self.yaw = wrap(self.yaw + ky * wrap(pose[2] - self.yaw))
            self.yaw_var *= 1 - ky
