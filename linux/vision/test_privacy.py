"""Privacy and caution tests (SR-020, SR-021). Person detection quality itself is for TP-V03 on real images."""

from __future__ import annotations

import dataclasses
import math
import resource
from pathlib import Path

import numpy as np
import pytest

from linux.nav.caution import Caution
from linux.vision import tag_logger
from linux.vision.config import load_camera
from linux.vision.detector import make_detector
from linux.vision.geometry import robot_in_world
from linux.vision.people import Person, PersonDetector
from linux.vision.pipeline import process
from linux.vision.privacy import FrameScope, dumpable, harden_process, require_hardening
from linux.vision.tag_logger import nearest_bin
from linux.vision.test_vision import TAGS, render

CAM = load_camera(Path(__file__).parent / "config" / "camera.example.json")


def test_frame_is_zeroed_after_processing_and_tags_still_found() -> None:
    frame = np.repeat(render(robot_in_world(6.0, 6.5, math.pi / 2), TAGS[7], 7)[:, :, None], 3, axis=2)
    res = process(frame, CAM, make_detector(), PersonDetector())
    assert [o.id for o in res.observations] == [7]
    assert not frame.any()


def test_frame_is_zeroed_even_when_processing_fails() -> None:
    frame = np.full((480, 640, 3), 200, np.uint8)

    class Boom(PersonDetector):
        def detect(self, *args: object, **kwargs: object) -> list[Person]:
            raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        process(frame, CAM, make_detector(), Boom())
    assert not frame.any()


def test_scope_wipes_every_tracked_buffer() -> None:
    a, b = np.ones((4, 4), np.uint8), np.ones((2, 2), np.float32)
    with FrameScope() as s:
        s.track(a)
        s.track(b)
    assert not a.any()
    assert not b.any()


def test_scope_refuses_buffers_it_cannot_wipe() -> None:
    ro = np.ones((2, 2))
    ro.flags.writeable = False
    with FrameScope() as s, pytest.raises(ValueError, match="writeable"):
        s.track(ro)


def test_person_summary_holds_no_pixels() -> None:
    fields = {f.name: f.type for f in dataclasses.fields(Person)}
    assert set(fields) == {"bearing_deg", "distance_m", "cam"}


def test_empty_scene_has_no_people() -> None:
    frame = np.full((480, 640), 128, np.uint8)
    assert process(frame, CAM, make_detector(), PersonDetector()).persons == []


def test_scope_wipes_base_of_a_view() -> None:
    full = np.ones((8, 8), np.uint8)
    with FrameScope() as s:
        s.track(full[2:4, 2:4])
    assert not full.any()


def test_harden_process_disables_core_dumps() -> None:
    applied = harden_process()
    assert applied["core_limit_zero"]
    assert resource.getrlimit(resource.RLIMIT_CORE) == (0, 0)
    if dumpable() is not None:
        assert dumpable() == 0
        assert all(require_hardening().values())


def test_caution_triggers_holds_and_only_lowers_speed() -> None:
    c = Caution()
    assert not c.update(0.0, [], None)
    assert c.update(1.0, [Person(5.0, 2.5)], None)
    assert c.update(2.5, [], None)
    assert not c.update(3.5, [], None)
    assert c.update(4.0, [], 1.0)
    assert c.speed(0.38, True) == pytest.approx(0.10)
    assert c.speed(0.05, True) == pytest.approx(0.05)
    assert c.speed(0.38, False) == pytest.approx(0.38)
    assert not c.update(10.0, [Person(0.0, 6.0)], 4.0)
    assert c.update(20.0, [], None, blind=True)
    assert c.update(21.5, [], None)


def test_camera_candidates_numeric_order(monkeypatch: pytest.MonkeyPatch) -> None:
    devs = ["/dev/video10", "/dev/video2", "/dev/video0", "/dev/video3", "/dev/video1"]
    monkeypatch.setattr(tag_logger.glob, "glob", lambda _: devs)
    assert tag_logger.candidates(None) == ["/dev/video2", "/dev/video3", "/dev/video10"]
    assert tag_logger.candidates("/dev/v4l/by-id/cam0") == ["/dev/v4l/by-id/cam0"]


def test_logged_person_data_is_coarse() -> None:
    assert nearest_bin([2.74, 4.1]) == 2.5
    assert nearest_bin([]) is None
