# Threat model — single camera and AprilTag localization (rev 1, 2026-11-21)

Owner: Team D · related SR-017, SR-018 · ADR-0007 · DFMEA F-010–F-012. Method: STRIDE per data flow; risk = impact
(1–5) × likelihood (1–5).

## Assets
| Asset | Why it matters |
|---|---|
| Robot pose estimate | Integrity: a wrong pose sends the robot along the wrong lane (safety chain still stops it) |
| Tag map JSON | Integrity: defines where every tag is; an edit moves every fix |
| Camera frames | Privacy: workers appear in view |
| Tag logs (JSON lines) | Integrity for TP-V02 evidence; no personal data if frames are not stored |

## Data flows and trust boundaries
| Flow | From → To | Channel | Crosses boundary? |
|---|---|---|---|
| Camera frames | USB camera → `linux/vision` | USB/V4L2 | Yes (physical device, anything in view) |
| Printed tags | Plant walls → camera | Optical | Yes (anyone can print or move a tag) |
| Tag map / camera config | Repo or web UI → `linux/vision` | File | Yes when edited from the web UI (future) |
| Pose fix | `linux/vision` → navigator (Linux) | In-process | No; MCU safety does not consume it |

## Threats
| ID | Flow | STRIDE | Attack scenario | Impact | Likelihood | Risk | Control | SR | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | Printed tags | Spoofing | Someone shows a printed tag with a mapped ID somewhere else | 3 | 2 | 6 | 2-read confirmation against odometry; reprojection gate; MCU stops stay independent; log-only until TP-V02 (L3 tests it) | SR-018, SR-017 | Team D | open |
| T2 | Printed tags | Tampering | A tag is moved or rotated (cleaning crew, forklift) | 3 | 3 | 9 | Same gates; re-survey after layout changes; replay logs flag growing disagreement with LiDAR | SR-018 | Team D | open |
| T3 | Tag map | Tampering | Map edited with wrong coordinates | 3 | 2 | 6 | Map in git with review; loader validates family, unique IDs, size range; web UI editing (future) needs auth | SR-018 | Team D | open |
| T4 | Camera frames | Information disclosure | Frames with workers saved or streamed | 3 | 2 | 6 | `tag_logger` never writes frames; any live view on the web UI must be opt-in, local network only | SR-018 | Team D | open |
| T5 | Camera frames | Denial of service | Camera covered, unplugged or blinded | 2 | 3 | 6 | Status "none"/"rejected" is logged; pose falls back to odometry + LiDAR; robot never depends on vision to stop | SR-018 | Team D | open |
| T6 | Dependencies | Tampering | Malicious or broken OpenCV wheel | 3 | 1 | 3 | Pin versions in the robot image; install from PyPI over HTTPS; CI runs the synthetic-image tests | SR-018 | Team D | open |

## Residual risks and accepted limits
Tag spoofing is accepted for the prototype because the pose correction is log-only until TP-V02 and never feeds a
safety function. AprilTags carry no authentication.

## Verification
TP-V02 part L3 (unmapped, moved, covered and hand-held tags) and L4 (no frames written). Not run yet.
