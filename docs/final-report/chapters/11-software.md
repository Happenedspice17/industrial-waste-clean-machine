# Software, tools and repository engineering

The repository is not only storage: it enforces the engineering method. This chapter describes the software that
exists today and the automation around it. Robot firmware starts after the suction gate (ADR-0004); what runs today
is a bench tool and the engineering checkers.

## AprilTag bench localization app (`linux/apriltag_pose/`)

**Why.** The team wanted to test pose estimation now, with one USB camera on the UNO Q and printed AprilTags, before
the LiDAR stack exists (ADR-0007). It is a **bench test tool only**: LiDAR + encoders + IMU remain the localization
authority, and the MCU sketch only prints the poses it receives.

| File | What it does |
|---|---|
| `app.yaml` | Arduino App Lab manifest (web UI brick) |
| `python/main.py` (628 lines) | Camera-mode probe (largest image with ≥ 40 fps), `cv2.aruco` detection with sub-pixel corners, planar solver, ambiguity refusal, Bridge `pose` message |
| `python/web.py` (281 lines) | Page on port 7000: map, pose, test estimate, mount calibration; camera stream **off** by default (`STREAM = False`) |
| `python/logbook.py` | `run.jsonl`: frame records (≈ 30 Hz), decision reasons, camera connect/disconnect — no images; rotates at 20 MB |
| `python/test_pose.py` | Unit tests: Jacobian, one-tag pose, unknown ID, wrong map, mount calibration, privacy (7 tests) |
| `sketch/sketch.ino` | MCU side (STM32): receives `pose(x, y, yaw, n)` over the Bridge and prints it every 500 ms; prints "pose STALE" if nothing arrived for 1 s |

### Pipeline

1. **Camera probe at start.** Each candidate mode is opened and measured over 30 frames; the app picks the largest
   image that delivers ≥ 40 fps (640 × 480 MJPG ≈ 45 fps on the bench camera). Exposure is set from the delivered
   rate. `/dev/video0–1` are internal on the UNO Q, so only existing `/dev/video*` from index 2 are probed, and a
   background grabber re-finds the camera on unplug.
2. **Detection.** OpenCV ArUco with the `DICT_APRILTAG_36h11` dictionary [72] and sub-pixel corner refinement.
   `pupil_apriltags` was rejected because its import failed on the board's App Lab image.
3. **Seeds.** IPPE square solutions per tag [67] are used only as starting points.
4. **Planar solve.** Gauss–Newton with an analytic Jacobian over all corners of all known tags (equation 4), with
   camera height `CAM_Z` and pitch `CAM_PITCH` fixed, so only (x, y, yaw) are estimated.
5. **Refusals instead of wrong poses.** The app publishes **no pose** and logs the reason when: no markers, unknown
   IDs, tag beyond 4 m (`too_far`), per-tag camera positions more than 0.5 m apart (`tags_disagree`, a map error,
   never averaged), reprojection error above 2 px (`reproj`), or two distinct solutions fit and no pose younger than
   1 s exists to choose between them (`ambiguous_no_prior`).
6. **Outputs.** Validated poses go to the MCU over the Bridge (≤ 50 messages/s); every frame decision goes to the log
   (≥ 20 records/s, plus every change of reason); the web page shows the map and numbers. Test-mode single-tag
   estimates are shown on the page and logged but never sent to the MCU.
7. **Mount calibration.** A button collects ≥ 20 single-tag views in 2 s, measures camera height and pitch and applies
   them to the running session only (restart restores the committed values, threat model T-03).

### Results so far (TP-V02)

| Evidence | Result |
|---|---|
| Unit tests (simulation) | 7 passed |
| Simulation, 0.20 m tags, planar solver v2, camera pitched 7° | Position p50 / p90 = 0.024 / 0.091 m; yaw p50 / p90 = 0.7 / 2.2° (101 of 300 random poses saw a tag) |
| Simulation, same, camera level | 0.020 / 0.112 m; 0.5 / 2.7° — **borderline** vs the 0.10 m target |
| Bench, UNO Q, 22 Nov 2026 (desk setup, untaped poses) | Camera modes: 320 × 240 MJPG 66.9 fps … 640 × 480 MJPG 45.2 fps (startup probe, 30 frames each); processing ≈ 5 ms/frame without tags, 15–30 ms with tags |
| Bench, same session | Every planar solve failed (`reproj` 75–81 px): single-tag fit put the camera at 0.39–0.41 m and 0–1.3° pitch vs configured 0.51 m / 6.5°; two tags disagreed by 0.15–0.21 m → the `TAGS` map entry did not match the real tag |

The bench log diagnosed the failure: the configured mount height and pitch were guesses (rule 5 broken), and one tag
position was wrong. Actions: `CAM_Z = 0.40`, `CAM_PITCH = 0.5` (deduced from the log) and the mount-calibration button.
The app has not been re-run on the board since these changes; the committed camera intrinsics `K_CAL` (fx = fy = 600
px) are still a placeholder. **SR-018–SR-021 stay draft until the physical test passes.**

## Engineering checkers and calculators (`tools/`)

Plain Python, no network. `python tools/check_all.py` runs every blocking check, locally and in CI.

| Script | What it does |
|---|---|
| `check_all.py` | Branch name, traceability, DFMEA, WCCA, ruff lint + format, pytest |
| `check_branch.py` | Branch name follows `CONTRIBUTING.md` (`<type>/<issue>-<desc>`, `claude/…`, `release/…`) |
| `check_commit_msg.py` | Conventional Commit message or PR title (`type(scope): subject`) [74] |
| `check_traceability.py` | `requirements.yaml` structure and R → SR → test links |
| `fmea.py` | DFMEA/PFMEA ranking (RPN), mandatory actions for S ≥ 9, YC/YS classes vs the SCCAF register |
| `wcca.py` | Worst-case dividers (EVA + RSS), logic levels, fuse/wire per branch, runtime |
| `dfma.py` | Design efficiency DE = 3 · N_min / Σ assembly time |
| `econ.py` | Economics of one robot: net benefit, payback, NPV, scenarios and tornado sensitivity |

Unit tests for the tools live in `tests/test_tools.py`; app tests live next to their code (`linux/**/test_*.py`).
At the last release, `pytest` ran 24 passed and 1 skipped (OpenCV not installed in CI).

## Parametric CAD (`cad/`)

OpenSCAD was chosen because it is text-based (diff-able in Git), fully parametric, light on CPU and renders headless
in CI. Structure: `lib/common.scad` (hex prism, D-bore, holes, captive nuts), `parts/<part>.scad` (one part per file,
parameters at the top), `params/<part>.json` (customizer parameter sets) and `tools/render.sh` (headless render to
STL). Rules: measure real parts first and record value, date and instrument; PETG for anything in the oil path;
n ≥ 2 (n ≥ 3 at bump mounts). First part: `wheel_hub_hex` (M2), which adapts the JGB37-3530 D-shaft to the Talon
12 mm hex wheel — **draft; shaft and wheel dimensions still to measure.** Most CAD waits for the suction decision.

## Simulation (`sim/`)

| Folder | Purpose | Status |
|---|---|---|
| `coverage/` | Boustrophedon coverage of a plant cell | Semester-1 result (96 %, 25.6 min, 167 m²/h, 68 Wh) — code to be ported here |
| `sensors/` | Noisy sensor models: LiDAR dropouts on reflective metal, float bounce, pressure noise, RPC delay, clock jumps | Planned — must reproduce failures seen in field logs |
| `replay/` | Run a field log through the decision code as a regression test | Planned |

## Continuous integration and repository rules

| Workflow | Job | Blocks merge |
|---|---|---|
| `branch-policy.yml` | Branch name, PR title (Conventional Commit), PR body has requirement refs + test evidence, PR changes `CHANGELOG.md` | Yes |
| `ci.yml` (`python`) | ruff, pytest, traceability check, FMEA/WCCA sanity | Yes |
| `ci.yml` (`firmware`) | clang-format + cppcheck when `firmware/**` has C/C++ | Yes |
| `cad.yml` | OpenSCAD render of changed parts to STL artifact | Yes (render must succeed) |

**Branch model.** `main` holds releases (protected); `develop` is the integration branch (protected); work branches
are `<type>/<issue>-<short-desc>` with type in feature, fix, hw, cad, docs, test, sim, refactor, chore, exp. Releases
go through `release/vX.Y.Z`. Commits follow Conventional Commits with a scope per module (`m1`…`m9`, `req`, `docs`,
`ci`, `cad`, `sim`, `fw`, `linux`) and reference requirement IDs (`Refs: SR-012`). Force pushes and `--no-verify` are
blocked by a local hook.

**Releases so far.** v0.1.0 (21 Nov 2026, initial design baseline), v0.2.0 (22 Nov 2026, AprilTag bench app and
final presentation v2), v0.2.1 (24 Nov 2026, presentation v3 with the Business Model Canvas). Full history in
Appendix E.

## AI agents and commands in the repository (`.claude/`)

The repository includes configuration for Claude Code: 13 expert agents (systems architect, requirements engineer,
DFMA/FMEA engineer, WCCA engineer, embedded safety reviewer, ISO compliance, business analyst, CAD, sustainability,
test and simulation, git gatekeeper, docs writer, cybersecurity engineer), 14 slash commands (`/req`, `/fmea`,
`/dfma`, `/wcca`, `/iso`, `/bmc`, `/econ`, `/impact`, `/sdg`, `/cad`, `/review`, `/log`, `/adr`, `/security`) and a
safety hook that blocks commits on protected branches. AI output is treated as a draft that a team member reviews
(Appendix F).
