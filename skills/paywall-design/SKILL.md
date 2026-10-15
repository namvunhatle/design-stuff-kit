---
name: paywall-design
description: Plan, explore, or review a subscription paywall and the journey that leads to it in a consumer app. Covers selling the outcome before the price, multi-page paywalls, trial timelines, risk-reducing copy, plan count, anchoring, deliberate friction, polish, dark patterns to avoid, Apple review risk, and what to measure. Use when designing or critiquing a paywall, trial offer, plan picker, or upgrade screen, or when deciding what to A/B test on one. Not a build guide; web-explore, figma-design-system-ui, and ux-copywriter do the building and the words. Also triggers on Vietnamese requests such as "thiết kế paywall", "màn hình trả phí", "màn mua gói", "tăng tỉ lệ dùng thử", "review paywall".
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Paywall design

There is no universal best paywall. What converts for one audience fails for another, so treat everything below as a starting hypothesis to test, not a rule to apply. Most of it comes from Jonathan Parra ("The Paywall Guy"), who reports having designed more than 4,700 paywalls (see Sources). Numbers attributed to him are his reported results, not results this kit has measured.

## When to read this

- **Planning:** before wireframing a paywall or the onboarding that leads to it. Decide the journey (§1) before the screen (§2).
- **Exploring:** when choosing directions for `web-explore`. Use §6 to make the options differ in kind, not only in colour.
- **Reviewing:** run the checklist in §7 on rendered screens, alongside `design-critique`.
- **Before submission:** check §5 with the designer. App Review risk is a product and legal decision, not a design call.

## 1. The journey decides more than the screen

- **People often decide to pay before they see the paywall.** The onboarding, the first value moment, and the promise the app makes all happen earlier. A paywall cannot rescue a journey that never showed the value.
- **Sell the outcome, then the price.** Opal (screen-time app) framed its value as getting years of life back before asking for payment. Parra reports trial starts rising from 7% to 17%. Name the outcome in the user's terms (time, money, health, a skill), not the feature list.
- **Ask where the paywall sits.** After onboarding, at a feature gate, after a first success, or on a later session. Each is a different user with different intent. Map them before designing one screen for all.

## 2. Structure

- **Multi-page beats single page, in Parra's experience almost always.** Unfold the information over 2–4 steps: outcome → how it works or proof → plan and trial terms. Each step carries one idea, which lowers cognitive load (`motion-principles` §3, staging, applies to content too).
- **Two plans on the base paywall.** Annual and monthly is the usual pair, with one preselected. More options belong behind a "See all plans" link or on a later screen.
- **Show the trial as a timeline.** Blinkist's pattern: today (full access), a reminder day before the trial ends, the day billing starts with the amount. It answers "when will I be charged?" before the user has to ask.

## 3. Lowering risk and friction

- **"Cancel anytime" under the main button,** and a right-pointing chevron on the button. Parra reports both as consistent winners. They are cheap to test first.
- **Social proof:** real ratings and reviews, close to the decision point. Use only real, current numbers.
- **Anchor the price** against a daily expense ("less than a coffee a week") or show the annual plan as a monthly equivalent. The arithmetic must be correct and the billed amount must stay the most visible price (§5).
- **Friction can help.** Asking for payment details up front for the trial reduced trial starts but, in a case Parra describes, doubled paying customers, because it filtered out people who were never going to pay. Judge it on paid conversion, not on trial starts (§6).

## 4. Polish

High-quality motion and a coherent world (Parra cites Focus Town) are becoming the baseline users expect, not a bonus. Polish means the paywall feels like the same product as the rest of the app. Plan motion with `motion-principles`, keep it calm enough that the price and terms stay readable, and give it a reduced-motion version.

## 5. Patterns to avoid or clear first

- **Spin-the-wheel discounts and fake urgency** (countdowns that reset, "only 3 left" for software) can raise short-term revenue but cost trust. For a product that wants long-term subscribers, do not propose them. If the designer asks for one, name the trade-off and let them decide.
- **Free-trial toggles.** Parra reports that Apple became stricter in early 2026 about trial toggles it considers misleading, and that some apps were rejected. Treat any toggle that switches between "trial" and "no trial" as needing a check against the current App Review Guidelines (subscriptions, §3.1.2) before handoff.
- **Always shown clearly:** the billed amount and period, what happens after the trial, how to cancel, and Restore Purchases. Close (X) must be visible and work. These are App Store requirements, not style choices; confirm current wording with the product owner.

## 6. What to test, and what to judge it on

- **Test radically different ideas, not only button colours:** video paywall, plain bullet list, long-form page, multi-page flow, outcome-first vs price-first. Small tweaks come after a direction wins.
- **Judge on retention and lifetime value (LTV),** not on the conversion spike. A tactic that doubles trials and then doubles refunds or cancellations is a loss. Agree the success metric with the product owner before the test, and record it in the brief.
- Find real examples of a pattern with the `scout` agent on Mobbin before inventing one, and cite which apps you looked at.

## 7. Review checklist

- [ ] The value or outcome was shown before this screen, in the user's terms.
- [ ] One idea per page; the base screen offers at most two plans, one preselected.
- [ ] Trial terms read as a timeline: start, reminder, first charge with amount and date.
- [ ] "Cancel anytime" (or the true cancellation terms) sits near the main button.
- [ ] The billed price is the most prominent price; any per-day or per-month anchor is arithmetically correct.
- [ ] Social proof is real and current.
- [ ] Close, Restore Purchases, terms, and privacy links are visible and work.
- [ ] No fake urgency, no reset timers, no gambling mechanics, no trial toggle that has not been cleared against current App Review rules.
- [ ] Motion supports the reading order and has a reduced-motion version.
- [ ] The test plan names the metric (paid conversion, retention, LTV), not only trial starts.

## Sources

Jonathan Parra, interviewed on paywall design: [YouTube video](https://www.youtube.com/watch?v=9ypqs_2fAl8). The cases (Opal, Blinkist, Focus Town), the reported numbers, and the 2026 Apple note are his, taken from a summary of the video; check the video before quoting a number to a stakeholder. The checklist, the routing to kit skills, and the App Store hygiene items were written for this kit.
