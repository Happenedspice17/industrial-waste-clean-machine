# 06 · GitHub setup and branch validation

## Branch model

- `main`: released, demo-ready. Protected. Only merges from `develop` or `release/*` / `hotfix/*` via PR.
- `develop`: integration. Protected. Merges from work branches via PR.
- Claude Code cloud sessions push to `claude/<session-name>`; merge them into `develop` by PR like any work branch.
- Work branches: `<type>/<issue>-<short-desc>` with type in
  `feature | fix | hw | cad | docs | test | sim | refactor | chore | exp`, e.g. `feature/12-suction-rig-logger`,
  `cad/18-wheel-hub-hex`. Release: `release/vX.Y.Z`. Hotfix: `hotfix/<issue>-<desc>`.
- Commits: Conventional Commits `type(scope): subject` (scope = module m1..m9, req, docs, ci, cad, sim, fw, linux).
  Reference requirement IDs in the body: `Refs: SR-012`.

## Checks (CI, `.github/workflows/`)

| Workflow | Job | Blocks merge |
|---|---|---|
| `branch-policy.yml` | branch name, PR title (Conventional Commit), PR body has requirement refs + test evidence | Yes |
| `ci.yml` | ruff, pytest, traceability check, FMEA/WCCA sanity, markdown links (light) | Yes |
| `ci.yml` (`firmware`) | clang-format check + cppcheck when `firmware/**` has C/C++ | Yes |
| `cad.yml` | OpenSCAD render of changed parts to STL artifact | Yes (render must succeed) |

## Who can push

Only the repository owner (`Happenedspice17`) has write access; Claude Code pushes through the owner's account
(Claude GitHub App). Team members contribute through forks + PRs or as read-only collaborators. Because the owner
cannot approve their own PRs, `branch-protection.json` requires 0 approvals and relies on the `policy` and `python`
checks; raise it to 1 if a second writer is added.

## Rulesets (run once with admin rights)

```bash
REPO=<owner>/<repo>
gh api -X PUT repos/$REPO/branches/main/protection --input .github/branch-protection.json
gh api -X PUT repos/$REPO/branches/develop/protection --input .github/branch-protection.json
```

If the CLI call is awkward, set the same rules in Settings → Rules → Rulesets: require PR, required checks (approvals: 0 while solo), dismiss stale
approvals, require status checks `policy` and `python` (plus `firmware`/`cad` when relevant), block force pushes,
require linear history, restrict deletions.

## Local guards

- `pre-commit install --hook-type pre-commit --hook-type commit-msg` → ruff, branch check, commit message check.
- Claude Code hook `.claude/hooks/pre_bash_guard.py` blocks commits/pushes on `main`/`develop`, `--force`, `--no-verify`.
