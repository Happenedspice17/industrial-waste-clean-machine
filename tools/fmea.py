#!/usr/bin/env python3
"""DFMEA/PFMEA sanity check and ranking: RPN = S x O x D; any S >= 9 needs an action."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REQUIRED = ["id", "item", "failure_mode", "effect", "severity", "cause", "occurrence", "detection", "action", "req"]


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def analyze(rows: list[dict[str, str]]) -> tuple[list[tuple[str, int, int]], list[str]]:
    errors: list[str] = []
    ranked: list[tuple[str, int, int]] = []
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
        ranked.append((rid, s * o * d, s))
    ranked.sort(key=lambda t: (t[2] >= 9, t[1]), reverse=True)
    return ranked, errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1] / "risk" / "dfmea.csv"
    ranked, errors = analyze(load(path))
    print(f"{'ID':<8}{'RPN':>6}{'S':>4}  flag")
    for rid, rpn, s in ranked:
        print(f"{rid:<8}{rpn:>6}{s:>4}  {'MANDATORY (S>=9)' if s >= 9 else ''}")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
