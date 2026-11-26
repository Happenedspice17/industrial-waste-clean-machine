# Risk, quality and security analysis

The project treats risk like a requirement: every failure mode, special characteristic, circuit and threat is in a
file that a script checks on every change. This chapter presents the current state of each register.

## Design FMEA (DFMEA)

Source: `risk/dfmea.csv` · tool: `python tools/fmea.py risk/dfmea.csv`. Severity (S), occurrence (O) and detection
(D) are scored 1–10; RPN = S × O × D. Any row with S ≥ 9 gets a **mandatory** action regardless of RPN.

**(a) Failure modes**

| ID | Item | Function | Failure mode | Effect | Cause |
|---|---|---|---|---|---|
| F-001 | M3 vacuum unit | Lift oil and chips | Cannot lift steel chips | Chips stay on floor (M1 fails) | 80 W motor below pickup velocity for steel |
| F-004 | M2 drive | Stop within distance on oil | Wheel slip on oil | Collision | Low friction (mu ~ 0.1) |
| F-005 | M7 MCU/Linux link | Keep commands fresh | Linux late / RPC stall | Robot moves on stale command | Side load (web queries; clock jumps) |
| F-008 | M6 vision container check | Cross-check tank and basket level | Vision reads wrong level | False 'check floats' warning or missed float fault | Oil film on tank wall; poor view angle |
| F-007 | M6 vision residue check | Flag uncleaned patches | False residue on oil sheen or chip glare | Extra re-pass (time lost; M3 drops) | Specular reflections from LED on oily floor |
| F-002 | M5 tank | Hold liquid without reaching vacuum | Liquid reaches vacuum port | Vacuum motor damage; electric hazard | Overfill / float stuck |
| F-006 | M4 compactor | Press chips with limited force | Over-force / pinch | Part breakage; finger injury | Load-cell failure; lid open |
| F-003 | M8 e-stop | Cut actuator power | Relay contacts weld | Robot keeps moving after e-stop | Inrush above contact rating |
| F-009 | M6 vision software | Stay advisory | Vision output enabled before validation | Wrong re-pass or warnings in plant | Flag switched on without evidence |

**(b) Scores, controls and actions** (sorted by RPN)

| ID | S | O | D | RPN | Class | Prevention | Detection control | Action | Owner | Req. |
|---|:-:|:-:|:-:|:-:|:-:|---|---|---|---|---|
| F-001 | 7 | 6 | 4 | 168 | YS | Suction rig test before build | Rig test chip lift g/s | Decide A/B (ADR-0004) | Team A | SR-001 |
| F-004 | 8 | 5 | 4 | 160 | YS | Speed limit; rubber wheels | Braking test on oiled floor | Braking tests 10x | Team A | SR-005 |
| F-005 | **9** | 4 | 3 | 108 | YC | Heartbeat + T_stale on MCU | Fault injection test | Test heartbeat loss | Team D | SR-007 |
| F-008 | 5 | 5 | 4 | 100 | YS | Floats stay authority; vision warns only | TP-V01 fill/drain cycles | Run TP-V01; decide camera placement via DFMA | Team D | SR-016 |
| F-007 | 4 | 6 | 4 | 96 | — | Shroud + fixed exposure + reflection filter (ADR-0006) | TP-V01 labelled frames | Run TP-V01; test cross-polarized LED | Team D | SR-015 |
| F-002 | **9** | 3 | 3 | 81 | YC | Float shut-off in hardware + level cut-off | Overfill test | Test float shut-off 5x | Team B | SR-008 |
| F-006 | **9** | 3 | 3 | 81 | YC | Force limit + lid interlock | Load-cell log; interlock test | Interlock + limit tests | Team B | SR-009 |
| F-003 | **10** | 2 | 4 | 80 | YC | 40 A relay; inrush calc in WCCA | Periodic e-stop test | WCCA relay inrush; consider second relay in series | Team C | SR-006 |
| F-009 | 6 | 3 | 3 | 54 | — | Flags default off; PR checklist needs TP-V01 report | Code review + traceability check | Enforce SR-017 in review | Team D | SR-017 |

**Reading.** The top risk by RPN is exactly why the design is not frozen: can an 80 W, 12 V vacuum lift steel chips
(F-001, RPN 168)? The second is wheel slip on oil (F-004). Four rows have S ≥ 9 (F-002, F-003, F-005, F-006): they are
the safety functions, and all four have hardware or MCU controls plus a re-verification test. All rows are **open**
until their test runs. PFMEA rows (`risk/pfmea.csv`) will be written when the build and assembly process steps are
defined.

## Internal SCCAF — special characteristics

Source: `docs/08-sccaf.md`, register `risk/sccaf.csv`. An internal version of the Special Characteristics
Communication and Agreement Form (Ford FAF03-111-2 under procedure FAP-03-111 [64]), adapted to an academic prototype.
Purpose: every characteristic that can hurt someone, break a regulation or make a metric fail is identified in the
DFMEA, gets an agreed control before build, and is traced to its validation evidence. The class is **computed** from
the DFMEA by `tools/fmea.py::special_class()`, so it cannot drift; CI fails if a YC/YS row has no register entry or a
different class.

| DFMEA severity (S) | Occurrence (O) | Design class | Agreed class after PFMEA / control plan | Typical control |
|---|---|---|---|---|
| 9–10 (safety, regulation) | any | **YC** — potential critical | **CC** — critical | Error-proofing or 100 % check, re-verified after any change |
| 5–8 | 4–10 | **YS** — potential significant | **SC** — significant | Measured check per build/batch with recorded results |
| 5–8 | 1–3 | none | none | Normal design and build controls |
| 1–4 | any | none | none | Normal design and build controls |

| SCCAF | DFMEA | Class | Characteristic | Specification | Control method | Design / build / validation owner | Status |
|---|---|:-:|---|---|---|---|---|
| SC-001 | F-001 | YS | Chip lift rate at the nozzle (g/s) | TBD from suction rig (ADR-0004) | Suction rig test before build; repeat after any nozzle/hose change | Team A / A / D | open |
| SC-002 | F-002 | YC | Float shut-off closes vacuum port before liquid reaches it | Closes with port margin TBD (measured) | Overfill test 5× after build and after any tank/float change | Team B / B / C | open |
| SC-003 | F-003 | YC | Main relay contact rating vs worst-case inrush | Rating > WCCA inrush with margin | WCCA + periodic e-stop cut test | Team C / C / C | open |
| SC-004 | F-008 | YS | Vision container-level agreement with floats | ≥ 95 % (SR-016) | TP-V01 fill/drain cycles; log-only until pass | Team D / D / D | open |
| SC-005 | F-004 | YS | Stopping distance on oiled floor from 0.38 m/s | ≤ 0.10 m (SR-005) | Braking test 10× on reference oil; speed limit in MCU | Team A / A / D | open |
| SC-006 | F-005 | YC | MCU stop on heartbeat loss (T_stale) | All motion stops within T_stale (SR-007) | Fault-injection test (kill Linux app / block RPC) after every firmware release | Team D / D / C | open |
| SC-007 | F-006 | YC | Compactor force limit and lid interlock | ≤ 100 kgf; no motion with lid open (SR-009) | Load-cell log + interlock test after any compactor change | Team B / B / C | open |

All seven are pending advisor sign-off (Dr. Hiram Eredín Ponce Espinosa) and are built at the UP lab. Note the
deliberate separation of duties: for the four critical (YC) characteristics, the validation owner is a different
team from the design owner.

### SCCAF workflow and role mapping

1. DFMEA row written → `tools/fmea.py` prints its class (YC / YS / none).
2. YC/YS → row in `risk/sccaf.csv`: characteristic, specification (measured, not from CAD alone), proposed control,
   owners, `agreed_class` = TBD.
3. Process step defined → PFMEA rows and control method; `agreed_class` set to CC or SC.
4. Agreement: design owner, build owner, validation owner and advisor sign; decision recorded in the engineering log.
5. Validation evidence: test report in `docs/test-reports/` referencing the SR; `status` = closed only then.

| Ford role | This project |
|---|---|
| Product Development | Design owner: module team (A/B/C/D) |
| Supplier Technical Assistance (STA) | Purchasing / supplier lead of the module team |
| Manufacturing | Build owner: team that assembles the module |
| Supplier and sub-tier | Vendors and print services |
| PPAP submission | Test report + measured parts before integration |
| Approval | Advisor sign-off |

The SCCAF also applies when a part changes source or build location with the same design (new supplier, another 3D
printer or filament, another workshop) and when a control changes before validation.

## Worst-case circuit analysis

The WCCA results are in Section 7.8. Summary: 8 checks, 7 pass and 1 warning (battery-sense divider margin 4.1 %).
Open WCCA items: relay inrush for F-003/SC-003; USB hub power budget with LiDAR + camera on the same hub (ADR-0001,
ADR-0006); UNO Q supply limits (to verify against the official documentation).

## Design for manufacture and assembly (DFMA)

Source: `risk/dfma/m4_separation_example.csv` · tool: `python tools/dfma.py`. First pass on module M4 (separation
chamber), Boothroyd–Dewhurst method [69].

| Part | Qty | Theoretical minimum | Handling (s) | Insertion (s) |
|---|:-:|:-:|:-:|:-:|
| Chamber body | 1 | 1 | 1.95 | 1.5 |
| Lid | 1 | 1 | 1.95 | 2.5 |
| Lid screws M5 | 4 | 0 | 1.8 | 5.0 |
| Mesh basket | 1 | 1 | 1.95 | 2.0 |
| Magnet bars | 10 | 0 | 2.5 | 3.0 |
| Magnet holder | 1 | 0 | 1.95 | 4.0 |
| Chip basket | 1 | 1 | 1.95 | 1.5 |
| Actuator | 1 | 1 | 2.25 | 6.0 |
| Actuator bracket | 1 | 0 | 1.95 | 4.0 |
| Bracket screws M5 | 4 | 0 | 1.8 | 5.0 |
| Pressing plate | 1 | 1 | 1.95 | 3.0 |
| Gasket | 1 | 0 | 3.0 | 6.5 |

| Result | Value |
|---|---|
| Parts / theoretical minimum | 27 / 6 |
| Total assembly time | 159.3 s |
| Design efficiency $DE = 3 N_{min} / \sum t$ | **11.3 %** |

**Reading and actions.** 11.3 % is low (well-designed assemblies reach 25–60 %, deduced from typical DFMA practice):
fasteners and separate magnets dominate the time. Before CAD: mold or print the magnet holder into the chamber wall
(10 magnets + holder → one insert), replace the four lid screws with two quarter-turn latches or a clamp ring, and
integrate the actuator bracket into the chamber body. Re-run `tools/dfma.py` after each change.

## Cybersecurity threat model

Source: `docs/security/threat-model.md` (rev 1, 22 Nov 2026). Scope: the AprilTag bench localization app on the UNO Q
Linux side, its web page on port 7000, its log and the Bridge pose message to the MCU sketch. Method: STRIDE per data
flow [70]; risk = impact (1–5) × likelihood (1–5). Target security level for the prototype: IEC 62443 SL 1–2 [71].

### Assets

| Asset | Why it matters |
|---|---|
| Camera frames | Privacy: plant staff can be in view |
| Pose estimate | Integrity: a wrong pose could mislead tests or, later, navigation |
| Mount / tag configuration | Integrity: changes every pose |
| `run.jsonl` log | Evidence for tests (integrity); holds poses and timings, no images |
| Board availability | The same Linux side will run navigation later |

### Data flows and trust boundaries

| Flow | From → To | Channel | Crosses boundary? |
|---|---|---|---|
| Camera frames | USB camera → app (Linux) | USB / V4L2 | Yes (physical device) |
| Page, pose JSON, log | App → any browser on the network | HTTP, port 7000, no auth, no TLS | Yes |
| Calibration commands | Browser → app (`POST /calibrate`, `/calibrate/apply`) | HTTP, no auth | Yes |
| Validated pose | App → MCU sketch | Bridge RPC `pose` | Yes (Linux not trusted for safety) |
| Printed tags | Environment → camera | Optical | Yes |

### Threats

| ID | STRIDE | Attack scenario | I | L | Risk | Control | SR | Status |
|---|:-:|---|:-:|:-:|:-:|---|---|---|
| T-01 | I | Anyone on the network opens `/frame.jpg` and sees people at the machines | 4 | 3 | 12 | `STREAM = False` default: no frame kept, `/frame.jpg` → 404; no images on disk | SR-020 | mitigated (sim-tested) |
| T-02 | I | Anyone on the network downloads `run.jsonl` (poses, timings, camera info) | 2 | 3 | 6 | No personal data in the log; lab network only | SR-020 | accepted (bench) |
| T-03 | T | A LAN user presses **Apply** with bad calibration values; poses become wrong or vanish | 3 | 2 | 6 | Session-only (restart restores committed values); applied values logged; pose to MCU is print-only | SR-021 | open until auth |
| T-04 | D | Request flood or repeated 20 MB log downloads slow the board | 2 | 2 | 4 | Log rotates at 20 MB; lab network only | — | accepted (bench) |
| T-05 | S | Someone places a fake tag with a known ID; pose jumps | 2 | 2 | 4 | `tags_disagree` and `reproj` checks refuse inconsistent views; LiDAR stays the authority | SR-018 | mitigated |
| T-06 | E | Pose messages used later to drive motion without validation | 5 | 1 | 5 | SR-017 log-only gate; MCU sketch only prints; test estimates never sent | SR-017, SR-019 | mitigated (inspection) |

**Residual risks.** No authentication or TLS on port 7000: accepted only on an isolated lab network. Before any use on
the plant network or with motion enabled: add a token on every request (or disable the page), require it for POST,
and serve over TLS (a new SR will be written then). Turning `STREAM = True` for debugging exposes T-01 again; it must
be set back to `False` before committing. Future scope of the threat model: RFID authorization (cloning of cards),
the full web UI, Wi-Fi, firmware updates, dependencies and the CI supply chain.
