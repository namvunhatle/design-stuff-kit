# Rive MCP field notes

From building and testing a press-feedback button (artboard, layout, two timelines, view model, two transitions, two listeners) in the Rive editor, 2026-09-30, editor beta 0.9.46. These are observed behaviors, not documented guarantees. If the editor updates, re-test before trusting them.

## Units

- **Keyframe values for scale and opacity are percentages.** `modifyKeyFrames` with `1` made the layout render at about 1% (the button vanished during Play). Use `100` for 100%, `88` for 88%. `query_property_values` and `set_property_values` also use percentages (scale and opacity read `100`).
- `modifyKeyFrames` echoes back the number you sent, so the reply cannot confirm the unit. Confirm by playing the state machine and looking.
- Rotation is in degrees. Colors are `#aarrggbb`.

## Tool quirks

- `layout_editor.createLayout` fails schema validation when a child is text. Create the layout, then add text with `appendLayout`.
- A new artboard already has one timeline and one state machine wired Entry to that timeline. Rename the timeline (`renameAnimations`) and reuse it; create new ones only for extra animations.
- `create_listeners` accepts a constant `value` for `viewModelChange`, but its reply does not echo it. Read it back with `query_property_values` on the listener action's bindable property (key `propertyvalue`).
- `viewmodel_editor.createViewModels` also creates an auto-named `Instance`. Bind the instance you mean with `bindViewModelToArtboard`, and check `listViewModelInstances` so you know which one the artboard uses.
- `set_property_values` on a transition (`duration` key) stored `100` and `queryStateMachine` reported `duration: 100` with `durationIsPercentage: false`. The unit is presumably milliseconds but was not checked visually. `enableEarlyExit` (allow exit during transition) is reported by `queryStateMachine` but no key for it was found; set it in the editor if the spec needs it.

## What the tools can and cannot verify

- `simulateStateMachine` checks logic: which states and transitions fire when view-model values change. It **stops as soon as the machine settles**, so an input scheduled after that frame is silently dropped. Schedule the return input soon after the first transition, and check `transitionsObserved` and `finalStates`.
- It does not render, and it does not simulate pointer input. Listener behavior (hit areas, `down`/`up`/`exit`) is only proven by playing in the editor.
- `capture_artboard` shows the static design, not an animation frame. A correct capture does not prove the Play state looks right.
- So a finished build always ends with the designer pressing Play and reporting or screenshotting what they see. Do not report "works" from tool output alone.

## Playing it in the editor (for the designer)

Sources: https://rive.app/docs/editor/interface-overview/toolbar, https://rive.app/docs/editor/interface-overview/debug-panel, https://rive.app/docs/editor/fundamentals/design-vs-animate-mode.

1. Switch to **Animate Mode** (Mode Toggle in the toolbar, or `Tab`).
2. Select the state machine in the Animations list, not a timeline.
3. Use the toolbar's Play State Machine control. The stage shows a "Playing State Machine" banner.
4. Press and hold the target on the stage.
5. Open the Debug Panel Console, State Machine console, to see states entered and transitions taken.

While a timeline is selected in Animate Mode, edits on the stage can create keys by accident. Select the state machine, or switch to Design Mode, before touching objects.

## Design defaults that avoid a false "nothing happens"

- A 4% scale change on a 240 px button is barely visible. For a test, use a clear change (about 88% scale) and tune down afterward.
- If the layout renders as the artboard background color only, suspect a wrong keyframe unit before suspecting the state machine.
- Export of a `.riv` for runtime (Publish, or Export, For runtime) is documented as a paid-plan feature.

## Building bigger scenes (learned on the Ring Burst scene)

- **Groups:** `group_editor` with `parentId` and `x`/`y` reported success but the group did not exist. Create the empty group without `parentId`, then create shapes with `parentId` set to the group. The group's `x`/`y` were also ignored (it landed at 0,0), so read the group's position back and set it with `set_property_values` (keys `13`, `14`).
- **Wrapping changes coordinates:** `group_editor` with `objectIds` moves the new group's origin to the contents' bounds, so children keep their look but their `x`/`y` change. Re-read positions (`query_property_values`, keys `13`, `14`) before keying them, and key values in the group's local space.
- **Timeline length and rate:** an animation object exposes `fps` (56), `duration` (57, in frames), `loop` (59: 0 one-shot, 1 loop, 2 ping-pong). New timelines are 60 fps and 60 frames. Set `duration` with `set_property_values`.
- **Keyframes:** send generated keyframes in batches of about 80 `add` items. Each item can carry its own `interpolationType` and `cubicParams`. Put a `hold` keyframe at frame 0 to define the resting value before the animation starts moving that property.
- **Draw order:** a parent's children list reads front to back (first is on top). Objects created later appear on top unless reparented.
- **Shape parameters:** `createParametricShapes` supports rectangle, ellipse, polygon, star with gradients and `feather`. `addTrimPaths` exists for stroke draw-on effects.

## Scripts in the scene

- `manage_scripts.create` with source creates and classifies the script (a Node script is listed as protocol `node`). Then `recompile_all_scripts` and `script_diagnostics` (empty list means clean).
- No tool adds a Node script instance to an artboard. The designer must right-click the artboard and pick the script (docs: Creating Scripts), or drag it from Assets.
- The instance lands where the designer clicked, often outside the artboard, so particles emit off-canvas and nothing shows. After the designer adds it, find it with `find_objects` (it is a `ScriptedDrawable`; `get_artboard_hierarchy` at shallow depth may not list it), read `x`/`y` (keys `13`, `14`), and set them to the intended origin.
- The script asset has `includeInExport: false` by default. Turn it on before handing a `.riv` to developers, or the runtime file will not contain the script.
- Console stays empty until the scene plays with the script in it; an empty console before that is not a sign of success or failure.

## Lessons from a sky-scene build with scripts (2026-10-01)

Every item below cost at least one wrong "done". Read before the first write.

**Units (verify by reading back, not by trusting the echo)**
- `set_property_values` AND `modifyKeyFrames` both use **percent** for scale and opacity: `100` = full, `33.3` = one third. A `0.333` is 0.33%. Writing `1` for opacity gives 1%, not full.
- Reading back during Play shows the live value in the same unit (`wind` opacity `1.0` next to siblings at `100.0` exposed the bug). Compare a suspect object with a healthy sibling.
- Images import at native pixel size (1080x2400). Scale `33.33` to fit a 360x800 artboard; check `computedwidth` (810) and `computedheight` (811) after.

**State is sticky**
- Rive keeps the last value of a property when the active animation does not key it. An Idle state that dims opacity to 70 leaves it at 70 in Play unless Play keys opacity to 100 too. Every state that can follow must key (or hold) every property any sibling state touched, including "off" states (key opacity 0 for each object a looping state fades in).
- A loop that animates opacity must start and end on the same value or it snaps at the wrap.

**Defaults that look like bugs**
- New animations are **one-shot** (`loop` key 59 = 0). Set 1 for anything that must repeat, then read it back. Looping is still worth confirming in Play; the property can look right and the stage can be paused.
- A seamless horizontal drift needs the end copy identical to the start copy (A, mirrored B, A) and an end key of exactly one period (here -720 for a 360 wide tile).
- Pointer `dragStart` listeners are created but do not fire at runtime; use `drag`.
- Wrapping objects with `group_editor` moves the group origin: re-read `x`/`y` (13, 14) of the group and children and reset the group to 0,0 before keying absolute positions.
- State speed is key 292 on the state; transition mix duration is key 158 (ms); transition flags 152: `4` = exit time, `12` = exit time as a percentage (exit time 100 = at the end).

**What the tools cannot prove**
- `capture_artboard` always renders the resting artboard, even while the editor is playing, and `query_property_values` while paused returns frozen values. Neither shows an animation frame. For Play, read live values twice a few seconds apart (changing numbers = running), then ask the designer for a screenshot of the Play state at 100% zoom.
- Editor zoom matters: at 25% zoom, slow drift and small flares read as "nothing moves".
- Say what was not seen. Do not report done from tool output.

**Environment**
- The editor is sandboxed and cannot read files outside its own folders. Upload assets and scripts through the local MCP HTTP endpoint (`initialize`, then `notifications/initialized`, then `tools/call`) with a data URI or script source; no session header is returned.
- A Node script instance must be added to the artboard by the designer (right-click artboard); then set its `x`/`y` to 0,0.

**Design**
- Do not add a decorative highlight (a breathing glow, ripple rings) unasked. A highlight has to belong to the subject (sky: stars, meteors, cloud light), or it reads cheap. Ask once which direction before building a new visual layer.
