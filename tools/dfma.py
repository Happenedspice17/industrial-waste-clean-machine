#!/usr/bin/env python3
"""Boothroyd-Dewhurst design efficiency: DE = 3 * N_min / total manual assembly time (s)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


def design_efficiency(rows: list[dict[str, str]], t_ideal: float = 3.0) -> dict[str, float]:
    n_parts = 0
    n_min = 0
    total_t = 0.0
    for r in rows:
        q = int(r["qty"])
        n_parts += q
        n_min += int(r["min_theoretical"]) * q
        total_t += q * (float(r["handling_s"]) + float(r["insertion_s"]))
    de = t_ideal * n_min / total_t if total_t else 0.0
    return {"parts": n_parts, "n_min": n_min, "time_s": total_t, "design_efficiency": de}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: dfma.py <worksheet.csv>  (columns: part,qty,min_theoretical,handling_s,insertion_s)")
        return 2
    with Path(argv[1]).open(encoding="utf-8", newline="") as fh:
        res = design_efficiency(list(csv.DictReader(fh)))
    print(
        f"parts {res['parts']}, theoretical minimum {res['n_min']}, assembly time {res['time_s']:.1f} s, "
        f"design efficiency {res['design_efficiency'] * 100:.1f} %"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
