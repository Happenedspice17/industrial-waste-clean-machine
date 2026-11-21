# 07 · Glossary and project lingo

Definitions as used in this repo. When a term has two meanings, the **watch out** column says how to tell them apart.
Add a term here the first time it appears in a doc, PR or chat summary.

## IDs and naming

| Term | Meaning | Watch out |
|---|---|---|
| R1–R10 | Stakeholder requirements (importance 1–10) in `requirements/requirements.yaml` | Not ranked; equal values are intentional |
| SR-NNN | System requirement, child of an R or another SR; exactly one "shall" | Status draft → approved → verified |
| OE1–OE6 | Specific objectives of the project (proposal) | Map to R IDs in `docs/00-project-context.md` §2 |
| **M1–M9 (modules)** | Chassis, Mobility, Collection, Separation, Storage, Perception, Control, Power + safety, Operator interface | Same letters as the metrics; say "module M3" |
| **M1–M3 (metrics)** | Recovery, Purity, Coverage pass thresholds | Say "metric M1"; in code use `metric_m1` |
| I1–I13 | Interfaces between modules (power, signals, hose, gravity flow, rails) | Listed in `docs/00-project-context.md` §5 |
| C01–C36 | Component codes from the selection matrices | C05, C07, C09 retired |
| F-NNN | DFMEA/PFMEA row ID in `risk/dfmea.csv` | Unique; checked by `tools/fmea.py` |
| SC-NNN | SCCAF register row in `risk/sccaf.csv` | Not "SC" the class |
| TP-xxx | Test protocol (e.g., TP-V01 vision validation) in `docs/test-reports/` | Protocol = plan; report = result |
| ADR-NNNN | Architecture Decision Record in `docs/adr/` | One decision per file |
| Team A/B/C/D | Build teams: A chassis + mobility, B separation + storage, C power + safety + HMI, D control + navigation + vision | |

## Engineering method

| Term | Meaning |
|---|---|
| DFMA | Design for Manufacture and Assembly: part count, assembly time, design efficiency `DE = 3·Nmin/Σt` (`tools/dfma.py`) |
| DFMEA / PFMEA | Design / Process Failure Mode and Effects Analysis: each failure mode scored S × O × D |
| S, O, D, RPN | Severity, Occurrence, Detection (1–10); RPN = S × O × D. Any S ≥ 9 needs an action (`tools/fmea.py`) |
| WCCA | Worst-Case Circuit Analysis: tolerances, temperature and supply limits on an interface (`tools/wcca.py`) |
| EVA / RSS | Extreme Value Analysis (all limits at once) / Root Sum Square (statistical) — the two WCCA methods |
| Verification methods | Test, Analysis, Inspection, Demonstration — one per SR |
| Traceability | R → SR → test/report link checked by `tools/check_traceability.py` |
| Definition of done | Artifacts every task must leave (`CLAUDE.md` rule 12) |
| Evidence labels | "estimate", "simulation", "measured (date, conditions)", "(deduced)" — every number carries one |
| Midpoint threshold | Threshold set halfway between two measured real readings, never from CAD or a datasheet alone |
| Min-of-3 / 2-read confirm / capped votes | Filters so one bad reading never changes state (lesson 4) |
| Log-only mode | A sensor or function runs and logs, but its output changes nothing until validated (a.k.a. shadow mode) |
| Validation gate | Rule that an output is enabled only after its protocol passes on the real robot (SR-017) |
| Engineering log | One entry per stage: problem, hypothesis, change, evidence, reasoning, result, commits (`docs/engineering-log/`) |
| Lessons learned | 21 rules from the maze-solver robot (`docs/01-lessons-learned.md`) |
| Suction rig | Bench test of vacuum + hose + tank before building the robot (ADR-0004) |
| Option A / B (collection) | A: brush + vacuum carry oil and chips. B: brush throws chips to a front hopper; vacuum takes only liquid |
| Idealist / pessimist scenario | Best / worst plant conditions used to judge the design (`docs/00-project-context.md` §7) |
| Protection terms | The 10 design safeguards (safety factor, current limit, fuses, …) in §6 of the context file |
| n | Structural safety factor (n ≥ 2 general, n ≥ 3 at bump mounts) |
| Threat model | Assets, data flows, trust boundaries and threats with controls (`docs/templates/threat-model.md`) |
| STRIDE | Threat classes: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege |
| IEC 62443 / SL | Industrial cybersecurity standard family / security level (target SL 1–2 for the prototype) |
| CSRF | Cross-site request forgery: a page tricks the browser into a state-changing request — state changes use POST + token |
| BadUSB | A USB device that pretends to be another class (e.g., a "camera" that types like a keyboard) |
| SCCAF | Special Characteristics Communication and Agreement Form (Ford FAF03-111-2); internal version in `docs/08-sccaf.md` |
| Special characteristic | A product/process characteristic whose variation affects safety, regulation or a key metric |
| YC / YS | Potential critical (DFMEA S 9–10) / potential significant (S 5–8 and O 4–10) characteristic |
| CC / SC | Critical / significant characteristic agreed after PFMEA and control plan |
| Control plan | List of how each characteristic is checked during build (method, frequency, reaction) |
| PPAP | Production Part Approval Process (automotive); here replaced by test report + measured parts |
| STA | Supplier Technical Assistance (Ford); here the module's purchasing/supplier lead |

## Robot and control

| Term | Meaning | Watch out |
|---|---|---|
| UNO Q | Arduino UNO Q 2 GB board: STM32U585 **MCU** (real time, Zephyr) + Qualcomm QRB2210 **MPU** (Debian Linux, Python) | "Linux side" = MPU |
| Bridge / RPC | Arduino link between MCU and Linux used for commands and status | Latency must be measured |
| Heartbeat / T_stale | Linux sends a heartbeat every 100 ms; the MCU stops all motion if none arrives within T_stale (≈300 ms, to tune) | |
| Segment | One motion order (`move(segment_id, …)`) the MCU executes and finishes by itself | |
| Split by timing | MCU owns everything with a deadline; Linux decides with the robot stopped or between segments (ADR-0002) | |
| E-stop | Mushroom button that opens the main relay coil in hardware; restart needs RFID card + start button | Never software-only |
| Float shut-off | Mechanical float that closes the vacuum port before liquid reaches the motor | Hardware, not code |
| Level cut-off | MCU stops suction when floats report full | Floats are the authority |
| Watchdog | MCU timer that stops everything if the control loop or checks fail | Never removed |
| Sensor authority | The sensor that decides a quantity; others only support (`docs/02-architecture.md`) | |
| Residue check | Vision task: flags uncleaned patches behind the squeegee → re-pass request (SR-015) | Advisory only |
| Container-level cross-check | Vision task: reads tank/basket low-half-full and warns if floats disagree (SR-016) | Advisory only |
| Boustrophedon | Back-and-forth (lawn-mower) coverage pattern used in the coverage simulation | |
| Scan matching | Aligning a LiDAR scan to the saved map to correct pose drift | |
| Localize against a saved map | Map once, save, then localize every shift (lesson 8) | Not full SLAM |
| IMU mode | BNO055 fusion without magnetometer (steel distorts it) | |

## Process, plant and business

| Term | Meaning | Watch out |
|---|---|---|
| Shift change | The cleaning window between production shifts (≥ 30 min idealist, < 15 min pessimist) | |
| Chips / swarf | Metal cuttings from machining (Spanish: *viruta*) | |
| Ferrous fraction | The magnetic (steel/iron) part of the chips, captured by magnets | |
| Compaction | Pressing chips in the basket to drain oil and reduce volume (≤ 100 kgf) | |
| Squeegee | Rubber blade that pushes the oil film to the nozzle (Spanish: *jalador*) | |
| Leak tray | Tray under tank and chamber that contains drips | |
| **DoD (battery)** | Depth of discharge — 50 % for the SLA battery | Not "definition of done" — always spell that one out |
| SLA | Sealed lead-acid battery (12 V 24 Ah) | |
| BOM | Bill of materials (listed MXN 15,849.50) | |
| NPV / payback | Net present value (3 yr, 12 %) / time to recover the investment | Base vs pessimistic case |
| BMC | Business Model Canvas (`docs/04-business.md`) | |
| SDG | UN Sustainable Development Goals (Spanish: ODS) | |
| NOM / STPS / SEMARNAT | Mexican official standards / labor ministry / environment ministry | NOM titles stay in Spanish |
| ISO 3691-4 | Safety standard for driverless industrial trucks (AGV/AMR) | |
| AGV / AMR | Automated guided vehicle / autonomous mobile robot | |

## Git and tooling

| Term | Meaning |
|---|---|
| `main` / `develop` | Released branch / integration branch. Never commit on them directly |
| Work branch | `<type>/<issue>-<desc>`; Claude cloud sessions use `claude/<name>` |
| Conventional Commit | `type(scope): subject`, e.g., `feat(m3): …`; body `Refs: SR-xxx` |
| PR | Pull request into `develop` (releases: `develop` → `main`) |
| CI checks | `policy` (names, PR body) and `python` (ruff, pytest, traceability, FMEA, WCCA) |
| `check_all.py` | Runs every local check before a PR |
| Pre-commit | Local hooks: ruff, branch name, commit message, traceability |
| CODEOWNERS | Who must be asked to review a path (repo owner) |

## Spanish ↔ English (team chat → repo)

| Spanish | English in repo |
|---|---|
| bitácora | engineering log |
| viruta | chips |
| jalador | squeegee |
| cambio de turno | shift change |
| paro de emergencia | emergency stop (e-stop) |
| tanque / canastilla | tank / basket |
| requisito | requirement |
| entregable | deliverable |
| comparación por pares | pairwise comparison |
| matriz de calidad | quality (weighted) matrix |
| escenario idealista / pesimista | idealist / pessimist scenario |
| ODS | SDG |
