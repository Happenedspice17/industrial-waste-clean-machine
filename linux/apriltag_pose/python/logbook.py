import json
import os
import threading
import time
from collections import deque

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
PATH = os.path.join(DIR, "run.jsonl")
MAX_BYTES = 20_000_000

_lock = threading.Lock()
tail = deque(maxlen=300)
os.makedirs(DIR, exist_ok=True)
_f = open(PATH, "a", buffering=1)  # noqa: SIM115  kept open for the whole run


def _conv(o):
    if hasattr(o, "tolist"):
        return o.tolist()
    return str(o)


def write(kind, **rec):
    global _f
    rec = {
        "t": round(time.monotonic(), 4),
        "wall": time.strftime("%H:%M:%S"),
        "kind": kind,
        **rec,
    }
    line = json.dumps(rec, default=_conv, separators=(",", ":"))
    with _lock:
        _f.write(line + "\n")
        tail.append(line)
        if _f.tell() > MAX_BYTES:
            _f.close()
            os.replace(PATH, PATH + ".1")
            _f = open(PATH, "a", buffering=1)  # noqa: SIM115
