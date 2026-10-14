#!/usr/bin/env python3
"""Check a Rive motion export against the kit's motion gates. Measures; never judges taste.

Usage: python3 motion_lint.py timeline.json motion-spec.json [--out lint.md]

timeline.json comes from rive_export.py. motion-spec.json is written with the designer
before building (format: motion-principles §4). Exit code 1 when any gate fails.
Every number in the report comes from the keyframes and the state machine in the file.
"""
import argparse, itertools, json, re, sys
from collections import defaultdict

EPS = 0.01
TRANSFORM = {"x", "y", "rotation", "scaleX", "scaleY"}
DEFAULTS = {"startWindowMs": 100, "maxStartsPerWindow": 2, "settleToleranceMs": 34, "maxOvershoots": 1,
            "responseMs": 100, "budgetMs": 1000, "arcMinPx": 40, "volumeTolerance": 0.10, "maxFlashesPerSecond": 3}


class Lint:
    def __init__(self, tl, spec):
        self.tl, self.spec = tl, spec
        self.th = {**DEFAULTS, **spec.get("thresholds", {})}
        self.obj = {i: o["name"] for i, o in tl["objects"].items()}
        self.types = {i: o.get("types", []) for i, o in tl["objects"].items()}
        self.ambient = set(spec.get("ambient", []))
        self.unit_of = {}
        for label, names in spec.get("groups", {}).items():
            for n in names:
                self.unit_of[n] = label
        self.anims = {a["id"]: a for a in tl["animations"]}
        self.by_name = {a["name"]: a for a in tl["animations"]}
        self.findings = []  # (severity, gate, where, text)

    def add(self, sev, gate, where, text):
        for w in self.spec.get("waivers", []):
            if gate.startswith(w.get("gate", "?") + " ") and w.get("moment") in (None, where):
                sev, text = "waived", f"{text} Waived: {w.get('reason', 'no reason given')}"
        if (sev, gate, where, text) not in self.findings:
            self.findings.append((sev, gate, where, text))

    # ---------- track helpers ----------
    @staticmethod
    def changes(keys):
        """[(start, end)] of every segment where the value changes. A hold key jumps at the next key."""
        out = []
        for (f0, v0, i0, _), (f1, v1, _, _) in zip(keys, keys[1:]):
            if abs(v1 - v0) > EPS:
                out.append((f1, f1) if i0 == "hold" else (f0, f1))
        return out

    def track_info(self, t):
        ch = self.changes(t["keys"])
        if not ch:
            return None
        v0 = t["keys"][0][1]
        amp = max(abs(k[1] - v0) for k in t["keys"])
        peak = max(t["keys"], key=lambda k: abs(k[1] - v0))[0]
        return {"start": ch[0][0], "end": ch[-1][1], "amp": amp, "peak": peak}

    def name(self, t):
        return self.obj.get(t["objectId"], t["objectId"])

    def unit(self, t):
        return self.unit_of.get(self.name(t), self.name(t))

    def ms(self, frames, a):
        return round(frames * 1000 / a["fps"])

    def frames(self, ms, a):
        return ms * a["fps"] / 1000

    def moment(self, a):
        return self.spec.get("moments", {}).get(a["name"], {})

    def moving(self, a):
        """{unit: {'start','end','tracks':[(track, info)]}} for moving tracks; ambient ones count only as the primary."""
        units, primary = {}, self.moment(a).get("primary")
        for t in a["tracks"]:
            if (self.name(t) in self.ambient or self.unit(t) in self.ambient) and primary not in (self.name(t), self.unit(t)):
                continue
            info = self.track_info(t)
            if not info:
                continue
            u = units.setdefault(self.unit(t), {"start": info["start"], "end": info["end"], "tracks": []})
            u["start"], u["end"] = min(u["start"], info["start"]), max(u["end"], info["end"])
            u["tracks"].append((t, info))
        return units

    # ---------- gates on keyframes ----------
    def gate_poses(self):
        if not self.spec.get("posesApproved"):
            self.add("fail", "G0 Pose to pose", "spec",
                     "Key poses are not approved. Show the start, peak, and end poses as stills and record "
                     "`posesApproved` (date) in the spec before tuning timing.")

    def gate_staging(self, a, units):
        w = self.frames(self.th["startWindowMs"], a)
        starts = sorted((u["start"], n) for n, u in units.items())
        worst = []
        for s, _ in starts:
            inside = [n for f, n in starts if s <= f < s + w]
            if len(inside) > len(worst):
                worst = inside
        if len(worst) > self.th["maxStartsPerWindow"]:
            detail = ", ".join(f"{n} f{units[n]['start']}" for n in worst)
            self.add("fail", "G1 Staging", a["name"],
                     f"{len(worst)} things start moving within {self.th['startWindowMs']} ms (max "
                     f"{self.th['maxStartsPerWindow']}): {detail}. Sequence them cause → effect, or declare "
                     "parts of one motion as a group in the spec.")

    def gate_settle(self, a, units):
        p = self.moment(a).get("primary")
        if not p:
            self.add("warn", "G2 Settle", a["name"], "No `primary` declared for this moment; settle check skipped.")
            return
        if p not in units:
            self.add("fail", "G2 Settle", a["name"], f"Declared primary '{p}' does not move in this animation.")
            return
        stop = units[p]["end"] + self.frames(self.th["settleToleranceMs"], a)
        late = [(n, u["end"]) for n, u in units.items() if n != p and u["end"] > stop]
        if late:
            detail = ", ".join(f"{n} until f{e} ({self.ms(e, a)} ms)" for n, e in late)
            self.add("fail", "G2 Settle", a["name"],
                     f"{p} settles at f{units[p]['end']} ({self.ms(units[p]['end'], a)} ms) but {detail} keeps "
                     "moving. Nothing moves after the primary settles.")

    def gate_overshoot(self, a, units):
        osc = set(self.moment(a).get("oscillate", []))
        for n, u in units.items():
            for t, _ in u["tracks"]:
                if t["prop"] not in TRANSFORM or f"{self.name(t)}.{t['prop']}" in osc or self.name(t) in osc:
                    continue
                final = t["keys"][-1][1]
                signs = [1 if k[1] - final > EPS else -1 for k in t["keys"] if abs(k[1] - final) > EPS]
                flips = sum(1 for x, y in zip(signs, signs[1:]) if x != y)
                if flips > self.th["maxOvershoots"]:
                    vals = " → ".join(f"{k[1]:g}" for k in t["keys"])
                    self.add("fail", "G3 Overshoot", a["name"],
                             f"{self.name(t)}.{t['prop']} crosses its rest value {flips} times ({vals}); "
                             f"max {self.th['maxOvershoots']}. Declare it in `oscillate` if it is a shake.")
                if any("elastic" in str(k[2]) or "bounce" in str(k[2]) for k in t["keys"]):
                    self.add("warn", "G3 Overshoot", a["name"],
                             f"{self.name(t)}.{t['prop']} uses an elastic or bounce ease; count its overshoots by eye.")

    def gate_arcs(self, a):
        straight = set(self.moment(a).get("straight", []))
        by_obj = defaultdict(dict)
        for t in a["tracks"]:
            if t["prop"] in ("x", "y") and self.name(t) not in self.ambient:
                by_obj[self.name(t)][t["prop"]] = t
        for n, xy in by_obj.items():
            if n in straight:
                continue
            ix, iy = (self.track_info(xy[p]) if p in xy else None for p in ("x", "y"))
            dx, dy = (i["amp"] if i else 0 for i in (ix, iy))
            far = max(dx, dy)
            if far < self.th["arcMinPx"]:
                continue
            same = ix and iy and [(k[0], k[2], k[3]) for k in xy["x"]["keys"]] == [(k[0], k[2], k[3]) for k in xy["y"]["keys"]]
            if min(dx, dy) < 0.1 * far or same:
                self.add("warn", "G6 Arcs", a["name"],
                         f"{n} travels {far:.0f} px in a straight line. Curve a free movement (different eases "
                         "or timing on x and y), or list it in `straight` if it moves along the layout.")

    def gate_volume(self, a):
        tracks = defaultdict(dict)
        for t in a["tracks"]:
            if t["prop"] in ("scaleX", "scaleY"):
                tracks[t["objectId"]][t["prop"]] = t["keys"]

        def at(keys, f):
            if f <= keys[0][0]:
                return keys[0][1]
            for (f0, v0, i0, _), (f1, v1, _, _) in zip(keys, keys[1:]):
                if f0 <= f <= f1:
                    return v0 if i0 == "hold" and f < f1 else v0 + (v1 - v0) * (f - f0) / max(f1 - f0, 1)
            return keys[-1][1]

        for oid, s in tracks.items():
            if len(s) < 2:
                continue
            sx, sy = s["scaleX"], s["scaleY"]
            base = at(sx, 0) * at(sy, 0) or 1
            for f in sorted({k[0] for k in sx + sy}):
                x, y = at(sx, f), at(sy, f)
                if abs(x - y) <= 2:
                    continue
                if any("Text" in ty for ty in self.types.get(oid, [])):
                    self.add("fail", "G7 Volume", a["name"], f"{self.obj.get(oid, oid)} is text and is deformed at f{f} ({x:g}/{y:g}).")
                    break
                dev = x * y / base - 1
                if abs(dev) > self.th["volumeTolerance"]:
                    self.add("fail", "G7 Volume", a["name"],
                             f"{self.obj.get(oid, oid)} at f{f}: {x:g}% × {y:g}% changes its area by {dev:+.0%} "
                             f"(max ±{self.th['volumeTolerance']:.0%}). Squash on one axis, stretch on the other.")
                    break

    def gate_flash(self, a):
        win = a["fps"]
        for t in a["tracks"]:
            if t["prop"] != "opacity":
                continue
            rises = [f1 for (f0, v0, *_), (f1, v1, *_) in zip(t["keys"], t["keys"][1:]) if v1 - v0 >= 50]
            for i, f in enumerate(rises):
                n = sum(1 for g in rises[i:] if g < f + win)
                if n > self.th["maxFlashesPerSecond"]:
                    self.add("fail", "G10 Flashes", a["name"],
                             f"{self.name(t)} flashes {n} times within 1 s from f{f}; keep it at "
                             f"{self.th['maxFlashesPerSecond']} or fewer (photosensitivity).")
                    break

    def gate_loop_seam(self, a):
        for t in a["tracks"]:
            k = t["keys"]
            if len(k) > 1 and abs(k[0][1] - k[-1][1]) > EPS:
                self.add("fail", "G9 Loop seam", a["name"],
                         f"{self.name(t)}.{t['prop']} starts at {k[0][1]:g} and ends at {k[-1][1]:g}; the loop snaps at the wrap.")

    # ---------- state machine ----------
    def sm_layers(self):
        for sm in self.tl.get("stateMachines", []):
            for L in sm.get("layers", []):
                yield sm, L

    @staticmethod
    def cond_parts(t, rm):
        trig, rmv, other = [], [], []
        for c in t.get("conditions", []):
            name = (c.get("leftComparator") or {}).get("viewModelPropertyName")
            if c.get("type") == "triggerFired":
                trig.append(name)
            elif rm and name == rm:
                want = (c.get("rightComparator") or {}).get("value")
                rmv.append(want if c.get("operation") == "equal" else (not want))
            else:
                other.append(name)
        return trig, rmv, other

    def rm_prop(self):
        if self.spec.get("reducedMotionProperty"):
            return self.spec["reducedMotionProperty"]
        for _, L in self.sm_layers():
            for t in L["transitions"]:
                for c in t.get("conditions", []):
                    n = (c.get("leftComparator") or {}).get("viewModelPropertyName") or ""
                    if re.search(r"reduc", n, re.I):
                        return n
        return None

    def layer_graph(self, L, mode, rm):
        """Reachable, non-transient states of a layer when reduced motion == mode."""
        st = {s["id"]: s for s in L["states"]}
        anyid = L.get("anyStateId")
        ok = lambda t: all(v == mode for v in self.cond_parts(t, rm)[1]) and not t.get("isDisabled")
        out = defaultdict(list)
        for t in L["transitions"]:
            if ok(t):
                out[t["fromStateId"]].append(t)
        seen, todo = set(), [L.get("entryStateId")]
        while todo:
            s = todo.pop()
            if s in seen or s is None:
                continue
            seen.add(s)
            todo += [t["toStateId"] for t in out[s] + out[anyid]]

        def instant(t):  # fires at once in this mode: no trigger, no exit time, only reduced-motion conditions
            trig, rmv, other = self.cond_parts(t, rm)
            return not trig and not other and not t.get("enableExitTime") and (rmv or t["fromStateId"] == L.get("entryStateId"))
        live = []
        for s in seen:
            if st.get(s, {}).get("type") != "animation":
                continue
            leaves = [t for t in out[s] + [t for t in out[anyid] if t["toStateId"] != s] if instant(t)]
            if not leaves:
                live.append(s)
        return st, live, out, anyid

    def gate_state_machine(self):
        rm = self.rm_prop()
        triggers = sorted({n for _, L in self.sm_layers() for t in L["transitions"] for n in self.cond_parts(t, rm)[0] if n})
        modes = [False, True] if rm else [False]
        if not rm:
            self.add("fail", "G8 Reduced motion", "state machine",
                     "No reduced-motion property found (name it in `reducedMotionProperty`). The reduced version must be built, not promised.")

        for mode in modes:
            label = "reduced motion" if mode else "normal"
            graphs = [(L, *self.layer_graph(L, mode, rm)) for _, L in self.sm_layers()]
            for trig in triggers:
                gaps, full = [], False
                for L, st, live, out, anyid in graphs:
                    deaf = []
                    for s in live:
                        hits = [t for t in out[s] + out[anyid] if trig in self.cond_parts(t, rm)[0]]
                        if not hits:
                            deaf.append(s)
                        for t in hits:
                            if t.get("enableExitTime"):
                                self.add("fail", "G4 Response", f"{L['layerName']}",
                                         f"`{trig}` waits for exit time before leaving {st[s].get('name') or s}; answer input at once.")
                    if live and not deaf and any(trig in self.cond_parts(t, rm)[0] for ts in out.values() for t in ts):
                        full = True
                    elif deaf and len(deaf) < len(live):
                        gaps.append(f"{L['layerName']}: ignored in {', '.join(st[s].get('name') or s for s in deaf)}")
                if not full:
                    if gaps:
                        self.add("warn", "G4 Response", f"{label}",
                                 f"`{trig}` has no layer that answers it in every state. " + "; ".join(gaps) + ".")
                    else:
                        self.add("fail", "G4 Response", f"{label}", f"`{trig}` gets no visible response at all in {label}.")

            if mode:  # reduced motion: nothing but opacity may change
                for L, st, live, out, anyid in graphs:
                    for s in live:
                        an = self.anims.get(st[s].get("animationId"))
                        if not an:
                            continue
                        moving = sorted({f"{self.name(t)}.{t['prop']}" for t in an["tracks"]
                                         if t["prop"] in TRANSFORM and self.track_info(t)})
                        if moving:
                            self.add("fail", "G8 Reduced motion", an["name"],
                                     f"Plays in reduced motion ({L['layerName']}) and moves: {', '.join(moving[:6])}"
                                     f"{' …' if len(moving) > 6 else ''}. Use opacity or an instant change.")

        for _, L in self.sm_layers():
            st = {s["id"]: s for s in L["states"]}
            sig = defaultdict(int)
            for t in L["transitions"]:
                key = (t["fromStateId"], t["toStateId"], json.dumps(sorted(json.dumps(
                    {k: c.get(k) for k in ("type", "operation")} | {"l": (c.get("leftComparator") or {}).get("viewModelPropertyName"),
                     "r": (c.get("rightComparator") or {}).get("value")}, sort_keys=True) for c in t.get("conditions", []))),
                       t.get("enableExitTime"))
                sig[key] += 1
                if (not t.get("conditions") and not t.get("enableExitTime")
                        and t["fromStateId"] != L.get("entryStateId") and not t.get("isDisabled")):
                    self.add("fail", "G11 State machine", L["layerName"],
                             f"{st[t['fromStateId']].get('name') or 'state'} → {st[t['toStateId']].get('name')} has no condition "
                             "and no exit time, so it fires every frame.")
            for (f, to, _, _), c in sig.items():
                if c > 1:
                    self.add("warn", "G11 State machine", L["layerName"],
                             f"{st[f].get('name') or st[f]['type']} → {st[to].get('name')} exists {c} times with the same conditions.")
            anims = [self.anims[s["animationId"]] for s in L["states"] if s.get("animationId") in self.anims]
            keyed = {a["name"]: {(t["objectId"], t["prop"]) for t in a["tracks"]} for a in anims}
            union = set().union(*keyed.values()) if keyed else set()
            for n, ks in keyed.items():
                miss = union - ks
                if miss and len(keyed) > 1:
                    ex = ", ".join(sorted(f"{self.obj.get(o, o)}.{p}" for o, p in miss)[:4])
                    self.add("warn", "G11 State machine", f"{L['layerName']} / {n}",
                             f"Does not key {len(miss)} propert{'y' if len(miss) == 1 else 'ies'} its sibling states key "
                             f"({ex}{' …' if len(miss) > 4 else ''}); they keep the last state's value.")

        owners = defaultdict(set)
        for _, L in self.sm_layers():
            for s in L["states"]:
                for t in self.anims.get(s.get("animationId"), {}).get("tracks", []):
                    owners[(t["objectId"], t["prop"])].add(L["layerName"])
        clash = sorted(f"{self.obj.get(o, o)}.{p} ({', '.join(sorted(ls))})" for (o, p), ls in owners.items() if len(ls) > 1)
        if clash:
            self.add("warn", "G11 State machine", "layers",
                     f"Keyed on more than one layer, so the lower layer wins: {', '.join(clash[:5])}{' …' if len(clash) > 5 else ''}.")

    def gate_response_timing(self):
        rm = self.rm_prop()
        entered = defaultdict(set)
        for _, L in self.sm_layers():
            st = {s["id"]: s for s in L["states"]}
            for t in L["transitions"]:
                trig = self.cond_parts(t, rm)[0]
                an = st.get(t["toStateId"], {}).get("animationId")
                if trig and an in self.anims:
                    entered[an] |= set(trig)
        for aid, trig in entered.items():
            a = self.anims[aid]
            units = self.moving(a)
            if not units:
                continue
            first = min(u["start"] for u in units.values())
            last = max(u["end"] for u in units.values())
            if self.ms(first, a) > self.th["responseMs"]:
                self.add("fail", "G4 Response", a["name"],
                         f"Answers `{', '.join(sorted(trig))}` after {self.ms(first, a)} ms (max {self.th['responseMs']}).")
            budget = self.moment(a).get("budgetMs", self.th["budgetMs"])
            if a.get("loop", 0) == 0 and self.ms(last, a) > budget:
                self.add("fail", "G5 Timing", a["name"], f"Settles at {self.ms(last, a)} ms; budget {budget} ms.")

    # ---------- run ----------
    def run(self):
        self.gate_poses()
        sheets = []
        for a in self.tl["animations"]:
            if a.get("loop"):
                self.gate_loop_seam(a)
                self.gate_flash(a)
                continue
            units = self.moving(a)
            if not units:
                continue
            self.gate_staging(a, units)
            self.gate_settle(a, units)
            self.gate_overshoot(a, units)
            self.gate_arcs(a)
            self.gate_volume(a)
            self.gate_flash(a)
            sheets.append((a, units))
        if self.tl.get("stateMachines"):
            self.gate_state_machine()
            self.gate_response_timing()
        return sheets

    def report(self, sheets):
        fails = [f for f in self.findings if f[0] == "fail"]
        warns = [f for f in self.findings if f[0] == "warn"]
        waived = [f for f in self.findings if f[0] == "waived"]
        L = [f"# Motion lint · {self.tl.get('file')} / {self.tl.get('artboard')}", "",
             f"Exported {self.tl.get('exportedAt')}. **{len(fails)} fail, {len(warns)} warn, {len(waived)} waived.** "
             + ("Do not show this to the designer until every fail is fixed or the spec records why it stays."
                if fails else "Gates pass. Feel is still unproven until the designer plays it."), ""]
        for sev, title in (("fail", "Fails"), ("warn", "Warnings"), ("waived", "Waived by the designer")):
            items = sorted((f for f in self.findings if f[0] == sev), key=lambda f: f[1])
            if items:
                L += [f"## {title}", ""] + [f"- **{g}** · {w}: {t}" for _, g, w, t in items] + [""]
        L += ["## Beat sheets", "", "Each one-shot animation, units in start order. Times in ms from the start of the state; ★ = declared primary; ambient objects left out.", ""]
        for a, units in sheets:
            p = self.moment(a).get("primary")
            L += [f"### {a['name']} ({self.ms(a['frames'] or 0, a)} ms)", "", "| Unit | Start | Peak | Settled | Moves |", "|---|---|---|---|---|"]
            for n, u in sorted(units.items(), key=lambda kv: (kv[1]["start"], kv[0])):
                peak = max(u["tracks"], key=lambda ti: ti[1]["amp"])[1]["peak"]
                props = sorted({f"{self.name(t)}.{t['prop']} {i['amp']:.0f}" for t, i in u["tracks"]})
                L.append(f"| {'★ ' if n == p else ''}{n} | {self.ms(u['start'], a)} | {self.ms(peak, a)} | "
                         f"{self.ms(u['end'], a)} | {', '.join(props[:4])}{' …' if len(props) > 4 else ''} |")
            L.append("")
        return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("timeline")
    ap.add_argument("spec")
    ap.add_argument("--out")
    a = ap.parse_args()
    lint = Lint(json.load(open(a.timeline)), json.load(open(a.spec)))
    text = lint.report(lint.run())
    if a.out:
        open(a.out, "w").write(text + "\n")
        n = sum(1 for f in lint.findings if f[0] == "fail")
        w = sum(1 for f in lint.findings if f[0] == "warn")
        print(f"{n} fail, {w} warn, {len(lint.findings) - n - w} waived → {a.out}")
    else:
        print(text)
    sys.exit(1 if any(f[0] == "fail" for f in lint.findings) else 0)


if __name__ == "__main__":
    main()
