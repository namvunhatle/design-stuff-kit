---
name: explore-vs-final
description: Choose the right construction fidelity for exploratory design options versus a selected design ready for handoff. Use when building or reviewing Figma screens that may still be compared, discarded, or finalized. Also triggers on Vietnamese requests such as "bản nháp hay bản final", "dựng kỹ đến mức nào", "đang explore hay đã chốt".
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Explore versus final

Match the construction effort to the decision stage. An option being compared needs fast iteration; a selected design needs structure that survives reuse and handoff.

| | Explore | Final / handoff |
|---|---|---|
| Purpose | Compare directions | Implement and maintain the chosen direction |
| Layout | Direct positioning is acceptable | Use appropriate auto layout and constraints |
| Tokens | Local values are acceptable | Bind to the destination design system where a suitable token exists |
| Components | Only where they speed comparison | Define reusable parts and real states |
| Content | Realistic copy and structure | Approved copy and complete states |
| Verification | Compare options and identify tradeoffs | Check responsive behavior, accessibility, tokens, and handoff |

## Enter Explore mode

Use Explore when the request asks for alternatives, concepts, or several options and at least one is expected to be rejected. Build options where they can be compared without disturbing reviewed work. Label them clearly and keep decision notes nearby.

Explore permits raw construction. It does not permit vague content, broken interactions, or writes to a shared design-system library. If the file has local safety rules, follow them in both modes.

## Move to Final

Once the designer selects an option, bring that option into the destination system. Add auto layout and constraints where needed; bind fitting tokens; turn repeated elements and meaningful states into components or properties; verify copy, accessibility, and edge states. Record intentional exceptions instead of forcing a token that changes the design.

Keep rejected options available as exploration history if the designer wants them. Do not polish every option before a decision just to make their construction identical.

If the request does not reveal whether the output is for comparison or handoff, ask which stage the designer needs before choosing the construction method.
