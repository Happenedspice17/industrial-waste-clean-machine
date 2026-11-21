#!/usr/bin/env python3
"""Economic evaluation of one robot in the reference plant (reproduces Activity 06 numbers)."""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Params:
    min_wage_day: float = 315.04  # MXN, 2026 general zone (EY, Jan 2026)
    wage_factor: float = 1.15  # industrial wage over minimum (assumption)
    burden: float = 1.40  # employer burden (assumption)
    days: int = 300
    cycles_per_day: int = 3
    hours_saved_day: float = 2.0  # 3 h manual -> 1 h with robot (assumption)
    chips_kg_cycle: float = 1.5  # assumption
    oil_l_cycle: float = 1.0  # assumption
    oil_density: float = 0.88
    absorbent_kg_cycle: float = 0.5  # assumption
    disposal_mxn_kg: float = 6.0  # assumption, range 2-10
    absorbent_mxn_kg: float = 20.0  # assumption
    oil_collection_mxn_kg: float = 2.0  # assumption
    scrap_mxn_kg: float = 2.5  # below HMS reference 4.00 (Oct 2026)
    fines_fraction: float = 0.05
    kwh_cycle: float = 0.15
    tariff_mxn_kwh: float = 1.347  # CFE GDMTO Jul 2026
    battery_mxn: float = 1290.0
    batteries_year: int = 2
    consumables_year: float = 1200.0
    maint_hours_year: float = 24.0
    tech_rate: float = 120.0
    hardware: float = 20160.08  # BOM + tooling + 15 % contingency
    assembly_h: float = 60.0
    commissioning_h: float = 16.0
    eng_rate: float = 150.0
    nre_share: float = 0.0
    rate: float = 0.12
    years: int = 3


def evaluate(p: Params) -> dict[str, float]:
    hr = p.min_wage_day * p.wage_factor * p.burden / 8
    cycles = p.days * p.cycles_per_day
    labor = p.hours_saved_day * p.days * hr
    chips = p.chips_kg_cycle * cycles
    oil = p.oil_l_cycle * cycles * p.oil_density
    absorbent = p.absorbent_kg_cycle * cycles
    waste_today = (chips + oil + absorbent) * p.disposal_mxn_kg + absorbent * p.absorbent_mxn_kg
    waste_robot = (
        oil * p.oil_collection_mxn_kg
        + p.fines_fraction * chips * p.disposal_mxn_kg
        - (1 - p.fines_fraction) * chips * p.scrap_mxn_kg
    )
    waste_benefit = waste_today - waste_robot
    opex = (
        p.kwh_cycle * cycles * p.tariff_mxn_kwh
        + p.batteries_year * p.battery_mxn
        + p.consumables_year
        + p.maint_hours_year * p.tech_rate
    )
    invest = p.hardware + (p.assembly_h + p.commissioning_h) * p.eng_rate + p.nre_share
    net = labor + waste_benefit - opex
    af = sum(1 / (1 + p.rate) ** t for t in range(1, p.years + 1))
    return {
        "labor_rate_h": hr,
        "labor_saved": labor,
        "waste_benefit": waste_benefit,
        "opex": opex,
        "investment": invest,
        "net_annual": net,
        "payback_years": invest / net if net > 0 else float("inf"),
        "npv": net * af - invest,
    }


SCENARIOS = {
    "base": Params(),
    "optimistic": Params(hours_saved_day=2.5),
    "pessimistic": Params(hours_saved_day=1.0),
}


def pessimistic() -> dict[str, float]:
    p = Params(hours_saved_day=1.0)
    r = evaluate(p)
    # waste -50 %, opex +30 %, investment +50 % (as in Activity 06)
    net = r["labor_saved"] + 0.5 * r["waste_benefit"] - 1.3 * r["opex"]
    inv = 1.5 * r["investment"]
    af = sum(1 / (1 + p.rate) ** t for t in range(1, p.years + 1))
    return {"net_annual": net, "investment": inv, "payback_years": inv / net, "npv": net * af - inv}


def tornado(base: Params) -> list[tuple[str, float, float]]:
    b = evaluate(base)["npv"]
    cases = [
        ("hours_saved_day", 1.0, 2.5),
        ("disposal_mxn_kg", 2.0, 10.0),
        ("scrap_mxn_kg", 1.0, 4.0),
        ("hardware", base.hardware * 1.5, base.hardware * 0.7),
    ]
    out = []
    for field, lo, hi in cases:
        npv_lo = evaluate(replace(base, **{field: lo}))["npv"] - b
        npv_hi = evaluate(replace(base, **{field: hi}))["npv"] - b
        out.append((field, npv_lo, npv_hi))
    return sorted(out, key=lambda t: abs(t[2] - t[1]), reverse=True)


def main() -> int:
    for name, p in SCENARIOS.items():
        if name == "pessimistic":
            continue
        r = evaluate(p)
        print(
            f"{name:<12} net {r['net_annual']:>10,.0f}/yr  invest {r['investment']:>9,.0f}  "
            f"payback {r['payback_years'] * 12:>5.1f} mo  NPV {r['npv']:>10,.0f}"
        )
    pe = pessimistic()
    print(
        f"{'pessimistic':<12} net {pe['net_annual']:>10,.0f}/yr  invest {pe['investment']:>9,.0f}  "
        f"payback {pe['payback_years'] * 12:>5.1f} mo  NPV {pe['npv']:>10,.0f}"
    )
    print("tornado (NPV delta low/high):")
    for f, lo, hi in tornado(Params()):
        print(f"  {f:<18} {lo:>10,.0f} {hi:>10,.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
