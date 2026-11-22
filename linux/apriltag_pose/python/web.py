import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import cv2
import logbook

PORT = 7000
JPEG_Q = 60
# camera image on the page; off = no frame leaves the robot (faces, people)
STREAM = False
_lock = threading.Lock()
_frame = None
_state = {"ok": False, "cam": False, "t": 0.0}
# POST path -> callable returning a dict (registered by main.py)
ACTIONS = {}


def publish(frame, state):
    global _frame
    with _lock:
        _frame = frame if STREAM else None
        _state.clear()
        _state.update(state)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            self._send(200, "text/html; charset=utf-8", PAGE.encode())
        elif path == "/pose":
            with _lock:
                s = dict(_state)
            s["age"] = round(time.monotonic() - s.pop("t"), 3)
            s["stream"] = STREAM
            self._send(200, "application/json", json.dumps(s, default=logbook._conv).encode())
        elif path == "/log":
            with logbook._lock:
                body = "\n".join(logbook.tail) + "\n"
            self._send(200, "text/plain; charset=utf-8", body.encode())
        elif path == "/log.jsonl":
            with logbook._lock, open(logbook.PATH, "rb") as f:
                body = f.read()
            self._send(200, "application/x-ndjson", body)
        elif path == "/frame.jpg":
            if not STREAM:
                self._send(404, "text/plain", b"stream disabled")
                return
            with _lock:
                f = _frame
            if f is None:
                self._send(503, "text/plain", b"no frame")
                return
            _, buf = cv2.imencode(".jpg", f, [cv2.IMWRITE_JPEG_QUALITY, JPEG_Q])
            self._send(200, "image/jpeg", buf.tobytes())
        else:
            self._send(404, "text/plain", b"not found")

    def do_POST(self):
        fn = ACTIONS.get(self.path.split("?")[0])
        if fn is None:
            self._send(404, "text/plain", b"not found")
            return
        self._send(200, "application/json", json.dumps(fn(), default=logbook._conv).encode())

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def start(port=PORT):
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"web on :{port}")


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AprilTag Pose</title>
<style>
:root { --bg:#f6f7f9; --card:#fff; --fg:#1b1f24; --mut:#667085; --line:#d0d5dd;
  --ok:#12b76a; --warn:#f79009; --bad:#f04438; --tag:#2e90fa; --bot:#7a5af8; }
@media (prefers-color-scheme: dark) { :root { --bg:#0f1115; --card:#181b21; --fg:#e6e8eb;
  --mut:#98a2b3; --line:#2b313b; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.4 system-ui,sans-serif; }
main { max-width:1100px; margin:0 auto; padding:16px; display:grid; gap:16px;
  grid-template-columns:1fr; }
@media (min-width:860px) { main { grid-template-columns:1fr 1fr; } }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px; }
h1 { font-size:18px; margin:0; }
header { display:flex; align-items:center; gap:12px; flex-wrap:wrap; grid-column:1/-1; }
.pill { padding:3px 10px; border-radius:999px; font-weight:600; font-size:13px; color:#fff; }
.nums { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-top:10px; }
.nums div { text-align:center; } .nums b { display:block; font-size:22px; font-variant-numeric:tabular-nums; }
.nums span, .meta { color:var(--mut); font-size:13px; }
img, canvas { width:100%; display:block; border-radius:8px; background:#000; }
canvas { background:transparent; aspect-ratio:1/1; }
button { font:inherit; padding:6px 12px; border-radius:8px; border:1px solid var(--line);
  background:var(--card); color:var(--fg); cursor:pointer; }
.legend { display:flex; flex-wrap:wrap; gap:6px 14px; margin-top:8px; color:var(--mut); font-size:12px; }
.legend i { display:inline-block; width:12px; height:12px; margin-right:5px; vertical-align:-2px; border-radius:2px; }
</style>
</head>
<body>
<main>
  <header><h1>AprilTag Pose</h1><span id="st" class="pill">…</span><span id="meta" class="meta"></span>
    <a class="meta" href="/log" target="_blank">log</a><a class="meta" href="/log.jsonl" download="run.jsonl">download</a></header>
  <section class="card" id="camcard" hidden><img id="cam" alt="camera"></section>
  <section class="card">
    <canvas id="map"></canvas>
    <div class="legend">
      <span><i style="background:var(--bot)"></i>robot (validated pose)</span>
      <span><i style="border:2px dashed var(--warn)"></i>robot (test estimate)</span>
      <span><i style="background:var(--mut);border-radius:50%"></i>where each tag alone puts it</span>
      <span><i style="background:var(--tag)"></i>tag (line = facing)</span>
      <span><i style="background:var(--bot);opacity:.15"></i>camera view</span>
    </div>
    <div class="nums">
      <div><b id="x">–</b><span>x (m)</span></div>
      <div><b id="y">–</b><span>y (m)</span></div>
      <div><b id="yaw">–</b><span>yaw (°)</span></div>
    </div>
  </section>
  <section class="card" style="grid-column:1/-1">
    <h2 style="font-size:15px;margin:0 0 6px">Camera mount</h2>
    <div class="meta" id="mount"></div>
    <p class="meta" style="margin:6px 0">Hold the camera still, at its real height, with a tag in view, then press
      Calibrate (takes 2 s). Values are relative to the tag heights in TAGS.</p>
    <button id="cal">Calibrate mount</button> <button id="apply" hidden>Apply (this session only)</button>
    <pre id="calout" class="meta" style="white-space:pre-wrap;margin:8px 0 0"></pre>
  </section>
</main>
<script>
const $ = id => document.getElementById(id);
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const trail = [];
let last = null;

function status(s) {
  let txt, col;
  if (!s) { txt = "OFFLINE"; col = css("--bad"); }
  else if (!s.cam) { txt = "NO CAMERA"; col = css("--bad"); }
  else if (s.age > 1) { txt = "STALE"; col = css("--bad"); }
  else if (s.ok) { txt = "OK"; col = css("--ok"); }
  else if (s.test) { txt = "TEST ESTIMATE"; col = css("--warn"); }
  else { txt = "NO POSE"; col = css("--warn"); }
  $("st").textContent = txt; $("st").style.background = col;
  const perf = s && s.w ? `${s.w}x${s.h} · cam ${s.cam_fps} fps · proc ${s.fps} fps · ${s.ms} ms` : "";
  let why = "";
  if (s && s.ok) why = ` · tags ${s.tags.join(", ")} · err ${s.err.toFixed(2)} px`;
  else if (s && s.test) why = ` · from tag #${s.tags[0]} only, not validated · ${s.reason}`;
  else if (s && s.reason) why = ` · ${s.reason}`;
  $("meta").textContent = perf + why;
}

function line(g, a, b, color, width, dash) {
  g.strokeStyle = color; g.lineWidth = width; g.setLineDash(dash || []);
  g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke(); g.setLineDash([]);
}

function draw(s) {
  const c = $("map"), r = c.getBoundingClientRect(), dpr = devicePixelRatio || 1;
  c.width = r.width * dpr; c.height = r.width * dpr;
  const g = c.getContext("2d"); g.scale(dpr, dpr);
  const W = r.width, tags = (s && s.map) || [];
  const views = ((s && s.views) || []).filter(v => Math.abs(v.x) < 50 && Math.abs(v.y) < 50);
  const pts = tags.map(t => [t.x, t.y]).concat(trail, views.map(v => [v.x, v.y]), [[0, 0]]);
  if (last) pts.push([last.x, last.y]);
  let x0 = Math.min(...pts.map(p => p[0])) - 0.6, x1 = Math.max(...pts.map(p => p[0])) + 0.6;
  let y0 = Math.min(...pts.map(p => p[1])) - 0.6, y1 = Math.max(...pts.map(p => p[1])) + 0.6;
  const span = Math.max(x1 - x0, y1 - y0), k = W / span;
  const P = (x, y) => [(x - x0) * k, W - (y - y0) * k];
  const step = span > 8 ? 2 : span > 3 ? 1 : 0.5;
  g.font = "11px system-ui"; g.fillStyle = css("--mut");
  for (let v = Math.ceil(x0 / step) * step; v <= x1; v += step) {
    const [a] = P(v, 0); line(g, [a, 0], [a, W], css("--line"), v === 0 ? 2 : 1);
    g.fillText(`${+v.toFixed(1)}`, a + 3, W - 4);
  }
  for (let v = Math.ceil(y0 / step) * step; v <= y1; v += step) {
    const [, b] = P(0, v); line(g, [0, b], [W, b], css("--line"), v === 0 ? 2 : 1);
    g.fillText(`${+v.toFixed(1)}`, 3, b - 3);
  }
  g.fillText("x (m) →", W - 52, W - 16); g.fillText("↑ y (m)", 3, 12);
  const live = s && s.age <= 1 && (s.ok || s.test);
  if (live) {
    const [rx, ry] = P(s.x, s.y), a = s.yaw * Math.PI / 180, f = (s.fov || 60) * Math.PI / 360, R = 1.5;
    g.fillStyle = css("--bot"); g.globalAlpha = 0.12; g.beginPath(); g.moveTo(rx, ry);
    for (let t = -f; t <= f + 1e-6; t += f / 8) { const [px, py] = P(s.x + R * Math.cos(a + t), s.y + R * Math.sin(a + t)); g.lineTo(px, py); }
    g.closePath(); g.fill(); g.globalAlpha = 1;
  }
  g.font = "12px system-ui";
  for (const t of tags) {
    const a = t.yaw * Math.PI / 180, h = 0.15, p = P(t.x, t.y);
    line(g, P(t.x - Math.sin(a) * h, t.y + Math.cos(a) * h), P(t.x + Math.sin(a) * h, t.y - Math.cos(a) * h), css("--tag"), 4);
    line(g, p, P(t.x + Math.cos(a) * 0.3, t.y + Math.sin(a) * 0.3), css("--tag"), 1.5);
    g.fillStyle = css("--fg"); g.fillText(`#${t.id}`, p[0] + 6, p[1] - 6);
  }
  for (const v of views) {
    const t = tags.find(t => t.id === v.id), p = P(v.x, v.y);
    if (t) line(g, p, P(t.x, t.y), css("--mut"), 1, [4, 4]);
    g.fillStyle = css("--mut"); g.beginPath(); g.arc(p[0], p[1], 4, 0, 7); g.fill();
    g.fillText(`#${v.id} ${v.dist.toFixed(2)} m`, p[0] + 6, p[1] + 14);
  }
  if (trail.length > 1) {
    g.strokeStyle = css("--bot"); g.globalAlpha = 0.4; g.lineWidth = 2; g.beginPath();
    trail.forEach((p, i) => { const [a, b] = P(p[0], p[1]); i ? g.lineTo(a, b) : g.moveTo(a, b); });
    g.stroke(); g.globalAlpha = 1;
  }
  if (last) {
    const [rx, ry] = P(last.x, last.y), L = 14;
    if (live) for (const id of last.tags) { const t = tags.find(t => t.id === id); if (t) line(g, [rx, ry], P(t.x, t.y), css("--bot"), 1); }
    g.save(); g.translate(rx, ry); g.rotate(-last.yaw * Math.PI / 180);
    g.beginPath(); g.moveTo(L, 0); g.lineTo(-L * 0.7, L * 0.6); g.lineTo(-L * 0.7, -L * 0.6); g.closePath();
    if (!live) { g.fillStyle = css("--mut"); g.fill(); }
    else if (last.ok) { g.fillStyle = css("--bot"); g.fill(); }
    else { g.setLineDash([3, 3]); g.strokeStyle = css("--warn"); g.lineWidth = 2; g.stroke(); }
    g.restore();
    g.fillStyle = css("--fg");
    g.fillText(`(${last.x.toFixed(2)}, ${last.y.toFixed(2)}) ${last.yaw.toFixed(0)}°`, rx + 12, ry - 10);
  }
}

function mount(s) {
  if (!s || !s.mount) return;
  $("mount").textContent = `current: CAM_Z = ${s.mount.z} m · CAM_PITCH = ${s.mount.pitch}°`;
  const c = s.calib || {};
  let out = "";
  if (c.state === "running") out = "measuring...";
  else if (c.state === "failed") out = "failed: " + c.error;
  else if (c.state === "done" || c.state === "applied")
    out = `measured from ${c.n} tag views (spread z ${c.z_spread} m, pitch ${c.pitch_spread}°)\\n` +
      `paste in python/main.py:\\nCAM_X, CAM_Y, CAM_Z, CAM_YAW = 0.0, 0.0, ${c.cam_z}, 0.0\\nCAM_PITCH = ${c.cam_pitch}` +
      (c.state === "applied" ? "\\n(applied to this session)" : "");
  $("calout").textContent = out;
  $("apply").hidden = c.state !== "done";
}

async function post(path) {
  try { await fetch(path, { method: "POST" }); } catch (e) {}
}

async function tick() {
  let s = null;
  try { s = await (await fetch("/pose", { cache: "no-store" })).json(); } catch (e) {}
  if (s && (s.ok || s.test)) {
    last = s;
    trail.push([s.x, s.y]); if (trail.length > 200) trail.shift();
    $("x").textContent = s.x.toFixed(2); $("y").textContent = s.y.toFixed(2); $("yaw").textContent = s.yaw.toFixed(1);
  }
  status(s); draw(s); mount(s);
  if (s && s.stream && $("camcard").hidden) { $("camcard").hidden = false; frame(); }
}

function frame() {
  const im = new Image();
  im.onload = () => { $("cam").src = im.src; setTimeout(frame, 66); };
  im.onerror = () => setTimeout(frame, 1000);
  im.src = "/frame.jpg?t=" + Date.now();
}

$("cal").onclick = () => post("/calibrate");
$("apply").onclick = () => post("/calibrate/apply");
setInterval(tick, 200); tick();
</script>
</body>
</html>
"""
