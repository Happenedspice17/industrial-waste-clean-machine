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
            self._send(
                200, "application/json", json.dumps(s, default=logbook._conv).encode()
            )
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
</style>
</head>
<body>
<main>
  <header><h1>AprilTag Pose</h1><span id="st" class="pill">…</span><span id="meta" class="meta"></span>
    <a class="meta" href="/log" target="_blank">log</a><a class="meta" href="/log.jsonl" download="run.jsonl">download</a></header>
  <section class="card" id="camcard" hidden><img id="cam" alt="camera"></section>
  <section class="card">
    <canvas id="map"></canvas>
    <div class="nums">
      <div><b id="x">–</b><span>x (m)</span></div>
      <div><b id="y">–</b><span>y (m)</span></div>
      <div><b id="yaw">–</b><span>yaw (°)</span></div>
    </div>
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
  else if (!s.ok) { txt = "NO POSE"; col = css("--warn"); }
  else { txt = "OK"; col = css("--ok"); }
  $("st").textContent = txt; $("st").style.background = col;
  const perf = s && s.w ? `${s.w}×${s.h} · cam ${s.cam_fps} fps · proc ${s.fps} fps · ${s.ms} ms` : "";
  const tags = s && s.ok ? ` · tags ${s.tags.join(", ")} · err ${s.err.toFixed(2)} px`
    : s && s.reason ? ` · ${s.reason}` : "";
  $("meta").textContent = perf + tags;
}

function draw(s) {
  const c = $("map"), r = c.getBoundingClientRect(), dpr = devicePixelRatio || 1;
  c.width = r.width * dpr; c.height = r.width * dpr;
  const g = c.getContext("2d"); g.scale(dpr, dpr);
  const W = r.width, tags = (s && s.map) || [];
  const raw = ((s && s.raw) || []).filter(q => Math.abs(q[0]) < 50 && Math.abs(q[1]) < 50);
  if (s) s.raw = raw;
  const pts = tags.map(t => [t.x, t.y]).concat(trail, raw);
  if (!pts.length) return;
  let x0 = Math.min(...pts.map(p => p[0])) - 0.5, x1 = Math.max(...pts.map(p => p[0])) + 0.5;
  let y0 = Math.min(...pts.map(p => p[1])) - 0.5, y1 = Math.max(...pts.map(p => p[1])) + 0.5;
  const k = W / Math.max(x1 - x0, y1 - y0);
  const P = (x, y) => [(x - x0) * k, W - (y - y0) * k];
  g.strokeStyle = css("--line"); g.lineWidth = 1;
  for (let v = Math.ceil(x0); v <= x1; v++) { const [a] = P(v, 0); g.beginPath(); g.moveTo(a, 0); g.lineTo(a, W); g.stroke(); }
  for (let v = Math.ceil(y0); v <= y1; v++) { const [, b] = P(0, v); g.beginPath(); g.moveTo(0, b); g.lineTo(W, b); g.stroke(); }
  g.font = "12px system-ui";
  for (const t of tags) {
    const a = t.yaw * Math.PI / 180, h = 0.15, [px, py] = P(t.x, t.y);
    const [ax, ay] = P(t.x - Math.sin(a) * h, t.y + Math.cos(a) * h);
    const [bx, by] = P(t.x + Math.sin(a) * h, t.y - Math.cos(a) * h);
    const [nx, ny] = P(t.x + Math.cos(a) * 0.25, t.y + Math.sin(a) * 0.25);
    g.strokeStyle = css("--tag"); g.lineWidth = 4;
    g.beginPath(); g.moveTo(ax, ay); g.lineTo(bx, by); g.stroke();
    g.lineWidth = 1.5; g.beginPath(); g.moveTo(px, py); g.lineTo(nx, ny); g.stroke();
    g.fillStyle = css("--fg"); g.fillText(`#${t.id}`, px + 6, py - 6);
  }
  for (const q of (s && s.raw) || []) {
    const [a, b] = P(q[0], q[1]);
    g.fillStyle = css("--mut"); g.beginPath(); g.arc(a, b, 4, 0, 7); g.fill();
  }
  if (trail.length > 1) {
    g.strokeStyle = css("--bot"); g.globalAlpha = 0.4; g.lineWidth = 2; g.beginPath();
    trail.forEach((p, i) => { const [a, b] = P(p[0], p[1]); i ? g.lineTo(a, b) : g.moveTo(a, b); });
    g.stroke(); g.globalAlpha = 1;
  }
  if (last) {
    const [rx, ry] = P(last.x, last.y), a = -last.yaw * Math.PI / 180, L = 14;
    g.save(); g.translate(rx, ry); g.rotate(a);
    g.fillStyle = s && s.ok && s.age <= 1 ? css("--bot") : css("--mut");
    g.beginPath(); g.moveTo(L, 0); g.lineTo(-L * 0.7, L * 0.6); g.lineTo(-L * 0.7, -L * 0.6); g.closePath(); g.fill();
    g.restore();
  }
}

async function tick() {
  let s = null;
  try { s = await (await fetch("/pose", { cache: "no-store" })).json(); } catch (e) {}
  if (s && s.ok) {
    last = s;
    trail.push([s.x, s.y]); if (trail.length > 200) trail.shift();
    $("x").textContent = s.x.toFixed(2); $("y").textContent = s.y.toFixed(2); $("yaw").textContent = s.yaw.toFixed(1);
  }
  status(s); draw(s);
  if (s && s.stream && $("camcard").hidden) { $("camcard").hidden = false; frame(); }
}

function frame() {
  const im = new Image();
  im.onload = () => { $("cam").src = im.src; setTimeout(frame, 150); };
  im.onerror = () => setTimeout(frame, 1000);
  im.src = "/frame.jpg?t=" + Date.now();
}

setInterval(tick, 200); tick();
</script>
</body>
</html>
"""
