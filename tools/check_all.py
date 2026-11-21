#!/usr/bin/env python3
"""Run every project check. Exit non-zero if any blocking check fails."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable

CHECKS: list[tuple[str, list[str], bool]] = [
    ("branch name", [PY, "tools/check_branch.py"], True),
    ("traceability", [PY, "tools/check_traceability.py"], True),
    ("DFMEA", [PY, "tools/fmea.py", "risk/dfmea.csv"], True),
    ("WCCA", [PY, "tools/wcca.py", "risk/wcca.yaml"], True),
    ("ruff lint", ["ruff", "check", "."], True),
    ("ruff format", ["ruff", "format", "--check", "."], True),
    ("pytest", [PY, "-m", "pytest", "-q"], True),
]


def main() -> int:
    failed = []
    for name, cmd, blocking in CHECKS:
        if cmd[0] == "ruff" and shutil.which("ruff") is None:
            print(f"[SKIP] {name}: ruff not installed (pip install ruff)")
            continue
        res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        ok = res.returncode == 0
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            print((res.stdout + res.stderr).strip()[-2000:])
            if blocking:
                failed.append(name)
    if failed:
        print(f"\nFAILED: {', '.join(failed)}")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
