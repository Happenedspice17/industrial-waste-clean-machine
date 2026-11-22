#!/usr/bin/env python3
"""Run the single camera, detect AprilTags and log JSON lines (SR-018, TP-V02). Log-only (SR-017).

Frames are never written to disk (privacy, threat model TM-V01); only tag IDs, corners and the fix.
Usage: python -m linux.vision.tag_logger --tags tag_map.json --camera camera.json --out run.jsonl
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
import time
from pathlib import Path

import cv2

from linux.vision.config import load_camera, load_tag_map
from linux.vision.detector import detect, make_detector
from linux.vision.localizer import Localizer


def open_camera(width: int, height: int) -> cv2.VideoCapture:
    """/dev/video0-1 are internal on the UNO Q: probe from index 2 (ADR-0006 integration notes)."""
    for dev in sorted(glob.glob("/dev/video*")):
        idx = int(dev.removeprefix("/dev/video"))
        if idx < 2:
            continue
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            return cap
    raise RuntimeError("no USB camera found at /dev/video2+")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tags", type=Path, required=True)
    ap.add_argument("--camera", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seconds", type=float, default=60.0)
    a = ap.parse_args(argv)
    tags, cam = load_tag_map(a.tags), load_camera(a.camera)
    cap = open_camera(cam.width, cam.height)
    actual = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if actual != (cam.width, cam.height):
        raise RuntimeError(f"camera gives {actual}, calibration is {cam.width}x{cam.height}")
    det, loc = make_detector(), Localizer(tags, cam)
    t0 = time.monotonic()
    with a.out.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"type": "meta", "tags": str(a.tags), "camera": str(a.camera), "size": actual}) + "\n")
        while time.monotonic() - t0 < a.seconds:
            ok, frame = cap.read()
            t = time.monotonic() - t0
            if not ok:
                f.write(json.dumps({"type": "frame", "t": round(t, 3), "ok": False}) + "\n")
                continue
            obs = detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), det)
            fix = loc.update(obs, None)
            rec = {
                "type": "frame",
                "t": round(t, 3),
                "ok": True,
                "obs": {o.id: o.corners.round(2).tolist() for o in obs},
                "status": fix.status,
                "pose": [round(v, 4) for v in fix.pose] if fix.pose else None,
                "rejected": fix.rejected,
                "nav": fix.use_for_nav,
            }
            f.write(json.dumps(rec) + "\n")
    cap.release()
    return 0


if __name__ == "__main__":
    sys.exit(main())
