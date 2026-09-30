# Data binding

Source: https://rive.app/docs/editor/data-binding/ (overview, view-models, property-types, migration-guide, converters, lists). Checked 2026-09-30.

## Model

1. **View model:** defines the shape of the data.
2. **Instance:** holds actual values.
3. **Binding:** connects a property to an element in the scene.
4. Values change from the editor, runtime code, state machines, or scripts. Listeners, code, and scripts can react to changes. Bound elements update automatically.

Bindings ignore hierarchy, so elements can move or nest without breaking runtime code.

## Data binding replaces inputs and events

Docs state that data binding replaces both **state machine inputs** and **runtime event listeners**. Existing files keep working; data binding is recommended for new work.

| | Inputs | Events | View-model properties |
|---|:-:|:-:|:-:|
| Number, Boolean | yes | yes | yes |
| Trigger | yes | no | yes |
| String | no | yes | yes |
| Enum, Color, nested view model, List, Image, Artboard | no | no | yes |

- Inputs only drive transitions. Properties can also drive blend states and any bindable property, can pass through converters, and can be shared across the file.
- To convert an old file: editor hamburger menu, **Convert Inputs to View Models**, then update runtime code.
- Instead of a General event, make a view-model property, update it from the file (animation, listener, script), and let code subscribe to it.
- Instead of writing to a text run by name, bind a String property to it.

## Property types

Number, String, Boolean, Color, Trigger (fire and forget), Enum (fixed options), Image, Font, Artboard (must be a Component first), View Model (nesting), List (collection of view models).

- Image and Font properties affect a **single instance**. To replace an asset file-wide, use asset loading instead.
- A view-model instance assigned to a nested component must be referenced from the main view model.

## Constraints or data binding?

Constraints: direct object-to-object, purely visual, editor-only. Data binding: value comes from code, several elements share it, or you need logic via converters.

## Converters

Pad, Range map, Numeric interpolator, Formula, Number to list, Color interpolator, and Converter Scripts (Luau). Converters can be grouped and reordered; they run in order.

## Lists

A List property holds view-model instances, optionally tied to artboards, for repeating content (inventory, messages, generated UI). See https://rive.app/docs/editor/data-binding/lists for the full set of behaviors.

## Naming

Property and view-model names are the developer API. Pick final names before handoff.
