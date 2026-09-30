# Data binding

Source: https://rive.app/docs/editor/data-binding/ (overview, view-models, property-types, migration-guide, converters, lists). Checked 2026-09-30.

## Model

1. **View model:** defines the shape of the data.
2. **Instance:** holds actual values.
3. **Binding:** connects a property to an element in the scene.
4. Values change from the editor, runtime code, state machines, or scripts. Listeners, code, and scripts can react to changes. Bound elements update automatically.

Bindings ignore hierarchy, so elements can move or nest without breaking runtime code.

## What data binding does

View-model properties drive transitions, blend states, and any bindable property in the editor. They can pass through converters and be shared across the file. Code, animations, listeners, and scripts write to them; the app subscribes to them.

- Communicating back to the app: make a view-model property, update it from the file (animation, listener, script), and let code subscribe to it.
- Text: bind a String property to a text run instead of addressing the run by name or path.
- If a file you are handed still has legacy controls, editor hamburger menu, **Convert Inputs to View Models**, then update the runtime code.

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
