# Luau scripting

Sources: https://rive.app/docs/scripting/ (getting-started, protocols, script-inputs, data-binding, pointer-events, debugging) and the live `get_scripting_reference` tool of Rive MCP. Checked 2026-09-30.

Luau is the Lua-derived language (typed, from Roblox) that Rive runs inside the editor. Use it only when state machines, data binding, and converters cannot do the job: procedural drawing, physics, custom layout, custom transition logic. Everything below is what Rive's scaffolds and docs show; if a snippet fails to compile, read the API through the tool, not from memory.

## Read the API from the editor

`get_scripting_reference` takes a required `topic`. An unknown topic returns the valid keys: `rive/gradient`, `rive/mat2d`, `rive/mat4`, `rive/path`, `rive/color`, `rive/paint`, `rive/renderer`, `rive/artboards`, `rive/dataValue`, `rive/interfaces`, `rive/image`, `rive/text`, `rive/mesh`, `rive/vector`, `rive/gpu`, `rive/gpu_types`, `rive/promise`, `rive/testing`, `rive/fileFormat`, `rive/base`, `rive/typeslib`, `@luau`. Other MCP tools for scripts: `manage_scripts`, `get_scripts`, `script_diagnostics`, `recompile_all_scripts`, `run_tests`, `read_console`.

**Vectors.** Use `Vector` with its static functions: `Vector.xy(x, y)`, `Vector.length(v)`, `Vector.dot(a, b)`, `Vector.lerp(a, b, t)`. Confirm signatures in `rive/vector` before use.

## Protocols

The protocol you pick generates a typed scaffold. Available: **Node**, **Layout**, **Converter**, **Path Effect**, **Transition Condition**, **Listener Action**, **Blank** (shared helpers via `require`), **Test**, and File Format / Text File Format. WGSL shaders are separate (https://rive.app/docs/scripting/wgsl-shaders.md).

Every script defines a type for its data, lifecycle functions, and returns a factory:

```lua
type MyNode = { speed: Input<number> }

function init(self: MyNode, context: Context): boolean return true end
function advance(self: MyNode, seconds: number): boolean return true end
function update(self: MyNode) end
function draw(self: MyNode, renderer: Renderer) end

return function(): Node<MyNode>
  return { speed = 1, init = init, advance = advance, update = update, draw = draw }
end
```

| Protocol | Factory returns | Required functions | Notes |
|---|---|---|---|
| Node | `Node<T>` | `init`, `draw` | `advance(seconds)` each frame, `update` when any input changes. Needs to be added to the artboard (right-click artboard, pick script); position sets where it renders. |
| Layout | `Layout<T>` | `resize(self, size)` | `measure(self)` optional; only matters when Fit is Hug. Add as child of a Layout. |
| Converter | `Converter<T, In, Out>` | `convert` | `reverseConvert` for two-way binding. Made from Data panel: `+`, Converters, Script. |
| Path Effect | `PathEffect<T>` | `update(self, pathData): PathData` | `init`, `advance` optional. |
| Transition Condition | `TransitionCondition<T>` | `evaluate(self): boolean` | Runs every frame while the transition is active; keep it fast and side-effect free. |
| Listener Action | `ListenerAction<T>` | `perform(self, pointerEvent)` | Side effects only, no return value. |
| Test | none | `setup(test: Tester)` | `test.case`, `test.group`, `expect(x).is(...)`. |

If a Node script does not show in the artboard menu: it must be in the Assets panel, the Problems panel must be clean, and the factory must return a table with at least `init` and `draw`.

## Script inputs

Declare inputs in the data type, give defaults in the factory:

```lua
type ScriptInputs = {
  score: Input<number>,
  menu: Input<Data.MenuVM>,                 -- a view model
  enemy: Input<Artboard<Data.Enemy>>,       -- an artboard template
}
-- factory: score = 0, menu = late(), enemy = late()
```

- Set them in the Inspector, or right-click an input and choose **Data Bind** to drive it from a view-model property.
- Scripts cannot write to their own inputs. To write to data, go through `context` or a view-model input.
- `update` fires whenever any input changes.

## Data binding from scripts

`init(self, context)` gets a `Context`:

```lua
local vmi = context:viewModel()               -- this node's view model instance
local root = context:rootViewModel()
local glob = context:globalViewModel('MyGlobalVM')
local score = vmi:getNumber('score')          -- also getString, getBoolean, getColor, getTrigger,
if score then score.value = 100 end           -- getList, getViewModel, getEnum, getImage, getFont, getBlob
```

Getters can return nil; check before use. Fire triggers with `trigger:fire()`. Subscribe with `property:addListener(fn)` (works for triggers too). If a script only reads values, bind them to script inputs instead of going through `context`.

## Pointer events

Handlers on a Node script: `pointerDown`, `pointerMove`, `pointerUp`, `pointerExit` taking `(self, event: PointerEvent)`. `event.position` is the location, `event.id` identifies each finger for multi-touch, and `event:hit()` marks it handled (stops it reaching things behind). Some doc snippets name the handlers `onPointerDown`; follow the scaffold Rive generates.

## Drawing

Create `Path.new()` and `Paint.new()` once in `init`, reuse them in `draw`. Path: `moveTo`, `lineTo`, `quadTo`, `cubicTo`, `close`, `reset`. Renderer: `drawPath(path, paint)`, plus save, restore, transform, clip. Keep allocation out of `draw`.

## Testing and debugging

- Test scripts run with `run_tests`; put logic worth testing in a Blank (util) script and `require('Name')` it.
- Debug: `print()` output in the Debug panel (`read_console` over MCP), and the Problems panel for compile errors. `script_diagnostics` returns the same problems.

## Worked example

`examples/particle-burst.luau` is a complete Node script (real-time particles with drag, gravity, additive glow). It compiled clean and rendered as expected in the editor. Patterns it demonstrates: a deterministic LCG for repeatable randomness, one `Path` per color reused every frame (reset in `advance`, drawn in `draw`), `Paint.with({ blendMode = 'additive', feather = n })` for glow, clamped `dt`, and inputs (`count`, `speed`, `gravity`, `drag`, `period`) so the designer can tune it in the Inspector. Placement and export caveats are in `mcp-field-notes.md`.

## Rules for this skill

1. Spec first: say in the plan why a script is needed and which protocol.
2. Prefer a Converter script over a Node script when the goal is only to reshape data.
3. After writing or editing: recompile, read diagnostics, read the console, and only then report success.
4. Scripts ship inside the `.riv`, but script and GPU features depend on runtime support. Confirm the developer's runtime supports scripting before relying on it.
