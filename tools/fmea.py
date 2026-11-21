#!/usr/bin/env python3
"""DFMEA/PFMEA sanity check and ranking: RPN = S x O x D; any S >= 9 needs an action.

Also classifies special characteristics (YC/YS, docs/08-sccaf.md) and, when risk/sccaf.csv sits next to the FMEA
file, checks that every YC/YS row has a matching SCCAF register entry."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REQUIRED = ["id", "item", "failure_mode", "effect", "severity", "cause", "occurrence", "detection", "action", "req"]


def special_class(s: int, o: int) -> str:
    """YC = potential critical (S 9-10); YS = potential significant (S 5-8 and O 4-10); '' = none."""
    if s >= 9:
        return "YC"
    if s >= 5 and o >= 4:
        return "YS"
    return ""


def sccaf_errors(rows: list[dict[str, str]], register: list[dict[str, str]]) -> list[str]:
    """Every YC/YS DFMEA row needs a register entry with the same class."""
    reg = {r.get("dfmea_id", ""): r.get("class", "") for r in register}
    errors = []
    for r in rows:
        try:
            cls = special_class(int(r["severity"]), int(r["occurrence"]))
        except (KeyError, ValueError):
            continue
        rid = r.get("id", "?")
        if cls and rid not in reg:
            errors.append(f"{rid}: {cls} needs an SCCAF register entry (risk/sccaf.csv)")
        elif rid in reg and reg[rid] != cls:
            errors.append(f"{rid}: SCCAF class '{reg[rid]}' but DFMEA S/O give '{cls or 'none'}'")
    return errors


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def analyze(rows: list[dict[str, str]]) -> tuple[list[tuple[str, int, int, str]], list[str]]:
    errors: list[str] = []
    ranked: list[tuple[str, int, int, str]] = []
    ids = [r.get("id", "?") for r in rows]
    errors += [f"duplicate id {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    for r in rows:
        rid = r.get("id", "?")
        missing = [k for k in REQUIRED if not (r.get(k) or "").strip()]
        if missing:
            errors.append(f"{rid}: missing {missing}")
            continue
        try:
            s, o, d = int(r["severity"]), int(r["occurrence"]), int(r["detection"])
        except ValueError:
            errors.append(f"{rid}: S/O/D must be integers")
            continue
        if not all(1 <= v <= 10 for v in (s, o, d)):
            errors.append(f"{rid}: S/O/D must be in 1..10")
            continue
        if s >= 9 and r["action"].strip().lower() in {"", "none", "-"}:
            errors.append(f"{rid}: severity {s} requires an action")
        ranked.append((rid, s * o * d, s, special_class(s, o)))
    ranked.sort(key=lambda t: (t[2] >= 9, t[1]), reverse=True)
    return ranked, errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1] / "risk" / "dfmea.csv"
    rows = load(path)
    ranked, errors = analyze(rows)
    register = path.with_name("sccaf.csv")
    if register.exists():
        errors += sccaf_errors(rows, load(register))
    print(f"{'ID':<8}{'RPN':>6}{'S':>4}  {'class':<6}flag")
    for rid, rpn, s, cls in ranked:
        print(f"{rid:<8}{rpn:>6}{s:>4}  {cls:<6}{'MANDATORY (S>=9)' if s >= 9 else ''}")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
