# Handoff, runtimes, and MCP limits

Sources: https://rive.app/docs/editor/ai/mcp.md, https://rive.app/docs/runtimes/react/data-binding.md, https://rive.app/docs/runtimes/react/best-practices.md, https://rive.app/docs/runtimes/react/state-machines.md. Checked 2026-09-30.

## What Rive MCP can do (per docs; the list grows)

Create and manage files and artboards; inspect and edit the scene; build shapes, paths, layouts, component instances, lists; edit animations, state machines, states, transitions, conditions, keyframes, interpolation; create view models, properties, instances, bindings, property groups; manage Luau scripts and WGSL shaders, with diagnostics, recompile, tests, search, and console output.

Only available in the desktop editor on macOS and Windows, and the Early Access app must be open. Read the tool list from the server each session.

## Runtimes

Web (JS, WebGL2, Canvas), React, React Native, Flutter, Apple, Android, Unity, Unreal, C++, Defold. Community: Angular, C#, Qt, RiveCMP. Support differs by runtime; check the developer's runtime page before promising a feature.

## React hooks (verified against the docs)

```ts
useViewModel(rive, options?)            // { useDefault: true } | { name: 'VMName' }; not a bare string
useViewModelInstance(viewModel, options?) // { useDefault } | { name } | { useNew: true } | { rive } to bind
useViewModelInstanceNumber('path', instance) // returns { value, setValue }
```

Property paths can be nested, e.g. `'settings/volume'`. Sibling hooks exist for other property types; see the React data-binding page.

- Keep `useRive` and its `RiveComponent` together in one dedicated wrapper component. Recreating the canvas restarts or blanks the animation.
- State machines advance per frame and can "settle" when nothing changes; paused state machines keep the last frame.

## Reduced motion

Rive publishes a reduced-motion example file (https://rive.app/community/files/28077-53052-accessibility-reduced-motion). Build a static or shortened path into the state machine, for example a boolean view-model property that the app sets from `prefers-reduced-motion`, and list it in the handoff table.

## Handoff table (include with the .riv)

| Item | Value |
|---|---|
| Artboard name | |
| State machine name | |
| View model name | |
| Properties (name, type, direction: app to Rive, Rive to app) | |
| Reduced-motion property | |
| Runtime | |
