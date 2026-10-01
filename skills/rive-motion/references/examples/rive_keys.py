"""Generate Rive keyframes from Python through the local Rive MCP (HTTP).

Why: hand-typed keyframes drift, and loops need hundreds of sampled keys.
Copy to a scratch folder, keep object ids in a JSON file, and build each
animation from a script you can re-run (wipe, then add).

Proven on the R1 name-card build (2026-10-01). Units: scale and opacity in
percent, rotation in degrees, x/y in artboard pixels.
"""
import json, math, subprocess

URL = "http://127.0.0.1:9791/mcp"
H = ['-H', 'Content-Type: application/json', '-H', 'Accept: application/json, text/event-stream']
_n = [100]

def _curl(body, sid=None, head=False):
    cmd = ['curl', '-si' if head else '-s', URL] + H + (['-H', 'mcp-session-id: ' + sid] if sid else []) + ['-d', json.dumps(body)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

_r = _curl({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "rive_keys", "version": "1"}}}, head=True)
_sid = next((l.split(':', 1)[1].strip() for l in _r.splitlines() if l.lower().startswith('mcp-session-id:')), None)
_curl({"jsonrpc": "2.0", "method": "notifications/initialized"}, _sid)

def call(tool, args):
    _n[0] += 1
    raw = _curl({"jsonrpc": "2.0", "id": _n[0], "method": "tools/call", "params": {"name": tool, "arguments": args}}, _sid)
    try:
        j = json.loads(raw[raw.index('{'):])
        c = (j['result'].get('structuredContent') or {}).get('content') or j['result']['content'][0]['text']
        try: return json.loads(c)
        except Exception: return c
    except Exception:
        return {'raw': raw[:400]}

# property keys
X, Y, ROT, SX, SY, OP = 13, 14, 15, 16, 17, 18
# eases (cubic x1,y1,x2,y2); cubic cannot overshoot, so key peaks explicitly
IO   = dict(interpolationType='cubic', cubicParams=dict(x1=.45, y1=0, x2=.55, y2=1))
OUT  = dict(interpolationType='cubic', cubicParams=dict(x1=.25, y1=.46, x2=.45, y2=.94))
DEC  = dict(interpolationType='cubic', cubicParams=dict(x1=.2, y1=.6, x2=.35, y2=1))
ACC  = dict(interpolationType='cubic', cubicParams=dict(x1=.5, y1=0, x2=.9, y2=.6))
LIN  = dict(interpolationType='linear')
HOLD = dict(interpolationType='hold')

def S(obj, key, pts, eases=None, ease=IO, out=None):
    """Append keys for (frame, value) pairs. The ease of key i drives the segment after it."""
    for i, (f, v) in enumerate(pts):
        d = HOLD if i == len(pts) - 1 else (eases[i] if eases else ease)
        out.append(dict(objectId=obj, propertyKey=key, frame=f, value=round(v, 2) if isinstance(v, float) else v, **d))
    return out

def keys(anim):
    return call('animation_editor', {"command": "queryKeyFrames", "data": {"queryKeyFrames": {"animationIds": [anim]}}})['keyframes'][anim]

def mod(anim, add=None, delete=None, change=None):
    """Batched modifyKeyFrames: deletes in 80s, adds/changes in 70s."""
    for i in range(0, len(delete or []), 80):
        call('animation_editor', {"command": "modifyKeyFrames", "data": {"modifyKeyFrames": {"animationId": anim, "delete": delete[i:i + 80]}}})
    for name, items in (('add', add), ('change', change)):
        for i in range(0, len(items or []), 70):
            r = call('animation_editor', {"command": "modifyKeyFrames", "data": {"modifyKeyFrames": {"animationId": anim, name: items[i:i + 70]}}})
            if not (isinstance(r, dict) and r.get('success')): print('ERR', anim, str(r)[:200])

def wipe(anim, only=None):
    """Delete all keys (or only those on the given object ids) before rebuilding."""
    mod(anim, delete=[k['keyframeId'] for k in keys(anim) if only is None or k['objectId'] in only])

def periodic(obj, key, fn, N, step=8, out=None):
    """Seamless loop: fn(u) with u in [0,1); use whole-number harmonics of 2*pi*u."""
    return S(obj, key, [(f, fn(f / N)) for f in range(0, N + 1, step)], ease=LIN, out=out)

# example: a feathered blob that breathes twice and drifts once per 24 s loop
# k = []
# periodic(blob, SX, lambda u: 100 + 8 * math.sin(2 * math.pi * 2 * u), 1440, out=k)
# periodic(blob, X,  lambda u: 180 + 30 * math.sin(2 * math.pi * u),     1440, out=k)
# mod(anim_id, add=k); call('set_property_values', {"propertyValues": {anim_id: {"57": 1440, "59": 1}}})
