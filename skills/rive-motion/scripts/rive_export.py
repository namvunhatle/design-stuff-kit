#!/usr/bin/env python3
"""Export the open Rive artboard's animations and state machines to JSON, read-only.

The motion lint and the motion critic read this file instead of the build script,
so they check what is really in the Rive file, not what was meant.

Usage: python3 rive_export.py --out motion/<feature>/timeline.json [--artboard NAME]

Needs the Rive desktop editor (Early Access) open with the file, and its local MCP
server at http://127.0.0.1:9791/mcp. Only read tools are called.
"""
import argparse, datetime, json, sys, urllib.request

URL = "http://127.0.0.1:9791/mcp"
_sid = None
_n = [1]


def _post(body):
    global _sid
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST", headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        **({"mcp-session-id": _sid} if _sid else {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        _sid = r.headers.get("mcp-session-id") or _sid
        raw = r.read().decode()
    if not raw.strip():
        return None
    if raw.lstrip().startswith("{"):
        return json.loads(raw)
    data = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")]  # SSE reply
    return json.loads(data[-1]) if data else None


def connect():
    try:
        _post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "rive_export", "version": "1"}}})
    except OSError as e:
        sys.exit(f"Rive MCP is not reachable at {URL} ({e}). Open the Rive desktop editor with the file.")
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"})


def call(tool, args):
    _n[0] += 1
    j = _post({"jsonrpc": "2.0", "id": _n[0], "method": "tools/call", "params": {"name": tool, "arguments": args}})
    if not j or "error" in j:
        sys.exit(f"{tool} failed: {(j or {}).get('error')}")
    res = j["result"]
    c = (res.get("structuredContent") or {}).get("content") or res["content"][0]["text"]
    out = json.loads(c) if isinstance(c, str) else c
    if isinstance(out, dict) and out.get("success") is False:
        sys.exit(f"{tool} failed: {str(out)[:300]}")
    return out


def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--artboard", help="expected artboard name; stops if a different one is active")
    a = ap.parse_args()
    connect()

    session = call("session_info", {})
    boards = call("list_artboards", {})["artboards"]
    active = next((b for b in boards if b.get("isActive")), boards[0])
    if a.artboard and active["name"] != a.artboard:
        sys.exit(f"Active artboard is '{active['name']}', not '{a.artboard}'. Select it in the editor and run again.")

    anims = call("animation_editor", {"command": "listLinearAnimations", "data": {}})["linearAnimations"]
    ids = [x["id"] for x in anims]
    props = {}
    for part in chunks(ids, 40):
        props.update(call("query_property_values", {"propertyKeys": {i: [56, 57, 59] for i in part}})["values"])
    keys = {}
    for part in chunks(ids, 4):
        keys.update(call("animation_editor", {"command": "queryKeyFrames",
                                              "data": {"queryKeyFrames": {"animationIds": part}}})["keyframes"])

    machines = []
    for sm in call("animation_editor", {"command": "listStateMachines", "data": {}})["stateMachines"]:
        machines.append(call("animation_editor", {"command": "queryStateMachine",
                                                  "data": {"queryStateMachine": {"stateMachineId": sm["id"]}}}))

    obj_ids = sorted({k["objectId"] for ks in keys.values() for k in ks} |
                     {l["targetId"] for m in machines for l in m.get("listeners", []) if l.get("targetId")})
    objects = {}
    for part in chunks(obj_ids, 50):
        for o in call("query_objects", {"objectIds": part, "depth": 0})["objects"]:
            objects[o["id"]] = {"name": o.get("name") or o["id"], "types": o.get("types", [])}

    out = {"source": "rive", "file": session.get("activeFileName"), "artboard": active["name"],
           "exportedAt": datetime.datetime.now().isoformat(timespec="seconds"),
           "objects": objects, "animations": [], "stateMachines": machines}
    for x in anims:
        p = props.get(x["id"], {})
        tracks = {}
        for k in keys.get(x["id"], []):
            t = tracks.setdefault((k["objectId"], k["propertyKey"]), {
                "objectId": k["objectId"], "prop": k.get("propertyName", str(k["propertyKey"])),
                "propKey": k["propertyKey"], "keys": []})
            t["keys"].append([k["frame"], k["value"], k.get("interpolationType", "linear"), k.get("cubicParams")])
        for t in tracks.values():
            t["keys"].sort(key=lambda r: r[0])
        out["animations"].append({"id": x["id"], "name": x["name"], "fps": p.get("56", 60),
                                  "frames": p.get("57"), "loop": p.get("59", 0), "tracks": list(tracks.values())})

    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    n = sum(len(t["keys"]) for an in out["animations"] for t in an["tracks"])
    print(f"Exported {len(anims)} animations ({n} keys), {len(machines)} state machine(s) "
          f"from '{out['file']}' / {active['name']} to {a.out}")


if __name__ == "__main__":
    main()
