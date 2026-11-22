"""Person detection that keeps no pixels (SR-020, SR-021, ADR-0009).

OpenCV HOG people detector on a downscaled grey copy (HOG was removed in OpenCV 5, hence the pin to < 5).
Output is only bearing and a rough distance per person. This is
NOT a safety sensor (ISO 3691-4 stays with LiDAR + bumpers, ADR-0006 option C): a detection can only slow the robot
and make localization stricter. Detection quality on the real floor is unknown until TP-V03.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import cv2
import numpy as np

from linux.vision.config import Camera
from linux.vision.privacy import FrameScope

PERSON_HEIGHT_M = 1.7
MAX_WIDTH_PX = 320


@dataclass(frozen=True)
class Person:
    bearing_deg: float
    """Left positive, from the camera optical axis."""
    distance_m: float
    """Rough: assumes a standing person 1.7 m tall fully in view (estimate)."""
    cam: int = 0


class PersonDetector:
    def __init__(self) -> None:
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, gray: np.ndarray, cam: Camera, scope: FrameScope, cam_idx: int = 0) -> list[Person]:
        scale = min(1.0, MAX_WIDTH_PX / gray.shape[1])
        small = scope.track(cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA))
        boxes, _ = self.hog.detectMultiScale(small, winStride=(8, 8), padding=(8, 8), scale=1.05)
        out = []
        for x, _y, w, h in boxes:
            u = (x + w / 2) / scale
            h_px = h / scale
            bearing = -math.degrees(math.atan2(u - cam.matrix[0, 2], cam.matrix[0, 0]))
            out.append(
                Person(round(bearing, 1), round(cam.matrix[1, 1] * PERSON_HEIGHT_M / max(h_px, 1.0), 2), cam_idx)
            )
        return out
