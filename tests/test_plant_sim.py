"""Smoke test of the whole-mission simulator (SR-019, SR-020, SR-022, SR-023). Simulation only."""

from __future__ import annotations

from sim import plant_sim


def test_worlds_are_reproducible_and_have_home_pair() -> None:
    a, b = plant_sim.make_world(3), plant_sim.make_world(3)
    assert a.machines == b.machines
    assert {100, 101} <= set(a.tags)
    assert plant_sim.make_world(4).moved_tag is not None


def test_short_mission_runs_without_contact() -> None:
    res = plant_sim.run_map(1, seed=0, max_minutes=4.0)
    assert res.contacts == 0
    assert res.machine_hits == 0
    assert res.coverage_pct > 0
    assert res.frames_fix_pct > 0
