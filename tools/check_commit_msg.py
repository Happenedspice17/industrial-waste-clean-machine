#!/usr/bin/env python3
"""Validate a Conventional Commit message (file path argument, as used by the commit-msg hook) or a PR title."""

from __future__ import annotations

import re
import sys

TYPES = "feat|fix|docs|test|refactor|perf|build|ci|chore|revert|hw|cad|sim|req|risk"
HEADER = re.compile(rf"^({TYPES})(\([a-z0-9-]+\))?(!)?: [^\s].{{2,71}}$")


def validate(message: str) -> list[str]:
    lines = message.strip().splitlines()
    if not lines:
        return ["empty message"]
    header = lines[0]
    errors: list[str] = []
    if header.startswith(("Merge ", 'Revert "')):
        return errors
    if not HEADER.match(header):
        errors.append(f"header must be '<type>(<scope>): <subject>' (types: {TYPES.replace('|', ', ')}; max 72 chars)")
    if header.endswith("."):
        errors.append("subject must not end with a period")
    if len(lines) > 1 and lines[1].strip():
        errors.append("second line must be blank")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: check_commit_msg.py <file-or-text>", file=sys.stderr)
        return 2
    arg = argv[1]
    try:
        with open(arg, encoding="utf-8") as fh:
            msg = "\n".join(line for line in fh.read().splitlines() if not line.startswith("#"))
    except OSError:
        msg = arg
    errors = validate(msg)
    if errors:
        for e in errors:
            print(f"check_commit_msg: {e}", file=sys.stderr)
        return 1
    print("check_commit_msg: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
