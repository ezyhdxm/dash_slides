"""Check a Dash app without opening a browser: it loads, its callbacks fit its layout, and every callback runs once.

Usage:  python check_app.py path/to/app.py [more apps...]

For each app it
  1. imports the file (the `if __name__ == "__main__":` block does not run, so no server starts)
  2. asks the app, through Flask's test client, for its layout and its callbacks, as the browser would
  3. checks that every Input, State and Output id exists in the layout (pattern-matching ids are skipped)
  4. calls each callback once with the layout's starting values, as the page load does, and reports errors
  5. prints the wiring: Input(id.prop) -> Output(id.prop)
Exit code 0 when every app passes, 1 otherwise. Step 4 skips callbacks with prevent_initial_call, and ids or
props missing from the starting layout (made by other callbacks), so it can miss errors; still run the app.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path


def load(path):
    path = Path(path).resolve()
    sys.path.insert(0, str(path.parent))                 # so the app's own imports (data.py ...) work
    spec = importlib.util.spec_from_file_location(f"_checked_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    from dash import Dash
    apps = [v for v in vars(mod).values() if isinstance(v, Dash)]
    if not apps:
        raise LookupError("no Dash app found at module level (expected app = Dash(__name__))")
    return apps[0]


def walk(node, found):
    """Collect {id: {prop: value}} from the layout JSON."""
    if isinstance(node, dict):
        props = node.get("props")
        if isinstance(props, dict) and "type" in node:
            cid = props.get("id")
            if isinstance(cid, str):
                found[cid] = props
            for v in props.values():
                walk(v, found)
        else:
            for v in node.values():
                walk(v, found)
    elif isinstance(node, list):
        for v in node:
            walk(v, found)


def parse_outputs(s):
    """'..a.figure...b.children..' or 'a.figure' -> [('a', 'figure'), ('b', 'children')]."""
    parts = s.strip(".").split("...") if s.startswith("..") else [s]
    return [tuple(p.rsplit(".", 1)) for p in parts]


def check(path):
    app = load(path)
    app.server.testing = True                        # a callback's exception reaches us instead of a bare 500
    client = app.server.test_client()
    layout = client.get("/_dash-layout")
    if layout.status_code != 200:
        return [f"layout request failed ({layout.status_code})"], []
    ids = {}
    walk(layout.get_json(), ids)
    deps = client.get("/_dash-dependencies").get_json()
    problems, wiring = [], []
    for cb in deps:
        if cb["output"].startswith("{") or any(isinstance(d["id"], str) and d["id"].startswith("{")
                                               for d in cb["inputs"] + cb["state"]):
            wiring.append("(pattern-matching callback, not checked)")
            continue
        outs = parse_outputs(cb["output"])
        ins = [(d["id"], d["property"]) for d in cb["inputs"]]
        sts = [(d["id"], d["property"]) for d in cb["state"]]
        for cid, prop in ins + sts + outs:
            if cid not in ids:
                problems.append(f"id '{cid}' (used as {cid}.{prop}) is not in the layout")
        wiring.append(", ".join(f"Input({i}.{p})" for i, p in ins)
                      + "".join(f", State({i}.{p})" for i, p in sts)
                      + " -> " + ", ".join(f"Output({i}.{p})" for i, p in outs))
        if cb.get("prevent_initial_call") or any(i not in ids for i, _ in ins + sts + outs):
            continue
        body = {"output": cb["output"],
                "outputs": [{"id": i, "property": p} for i, p in outs] if len(outs) > 1 or cb["output"].startswith("..")
                else {"id": outs[0][0], "property": outs[0][1]},
                "inputs": [{"id": i, "property": p, "value": ids[i].get(p)} for i, p in ins],
                "state": [{"id": i, "property": p, "value": ids[i].get(p)} for i, p in sts],
                "changedPropIds": []}
        try:
            r = client.post("/_dash-update-component", json=body)
            if r.status_code not in (200, 204):
                problems.append(f"callback {wiring[-1]} failed on page load (HTTP {r.status_code})")
        except Exception as e:
            lines = [ln.strip() for ln in str(e).splitlines() if ln.strip()]
            problems.append(f"callback {wiring[-1]} raised on page load: {type(e).__name__}: "
                            + " ".join(lines[:3])[:300])
    return problems, wiring


def main(paths):
    if len(paths) > 1:                               # one process per app: callbacks registered with the
        codes = [subprocess.run([sys.executable, __file__, p]).returncode for p in paths]   # global @callback
        return 0 if not any(codes) else 1            # would otherwise pile up across apps
    ok = True
    for p in paths:
        try:
            problems, wiring = check(p)
        except Exception as e:                       # an import error, a syntax error ...
            problems, wiring = [f"{type(e).__name__}: {e}"], []
        print(f"{'PASS' if not problems else 'FAIL'}  {p}")
        for w in wiring:
            print(f"      {w}")
        for m in problems:
            print(f"  !!  {m}")
        ok &= not problems
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1:]))
