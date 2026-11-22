#!/usr/bin/env python3
"""Run the camera, detect AprilTags and people, log JSON lines (SR-018, SR-020, SR-021, TP-V02, TP-V03). Log-only.

Privacy (SR-021, TM-V01, privacy review 2026-11-22): the process refuses to open a camera unless hardening applied;
frames are tracked right after each read and zeroed after processing; the log is created 0600 and holds tag corners,
the fix and, for people, only a count and the nearest distance in 0.5 m bins (no bearings: no location track).
Usage: python -m linux.vision.tag_logger --tags tag_map.json --camera camera.json --out run.jsonl
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import cv2

from linux.nav.caution import Caution
from linux.vision.config import load_camera, load_tag_map
from linux.vision.detector import make_detector
from linux.vision.localizer import Localizer
from linux.vision.people import PersonDetector
from linux.vision.pipeline import process
from linux.vision.privacy import FrameScope, require_hardening


def candidates(device: str | None) -> list[str]:
    """Configured stable path (``/dev/v4l/by-id/...``) if given; else /dev/video2+ in numeric order (0-1 are internal
    on the UNO Q, ADR-0006). Numeric order matters once four cameras are fitted (``video10`` after ``video2``)."""
    if device:
        return [device]
    found = []
    for dev in glob.glob("/dev/video*"):
        m = re.fullmatch(r"/dev/video(\d+)", dev)
        if m and int(m.group(1)) >= 2:
            found.append((int(m.group(1)), dev))
    return [d for _, d in sorted(found)]


def open_camera(width: int, height: int, device: str | None) -> tuple[cv2.VideoCapture, dict]:
    for dev in candidates(device):
        cap = cv2.VideoCapture(dev, cv2.CAP_V4L2)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            buf_ok = bool(cap.set(cv2.CAP_PROP_BUFFERSIZE, 1))
            return cap, {"device": dev, "buffersize_set": buf_ok, "buffersize": cap.get(cv2.CAP_PROP_BUFFERSIZE)}
    raise RuntimeError("no USB camera found")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def nearest_bin(distances: list[float]) -> float | None:
    return round(min(distances) * 2) / 2 if distances else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tags", type=Path, required=True)
    ap.add_argument("--camera", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seconds", type=float, default=60.0)
    a = ap.parse_args(argv)
    hardening = require_hardening()
    tags, cam = load_tag_map(a.tags), load_camera(a.camera)
    device = json.loads(a.camera.read_text(encoding="utf-8")).get("device")
    cap, cap_info = open_camera(cam.width, cam.height, device)
    try:
        actual = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        if actual != (cam.width, cam.height):
            raise RuntimeError(f"camera gives {actual}, calibration is {cam.width}x{cam.height}")
        det, loc, people, caution = make_detector(), Localizer(tags, cam), PersonDetector(), Caution()
        fd = os.open(a.out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        t0 = time.monotonic()
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            meta = {"type": "meta", "tags_sha": _digest(a.tags), "camera_sha": _digest(a.camera), "size": actual}
            f.write(json.dumps({**meta, **cap_info, "hardening": hardening}) + "\n")
            while time.monotonic() - t0 < a.seconds:
                with FrameScope() as scope:
                    ok, frame = cap.read()
                    t = time.monotonic() - t0
                    if ok:
                        scope.track(frame)
                        res = process(frame, cam, det, people)
                    del frame
                if not ok:
                    caution.update(t, [], None, blind=True)
                    f.write(json.dumps({"type": "frame", "t": round(t, 3), "ok": False, "caution": True}) + "\n")
                    continue
                careful = caution.update(t, res.persons, None)
                fix = loc.update(res.observations, None, caution=careful)
                rec = {
                    "type": "frame",
                    "t": round(t, 3),
                    "ok": True,
                    "obs": [[o.id, o.cam, o.corners.round(2).tolist()] for o in res.observations],
                    "people": len(res.persons),
                    "nearest_person_m": nearest_bin([p.distance_m for p in res.persons]),
                    "caution": careful,
                    "status": fix.status,
                    "source": fix.source,
                    "pose": [round(v, 4) for v in fix.pose] if fix.pose else None,
                    "rejected": fix.rejected,
                    "nav": fix.use_for_nav,
                }
                f.write(json.dumps(rec) + "\n")
    finally:
        cap.release()
    return 0


if __name__ == "__main__":
    sys.exit(main())
