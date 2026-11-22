# Privacy and memory-residence review — camera and person detection (2026-11-22)

Scope: `linux/vision/privacy.py`, `linux/vision/people.py`, `linux/vision/pipeline.py`, `linux/vision/tag_logger.py`,
`linux/nav/caution.py`, `linux/vision/test_privacy.py` (working tree, uncommitted). Threat model:
`docs/security/TM-V01-camera-apriltag.md` rev 2. Requirements: SR-021 (privacy of camera data), SR-020 (caution),
SR-019 (multi-tag trust), SR-018, SR-017.

Owner requirement under review: processing of people/images must be eliminated or censored, and frames/person images
must not stay allocated in memory.

Method: code reading, `python -m pytest -q linux` (31 passed, OpenCV 4.14.0, numpy 2.5.3, this dev container, not the
robot), small experiments in the dev container (`harden_process()` returned both flags True and `PR_GET_DUMPABLE`
read 0; `sorted()` on `/dev/video*` names puts `video10` before `video2`). Items marked "(deduced)" come from
knowledge of OpenCV/Linux internals and were not measured on the robot. No code was changed by this review.

Safety note: none of the findings below weakens a safety stop; the camera is not a safety sensor and the MCU clamps
every command (CLAUDE.md rule 1). Severities rate privacy and integrity impact.

## Findings
| ID | File:line | Severity | Finding | Recommended fix | SR |
|---|---|---|---|---|---|
| P-01 | `requirements/requirements.yaml` (SR-019, SR-020, SR-021 absent); cited in `linux/vision/privacy.py:1`, `people.py:1`, `nav/caution.py:1`, `localizer.py:1` | High | The three requirements this code implements do not exist in the single source of truth (rule 3); ADR-0008 and ADR-0009 are cited but missing from `docs/adr/`; TP-V03 is cited but not written. The traceability checker cannot catch code citing undefined IDs. Verified by grep. | Add SR-019/020/021 with one "shall" and a verifiable acceptance each (e.g., SR-021: "0 image files and 0 listening frame servers on the robot image; frame and all pipeline copies zeroed before `process()` returns"); write ADR-0009 (privacy design) and TP-V03. | SR-019, SR-020, SR-021 |
| P-02 | `linux/vision/pipeline.py:1`, `pipeline.py:25`; `privacy.py:3-5`; `tag_logger.py:4` | High | Claims "all pixels wiped" overstate what the code can do. Only numpy arrays visible to Python are zeroed. Not reachable: V4L2 mmap ring buffers (kernel, typically 4 frames) (deduced); the OpenCV `VideoCapture` internal conversion buffer that keeps the last decoded BGR frame between reads (deduced); ArUco threshold images and the HOG image pyramid (`scale=1.05` gives many levels) and its padded copy, freed by `cv::fastFree` without zeroing (deduced); allocator free lists. `privacy.py:7-9` states the limit honestly; the other docstrings do not. | Reword to "every buffer created by the pipeline is zeroed; OpenCV/kernel buffers are not reachable (TM-V01 T9)". Optional: `cv2.setUseOptimized` does not help; the real mitigations are OS-level (P-05, P-06, P-07). Consider a separate capture+detect process that exits per run so its whole address space is returned to the kernel. | SR-021 |
| P-03 | `linux/vision/tag_logger.py:51` | Medium | `harden_process()` result is logged but not enforced: if `prctl` or `setrlimit` fails, the logger still opens the camera (fail-open of a privacy control). It is also only called by `tag_logger`; any future entry point (web UI, multi-camera runner) that imports `pipeline.process` is unhardened. | Refuse to open any camera unless both flags are True (raise and exit non-zero); call it from a single camera-runner entry point and assert it in `open_camera`. | SR-021 |
| P-04 | `linux/vision/tag_logger.py:31-41` | Medium | Camera chosen as the first `/dev/video2+` that opens: no vendor/product/serial check, so a swapped camera, a BadUSB camera or a `v4l2loopback` device is accepted. `sorted(glob)` is lexicographic (`video10` < `video2`, verified), which will mis-map cameras when ≥ 4 are fitted (each UVC camera creates 2 nodes). | udev rule matching VID/PID/serial with a stable symlink; config maps each camera index to `/dev/v4l/by-id/...` or by-path; log and refuse unknown devices; alarm if the device also enumerates as HID. | SR-021, SR-019 |
| P-05 | `linux/vision/privacy.py:24-38` (image level) | Medium | `RLIMIT_CORE=0` alone may not stop a dump when `kernel.core_pattern` pipes to systemd-coredump (deduced; the pipe handler decides); non-dumpable is the stronger control. Swap is not addressed in code: numpy/OpenCV buffers can be paged to swap/zram backing storage on the eMMC. No `mlock`. | Image: swap off or encrypted per boot, `fs.suid_dumpable=0`, coredump `Storage=none`. Add a commissioning check that reads `/proc/swaps` and `PR_GET_DUMPABLE` and refuses to start the camera if swap is active unencrypted. | SR-021 |
| P-06 | `linux/vision/tag_logger.py:59`, `:81`, `:84` | Medium | Log re-identification: each frame logs person bearing and distance with robot pose and time. Together they give an absolute location track of workers; linked to the shift roster (file mtime gives wall-clock start) this is personal data under LFPDPPP. File is created with the default umask (typically 0644, world-readable). `meta` logs full config paths (may reveal a home directory/user name). | Log only what TP-V03 needs: person count and nearest distance in 0.5 m bins, or only the caution flag in field runs; create the file with mode 0600 (`os.open(..., 0o600)`); write to tmpfs and move to private release assets; 30-day retention and access list in the logging README; log config file hashes instead of paths. | SR-021 |
| P-07 | Robot image (no file) | Medium | Nothing yet guarantees that only the app can open `/dev/video*`, that the app runs as non-root, or that no streaming server exists. Any process in group `video` (or root) bypasses every in-process control. | Dedicated non-root user, sole member of `video`; read-only code dir; commissioning checklist: `ss -ltnp` shows only the web UI port, no `mjpg-streamer`/`motion`. | SR-021 |
| P-08 | `linux/vision/privacy.py:64-70` | Medium | `redact()` is a deny-list: it blacks out only HOG boxes. HOG misses sitting, partly occluded and close people, so any debug view built on it would show unredacted workers. `PersonDetector.detect` returns no boxes, so there is no correct caller today and boxes from the 320 px image would be mis-scaled if passed directly. Dead code (rule 10). | Delete `redact()` until a debug view is approved by ADR; if a view is ever needed, use an allow-list (show only tag ROIs, black everything else). | SR-021 |
| P-09 | `linux/vision/tag_logger.py:39` | Low | `CAP_PROP_BUFFERSIZE=1` return value not checked; the V4L2 backend may ignore it, so more frames stay queued in kernel buffers (and are stale, lesson 12). | Check the return of `cap.set` and `cap.get`; log the effective buffer count in `meta`. | SR-021 |
| P-10 | `linux/vision/tag_logger.py:67-73`, `:89` | Low | A frame read at `:67` is not zeroed if an exception (e.g., `KeyboardInterrupt`) arrives before `process()` at `:72`; `cap.release()` is not in `finally`, so on any exception the capture (and its buffers) is only released at interpreter exit. | Wrap read+process in `FrameScope` at the call site (track the frame right after `read`); `try/finally: cap.release()`. | SR-021 |
| P-11 | `linux/vision/privacy.py:59-61` | Low | If one `fill(0)` raised, later buffers would not be wiped. Low likelihood (only writeable arrays are tracked). Views: if a caller passes a view of a larger buffer (future multi-camera ROI), only the view is wiped. | Wipe in a `try` per buffer and re-raise after the loop; in `track()`, also track `buf.base` when it is an ndarray. | SR-021 |
| P-12 | `linux/vision/test_privacy.py:77-80` | Low | The hardening test asserts only the core limit, not `non_dumpable`, the stronger control. No test checks that a `tag_logger` run writes no image data (TP-V02 L4 is manual). | Assert `prctl(PR_GET_DUMPABLE)==0` on Linux; add a test that runs `main()` with a fake capture and checks the output contains only JSON with no arrays larger than 4×2. | SR-021 |
| P-13 | `linux/vision/tag_logger.py:69-71` | Low | When the camera fails, `caution.update` is skipped, so caution drops after `hold_s` while the camera is blind (fail-open of an advisory function). Safety is unaffected (MCU stops). | On read failure or stale frames, keep caution active (call `update` with a "camera unavailable" trigger). | SR-020 |
| P-14 | `linux/vision/people.py:39-41` | Low | No per-frame time budget for HOG (lesson 12) and detection weights are discarded (no threshold). At 320 px width the 64×128 HOG window misses people farther than about 4 m with the example calibration (deduced: 277 px focal at that scale × 1.7 m / 128 px); distance is biased short because HOG boxes include padding (conservative for caution). | Measure HOG time on the QRB2210; skip person detection when over budget and report it; keep weights for a TP-V03-derived threshold (rule 5). | SR-020 |
| P-15 | `linux/vision/localizer.py:190-191` | Low (log-only now) | Tag-pair trust: two printed tags at the surveyed spacing pass the pair cross-check and are accepted in one frame; home IDs 100–101 are printable from `docs/apriltags/`. Accepted only while `NAV_ENABLED=False`. | Before enabling: bound multi-tag jumps with LiDAR scan agreement; dock confirmed by LiDAR geometry and charging contacts; add printed-pair cases to TP-V02 L3 (TM-V01 T7, T8). | SR-019, SR-017 |
| P-16 | `linux/vision/tag_logger.py:80` | Low | `obs` is a dict keyed by tag ID, so two detections of the same ID in one frame (a duplicated printed tag) collapse to one entry: spoof evidence is lost from the TP-V02 log. | Log a list of `[id, cam, corners]`. | SR-018 |
| P-17 | `pyproject.toml:9` | Low | `opencv-python-headless>=4.8,<5` and `numpy>=1.26` are ranges, not pins. | Exact pins with hashes in the robot image lockfile; `pip-audit` on change. | SR-021 |

## Verified by tests (dev container, 2026-11-22, `python -m pytest -q linux`: 31 passed)
- The input frame (BGR or grey) is all zeros after `process()` returns, and tags are still detected:
  `test_frame_is_zeroed_after_processing_and_tags_still_found`.
- The frame is zeroed when processing raises: `test_frame_is_zeroed_even_when_processing_fails`.
- `FrameScope` zeroes every tracked buffer of any dtype and refuses read-only buffers:
  `test_scope_wipes_every_tracked_buffer`, `test_scope_refuses_buffers_it_cannot_wipe`.
- `Person` has only `bearing_deg`, `distance_m`, `cam` (no pixel field): `test_person_summary_holds_no_pixels`.
- No false person in a flat grey scene: `test_empty_scene_has_no_people`.
- `redact()` blacks out a box plus margin: `test_redact_blacks_out_box_with_margin`.
- `RLIMIT_CORE` is (0, 0) after `harden_process()`: `test_harden_process_disables_core_dumps`. Non-dumpable was
  checked by hand only (P-12).
- Caution triggers, holds 2 s, and only lowers speed: `test_caution_triggers_holds_and_only_lowers_speed`; caution
  makes a tag-pair jump need 2 reads: `test_caution_requires_two_reads_for_multi_tag_jump` (`test_vision.py`).

Not verified: anything on the robot image (swap, coredump, `video` group, listening ports, udev rule), wiping of
OpenCV/kernel buffers (not possible from Python), HOG detection quality (TP-V03), TP-V02 L3/L4.

## Residual risk
Python and OpenCV cannot guarantee that no copy of a frame remains in RAM: kernel V4L2 buffers, the `VideoCapture`
conversion buffer, OpenCV temporaries and freed allocator pages hold pixels until overwritten (deduced). The code
reduces residence to the buffers it creates (zeroed per frame) and, with `harden_process`, keeps them out of core
dumps and same-user ptrace. Root on the robot, a cold-boot/DMA attacker, or an unencrypted swap device can still
recover recent frames; the image controls in TM-V01 (swap off/encrypted, non-root app user alone in `video`, no
streaming server, tmpfs logs with retention) are required before people are filmed, and must be verified in TP-V03.
Person summaries in logs remain personal data when linkable to rosters (P-06). Tag, tag-pair and home-tag spoofing
remain accepted only while vision is log-only (SR-017). With 2 High findings (P-01, P-02) open, SR-021 should not be
reported as met.

## Disposition (2026-11-22, after the review)
| ID | Status |
|---|---|
| P-01 | Closed: SR-019–SR-023, ADR-0008/0009/0010, TP-V03 added; traceability check fails on cited-but-undefined SR IDs |
| P-02 | Closed: docstrings now say only buffers created by the pipeline are zeroed |
| P-03 | Closed: `require_hardening()` refuses to open a camera if hardening fails |
| P-04 | Partial: optional `device` (stable `/dev/v4l/by-id` path) in camera config, numeric ordering; udev rule on the image open |
| P-05, P-07 | Open (robot image), listed in TP-V03 P4 |
| P-06 | Closed in code: count + nearest-distance bin only, file 0600, config hashes; retention policy open |
| P-08 | Closed: `redact()` deleted |
| P-09 | Closed: buffer-size result logged in `meta` |
| P-10, P-11, P-12, P-13, P-16 | Closed (tests listed in TM-V01) |
| P-14 | Open: HOG time budget to measure in TP-V03 |
| P-15 | Accepted while log-only; LiDAR agreement required before enabling (ADR-0008, F-013) |
| P-17 | Open: exact pins with hashes in the robot image lockfile |
