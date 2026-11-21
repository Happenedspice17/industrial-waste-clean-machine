# Start here (first Claude Code session)

1. Create the GitHub repo (private), clone it, copy this kit into it, then:
   ```bash
   git switch -c chore/1-repo-bootstrap
   python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]"
   pre-commit install --hook-type pre-commit --hook-type commit-msg
   python tools/check_all.py
   git add -A && git commit -m "chore(repo): bootstrap project context, agents and checks"
   git push -u origin chore/1-repo-bootstrap   # open PR → main (first merge), then create develop from main
   ```
2. Protect `main` and `develop` (`docs/06-github-setup.md`), fill `.github/CODEOWNERS` with usernames.
3. First prompt to Claude Code:
   > Read CLAUDE.md and docs/00–02. Using the systems-architect and requirements-engineer agents, propose the
   > suction-rig test plan (ADR-0004), the requirements it verifies and the minimal firmware/Linux code needed to log
   > it at 20 Hz. Apply the lessons learned and warn me about any conflict.
4. Use the slash commands (`/req`, `/fmea`, `/wcca`, `/cad`, `/review`, …) — list them with `/help`.
