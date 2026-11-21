#!/usr/bin/env python3
"""Worst-case circuit analysis: dividers (EVA + RSS), logic levels, power branches."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

# Conservative chassis-wiring ampacity (A) for PVC hook-up wire in bundles; verify with the wire datasheet.
AMPACITY = {22: 3, 20: 5, 18: 7, 16: 10, 14: 15, 12: 20, 10: 30}


def divider(vin: float, r_top: float, r_bot: float) -> float:
    return vin * r_bot / (r_top + r_bot)


def divider_wc(vin: dict, rt: dict, rb: dict) -> dict[str, float]:
    vmax = divider(vin["max"], rt["nom"] * (1 - rt["tol"]), rb["nom"] * (1 + rb["tol"]))
    vmin = divider(vin["min"], rt["nom"] * (1 + rt["tol"]), rb["nom"] * (1 - rb["tol"]))
    vnom = divider(vin["nom"], rt["nom"], rb["nom"])
    k = rb["nom"] / (rt["nom"] + rb["nom"])
    # dk/k = (1 - k) * (dRb/Rb - dRt/Rt)  ->  RSS of the two tolerances
    rel = (1 - k) * math.sqrt(rt["tol"] ** 2 + rb["tol"] ** 2)
    vrss = vin["max"] * k * (1 + rel)
    return {"vmin": vmin, "vnom": vnom, "vmax": vmax, "vmax_rss": vrss}


def logic_margin(driver: dict, receiver: dict) -> tuple[float, float]:
    return driver["voh_min"] - receiver["vih_min"], receiver["vil_max"] - driver["vol_max"]


def run(cfg: dict) -> tuple[list[str], list[str]]:
    out: list[str] = []
    errors: list[str] = []
    sup = cfg.get("supply", {})
    for d in cfg.get("dividers", []):
        r = divider_wc(sup[d["vin_key"]], d["r_top"], d["r_bot"])
        margin = (d["vout_limit"] - r["vmax"]) / d["vout_limit"]
        status = "FAIL" if margin < 0 else ("WARN" if margin < 0.10 else "OK")
        out.append(
            f"divider {d['name']}: Vout {r['vmin']:.3f}..{r['vmax']:.3f} V (nom {r['vnom']:.3f}, RSS max "
            f"{r['vmax_rss']:.3f}) limit {d['vout_limit']} V margin {margin * 100:.1f} % {status}"
        )
        if status == "FAIL":
            errors.append(f"divider {d['name']} exceeds limit")
    for lg in cfg.get("logic", []):
        hi, lo = logic_margin(lg["driver"], lg["receiver"])
        status = "OK" if hi > 0 and lo > 0 else "FAIL"
        out.append(f"logic {lg['name']}: high margin {hi:.2f} V, low margin {lo:.2f} V {status}")
        if status == "FAIL":
            errors.append(f"logic {lg['name']} incompatible")
    pw = cfg.get("power", {})
    for b in pw.get("branches", []):
        amp = AMPACITY.get(int(b["wire_awg"]))
        ok_fuse = b["fuse_a"] >= 1.25 * b["nom_a"]
        ok_wire = amp is not None and b["fuse_a"] <= amp
        status = "OK" if ok_fuse and ok_wire else "FAIL"
        out.append(
            f"branch {b['name']}: nom {b['nom_a']} A peak {b['peak_a']} A fuse {b['fuse_a']} A "
            f"wire {b['wire_awg']} AWG (ampacity {amp} A) {status}"
        )
        if not ok_fuse:
            errors.append(f"branch {b['name']}: fuse below 1.25 x nominal (nuisance trips)")
        if not ok_wire:
            errors.append(f"branch {b['name']}: fuse above wire ampacity")
    if pw.get("battery_wh_usable") and pw.get("avg_load_w"):
        out.append(f"runtime: {60 * pw['battery_wh_usable'] / pw['avg_load_w']:.0f} min at {pw['avg_load_w']} W")
    return out, errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1] / "risk" / "wcca.yaml"
    out, errors = run(yaml.safe_load(path.read_text(encoding="utf-8")))
    print("\n".join(out))
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
