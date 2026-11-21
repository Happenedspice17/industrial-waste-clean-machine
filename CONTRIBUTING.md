# Contributing

## Flow
1. Open/assign an issue (requirement, bug or risk template).
2. Branch from `develop`: `git switch -c <type>/<issue>-<short-desc>`
   types: feature, fix, hw, cad, docs, test, sim, refactor, chore, exp · release/vX.Y.Z · hotfix/<issue>-<desc>.
3. Commit with Conventional Commits: `type(scope): subject` (types: feat, fix, docs, test, refactor, perf, build, ci,
   chore, revert, hw, cad, sim, req, risk; scope: m1..m9, fw, linux, sim, cad, req, docs, ci). Body: `Refs: SR-xxx`.
4. `python tools/check_all.py` must pass. Open a PR to `develop` with the template filled. One approval required.
5. Releases: `release/vX.Y.Z` → PR to `main` → tag. Mark the demo version as final in README (lesson 21).

Never: commit on `main`/`develop`, force push, `--no-verify`, commit secrets or raw logs (use release assets).

## Setup
```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pre-commit install --hook-type pre-commit --hook-type commit-msg
```
