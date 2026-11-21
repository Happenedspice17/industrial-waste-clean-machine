# Requirements

`requirements.yaml` is the single source of truth. Rules in `.claude/agents/requirements-engineer.md`.
Tests reference requirements by ID (e.g., `def test_sr004_overspeed_cut():` or a `Refs: SR-004` line in a test report),
and approved requirements list them in `verified_by`. `python tools/check_traceability.py` enforces it.
