# CLAUDE.md — Autonomous Industrial Waste Cleaning and Separation Robot

This file is loaded in every Claude Code session. Read it fully before acting.
Deeper context lives in `docs/` — read the file that matches the task before answering.

## 1. What this project is

An autonomous mobile robot that cleans lubricant and metal chips from a machining-plant floor during shift changes,
separates the ferrous fraction and coarse solids from the liquid on board, compacts the chips, and stores the two
waste streams in separate containers. Capstone of *Proyecto Mecatrónico I/II*, Universidad Panamericana (Mexico).

- Controller: **Arduino UNO Q 2 GB (ABX00162)** — STM32U585 MCU (Zephyr + Arduino core, real time) + Qualcomm
  Dragonwing QRB2210 MPU (Debian Linux, Python), linked by the Arduino Bridge (RPC).
- Status (Nov 2026): **initial design, not frozen** (requirements, selection, conceptual design, 9 modules, priced
  BOM, simulations). Waiting on the vacuum (suction rig) test to validate the collection concept (ADR-0004) before
  freezing. **No physical prototype or test results yet.**
- Team (7): Franco Zavala Morgan · María Ruiz Mejía · Manuel Harari López · Ian Carlo Olivares Chávez ·
  Carlos Emiliano Escamilla Garibay · Luis Roberto Sánchez Salgado · Juan Manuel Vásquez Paniagua.
  Advisor: Dr. Hiram Eredín Ponce Espinosa.
- Language: code, commits, docs and deliverables in **English**; the team chats in Spanish. Keep original Spanish
  names (e.g., NOM titles) when they are proper names.

## 2. Where things are

| Path | Contents |
|---|---|
| `docs/00-project-context.md` | Full project knowledge: requirements, modules, BOM, interfaces, metrics, scenarios, economics, open decisions |
| `docs/01-lessons-learned.md` | 21 lessons from the previous UNO Q robot (maze solver). **Apply them by default.** |
| `docs/02-architecture.md` | MCU/Linux split, states, interfaces, safety chain |
| `docs/03-standards-matrix.md` | ISO / IEC / NOM applicability with clauses and evidence |
| `docs/04-business.md` | Business Model Canvas, economics, SWOT, technological impact |
| `docs/05-sustainability-sdg.md` | SDG mapping and environmental impact method |
| `docs/06-github-setup.md` | Branch rules, rulesets, CI checks |
| `docs/07-glossary.md` | Definitions and project lingo (check it before naming things) |
| `docs/08-sccaf.md` | Internal SCCAF: YC/YS → CC/SC special characteristics, register `risk/sccaf.csv` |
| `docs/adr/` | Architecture Decision Records (one decision per file) |
| `docs/engineering-log/` | Engineering log per stage |
| `docs/templates/` | DFMEA, PFMEA, DFMA, WCCA, requirement, BMC, impact, SDG, test-report templates |
| `requirements/requirements.yaml` | Single source of truth for requirements and traceability |
| `risk/` | DFMEA, SCCAF register, WCCA data |
| `tools/` | Python checkers and calculators (traceability, branch, commit msg, FMEA, WCCA, DFMA, economics) |
| `cad/` | Parametric OpenSCAD parts (`lib/`, `parts/`, `params/`) |
| `firmware/mcu/` | STM32U585 code (Zephyr / Arduino core) |
| `linux/` | QRB2210 Python app (navigation, web UI, logging) |
| `sim/` | Simulators (coverage, sensors with noise, replay of field logs) |

## 3. Non-negotiable rules

1. **Safety does not depend on software.** The e-stop opens the main relay coil in hardware. Never move a safety
   function into code only. Never remove the watchdog, current limits, float shut-off or force limit.
2. **Split by timing requirement, not by complexity.** MCU executes every motion order autonomously and stops by
   itself on obstacle, bumper, stale command or fault. Linux decides. If Linux is late, the robot stops — it never
   keeps moving on old commands.
3. **Requirements first.** Every feature, test and part traces to a requirement ID in `requirements/requirements.yaml`.
   New behavior without a requirement → write the requirement first (use `/req`).
4. **No claims without evidence.** Performance numbers are "estimate", "simulation" or "measured (date, conditions)".
   Never present simulation as a physical test. Mark inferences as "(deduced)".
5. **Thresholds come from measured data**: midpoint between two real readings, never from CAD or datasheet alone.
6. **One bad reading never changes state alone**: min-of-3, confirm jumps on 2 consecutive reads, capped vote counters.
7. **Simulate before tuning; log every run raw** (~20 Hz sensors + every decision) and make the simulator reproduce
   field failures.
8. **Measure real parts before modeling CAD.** CAD is parametric OpenSCAD; parameters in `cad/params/*.json`.
9. **Git:** never commit to `main`/`develop`; branch names and commit messages follow `CONTRIBUTING.md`; never
   `--force` push, never `--no-verify`. Do not commit unless the user asks. Run `python tools/check_all.py` before
   proposing a PR.
10. **Removing code is engineering.** Prefer deleting dead paths over adding flags.
11. If a request contradicts a lesson in `docs/01-lessons-learned.md` or a rule above, **say so before doing it**.
12. **Definition of done — every task validates and documents itself.** Say explicitly which artifacts apply and write
    them in the same PR; if one does not apply, write "N/A: <reason>" in the PR:

    | Task touches | Required artifacts |
    |---|---|
    | Any behavior | Requirement SR-xxx (`/req`) + test protocol and test report (`docs/test-reports/`) |
    | Part or assembly | DFMA worksheet (`/dfma`) + DFMEA rows (`/fmea`) + measured dimensions before CAD |
    | Process step (build, assembly, operation) | PFMEA rows (`/fmea`) |
    | Wiring, power, sensor interface | WCCA (`/wcca`) |
    | Safety function | DFMEA + ISO/NOM check (`/iso`) + re-verification test |
    | DFMEA row classed YC/YS | SCCAF register entry (`docs/08-sccaf.md`, `risk/sccaf.csv`) |
    | Camera, web UI, RPC, RFID, network, logs, dependencies, CI | Security review + threat model update (`/security`) |
    | Decision between options | ADR (`/adr`) |
    | Every task | Engineering log entry (`/log`): change, evidence, validation result |
    | Every PR | `CHANGELOG.md` entry under Unreleased: PR number, date, type, what changed, validation, IDs (CI-checked) |

## 4. Expert subagents (`.claude/agents/`)

Use them proactively when the task matches:
`systems-architect`, `requirements-engineer`, `dfma-fmea-engineer`, `wcca-engineer`, `embedded-safety-reviewer`,
`iso-compliance`, `business-analyst`, `cad-parametric`, `sustainability-sdg`, `test-sim-engineer`, `git-gatekeeper`,
`docs-writer`, `cybersecurity-engineer`. Multi-agent rule: one file per agent, agents never commit, give them the key facts in the prompt,
verify their claims (dates, order of events, commands) before integrating.

## 5. Slash commands (`.claude/commands/`)

`/req` new requirement · `/fmea` DFMEA/PFMEA entry · `/dfma` assembly review · `/wcca` worst-case analysis ·
`/iso` standards check · `/bmc` business canvas · `/econ` economic evaluation · `/impact` technological impact ·
`/sdg` SDG assessment · `/cad` parametric part · `/review` pre-PR review · `/log` log entry · `/adr` decision record · `/security` threat model + security review.

## 6. Commands that must pass

```bash
python tools/check_all.py          # branch, traceability, FMEA sanity, WCCA, ruff, pytest
pytest -q                          # unit tests for tools and linux/
ruff check . && ruff format --check .
```

## 7. Key numbers (do not re-derive unless inputs change)

Speed ≤ 0.38 m/s (0.15 m/s cleaning) · battery 12 V 24 Ah SLA, 144 Wh usable (50 % DoD) · ≈165 W average load
(incl. dosing pump) → ≈52 min · listed BOM MXN 15,849.50 (17,530.50 with tooling; ≈20,160 with 15 % contingency)
+ ≈1,000 dosing estimate → ≈21,310 · degreaser ≈20 mL/m² (estimate, ADR-0008) · metrics: M1 recovery
≥85 %, M2 purity ≥95 % liquid / ≥90 % solids, M3 coverage ≥100 m²/h with 0 incidents · simulation: 96 % coverage,
25.6 min, 167 m²/h, 68 Wh per cycle in a 12×8 m cell.
