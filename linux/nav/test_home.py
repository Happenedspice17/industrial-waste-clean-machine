"""Docking on the home tag pair (SR-023): closed loop with synthetic tag corners (simulation, not field data)."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from linux.nav.fusion import PoseFusion
from linux.nav.home import DOCKED, FAILED, Docking
from linux.vision.config import load_camera, load_home, load_tag_map
from linux.vision.detector import Observation, tag_corners
from linux.vision.geometry import inv_tf, robot_in_world
from linux.vision.localizer import Fix, Gates, Localizer
from sim.tag_visibility import visible

CFG = Path(__file__).resolve().parents[1] / "vision" / "config"
TAGS = load_tag_map(CFG / "tag_map.example.json")
HOME = load_home(CFG / "tag_map.example.json", TAGS)
CAM = load_camera(CFG / "camera.example.json")


def observe(pose: tuple[float, float, float], rng: np.random.Generator, ids: tuple[int, ...]) -> list[Observation]:
    robot = robot_in_world(*pose)
    out = []
    for tid in ids:
        tag = TAGS[tid]
        if not visible(tag, CAM, robot, Gates()):
            continue
        tf = inv_tf(robot @ CAM.mount) @ tag.pose
        pts = (tf[:3, :3] @ tag_corners(tag.size).T).T + tf[:3, 3]
        uv = (CAM.matrix @ (pts / pts[:, 2:3]).T).T[:, :2]
        out.append(Observation(tid, uv + rng.normal(0.0, 0.3, uv.shape)))
    return out


def run(start: tuple[float, float, float], ids: tuple[int, ...], seconds: float = 120.0) -> tuple[str, tuple]:
    assert HOME is not None
    rng = np.random.default_rng(3)
    dock, loc = Docking(HOME), Localizer(TAGS, CAM)
    true = list(start)
    est = [start[0] + 0.10, start[1] - 0.08, start[2] + math.radians(3)]
    t, dt = 0.0, 0.1
    while t < seconds:
        fix = loc.update(observe(tuple(true), rng, ids), tuple(est)) if ids else Fix("none")
        if fix.status == "accepted" and fix.pose is not None:
            est = list(fix.pose)
        cmd = dock.step(t, tuple(est), fix)
        if cmd.state in {DOCKED, FAILED}:
            return cmd.state, tuple(true)
        for p in (true, est):
            p[0] += cmd.v * math.cos(p[2]) * dt
            p[1] += cmd.v * math.sin(p[2]) * dt
            p[2] += cmd.w * dt
        t += dt
    return "timeout", tuple(true)


@pytest.mark.parametrize("start", [(3.0, 2.5, math.radians(200)), (1.0, 2.6, math.radians(-60)), (2.4, 2.2, 4.0)])
def test_docks_within_tolerance(start: tuple[float, float, float]) -> None:
    state, end = run(start, HOME.tags if HOME else ())
    assert state == DOCKED
    assert math.hypot(end[0] - 1.5, end[1] - 1.0) < 0.07
    assert abs(math.degrees((end[2] - math.radians(270) + math.pi) % (2 * math.pi) - math.pi)) < 4.0


def test_fails_safe_without_home_tags() -> None:
    """No home tags in view: never declares docked; ends in FAILED after the retries."""
    state, _ = run((2.0, 1.8, math.radians(-90)), ())
    assert state in {FAILED, "timeout"}
    assert state != DOCKED


def test_fusion_trusts_fix_more_after_long_drive() -> None:
    f = PoseFusion((0.0, 0.0, 0.0))
    f.predict(0.5, 0.0, 0.0, 3.0)
    f.correct((0.6, 0.0, 0.0), 0.10, 3.0)
    small = f.x - 0.5
    g = PoseFusion((0.0, 0.0, 0.0))
    for _ in range(20):
        g.predict(0.5, 0.0, 0.0, 3.0)
    g.correct((10.1, 0.0, 0.0), 0.10, 3.0)
    assert 0 < small < 0.05
    assert g.x - 10.0 > 0.06
