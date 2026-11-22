import glob
import math
import os
import threading
import time
import traceback
from collections import Counter

os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

import cv2
import numpy as np
from arduino.app_utils import App, Bridge

import logbook
import web

TARGET_FPS = 60
# camera modes tried at startup (w, h, fps, fourcc); the fastest measured one wins
MODES = [
    (320, 240, 60, "MJPG"),
    (320, 240, 60, "YUYV"),
    (640, 480, 60, "MJPG"),
    (320, 240, 30, "YUYV"),
    (640, 480, 30, "MJPG"),
]
# manual exposure in V4L2 units (100 us); must stay < 1/fps (166 at 60 fps). None = auto
EXPOSURE = 100
CAL_W, CAL_H = 640, 480
K_CAL = np.array([[600.0, 0, 320.0], [0, 600.0, 240.0], [0, 0, 1]])
K = K_CAL.copy()
D = np.zeros(5)
TAG_SIZE = 0.20
MAX_ERR_PX = 2.0
MAX_DIST = 4.0
SAME_M, SAME_DEG = 0.15, 8.0
PRIOR_TTL = 1.0

CAM_X, CAM_Y, CAM_Z, CAM_YAW = 0.0, 0.0, 0.51, 0.0
CAM_PITCH = 6.5  # deg, + = camera looks up
# per-tag camera positions further apart than this: the TAGS map is wrong
TAGS_AGREE_M = 0.5

# id: (x, y, z, yaw_deg) of tag center; yaw = direction the tag faces (into the room)
TAGS = {
    0: (0.0, 0.0, 0.55, 0.0),
    1: (0.0, -0.41, 0.61, 0.0),
}

_h = TAG_SIZE / 2
OBJ = np.array(
    [[-_h, _h, 0], [_h, _h, 0], [_h, -_h, 0], [-_h, -_h, 0]], dtype=np.float32
)


def tf(R, t):
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = np.ravel(t)
    return T


def world_tag(x, y, z, yaw_deg):
    a = math.radians(yaw_deg)
    n = np.array([math.cos(a), math.sin(a), 0.0])
    up = np.array([0.0, 0.0, 1.0])
    return tf(np.column_stack([np.cross(-n, up), up, n]), [x, y, z])


def robot_cam():
    c, s = math.cos(CAM_YAW), math.sin(CAM_YAW)
    Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    p = math.radians(-CAM_PITCH)
    Ry = np.array(
        [[math.cos(p), 0, math.sin(p)], [0, 1, 0], [-math.sin(p), 0, math.cos(p)]]
    )
    base = np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]], dtype=float)
    return tf(Rz @ Ry @ base, [CAM_X, CAM_Y, CAM_Z])


T_WT = {k: world_tag(*v) for k, v in TAGS.items()}
MAP = [{"id": k, "x": v[0], "y": v[1], "yaw": v[3]} for k, v in TAGS.items()]
T_RC = robot_cam()
T_CR = np.linalg.inv(T_RC)
R_RC, t_RC = T_RC[:3, :3], T_RC[:3, 3]

params = cv2.aruco.DetectorParameters()
params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
det = cv2.aruco.ArucoDetector(
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11), params
)

grab = None
seq = 0
res = None
last_pose = None
last_t = 0.0
prev_t = 0.0
fps = 0.0


def fourcc(c):
    return (
        int(c.get(cv2.CAP_PROP_FOURCC)).to_bytes(4, "little").decode(errors="replace")
    )


def configure(dev, w, h, f, cc):
    c = cv2.VideoCapture(dev, cv2.CAP_V4L2)
    if not c.isOpened():
        return None
    c.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*cc))
    c.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    c.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    c.set(cv2.CAP_PROP_FPS, f)
    c.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if EXPOSURE is not None:
        c.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        c.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    return c


def measure(c, n=30):
    for _ in range(3):
        if not c.read()[0]:
            return 0.0, None
    t0 = time.monotonic()
    for _ in range(n):
        ok, f = c.read()
        if not ok:
            return 0.0, None
    return n / (time.monotonic() - t0), f.shape


def open_cam():
    devs = sorted(glob.glob("/dev/video*"), key=lambda p: int(p[10:]))
    print(f"video devices: {devs}")
    for d in devs:
        results = []
        for w, h, f, cc in MODES:
            c = configure(d, w, h, f, cc)
            if c is None:
                break
            fps_meas, shape = measure(c)
            got = {
                "req": [w, h, f, cc],
                "got": [shape[1], shape[0]] if shape else None,
                "fourcc": fourcc(c),
                "driver_fps": c.get(cv2.CAP_PROP_FPS),
                "measured_fps": round(fps_meas, 1),
                "exposure": c.get(cv2.CAP_PROP_EXPOSURE),
            }
            print(f"{d} mode {got}")
            results.append(got)
            c.release()
        logbook.write("camera_modes", dev=d, modes=results)
        good = [r for r in results if r["got"]]
        if not good:
            print(f"{d}: no frames")
            continue
        best = max(
            good, key=lambda r: (min(r["measured_fps"], TARGET_FPS), r["got"][0])
        )
        c = configure(d, *best["req"])
        print(f"camera {d} -> {best}")
        logbook.write("camera", dev=d, **best)
        return c
    return None


class Grabber:
    # reads frames in its own thread so capture overlaps processing; loop takes the newest
    def __init__(self, cap):
        self.cap = cap
        self.cv = threading.Condition()
        self.frame = None
        self.seq = 0
        self.alive = True
        self.fps = 0.0
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        prev = 0.0
        while self.alive:
            ok, f = self.cap.read()
            t = time.monotonic()
            with self.cv:
                if not ok:
                    self.alive = False
                    self.cv.notify_all()
                    break
                if prev:
                    dt = max(t - prev, 1e-3)
                    self.fps = 0.9 * self.fps + 0.1 / dt if self.fps else 1 / dt
                prev = t
                self.frame, self.seq = f, self.seq + 1
                self.cv.notify_all()
        self.cap.release()

    def next(self, last_seq, timeout=1.0):
        with self.cv:
            self.cv.wait_for(lambda: self.seq != last_seq or not self.alive, timeout)
            if not self.alive or self.seq == last_seq:
                return None, last_seq
            return self.frame, self.seq

    def stop(self):
        self.alive = False


def set_res(w, h):
    # intrinsics scale with resolution; calibrate once at CAL_W x CAL_H
    global K, res
    K = K_CAL * np.array([[w / CAL_W], [h / CAL_H], [1.0]])
    res = (w, h)
    print(f"resolution {w}x{h}")
    logbook.write("resolution", w=w, h=h, K=K)


def T_robot(x, y, yaw):
    c, s = math.cos(yaw), math.sin(yaw)
    return tf(np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]), [x, y, 0.0])


def resjac(pose, pts_w, obs):
    # residuals in normalized image coords and their Jacobian wrt (x, y, yaw)
    x, y, yaw = pose
    c, s = math.cos(yaw), math.sin(yaw)
    dx, dy = pts_w[:, 0] - x, pts_w[:, 1] - y
    q0, q1 = c * dx + s * dy, -s * dx + c * dy
    Pc = np.outer(q0, R_RC[0]) + np.outer(q1, R_RC[1]) + np.outer(pts_w[:, 2], R_RC[2])
    Pc -= t_RC @ R_RC
    z = Pc[:, 2]
    if np.any(z <= 0.05):
        return None, None
    u, v = Pc[:, 0] / z, Pc[:, 1] / z
    r = np.empty(2 * len(z))
    r[0::2], r[1::2] = u - obs[0::2], v - obs[1::2]
    J = np.empty((2 * len(z), 3))
    dPx = -c * R_RC[0] + s * R_RC[1]
    dPy = -s * R_RC[0] - c * R_RC[1]
    dPa = np.outer(q1, R_RC[0]) - np.outer(q0, R_RC[1])
    for k, dP in enumerate((dPx, dPy)):
        J[0::2, k] = (dP[0] - u * dP[2]) / z
        J[1::2, k] = (dP[1] - v * dP[2]) / z
    J[0::2, 2] = (dPa[:, 0] - u * dPa[:, 2]) / z
    J[1::2, 2] = (dPa[:, 1] - v * dPa[:, 2]) / z
    return r, J


def refine(pose, pts_w, obs, iters=10):
    # Gauss-Newton on (x, y, yaw): camera height and tilt are fixed by the mount
    p = np.array(pose, dtype=float)
    cost, stall = math.inf, 0
    for _ in range(iters):
        r, J = resjac(p, pts_w, obs)
        if r is None:
            return None, math.inf
        c = float(r @ r)
        stall = stall + 1 if c > 0.99 * cost else 0
        if stall >= 2:
            break
        cost = min(cost, c)
        step = np.linalg.solve(J.T @ J + 1e-9 * np.eye(3), -(J.T @ r))
        step *= min(1.0, 0.5 / max(1e-9, np.max(np.abs(step))))
        p += step
        if np.max(np.abs(step)) < 1e-6:
            break
    r, _ = resjac(p, pts_w, obs)
    if r is None:
        return None, math.inf
    p[2] = math.atan2(math.sin(p[2]), math.cos(p[2]))
    return p, float(math.sqrt(2 * np.mean(r**2)) * K[0, 0])


def seeds(tag_id, corners):
    # both IPPE solutions of each tag (free 6-DOF), flattened to the floor plane as seeds
    n, rvecs, tvecs, errs = cv2.solvePnPGeneric(
        OBJ, corners, K, D, flags=cv2.SOLVEPNP_IPPE_SQUARE
    )
    out, raw = [], []
    for rvec, tvec, err in zip(rvecs[:n], tvecs[:n], np.ravel(errs)[:n]):
        R, _ = cv2.Rodrigues(rvec)
        T_wc = T_WT[tag_id] @ np.linalg.inv(tf(R, tvec))
        T = T_wc @ T_CR
        dist = float(np.linalg.norm(tvec))
        raw.append(
            {
                "dist": round(dist, 3),
                "err": round(float(err), 3),
                "cam_xyz": np.round(T_wc[:3, 3], 3),
                "cam_pitch": round(
                    math.degrees(math.asin(np.clip(T_wc[2, 2], -1, 1))), 1
                ),
                "yaw": round(math.degrees(math.atan2(T[1, 0], T[0, 0])), 1),
            }
        )
        if dist <= MAX_DIST:
            out.append((T[0, 3], T[1, 3], math.atan2(T[1, 0], T[0, 0])))
    return out, raw


def same(a, b):
    dyaw = abs((a[2] - b[2] + math.pi) % (2 * math.pi) - math.pi)
    return (
        math.hypot(a[0] - b[0], a[1] - b[1]) < SAME_M and math.degrees(dyaw) < SAME_DEG
    )


def side_px(c):
    return float(np.mean(np.linalg.norm(c - np.roll(c, 1, axis=0), axis=1)))


def estimate(gray, frame=None, prior=None):
    corners, ids, rej = det.detectMarkers(gray)
    diag = {"rejected": len(rej), "det": [], "sols": [], "reason": None}
    if ids is None or len(ids) == 0:
        diag["reason"] = "no_markers"
        return None, diag
    if frame is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    pts_w, uv, cand, used = [], [], [], []
    for c, tag_id in zip(corners, ids.ravel()):
        tag_id = int(tag_id)
        c = c.reshape(4, 2)
        d = {"id": tag_id, "side_px": round(side_px(c), 1), "known": tag_id in T_WT}
        diag["det"].append(d)
        if not d["known"]:
            continue
        Tw = T_WT[tag_id]
        pts_w.append(OBJ @ Tw[:3, :3].T + Tw[:3, 3])
        uv.append(cv2.undistortPoints(c.reshape(-1, 1, 2), K, D).reshape(-1))
        s, d["ippe"] = seeds(tag_id, c)
        cand += s
        used.append(tag_id)
    if not used:
        diag["reason"] = f"unknown_ids {[d['id'] for d in diag['det']]}"
        return None, diag
    if not cand:
        diag["reason"] = f"too_far >{MAX_DIST}m"
        return None, diag
    # free 6-DOF camera pose from each tag alone (best IPPE branch): what the mount really is
    fits = [
        min(d["ippe"], key=lambda q: q["err"]) for d in diag["det"] if d.get("ippe")
    ]
    diag["fit"] = {
        "cam_z": round(float(np.median([q["cam_xyz"][2] for q in fits])), 3),
        "cam_pitch": round(float(np.median([q["cam_pitch"] for q in fits])), 1),
    }
    # two tags agree if any pair of their IPPE branches puts the camera at the same spot
    xy = [[q["cam_xyz"][:2] for q in d["ippe"]] for d in diag["det"] if d.get("ippe")]
    spread = max(
        (
            min(math.dist(a, b) for a in xa for b in xb)
            for i, xa in enumerate(xy)
            for xb in xy[i + 1 :]
        ),
        default=0.0,
    )
    if spread > TAGS_AGREE_M:
        diag["reason"] = f"tags_disagree {spread:.2f}m (check TAGS)"
        return None, diag
    pts_w, uv = np.vstack(pts_w), np.concatenate(uv)
    sols = []
    for s0 in cand:
        if any(same(s0, q) for q, _ in sols):
            continue
        p, e = refine(s0, pts_w, uv)
        if p is None:
            continue
        diag["sols"].append({"x": p[0], "y": p[1], "yaw": math.degrees(p[2]), "rms": e})
        if e <= MAX_ERR_PX and not any(same(p, q) for q, _ in sols):
            sols.append((p, e))
    if not sols:
        best = min((q["rms"] for q in diag["sols"]), default=math.inf)
        f = diag["fit"]
        # planar model does not fit: CAM_Z / CAM_PITCH / tag z / TAG_SIZE / K
        diag["reason"] = (
            f"reproj {best:.1f}px > {MAX_ERR_PX} "
            f"(cam_z~{f['cam_z']} pitch~{f['cam_pitch']} vs {CAM_Z}/{CAM_PITCH})"
        )
        return None, diag
    if len(sols) > 1:
        # mirror ambiguity (small or oblique tag): only a recent pose can pick the branch
        if prior is None:
            diag["reason"] = "ambiguous_no_prior"
            return None, diag
        sols.sort(key=lambda s: math.hypot(s[0][0] - prior[0], s[0][1] - prior[1]))
    (x, y, yaw), err = sols[0]
    diag["reason"] = "ok"
    if frame is not None:
        T_cw = np.linalg.inv(T_robot(x, y, yaw) @ T_RC)
        for tag_id in used:
            T = T_cw @ T_WT[tag_id]
            cv2.drawFrameAxes(
                frame, K, D, cv2.Rodrigues(T[:3, :3])[0], T[:3, 3], TAG_SIZE
            )
    return (x, y, yaw, used, err), diag


stats = Counter()
stats_t = 0.0


def summary(t, perf):
    global stats_t
    if t - stats_t < 1.0:
        return
    print(f"[1s] {perf} {dict(stats)}")
    stats.clear()
    stats_t = t


def loop():
    global grab, seq, last_pose, last_t, prev_t, fps
    if grab is None:
        cap = open_cam()
        if cap is None:
            print("no camera, retrying")
            logbook.write("no_camera", devs=glob.glob("/dev/video*"))
            web.publish(
                None, {"ok": False, "cam": False, "t": time.monotonic(), "map": MAP}
            )
            time.sleep(2)
            return
        grab = Grabber(cap)
    frame, seq = grab.next(seq)
    if frame is None:
        print("camera stopped, reopening")
        logbook.write("camera_stopped")
        grab.stop()
        grab = None
        return
    t = time.monotonic()
    if prev_t:
        fps = 0.9 * fps + 0.1 / max(t - prev_t, 1e-3) if fps else 1 / (t - prev_t)
    prev_t = t
    h, w = frame.shape[:2]
    if res != (w, h):
        set_res(w, h)
    frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prior = last_pose if t - last_t < PRIOR_TTL else None
    try:
        est, diag = estimate(gray, frame, prior)
    except Exception:  # noqa: BLE001  log any pose bug instead of killing the app
        logbook.write("error", tb=traceback.format_exc())
        print(traceback.format_exc())
        est, diag = None, {"reason": "exception"}
    ms = (time.monotonic() - t) * 1000
    perf = f"cam={grab.fps:.1f}fps proc={fps:.1f}fps {ms:.0f}ms"
    stats[diag["reason"].split(" ")[0]] += 1
    raw = [
        [float(v) for v in q["cam_xyz"][:2]]
        for d in diag.get("det", [])
        for q in d.get("ippe", [])
    ]
    info = {
        "cam": True,
        "t": t,
        "map": MAP,
        "w": w,
        "h": h,
        "cam_fps": round(grab.fps, 1),
        "fps": round(fps, 1),
        "ms": round(ms, 1),
        "reason": diag["reason"],
        "raw": raw,
    }
    rec = {
        "seq": seq,
        "cam_fps": grab.fps,
        "fps": fps,
        "ms": ms,
        "prior": prior,
        **diag,
    }
    if est is None:
        logbook.write("frame", ok=False, **rec)
        web.publish(frame, {"ok": False, **info})
        Bridge.notify("pose", 0.0, 0.0, 0.0, 0)
        summary(t, perf)
        return
    x, y, yaw, used, err = est
    last_pose, last_t = (x, y, yaw), t
    pose = {
        "x": float(x),
        "y": float(y),
        "yaw": math.degrees(yaw),
        "tags": used,
        "err": err,
    }
    logbook.write("frame", ok=True, pose=pose, **rec)
    web.publish(frame, {"ok": True, **info, **pose})
    Bridge.notify("pose", float(x), float(y), float(yaw), len(used))
    summary(t, perf + f" x={x:.2f} y={y:.2f} yaw={math.degrees(yaw):.0f}")


logbook.write(
    "start",
    TARGET_FPS=TARGET_FPS,
    MODES=MODES,
    CAM_PITCH=CAM_PITCH,
    EXPOSURE=EXPOSURE,
    K_CAL=K_CAL,
    D=D,
    TAG_SIZE=TAG_SIZE,
    MAX_ERR_PX=MAX_ERR_PX,
    MAX_DIST=MAX_DIST,
    CAM=[CAM_X, CAM_Y, CAM_Z, CAM_YAW],
    TAGS=TAGS,
)
print(f"log file: {logbook.PATH}")
web.start()
App.run(user_loop=loop)
