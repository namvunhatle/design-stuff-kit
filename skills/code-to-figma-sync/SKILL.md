---
name: code-to-figma-sync
description: Bring a Figma file back in line with a coded motion prototype after the code has moved ahead of it. Measures the live build at chosen timestamps, rebuilds frames and Smart Animate keyframes to match, and records a mapping so the two stay comparable. Use when the code prototype is the source of truth and Figma is stale; not for designing motion in Figma first (figma-prototype-motion) or for web-to-Android parity (web-android-port).
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Bring Figma back in line with the code

Motion is usually born in Figma. Then the coded prototype gets tuned by feel, and Figma goes stale: a developer or stakeholder opens the file and sees an older animation than the one that shipped. This skill rebuilds Figma from what the **live build actually does**. The build is the source of truth; Figma is the record.

```text
Figma frames → sprites → coded timeline → measure at N timestamps → Figma keyframes
```

## 0. Preflight

- The prototype must open **paused at a given second** (`?t=12.4`, audio off). Without it, nothing below is measurable. Add it first (`prototype-vercel-deploy` §1).
- Timeline events should be named constants (`T_DROP`, `b(n)`), not scattered timeouts. If they are not, list the events with their times before starting.
- Follow `figma-workflow`: pin the file key, save a restore point, build in a **new labeled section**, and do not edit frames the designer approved (`designer-in-the-loop` §1). Load `figma-prototype-motion` and `figma-console-api` before touching reactions.
- Say up front what the sync will not prove: feel and sound. The designer plays both and judges.

## 1. Choose the checkpoints

Pick 5 to 10 timestamps that carry the story: each scene's first stable frame, each accent, the peak of each transition, and the final rest frame. Prefer beats or named events to round numbers. Write them as a table: label, time, what should be on screen.

The Figma side gets **one frame per checkpoint**, not one per animation frame. Smart Animate interpolates between them.

## 2. Measure the live build

At each checkpoint, capture the page at `?t=<time>` in a fixed viewport and record, per moving element: x, y, scale, opacity, rotation, plus z-order.

- Read positions from the DOM (`getBoundingClientRect`, computed transform) rather than eyeballing screenshots. Keep a screenshot as the visual check.
- Convert to Figma space with one fixed scale factor between the design frame and the viewport; record it.
- Note which values are eased in code. Only the endpoints go into Figma; the easing goes into the reaction (see `figma-prototype-motion`).

`web-android-port` has `capture_web.mjs` for the capture step.

## 3. Rebuild in Figma

1. New section, named for the code version it mirrors (for example `v1.3.3 · synced`). Never overwrite the previous sync; it is history.
2. One frame per checkpoint, same size, **matching layer names and hierarchy in every frame** (Smart Animate matches by name and path).
3. Set each element's position, scale, and opacity from the measurement table with a script, then read the values back and compare. Report the largest deviation.
4. Wire the reactions in checkpoint order. Set durations from the time differences between checkpoints. Use the reaction timeout rules and easing tricks in `figma-prototype-motion`; `AFTER_TIMEOUT` does not accept 0.
5. Anything code does that Smart Animate cannot (particles, per-frame scripts, blur animation, audio) is drawn as a static beat frame and **labeled** as "approximated" on the canvas.

## 4. Record the mapping

Add a short table to the project's `Figma_Map` file and a line to `Session_Log`:

| Checkpoint | Time | Beat or event | Figma node | Largest deviation |
|---|---|---|---|---|

Also record the code version, the scale factor, and which behaviors are approximated. This is what lets the next sync start from a diff, not from zero.

## 5. Verify

- Re-run the geometry read-back on the Figma frames and compare against the measurement table. Do not rely on a screenshot alone.
- Query the reaction graph: destinations, timeouts, and durations.
- Put a Figma frame and the live capture at the same timestamp side by side and hand them to the designer.
- Have the designer press Present in Figma. Figma MCP cannot play it.

## When code and Figma disagree

The code wins for what shipped. If the Figma version is the approved design and the code drifted, that is a bug in the code, not a reason to sync. Ask which side is right before writing anything.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Smart Animate cross-fades instead of moving | Layer names or hierarchy differ between frames | Rename to match; verify with a path query |
| Frames match but the chain feels different | Durations came from round numbers, not checkpoint deltas | Recompute durations from the measured times |
| Blur or shadow looks different | Code uses a blur radius and Figma uses a different sigma | Compare the two on one frame and record the conversion once |
| Element clipped in Figma but not in code | Code clips at the viewport, the design frame is smaller | Measure at the design frame size, or note the clip |
| Sync drifts again next week | No mapping table | Keep §4 up to date on every code version that changes visuals |
