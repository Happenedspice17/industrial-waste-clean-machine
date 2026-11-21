# Engineering log — 2026-11-21 Status "initial design" and cybersecurity agent

- **Problem:** README/CLAUDE.md said "design phase complete", but the design is not frozen until the vacuum (suction
  rig) test validates the collection concept. No owner existed for cybersecurity (vision data, web UI, RPC, RFID).
- **Change:** Status set to "initial design, not frozen; waiting on vacuum test (ADR-0004)". Added
  `cybersecurity-engineer` agent, `/security` command, threat-model template, glossary terms, PR checklist item and a
  definition-of-done row; `/review` now runs the security agent on attack-surface changes.
- **Evidence:** `python tools/check_all.py` passes. No threat model written yet (first `/security` run will create
  `docs/security/threat-model.md`).
- **Reasoning:** Security must never weaken safety: stops work with Linux compromised; vision stays advisory.
- **Result:** Pending: first threat model, security SRs, security test protocol.
- **Commits:** branch `chore/security-agent-initial-design`.
