# DOCUMENT 1C

# AI DECISION FRAMEWORK

**Version:** 2.0
**Status:** Governing Engineering Specification — Autonomous Operation
**Authority:** Governs how Claude Code decides and operates *without human supervision*.
Subordinate to **Document 1A** (Project Instructions / `Agent.md`) and complementary to
**Document 1B** (Engineering Constitution). Where 1B defines *what* Claude Code is and *how it
must work*, this document defines *how it must decide and execute alone*.

Conflict rule: **1A > 1B > 1C.**

---

## §1 Purpose

Project Meridian V2 is developed autonomously. This document removes the need for per-milestone
confirmation by pre-authorising Claude Code to make and execute decisions, while constraining that
autonomy to five explicit pause conditions and a fixed workflow. It also governs *which installed
skills* Claude Code may invoke — preventing indiscriminate, checkbox skill usage that degrades rather
than improves the result.

---

## §2 Autonomous Execution Protocol

After receiving this specification, Claude Code shall execute the project autonomously without
requesting confirmation after every milestone.

The only circumstances under which Claude Code may pause and ask the user for input are:

1. A decision would permanently delete user data.
2. A required file is missing or corrupted.
3. Credentials, secrets, API keys, or external accounts are required.
4. Two equally valid design directions exist and neither can be objectively preferred from the specification.
5. A legal, ethical, or security concern requires user approval.

In all other cases, Claude Code shall:

* Determine the next logical task.
* Execute it.
* Test it.
* Debug it.
* Refactor it.
* Optimize it.
* Commit or checkpoint the work.
* Continue automatically until the project is complete.

Claude Code must never stop merely because a milestone has been reached.

---

## §3 Master Workflow

Claude Code shall follow this sequence without interruption:

```
1.  Audit existing portfolio
2.  Verify original works
3.  Create timestamped backup
4.  Verify backup integrity
5.  Create mo-portfolio-v2
6.  Audit architecture
7.  Identify technical debt
8.  Produce improvement plan
9.  Build section-by-section
10. Test every section
11. Debug
12. Refactor
13. Accessibility audit
14. Performance optimization
15. Responsive testing
16. Cross-browser testing
17. Final polish
18. Lighthouse audit
19. Final QA
20. Generate documentation
21. Project complete
```

Progress through this sequence is tracked in `TodoWrite`. Steps already satisfied by prior work are
marked complete and not repeated.

---

## §4 Skill Governance — Intelligent Skill Selection

Installed skills are *capabilities*, not *obligations*. Claude Code shall **not** invoke a skill
merely because it is installed. Before invoking any skill, Claude Code shall ask itself:

* Does this skill solve a problem the specification *actually has*?
* Is native HTML/CSS/vanilla JS (or GSAP, where approved) sufficient and *simpler*?
* Does invoking the skill add recruiter-visible or *measurable* value?
* Does it fit the approved stack (no React/Vue/Angular/build system unless justified — §9 of 1B)?

If the answer to the first is **"no"**, or to the others **"yes (simpler)"**, **do not invoke** the skill.

### §4.1 Skill Fit Test (decision matrix)

| Installed skill | Verdict for THIS portfolio | Invoke when… |
|---|---|---|
| `gsap-core` · `gsap-scrolltrigger` · `gsap-timeline` · `gsap-utils` · `gsap-plugins` | **APPLY** | Scroll choreography, section reveals, hero sequencing, micro-interactions (§11 of 1B). Core to the motion system. |
| `motion-dev-animations` | **REFERENCE** | Technique inspiration for vanilla motion. Prefer GSAP for implementation. Do not force a Motion library. |
| `motion-framer` | **DO NOT APPLY** | React-only. Excluded by §9 of 1B. |
| `threejs-webgl` · `spline-interactive` · `lightweight-3d-effects` | **APPLY ONLY IF MEANINGFUL** | A storytelling 3D element that helps a recruiter (e.g. an interactive map of countries taught, or subtle hero depth). Never spinning cubes / random particles (§10 of 1B). Default: **do not force**. |
| `aframe-webxr` | **DO NOT APPLY** | No XR requirement for a recruiter portfolio. |
| `lottie-animations` | **APPLY ONLY IF BENEFICIAL** | An animated explainer illustration. Default: not needed. |
| `higgsfield-*` (generate · websites · video-explainer · product-photoshoot · soul-id · marketplace-cards) | **APPLY ONLY IF ASSET NEEDED** | Producing the missing teaching video / portrait assets. Requires user-supplied source or approval (pause reason #3 / #5). Never auto-generate credentials or qualifications. |
| `seedance2` | **APPLY ONLY IF VIDEO NEEDED** | Generating the demo video asset. Requires approval (pause #3 / #5). |
| `design-system` · `ui-ux-pro-max` · `modern-web-design` · `brand` · `design` | **REFERENCE** | Lens for the Creative Review Board (§7). Not applied as code. |
| `animated-component-libraries` | **REFERENCE** | Inspiration only; implement in vanilla/CSS. |
| `banner-design` · `slides` · `pixijs` · `playcanvas` · `babylonjs` · `rive` · `blender-web-pipeline` · `substance-3d` | **DO NOT APPLY** | Out of scope for a vanilla, build-free recruiter portfolio. |

### §4.2 Principle

Claude Code selects the **smallest sufficient** tool. GSAP + vanilla JS cover the vast majority of
this project. 3D, Lottie, and generative skills are opt-in and must clear the Fit Test first. Forcing
an installed skill into a project that does not need it is a defect, not diligence.

---

## §5 Chain of Quality (mandatory pre-commit gate)

Before any commit or checkpoint, Claude Code shall confirm **ALL** of:

- [ ] Feature implemented per spec
- [ ] Tested (served locally; no console errors; no 404s on CSS/JS/assets)
- [ ] Accessible (keyboard, visible focus, labels, reduced motion)
- [ ] Performant (no render-blocking; CLS-safe; lazy media)
- [ ] Responsive (desktop / tablet / mobile each intentional)
- [ ] No dead/duplicate code; design tokens used; no `!important`
- [ ] Skill usage passed the §4 Fit Test
- [ ] Self-review questions (§8) answered

If any box is unchecked, fix it *before* committing. Never stack fixes on broken code (§17 of 1B).

---

## §6 Decision Matrix (design alternatives)

When choosing between alternatives, score each on:

1. Clarity for a recruiter
2. Accessibility
3. Performance cost
4. Maintainability
5. Alignment with §10–§12 motion principles (1B)

Prefer the option that wins on **clarity + accessibility** without sacrificing performance. When tied,
prefer the simpler, more standard solution.

---

## §7 Creative Review Board

Before finalising any section, Claude Code shall critique it from these lenses (no human needed):

* **Creative Director** — Is it premium, cohesive, timeless? Would Apple / Stripe / Linear ship it?
* **Recruiter** — In <10 seconds, can I see *who* this person is, their strengths, and *how to contact* them?
* **Performance Engineer** — Any render-blocking, layout shift, or wasted bytes?
* **Accessibility Auditor** — Keyboard, focus, contrast, screen-reader, reduced motion?
* **End User** — Readable, fast, pleasant on mobile?
* **Security Auditor** — Any leaked secret, unsafe third-party, or injection vector?

Each lens must pass, or carry a documented, justified exception.

---

## §8 Never Settle Protocol

The first acceptable solution is a *starting point*, not a finish. After each section:

1. Does it meet WCAG AA + the performance budget (§15 of 1B)? If no → iterate.
2. Can it be simpler / faster / clearer / more accessible? If yes → improve.
3. Would a senior studio ship it? If no → refine.

Repeat until the answer is "yes" on all, or a justified exception is recorded. Then commit and continue.

---

## §9 Relationship to other documents

* **1A (`Agent.md`)** — source of truth for content rules (never invent; HTML/CSS/vanilla only).
  Overrides 1C on content integrity.
* **1B (Engineering Constitution)** — defines roles, lifecycle, coding standards, budgets. 1C
  operationalises 1B.
* **1C (this document)** — defines autonomous execution + skill governance.

When unsure which governs, pause (§2 reason #5) and ask.
