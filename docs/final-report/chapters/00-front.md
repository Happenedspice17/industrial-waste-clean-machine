# Read this first: the project repository {.unnumbered}

<div class="gh-box">
<div class="lbl">Project repository on GitHub · public link</div>
<div class="url"><a href="https://github.com/Happenedspice17/industrial-waste-clean-machine">github.com/Happenedspice17/industrial-waste-clean-machine</a></div>
<div class="row">
<img src="img/repo_qr.png" alt="QR code to the repository">
<div>

**This report is generated from the repository, and the repository is the project.** Every number, requirement,
risk, calculation and decision in these pages has a file behind it that you can open, run and check. The report is a
snapshot (branch `develop`, 27 November 2026: release **v0.2.1** plus the first suction pre-test TP-S01, the
degreaser decision ADR-0008 and this report); the repository is the living version.

<span class="badge">CI</span> Every change passes automatic checks: requirement traceability, DFMEA + SCCAF, worst-case
circuit analysis, lint and unit tests.
<span class="badge">MIT</span> Open-source license.

</div>
</div>
</div>

## What you will find there {.unnumbered}

| Folder / file | What it contains | Report chapter |
|---|---|---|
| `README.md` | Project showcase: problem, how it works, architecture, status, roadmap | 1, 6, 13 |
| `docs/00-project-context.md` | Single source of truth for every project fact (requirements, modules, BOM, interfaces, metrics, scenarios, economics) | All |
| `docs/01-lessons-learned.md` | 21 lessons from the team's previous Arduino UNO Q robot | 17 |
| `docs/02-architecture.md` | MCU/Linux split, Bridge RPC protocol, states, sensor hierarchy, safety chain | 6 |
| `docs/03-standards-matrix.md` | ISO 3691-4, NOM-001-STPS-2008 and other standards with clauses and evidence | 10 |
| `docs/04-business.md` · `docs/05-sustainability-sdg.md` | Business Model Canvas, economics, SDG mapping | 14–16 |
| `docs/08-sccaf.md` | Internal SCCAF (special characteristics YC/YS → CC/SC) | 9 |
| `docs/adr/` | Eight Architecture Decision Records | 12 |
| `docs/test-reports/` | First physical pre-test TP-S01 (measured 24 Nov 2026, with photos and the operator log) and protocols TP-S02, TP-V01, TP-V02 with pass criteria fixed before testing | 13 |
| `docs/security/threat-model.md` | STRIDE threat model of the camera app, web page, log and Bridge | 9 |
| `docs/semester-1-deliverables/` | Every course deliverable: proposal, conceptual design, models, scenarios, impact, standards, presentations | 2 |
| `requirements/requirements.yaml` | 10 stakeholder requirements → 25 system requirements, with verification and acceptance | 3, App. C |
| `risk/` | DFMEA, PFMEA, SCCAF register, WCCA inputs, DFMA worksheets | 9 |
| `tools/` | Python checkers and calculators: traceability, FMEA, WCCA, DFMA, economics, git policy | 7, 9, 11 |
| `linux/apriltag_pose/` | AprilTag bench-localization app for the UNO Q (Python + MCU sketch) | 11 |
| `cad/` | Parametric OpenSCAD parts | 11 |
| `docs/final-report/` | **Source files of this report** (Markdown + CSS + build script) | — |

## How to use it in five minutes {.unnumbered}

```bash
# 1. Get the code (needs Git and Python 3.11 or newer)
git clone https://github.com/Happenedspice17/industrial-waste-clean-machine.git
cd industrial-waste-clean-machine

# 2. Create an isolated Python environment and install the tools
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# 3. Run every check the CI runs (traceability, DFMEA/SCCAF, WCCA, lint, tests)
python tools/check_all.py

# 4. Reproduce the numbers of this report
python tools/fmea.py risk/dfmea.csv                  # risk ranking (RPN) and YC/YS classes  → Chapter 9
python tools/wcca.py risk/wcca.yaml                  # worst-case circuits and runtime        → Chapter 9
python tools/dfma.py risk/dfma/m4_separation_example.csv   # design efficiency                → Chapter 9
python tools/econ.py                                 # payback, NPV, scenarios, tornado       → Chapter 14
```

No Git? Open the link above, press the green **Code** button and choose **Download ZIP**. Every Markdown file is
readable directly in the browser. The complete guide (cloning, the tools, the AprilTag app on the UNO Q, the
contribution workflow and how to rebuild this report) is in **Appendix A**.

# Abstract {.unnumbered}

Machining shops, foundries and metal-forming lines accumulate lubricant, coolant and metal chips on their floors.
Cleaning during production is unsafe, so the contamination stays on walkways until a stoppage; the people who clean
it handle metalworking fluids and sharp chips, and the waste ends up mixed into one hazardous stream with no recycling
value. Same-level falls are the second most costly cause of serious injury in U.S. manufacturing (USD 1.20 billion a
year), and Mexico recorded 290,527 work accidents in 2023. Commercial autonomous scrubbers cost about MXN 2 million,
clean with water and do not separate waste; in the literature and five patents reviewed, no system combines autonomous
floor collection with on-board separation of the liquid and ferrous fractions into independent containers.

This report documents the first semester of a capstone project that answers that gap: a compact
(≈ 700 × 500 × 450 mm), differential-drive, oil-compatible autonomous robot that works in a cleared area during shift
changes. A low-dose, low-foam degreaser spray wets the strip, a rotary brush and squeegee feed a nozzle, and a 12 V wet/dry vacuum draws the mixture into a sealed separation
chamber where a stainless mesh basket retains coarse solids, neodymium magnets capture the ferrous chips and a
force-limited linear actuator compacts and drains them; the liquid flows by gravity into a separate 20 L tank. An
Arduino UNO Q splits the work by timing requirement: its STM32U585 microcontroller executes every motion order and
stops by itself, while its Qualcomm QRB2210 Linux processor plans, localizes with LiDAR, IMU and encoders, logs and
serves the operator interface. The emergency stop cuts every actuator through a relay in hardware.

The design was developed with the VDI 2206 V-model and systematic-design tools: ten weighted stakeholder requirements,
a quality matrix and a pairwise comparison (rank agreement raised from 0.26 to 0.83 after correction), a goal tree,
SWOT, black and white boxes, an 18-function morphological matrix, nine modules with 13 interfaces and a priced bill of
materials (MXN 15,849.50 listed; ≈ MXN 20,160 with tooling and contingency, ≈ MXN 21,310 with the dosing system). Ethical value requirements were added
following IEEE 7000-2021. The engineering record includes 25 system requirements with acceptance criteria, a DFMEA
with 14 failure modes, a PFMEA, an internal SCCAF with 11 special characteristics, a worst-case circuit analysis, a DFMA
review, a STRIDE threat model, eight architecture decision records, one test report and three test protocols, all checked automatically
in a public GitHub repository. A coverage simulation of a 12 × 8 m cell gives 96 % coverage in 25.6 min (167 m²/h),
inside a 30-minute shift change. The economic evaluation of the dry concept (Activity 06) gives a 6.6-month payback;
with the degreaser the base case becomes 8.4 months and the pessimistic case turns negative, so the dose must be
measured. A bench localization app with AprilTags runs on the UNO Q.

**No prototype exists yet.** The only physical evidence is an exploratory suction pre-test (TP-S01, measured
24 November 2026, handheld vacuum, no brush): dry suction removed nothing visible and lifted 0 of 5 heavy coins; with
a degreaser about 85–90 % of the film came off (visual estimate) and 30 % of the coin mass was lifted. This led the
team to adopt a low-dose degreaser ahead of the brush (ADR-0008). Every other performance figure is labeled as an
estimate, a calculation or a simulation. The design is not frozen: the first gate of the next semester is the suction
rig with brush, degreaser and a wet trap (TP-S02), which decides whether the vacuum carries the chips (option A) or the
chips go to a front hopper (option B).

**Keywords:** autonomous mobile robot, industrial cleaning, waste segregation, magnetic separation, metalworking
fluids, coverage path planning, Arduino UNO Q, functional safety, ISO 3691-4, NOM-001-STPS-2008, IEEE 7000.

## Key numbers {.unnumbered}

<div class="tiles">
<div class="tile"><div class="n">10 R → 25 SR</div><div class="d">stakeholder → system requirements, traced in CI</div></div>
<div class="tile"><div class="n">9 modules</div><div class="d">13 interfaces · 32 priced components</div></div>
<div class="tile"><div class="n">MXN 15,849.50</div><div class="d">listed BOM · ≈ 20,160 with tooling + 15 % contingency</div></div>
<div class="tile"><div class="n">0.38 m/s</div><div class="d">top speed (0.15 m/s cleaning) · calculation</div></div>
<div class="tile"><div class="n">≤ 7.4 cm</div><div class="d">braking on oil from 0.38 m/s (μ = 0.1) · calculation</div></div>
<div class="tile"><div class="n">≈ 52 min</div><div class="d">runtime per charge (144 Wh / 165 W with dosing) · estimate</div></div>
<div class="tile"><div class="n">96 % · 25.6 min</div><div class="d">coverage of a 12 × 8 m cell · simulation</div></div>
<div class="tile"><div class="n">167 m²/h</div><div class="d">coverage rate vs. ≥ 100 target · simulation</div></div>
<div class="tile"><div class="n">8.4 months</div><div class="d">payback with degreaser (NPV MXN 79,529) · 6.6 months dry concept · estimate</div></div>
<div class="tile"><div class="n">0 % → 85–90 %</div><div class="d">film removed: dry suction vs with degreaser · measured 24 Nov 2026 (TP-S01, visual)</div></div>
<div class="tile"><div class="n">2 of 5 coins</div><div class="d">30 % of the "chip" mass lifted with degreaser, no brush · measured (TP-S01)</div></div>
<div class="tile"><div class="n">≈ 20 mL/m²</div><div class="d">degreaser dose (ADR-0008) · estimate, set by TP-S02</div></div>
</div>

## Evidence labels used in this report {.unnumbered}

Rule 4 of the project: no claim without evidence. Every number carries one of these labels.

| Label | Meaning |
|---|---|
| **Calculation** | Derived from a formula with stated inputs (shown in the text) |
| **Estimate** | Engineering judgment or assumption, to be replaced by a measurement |
| **Simulation** | Result of a computer model; never presented as a physical test |
| **Measured (date, conditions)** | Physical measurement on real hardware |
| **(deduced)** | Inference by the authors not written in a source, code or commit |

