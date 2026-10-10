# Route design work in Codex

Use the project's configured model and effort unless the designer has chosen another supported configuration. Do not hardcode model names or prices into project instructions. Bundled `agents/*.md` files describe roles; they do not register agents or choose a model.

| Work | Role | How to run it |
|---|---|---|
| Flow, IA, directions, token map, build plan, product voice | Main session with the designer | Keep decisions and trade-offs with the designer |
| Build an approved plan or fix render failures | `ui-builder`, `wireframe-builder` | Use the role brief in the current session, or delegate bounded work when available and authorized |
| Contrast, clipping, targets, pixel parity | `wx-render`, `wx-compare` | Run deterministic checks before visual critique |
| Quality, direction, regression | `design-critic` | Independent reviewer with a blind brief; continue the same reviewer across rounds |
| Review a Figma file or a batch of copy | `figma-auditor`, `copy-reviewer` | Send only the relevant scope and rules |
| Node IDs, tokens, components, references, long specs | `scout` | Gather facts and return references; the main session chooses |

Keep small edits in the main session. When delegation is available and authorized, give each reviewer or builder a clear scope and only the context it needs. Inherit the session model unless the user or applicable project instructions explicitly select another available model.

If independent review is unavailable, explain the limitation and offer a separate reviewer session with the brief. Do not report self-review as a blind critique. Skill frontmatter does not configure model routing or create a forked Codex agent.

Record useful model comparisons only from actual runs: the same task, rubric, score, and measured usage. Do not promise savings based on Claude aliases, assumed cache behavior, or fixed token estimates.
