# State machines

Source: https://rive.app/docs/editor/state-machine/ (states, transitions, listeners, layers). Checked 2026-09-30.

## Anatomy

A graph of **states**, **transitions**, and **layers**. Every artboard has at least one state machine; you can add more. States are timeline animations. Typical button: Idle, Hovered, Clicked.

## States

- **Entry:** where the machine starts. Several animations can hang off it (a switch that can start on or off).
- **Exit:** tells the layer to stop playing. Niche; useful with multiple layers.
- **Any State:** states connected to it can play regardless of the current state (e.g. swapping a character skin).
- **Single animation:** one timeline. One-shot, looping, or ping-pong depending on the timeline. Most states are this.
- **1D blend:** mixes timelines with one number property across a range (health bar 0 to 100). The mix is additive, not linear, so results can surprise you; key only a few properties per timeline.
- **Additive blend:** mixes timelines with several number properties, either *by value* (fixed baseline pose) or *by property* (mixed in via its own number property).
- **Speed:** per state. Negative plays backward.
- **Captions:** editor-only notes, not exported.
- **Actions** on state start or end: set property values, report events, align targets, control focus, fire a scripted action.

## Transitions

- A transition path is **one-way**. Going back needs a second path. Several paths between the same two states give "or" logic.
- **No conditions = fires as soon as reached.** This causes rapid flipping or skipped states. Always add conditions or exit time on purpose.
- **Condition** = source value + operator + comparison value. Sources: view-model properties, events, built-ins (artboard width, height, ratio). Operators: equals, not equals, greater/less (or equal), depending on type. The comparison value can be fixed or data bound. Multiple conditions on one transition are AND.
- **Duration:** default 0, so states snap. Set it for any visible blend.
- **Exit Time:** off by default. Use 100% to play the whole animation before leaving.
- **Pause source when exiting:** freezes the outgoing state during the transition.
- **Allow exit during transition:** lets a hover-out reverse mid-transition. Turn on for hover and press states.
- **Interpolation:** linear by default; cubic and others available.
- **Actions** on transition start or end, same set as state actions.
- **Randomize exit:** weighted random choice among outgoing paths (weights 3 and 1 give 75% and 25%).
- **Disable transition:** temporarily off without deleting; use to isolate a bug.

## Listeners

Created under the state machine graph. Options:

- **Target:** an element (for pointer interactions) or the artboard / nested component (for view-model property changes and Rive events).
- **Opaque target:** on stops pointer events at this hit area; off lets them pass to listeners underneath.
- **Listen to:** View Model Property Change, Rive Event (both need an artboard or component target), Pointer Enter, Exit, Move, Down, Up, Drag, Click.
- A property-change listener fires on any change. You cannot specify the expected value or direction.
- Pointer Exit may not fire when the target touches the canvas edge, because Rive stops seeing the pointer.
- **Listener actions:** change a view-model property, align to target (with Preserve Offset), report an event, fire a scripted action, fire a Rive event. Values in listener actions can be data bound.

## Layers

One state plays per layer at a time. Add layers for independent behavior (walk cycle on one, hover on another). Layers lower in the list win when two animate the same property. Layers can be disabled, duplicated, reordered.

## Events

Events live on the artboard and can fire from timelines, states, transitions, or listeners. Types: Open URL and Audio. To communicate between artboards or with the app, use data binding.
