# Threat model — camera, AprilTag localization and person detection (rev 2, 2026-11-22)

Owner: Team D · related SR-017, SR-018, SR-019 (multi-tag trust), SR-020 (caution), SR-021 (privacy of camera data) ·
ADR-0006, ADR-0007 (ADR-0008 and ADR-0009 are cited in code but are not yet in `docs/adr/`) · DFMEA F-010–F-012 ·
review `docs/security/privacy-review-2026-11-22.md`. Method: STRIDE per data flow; risk = impact (1–5) × likelihood
(1–5).

Revision history: rev 1 (2026-11-21) single camera + AprilTags. Rev 2 (2026-11-22) adds person detection (caution
mode), privacy of frames in memory, tag-pair and home-tag spoofing, camera device selection, multi-camera future and
the controls still needed on the robot image. SR-019 to SR-023 were added to `requirements/requirements.yaml` and
`tools/check_traceability.py` now fails on any cited but undefined SR ID (P-01 closed, 2026-11-22).

Scope rule (unchanged): the camera is never a safety sensor. MCU stops, LiDAR stop zone, bumpers, watchdog and the
hardware e-stop work with Linux and every camera fully compromised (CLAUDE.md rule 1, ADR-0002). Vision outputs can
only correct the navigator pose (log-only while `NAV_ENABLED = False`, SR-017) or lower the speed request (caution).

## Assets
| Asset | Why it matters |
|---|---|
| Robot pose estimate | Integrity: a wrong pose sends the robot along the wrong lane (safety chain still stops it) |
| Tag map JSON | Integrity: defines where every tag is; an edit moves every fix |
| Home (dock) tag pair, IDs 100–101 | Integrity: defines where the robot docks; printable by anyone |
| Camera frames (raw, grey, downscaled copies) | Privacy (SR-021, LFPDPPP): workers appear in view; owner requires that person images are not kept in memory, disk or network |
| Person summaries (bearing, rough distance, camera index) | Privacy: no pixels, but with pose and time they become a location track of workers |
| Caution flag | Availability/integrity of an advisory speed reduction (SR-020); not a safety function |
| Tag logs (JSON lines) | Integrity for TP-V02/TP-V03 evidence; contain person summaries, so they are personal data when linkable to a shift roster |
| Camera devices `/dev/video*` | Confidentiality: any process that can open them can capture people |

## Data flows and trust boundaries
| Flow | From → To | Channel | Crosses boundary? |
|---|---|---|---|
| Camera frames | USB camera → V4L2 kernel buffers → OpenCV `VideoCapture` → `linux/vision/pipeline.py` | USB/V4L2, mmap | Yes (physical device, anything in view; kernel/OpenCV buffers outside Python control) |
| Printed tags | Plant walls / home station → camera | Optical | Yes (anyone can print, move or hold a tag) |
| Tag map / camera config | Repo or web UI → `linux/vision` | File | Yes when edited from the web UI (future) |
| Grey and downscaled copies | `pipeline.process` → `detector.detect`, `people.PersonDetector.detect` | In-process (numpy + OpenCV C++ temporaries) | No, but OpenCV internal temporaries are not wiped |
| Person summaries | `people.py` → `nav/caution.py` → localizer (`caution=`) and speed request | In-process | No |
| Speed request | Linux navigator → MCU | Bridge RPC | Yes; MCU clamps to SR-004 limits whatever Linux sends |
| Pose fix | `linux/vision` → navigator (Linux) | In-process | No; MCU safety does not consume it |
| Run log | `tag_logger.py` → `--out` JSON lines file → private release asset | File | Yes (leaves the process; persists) |
| Debug view of frames | — | — | Does not exist (no HTTP/socket code in `linux/`, verified by grep 2026-11-22); `redact()` deleted (P-08) |
| Crash / swap | Process memory → core dump, swap device | Kernel | Yes (pixels can reach disk) |
| Multi-camera (planned, ≥ 4) | 4 × USB camera → same process | USB/V4L2 | Yes; device-to-calibration mapping becomes a trust issue |

## Threats
| ID | Flow | STRIDE | Attack scenario | Impact | Likelihood | Risk | Control | SR | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | Printed tags | Spoofing | Someone shows a printed tag with a mapped ID somewhere else | 3 | 2 | 6 | 2-read confirmation against odometry; reprojection gate; MCU stops stay independent; log-only until TP-V02 (L3 tests it) | SR-018, SR-017 | Team D | open |
| T2 | Printed tags | Tampering | A tag is moved or rotated (cleaning crew, forklift) | 3 | 3 | 9 | Same gates; pair disagreement rejects both tags (`localizer.py`, test `test_tags_that_disagree_are_all_rejected`); re-survey after layout changes; replay logs flag growing disagreement with LiDAR | SR-018, SR-019 | Team D | open |
| T3 | Tag map | Tampering | Map edited with wrong coordinates | 3 | 2 | 6 | Map in git with review; loader validates family, unique IDs, size range (`config.py`); web UI editing (future) needs auth | SR-018 | Team D | open |
| T4 | Camera frames | Information disclosure | Frames with workers saved or streamed | 4 | 2 | 8 | `tag_logger.py` never writes frames (no `imwrite`, no server in `linux/`); `pipeline.process` zeroes frame and copies; any live view must be opt-in, authenticated, LAN only, and needs an ADR | SR-021 | Team D | open |
| T5 | Camera frames | Denial of service | Camera covered, unplugged or blinded | 2 | 3 | 6 | Status "none"/"rejected" is logged; pose falls back to odometry + LiDAR; robot never depends on vision to stop. Gap: caution drops after `hold_s` while the camera is blind (fail-open of an advisory function) | SR-018, SR-020 | Team D | open |
| T6 | Dependencies | Tampering | Malicious or broken OpenCV wheel | 3 | 1 | 3 | `opencv-python-headless>=4.8,<5` (HOG needs < 5) and `numpy>=1.26` are ranges, not pins: pin exact versions with hashes in the robot image; `pip-audit` before upgrades; CI runs the synthetic-image tests | SR-018, SR-021 | Team D | open |
| T7 | Tag pair | Spoofing | Two printed tags with mapped IDs, mounted at the surveyed spacing, are shown together. The pair cross-check only proves the two tags agree with each other, not that they are the real ones: **two printed tags together defeat the pair cross-check** and give an accepted fix in one frame, even 1.5 m / 10° away from odometry (by design, `test_two_agreeing_tags_are_trusted_at_once_even_far_from_odometry`). Under caution it needs only 2 reads, which a static fake gives | 3 | 2 | 6 | Log-only while `NAV_ENABLED = False` (SR-017); MCU stops independent. Needed before enabling: bound any multi-tag jump against LiDAR scan match or odometry (e.g., jump > `jump_m` needs LiDAR agreement); include case "printed pair" in TP-V02 L3 | SR-019, SR-017 | Team D | open |
| T8 | Home tags 100–101 | Spoofing | Home IDs 100–101 are public (printable sheet in `docs/apriltags/`); a printed home pair placed elsewhere makes the robot "find" the dock in the wrong place and drive its approach (`approach_m`) toward a wall, a person or a machine | 3 | 2 | 6 | Log-only (SR-017); MCU LiDAR/bumper stops and speed clamp stay. Needed: dock confirmation by LiDAR geometry of the station and charging-contact voltage before declaring "docked"; tamper-evident mounting of the real home tags; TP-V02 L3 case "printed home pair" | SR-019, SR-017 | Team D | open |
| T9 | Frames in process memory | Information disclosure | A local attacker or another process reads frame residue from the app's memory (`/proc/<pid>/mem`, ptrace) or from buffers the code cannot reach: V4L2 mmap ring buffers, OpenCV `VideoCapture` conversion buffer, ArUco/HOG pyramid temporaries, freed allocator pages | 3 | 2 | 6 | `privacy.FrameScope` zeroes every tracked numpy buffer, also on exceptions (`pipeline.py`, tests in `test_privacy.py`); `privacy.harden_process()` sets `PR_SET_DUMPABLE 0` (blocks same-UID ptrace and `/proc/<pid>/mem`). Python cannot wipe OpenCV/kernel buffers: residue reduced, not eliminated. Needed: app as non-root user, nothing else running as that user; fail closed if `non_dumpable` is False | SR-021 | Team D | open |
| T10 | Crash / swap | Information disclosure | A crash writes a core dump, or memory pressure pages frame buffers to swap/zram backing storage, and pixels persist on the eMMC | 4 | 2 | 8 | `harden_process()` sets `RLIMIT_CORE = 0` and non-dumpable (tested: `test_harden_process_disables_core_dumps`). Needed on the robot image: swap off (or encrypted with a random key per boot), `fs.suid_dumpable = 0`, systemd-coredump `Storage=none`, no `apport`/crash reporters | SR-021 | Team D | open (image) |
| T11 | Run log | Information disclosure | Person bearing + distance + robot pose + timestamp per frame reconstructs where workers were and when; linked with the shift roster this identifies people (personal data, LFPDPPP) | 3 | 3 | 9 | No pixels in logs. Done (P-06): log holds only person count and nearest distance in 0.5 m bins, file mode 0600, configs by hash. Still needed: logs on tmpfs or private release assets only, 30-day retention and access list in the logging README | SR-021 | Team D | open |
| T12 | Camera device | Spoofing | A different USB device (swapped camera, `v4l2loopback` virtual device, BadUSB camera + HID) is opened because `open_camera` takes the first `/dev/video2+` that opens; injected frames could fake tags or hide people | 3 | 2 | 6 | Probe skips internal `/dev/video0–1`. Needed: udev rule matching vendor/product/serial with a stable symlink (`/dev/v4l/by-id/...`); log new USB devices; HID enumeration is an alarm; no `v4l2loopback` module in the image | SR-021, SR-018 | Team D | open |
| T13 | Camera device | Information disclosure | Another local user or service opens `/dev/video*` and captures people directly, bypassing all in-process controls | 4 | 2 | 8 | None in code. Needed: only the app user in group `video`; no other login users in that group; no frame streaming server (mjpg-streamer, motion, web UI stream) installed; firewall per the main threat model | SR-021 | Team D | open (image) |
| T14 | Person summaries → caution | Denial of service / tampering | HOG misses people (sitting, partly occluded, closer than ≈1 m, farther than ≈4 m at 320 px width (deduced)) or gives false positives; vision CPU load delays the RPC loop | 2 | 3 | 6 | Caution only lowers the speed request (`nav/caution.py`, test `test_caution_triggers_holds_and_only_lowers_speed`); MCU stops do not depend on it; detection quality measured in TP-V03 (not written yet); per-frame CPU budget needed (lesson 12) | SR-020 | Team D | open |
| T15 | Debug view (future) | Information disclosure | A debug view relies on `redact()` to black out HOG person boxes; HOG misses a person, so the person is shown unredacted | 4 | 2 | 8 | View does not exist and is off by default. Needed before any view: ADR; allow-list redaction (show only tag ROIs, black everything else) instead of deny-list; auth on the web UI; never by default | SR-021 | Team D | open |
| T16 | Multi-camera (planned) | Tampering / information disclosure | With ≥ 4 cameras, lexicographic order of `/dev/video*` (`video10` before `video2`) or re-enumeration after reboot maps a camera to the wrong calibration (bad poses) and multiplies the frame buffers held in kernel/OpenCV | 3 | 3 | 9 | `Observation.cam` and `Person.cam` carry the camera index; localizer rejects unknown indices. Needed: by-id/by-path mapping per camera in config; per-camera `FrameScope`; repeat T9/T10/T13 checks for every camera | SR-019, SR-021 | Team D | open |
| T17 | App process | Elevation of privilege | App runs as root (default on a dev board); every in-process privacy control becomes moot and a compromise reaches the camera, logs and RPC | 4 | 2 | 8 | Needed on the image: dedicated non-root user in group `video` (and `dialout` only if needed), read-only code directory, secrets 0600 outside the repo; MCU still clamps every command | SR-021 | Team D | open (image) |

## Controls that exist in code (verified 2026-11-22, `python -m pytest -q linux`: 31 passed)
| Control | File | Test |
|---|---|---|
| Frame and every tracked copy zeroed before `process()` returns, also on exceptions | `linux/vision/pipeline.py`, `linux/vision/privacy.py` (`FrameScope`) | `test_frame_is_zeroed_after_processing_and_tags_still_found`, `test_frame_is_zeroed_even_when_processing_fails`, `test_scope_wipes_every_tracked_buffer`, `test_scope_refuses_buffers_it_cannot_wipe` |
| Core dumps off, process non-dumpable; camera refused if either fails (fail-closed, P-03) | `linux/vision/privacy.py` (`require_hardening`), called first in `linux/vision/tag_logger.py` | `test_harden_process_disables_core_dumps` (core limit and `PR_GET_DUMPABLE == 0`) |
| Views wiped through their base buffer; wipe continues if one buffer fails (P-11) | `linux/vision/privacy.py` | `test_scope_wipes_base_of_a_view` |
| Frame tracked right after `read()`, capture released in `finally` (P-10); cameras by configured `/dev/v4l/by-id` path or numeric order (P-04, partial) | `linux/vision/tag_logger.py` | `test_camera_candidates_numeric_order` |
| Blind camera keeps caution on (P-13) | `linux/nav/caution.py` | `test_caution_triggers_holds_and_only_lowers_speed` |
| Coarse person logging, 0600 file (P-06) | `linux/vision/tag_logger.py` | `test_logged_person_data_is_coarse` |
| Person output holds no pixels (bearing, distance, cam) | `linux/vision/people.py` | `test_person_summary_holds_no_pixels` |
| HOG runs on a downscaled grey copy (≤ 320 px wide) that is tracked and wiped | `linux/vision/people.py` | indirect (scope tests) |
| Caution can only lower speed and holds 2 s | `linux/nav/caution.py` | `test_caution_triggers_holds_and_only_lowers_speed` |
| Caution makes multi-tag jumps need 2 reads | `linux/vision/localizer.py` | `test_caution_requires_two_reads_for_multi_tag_jump` |
| No frames written or served | `linux/vision/tag_logger.py`; no HTTP/socket code in `linux/` | grep only; TP-V02 L4 on the robot not run |

## Controls still needed on the robot image (owner: Team D, before the first run with people present)
1. Swap off (`swapoff -a`, no zram swap), or swap encrypted with a random per-boot key.
2. `fs.suid_dumpable = 0`; systemd-coredump `Storage=none` and `ProcessSizeMax=0`; no crash reporters.
3. App runs as a dedicated non-root user, the only member of group `video`; camera matched by udev rule (vendor,
   product, serial) with a stable symlink; no `v4l2loopback`.
4. No frame streaming server installed or listening (check `ss -ltnp` in the commissioning checklist).
5. Run logs written to tmpfs (or 0600 files) and moved to private release assets; 30-day retention and access list in
   the logging README.
6. Exact version pins with hashes for `opencv-python-headless` and `numpy`; `pip-audit` before each upgrade.

## Residual risks and accepted limits
- Tag and tag-pair spoofing (T1, T7) and home-tag spoofing (T8) are accepted for the prototype only because pose
  correction is log-only until TP-V02 and never feeds a safety function. AprilTags carry no authentication; two
  printed tags defeat the pair cross-check. These must be re-assessed before `NAV_ENABLED` is set.
- Frame residue in OpenCV and kernel buffers (T9) cannot be eliminated from Python; the controls reduce the time and
  number of copies and keep them out of disk, network and other processes. Root on the robot can read them.
- Person detection is advisory; misses and false positives affect productivity, not safety.

## Verification
TP-V02 part L3 (unmapped, moved, covered and hand-held tags; to add: printed pair, printed home pair) and L4 (no
frames written). TP-V03 (`docs/test-reports/TP-V03-person-caution-privacy.md`: person detection, caution, privacy checks on the
robot image: swap, core dumps, `video` group, listening ports) written, not run. TP-N01 adds the printed home pair
case.
