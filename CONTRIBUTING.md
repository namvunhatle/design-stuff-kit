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

## Releasing

The plugin's `version` in `.claude-plugin/plugin.json` decides what users get. Pushing to `main` without changing it reaches nobody who installed from the marketplace, so a half-finished change on `main` is safe until you bump the number.

1. Work on a branch. Add your clone as a marketplace to try changes in place (`claude plugin marketplace add /path/to/design-stuff-kit`, then `/reload-plugins`).
2. Run `claude plugin validate .` and test in a real project.
3. Bump `version` (semver: `0.1.1-beta` for fixes, `0.2.0-beta` for new skills or behaviour; drop `-beta` at 1.0.0). Add a section to `CHANGELOG.md` under the new number, with an **In your project** list for any hand edit users must make.
4. Merge to `main`, push, then tag the release: `claude plugin tag --push`. This creates `design-stuff-kit--v<version>`.

Users with auto-update get the release at their next session; others run `/plugin marketplace update design-stuff-kit`.
