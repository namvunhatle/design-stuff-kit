---
name: voice-tone-builder
description: Build or audit a product voice and tone guide across onboarding, success, errors, payments, and destructive actions by applying Yummy Labs' voice and tone framework from their ux-copywriter package. Use for a reusable voice guide or a consistency audit across screens; use ux-copywriter for a single label or message.
metadata:
  author: namvunhatle (routing only)
  framework-author: Yummy Labs
  framework-file: ux-copywriter/references/voice-tone-builder.md
  version: 2.0.0
---

# Voice and tone builder

This skill is an entry point, not a framework. The voice and tone method it applies is written by **Yummy Labs** and ships inside their `ux-copywriter` package as `references/voice-tone-builder.md`. This repository does not redistribute or paraphrase it. Credit Yummy Labs when you describe the method to the designer.

## 1. Load the framework

Read `.claude/skills/ux-copywriter/references/voice-tone-builder.md` in full before writing anything.

If the file is missing, stop. Tell the designer that the Yummy Labs `ux-copywriter` package is not installed and give its source: <https://yummy-design-sprint.notion.site/Claude-UX-Copywriter-Skill-31962791470980989abdcd6312890920>. Do not reconstruct the framework from memory; a remembered version is neither accurate nor properly credited.

## 2. Gather the product evidence

The framework needs real material. Before defining or auditing a voice, collect:

- the product's purpose, audience, and any brand or legal constraints;
- current interface copy from several contexts, including at least one high point (a success or reward) and one low point (an error, payment failure, or destructive confirmation);
- the product's languages and any existing voice guide.

If the project has none of this, ask for representative screens or a text export. Do not invent the product's personality from its category.

## 3. Apply it to this product

Follow the framework's steps and checks as written. Keep the result specific to this product: every attribute, tone shift, and example should come from its real screens and users. Mark any assumption about a user's emotional state as a hypothesis the team can test.

## 4. Deliver

Return the guide in chat. Save it to the project (for example `Voice_Tone.md`) only when the designer asks. Once a guide exists, `ux-copywriter` can write individual strings against it and the `copy-reviewer` agent can audit a batch of screens for drift.
