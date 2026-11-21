#!/usr/bin/env python3
"""Validate the current (or given) branch name against the project convention."""

from __future__ import annotations

import os
import re
import subprocess
import sys

TYPES = "feature|fix|hw|cad|docs|test|sim|refactor|chore|exp"
PATTERNS = [
    rf"^({TYPES})/([0-9]+-)?[a-z0-9][a-z0-9-]{{2,60}}$",
    r"^release/v\d+\.\d+\.\d+$",
    r"^hotfix/([0-9]+-)?[a-z0-9][a-z0-9-]{2,60}$",
    r"^claude/[a-z0-9-]{3,60}$",  # Claude Code cloud sessions push here; merge via PR to develop
]
LONG_LIVED = {"main", "develop"}


def is_valid(name: str) -> bool:
    return name in LONG_LIVED or any(re.match(p, name) for p in PATTERNS)


def current_branch() -> str:
    env = os.environ.get("GITHUB_HEAD_REF") or os.environ.get("BRANCH_NAME")
    if env:
        return env
    out = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=False)
    return out.stdout.strip()


def main(argv: list[str]) -> int:
    name = argv[1] if len(argv) > 1 else current_branch()
    if not name or name == "HEAD":
        print("check_branch: detached HEAD or no git repo, skipped")
        return 0
    if is_valid(name):
        print(f"check_branch: OK ({name})")
        return 0
    print(
        f"check_branch: INVALID branch '{name}'. Use <type>/<issue>-<desc> with type in {TYPES.replace('|', ', ')}, "
        "release/vX.Y.Z or hotfix/<issue>-<desc> (lowercase, hyphens).",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
