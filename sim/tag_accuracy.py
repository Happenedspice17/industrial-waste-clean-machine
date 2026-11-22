#!/usr/bin/env python3
"""Single-tag pose error vs range (simulation, SR-018): projected corners + Gaussian pixel noise, IMU heading prior
with 1.5 deg (1 sigma) error. Real corner noise must come from TP-V02. Usage: python sim/tag_accuracy.py"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from linux.vision.config import Camera, Tag, load_camera  # noqa: E402
from linux.vision.detector import Observation, tag_corners  # noqa: E402
from linux.vision.geometry import inv_tf, robot_in_world, tag_in_world, wrap  # noqa: E402
from linux.vision.localizer import Gates, Localizer  # noqa: E402

CAM = load_camera(ROOT / "linux" / "vision" / "config" / "camera.example.json")


def corners(robot: np.ndarray, tag: Tag, cam: Camera) -> np.ndarray:
    tf = inv_tf(robot @ cam.mount) @ tag.pose
    pts = (tf[:3, :3] @ tag_corners(tag.size).T).T + tf[:3, 3]
    return (cam.matrix @ (pts / pts[:, 2:3]).T).T[:, :2]


def p95_error(dist: float, noise_px: float, size: float = 0.22, n: int = 200, seed: int = 1) -> tuple[float, float]:
    """95th-percentile (position m, heading deg) error for one tag ``dist`` m ahead, +/-20 deg heading, +/-1 m side."""
    rng = np.random.default_rng(seed)
    tag = Tag(0, size, tag_in_world(6.0, 8.0, 0.9, math.radians(270)))
    loc = Localizer({0: tag}, CAM, Gates(max_range_m=99.0))
    errs = []
    for _ in range(n):
        yaw = math.radians(90 + rng.uniform(-20, 20))
        x, y = 6.0 + rng.uniform(-1, 1), 8.0 - dist
        robot = robot_in_world(x, y, yaw)
        obs = Observation(0, corners(robot, tag, CAM) + rng.normal(0.0, noise_px, (4, 2)))
        fix = loc.update([obs], (x, y, yaw + math.radians(rng.normal(0.0, 1.5))))
        if fix.pose:
            errs.append((math.hypot(fix.pose[0] - x, fix.pose[1] - y), abs(math.degrees(wrap(fix.pose[2] - yaw)))))
    pos, ang = np.percentile(np.array(errs), 95, axis=0)
    return float(pos), float(ang)


def main() -> int:
    print("range m | noise px | p95 position m | p95 heading deg   (simulation, 0.22 m tag, 640x480 60 deg HFOV)")
    for d in (1.5, 2.5, 3.5, 4.5, 5.5):
        for noise in (0.3, 0.7):
            pos, ang = p95_error(d, noise)
            print(f"{d:7.1f} | {noise:8.1f} | {pos:14.3f} | {ang:15.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
