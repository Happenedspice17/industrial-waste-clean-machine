"""Ultrasonic level filter (SR-022): firmware C++ on the host and its Python mirror give the same results."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from sim import level_model as lm

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(shutil.which("g++") is None, reason="g++ not installed")
def test_firmware_level_filter_host_build(tmp_path: Path) -> None:
    exe = tmp_path / "test_level"
    src = [ROOT / "firmware/mcu/level.cpp", ROOT / "firmware/mcu/test/test_level.cpp"]
    subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-Werror", "-o", str(exe), *map(str, src)], check=True)
    res = subprocess.run([str(exe)], capture_output=True, text=True, check=False)
    assert res.returncode == 0, res.stdout


def test_python_mirror_same_vectors() -> None:
    assert lm.echo_to_mm(1749, 200) == 300
    assert lm.echo_to_mm(1749, 400) == 310
    assert lm.echo_to_mm(0, 200) == lm.echo_to_mm(30000, 200) == 0
    f = lm.Filter()
    f.tick(0)
    assert f.state == lm.FAULT
    t = 0
    for _ in range(3):
        t += 100
        f.add(380, t)
    assert f.state == lm.LOW
    f.add(130, t := t + 100)
    assert f.state == lm.LOW
    f.add(130, t := t + 100)
    assert f.state == lm.LOW
    f.add(130, t := t + 100)
    assert (f.state, f.pct) == (lm.FULL, 90)
    for _ in range(4):
        f.add(175, t := t + 100)
    assert f.state == lm.FULL
    f.add(10, t := t + 100)
    assert f.rejected == 1
    f.tick(t + 600)
    assert f.state == lm.FAULT
