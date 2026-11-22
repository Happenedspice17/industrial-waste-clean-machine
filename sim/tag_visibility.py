#!/usr/bin/env python3
"""Tag layout check (simulation, SR-018): share of robot poses in the cell that see >= 1 usable tag.

Uses the same frames and gates as linux/vision. Ignores occlusion by machines and people (optimistic).
Usage: python sim/tag_visibility.py [tag_map.json] [camera.json]
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from linux.vision.config import Camera, Tag, load_camera, load_tag_map  # noqa: E402
from linux.vision.detector import tag_corners  # noqa: E402
from linux.vision.geometry import inv_tf, robot_in_world  # noqa: E402
from linux.vision.localizer import Gates  # noqa: E402

CFG = ROOT / "linux" / "vision" / "config"
HOME_GAP = 0.40
HOME_DOCK_M = 1.0


def station_layout(
    width: float, height: float, spacing: float, z: float, size: float, *, pair_gap: float = 0.60
) -> dict:
    """Stations of two tags ``pair_gap`` m apart on the four walls, facing inwards, one every ``spacing`` m.

    IDs go counter-clockwise from the (0, 0) corner. A home station (IDs 100, 101) sits on the y = 0 wall at x = 1.5 m
    with the dock 1.0 m in front of it, robot facing the tags: both home tags stay in a 60 deg view while docked.
    """
    tags = []
    walls = [(width, 90.0, "x"), (height, 180.0, "y"), (width, 270.0, "-x"), (height, 0.0, "-y")]
    for length, yaw, axis in walls:
        n = max(1, round(length / spacing))
        for i in range(n):
            centre = (i + 0.5) * length / n
            if axis == "x" and abs(centre - 1.5) < spacing / 2:
                continue
            for off in (-pair_gap / 2, pair_gap / 2):
                s = centre + off
                x, y = {"x": (s, 0.0), "y": (width, s), "-x": (width - s, height), "-y": (0.0, height - s)}[axis]
                tags.append({"id": len(tags), "x": round(x, 3), "y": round(y, 3), "z": z, "yaw_deg": yaw})
    for i, off in enumerate((-HOME_GAP / 2, HOME_GAP / 2)):
        tags.append({"id": 100 + i, "x": round(1.5 + off, 3), "y": 0.0, "z": z, "yaw_deg": 90.0})
    home = {"tags": [100, 101], "dock": {"x": 1.5, "y": HOME_DOCK_M, "yaw_deg": 270.0}, "approach_m": 1.0}
    return {
        "family": "tag36h11",
        "tag_size_m": size,
        "source": "example layout (simulation)",
        "tags": tags,
        "home": home,
    }


def visible(tag: Tag, cam: Camera, robot: np.ndarray, g: Gates) -> bool:
    cam_from_tag = inv_tf(robot @ cam.mount) @ tag.pose
    pts = (cam_from_tag[:3, :3] @ tag_corners(tag.size).T).T + cam_from_tag[:3, 3]
    if np.any(pts[:, 2] <= 0.05):
        return False
    uv = (cam.matrix @ (pts / pts[:, 2:3]).T).T[:, :2]
    if np.any(uv < 0) or np.any(uv[:, 0] >= cam.width) or np.any(uv[:, 1] >= cam.height):
        return False
    side = float(np.mean(np.linalg.norm(uv - np.roll(uv, 1, axis=0), axis=1)))
    p = inv_tf(cam_from_tag)[:3, 3]
    dist = float(np.linalg.norm(p))
    view = math.degrees(math.acos(float(p[2]) / dist))
    return side >= g.min_side_px and dist <= g.max_range_m and view <= g.max_view_deg


def coverage(tags: dict[int, Tag], cam: Camera, width: float, height: float, step: float = 0.25) -> dict[str, float]:
    g = Gates()
    headings = {"along x (0/180 deg)": (0.0, 180.0), "all 8 headings": tuple(range(0, 360, 45))}
    out = {}
    for name, hs in headings.items():
        hit = total = 0
        for x in np.arange(0.5, width - 0.5 + 1e-9, step):
            for y in np.arange(0.5, height - 0.5 + 1e-9, step):
                for h in hs:
                    robot = robot_in_world(float(x), float(y), math.radians(h))
                    total += 1
                    hit += any(visible(t, cam, robot, g) for t in tags.values())
        out[name] = hit / total
    return out


def route_gaps(
    tags: dict[int, Tag], cam: Camera, width: float, height: float, lane: float = 0.5
) -> tuple[float, float]:
    """Boustrophedon along x, lanes ``lane`` m apart. Returns (longest, mean) metres without a usable tag."""
    g = Gates()
    gaps, run, step = [], 0.0, 0.05
    for i, y in enumerate(np.arange(0.5, height - 0.5 + 1e-9, lane)):
        xs = np.arange(0.5, width - 0.5 + 1e-9, step)
        heading = 0.0 if i % 2 == 0 else math.pi
        for x in xs if i % 2 == 0 else xs[::-1]:
            robot = robot_in_world(float(x), float(y), heading)
            if any(visible(t, cam, robot, g) for t in tags.values()):
                if run > 0:
                    gaps.append(run)
                run = 0.0
            else:
                run += step
    gaps.append(run)
    return max(gaps), float(np.mean(gaps))


def main() -> int:
    tag_path = Path(sys.argv[1]) if len(sys.argv) > 1 else CFG / "tag_map.example.json"
    cam_path = Path(sys.argv[2]) if len(sys.argv) > 2 else CFG / "camera.example.json"
    tags, cam = load_tag_map(tag_path), load_camera(cam_path)
    xs = [float(t.pose[0, 3]) for t in tags.values()]
    ys = [float(t.pose[1, 3]) for t in tags.values()]
    res = coverage(tags, cam, max([*xs, 1.0]), max([*ys, 1.0]))
    print(f"{len(tags)} tags · poses with >= 1 usable tag (simulation, no occlusion):")
    for k, v in res.items():
        print(f"  {k}: {v * 100:.1f} %")
    longest, mean = route_gaps(tags, cam, max([*xs, 1.0]), max([*ys, 1.0]))
    print(f"  coverage route: longest stretch without a tag {longest:.1f} m, mean gap {mean:.1f} m")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--layout":
        print(json.dumps(station_layout(12.0, 8.0, 3.0, 0.9, 0.16), indent=2))
        sys.exit(0)
    sys.exit(main())
