#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block unsafe git operations.

Reads the hook JSON from stdin. Exit code 2 blocks the tool call and shows stderr to Claude.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

PROTECTED = {"main", "master", "develop"}


def current_branch() -> str:
    try:
        out = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def check(command: str, branch: str) -> str | None:
    cmd = " ".join(command.split())
    if re.search(r"\bgit\b.*\s--no-verify\b", cmd):
        return "Blocked: --no-verify bypasses project checks."
    if re.search(r"\bgit\s+push\b.*(\s--force\b|\s-f\b|\s--force-with-lease\b)", cmd):
        return "Blocked: force push is not allowed (see CONTRIBUTING.md)."
    if re.search(r"\bgit\s+push\b.*\b(origin\s+)?(main|master|develop)\b", cmd):
        return "Blocked: push to protected branch. Open a PR instead."
    if re.search(r"\bgit\s+commit\b", cmd) and branch in PROTECTED:
        return f"Blocked: do not commit on '{branch}'. Create a branch: git switch -c <type>/<issue>-<desc>."
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = (data.get("tool_input") or {}).get("command", "")
    if not command:
        return 0
    msg = check(command, current_branch())
    if msg:
        print(msg, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
