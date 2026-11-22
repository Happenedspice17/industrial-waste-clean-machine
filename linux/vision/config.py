"""Tag map and camera configuration (SR-018). Values come from measurement, never from CAD alone (rules 5, 8)."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from linux.vision.geometry import Mat, cam_in_robot, tag_in_world

FAMILY = "tag36h11"


@dataclass(frozen=True)
class Tag:
    id: int
    size: float
    pose: Mat


@dataclass(frozen=True)
class Camera:
    matrix: Mat
    dist: Mat
    width: int
    height: int
    mount: Mat


def load_tag_map(path: Path) -> dict[int, Tag]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("family") != FAMILY:
        raise ValueError(f"tag map family must be {FAMILY}")
    default = float(data["tag_size_m"])
    tags: dict[int, Tag] = {}
    for t in data["tags"]:
        tid = int(t["id"])
        if tid in tags:
            raise ValueError(f"duplicate tag id {tid}")
        size = float(t.get("size_m", default))
        if not 0.02 <= size <= 1.0:
            raise ValueError(f"tag {tid}: size_m {size} out of range")
        pose = tag_in_world(float(t["x"]), float(t["y"]), float(t["z"]), math.radians(float(t["yaw_deg"])))
        tags[tid] = Tag(tid, size, pose)
    return tags


def load_camera(path: Path) -> Camera:
    d = json.loads(path.read_text(encoding="utf-8"))
    k = np.array([[d["fx"], 0.0, d["cx"]], [0.0, d["fy"], d["cy"]], [0.0, 0.0, 1.0]], dtype=float)
    m = d["mount"]
    mount = cam_in_robot(m["x"], m["y"], m["z"], math.radians(m["yaw_deg"]), math.radians(m["pitch_deg"]))
    return Camera(k, np.array(d.get("dist", [0.0] * 5), dtype=float), int(d["width"]), int(d["height"]), mount)
