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
class Home:
    """Docking station marked by two tags (ADR-0008): dock pose = where the robot stops, facing the tags."""

    tags: tuple[int, ...]
    dock: tuple[float, float, float]
    approach_m: float


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


def load_home(path: Path, tags: dict[int, Tag]) -> Home | None:
    data = json.loads(path.read_text(encoding="utf-8")).get("home")
    if data is None:
        return None
    ids = tuple(int(i) for i in data["tags"])
    if len(ids) < 2 or any(i not in tags for i in ids):
        raise ValueError("home needs at least two tags that are in the tag map")
    d = data["dock"]
    return Home(ids, (float(d["x"]), float(d["y"]), math.radians(float(d["yaw_deg"]))), float(data["approach_m"]))


def load_cameras(path: Path) -> list[Camera]:
    """One file per camera now; a list file ``{"cameras": [...paths]}`` when the four cameras arrive (ADR-0008)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if "cameras" not in data:
        return [load_camera(path)]
    return [load_camera(path.parent / c) for c in data["cameras"]]
