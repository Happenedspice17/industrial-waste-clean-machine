# Threat model — AprilTag bench localization app (rev 1, 2026-11-22)

Owner: project team · reviewer: Claude Code (AI, 2026-11-22) · related SR-017–SR-021, ADR-0007, TP-V02.
Scope: `linux/apriltag_pose/` running in Arduino App Lab on the UNO Q (Linux side), its web page on port 7000, its log
and the Bridge pose message to the MCU sketch. Method: STRIDE per data flow; risk = impact (1–5) × likelihood (1–5).

## Assets
| Asset | Why it matters (safety, privacy, availability, integrity) |
|---|---|
| Camera frames | Privacy: plant staff can be in view |
| Pose estimate | Integrity: a wrong pose could mislead tests or, later, navigation |
| Mount / tag configuration | Integrity: changes every pose |
| `run.jsonl` log | Evidence for tests (integrity); holds poses and timings, no images |
| Board availability | The same Linux side will run navigation later |

## Data flows and trust boundaries
| Flow | From → To | Channel | Crosses boundary? |
|---|---|---|---|
| Camera frames | USB camera → app (Linux) | USB / V4L2 | Yes (physical device) |
| Page, pose JSON, log | App → any browser on the network | HTTP, port 7000, no auth, no TLS | Yes |
| Calibration commands | Browser → app (`POST /calibrate`, `/calibrate/apply`) | HTTP, no auth | Yes |
| Validated pose | App → MCU sketch | Bridge RPC `pose` | Yes (Linux not trusted for safety) |
| Printed tags | Environment → camera | Optical | Yes |

## Threats
| ID | Flow | STRIDE | Attack scenario | Impact | Likelihood | Risk | Control | SR | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| T-01 | Camera frames | I | Anyone on the network opens `/frame.jpg` and sees people at the machines | 4 | 3 | 12 | `STREAM = False` default: no frame kept, `/frame.jpg` → 404; no images on disk | SR-020 | team | mitigated (sim-tested) |
| T-02 | Page / log | I | Anyone on the network downloads `run.jsonl` (poses, timings, camera info) | 2 | 3 | 6 | No personal data in the log; lab network only | SR-020 | team | accepted (bench) |
| T-03 | Calibration | T | A LAN user presses **Apply** with bad values; poses become wrong or vanish | 3 | 2 | 6 | Session-only (restart restores committed values); applied values logged (`calib_apply`); pose sent to MCU is print-only | SR-021 | team | open until auth |
| T-04 | Page / log | D | Request flood or repeated 20 MB log downloads slow the board | 2 | 2 | 4 | Log rotates at 20 MB; lab network only | — | team | accepted (bench) |
| T-05 | Printed tags | S | Someone places a fake tag with a known ID; pose jumps | 2 | 2 | 4 | `tags_disagree` and `reproj` checks refuse inconsistent views; LiDAR stays the authority (ADR-0007) | SR-018 | team | mitigated |
| T-06 | Validated pose | E | Pose messages used later to drive motion without validation | 5 | 1 | 5 | SR-017 log-only gate; MCU sketch only prints; TEST estimates never sent | SR-017, SR-019 | team | mitigated (inspection) |

## Residual risks and accepted limits
- No authentication or TLS on port 7000: accepted only on an isolated lab network. **Before any use on the plant
  network or with motion enabled:** add a token on every request (or disable the page), require it for POST, and
  serve over TLS (new SR to be written then).
- Turning `STREAM = True` for debugging exposes T-01 again; set it back to `False` before committing.

## Verification
TP-V02 parts C, D, E, F. Simulation results in the report; physical run pending.
