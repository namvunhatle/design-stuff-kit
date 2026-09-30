# Layouts

Source: https://rive.app/docs/editor/layouts/ (overview, parameters, component-sizing). Checked 2026-09-30.

## Model

A Layout is a container whose position and size follow rules relative to its parent or children. Any object (text, shape, path, group, image, component) placed in a Layout inherits positioning from it.

- **Layouts only position other Layouts.** A Row layout arranges its Layout children.
- Layouts nest: outer is the parent, inner the child. Combine and nest to build whole interfaces.
- **Absolute:** placed freely on the artboard like any object.
- **Relative:** takes part in the parent's flow (direction, gap, padding). Toggle with the icon at the top right of the layout inspector.

Use cases: pin items to edges, buttons and labels that hug their text, lists and grids that reflow, animate, and scroll.

## Component sizing (for component instances)

- **Node** (default): scales as one object via the Scale property. Use when the parent layout does not matter.
- **Leaf:** fits contents into the available space without reflowing. Good for icons and illustrations. Fit options: Fill (default, stretches), Contain, Cover, Fit Width, Fit Height, None, Scale Down. Alignment is a 9-point grid or X/Y from -1 to 1.
- **Layout:** resizes the component's artboard so its contents reflow.

## Planning tip

Decide in the spec which artboard sizes the asset must survive (see the artboard width, height, and ratio built-ins, which can act as transition conditions), and pick Layout sizing for anything that has to reflow.

Full parameter list: https://rive.app/docs/editor/layouts/layout-parameters.md
