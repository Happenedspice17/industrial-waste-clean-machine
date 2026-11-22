"""One camera frame in, tag observations and person summaries out (SR-021).

Every buffer created here is zeroed before returning; OpenCV and kernel (V4L2) internal buffers are not reachable from
Python (TM-V01, privacy review P-02).
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from linux.vision.config import Camera
from linux.vision.detector import Observation, detect
from linux.vision.people import Person, PersonDetector
from linux.vision.privacy import FrameScope


@dataclass(frozen=True)
class FrameResult:
    observations: list[Observation]
    persons: list[Person]


def process(
    frame: np.ndarray, cam: Camera, tag_det: cv2.aruco.ArucoDetector, people: PersonDetector | None, cam_idx: int = 0
) -> FrameResult:
    """``frame`` (BGR or grey) and the grey copy are zeroed in place before this returns, whatever happens."""
    with FrameScope() as scope:
        scope.track(frame)
        gray = scope.track(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if frame.ndim == 3 else frame.copy())
        obs = detect(gray, tag_det, cam_idx)
        persons = people.detect(gray, cam, scope, cam_idx) if people else []
    return FrameResult(obs, persons)
