"""Robot pose from AprilTag corners (SR-018, SR-019, SR-017, ADR-0007, ADR-0008).

The robot stands on the floor and each camera mount is measured, so only (x, y, yaw) is unknown; it is solved from
tag corners by Levenberg-Marquardt. Trust rules:

* **Two or more tags in the same frame that agree with each other** (tag pair at a station, or any two mapped tags)
  are a cross-check on their own: the fix is accepted at once, solved jointly without the IMU prior, even if it is far
  from odometry. If they disagree, all are rejected (a tag was moved or misread).
* **One tag** constrains heading weakly: solved with the IMU heading prior; a jump from odometry needs a consistent
  read from a **different** tag (rule 6, lesson 4): the same tag seen again is not independent, so a moved tag seen
  alone can never pull the pose (found in simulation, docs/sim/plant-sim-20-maps.md).
* **Caution** (person or obstacle reported): multi-tag fixes also need 2 consistent reads.

Output is a pose correction for the Linux navigator only; it never commands motion and the MCU keeps its own stops
(ADR-0002). ``NAV_ENABLED`` stays False until TP-V02 passes and its report is committed (SR-017).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

import cv2
import numpy as np

from linux.vision.config import Camera, Tag
from linux.vision.detector import Observation, tag_corners
from linux.vision.geometry import Mat, inv_tf, robot_in_world, wrap, yaw_of

NAV_ENABLED = False

Pose = tuple[float, float, float]
Group = tuple[Mat, Mat, Camera]


@dataclass(frozen=True)
class Gates:
    """Initial values (estimate). Replace with midpoints of TP-V02 measurements (rule 5)."""

    max_range_m: float = 4.0
    max_view_deg: float = 60.0
    max_reproj_px: float = 1.5
    min_side_px: float = 20.0
    pixel_sigma: float = 0.5
    yaw_prior_deg: float = 3.0
    agree_m: float = 0.25
    agree_deg: float = 8.0
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
    source: str = ""
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


def reproj_rms(pose: Pose, groups: Sequence[Group]) -> float:
    err = np.vstack([project(pose, w, c) - i for w, i, c in groups])
    return float(np.sqrt(np.mean(np.sum(err**2, axis=1))))


def _residual(p: Mat, groups: Sequence[Group], *, prior_yaw: float | None, g: Gates) -> Mat:
    pose = (float(p[0]), float(p[1]), float(p[2]))
    r = np.concatenate([(project(pose, w, c) - i).ravel() for w, i, c in groups]) / g.pixel_sigma
    if prior_yaw is None:
        return r
    return np.append(r, wrap(p[2] - prior_yaw) / math.radians(g.yaw_prior_deg))


def solve_planar(groups: Sequence[Group], guess: Pose, *, prior_yaw: float | None, g: Gates) -> Pose:
    """Levenberg-Marquardt on (x, y, yaw): corner reprojection error plus an optional IMU heading prior."""
    p = np.array(guess, dtype=float)
    lam = 1e-3
    err = _residual(p, groups, prior_yaw=prior_yaw, g=g)
    for _ in range(30):
        jac = np.empty((err.size, 3))
        for k, h in enumerate((1e-4, 1e-4, 1e-5)):
            dp = p.copy()
            dp[k] += h
            jac[:, k] = (_residual(dp, groups, prior_yaw=prior_yaw, g=g) - err) / h
        step = np.linalg.solve(jac.T @ jac + lam * np.eye(3), -jac.T @ err)
        trial = p + step
        trial_err = _residual(trial, groups, prior_yaw=prior_yaw, g=g)
        if trial_err @ trial_err < err @ err:
            p, err, lam = trial, trial_err, lam * 0.3
            if np.max(np.abs(step)) < 1e-7:
                break
        else:
            lam *= 10
    return float(p[0]), float(p[1]), wrap(float(p[2]))


def world_corners(tag: Tag) -> Mat:
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
    grp = [(world_corners(tag), obs.corners, cam)]
    prior = odom[2] if odom else None
    sols = [solve_planar(grp, s, prior_yaw=prior, g=g) for s in _guesses(obs, tag, cam, odom)]
    if not sols:
        return "no pose"
    pose = min(sols, key=lambda s: float(np.sum(_residual(np.array(s), grp, prior_yaw=prior, g=g) ** 2)))
    rms = reproj_rms(pose, grp)
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
    def __init__(self, tags: dict[int, Tag], cams: Camera | Sequence[Camera], gates: Gates | None = None) -> None:
        self.tags = tags
        self.cams = [cams] if isinstance(cams, Camera) else list(cams)
        self.g = gates or Gates()
        self._pending: Pose | None = None
        self._pending_ids: set[int] = set()
        self._votes = 0

    def update(self, observations: list[Observation], odom: Pose | None, *, caution: bool = False) -> Fix:
        """``odom``: dead-reckoning pose (encoders + IMU) or None before the first fix.
        ``caution``: a person or obstacle is reported (camera or LiDAR); multi-tag fixes then also need 2 reads."""
        fix = Fix("none")
        good = self._screen(observations, odom, fix)
        if not good:
            fix.status = "rejected" if fix.rejected else "none"
            return fix
        multi = len(good) >= 2
        if multi and not all(_small(_diff(p, good[0][1]), self.g.agree_m, self.g.agree_deg) for _, p in good):
            fix.rejected.update({o.id: "tags disagree" for o, _ in good})
            fix.status = "rejected"
            self._pending, self._votes = None, 0
            return fix
        fix.ids = [o.id for o, _ in good]
        fix.source = "multi" if multi else "single"
        groups = [(world_corners(self.tags[o.id]), o.corners, self.cams[o.cam]) for o, _ in good]
        prior = None if multi else (odom[2] if odom else None)
        fix.pose = solve_planar(groups, good[0][1], prior_yaw=prior, g=self.g)
        if multi and not caution:
            return self._accept(fix)
        offset = _diff(fix.pose, odom) if odom else fix.pose
        if odom and _small(offset, self.g.jump_m, self.g.jump_deg):
            return self._accept(fix)
        ids = set(fix.ids)
        same = self._pending is not None and _small(_diff(offset, self._pending), self.g.confirm_m, self.g.confirm_deg)
        if same and (multi or not ids <= self._pending_ids):
            self._votes = min(self._votes + 1, self.g.votes_cap)
            self._pending_ids |= ids
        elif not same:
            self._votes, self._pending_ids = 1, ids
        self._pending = offset
        if self._votes >= self.g.votes_needed:
            return self._accept(fix)
        fix.status = "pending"
        return fix

    def _screen(self, observations: list[Observation], odom: Pose | None, fix: Fix) -> list[tuple[Observation, Pose]]:
        good = []
        for obs in observations:
            tag = self.tags.get(obs.id)
            if tag is None:
                res: Pose | str = "not in map"
            elif obs.cam >= len(self.cams):
                res = f"unknown camera {obs.cam}"
            else:
                res = _check(obs, tag, self.cams[obs.cam], self.g, odom)
            if isinstance(res, str):
                fix.rejected[obs.id] = res
            else:
                good.append((obs, res))
        return good

    def _accept(self, fix: Fix) -> Fix:
        self._pending, self._votes, self._pending_ids = None, 0, set()
        fix.status = "accepted"
        return fix
