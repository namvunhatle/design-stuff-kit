---
name: web-explore
description: Explore UI directions as HTML phone screens with a live preview, then render them to PNG and check them automatically before a critic and the designer review them. Use when the designer wants to compare directions or try a screen quickly before committing to Figma, or wants a quick demo on a real phone. Not for building the chosen design for handoff (ship-to-figma) or for a stakeholder motion prototype in React (interactive-prototype).
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Explore on the web

HTML is the fastest canvas for exploring: one save, one reload, and it runs on a real phone. Motion plays, which Figma MCP cannot do. This skill is **phase 1** of the kit's web-to-Figma workflow:

```text
1 Explore (this skill)  →  2 Lock (ship-to-figma)  →  3 Build in Figma (ship-to-figma)
   HTML, live preview        designer picks one,         design-system UI track,
   render + checks           token map approved          parity, audit, re-critique
   design-critic
```

Explorations are disposable. Once a direction is built in Figma, **Figma is the source of truth** and these files become history.

## 0. Setup (once per working folder)

Needs Node.js 18+. Make a folder for the feature, outside the product's source code, and copy the assets in so it also deploys as is:

```sh
mkdir -p explore/<feature> && cd explore/<feature>
cp ../../.claude/skills/web-explore/assets/{frame.css,frame.js,starter.html} .
mv starter.html explore.html
npm init -y >/dev/null && npm i -D playwright     # render step only
```

`render.mjs` uses installed Google Chrome when it finds it. Otherwise run `npx playwright install chromium` once. Tell the designer before installing anything.

## 1. Brief and mode

Settle these in one short message before drawing: the product and who it is for, the core action, the platform (iOS, Android, or both), three words for the feel, and what already exists. Use the project's `CLAUDE.md` first and do not re-ask what it answers.

Then pick the mode:

| Mode | When | How |
|---|---|---|
| **Free** | Finding a direction; the design system may not express it yet | Local values in `:root`, named by role |
| **Design system** | The direction is close, or the product must stay inside its system | `<html data-mode="ds">`, link `tokens.css`, and use only its variables |

For design-system mode, keep the system's tokens in the project's `design-tokens.json`, each with a description of what it is for (derive it from Figma variables with `figma_get_token_values` or `figma_export_tokens`, resolved for the product's modes). Generate the CSS:

```sh
node .claude/skills/web-explore/scripts/tokens-to-css.mjs design-tokens.json --out explore/<feature>/tokens.css
```

The descriptions travel into `tokens.css` as comments, which is how Claude picks the right token. The render check then flags every colour that is not a token. Those flags are your token-map questions for phase 2, found early.

## 2. Three directions, then one

When the task is "explore", render the core screen three ways in one file (`explore.html`). Make the three genuinely different: a different ground (light, dark, or a colour field or image), a different type family, and a different source of richness (photo, illustration or shape, colour and material). Three tints of one layout is one direction.

Use real, specific content, never lorem or grey boxes. Give each a one-sentence concept. After rendering, write in `DIRECTION.md` which one you would pick, and one line on why each of the others lost. The designer decides.

Then build the chosen direction out in `mockup.html`: the core screen in a realistic mid-use state, one level deeper, one other step of the core loop, the key feedback moment as 2 to 4 frozen frames (`data-freeze`), dark mode if the product has it, and an empty or first-run state if it matters.

## 3. Live preview

```sh
node ../../.claude/skills/web-explore/scripts/serve.mjs mockup.html
```

It reloads on every save and prints a LAN address. Open it on a phone on the same Wi-Fi to try touch, motion, and reading distance in hand. For a link that works anywhere, use `prototype-vercel-deploy`.

Markup rules (full list in the header of `frame.css`): one `<section class="screen" data-name="…">` per frame, set `data-device` per screen or on `<html>`, and build with flex or grid so the same markup survives the small-phone pass.

## 4. Render and check

```sh
node ../../.claude/skills/web-explore/scripts/render.mjs mockup.html --out shots/r1
node ../../.claude/skills/web-explore/scripts/render.mjs mockup.html --out shots/r1-small --small
```

With the kit's slash command, `/render explore/<feature>/mockup.html` does this from the project root and picks the next `shots/rN` and `--compare` for you. Each run writes one 3x PNG per screen, `sheet.png`, and `report.md`. It exits with code 1 on any FAIL.

| Check | Level |
|---|---|
| Text clipped by its container, outside the screen, or overlapping other text | FAIL |
| Text contrast below WCAG AA (4.5:1, or 3:1 for large text) | FAIL |
| Touch target under 44 × 44 pt (iOS) or 48 × 48 dp (Android) | FAIL |
| Two screens that render the same (one is broken or never drew); `data-identical-ok` marks intended twins | FAIL |
| A JavaScript error on the page | FAIL |
| Text under 11 px; ellipsis truncation; text over an image or gradient (contrast not measurable) | warn |
| Design-system mode: a colour that is not in `tokens.css` | warn |

From round 2, add `--compare shots/r1` (the previous round). The report lists which screens did not change, so an edit that did not land is caught, and only the changed screens go to the critic.

Fix every FAIL. Answer every warn: fix it, or write one line on why it is deliberate. The attribute escapes (`data-bleed`, `data-overlap-ok`, `data-decorative`) are for intent, not for silencing a defect. Then open every PNG at full size; the sheet shows the flow, but defects live in the full frames.

## 5. Critique

Run `design-critique` with the `design-critic` agent: phase `explore`, the PNG paths, `report.md`, and the project's `critique/config.md` and `anchors.md` if they exist. Iterate into `shots/r2`, `shots/r3`, and so on, until the critic's stop rule says "Ready", or the budget runs out.

"Ready" means ready for the designer. Show them the sheet, the live link, and the scores, and let them judge the feel in hand (`designer-in-the-loop` §3).

## 6. Hand over to phase 2

When the designer picks a direction, continue with `ship-to-figma`. Keep `DIRECTION.md`, `CRITIQUE.md`, and the final `shots/` folder; phase 3 is scored against them.

## Hard rules

| Never | Instead |
|---|---|
| Grey placeholder boxes, lorem, emoji as icons | Real content, drawn shapes or real images, one icon set |
| A layout made of absolute coordinates | Flex or grid; absolute only for overlays and artwork |
| Animating width, height, top, or margin | Transform, opacity, filter; respect `prefers-reduced-motion` |
| Claiming a motion "feels right" | Say what you measured; the designer plays it |
| Polishing all three directions before a pick | Equal craft, not equal finish; polish only the winner |
| Editing Figma in this phase | Figma starts in phase 3, after the designer approves the token map |
