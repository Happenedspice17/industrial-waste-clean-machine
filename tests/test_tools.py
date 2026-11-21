"""Unit tests for project tools. Requirement-independent (tooling)."""

from __future__ import annotations

import pytest

from tools import check_branch, check_commit_msg, check_traceability, dfma, econ, fmea, wcca


@pytest.mark.parametrize(
    ("name", "ok"),
    [
        ("feature/12-suction-rig", True),
        ("cad/wheel-hub-hex", True),
        ("release/v1.2.0", True),
        ("hotfix/3-estop-relay", True),
        ("claude/magical-mendel-rphq63", True),
        ("main", True),
        ("Feature/x", False),
        ("feature/ab", False),
        ("random-branch", False),
    ],
)
def test_branch_names(name: str, ok: bool) -> None:
    assert check_branch.is_valid(name) is ok


def test_commit_messages() -> None:
    assert check_commit_msg.validate("feat(m3): add suction rig logger") == []
    assert check_commit_msg.validate("added stuff")
    assert check_commit_msg.validate("fix(m2): stop on overspeed.")


def test_traceability_rules() -> None:
    data = {
        "stakeholder": [{"id": "R1", "text": "x", "importance": 10}],
        "system": [
            {
                "id": "SR-001",
                "parent": "R1",
                "text": "The robot shall do X within 5 s.",
                "verification": "Test",
                "status": "draft",
            },
            {
                "id": "SR-002",
                "parent": "R9",
                "text": "The robot shall be fast and shall be robust.",
                "verification": "Test",
                "status": "approved",
            },
        ],
    }
    errors, warnings = check_traceability.check(data)
    assert any("SR-002: parent" in e for e in errors)
    assert any("exactly one 'shall'" in e for e in errors)
    assert any("verified_by" in e for e in errors)
    assert any("fast" in w for w in warnings)
    assert not any(e.startswith("SR-001") for e in errors)


def test_fmea_mandatory_action() -> None:
    rows = [
        {
            "id": "F1",
            "item": "a",
            "failure_mode": "b",
            "effect": "c",
            "severity": "9",
            "cause": "d",
            "occurrence": "2",
            "detection": "2",
            "action": "none",
            "req": "SR-001",
        },
        {
            "id": "F2",
            "item": "a",
            "failure_mode": "b",
            "effect": "c",
            "severity": "5",
            "cause": "d",
            "occurrence": "5",
            "detection": "5",
            "action": "test",
            "req": "SR-001",
        },
    ]
    ranked, errors = fmea.analyze(rows)
    assert any("F1" in e for e in errors)
    assert ranked[0][0] == "F1"


def test_divider_worst_case() -> None:
    vin = {"min": 10.5, "nom": 12.8, "max": 14.7}
    r = wcca.divider_wc(vin, {"nom": 33000, "tol": 0.01}, {"nom": 8200, "tol": 0.01})
    assert 2.9 < r["vmax"] < 3.0
    assert r["vmin"] < r["vnom"] < r["vmax"]
    assert r["vmax_rss"] <= r["vmax"]


def test_logic_margin() -> None:
    hi, lo = wcca.logic_margin({"voh_min": 3.2, "vol_max": 0.1}, {"vih_min": 2.31, "vil_max": 0.99})
    assert hi > 0 and lo > 0


def test_dfma_efficiency() -> None:
    rows = [{"part": "a", "qty": "1", "min_theoretical": "1", "handling_s": "1.5", "insertion_s": "1.5"}]
    assert dfma.design_efficiency(rows)["design_efficiency"] == pytest.approx(1.0)


def test_econ_reproduces_activity06() -> None:
    r = econ.evaluate(econ.Params())
    assert r["net_annual"] == pytest.approx(56968, abs=5)
    assert r["npv"] == pytest.approx(105269, abs=5)
    assert r["payback_years"] * 12 == pytest.approx(6.6, abs=0.1)
    pe = econ.pessimistic()
    assert pe["npv"] == pytest.approx(7928, abs=5)
