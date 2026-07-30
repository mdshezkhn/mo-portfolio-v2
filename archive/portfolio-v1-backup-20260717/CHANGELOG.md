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
