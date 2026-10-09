---
paths:
  - "explore/**"
---

# Web exploration folders

Loads only when Claude reads a file under `explore/`. If your explorations live elsewhere, change the path above. Path-scoped rules load when a matching file is read, not always when a new one is created, so the `web-explore` skill repeats anything that must hold from the first file.

- Files here are explorations, not product code. Do not import them into the app, and do not edit Figma from this folder's work until `ship-to-figma` phase 3.
- Once a direction is built in Figma, Figma is the source of truth. Leave the folder as history and do not keep editing it in parallel.
- One `<section class="screen" data-name="…">` per frame, built with flex or grid. Real content only.
- Render with `/design-kit:render` (or `wx-render`) and fix every FAIL before a critic or the designer sees the screens.
- In wireframe mode (`data-mode="wireframe"`), use greys and the `wireframe.css` primitives; copy stays real. The pick goes to the wireframe track in Figma, not `ship-to-figma`.
- In design-system mode, colours come from `tokens.css`, generated from `design-tokens.json`. Edit the JSON, not the CSS.
- Never write the maker's own score into `CRITIQUE.md`. The official score is the critic's.
