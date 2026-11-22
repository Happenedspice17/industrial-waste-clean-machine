"""Frames and transforms for AprilTag localization (SR-018).

World: floor frame, x/y on the floor, z up (m). Robot: x forward, y left, z up, origin on the floor between wheels.
Camera (OpenCV): x right, y down, z forward. Tag (OpenCV ArUco): x right, y up, z out of the tag towards the viewer.
"""

from __future__ import annotations

import math

import numpy as np

Mat = np.ndarray

CAM_IN_ROBOT = np.array([[0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, -1.0, 0.0]])


def rot_z(a: float) -> Mat:
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def rot_y(a: float) -> Mat:
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


def make_tf(rot: Mat, pos: Mat) -> Mat:
    tf = np.eye(4)
    tf[:3, :3] = rot
    tf[:3, 3] = np.asarray(pos, dtype=float).reshape(3)
    return tf


def inv_tf(tf: Mat) -> Mat:
    rot = tf[:3, :3].T
    return make_tf(rot, -rot @ tf[:3, 3])


def tag_in_world(x: float, y: float, z: float, yaw: float) -> Mat:
    """Tag on a vertical surface; yaw = world direction its face points to (rad)."""
    c, s = math.cos(yaw), math.sin(yaw)
    rot = np.column_stack([(-s, c, 0.0), (0.0, 0.0, 1.0), (c, s, 0.0)])
    return make_tf(rot, (x, y, z))


def cam_in_robot(x: float, y: float, z: float, yaw: float, pitch: float) -> Mat:
    """Camera mount; pitch > 0 tilts the optical axis up, yaw > 0 turns it left."""
    return make_tf(rot_z(yaw) @ rot_y(-pitch) @ CAM_IN_ROBOT, (x, y, z))


def robot_in_world(x: float, y: float, yaw: float) -> Mat:
    return make_tf(rot_z(yaw), (x, y, 0.0))


def tilt_deg(tf: Mat) -> float:
    """Angle between the frame's z axis and world up (deg); 0 for a robot standing on the floor."""
    return math.degrees(math.acos(max(-1.0, min(1.0, float(tf[2, 2])))))


def yaw_of(tf: Mat) -> float:
    return math.atan2(float(tf[1, 0]), float(tf[0, 0]))


def wrap(a: float) -> float:
    return (a + math.pi) % (2 * math.pi) - math.pi
