# Contributing

Open an issue to describe the design workflow and the failure your change addresses before adding a broad new skill. For a focused improvement, a pull request is enough.

- Keep each skill usable without private project context. Use synthetic examples and placeholders for Figma file keys and node IDs.
- Explain when the skill applies and when a nearby skill is a better fit.
- Include verification steps for claims about Figma writes or prototype behavior. Say clearly when a tool cannot verify the visual experience.
- Do not add credentials, internal links, client names, screenshots, user data, or unpublished design-system keys.
- Credit upstream authors and include the license terms when adding third-party material. Do not remove their attribution or replace it with this repository's author.
- Do not rewrite or paraphrase another author's framework and publish it as original. If a workflow depends on unlicensed third-party material, point to the installed file and its source instead.
- Agent templates must declare `tools:` explicitly. An agent without that line inherits every tool, including Figma write tools.

Before opening a pull request, review the diff and the entire new commit history for confidential material.
