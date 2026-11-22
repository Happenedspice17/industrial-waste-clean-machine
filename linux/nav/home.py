"""Return to home and dock on the two home tags (SR-023, ADR-0008).

After a suction round, or when the ultrasonic level reads full (SR-022), the planner brings the robot to the approach
point 1 m in front of the dock; this state machine then aligns on the home tag pair and drives straight in. It only
produces speed requests; the MCU executes them and stops by itself on bumpers, LiDAR stop zone or stale commands.
Docked is declared only on a fresh fix that sees both home tags (multi-tag trust, SR-019).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from linux.vision.config import Home
from linux.vision.geometry import wrap
from linux.vision.localizer import Fix, Pose

APPROACH, ALIGN, FINAL, BACK_OFF, DOCKED, FAILED = "approach", "align", "final", "back_off", "docked", "failed"


@dataclass(frozen=True)
class DockLimits:
    """Estimates; tune from TP-N01 (rule 5)."""

    approach_tol_m: float = 0.15
    align_tol_deg: float = 4.0
    dock_tol_m: float = 0.05
    dock_tol_deg: float = 3.0
    lost_s: float = 1.5
    abort_lateral_m: float = 0.25
    max_retries: int = 3
    v_transit: float = 0.30
    v_final: float = 0.08
    w_max: float = 0.6
    k_heading: float = 1.5
    k_lateral: float = 2.0


@dataclass(frozen=True)
class Command:
    v: float
    w: float
    state: str


def go_to(pose: Pose, target: tuple[float, float], v_max: float, lim: DockLimits) -> tuple[float, float]:
    dx, dy = target[0] - pose[0], target[1] - pose[1]
    err = wrap(math.atan2(dy, dx) - pose[2])
    w = max(-lim.w_max, min(lim.w_max, lim.k_heading * err))
    v = v_max * max(0.0, math.cos(err)) if abs(err) < math.radians(45) else 0.0
    return min(v, math.hypot(dx, dy)), w


class Docking:
    def __init__(self, home: Home, limits: DockLimits | None = None) -> None:
        self.home = home
        self.lim = limits or DockLimits()
        self.state = APPROACH
        self.retries = 0
        self._last_home_fix = -1e9
        self._home_pose: Pose | None = None
        x, y, yaw = home.dock
        self.approach = (x - home.approach_m * math.cos(yaw), y - home.approach_m * math.sin(yaw))

    def _sees_home(self, fix: Fix) -> bool:
        return fix.status == "accepted" and fix.source == "multi" and set(self.home.tags) <= set(fix.ids)

    def step(self, t: float, pose: Pose, fix: Fix) -> Command:
        """``pose``: current fused estimate; ``fix``: this frame's localizer output."""
        if self._sees_home(fix) and fix.pose is not None:
            self._last_home_fix, self._home_pose = t, fix.pose
        fresh = t - self._last_home_fix <= self.lim.lost_s
        handlers = {APPROACH: self._approach, ALIGN: self._align, FINAL: self._final, BACK_OFF: self._back_off}
        for _ in range(len(handlers)):
            handler = handlers.get(self.state)
            if handler is None:
                break
            cmd = handler(pose, fresh)
            if cmd is not None:
                return cmd
        return Command(0.0, 0.0, self.state)

    def _near_approach(self, pose: Pose) -> bool:
        return math.hypot(self.approach[0] - pose[0], self.approach[1] - pose[1]) <= self.lim.approach_tol_m

    def _approach(self, pose: Pose, fresh: bool) -> Command | None:
        if self._near_approach(pose):
            self.state = ALIGN
            return None
        return Command(*go_to(pose, self.approach, self.lim.v_transit, self.lim), APPROACH)

    def _align(self, pose: Pose, fresh: bool) -> Command | None:
        err = wrap(self.home.dock[2] - pose[2])
        if abs(math.degrees(err)) <= self.lim.align_tol_deg and fresh:
            self.state = FINAL
            return None
        return Command(0.0, max(-self.lim.w_max, min(self.lim.w_max, self.lim.k_heading * err)), ALIGN)

    def _final(self, pose: Pose, fresh: bool) -> Command:
        lim = self.lim
        if not fresh:
            return self._retry()
        p = self._home_pose if self._home_pose is not None else pose
        dock_x, dock_y, dock_yaw = self.home.dock
        c, s = math.cos(dock_yaw), math.sin(dock_yaw)
        along = (dock_x - p[0]) * c + (dock_y - p[1]) * s
        lateral = -(dock_x - p[0]) * s + (dock_y - p[1]) * c
        yaw_err = wrap(dock_yaw - p[2])
        tol = lim.dock_tol_m
        if abs(along) <= tol and abs(lateral) <= tol and abs(math.degrees(yaw_err)) <= lim.dock_tol_deg:
            self.state = DOCKED
            return Command(0.0, 0.0, DOCKED)
        if along < -tol or abs(lateral) > lim.abort_lateral_m:
            return self._retry()
        w = lim.k_heading * yaw_err + lim.k_lateral * lateral
        return Command(min(lim.v_final, max(0.0, along)), max(-lim.w_max, min(lim.w_max, w)), FINAL)

    def _back_off(self, pose: Pose, fresh: bool) -> Command:
        """Reverse straight out until the robot is back on the approach line, then align again."""
        dock_x, dock_y, dock_yaw = self.home.dock
        back = -((pose[0] - dock_x) * math.cos(dock_yaw) + (pose[1] - dock_y) * math.sin(dock_yaw))
        if back >= self.home.approach_m - self.lim.approach_tol_m:
            self.state = APPROACH
            return Command(0.0, 0.0, APPROACH)
        return Command(-self.lim.v_final, 0.0, BACK_OFF)

    def _retry(self) -> Command:
        self.retries += 1
        self.state = FAILED if self.retries > self.lim.max_retries else BACK_OFF
        return Command(0.0, 0.0, self.state)
