---
name: motion-principles
description: Apply the 12 classic principles of animation (squash and stretch, anticipation, staging, straight ahead and pose to pose, follow through and overlap, slow in and slow out, arcs, secondary action, timing, exaggeration, solid drawing, appeal) to product UI motion, calibrated for interfaces rather than cartoons. Use when planning, critiquing, or tuning any motion (Figma Smart Animate, Motion or CSS prototypes, Rive), or when a designer says a transition feels stiff, floaty, cheap, or "off" without knowing why. Not a build guide for any tool; the medium skills (figma-prototype-motion, rive-motion, interactive-prototype) do the building.
metadata:
  author: namvunhatle
  version: 1.0.0
---

# The 12 principles of animation, for product UI

The principles come from Disney's animators and were codified by Ollie Johnston and Frank Thomas in *The Illusion of Life* (1981). They describe how to make drawn characters feel alive. Product UI borrows them for a narrower goal: motion that explains what changed, where things went, and what the user can do next.

Use them as vocabulary and as a checklist, not as a quota. A calm product needs most of them at low intensity. The kit's own review history shows the risk: cartoon squash, bounce, and particles on a calm product were rejected as "quê" (tacky) (`${CLAUDE_PLUGIN_ROOT}/skills/rive-motion/references/motion-craft.md` §7). Intensity is a product decision. Ask the designer, or read the project's `design.md` or voice guide, before turning a principle up.

## When to read this

- **Planning:** before writing the motion spec in `figma-prototype-motion`, `rive-motion` §2, or a coded prototype. Name which principles the moment needs and at what intensity.
- **Diagnosing:** when the designer reports a feeling ("stiff", "floaty", "jerky", "cheap", "slow"), map it to a principle with the table in §2 before changing numbers.
- **Reviewing:** run §3 against a played or recorded piece. Tool output never proves feel; the designer's play-through does (`designer-in-the-loop`).

## 1. The principles, translated

Each entry gives the original idea, what it means in an interface, and the calibration that keeps it from looking cheap.

### 1. Squash and stretch

- **Origin:** a shape deforms to show weight and flexibility. A ball stretches as it falls and flattens on impact, keeping the same volume.
- **In UI:** a pressed button compresses slightly. A fast-moving dot or pill stretches along its path. A sheet or card overshoots on landing.
- **Calibrate:** keep volume (stretch one axis about as much as the other shrinks), and keep it small: about 2–5% on controls, up to 10–15% only on a small, playful, physical-feeling element. Stretch follows speed: it peaks on the fastest segment and squashes on impact, never early (`figma-prototype-motion` §3). Never deform text or a container that holds text. On a calm product, replace it with a plain press scale (about 97%).

### 2. Anticipation

- **Origin:** a small preparing move before the main action, like winding up before a kick.
- **In UI:** a slight pull back before a card flies off, a press state before navigation, an inhale before a success bloom.
- **Calibrate:** it runs against the direction of the exit (leaving left → wind up right; falling → compress) (`figma-prototype-motion` §4). Keep it short, about 50–120 ms. Never put it on the response to a tap, because it reads as lag. Use it only when the system starts the action, or as the first frames of a large, deliberate one.

### 3. Staging

- **Origin:** present one idea at a time, with composition, framing, and lighting, so the audience cannot miss it.
- **In UI:** one primary motion per moment. Everything else is still, dimmed, or clearly secondary. The motion leads the eye to the element the user needs next.
- **Calibrate:** if two elements both demand attention, stagger them or quiet one. Dim the background under a big moment rather than animating it (`motion-craft.md` §5). Swap copy only while it is invisible (`figma-prototype-motion` §4). Staging is the principle most often broken by "add more motion".

### 4. Straight ahead action and pose to pose

- **Origin:** straight ahead draws frame after frame for fluid, unpredictable action. Pose to pose sets key poses first and fills in between for control.
- **In UI:** pose to pose is the default. Design the start and end states as real frames (Figma variants, Rive states, React states), then animate between them. Straight ahead corresponds to procedural motion: springs, physics, particles, Rive scripts.
- **Calibrate:** approve the poses (static end states) before tuning motion, as `rive-motion` §3 and `motion-craft.md` §8 do. Use procedural motion only where the movement must react live (drag, scroll, data), not to decorate a fixed transition.

### 5. Follow through and overlapping action

- **Origin:** parts keep moving after the body stops (hair, clothing), and different parts move at different rates.
- **In UI:** children settle slightly after their container, an icon arrives a beat after its tile, a list's items finish a few frames apart. The hit-and-settle overshoot (`motion-craft.md` §2) is follow-through.
- **Calibrate:** one overshoot only, then rest. Offsets of about 20–80 ms between parts. Exit and entry should share time rather than queue. Nothing should still be moving after the destination has settled, or the whole transition reads as slow (`figma-prototype-motion` §4).

### 6. Slow in and slow out (ease in, ease out)

- **Origin:** real objects accelerate and decelerate, so there are more frames near the start and end of an action.
- **In UI:** elements entering the screen ease out (fast start, gentle stop); elements leaving ease in; elements moving within the screen ease in-out. Linear motion reads as mechanical, except for continuous loops such as spinners and progress bars.
- **Calibrate:** in a multi-keyframe chain, acceleration comes from keyframe spacing with linear segments, not from per-segment easing, or the velocity wobbles (`figma-prototype-motion` §3). Easing presets that worked are in `motion-craft.md` §2. On a beat grid, avoid elastic eases that oscillate against the beat (`beat-synced-motion` §3).

### 7. Arcs

- **Origin:** natural movement follows curved paths. Very fast arcs can blur into a smear.
- **In UI:** an element travelling a long diagonal (a card to a cart, a photo to its detail, a dot to its target) follows a slight curve. A shared-element transition reads as one object moving rather than two swapping.
- **Calibrate:** curve only long, free movements. Elements sliding along the layout's own axis (sheets, tabs, page pushes) move straight. In Figma, approximate a curve with intermediate keyframes off the straight line. In code, animate x and y with different eases. In Rive, use a path or a script. A smear is a few frames of stretch or a blurred copy, never a live blur (`motion-craft.md` §5).

### 8. Secondary action

- **Origin:** supporting movement that adds life without stealing focus, like arms swinging while walking.
- **In UI:** a checkmark drawing inside a button that is already confirming, a subtle shine on a card as it lands, haptic or sound paired with a visual accent.
- **Calibrate:** it must support the primary action, start after it, and be smaller and quieter. If a reviewer remembers the secondary action and not the state change, cut it. Particles and ring shapes are the usual offenders (`motion-craft.md` §7).

### 9. Timing

- **Origin:** the number of frames sets weight and mood. Light things move fast; heavy or slow things take more frames.
- **In UI:** duration follows distance, size, and importance. Starting points: micro feedback (press, toggle, hover) 100–150 ms; small component changes 150–250 ms; screen and sheet transitions 250–400 ms; large choreographed moments 500 ms and up, only when the user is not waiting. Exits are faster than entries. A cheap action (dismiss, cancel) is visibly quicker than a committing one.
- **Calibrate:** these are defaults, not law; the designer's play-through decides. Anything the user waits through repeatedly should get shorter, not longer. Music-led pieces take their timing from the beat grid (`beat-synced-motion` §3).

### 10. Exaggeration

- **Origin:** push reality further than life so the action reads clearly and has appeal.
- **In UI:** a slightly larger overshoot on a success moment, a bigger scale on the one hero element, a stronger shake on an error.
- **Calibrate:** exaggerate one thing per moment and only the meaningful one. Reserve it for rare, celebratory, or attention-critical moments, never for routine navigation. The kit's taste lessons say to lower intensity before adding more effects: most "too visible / crude" notes were fixed by lowering opacity and raising softness (`motion-craft.md` §7).

### 11. Solid drawing

- **Origin:** forms feel three-dimensional, with weight, balance, and volume. Avoid "twins", where both sides of a character mirror each other exactly.
- **In UI:** motion respects a consistent spatial model. Elevation, shadow, and scale agree (an element that lifts toward the user grows and gains shadow; one that recedes shrinks and dims). Layers keep their z-order through a transition. Objects keep their shape while they move.
- **Calibrate:** a sheet that slides up should leave the way it came. Two sibling elements should not move in perfect unison; offset or vary them (the UI version of "twins"). Animate transform and opacity so geometry stays crisp instead of reflowing layout mid-motion.

### 12. Appeal

- **Origin:** characters the audience wants to watch, through design, personality, and clarity.
- **In UI:** the motion has one consistent personality that matches the product's voice: calm and precise, warm and soft, or playful and springy. The same easing family, the same overshoot amount, and the same direction logic are used everywhere.
- **Calibrate:** appeal is set by the product, not by the principle list. Read the voice guide (`voice-tone-builder`) or ask. Check references on Mobbin before choosing a look for loading, AI, or success moments (`rive-motion` §2). Consistency usually looks better than one impressive moment.

## 2. From the designer's word to the principle

| The designer says | Check first | Usual fix |
|---|---|---|
| Stiff, robotic, mechanical | 6 slow in and slow out, 5 overlap | Ease the ends; offset children a few frames |
| Floaty, slow, sluggish | 9 timing, 5 follow through | Shorten; stop all motion when the destination settles |
| Jerky, janky | 6 (velocity wobble), 9 against the beat | Measure velocity per segment; snap accents to the grid |
| Cheap, tacky, toy-like | 10 exaggeration, 8 secondary action, 1 squash | Remove effects, lower intensity, keep one overshoot |
| Confusing, "what just happened?" | 3 staging, 7 arcs, 11 solid | One primary motion; keep the spatial model; move as one object |
| Laggy after a tap | 2 anticipation on a response | Remove the wind-up; respond in under 100 ms |
| Boring, lifeless | 5 overlap, 8 secondary action, 12 appeal | Add one supporting layer at low intensity |

## 3. Review checklist

Run it on a played or recorded piece, with the designer, and report each line as pass, fail, or not applicable:

1. One primary motion per moment; the eye lands where the user acts next (3).
2. Start and end states were approved as frames before motion was tuned (4).
3. Entries ease out, exits ease in, loops are linear or sine; no velocity wobble (6).
4. Durations fit distance and importance; exits faster than entries; nothing moves after the destination settles (9, 5).
5. Children and siblings offset; one overshoot at most (5, 11).
6. Long free movements curve; layout-axis movements stay straight (7).
7. Deformation keeps volume, follows speed, and never touches text (1).
8. Anticipation never delays a response to the user's input (2).
9. Secondary actions and exaggeration are quieter than the state change and match the product's intensity (8, 10, 12).
10. Reduced motion: a version without movement exists and keeps the same meaning (cross-fade or instant state change, no lost information). Only transform, opacity, and filter animate.

## Sources

The twelve principles are Ollie Johnston and Frank Thomas's, from *The Illusion of Life: Disney Animation* (1981). Summaries consulted: Adobe, ["The 12 principles of animation"](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html), and New York Film Academy, ["12 Principles of Animation"](https://www.nyfa.edu/student-resources/12-principles-of-animation/). Neither page's text is reproduced. The product-UI translations, calibrations, and checklist were written for this kit from its own review history.
