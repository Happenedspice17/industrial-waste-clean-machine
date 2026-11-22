"""Python mirror of firmware/mcu/level.{h,cpp} for the simulator (SR-022). Same vectors are tested on both."""

from __future__ import annotations

from dataclasses import dataclass

LOW, HALF, FULL, FAULT = "low", "half", "full", "fault"
VOTES_NEEDED, VOTES_CAP = 2, 3


@dataclass(frozen=True)
class Config:
    empty_mm: int = 400
    full_mm: int = 100
    half_pct: int = 40
    full_pct: int = 80
    release_pct: int = 70
    stale_ms: int = 500
    min_valid_mm: int = 30
    max_valid_mm: int = 600


def frame(mm: int) -> bytes:
    h, lo = mm >> 8, mm & 0xFF
    return bytes([0xFF, h, lo, (0xFF + h + lo) & 0xFF])


class Filter:
    def __init__(self, cfg: Config | None = None) -> None:
        self.cfg = cfg or Config()
        self.hist: list[int] = []
        self.pct = 0
        self.state = FAULT
        self.candidate = FAULT
        self.votes = 0
        self.last_ms = 0
        self.seen = False
        self.rejected = 0

    def _classify(self, pct: int) -> str:
        if self.state == FULL and pct >= self.cfg.release_pct:
            return FULL
        if pct >= self.cfg.full_pct:
            return FULL
        return HALF if pct >= self.cfg.half_pct else LOW

    def add(self, mm: int, now_ms: int) -> None:
        c = self.cfg
        if not c.min_valid_mm <= mm <= c.max_valid_mm:
            self.rejected += 1
            return
        self.hist = [*self.hist, mm][-3:]
        self.last_ms, self.seen = now_ms, True
        if len(self.hist) < 3:
            return
        d = sorted(self.hist)[1]
        span = c.empty_mm - c.full_mm
        self.pct = max(0, min(100, (c.empty_mm - d) * 100 // span if span > 0 else 100))
        s = self._classify(self.pct)
        if s == self.state:
            self.votes = 0
            return
        if s == self.candidate:
            self.votes = min(self.votes + 1, VOTES_CAP)
        else:
            self.candidate, self.votes = s, 1
        if self.votes >= VOTES_NEEDED or self.state == FAULT:
            self.state, self.votes = s, 0

    def tick(self, now_ms: int) -> None:
        if not self.seen or now_ms - self.last_ms > self.cfg.stale_ms:
            self.state = FAULT
            self.hist = []
