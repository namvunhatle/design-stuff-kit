---
name: rive-motion
description: Decide whether an interaction should be a Rive asset, then build it in the Rive desktop editor through Rive MCP (artboards, shapes, layouts, state machines, transitions, view-model data binding). Use for interactive, state-driven motion that ships to developers as a .riv file; not for Figma Smart Animate chains (figma-prototype-motion) or coded web prototypes (interactive-prototype).
metadata:
  author: namvunhatle
  version: 2.1.0
  mcp-server: rive
  docs-checked: 2026-09-30
---

# Rive motion

Rive earns its place when motion is **driven by state**: it reacts to input, loops, blends, or is bound to app data. A one-shot fade is not a Rive job.

This skill is the workflow. Facts about Rive live in `references/`, written from the official docs and dated. Rive's Early Access editor changes fast: when a reference and the live docs disagree, the docs win. Index: https://rive.app/docs/llms.txt (every page also exists as `.md`).

## 0. Preflight

Rive MCP is local. It only works while the **Rive desktop app (Early Access, macOS or Windows)** is running, at `http://127.0.0.1:9791/mcp`. Setup: `claude mcp add --transport http rive http://127.0.0.1:9791/mcp`, or the `rive` entry in `.claude/design-kit-templates/mcp.json.example`.

1. Check the server is connected and read its tool list. Tool names change; take them from the server, not from memory. If it is not connected, say so and stop; do not describe Rive edits as done.
2. Call `session_info` and `list_artboards`. Confirm which file and artboard you are editing before the first write.
3. Rive has no version history exposed through MCP. Tell the designer to duplicate the file first.
4. For Luau scripts, read `references/scripting-luau.md`, then `get_scripting_reference` (it needs a `topic`; an invalid one returns the valid keys) instead of writing the API from memory.

## 1. Choose the medium

| The motion... | Use |
|---|---|
| Is a click-through demo inside Figma | `figma-prototype-motion` |
| Is a coded prototype for a link or review | `interactive-prototype` (Motion) |
| Reacts to input or app state, has several states, loops, or ships in the product | **Rive** |
| Is a fixed, non-interactive clip | Lottie or video; Rive is overkill |

Say which you chose and why in one line.

## 2. Plan before building

Write a short spec and get a go-ahead before a substantial edit:

1. **Artboard:** size, and what scales (see `references/layouts.md`).
2. **States:** every state (idle, hover, pressed, loading, success, error), which loop, which blend.
3. **View model:** each property's name, type, and who sets it (user, app data, the state machine). Everything the app sends to or reads from the asset goes through view-model properties (`references/data-binding.md`).
4. **Transitions:** from, to, condition, duration, exit time. One table (`references/state-machines.md`).
5. **Listeners:** what pointer or property change triggers what.
6. **Reduced motion:** the static or shortened version, built in, not promised.

When the goal is to enhance motion beyond a click-through prototype, read `references/motion-craft.md` before planning: put events on a beat grid, add hit-and-settle and stagger, and use scripts, listeners, or data binding where the motion should react live.

## 3. Build

Work in this order, verifying each layer with a scene query before the next: artboard → shapes and layouts → animations (keyframes) → view model and bindings → state machine, states, transitions, listeners → scripts only if the spec needs them. After any script edit, recompile, read diagnostics and the console before saying it works.

Keyframe values for scale and opacity are percentages (`100`, not `1`). Add text to a layout with `appendLayout`, not inside `createLayout`. Details and other tool quirks: `references/mcp-field-notes.md`.

Name every object and view-model property as the developer will reference it. Renaming later breaks their code.

## 4. Verify and hand off

- Query the scene back and compare against the spec; do not rely on what you meant to write.
- Test each transition, including the way back out of every state. A transition path is one-way: the return needs its own path. `simulateStateMachine` covers the logic only; it does not render or simulate the pointer.
- **Have the designer press Play** (steps in `references/mcp-field-notes.md`) and report or screenshot the result. Tool output alone never proves the animation looks right; a wrong keyframe unit, for example, makes the layout vanish while every query still passes.
- Hand off the `.riv` with the spec table: artboard name, state machine name, view model name, property names and types. Note the runtime the developers use, because feature support differs by runtime (`references/handoff.md`).

Motion rules from the kit apply: animate transform, opacity, and filter; respect reduced motion.

## References

| File | Covers |
|---|---|
| `references/state-machines.md` | States, blend states, transitions, conditions, exit time, listeners, layers |
| `references/data-binding.md` | View models, property types, binding, converters, lists |
| `references/layouts.md` | Responsive layouts and component sizing |
| `references/scripting-luau.md` | Luau protocols (Node, Layout, Converter, Path Effect, Transition Condition, Listener Action, Test), script inputs, view-model access, tooling |
| `references/motion-craft.md` | What makes a scene feel premium (beat grid, hit-and-settle, stagger, layering) and when to go beyond keyframes |
| `references/examples/particle-burst.luau` | A working Node script: glowing real-time particles |
| `references/mcp-field-notes.md` | Observed Rive MCP units and quirks, what the tools can and cannot verify, how the designer plays the state machine |
| `references/handoff.md` | Runtimes, React hook signatures, MCP capabilities and limits, reduced motion |
