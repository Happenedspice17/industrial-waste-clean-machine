"""AprilTag 36h11 detection with OpenCV (SR-018). No frames are stored; only corner detections."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from linux.vision.geometry import Mat

DICT = cv2.aruco.DICT_APRILTAG_36h11


@dataclass(frozen=True)
class Observation:
    id: int
    corners: Mat
    """Image corners (4 x 2 px) in OpenCV order: top-left, top-right, bottom-right, bottom-left of the tag."""
    cam: int = 0
    """Index of the camera that saw it (one camera now, four planned; ADR-0008)."""

    @property
    def side_px(self) -> float:
        return float(np.mean(np.linalg.norm(self.corners - np.roll(self.corners, 1, axis=0), axis=1)))


def make_detector() -> cv2.aruco.ArucoDetector:
    params = cv2.aruco.DetectorParameters()
    params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    return cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(DICT), params)


def tag_corners(size: float) -> Mat:
    """Corners in the tag frame (m), same order as ``Observation.corners``."""
    h = size / 2
    return np.array([[-h, h, 0], [h, h, 0], [h, -h, 0], [-h, -h, 0]], dtype=np.float64)


def detect(gray: Mat, det: cv2.aruco.ArucoDetector, cam: int = 0) -> list[Observation]:
    corners, ids, _ = det.detectMarkers(gray)
    if ids is None:
        return []
    return [
        Observation(int(i), c.reshape(4, 2).astype(np.float64), cam)
        for c, i in zip(corners, ids.flatten(), strict=True)
    ]
