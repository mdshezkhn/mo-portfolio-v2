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
