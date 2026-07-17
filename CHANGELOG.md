## Stages 4–6 — Design System, Component Library, Build (Master Plan)

### Why
- Execute Stages 4–6 of the 1C §16 Stage Gate per the approved Master Implementation Plan
  (`docs/MASTER_IMPLEMENTATION_PLAN.md`). The prior build was code-complete but had diverged
  from its own approved design spec and was missing spec-mandated content/sections.

### Files Changed
- `docs/VISUAL_IDENTITY.md` (rewritten to v2.0 — reconciled to the live light/navy build; 2A §12
  implies light, so the spec now matches the build rather than the reverse).
- `assets/css/variables.css` (added 8px-base spacing-scale + section-padding tokens).
- `assets/css/sections.css` (Gallery + lightbox styles; Research/Credentials additions).
- `assets/css/components.css` (inline-SVG `.ic` icon style).
- `assets/css/layout.css` (footer nav + social styles).
- `assets/css/animations.css` (reveal rise 20px → 10px; hero 20px → 12px, per spec §15).
- `assets/js/gallery.js` (implemented: category filtering + accessible lightbox — Esc/←/→/backdrop,
  focus return; graceful when images missing).
- `assets/js/main.js` (removed inert `theme.js` + `timeline.js` imports/calls).
- `assets/js/theme.js`, `assets/js/timeline.js` (deleted — dead stubs).
- `index.html` (Classroom Moments gallery built; safeguarding & ethics statement; languages slot;
  Research "how this changed my classroom" + publications slots; richer footer w/ nav repeat +
  social; hero emoji → inline SVG).
- `ASSET_INVENTORY.md` (reconciled to actual code-referenced drop-in paths).
- `docs/specification/Document-2A-Creative-Brief-Recruiter-Psychology.md` (new — governing
  psychology companion; added per user direction).
- `docs/specification/Document-1C-AI-Decision-Framework.md` (added §16 Stage Gate Policy).

### New (closes §9 Authenticity beat)
- The `moments` section is now a real filterable Classroom Moments gallery with a lightbox. It
  shows graceful fallback tiles until classroom photos are dropped into `assets/images/classroom/`.

### Known Issues (user-supplied — pause reason #2)
- CV PDF, certificate thumbnails, WeChat QR, contact portrait, and classroom photos still missing
  (graceful fallbacks in place). Drop files at the paths in `ASSET_INVENTORY.md`.
- `[NEEDS INPUT]` slots remain in Research (classroom-change reflection, publications) and
  Credentials (languages proficiency) — user-authored content required before launch.
- "Harris University" MA (2007–2009) + 2009–2014 gap unverified — confirm before deploy.
- Philosophy/Leadership prose expansion pending user beliefs + examples.
- Lighthouse not yet run (needs Chrome locally).

---

## Phase 3 — Build & Remediation (Creative Brief §10)

### Why
- Begin the specification → implementation → review cycle per the consolidated
  plan (single Creative Brief `docs/specification/Document-2-Creative-Brief.md`;
  the 10-doc roadmap was scrapped as over-engineered). Close the two confirmed
  bugs carried from the V2 remediation pass.

### Files Changed
- `index.html` (added `no-js` on `<html>`; inline head script sets `.js`)
- `assets/css/animations.css` (gated `.reveal` hidden state on `.js`)
- `assets/js/navigation.js` (mobile-menu focus trap; focus first link on open)

### Fixes
- **FOUC / no-JS safety:** `.reveal { opacity:0 }` was not gated by a JS-availability
  class, yet `class="container reveal"` is in the HTML — so without JS the content
  was permanently invisible, and any flash risk existed. Hidden state is now
  `.js .reveal`; an inline head script adds `.js` before first paint. With JS:
  hidden from first paint, revealed by the observer (no flash). Without JS: content
  fully visible. Satisfies "JS failure → content visible by default" and Doc 1C §9.
- **Mobile-menu focus trap (a11y):** keyboard Tab / Shift+Tab now cycles within the
  open menu instead of escaping into hidden background content; focus moves to the
  first link on open; Escape still returns focus to the toggle.

### Side Effects
- None on visual design or performance. Reveal animation behaviour unchanged for
  JS users. `.reveal.is-visible` (later in source order) still wins over `.js .reveal`.

### Known Issues (unchanged — pause reason #2, user assets required)
- CV PDF, certificate thumbnails, WeChat QR, contact portrait still placeholder.
- "Harris University" MA + 2009–2014 gap still pending user confirmation.
- Lighthouse audit needs Chrome locally (Master Workflow step 18).

---

## Six-Act Narrative Realignment (Doc 1C §15)

### Why
- Adopt the cinematic six-act framework as the governing site structure (Doc 1C
  §15 + user direction). The previous linear order buried Professional Journey at
  #6, placed Leadership at #5, and Credentials at #9 — fighting the
  impression → journey → evidence → classroom → future → invitation arc.

### Files Changed
- `index.html` (reordered; nav realigned)
- `docs/INFORMATION_ARCHITECTURE.md` (added §0 Six Acts; §2 regrouped by act)
- `docs/PRD.md` (§9 rewritten as the six-act arc)

### New Section Order (single page)
Hero → Story → Journey → Impact → Credentials → Philosophy → Moments → Research →
Leadership → Contact.

### How
- Reordered sibling `<section>` blocks only. All `id`, `aria-labelledby`,
  skip-link target, and nav/hash deep-links preserved (verified: 10 open / 10 close,
  every nav anchor resolves). No CSS/JS/asset change.

### Side Effects
- None on performance or accessibility (structure and semantics unchanged).
- `Credentials` (with placeholder cert thumbnails) now appears in Act III earlier in
  the scroll; once real certificate images are added this reads as evidence, not a gap.
- Nav order now follows the narrative arc (Story → Journey → Impact → Credentials →
  Philosophy → Gallery → Research → Leadership → Contact).

### Known Issues (unchanged)
- CV PDF, certificate thumbnails, WeChat QR, contact portrait still placeholder (pause
  reason #2). "Harris University" MA + 2009–2014 gap still pending user confirmation.

---

- Added Section 22 Recruiter Journey (0–60s mapping)
- Google Fonts + Font Awesome retained for v1; performance target >=90 launch / >=95 post-optimization
- Page-weight budget replaced with lazy-loading + responsive images + FCP <1.5s
- Gallery, Teaching Philosophy, Research restored as distinct nav items/sections
- Safeguarding policy added; accessibility moved into every sprint; Sprint 0 added
- Operating rules adopted: One Improvement Rule, Version Freeze

### Visual Identity v1.1
- Official typography: **Fraunces + Manrope** (Inter/Roboto/Arial banned)
- Entrance motion reduced to 8–12px rise; "backgrounds never compete with content"
- Portraits: approachability over authority; width rhythm 1120/720 codified
- "One dominant action per viewport"; icons capped at 8; bento selective-use only
- Added section 18 Content Voice & Tone and section 19 Component Behavior

### Information Architecture v1.1
- About renamed **My Story**, moved before Teaching Impact
- Gallery renamed **Classroom Moments**; hero gains location + availability line
- Impact stats must answer Scale/Reach/Improvement/Leadership
- Philosophy capped at 700 words; Leadership Principles added; journey role weighting added
- Research requires "how this changed my classroom"; Currently Learning added; Connect on LinkedIn labeled

### Content Blueprint v1.1
- Purpose field added to every slot; Content Priority Matrix embedded per section
- Evidence Source made a hard publish gate; Proof Folder (private, off-repo) adopted
- Portfolio Asset Register adopted (ASSETS.md)

## Sprint 3 - Hero complete

### Files Changed
- `index.html`
- `assets/css/style.css`
- `assets/js/main.js`

### Why
- To optimize loading performance, ensure strict WCAG AA accessibility compliance, and eliminate dead code, all without altering visual appearance.

### New Features
- None.

### Fixes
- **HTML:** Added `tabindex="-1"` to `<main>` to enable reliable skip-link keyboard navigation.
- **HTML:** Connected all `<section>` elements to their headings via `aria-labelledby`, establishing valid ARIA landmarks.
- **HTML:** Moved `main.js` to `<head>` and added `defer` for non-blocking parallel loading.
- **HTML:** Removed deprecated `<meta name="author">` tag.
- **CSS:** Darkened `--text-muted` and `--border-strong` colors to pass WCAG AA contrast ratios (4.5:1 and 3:1 respectively).
- **CSS:** Removed unused CSS variables (`--bg-elevated`, `--surface-raised`, `--radius-md`, `--accent-text`).
- **CSS:** Removed orphaned transition code and unused `.card` rules.
- **CSS:** Removed unnecessary `transform` and `box-shadow` properties from nav link hover transitions.
- **CSS:** Relocated `::selection` pseudo-element out of a mobile-only media query to apply globally.
- **CSS:** Added a rule to prevent a focus outline on `<main>` when targeted by the skip link.

### Known Issues
- `assets/documents/Mohammed_Shehzad_Khan_CV.pdf` is missing; "Download CV" links throw a 404.
- Mobile menu lacks a keyboard focus trap; users can tab out into hidden background content.
- Deferring `main.js` introduced a regression: scroll-reveal elements briefly appear fully painted before the script hides them (Flash of Visible Content).

## V2 Remediation — Autonomous Pass (Project Meridian V2, Doc 1C)

### Files Changed
- `index.html`
- `assets/css/fonts.css` (new)
- `assets/css/{variables,reset,typography,layout,components,sections,animations,responsive}.css`
- `assets/js/utilities.js` (new)
- `assets/js/main.js`
- `assets/fonts/Fraunces-normal.woff2`, `Fraunces-italic.woff2`, `Manrope-normal.woff2` (new)
- Deleted: `assets/css/style.css` (obsolete `@import` wrapper)

### Why
- Execute the Document 1C Master Workflow autonomously: remove deploy-blockers and
  Doc 1B §15 performance violations without changing the visual design.

### Fixes
- **P1-1 (perf):** Removed the serial `@import` chain in `style.css`; the 8 modules are now
  linked directly in cascade order (parallel, non-blocking). Deleted the obsolete wrapper.
- **P1-2 (perf + China):** Self-hosted Fraunces + Manrope as variable woff2 (latin subset),
  preloaded with `font-display: swap`. Replaces Google Fonts, which is render-blocking and
  unreachable for the China-based audience.
- **P1-3 (perf):** Removed perpetual `will-change: transform` from `.hero-image img`.
- **P0-2 (deploy-blocker):** Replaced the `VIDEO_ID` placeholder YouTube iframe with a styled
  poster placeholder (no third-party request). Swap in a real embed when the ID is supplied.
- **P0-1 (deploy-blocker):** Favicon links now point to the existing `icon-192.svg`. Added
  `initImageFallbacks()` (progressive enhancement) that swaps any failed `<img>` for a styled
  placeholder, so missing certificate/QR/portrait images no longer show broken icons.
- **P2-1 (dead code):** Removed the unused `.badge-group` selector.
- **P2-2 (duplicate):** Removed the duplicate `scroll-behavior` declaration from `reset.css`
  (kept the `prefers-reduced-motion`-guarded one in `layout.css`).
- **P2-4 (consistency):** Updated stale `v1.0` version banners to `v2.0` across all CSS/JS.

### Known Issues (user-supplied assets required — Autonomous Protocol pause #2)
- Certificate thumbnails, WeChat QR, contact portrait, and the CV PDF are not in the repo;
  placeholders/fallbacks are shown until the real files are added at their referenced paths.
- Content verification (Doc 1A "never invent"): confirm "Harris University" (MA) and the
  2009–2014 date gap before deploy.
- Lighthouse audit (Master Workflow step 18) needs Chrome; run locally before publish.
