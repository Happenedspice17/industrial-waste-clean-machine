# Methodology and course activities

## Design methodology: the VDI 2206 V-model

The project follows the V-model for mechatronic systems in VDI 2206 [22]: it goes from requirements to a system
architecture, develops each domain (mechanical, electrical, software) in parallel and integrates them through staged
verification. The left branch (specification and design) is the work of this semester; the right branch (integration
and verification) is next semester's work, but its acceptance criteria are already fixed (Chapter 13), so the tests
cannot be bent to fit the results.

| V-model stage | What the team did | Where | Status |
|---|---|---|---|
| Requirements | Need, literature, five patents, ten weighted stakeholder requirements (R1–R10), 25 system requirements, three ethical value requirements | Ch. 1, 3 · `requirements/requirements.yaml` | Done |
| System design | Quality matrix (0/1/3/9), 231-pair comparison, black box, white boxes, morphological matrix (18 functions) | Ch. 3, 5 | Done |
| Architecture | Nine modules, 13 interfaces, MCU/Linux split, safety chain, states, sensor hierarchy | Ch. 6 · `docs/02-architecture.md` | Done |
| Domain design | Priced BOM, calculations, WCCA, DFMA, first CAD part, bench software | Ch. 7, 9, 11 | Partial (by plan) |
| First evidence | Handheld suction pre-test TP-S01 → degreaser decision ADR-0008 → rig protocol TP-S02 | Ch. 12, 13 | Exploratory test done |
| Analysis of the concept | Scenarios, simulation, DFMEA, SCCAF, threat model, economics, impact | Ch. 7–9, 14–16 | Done |
| Integration and verification | Suction rig → modules → integration → M1–M3 and safety tests → pilot | Ch. 13, 18 | Next semester |

The conceptual-design tools come from systematic engineering design: the black box and function structure abstract
the product as flows of material, energy and signals, and the morphological matrix combines alternative working
principles for each function into concepts [18]. Requirement weighting, concept screening and the product
architecture follow Ulrich, Eppinger and Yang [17]. The quality matrix uses the 0/1/3/9 relationship scale of the
house of quality [19], the component comparison borrows the pairwise logic of the analytic hierarchy process [20],
the goal tree follows the logical-framework approach [21], and the ethical analysis follows the value-based
engineering process of IEEE 7000-2021 [58].

## Engineering method applied throughout

Besides the course tools, the team applied a set of engineering practices from industry and from its previous robot
(Chapter 17). They are enforced by the repository, not just written down.

| Practice | What it means in this project | Enforcement |
|---|---|---|
| Requirements first | Every feature, test and part traces to a requirement ID | `tools/check_traceability.py` in CI |
| Evidence labels | Every number is calculation, estimate, simulation or measured (date, conditions) | Review rule; PR template |
| Risk analysis per change | DFMEA rows for every new part or function; any S ≥ 9 needs an action | `tools/fmea.py` in CI |
| Special characteristics | DFMEA rows classed YC/YS must have an agreed control (internal SCCAF) | `tools/fmea.py` cross-checks `risk/sccaf.csv` |
| Worst-case circuits | Dividers, logic levels, fuses and wires checked at tolerance limits | `tools/wcca.py` in CI |
| Decision records | Each decision between options gets an ADR with criteria and evidence | `docs/adr/` |
| Definition of done | Each task leaves its requirement, test protocol, analyses, engineering log entry and changelog entry in the same pull request | PR template; `CHANGELOG.md` checked in CI |
| Safety in hardware | The e-stop, float shut-off, fuses and force limit never depend on software | Architecture rule 1; reviewed in every PR |

## Course activities and how each one fed the project

The course *Proyecto Mecatrónico I* (Fall 2026) was organized in activities and three project evaluations. The
table maps each one to the part of this report that contains its result. The course material used as reference was
*01 Methodology for Mechatronics Engineering*, *02 Problem Statement*, *03 Requirements & Components Selection*,
*04 Conceptual Design* and the *Ethical Design Evidence (IEEE 7000-2021)* template.

| Activity | Due date | Result in the project | Report section | Archived file |
|---|---|---|---|---|
| ACT.01 Disruptive thinking | 20 Aug 2026 | Core idea: a robot that cleans and separates oil and chips at shift changes | 1.1, 1.5 | — |
| ACT.02 Setup the team | 27 Aug 2026 | Team of seven, roles, collaboration tools (GitHub, shared drive) | 18.2 | — |
| ACT.03 Technological benchmark | 3 Sep 2026 | Commercial scrubbers and patent prior art | 1.3 | — |
| PROJECT.01 First partial evaluation | 14 Sep 2026 | First proposal (motivation, problem, hypothesis, objective) | 2.4 | — |
| ACT.04 Design analysis | 2 Oct 2026 | Requirements, quality matrix, pairwise comparison, SWOT, goal tree | Ch. 3 | `Pairwise_Comparison_Corrected.xlsx` |
| ACT.05 Conceptual design | 8 Oct 2026 | Black box, UI selection, white boxes, morphological matrix, priced BOM | Ch. 5 · App. B | `Conceptual_Design_Waste_Robot.pptx` |
| Design of models (in-class) | Oct 2026 | Nine modules, layout, interfaces, flows, power and control architecture | Ch. 6 | `Design_of_Models_Waste_Robot.pptx` |
| Scenario analysis (in-class) | Oct 2026 | Idealist/pessimist scenarios, protection terms, metrics, evaluation | Ch. 8 | `Scenario_Analysis_Waste_Robot.pdf` |
| PROJECT.02 Second partial evaluation | 23 Oct 2026 | Improved proposal: revised proposal, design analysis, theoretical framework (39 references), conceptual design, calendar, one-pager | Ch. 1–5 | `Improved_Proposal_Waste_Robot.pdf` |
| Standards table (in-class) | Oct 2026 | ISO 3691-4 and NOM-001-STPS-2008 in the course table format | Ch. 10 | `Standards_Table_Waste_Robot.pdf` |
| RA1000 ACT.06 Technological impact analysis | 30 Oct 2026 | Economic, social, cultural, safety-health, ethical and global impact | Ch. 14 | `Activity06_Technological_Impact.pdf` |
| Suction pre-test (team initiative) | 24–25 Nov 2026 | TP-S01 measured; ADR-0008 low-dose degreaser; TP-S02 rig protocol; presentation v4 | 12.8, 13.3 | `docs/test-reports/TP-S01-…`, `Final_Presentation_Waste_Robot_v4.pdf` |
| Ethical Design Evidence (IEEE 7000-2021) | Nov 2026 | Ethical value requirements EVR-01–EVR-03, stakeholders, value conflict | 3.4 | Presentation v2–v4 |
| PROJECT.03 Final evaluation | 27 Nov 2026 | This technical report + final presentation + team evaluation | All | `docs/final-report/`, `Final_Presentation_Waste_Robot_v4.pdf` |

All archived files are in `docs/semester-1-deliverables/` of the repository, in English (the Spanish originals of
the standards table and the pairwise workbook were translated with the same content, formulas and layout).

## Evolution of the proposal

The proposal went through six drafts of the team brief and one improved proposal. The corrections are part of the
learning, so they are recorded here.

### Corrections made to the first-evaluation proposal

| # | Item in the first draft | Correction in the improved proposal |
|---|---|---|
| 1 | Cover listed six team members | All seven members are listed (Juan Manuel Vásquez Paniagua added) |
| 2 | Same-level-fall statistics (> 400,000 cases, 145 deaths) did not match the current data on the cited page | Figures re-checked against the cited sources: 264,920 days-away cases (2023–2024) and 134 deaths (2024) from NSC/BLS; Liberty Mutual manufacturing figures confirmed |
| 3 | Absolute claim that no existing system combines floor cleaning and waste separation | Replaced by a bounded statement: no such integration was found in the literature and patents reviewed |
| 4 | Hypothesis was qualitative and promised a "slip-free" floor and reusable waste streams | Hypothesis is testable against three metrics with pass thresholds (M1–M3); reuse and floor safety are expected benefits to validate |
| 5 | Navigation by SLAM or by fixed floor markings | Floor markings removed (oil fouls them); localization uses encoders, IMU and 2D LiDAR |
| 6 | "Magnetic decantation trap" with no solids handling | Separation chain defined: mesh basket → neodymium magnets → chip basket with force-limited linear-actuator compactor (requirement R3) |
| 7 | Only a general objective | Six specific objectives (OE1–OE6) with indicators and linked requirements |
| 8 | Benefits stated as certain outcomes | Benefits stated as expected results that the prototype tests must confirm |
| 9 | Mixed reference format | Single IEEE format; review articles distinguished from primary studies |

### Revision record of the team brief

| Draft | Date | Change |
|---|---|---|
| 2 | 24 Sep 2026 | Incorporated ten requirements and importance values; retained the 47 candidate IDs and weighted-selection results; specified Arduino UNO Q; documented both evaluation methods; replaced absolute performance and novelty assertions with testable objectives |
| 3 | 24 Sep 2026 | Replaced the active inventory with the 22 components supplied by the team; retained the conditional camera and a consolidated e-stop entry; marked requirement-coverage gaps |
| 4 | 24 Sep 2026 | Synchronized the brief and pairwise spreadsheet to the 22-component list; updated formulas, dropdowns and result ranges to 231 pairs |
| 5 | 25 Sep 2026 | Proposed a 33-item inventory from the 47-component weighted matrix (33 keep, 6 integrate, 8 discard); restored compaction, magnetic separation, overflow, leak, relay e-stop, IMU, bumper, LED lighting and RFID; removed water/steam outlets and the auxiliary-product container; recorded the corrected pairwise workbook (rank correlation 0.26 → 0.83) |
| 6 | 9 Oct 2026 | Added the seventh member; specific objectives OE1–OE6; conceptual design (black box, UI components, white boxes, morphological matrix, priced list: 32 items, MXN 15,849.50); drive and battery choices |
| Improved proposal | 23 Oct 2026 | Full rewrite for the second evaluation (corrections above), theoretical framework and weekly calendar |
| Repository | 21 Nov 2026 | All deliverables consolidated into one repository with requirements, risk registers, checks and decision records (v0.1.0) |
| Presentation v2/v3 | 22–24 Nov 2026 | Ten-slide final deck with IEEE 7000 EVRs, then the Business Model Canvas slide (v0.2.0, v0.2.1) |
| TP-S01 + ADR-0008 | 24–25 Nov 2026 | First physical pre-test; low-dose degreaser adopted; SR-022–SR-025, DFMEA F-010–F-014, PFMEA, SCCAF SC-008–SC-011, economics updated; presentation v4 with the test slide |

## Tools used by the team

| Tool | Use |
|---|---|
| Google Sheets / Excel | Weighted quality matrix (47 components), pairwise comparison (231 pairs), timeline and costs |
| PowerPoint / PDF | Course deliverables and presentations |
| GitHub | Single repository, pull requests, CI checks, releases, issues |
| Python 3.11 | Checkers and calculators (`tools/`), AprilTag bench app, simulations |
| OpenSCAD | Parametric CAD (text-based, diff-able in Git, renders in CI) |
| Arduino App Lab | Runs the Python + MCU sketch app on the Arduino UNO Q |
| Claude / Claude Code (Anthropic) | AI assistant for drafting, translation and repository setup, under the team's direction and review (Appendix F) |
