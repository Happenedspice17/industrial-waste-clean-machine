"""Tests for single-camera AprilTag localization (SR-018, SR-017). Synthetic images = simulation, not field data."""

from __future__ import annotations

import json
import math
from pathlib import Path

import cv2
import numpy as np
import pytest

from linux.vision import localizer as loc
from linux.vision.config import Camera, Tag, load_camera, load_tag_map
from linux.vision.detector import DICT, Observation, detect, make_detector, tag_corners
from linux.vision.geometry import inv_tf, robot_in_world, tag_in_world
from sim import tag_accuracy
from tools import gen_apriltags

CFG = Path(__file__).parent / "config"
CAM = load_camera(CFG / "camera.example.json")
SIZE = 0.16
TAGS = {7: Tag(7, SIZE, tag_in_world(6.0, 8.0, 0.9, math.radians(270)))}


def cam_from_tag(robot: np.ndarray, tag: Tag, cam: Camera = CAM) -> np.ndarray:
    return inv_tf(robot @ cam.mount) @ tag.pose


def render(robot: np.ndarray, tag: Tag, tag_id: int, px: int = 400) -> np.ndarray:
    """Draw the tag (with white quiet zone) into the camera image by plane homography."""
    marker = cv2.aruco.generateImageMarker(cv2.aruco.getPredefinedDictionary(DICT), tag_id, px, borderBits=1)
    quiet = px // 8
    src = cv2.copyMakeBorder(marker, quiet, quiet, quiet, quiet, cv2.BORDER_CONSTANT, value=255)
    n = src.shape[0]
    m_per_px = tag.size / px
    c = (n / 2 - 0.5) * m_per_px
    to_plane = np.array([[m_per_px, 0, -c], [0, -m_per_px, c], [0, 0, 1]])
    tf = cam_from_tag(robot, tag)
    h = CAM.matrix @ np.column_stack([tf[:3, 0], tf[:3, 1], tf[:3, 3]]) @ to_plane
    out = cv2.warpPerspective(src, h, (CAM.width, CAM.height), flags=cv2.INTER_AREA, borderValue=128)
    mask = cv2.warpPerspective(np.ones_like(src), h, (CAM.width, CAM.height))
    return np.where(mask > 0, out, 128).astype(np.uint8)


def obs_at(robot: np.ndarray, tid: int = 7, noise_px: float = 0.0, seed: int = 0) -> Observation:
    """Exact projected corners plus optional Gaussian pixel noise (no image)."""
    tf = cam_from_tag(robot, TAGS[tid])
    pts = (tf[:3, :3] @ tag_corners(TAGS[tid].size).T).T + tf[:3, 3]
    uv = (CAM.matrix @ (pts / pts[:, 2:3]).T).T[:, :2]
    return Observation(tid, uv + np.random.default_rng(seed).normal(0.0, noise_px, uv.shape))


def test_geometry_round_trip_recovers_robot_pose() -> None:
    robot = robot_in_world(5.0, 5.5, math.radians(80))
    fix = loc.Localizer(TAGS, CAM).update([obs_at(robot)], odom=(5.0, 5.5, math.radians(80)))
    assert fix.status == "accepted"
    assert fix.pose == pytest.approx((5.0, 5.5, math.radians(80)), abs=1e-9)


@pytest.mark.parametrize(("x", "y", "yaw_deg"), [(6.0, 6.5, 90), (6.0, 5.5, 90), (4.5, 5.5, 70), (7.0, 5.5, 105)])
def test_detect_and_localize_from_synthetic_image(x: float, y: float, yaw_deg: float) -> None:
    """Rendered image -> detector -> localizer; IMU heading prior off by 1 deg; odometry off by 0.2 m."""
    robot = robot_in_world(x, y, math.radians(yaw_deg))
    obs = detect(render(robot, TAGS[7], 7), make_detector())
    assert [o.id for o in obs] == [7]
    fix = loc.Localizer(TAGS, CAM).update(obs, odom=(x + 0.2, y, math.radians(yaw_deg + 1)))
    assert fix.status == "accepted"
    assert fix.pose is not None
    assert math.hypot(fix.pose[0] - x, fix.pose[1] - y) < 0.10
    assert abs(math.degrees(fix.pose[2]) - yaw_deg) < 2.0


def test_unknown_tag_ids_are_rejected() -> None:
    robot = robot_in_world(6.0, 5.5, math.radians(90))
    obs = detect(render(robot, TAGS[7], 3), make_detector())
    assert [o.id for o in obs] == [3]
    fix = loc.Localizer(TAGS, CAM).update(obs, None)
    assert fix.status == "rejected"
    assert fix.rejected == {3: "not in map"}


def test_gate_rejects_far_small_tag() -> None:
    fix = loc.Localizer(TAGS, CAM).update([obs_at(robot_in_world(6.0, 0.5, math.pi / 2))], None)
    assert fix.status == "rejected"
    assert fix.rejected[7].startswith(("side", "range"))


def test_gate_rejects_corners_that_do_not_fit_the_floor() -> None:
    """A tag moved or a wrong map entry: corners cannot be explained by a robot on the floor."""
    obs = obs_at(robot_in_world(6.0, 5.5, math.pi / 2))
    warped = obs.corners.copy()
    warped[0] += (6.0, -6.0)
    fix = loc.Localizer(TAGS, CAM).update([Observation(7, warped)], None)
    assert fix.status == "rejected"
    assert fix.rejected[7].startswith("reproj")


def test_pixel_noise_monte_carlo() -> None:
    """Simulation (sim/tag_accuracy.py): one 0.16 m tag at 2.5 m, 0.3 px noise, 1.5 deg IMU prior error."""
    pos, ang = tag_accuracy.p95_error(2.5, 0.3, n=100)
    assert pos < 0.10
    assert ang < 2.5


def test_two_tags_fix_heading_without_prior() -> None:
    """Two spread tags pin heading without odometry (first fix at start-up)."""
    tags = {**TAGS, 8: Tag(8, SIZE, tag_in_world(4.0, 8.0, 0.9, math.radians(270)))}
    robot = robot_in_world(5.0, 5.5, math.radians(95))
    obs = []
    for tid in (7, 8):
        tf = inv_tf(robot @ CAM.mount) @ tags[tid].pose
        pts = (tf[:3, :3] @ tag_corners(SIZE).T).T + tf[:3, 3]
        uv = (CAM.matrix @ (pts / pts[:, 2:3]).T).T[:, :2]
        obs.append(Observation(tid, uv + np.random.default_rng(tid).normal(0.0, 0.3, uv.shape)))
    lz = loc.Localizer(tags, CAM)
    lz.update(obs, None)
    fix = lz.update(obs, None)
    assert fix.status == "accepted"
    assert fix.pose is not None
    assert math.hypot(fix.pose[0] - 5.0, fix.pose[1] - 5.5) < 0.05
    assert abs(math.degrees(fix.pose[2]) - 95) < 1.0


def test_jump_needs_two_consistent_reads() -> None:
    """Lesson 4 / rule 6: one reading never moves the pose alone."""
    lz = loc.Localizer(TAGS, CAM)
    true = robot_in_world(6.0, 5.5, math.pi / 2)
    odom = (6.0, 5.0, math.pi / 2)
    assert lz.update([obs_at(true)], odom).status == "pending"
    assert lz.update([obs_at(true)], odom).status == "accepted"


def test_alternating_outliers_never_accepted() -> None:
    lz = loc.Localizer(TAGS, CAM)
    odom = (6.0, 4.0, math.pi / 2)
    a, b = robot_in_world(6.0, 5.5, math.pi / 2), robot_in_world(5.4, 5.2, math.pi / 2)
    statuses = [lz.update([obs_at(p)], odom).status for p in (a, b, a, b, a)]
    assert "accepted" not in statuses


def test_nav_output_off_until_tp_v02_passes() -> None:
    """SR-017: the pose correction stays log-only by default."""
    assert loc.NAV_ENABLED is False
    fix = loc.Localizer(TAGS, CAM).update([obs_at(robot_in_world(6.0, 5.5, math.pi / 2))], (6.0, 5.5, math.pi / 2))
    assert fix.status == "accepted"
    assert fix.use_for_nav is False


def test_tag_map_rejects_duplicates(tmp_path: Path) -> None:
    p = tmp_path / "m.json"
    tag = {"id": 1, "x": 0, "y": 0, "z": 1, "yaw_deg": 0}
    p.write_text(json.dumps({"family": "tag36h11", "tag_size_m": 0.2, "tags": [tag, tag]}))
    with pytest.raises(ValueError, match="duplicate"):
        load_tag_map(p)


def test_example_tag_map_loads() -> None:
    tags = load_tag_map(CFG / "tag_map.example.json")
    assert len(tags) == 20
    assert all(t.size == pytest.approx(0.16) for t in tags.values())


def test_generated_sheet_is_true_scale_and_detectable() -> None:
    assert gen_apriltags.parse_ids("0-2,5") == [0, 1, 2, 5]
    img, real_mm = gen_apriltags.page(5, 150.0, "A4", 300)
    assert real_mm == pytest.approx(150.0, abs=0.5)
    gray = np.array(img.convert("L").resize((img.width // 4, img.height // 4)))
    _, ids, _ = make_detector().detectMarkers(gray)
    assert ids is not None
    assert ids.flatten().tolist() == [5]


def test_oversized_tag_does_not_fit() -> None:
    with pytest.raises(ValueError, match="does not fit"):
        gen_apriltags.page(0, 250.0, "A4", 150)
