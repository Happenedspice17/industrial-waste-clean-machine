"""Privacy controls for camera frames (SR-021, ADR-0009, threat model TM-V01).

Rules: frames live only inside one ``FrameScope``; every pixel buffer the pipeline creates is registered and
overwritten with zeros when the scope closes; nothing leaves the scope except tag corners and person summaries
(bearing, distance), never pixels. Frames are never written to disk, logs or the network, and no debug view exists
(an image view needs its own ADR and an allow-list design: show tag regions only).

Limits (honest): Python and OpenCV may keep internal copies (driver ring buffers, allocator free lists) that this code
cannot reach; zeroing reduces, not eliminates, residence in RAM. ``harden_process`` blocks core dumps and ptrace-style
dumps so a crash does not spill frames to disk; swap must be disabled or encrypted on the robot image (TM-V01).
"""

from __future__ import annotations

import ctypes
import resource
import sys
from types import TracebackType

import numpy as np

PR_GET_DUMPABLE = 3
PR_SET_DUMPABLE = 4


def dumpable() -> int | None:
    """PR_GET_DUMPABLE on Linux (0 = not dumpable), None elsewhere."""
    if not sys.platform.startswith("linux"):
        return None
    return int(ctypes.CDLL(None, use_errno=True).prctl(PR_GET_DUMPABLE, 0, 0, 0, 0))


def require_hardening() -> dict[str, bool]:
    """Fail closed: no camera opens unless core dumps are off and the process is non-dumpable (P-03)."""
    applied = harden_process()
    if not all(applied.values()):
        raise RuntimeError(f"privacy hardening failed {applied}; camera not opened")
    return applied


def harden_process() -> dict[str, bool]:
    """Disable core dumps and mark the process non-dumpable (Linux). Returns what was applied."""
    applied = {"core_limit_zero": False, "non_dumpable": False}
    try:
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        applied["core_limit_zero"] = True
    except (ValueError, OSError):
        pass
    if sys.platform.startswith("linux"):
        try:
            libc = ctypes.CDLL(None, use_errno=True)
            applied["non_dumpable"] = libc.prctl(PR_SET_DUMPABLE, 0, 0, 0, 0) == 0
        except OSError:
            pass
    return applied


class FrameScope:
    """Holds pixel buffers for one frame and wipes all of them on exit, even on exceptions."""

    def __init__(self) -> None:
        self._buffers: list[np.ndarray] = []

    def track(self, buf: np.ndarray) -> np.ndarray:
        if not buf.flags.writeable:
            raise ValueError("pixel buffer must be writeable so it can be wiped")
        self._buffers.append(buf)
        if isinstance(buf.base, np.ndarray) and buf.base.flags.writeable:
            self._buffers.append(buf.base)
        return buf

    def __enter__(self) -> FrameScope:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        first_error: Exception | None = None
        for buf in self._buffers:
            try:
                buf.fill(0)
            except Exception as err:  # keep wiping the rest, re-raise after
                first_error = first_error or err
        self._buffers.clear()
        if first_error is not None:
            raise first_error
