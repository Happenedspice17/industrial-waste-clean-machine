#!/usr/bin/env python3
"""Check requirements.yaml structure and traceability to tests/reports."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VAGUE = ["fast", "robust", "user-friendly", "etc", "and/or", "as appropriate", "adequate", "easy", "quickly"]
METHODS = {"Test", "Analysis", "Inspection", "Demonstration"}
STATUSES = {"draft", "approved", "verified"}


def evidence_exists(ref: str, root: Path) -> bool:
    if (root / ref).exists():
        return True
    pattern = re.compile(rf"\b{re.escape(ref)}\b")
    for folder in ("tests", "linux", "firmware", "docs/test-reports"):
        base = root / folder
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if f.is_file() and f.suffix in {".py", ".c", ".cpp", ".h", ".md"}:
                try:
                    if pattern.search(f.read_text(encoding="utf-8", errors="ignore")):
                        return True
                except OSError:
                    continue
    return False


def _check_text(rid: str, text: str, errors: list[str], warnings: list[str]) -> None:
    n_shall = len(re.findall(r"\bshall\b", text))
    if n_shall != 1:
        errors.append(f"{rid}: text must contain exactly one 'shall' (found {n_shall})")
    low = text.lower()
    for v in VAGUE:
        if re.search(rf"\b{re.escape(v)}\b", low):
            warnings.append(f"{rid}: vague term '{v}'")


def _check_evidence(rid: str, r: dict, root: Path, errors: list[str]) -> None:
    if not r.get("acceptance"):
        errors.append(f"{rid}: approved requirement needs 'acceptance'")
    refs = r.get("verified_by") or []
    if not refs:
        errors.append(f"{rid}: approved requirement needs 'verified_by'")
    for ref in refs:
        if not evidence_exists(str(ref), root):
            errors.append(f"{rid}: evidence '{ref}' not found in repo")


def check(data: dict, root: Path = ROOT) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    stake = {r["id"] for r in data.get("stakeholder", [])}
    system = data.get("system", [])
    ids = [r.get("id") for r in system]
    errors += [f"duplicate id {dup}" for dup in sorted({i for i in ids if ids.count(i) > 1})]
    known = stake | set(ids)
    for r in system:
        rid = str(r.get("id", "?"))
        if not re.match(r"^SR-\d{3}$", rid):
            errors.append(f"{rid}: id must be SR-NNN")
        if r.get("parent") not in known:
            errors.append(f"{rid}: parent '{r.get('parent')}' not found")
        _check_text(rid, str(r.get("text", "")), errors, warnings)
        status = r.get("status")
        if status not in STATUSES:
            errors.append(f"{rid}: status must be one of {sorted(STATUSES)}")
        if r.get("verification") not in METHODS:
            errors.append(f"{rid}: verification must be one of {sorted(METHODS)}")
        if status in {"approved", "verified"}:
            _check_evidence(rid, r, root, errors)
        if "TBD" in str(r.get("acceptance", "")) and status == "verified":
            errors.append(f"{rid}: verified requirement cannot have TBD acceptance")
    return errors, warnings


def main() -> int:
    path = ROOT / "requirements" / "requirements.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors, warnings = check(data)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    n = len(data.get("system", []))
    print(f"check_traceability: {n} system requirements, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
