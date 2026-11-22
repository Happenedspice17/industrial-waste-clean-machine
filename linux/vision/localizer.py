"""Robot pose from AprilTag corners with gating and 2-read confirmation (SR-018, SR-017, lesson 4).

The robot stands on the floor and the camera mount is measured, so only (x, y, yaw) is unknown. Solving those 3 DOF
from the 4 corners is far less noisy than trusting a single tag's full 6-DOF orientation (simulation, test_vision).
Output is a pose correction for the Linux navigator only; it never commands motion and the MCU keeps its own stops
(ADR-0002). ``NAV_ENABLED`` stays False until TP-V02 passes and its report is committed (SR-017).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import cv2
import numpy as np

from linux.vision.config import Camera, Tag
from linux.vision.detector import Observation, tag_corners
from linux.vision.geometry import Mat, inv_tf, robot_in_world, wrap, yaw_of

NAV_ENABLED = False

Pose = tuple[float, float, float]


@dataclass(frozen=True)
class Gates:
    """Initial values (estimate). Replace with midpoints of TP-V02 measurements (rule 5)."""

    max_range_m: float = 4.0
    max_view_deg: float = 60.0
    max_reproj_px: float = 1.5
    min_side_px: float = 20.0
    pixel_sigma: float = 0.5
    yaw_prior_deg: float = 3.0
    jump_m: float = 0.30
    jump_deg: float = 10.0
    confirm_m: float = 0.15
    confirm_deg: float = 5.0
    votes_needed: int = 2
    votes_cap: int = 3


@dataclass
class Fix:
    status: str
    pose: Pose | None = None
    ids: list[int] = field(default_factory=list)
    rejected: dict[int, str] = field(default_factory=dict)

    @property
    def use_for_nav(self) -> bool:
        return NAV_ENABLED and self.status == "accepted"


def project(pose: Pose, world_pts: Mat, cam: Camera) -> Mat:
    cam_from_world = inv_tf(robot_in_world(*pose) @ cam.mount)
    rvec, _ = cv2.Rodrigues(cam_from_world[:3, :3])
    uv, _ = cv2.projectPoints(world_pts, rvec, cam_from_world[:3, 3], cam.matrix, cam.dist)
    return uv.reshape(-1, 2)


def reproj_rms(pose: Pose, world_pts: Mat, img: Mat, cam: Camera) -> float:
    return float(np.sqrt(np.mean(np.sum((project(pose, world_pts, cam) - img) ** 2, axis=1))))


def _residual(p: Mat, world_pts: Mat, img: Mat, cam: Camera, *, prior_yaw: float | None, g: Gates) -> Mat:
    r = (project((p[0], p[1], p[2]), world_pts, cam) - img).ravel() / g.pixel_sigma
    if prior_yaw is None:
        return r
    return np.append(r, wrap(p[2] - prior_yaw) / math.radians(g.yaw_prior_deg))


def solve_planar(world_pts: Mat, img: Mat, cam: Camera, guess: Pose, *, prior_yaw: float | None, g: Gates) -> Pose:
    """Levenberg-Marquardt on (x, y, yaw): corner reprojection error plus an optional IMU heading prior.

    One small tag far away constrains heading weakly (lateral offset and yaw look alike), so the IMU heading, which is
    the heading authority (docs/02-architecture.md), anchors yaw; two or more spread tags outweigh the prior.
    """
    p = np.array(guess, dtype=float)
    lam = 1e-3
    err = _residual(p, world_pts, img, cam, prior_yaw=prior_yaw, g=g)
    for _ in range(30):
        jac = np.empty((err.size, 3))
        for k, h in enumerate((1e-4, 1e-4, 1e-5)):
            dp = p.copy()
            dp[k] += h
            jac[:, k] = (_residual(dp, world_pts, img, cam, prior_yaw=prior_yaw, g=g) - err) / h
        step = np.linalg.solve(jac.T @ jac + lam * np.eye(3), -jac.T @ err)
        trial = p + step
        trial_err = _residual(trial, world_pts, img, cam, prior_yaw=prior_yaw, g=g)
        if trial_err @ trial_err < err @ err:
            p, err, lam = trial, trial_err, lam * 0.3
            if np.max(np.abs(step)) < 1e-7:
                break
        else:
            lam *= 10
    return float(p[0]), float(p[1]), wrap(float(p[2]))


def _world_corners(tag: Tag) -> Mat:
    return (tag.pose[:3, :3] @ tag_corners(tag.size).T).T + tag.pose[:3, 3]


def _guesses(obs: Observation, tag: Tag, cam: Camera, odom: Pose | None) -> list[Pose]:
    """Seeds: both IPPE solutions flattened onto the floor, plus odometry."""
    out = [odom] if odom else []
    n, rvecs, tvecs, _ = cv2.solvePnPGeneric(
        tag_corners(tag.size), obs.corners, cam.matrix, cam.dist, flags=cv2.SOLVEPNP_IPPE_SQUARE
    )
    for r, t in zip(rvecs[:n], tvecs[:n], strict=True):
        cam_from_tag = np.eye(4)
        cam_from_tag[:3, :3] = cv2.Rodrigues(r)[0]
        cam_from_tag[:3, 3] = np.asarray(t).reshape(3)
        robot = tag.pose @ inv_tf(cam_from_tag) @ inv_tf(cam.mount)
        out.append((float(robot[0, 3]), float(robot[1, 3]), yaw_of(robot)))
    return out


def _check(obs: Observation, tag: Tag, cam: Camera, g: Gates, odom: Pose | None) -> Pose | str:
    if obs.side_px < g.min_side_px:
        return f"side {obs.side_px:.0f} px"
    world = _world_corners(tag)
    prior = odom[2] if odom else None
    sols = [solve_planar(world, obs.corners, cam, s, prior_yaw=prior, g=g) for s in _guesses(obs, tag, cam, odom)]
    if not sols:
        return "no pose"
    pose = min(
        sols, key=lambda s: float(np.sum(_residual(np.array(s), world, obs.corners, cam, prior_yaw=prior, g=g) ** 2))
    )
    rms = reproj_rms(pose, world, obs.corners, cam)
    cam_in_tag = inv_tf(tag.pose) @ robot_in_world(*pose) @ cam.mount
    p = cam_in_tag[:3, 3]
    dist = float(np.linalg.norm(p))
    view = math.degrees(math.acos(max(-1.0, min(1.0, float(p[2]) / dist))))
    for bad, why in [
        (rms > g.max_reproj_px, f"reproj {rms:.2f} px"),
        (dist > g.max_range_m, f"range {dist:.2f} m"),
        (view > g.max_view_deg, f"view {view:.0f} deg"),
    ]:
        if bad:
            return why
    return pose


def _diff(a: Pose, b: Pose) -> Pose:
    return a[0] - b[0], a[1] - b[1], wrap(a[2] - b[2])


def _small(d: Pose, lin: float, ang_deg: float) -> bool:
    return math.hypot(d[0], d[1]) <= lin and abs(math.degrees(d[2])) <= ang_deg


class Localizer:
    def __init__(self, tags: dict[int, Tag], cam: Camera, gates: Gates | None = None) -> None:
        self.tags = tags
        self.cam = cam
        self.g = gates or Gates()
        self._pending: Pose | None = None
        self._votes = 0

    def update(self, observations: list[Observation], odom: Pose | None) -> Fix:
        """``odom``: current dead-reckoning pose in the world frame (encoders + IMU), or None before first fix."""
        good: list[tuple[Observation, Pose]] = []
        fix = Fix("none")
        for obs in observations:
            tag = self.tags.get(obs.id)
            res = _check(obs, tag, self.cam, self.g, odom) if tag else "not in map"
            if isinstance(res, str):
                fix.rejected[obs.id] = res
            else:
                good.append((obs, res))
                fix.ids.append(obs.id)
        if not good:
            fix.status = "rejected" if fix.rejected else "none"
            return fix
        world = np.vstack([_world_corners(self.tags[o.id]) for o, _ in good])
        img = np.vstack([o.corners for o, _ in good])
        fix.pose = solve_planar(world, img, self.cam, good[0][1], prior_yaw=odom[2] if odom else None, g=self.g)
        offset = _diff(fix.pose, odom) if odom else fix.pose
        if odom and _small(offset, self.g.jump_m, self.g.jump_deg):
            self._pending, self._votes = None, 0
            fix.status = "accepted"
            return fix
        if self._pending is not None and _small(_diff(offset, self._pending), self.g.confirm_m, self.g.confirm_deg):
            self._votes = min(self._votes + 1, self.g.votes_cap)
        else:
            self._votes = 1
        self._pending = offset
        if self._votes >= self.g.votes_needed:
            self._pending, self._votes = None, 0
            fix.status = "accepted"
        else:
            fix.status = "pending"
        return fix
