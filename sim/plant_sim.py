#!/usr/bin/env python3
"""Whole-mission simulation over random plant cells (simulation only; never physical evidence).

Per map: random cell, machines, columns, tag stations (pairs) on walls and machine faces, a home pair, 1-3 walking
people. The robot runs the boustrophedon route with drifting odometry + IMU, sees tags with one forward camera
(FOV, size, range, occlusion by machines and people, pixel noise, missed detections, rare outliers), fuses fixes with
the real ``Localizer``, slows down in caution mode (``Caution``), stops like the MCU would for close people, fills the
tank (ultrasonic level filter mirror), returns home on FULL or at the end of the round, docks with ``Docking``,
empties and resumes. Every 5th map has one wall tag moved after the survey (map not updated).

Usage: python sim/plant_sim.py [--maps 20] [--seed 0] [--jobs 4] [--out sim/out/plant] [--docs]
"""

from __future__ import annotations

import argparse
import csv
import heapq
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from linux.nav.caution import Caution  # noqa: E402
from linux.nav.home import DOCKED, FAILED, Docking  # noqa: E402
from linux.vision.config import Home, Tag, load_camera  # noqa: E402
from linux.vision.detector import Observation, tag_corners  # noqa: E402
from linux.vision.geometry import inv_tf, robot_in_world, tag_in_world, wrap  # noqa: E402
from linux.vision.localizer import Fix, Gates, Localizer  # noqa: E402
from linux.vision.people import Person  # noqa: E402
from sim import level_model  # noqa: E402
from sim.tag_visibility import HOME_DOCK_M, HOME_GAP, visible  # noqa: E402

CAM = load_camera(ROOT / "linux" / "vision" / "config" / "camera.example.json")
RES = 0.1
ROBOT_R = 0.30
CLEARANCE = 0.10
NOZZLE_W = 0.40
LANE = 0.35
TAG_Z, TAG_SIZE, PAIR_GAP = 0.9, 0.16, 0.60
V_CLEAN, V_TRANSIT = 0.15, 0.30
DT, CAM_EVERY = 0.1, 5
PERSON_R, PERSON_V = 0.25, 1.0
MCU_STOP_M = 0.6
HFOV = math.atan(CAM.matrix[0, 2] / CAM.matrix[0, 0])

Rect = tuple[float, float, float, float]


@dataclass
class World:
    w: float
    h: float
    machines: list[Rect]
    tags: dict[int, Tag]
    true_tags: dict[int, Tag]
    home: Home
    moved_tag: int | None
    people: int
    spill_full_frac: float


@dataclass
class Result:
    map_id: int
    size_m: str
    machines: int
    tag_count: int
    people: int
    moved_tag: int
    coverage_pct: float = 0.0
    pose_err_mean_m: float = 0.0
    pose_err_p95_m: float = 0.0
    pose_err_max_m: float = 0.0
    odom_only_final_err_m: float = 0.0
    frames_multi_pct: float = 0.0
    frames_fix_pct: float = 0.0
    longest_no_fix_m: float = 0.0
    caution_pct: float = 0.0
    mcu_stops: int = 0
    lidar_stops: int = 0
    contacts: int = 0
    machine_hits: int = 0
    full_returns: int = 0
    docks_ok: int = 0
    docks_failed: int = 0
    dock_err_max_m: float = 0.0
    moved_tag_bad_fixes: int = 0
    skipped_segments: int = 0
    recoveries: int = 0
    completed: bool = False
    minutes: float = 0.0
    trace: list[tuple[float, float, float, float, str]] = field(default_factory=list, repr=False)


# ---------------------------------------------------------------- map
def _overlap(a: Rect, b: Rect, gap: float) -> bool:
    return not (a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1])


def make_world(seed: int) -> World:
    rng = np.random.default_rng(seed)
    w, h = float(rng.uniform(10, 18)), float(rng.uniform(8, 12))
    machines: list[Rect] = []
    keep_out = (0.0, 0.0, 3.5, HOME_DOCK_M + 1.8)
    for _ in range(200):
        if len(machines) >= int(rng.integers(2, 6)):
            break
        mw, mh = (
            (float(rng.uniform(0.4, 0.5)),) * 2 if rng.random() < 0.3 else tuple(rng.uniform([1.0, 1.0], [3.0, 2.5]))
        )
        x0, y0 = float(rng.uniform(1.3, w - 1.3 - mw)), float(rng.uniform(1.3, h - 1.3 - mh))
        r = (x0, y0, x0 + mw, y0 + mh)
        if not _overlap(r, keep_out, 0.5) and all(not _overlap(r, m, 1.3) for m in machines):
            machines.append(r)
    specs: list[tuple[float, float, float]] = []

    def station(cx: float, cy: float, yaw_deg: float) -> None:
        ux, uy = -math.sin(math.radians(yaw_deg)), math.cos(math.radians(yaw_deg))
        for off in (-PAIR_GAP / 2, PAIR_GAP / 2):
            specs.append((cx + ux * off, cy + uy * off, yaw_deg))

    for length, yaw, pos in [
        (w, 90.0, lambda s: (s, 0.0)),
        (h, 180.0, lambda s: (w, s)),
        (w, 270.0, lambda s: (w - s, h)),
        (h, 0.0, lambda s: (0.0, h - s)),
    ]:
        n = max(1, round(length / 3.0))
        for i in range(n):
            s = (i + 0.5) * length / n
            if yaw == 90.0 and s < 3.5:
                continue
            station(*pos(s), yaw)
    for m in machines:
        if m[2] - m[0] < 0.8 or m[3] - m[1] < 0.8:
            continue
        face = int(rng.integers(4))
        cx, cy = (m[0] + m[2]) / 2, (m[1] + m[3]) / 2
        station(
            *[(cx, m[1] - 0.01, 270.0), (m[2] + 0.01, cy, 0.0), (cx, m[3] + 0.01, 90.0), (m[0] - 0.01, cy, 180.0)][face]
        )
    tags = {i: Tag(i, TAG_SIZE, tag_in_world(x, y, TAG_Z, math.radians(yaw))) for i, (x, y, yaw) in enumerate(specs)}
    for i, off in enumerate((-HOME_GAP / 2, HOME_GAP / 2)):
        tags[100 + i] = Tag(100 + i, TAG_SIZE, tag_in_world(1.5 + off, 0.0, TAG_Z, math.radians(90)))
    true_tags = dict(tags)
    moved = None
    if seed % 5 == 4:
        moved = int(rng.choice([i for i in tags if i < 100]))
        t = tags[moved]
        shift = t.pose.copy()
        shift[:3, 3] += t.pose[:3, 0] * 0.5
        true_tags[moved] = Tag(moved, t.size, shift)
    home = Home((100, 101), (1.5, HOME_DOCK_M, math.radians(270)), 1.0)
    return World(w, h, machines, tags, true_tags, home, moved, int(rng.integers(1, 4)), float(rng.uniform(0.5, 1.4)))


# ---------------------------------------------------------------- grid, planning, route
def grids(world: World) -> tuple[np.ndarray, np.ndarray]:
    nx, ny = round(world.w / RES), round(world.h / RES)
    xs = (np.arange(nx) + 0.5) * RES
    ys = (np.arange(ny) + 0.5) * RES
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    occ = np.zeros((nx, ny), bool)
    free = (gx > ROBOT_R) & (gx < world.w - ROBOT_R) & (gy > ROBOT_R) & (gy < world.h - ROBOT_R)
    for x0, y0, x1, y1 in world.machines:
        occ |= (gx >= x0) & (gx <= x1) & (gy >= y0) & (gy <= y1)
        dx = np.maximum(np.maximum(x0 - gx, 0), gx - x1)
        dy = np.maximum(np.maximum(y0 - gy, 0), gy - y1)
        free &= np.hypot(dx, dy) > ROBOT_R + CLEARANCE
    return occ, free


def astar(free: np.ndarray, a: tuple[float, float], b: tuple[float, float]) -> list[tuple[float, float]]:
    nx, ny = free.shape
    s = (min(nx - 1, int(a[0] / RES)), min(ny - 1, int(a[1] / RES)))
    g = (min(nx - 1, int(b[0] / RES)), min(ny - 1, int(b[1] / RES)))
    openq = [(0.0, s)]
    came: dict[tuple[int, int], tuple[int, int]] = {}
    cost = {s: 0.0}
    steps = [
        (1, 0, 1.0),
        (-1, 0, 1.0),
        (0, 1, 1.0),
        (0, -1, 1.0),
        (1, 1, 1.41),
        (1, -1, 1.41),
        (-1, 1, 1.41),
        (-1, -1, 1.41),
    ]
    while openq:
        _, cur = heapq.heappop(openq)
        if cur == g:
            break
        for dx, dy, c in steps:
            nb = (cur[0] + dx, cur[1] + dy)
            if not (0 <= nb[0] < nx and 0 <= nb[1] < ny) or (not free[nb] and nb != g):
                continue
            nc = cost[cur] + c
            if nc < cost.get(nb, 1e18):
                cost[nb], came[nb] = nc, cur
                heapq.heappush(openq, (nc + math.hypot(g[0] - nb[0], g[1] - nb[1]), nb))
    if g not in came and g != s:
        return [b]
    path, cur = [], g
    while cur != s:
        path.append(((cur[0] + 0.5) * RES, (cur[1] + 0.5) * RES))
        cur = came[cur]
    path.reverse()
    return [*path[::2], b]


def coverage_route(world: World, free: np.ndarray) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Clean segments (start, end) of a boustrophedon along x, lanes LANE m apart."""
    segs = []
    nx, ny = free.shape
    for k, y in enumerate(np.arange(ROBOT_R + 0.05, world.h - ROBOT_R, LANE)):
        j = min(ny - 1, int(y / RES))
        yc = (j + 0.5) * RES
        row = free[:, j]
        runs, start = [], None
        for i in range(nx + 1):
            on = i < nx and row[i]
            if on and start is None:
                start = i
            if not on and start is not None:
                if i - start >= 3:
                    runs.append(((start + 0.5) * RES, (i - 0.5) * RES))
                start = None
        lane = [((a, yc), (b, yc)) for a, b in runs]
        if k % 2:
            lane = [(e, s) for s, e in reversed(lane)]
        segs += lane
    return segs


# ---------------------------------------------------------------- sensing
def _seg_hits_rect(p: np.ndarray, q: np.ndarray, r: Rect) -> bool:
    t0, t1 = 0.0, 1.0
    d = q - p
    for k, lo, hi in ((0, r[0], r[2]), (1, r[1], r[3])):
        if abs(d[k]) < 1e-12:
            if p[k] < lo or p[k] > hi:
                return False
            continue
        a, b = (lo - p[k]) / d[k], (hi - p[k]) / d[k]
        t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
        if t0 > t1:
            return False
    return True


def observe(world: World, pose: np.ndarray, people: np.ndarray, rng: np.random.Generator) -> list[Observation]:
    robot = robot_in_world(*pose)
    cam_xy = (robot @ CAM.mount)[:2, 3]
    out = []
    for tid, tag in world.true_tags.items():
        if not visible(tag, CAM, robot, Gates(max_range_m=6.0, max_view_deg=75.0, min_side_px=12.0)):
            continue
        txy = tag.pose[:2, 3] + tag.pose[:2, 2] * 0.03
        if any(_seg_hits_rect(cam_xy, txy, m) for m in world.machines):
            continue
        if any(_point_seg_dist(pp, cam_xy, txy) < PERSON_R for pp in people):
            continue
        if rng.random() > 0.97:
            continue
        tf = inv_tf(robot @ CAM.mount) @ tag.pose
        pts = (tf[:3, :3] @ tag_corners(tag.size).T).T + tf[:3, 3]
        uv = (CAM.matrix @ (pts / pts[:, 2:3]).T).T[:, :2] + rng.normal(0, 0.4, (4, 2))
        if rng.random() < 0.01:
            uv[int(rng.integers(4))] += rng.normal(0, 3.0, 2)
        out.append(Observation(tid, uv))
    return out


def _rect_dist(p: np.ndarray, r: Rect) -> float:
    dx = max(r[0] - p[0], 0.0, p[0] - r[2])
    dy = max(r[1] - p[1], 0.0, p[1] - r[3])
    return math.hypot(dx, dy)


def _point_seg_dist(p: np.ndarray, a: np.ndarray, b: np.ndarray) -> float:
    d = b - a
    t = float(np.clip(np.dot(p - a, d) / max(float(d @ d), 1e-12), 0, 1))
    return float(np.linalg.norm(p - (a + t * d)))


def see_people(world: World, pose: np.ndarray, people: np.ndarray, rng: np.random.Generator) -> list[Person]:
    out = []
    for pp in people:
        rel = pp - pose[:2]
        dist = float(np.linalg.norm(rel))
        bearing = wrap(math.atan2(rel[1], rel[0]) - pose[2])
        if dist > 6.0 or abs(bearing) > HFOV or any(_seg_hits_rect(pose[:2], pp, m) for m in world.machines):
            continue
        if rng.random() < 0.85:
            out.append(Person(math.degrees(bearing), dist * float(rng.uniform(0.8, 1.2))))
    if rng.random() < 0.002:
        out.append(Person(0.0, float(rng.uniform(1, 5))))
    return out


# ---------------------------------------------------------------- mission
class Walkers:
    def __init__(self, world: World, free: np.ndarray, rng: np.random.Generator) -> None:
        self.rng, self.free = rng, free
        self.pos = np.array([self._spot() for _ in range(world.people)])
        self.goal = np.array([self._spot() for _ in range(world.people)])
        self.wait = np.zeros(world.people)

    def _spot(self) -> tuple[float, float]:
        idx = np.argwhere(self.free)
        i, j = idx[int(self.rng.integers(len(idx)))]
        return (i + 0.5) * RES, (j + 0.5) * RES

    def step(self, robot_xy: np.ndarray) -> None:
        """People walk to random goals; within 1.2 m of the robot they step away from it (they see it coming)."""
        for k in range(len(self.pos)):
            away = self.pos[k] - robot_xy
            da = float(np.linalg.norm(away))
            if da < 1.2:
                nxt = self.pos[k] + away / max(da, 1e-6) * PERSON_V * DT
                if self._is_free(nxt):
                    self.pos[k] = nxt
                    continue
            if self.wait[k] > 0:
                self.wait[k] -= DT
                continue
            d = self.goal[k] - self.pos[k]
            n = float(np.linalg.norm(d))
            if n < 0.1:
                self.goal[k] = self._spot()
                self.wait[k] = float(self.rng.uniform(0, 6))
                continue
            nxt = self.pos[k] + d / n * PERSON_V * DT
            if np.linalg.norm(nxt - robot_xy) >= 1.2:
                self.pos[k] = nxt
            else:
                self.goal[k] = self._spot()

    def _is_free(self, xy: np.ndarray) -> bool:
        i, j = int(xy[0] / RES), int(xy[1] / RES)
        return 0 <= i < self.free.shape[0] and 0 <= j < self.free.shape[1] and bool(self.free[i, j])


def follow(est: np.ndarray, target: tuple[float, float], v_max: float) -> tuple[float, float]:
    dx, dy = target[0] - est[0], target[1] - est[1]
    err = wrap(math.atan2(dy, dx) - est[2])
    w = float(np.clip(2.0 * err, -0.8, 0.8))
    v = v_max * max(0.0, math.cos(err)) if abs(err) < math.radians(35) else 0.0
    return v, w


class Mission:
    """One mission on one map. Mission modes: transit_clean -> clean -> ... -> go_home -> dock -> empty -> resume."""

    def __init__(self, map_id: int, seed: int) -> None:
        self.world = world = make_world(seed * 1000 + map_id)
        self.rng = rng = np.random.default_rng(seed * 7919 + map_id)
        self.occ, self.free = grids(world)
        self.segs = coverage_route(world, self.free)
        self.res = Result(
            map_id,
            f"{world.w:.1f}x{world.h:.1f}",
            len(world.machines),
            len(world.tags),
            world.people,
            -1 if world.moved_tag is None else world.moved_tag,
        )
        self.loc, self.caution, self.walkers = Localizer(world.tags, CAM), Caution(), Walkers(world, self.free, rng)
        self.level = level_model.Filter()
        area = float(self.free.sum()) * RES * RES
        self.fill_per_m2 = 1.0 / (area * world.spill_full_frac)
        self.tank = 0.0
        self.scale, self.bias, self.bias_rate = 1 + rng.normal(0, 0.01), 0.0, math.radians(0.3) / 60
        self.dock = world.home.dock
        self.true = np.array(self.dock)
        self.est, self.odo = self.true.copy(), self.true.copy()
        self.yaw_off = 0.0
        self.cleaned = np.zeros_like(self.free)
        nx, ny = self.free.shape
        self.gx, self.gy = np.meshgrid((np.arange(nx) + 0.5) * RES, (np.arange(ny) + 0.5) * RES, indexing="ij")
        self.target = self._target_cells()
        self.errs: list[float] = []
        self.frames = self.multi = self.fixes = self.cautious = self.steps = 0
        self.since_fix, self.longest = 0.0, 0.0
        self.mode, self.seg_i, self.resume_i = "transit_clean", 0, 0
        self.path: list[tuple[float, float]] = [(self.dock[0], self.dock[1] + 1.2)]
        self.docking: Docking | None = None
        self.empty_t, self.t, self.careful = 0.0, 0.0, False
        self.progress_t, self.progress_xy = 0.0, self.true[:2].copy()
        self.recover, self.blocked = 0, 0.0

    def _target_cells(self) -> np.ndarray:
        """Floor the nozzle can reach: within half a nozzle width of a cell the robot centre may occupy."""
        k = round(NOZZLE_W / 2 / RES)
        out = np.zeros_like(self.free)
        for dx in range(-k, k + 1):
            for dy in range(-k, k + 1):
                out |= np.roll(np.roll(self.free, dx, 0), dy, 1)
        return out & ~self.occ

    def run(self, max_minutes: float) -> Result:
        while self.t < max_minutes * 60 and self.mode != "done":
            self.step()
        return self.finish()

    def step(self) -> None:
        self.steps += 1
        self.walkers.step(self.true[:2])
        imu_yaw = self.true[2] + self.bias
        self.bias += self.rng.normal(0, self.bias_rate * math.sqrt(DT)) + self.bias_rate * DT * 0.2
        fix = self._camera(imu_yaw) if self.steps % CAM_EVERY == 0 else None
        if fix is None:
            self.careful = self.caution.update(self.t, [], None)
        self.cautious += self.careful
        v, w = self._recover() if self.recover > 0 else self._decide(fix)
        v_cmd = v
        v = self._limits(v)
        self.blocked = self.blocked + DT if v_cmd != 0 and v == 0 else 0.0
        if self.blocked > 3.0:
            self.recover, self.blocked = 30, 0.0
            self.res.recoveries += 1
        self._move(v, w)
        self.t += DT

    def _camera(self, imu_yaw: float) -> Fix:
        persons = see_people(self.world, self.true, self.walkers.pos, self.rng)
        lidar = min((float(np.linalg.norm(p - self.true[:2])) for p in self.walkers.pos), default=None)
        self.careful = self.caution.update(self.t, persons, lidar)
        obs = observe(self.world, self.true, self.walkers.pos, self.rng)
        fix = self.loc.update(obs, (float(self.est[0]), float(self.est[1]), float(self.est[2])), caution=self.careful)
        self.frames += 1
        if fix.status == "accepted" and fix.pose is not None:
            self.fixes += 1
            self.multi += fix.source == "multi"
            moved = self.world.moved_tag
            if moved in fix.ids and math.hypot(fix.pose[0] - self.true[0], fix.pose[1] - self.true[1]) > 0.3:
                self.res.moved_tag_bad_fixes += 1
            self.est[:] = fix.pose
            self.yaw_off = fix.pose[2] - imu_yaw
            self.longest, self.since_fix = max(self.longest, self.since_fix), 0.0
        return fix

    def _recover(self) -> tuple[float, float]:
        """Blocked by the LiDAR stop for 3 s: back up 0.3 m, then replan from the current estimate."""
        self.recover -= 1
        if self.recover == 0:
            if self.mode == "go_home":
                self._go_home()
            elif self.mode == "clean":
                self.seg_i += 1
                self.mode, self.path = "transit_clean", []
            else:
                self.path = []
        return -0.10, 0.0

    def _go_home(self) -> None:
        self.mode, self.path = "go_home", astar(self.free, (self.est[0], self.est[1]), docking_approach(self.world))

    def _follow_path(self, v_max: float) -> tuple[float, float] | None:
        """Follow ``self.path``; None when it is finished."""
        while self.path and math.hypot(self.path[0][0] - self.est[0], self.path[0][1] - self.est[1]) < 0.2:
            self.path.pop(0)
        return follow(self.est, self.path[0], v_max) if self.path else None

    def _transit(self) -> tuple[float, float] | None:
        if self.seg_i >= len(self.segs):
            self._go_home()
            return None
        if not self.path:
            self.path = astar(self.free, (self.est[0], self.est[1]), self.segs[self.seg_i][0])
        cmd = self._follow_path(V_TRANSIT)
        if cmd is None:
            self.mode = "clean"
        return cmd

    def _decide(self, fix: Fix | None) -> tuple[float, float]:
        if self.mode == "transit_clean":
            cmd = self._transit()
            if cmd is not None:
                return cmd
        if self.mode == "clean":
            seg = self.segs[self.seg_i]
            if math.hypot(seg[1][0] - self.est[0], seg[1][1] - self.est[1]) < 0.15 or _passed(self.est, seg):
                self.seg_i += 1
                self.mode, self.path = "transit_clean", []
                return 0.0, 0.0
            if self.level.state == level_model.FULL:
                self.res.full_returns += 1
                self.resume_i = self.seg_i
                self._go_home()
            else:
                return follow(self.est, seg[1], V_CLEAN)
        if self.mode == "go_home":
            cmd = self._follow_path(V_TRANSIT)
            if cmd is not None:
                return cmd
            self.mode, self.docking = "dock", Docking(self.world.home)
        if self.mode == "dock" and self.docking is not None:
            return self._dock(fix)
        if self.mode == "empty" and self.t - self.empty_t > 60:
            self.mode, self.path, self.seg_i = "transit_clean", [(self.dock[0], self.dock[1] + 1.2)], self.resume_i
        return 0.0, 0.0

    def _dock(self, fix: Fix | None) -> tuple[float, float]:
        assert self.docking is not None
        cmd = self.docking.step(
            self.t, (float(self.est[0]), float(self.est[1]), float(self.est[2])), fix or Fix("none")
        )
        if cmd.state not in (DOCKED, FAILED):
            return cmd.v, cmd.w
        ok = cmd.state == DOCKED
        self.res.docks_ok += ok
        self.res.docks_failed += not ok
        if ok:
            err = math.hypot(self.true[0] - self.dock[0], self.true[1] - self.dock[1])
            self.res.dock_err_max_m = round(max(self.res.dock_err_max_m, err), 3)
        if self.seg_i >= len(self.segs):
            self.mode = "done"
        else:
            self.mode, self.empty_t, self.tank, self.level = "empty", self.t, 0.0, level_model.Filter()
        return 0.0, 0.0

    def _limits(self, v: float) -> float:
        """Caution cap (Linux), then MCU stops: person close ahead, LiDAR obstacle at the nose."""
        if self.careful:
            v = self.caution.speed(v, True) if v > 0 else max(v, -0.10)
        tx, ty, tyaw = self.true
        for p in self.walkers.pos:
            close = np.linalg.norm(p - self.true[:2]) < MCU_STOP_M + ROBOT_R
            if v > 0 and close and abs(wrap(math.atan2(p[1] - ty, p[0] - tx) - tyaw)) < math.radians(60):
                self.res.mcu_stops += 1
                return 0.0
        nose = self.true[:2] + 0.1 * np.array([math.cos(tyaw), math.sin(tyaw)]) * np.sign(v)
        here = self.true[:2]
        if v != 0 and any(_rect_dist(nose, m) < min(ROBOT_R, _rect_dist(here, m)) for m in self.world.machines):
            self.res.lidar_stops += 1
            return 0.0
        return v

    def _move(self, v: float, w: float) -> None:
        true = self.true
        true[0] += v * math.cos(true[2]) * DT
        true[1] += v * math.sin(true[2]) * DT
        true[2] = wrap(true[2] + w * DT)
        for e in (self.est, self.odo):
            e[0] += v * self.scale * math.cos(e[2]) * DT
            e[1] += v * self.scale * math.sin(e[2]) * DT
        self.est[2] = wrap(true[2] + self.bias + self.yaw_off)
        self.odo[2] = wrap(true[2] + self.bias)
        self.since_fix += abs(v) * DT
        if v > 0 and any(np.linalg.norm(p - true[:2]) < ROBOT_R + PERSON_R - 0.05 for p in self.walkers.pos):
            self.res.contacts += 1
        if any(_rect_dist(true[:2], m) < ROBOT_R - 0.05 for m in self.world.machines):
            self.res.machine_hits += 1
        if self.mode == "clean":
            rx, ry = self.gx - true[0], self.gy - true[1]
            along = rx * math.cos(true[2]) + ry * math.sin(true[2])
            lat = -rx * math.sin(true[2]) + ry * math.cos(true[2])
            near = (np.abs(lat) <= NOZZLE_W / 2) & (along <= 0.05) & (along >= -0.05 - abs(v) * DT) & self.target
            self.tank += float((near & ~self.cleaned).sum()) * RES * RES * self.fill_per_m2
            self.cleaned |= near
        if self.steps % 2 == 0:
            d_mm = int(400 - 300 * min(self.tank, 1.2) + self.rng.normal(0, 4))
            self.level.add(max(0, d_mm), int(self.t * 1000))
        self.level.tick(int(self.t * 1000))
        self.errs.append(math.hypot(self.est[0] - true[0], self.est[1] - true[1]))
        self._stuck_check()
        if self.steps % 10 == 0:
            self.res.trace.append(
                (round(true[0], 2), round(true[1], 2), round(self.est[0], 2), round(self.est[1], 2), self.mode)
            )

    def _stuck_check(self) -> None:
        """No 0.3 m of progress in 90 s while moving between or along segments -> skip the segment (counted)."""
        if np.linalg.norm(self.true[:2] - self.progress_xy) > 0.3 or self.mode in ("empty", "dock", "done"):
            self.progress_t, self.progress_xy = self.t, self.true[:2].copy()
        elif self.t - self.progress_t > 90:
            self.res.skipped_segments += 1
            if self.mode in ("transit_clean", "clean"):
                self.seg_i += 1
                self.mode, self.path = "transit_clean", []
            else:
                self.path = astar(self.free, (self.est[0], self.est[1]), docking_approach(self.world))
            self.progress_t, self.progress_xy = self.t, self.true[:2].copy()

    def finish(self) -> Result:
        res, e = self.res, np.array(self.errs)
        res.coverage_pct = round(100 * float(self.cleaned.sum()) / max(1, int(self.target.sum())), 1)
        res.pose_err_mean_m = round(float(e.mean()), 3)
        res.pose_err_p95_m = round(float(np.percentile(e, 95)), 3)
        res.pose_err_max_m = round(float(e.max()), 3)
        res.odom_only_final_err_m = round(math.hypot(self.odo[0] - self.true[0], self.odo[1] - self.true[1]), 2)
        res.frames_multi_pct = round(100 * self.multi / max(1, self.frames), 1)
        res.frames_fix_pct = round(100 * self.fixes / max(1, self.frames), 1)
        res.longest_no_fix_m = round(max(self.longest, self.since_fix), 1)
        res.caution_pct = round(100 * self.cautious / max(1, self.steps), 1)
        res.minutes = round(self.t / 60, 1)
        res.completed = self.mode == "done"
        return res


def run_map(map_id: int, seed: int = 0, max_minutes: float = 240.0) -> Result:
    return Mission(map_id, seed).run(max_minutes)


def docking_approach(world: World) -> tuple[float, float]:
    x, y, yaw = world.home.dock
    return x - world.home.approach_m * math.cos(yaw), y - world.home.approach_m * math.sin(yaw)


def _passed(est: np.ndarray, seg: tuple[tuple[float, float], tuple[float, float]]) -> bool:
    (x0, _), (x1, _) = seg
    return (x1 - x0) * (est[0] - x1) > 0


# ---------------------------------------------------------------- output
def draw(world: World, res: Result, px: int = 30) -> Image.Image:
    img = Image.new("RGB", (int(world.w * px) + 20, int(world.h * px) + 34), "white")
    d = ImageDraw.Draw(img)

    def p(x: float, y: float) -> tuple[float, float]:
        return 10 + x * px, 10 + (world.h - y) * px

    d.rectangle([p(0, world.h), p(world.w, 0)], outline="black", width=2)
    for m in world.machines:
        d.rectangle([p(m[0], m[3]), p(m[2], m[1])], fill=(120, 120, 120))
    for tid, tag in world.true_tags.items():
        x, y = tag.pose[0, 3], tag.pose[1, 3]
        col = (0, 120, 0) if tid >= 100 else ((220, 0, 0) if tid == world.moved_tag else (0, 70, 200))
        d.rectangle([p(x - 0.1, y + 0.1), p(x + 0.1, y - 0.1)], fill=col)
    pts_true = [p(a, b) for a, b, *_ in res.trace]
    pts_est = [p(c, e) for _, _, c, e, _ in res.trace]
    if len(pts_true) > 1:
        d.line(pts_est, fill=(255, 150, 0), width=1)
        d.line(pts_true, fill=(0, 0, 0), width=1)
    d.text(
        (10, img.height - 20),
        f"map {res.map_id}: cov {res.coverage_pct}%  p95 {res.pose_err_p95_m} m  "
        f"docks {res.docks_ok}/{res.docks_ok + res.docks_failed}",
        fill="black",
    )
    return img


def montage(images: list[Image.Image], cols: int = 5) -> Image.Image:
    cw, ch = max(i.width for i in images), max(i.height for i in images)
    rows = math.ceil(len(images) / cols)
    out = Image.new("RGB", (cw * cols, ch * rows), "white")
    for k, im in enumerate(images):
        out.paste(im, ((k % cols) * cw, (k // cols) * ch))
    return out


COLS = [
    ("map_id", "Map"),
    ("size_m", "Cell m"),
    ("machines", "Mach."),
    ("people", "People"),
    ("moved_tag", "Moved tag"),
    ("coverage_pct", "Cover %"),
    ("pose_err_p95_m", "Pose p95 m"),
    ("pose_err_max_m", "Pose max m"),
    ("odom_only_final_err_m", "Odom-only end m"),
    ("frames_multi_pct", "Multi-tag frames %"),
    ("longest_no_fix_m", "Longest no fix m"),
    ("caution_pct", "Caution %"),
    ("contacts", "Contacts"),
    ("machine_hits", "Machine hits"),
    ("recoveries", "Recoveries"),
    ("full_returns", "Full returns"),
    ("docks_ok", "Docks ok"),
    ("docks_failed", "Docks failed"),
    ("dock_err_max_m", "Dock err max m"),
    ("moved_tag_bad_fixes", "Bad fixes moved tag"),
    ("minutes", "Min"),
]


def markdown(rows: list[dict[str, str]]) -> str:
    """Per-map table plus totals, from summary.csv rows."""
    head = "| " + " | ".join(t for _, t in COLS) + " |\n|" + "---|" * len(COLS) + "\n"
    body = "".join("| " + " | ".join(str(r[k]) for k, _ in COLS) + " |\n" for r in rows)

    def col(k: str) -> list[float]:
        return [float(r[k]) for r in rows]

    totals = (
        f"- Maps: {len(rows)}; completed: {sum(r['completed'] == 'True' for r in rows)}\n"
        f"- Coverage %: mean {np.mean(col('coverage_pct')):.1f}, min {min(col('coverage_pct')):.1f}\n"
        f"- Pose error p95 (m): median {np.median(col('pose_err_p95_m')):.3f}, worst {max(col('pose_err_p95_m')):.3f};"
        f" max over all maps {max(col('pose_err_max_m')):.3f}\n"
        f"- Odometry-only end error (m): median {np.median(col('odom_only_final_err_m')):.2f},"
        f" worst {max(col('odom_only_final_err_m')):.2f}\n"
        f"- Person contacts while moving: {int(sum(col('contacts')))}; machine hits: {int(sum(col('machine_hits')))}\n"
        f"- Dockings: {int(sum(col('docks_ok')))} ok, {int(sum(col('docks_failed')))} failed;"
        f" worst final error {max(col('dock_err_max_m')):.3f} m\n"
        f"- Returns on FULL level: {int(sum(col('full_returns')))}\n"
        f"- Bad fixes from moved tags: {int(sum(col('moved_tag_bad_fixes')))}"
        f" (maps with a moved tag: {sum(int(r['moved_tag']) >= 0 for r in rows)})\n"
    )
    return totals + "\n" + head + body


def _job(args: tuple[int, int]) -> tuple[Result, Image.Image]:
    map_id, seed = args
    res = run_map(map_id, seed)
    return res, draw(make_world(seed * 1000 + map_id), res)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--maps", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", type=Path, default=ROOT / "sim" / "out" / "plant")
    ap.add_argument("--docs", action="store_true", help="also write docs/sim/ summary and montage")
    ap.add_argument("--table", type=Path, help="only print the markdown table of an existing summary.csv")
    a = ap.parse_args(argv)
    if a.table:
        with a.table.open() as f:
            print(markdown(list(csv.DictReader(f))))
        return 0
    a.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(a.jobs) as ex:
        done = list(ex.map(_job, [(i, a.seed) for i in range(a.maps)]))
    rows = [{k: v for k, v in asdict(r).items() if k != "trace"} for r, _ in done]
    with (a.out / "summary.csv").open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    mont = montage([im for _, im in done])
    mont.save(a.out / "montage.png")
    for r, im in done:
        im.save(a.out / f"map_{r.map_id:02d}.png")
    for r in rows:
        print(r)
    if a.docs:
        docs = ROOT / "docs" / "sim"
        docs.mkdir(parents=True, exist_ok=True)
        mont.save(docs / "plant-sim-montage.png")
        (docs / "plant-sim-summary.csv").write_text((a.out / "summary.csv").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
