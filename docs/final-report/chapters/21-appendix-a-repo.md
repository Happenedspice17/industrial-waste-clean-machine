# Appendix A · How to use the GitHub repository {.unnumbered}

<div class="gh-box">
<div class="lbl">Repository</div>
<div class="url"><a href="https://github.com/Happenedspice17/industrial-waste-clean-machine">github.com/Happenedspice17/industrial-waste-clean-machine</a></div>
<div class="row">
<img src="img/repo_qr.png" alt="QR code to the repository">
<div>

Public · MIT license · default branch `main` (releases); `develop` is the integration branch · current release **v0.2.1**.
Scan the QR code or open the link. This appendix explains, step by step, how to read the project, run every check
and calculator, run the AprilTag app on the Arduino UNO Q, contribute a change and rebuild this report.

</div>
</div>
</div>

## A.1 Read it in the browser (no installation)

1. Open the link. The landing page shows `README.md`: problem, how it works, architecture diagrams, status, risks,
   decisions, simulations and roadmap.
2. Start with `docs/00-project-context.md` (all project facts in one file), then `docs/02-architecture.md`.
3. Requirements: `requirements/requirements.yaml`. Risks: `risk/dfmea.csv` and `risk/sccaf.csv` (GitHub shows CSV
   files as searchable tables).
4. Decisions: `docs/adr/`. Tests: `docs/test-reports/`. Course deliverables: `docs/semester-1-deliverables/`.
5. History: the **Commits** link shows every change with its message; `CHANGELOG.md` lists the releases v0.1.0,
   v0.2.0 and v0.2.1 (each merged to `main` through a `release/vX.Y.Z` branch); **Pull requests → Closed** shows each
   change with its validation; **Actions** shows the CI runs.
6. To download everything without Git: green **Code** button → **Download ZIP**.

## A.2 Install and run the checks (Windows, macOS or Linux)

Requirements: Git, Python 3.11 or newer.

```bash
git clone https://github.com/Happenedspice17/industrial-waste-clean-machine.git
cd industrial-waste-clean-machine
python -m venv .venv
source .venv/bin/activate              # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"                # installs ruff, pytest, pyyaml and the project tools
pre-commit install --hook-type pre-commit --hook-type commit-msg   # optional: local guards
python tools/check_all.py              # branch, traceability, DFMEA/SCCAF, WCCA, ruff, pytest
```

`check_all.py` prints one line per check and exits with an error if any fails. On a fresh clone, the branch check
may complain if you are on `main`/`develop` and about to commit: create a work branch first (A.5).

## A.3 Reproduce the numbers in this report

| Command | Output | Report |
|---|---|---|
| `python tools/fmea.py risk/dfmea.csv` | RPN ranking, mandatory actions (S ≥ 9), YC/YS classes checked against the SCCAF register | 9.1–9.3 |
| `python tools/wcca.py risk/wcca.yaml` | Divider worst case (EVA + RSS), logic-level margins, fuse vs wire per branch, runtime | 7.9 |
| `python tools/dfma.py risk/dfma/m4_separation_example.csv` | Parts, theoretical minimum, assembly time, design efficiency | 9.5 |
| `python tools/econ.py` | Activity 06 (dry) and degreaser base, optimistic, pessimistic: net benefit, payback, NPV; tornado | 14.2–14.3 |
| `python tools/check_traceability.py` | Checks R → SR → test links in `requirements.yaml` | 3.3 |
| `pytest -q` | Unit tests for the tools (and the AprilTag app if OpenCV is installed) | 11 |

To try a "what if", edit the input file (for example a fuse value in `risk/wcca.yaml`, a severity in
`risk/dfmea.csv` or a parameter in `tools/econ.py`) and run the tool again.

Expected output of the tools on `develop` (27 Nov 2026, after ADR-0008):

```text
$ python tools/fmea.py risk/dfmea.csv
ID         RPN   S  class flag
F-005      108   9  YC    MANDATORY (S>=9)
F-002       81   9  YC    MANDATORY (S>=9)
F-006       81   9  YC    MANDATORY (S>=9)
F-003       80  10  YC    MANDATORY (S>=9)
F-001      168   7  YS    
F-004      160   8  YS    
F-010      160   8  YS    
F-011      160   8  YS    
F-013      140   7  YS    
F-008      100   5  YS    
F-007       96   4        
F-012       63   7        
F-009       54   6        
F-014       45   3

$ python tools/wcca.py risk/wcca.yaml
divider battery_sense: Vout 2.057..2.973 V (nom 2.548, RSS max 2.959) limit 3.1 V margin 4.1 % WARN
logic bumper_switch_to_mcu: high margin 0.89 V, low margin 0.89 V OK
logic hx711_dout_to_mcu: high margin 0.59 V, low margin 0.59 V OK
branch drive: nom 3.0 A peak 12.0 A fuse 15 A wire 14 AWG (ampacity 15 A) OK
branch collection: nom 10.0 A peak 25.0 A fuse 20 A wire 12 AWG (ampacity 20 A) OK
branch separation: nom 2.0 A peak 8.0 A fuse 10 A wire 16 AWG (ampacity 10 A) OK
branch logic: nom 1.5 A peak 3.0 A fuse 5 A wire 18 AWG (ampacity 7 A) OK
branch dosing_pump: nom 0.7 A peak 2.0 A fuse 3 A wire 18 AWG (ampacity 7 A) OK
runtime: 52 min at 165 W

$ python tools/dfma.py risk/dfma/m4_separation_example.csv
parts 27, theoretical minimum 6, assembly time 159.3 s, design efficiency 11.3 %

$ python tools/econ.py
activity06   net     56,968/yr  invest    31,560  payback   6.6 mo  NPV    105,269
base         net     46,731/yr  invest    32,710  payback   8.4 mo  NPV     79,529
optimistic   net     56,241/yr  invest    32,710  payback   7.0 mo  NPV    102,371
pessimistic  net     15,879/yr  invest    49,065  payback  37.1 mo  NPV    -10,926
tornado (NPV delta low/high):
  hours_saved_day       -45,684     22,842
  solution_l_m2         -24,575     12,287
  disposal_mxn_kg       -11,889     11,889
  hardware              -10,655      6,393
  scrap_mxn_kg           -4,621      4,621
```

## A.4 Run the AprilTag bench app on the Arduino UNO Q

1. Install **Arduino App Lab** on a computer and connect the UNO Q (or open App Lab on the board itself).
2. Copy the folder `linux/apriltag_pose/` into App Lab as an app (it contains `app.yaml`, `python/` and `sketch/`).
3. Plug a USB camera into the UNO Q through a **powered** USB-C hub (when the board is powered from VIN, its USB-C
   port gives no 5 V to the hub).
4. Print tag36h11 tags (IDs used in `TAGS` in `python/main.py`), measure the black square with a caliper and write it
   to `TAG_SIZE`; tape-measure each tag's position and facing direction into `TAGS`.
5. Press **Run**. The Python side probes the camera modes and starts the web page; the MCU sketch prints validated
   poses on the App Lab serial Monitor.
6. On a phone or laptop on the same (isolated) network, open `http://<board-ip>:7000`. The page shows the map, the
   pose (**OK**, **TEST ESTIMATE** or **NO POSE** with the reason) and the **Calibrate mount** button.
7. Logs: `python/logs/run.jsonl` (no images). Open it from the page (**log** link) or press **download**, then replay it offline.
8. Unit tests on a computer: `pytest -q linux/apriltag_pose/python/test_pose.py` (needs OpenCV).

**Warnings.** The page has no authentication: use it only on an isolated lab network (threat model T-03, T-04). Do not
commit `STREAM = True` (privacy, SR-020). The camera intrinsics `K_CAL` are a placeholder until calibrated (TP-V02).

## A.5 Contribute a change (team workflow)

1. **Requirement first.** If the change adds behavior, add or edit an `SR-xxx` in `requirements/requirements.yaml`
   (parent, module, verification, acceptance).
2. **Branch** from `develop`: `git switch develop && git pull && git switch -c feature/12-suction-rig-logger`
   (types: feature, fix, hw, cad, docs, test, sim, refactor, chore, exp).
3. **Make the change and its evidence in the same branch** (definition of done): test protocol/report, DFMEA rows,
   SCCAF entry for YC/YS rows, WCCA for wiring, DFMA for parts, ISO/NOM check for safety functions, security review
   for camera/web/RPC/RFID/logs, ADR for decisions, engineering log entry, and a `CHANGELOG.md` entry; or "N/A:
   reason" in the PR.
4. **Run** `python tools/check_all.py`.
5. **Commit** with a Conventional Commit message: `feat(m3): log suction pressure at 20 Hz` with `Refs: SR-001` in
   the body.
6. **Push and open a pull request** to `develop`. CI runs `policy` (names, PR body, changelog) and `python` (lint,
   tests, traceability, FMEA, WCCA); `firmware` and `cad` jobs run when those folders change.
7. **Merge** when CI is green and a teammate has reviewed. Releases: `develop` → `release/vX.Y.Z` → `main`.

Never commit directly to `main` or `develop`, never force-push, never use `--no-verify`.

## A.6 Render a CAD part

Install OpenSCAD, then: `bash cad/tools/render.sh cad/parts/wheel_hub_hex.scad` → STL in `cad/out/`. Parameter sets
live in `cad/params/wheel_hub_hex.json`. Measure the real shaft and wheel before printing (values are still
placeholders).

## A.7 Rebuild this report

The report sources are in `docs/final-report/`: one Markdown file per chapter in `chapters/`, the cover in
`cover.html`, styles in `style.css`, figures in `img/`, and `build.sh`. Appendices C, D and E are generated from the
repository files by `gen_appendices.py`, so they never drift from the source of truth.

```bash
cd docs/final-report
./build.sh          # needs pandoc ≥ 3, Node.js with Playwright (Chromium) and Python 3
# → report.html, report.pdf (A4, page numbers), report.docx (editable)
```

## A.8 Where to ask

Open an **issue** in the repository (templates: bug, requirement, risk) or contact the team. The repository owner is
`Happenedspice17`; team members contribute through pull requests.
