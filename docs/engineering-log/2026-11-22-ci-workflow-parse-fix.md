# Engineering log — 2026-11-22 CI workflow parse fix

- **Problem:** `.github/workflows/ci.yml` failed on every run (including `develop` at f07284c) with zero jobs: the
  workflow was rejected at parse time, so no Python or firmware check ran on any PR.
- **Cause:** The `firmware` job used `hashFiles(...)` in a job-level `if:`; `hashFiles` is only available in
  step-level contexts.
- **Change:** Dropped the job-level `if:`. A first step (`detect firmware sources`) runs
  `find firmware -regex '.*\.\(c\|cpp\|h\|ino\)' | grep -q .` and writes `found=true|false` to `$GITHUB_OUTPUT`; the
  apt install, clang-format and cppcheck steps run only when `found == 'true'`.
- **Evidence:** `actionlint` 1.7.12 flags the old file ("calling function \"hashFiles\" is not allowed here") and
  passes on the new one. Clean venv (Python 3.13 locally; CI uses 3.11): `pip install -e ".[dev]"` succeeds; ruff
  check/format, traceability (21 SR, 0 errors), DFMEA, WCCA and `pytest -q` (24 passed, 1 skipped: `cv2` not
  installed) pass; `python tools/check_all.py` passes. Today `firmware/` holds no C/C++ sources, so the firmware job
  reports success with its checks skipped.
- **Not applicable:** requirement/test report (no robot behavior change), DFMA/DFMEA/PFMEA (no part or process),
  WCCA (no wiring), SCCAF (no YC/YS row), ADR (no design choice between options). Security: CI change adds no permissions, secrets or third-party actions; `permissions: contents: read` unchanged.
- **Result:** Pending first run on GitHub after push.
