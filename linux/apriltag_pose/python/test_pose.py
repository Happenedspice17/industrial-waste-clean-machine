"""Unit tests for the AprilTag bench pose app (SR-018, SR-019, SR-020, SR-021).

Simulation only: tags are drawn synthetically and warped into the image; no physical camera.
Skipped when OpenCV/numpy are not installed (CI installs only the tool dependencies).
"""

import math
import pathlib
import sys
import types

import pytest

cv2 = pytest.importorskip("cv2")
np = pytest.importorskip("numpy")

HERE = pathlib.Path(__file__).parent


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("APRILTAG_LOG_DIR", str(tmp_path))
    monkeypatch.syspath_prepend(str(HERE))
    for name in ("logbook", "web"):
        sys.modules.pop(name, None)
    sent = []
    stub = types.ModuleType("arduino.app_utils")
    stub.App = None
    stub.Bridge = types.SimpleNamespace(notify=lambda *a: sent.append(a))
    monkeypatch.setitem(sys.modules, "arduino", types.ModuleType("arduino"))
    monkeypatch.setitem(sys.modules, "arduino.app_utils", stub)
    src = (HERE / "main.py").read_text().replace("web.start()", "").replace("App.run(user_loop=loop)", "")
    g = {"__name__": "apriltag_main"}
    exec(compile(src, "main.py", "exec"), g)  # noqa: S102  load the App Lab script without starting it
    g["sent"] = sent
    g["set_res"](640, 480)
    return g


def render(g, x, y, yaw_deg, *, tags=None, mount=None):
    """Grey image of the tags seen by a camera on a robot at (x, y, yaw)."""
    a = math.radians(yaw_deg)
    rot = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    T_wr = g["tf"](rot, [x, y, 0])
    T_cw = np.linalg.inv(T_wr @ (mount if mount is not None else g["T_RC"]))
    img = np.full((480, 640), 255, np.uint8)
    for tid, T_wt in (tags or g["T_WT"]).items():
        T_ct = T_cw @ T_wt
        if T_ct[2, 3] <= 0.1:
            continue
        mk = cv2.aruco.generateImageMarker(g["det"].getDictionary(), tid, 200, borderBits=1)
        mk = cv2.copyMakeBorder(mk, 25, 25, 25, 25, cv2.BORDER_CONSTANT, value=255)
        k = g["TAG_SIZE"] * 250 / 200 / 2
        pts = np.array([[-k, k, 0], [k, k, 0], [k, -k, 0], [-k, -k, 0]])
        ip, _ = cv2.projectPoints(pts, cv2.Rodrigues(T_ct[:3, :3])[0], T_ct[:3, 3], g["K"], g["D"])
        H = cv2.getPerspectiveTransform(
            np.float32([[0, 0], [250, 0], [250, 250], [0, 250]]), np.float32(ip.reshape(4, 2))
        )
        warped = cv2.warpPerspective(mk, H, (640, 480), borderValue=255)
        mask = cv2.warpPerspective(np.full_like(mk, 255), H, (640, 480))
        img[mask > 0] = warped[mask > 0]
    return img


def test_jacobian_matches_numeric_sr018(app):
    rng = np.random.default_rng(0)
    pts = rng.random((8, 3)) * [1, 2, 0.6]
    p = np.array([2.0, 1.0, 3.0])
    r, J = app["resjac"](p, pts, np.zeros(16))
    num = np.column_stack([(app["resjac"](p + e, pts, np.zeros(16))[0] - r) / 1e-6 for e in np.eye(3) * 1e-6])
    assert np.abs(J - num).max() < 1e-4


def test_pose_recovered_from_one_tag_sr018(app):
    est, diag = app["estimate"](render(app, 0.75, -0.30, 170))
    assert diag["reason"] == "ok"
    x, y, yaw, used, err = est
    assert math.hypot(x - 0.75, y + 0.30) < 0.10
    assert abs((math.degrees(yaw) - 170 + 180) % 360 - 180) < 5
    assert used == [0] and err <= app["MAX_ERR_PX"]


def test_unknown_tag_gives_no_pose_sr018(app):
    img = render(app, 0.75, -0.30, 170)
    app["T_WT"].pop(0)
    est, diag = app["estimate"](img)
    assert est is None and diag["reason"].startswith("unknown_ids")


def test_wrong_tag_map_is_reported_sr018(app):
    real = {0: app["world_tag"](0, 0, 0.55, 0), 1: app["world_tag"](0, -0.41, 0.55, 0)}
    img = render(app, 1.0, -0.2, 180, tags=real)
    app["T_WT"].update({0: real[0], 1: app["world_tag"](0, 1.5, 0.55, 0)})
    est, diag = app["estimate"](img)
    assert est is None and diag["reason"].startswith("tags_disagree")


def test_calibration_recovers_mount_sr021(app):
    true_mount = app["T_RC"].copy()
    true_mount[2, 3] = 0.45  # camera really at 0.45 m while CAM_Z says otherwise
    img = render(app, 0.75, -0.30, 170, mount=true_mount)
    app["calib_start"]()
    t0 = app["calib"]["t0"]
    for i in range(30):
        _, diag = app["estimate"](img)
        app["calib_step"](t0 + i * 0.1, diag)
    view = app["calib_view"]()
    assert view["state"] == "done"
    assert abs(view["cam_z"] - 0.45) < 0.02
    assert app["calib_apply"]()["ok"] and app["CAM_Z"] == view["cam_z"]


def test_stream_off_keeps_no_frame_sr020(app):
    web = sys.modules["web"]
    assert web.STREAM is False
    web.publish(np.zeros((4, 4, 3), np.uint8), {"ok": False, "t": 0.0})
    assert web._frame is None


def test_log_has_no_images_sr019(app, tmp_path):
    _, diag = app["estimate"](render(app, 0.75, -0.30, 170))
    sys.modules["logbook"].write("frame", ok=True, **diag)
    text = (tmp_path / "run.jsonl").read_text()
    assert '"kind":"frame"' in text and len(text) < 5000
