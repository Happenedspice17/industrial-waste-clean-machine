# Requirements

`requirements.yaml` is the single source of truth. Every feature, part and test traces to an ID here (rule 3 in
[`CLAUDE.md`](../CLAUDE.md)); rules for writing them are in `.claude/agents/requirements-engineer.md`.

| Level | IDs | Today (Nov 2026) |
|---|---|---|
| Stakeholder | R1–R10, importance 1–10 | 10 (collection, separation, safe mobility and separate storage weigh 10) |
| System | SR-001–SR-021, each with `parent`, `module`, `priority`, `status`, `verified_by` | 21, all `draft`; SR-018–SR-021 verified by TP-V02 (AprilTag bench app) |
| Ethical (IEEE 7000) | EVR-01 safety · EVR-02 environment · EVR-03 privacy | Draft in the final presentation v2; to add here with `/req` once the team approves |

## Traceability chain

`R` → `SR` → test (`def test_sr004_…` or `Refs: SR-004` in [`docs/test-reports/`](../docs/test-reports/)) → evidence.
Approved requirements list their tests in `verified_by`. `python tools/check_traceability.py` (part of
`tools/check_all.py` and CI) enforces structure and links.

## Adding one

Use `/req`: write the requirement before the code, with a measurable acceptance criterion and the evidence label
(estimate, simulation or measured).
