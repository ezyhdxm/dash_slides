"""Start every demo app at once, each on its own port, for the slides' "Live app" buttons.

Run before the talk, from the repo root or from demos/:
    python demos/run_all.py
Leave it running; press Ctrl+C to stop all the apps.

    slide 5   02_hello_dash.py   http://127.0.0.1:8052
    slide 7   03_widgets.py      http://127.0.0.1:8053
    slide 8   04_callback.py     http://127.0.0.1:8054
    slide 10  05_click_detail.py  http://127.0.0.1:8055
"""
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEMOS = [("02_hello_dash.py", 8052), ("03_widgets.py", 8053), ("04_callback.py", 8054), ("05_click_detail.py", 8055)]
WINDOWS = os.name == "nt"


def port_busy(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def ready(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/_dash-layout", timeout=1) as r:
            return r.status == 200
    except OSError:
        return False


def stop(procs):
    for p in procs:
        if p.poll() is not None:
            continue
        if WINDOWS:     # the debug reloader starts a child process: stop the whole tree
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
        else:
            os.killpg(p.pid, signal.SIGTERM)


def main():
    busy = [port for _, port in DEMOS if port_busy(port)]
    if busy:
        sys.exit(f"Port(s) {busy} already in use. Stop whatever is using them (an earlier run_all.py?) and retry.")
    procs = []
    for script, port in DEMOS:
        log = open(HERE / f".{Path(script).stem}.log", "w")
        kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if WINDOWS else {"start_new_session": True}
        procs.append(subprocess.Popen([sys.executable, script], cwd=HERE, stdout=log, stderr=subprocess.STDOUT,
                                      env={**os.environ, "PORT": str(port), "PYTHONUNBUFFERED": "1"}, **kw))
    try:
        deadline = time.time() + 90
        waiting = dict(DEMOS)
        while waiting and time.time() < deadline:
            for script, port in list(waiting.items()):
                if ready(port):
                    del waiting[script]
            time.sleep(0.5)
        print()
        for script, port in DEMOS:
            ok = script not in waiting
            print(f"  {'ready ' if ok else 'FAILED'}  {script:<20} http://127.0.0.1:{port}")
            if not ok:
                print(f"          see demos/.{Path(script).stem}.log")
        print("\nOpen slides/index.html. Leave this window open; Ctrl+C stops all the apps.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stop(procs)
        print("\nstopped")


if __name__ == "__main__":
    main()
