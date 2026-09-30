# Motion craft: what makes a Rive scene feel premium

Goal of using Rive in this kit: motion that is better than a click-through prototype, not a like-for-like copy of it. Rive earns its place when motion is choreographed, layered, or driven live by input or data.

Source of the techniques: the A7 onboarding prototype (`A7Script.kt`, `docs/EXPERIENCE.md`, a coded Android/web build) rebuilt as a Rive scene ("Ring Burst") on 2026-09-30. Numbers below come from that script; they are a starting point, not a law.

## 1. Choreograph to a beat grid

- Pick the tempo first (A7: 100 BPM, one beat = 0.6 s = 36 frames at 60 fps). Put every major event on a beat or a half-beat. Compute frames from the grid, not by eye: `frame = round(seconds * 60)`.
- Write a timeline table before keying: event, beat, frame. A7's drop (ring burst) is beat 0, the next scene starts on beat 1, and each name swap lands on its own beat.
- The moving accent should arrive ON the beat that starts the next scene (A7: the comet dot flies for one beat and lands on beat 1).

## 2. Hit and settle, not just ease

Every accent gets a fast overshoot and a slower settle. A7's pulse: scale to 109% in 0.07 s, back to 100% in 0.33 s. Tiles pop to about 112% then settle. One overshoot only.

In Rive MCP a cubic keyframe cannot overshoot (control points y are limited to [-1, 1] and x to [0, 1]), so key the peak explicitly: a keyframe at the overshoot value, then a keyframe at the rest value.

Easing presets used (cubic `x1,y1,x2,y2`): out `0.25,0.46,0.45,0.94`; in `0.42,0,1,1`; in-out `0.45,0,0.55,1`; strong out `0.215,0.61,0.355,1`. The interpolation of the earlier keyframe drives the segment after it.

## 3. Stagger everything that repeats

Rings, tiles, trail ghosts, wave bars enter offset by 2 to 5 frames (0.03 to 0.08 s) each. There is no stagger control in Rive keyframes, so offset the start keyframes per object. Order tiles by distance from the center so the wall assembles outward.

## 4. Layer four things at once on a big moment

A7's ring burst is: a flash (scale 20% to 90%, opacity 0 to 60% to 0), three thin rings that open past the edges, a comet dot with a fading trail of ghost copies, and tiles popping from the center. Then a small camera shake on the next beat, four steps of 3 frames: (-4,3), (3,-2), (-1,1), (0,0). Put all scene content in one `cam` group and animate the group for the shake.

## 5. Cheap tricks that read as expensive

- Blur ramp: crossfade to a pre-blurred copy of the art instead of animating a live blur.
- Glow: additive blend plus feather on the paint (both exist in script `Paint.with` and as feather on Rive paints).
- Gradients on tiles (light corner to deep corner) instead of flat fills.
- Dim the background under a burst rather than wiping it.

## 6. Go beyond keyframes where Rive is strongest

Keyframes replay a fixed clip. Use these when the motion should react:

- **Scripts (Luau):** particles, physics, procedural paths. Example: `references/examples/particle-burst.luau` (72 additive glowing particles with drag and gravity, compiles clean, verified visually by the designer).
- **Data binding:** drive blend states, positions, or colors from a view-model property that the app or a pointer listener writes (touch position, scroll, progress).
- **Listeners:** pointer down, drag, enter and exit write view-model properties; transitions read them.
- **WGSL shaders:** GPU lighting, noise, chromatic offset (docs: scripting/wgsl-shaders).

## 7. Workflow that produced the scene

1. Read the source timeline (beat map and easings) and write the frame table.
2. Build static end state first, capture it, fix layout.
3. Generate the keyframes with a script (Python or similar) from the table, then send them in batches of about 80. Hand-typed keyframes drift; the tool echoes every keyframe back, so batches are large.
4. Simulate only for logic; ask the designer to Play and describe rhythm, overshoot, and density; then adjust numbers.
5. Add real-time layers (scripts, listeners) after the timeline feels right.
