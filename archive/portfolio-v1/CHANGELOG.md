## Gitee Deployment + Font Self-Hosting (2026-07-17)

Switched the deploy target from GitLab Pages to **Gitee Pages** so the site is reachable
inside mainland China (GitLab is blocked by the Great Firewall).

### Files Changed
- `index.html` — removed the Google Fonts `<link>` + preconnects (render-blocking and
  China-blocked); repointed canonical / Open Graph / Twitter / JSON-LD URLs to the Gitee
  Pages pattern `<gitee-username>.gitee.io/mo-portfolio/` (replace the placeholder with your
  real Gitee username before pushing).
- `assets/css/style.css` — added 8 `@font-face` rules (Fraunces 500/600/700 + italic 400,
  Manrope 400/500/600/700) serving woff2 from `assets/fonts/`.
- `assets/fonts/*.woff2` — 8 self-hosted font files (latin subset).
- `gitee-pages.yml` — added (branch: main, directory: ., https: true).
- `.gitlab-ci.yml` — removed (no longer the deploy target).
- `docs/PERFORMANCE.md`, `docs/PRD.md` — Google Fonts China risk marked resolved.

### Why
The stated goal is access from within China. Google Fonts is blocked there, so the previous
build would have stalled first paint and fallen back to system fonts. Self-hosting the woff2
files removes that dependency entirely.

### Pre-launch action
- Replace `<gitee-username>` in `index.html` with your actual Gitee username, then push to
  Gitee and enable Gitee Pages in the repo's Services panel.

---

## Stages 8–13 — Optimize · Accessibility · Performance · QA · Docs · Delivery (2026-07-17)

### Files Changed
- `index.html` — `.js` flag + delegated image-error handler in `<head>`; graceful video
  placeholder (replaces the `VIDEO_ID` iframe); favicon links trimmed to the SVG monogram.
- `assets/css/style.css` — 8 module stylesheets bundled into one file (no `@import`);
  `.reveal` gated behind `.js`; added missing-asset + video-placeholder styles.
- `assets/images/profile/profile.jpeg` — resized + recompressed (680 KB → 88 KB).
- `assets/icons/favicon.svg` — new hand-authored monogram (was missing).
- `docs/PERFORMANCE.md` — new performance budgets + Lighthouse prep.
- `ASSET_INVENTORY.md`, `docs/INFORMATION_ARCHITECTURE.md`, `docs/PRD.md` — reconciled with the
  built site (section order, real asset references, font/icon reality).
- `assets/css/*.css` (8 modules) — removed (content folded into `style.css`).

### Why
Finalize the v1.0 build for GitLab Pages: remove render-blocking CSS imports, shrink the LCP
image, fix a no-JS hidden-content bug, replace broken/placeholder assets with graceful
treatments, and bring the spec docs in line with what was actually built.

### Fixes / New
- **CSS:** Single bundled `style.css` (8 → 1 request).
- **CSS:** `.reveal` hidden state now requires `.js`, so no-JS / crawler views stay visible.
- **Images:** Hero `profile.jpeg` 680 KB → 88 KB (87% smaller).
- **Images:** Delegated `error` handler shows a calm placeholder for any missing image instead
  of a broken-icon; dropping the real file at the referenced path fixes it automatically.
- **Video:** `VIDEO_ID` placeholder embed replaced with a labelled placeholder block.
- **A11y (WCAG AA):** Structure audit passed — 10/10 `aria-labelledby` targets resolve, 9/9
  in-page anchors resolve, 7/7 images have alt, no unclosed tags, `lang` set, skip-link present,
  reduced-motion handled in CSS + JS, Escape/outside-click/focus-return on the mobile menu.
- **Favicon:** Added SVG monogram; removed two link references to files that do not exist
  (`favicon.ico`, `apple-touch-icon.png`) to eliminate 404s.

### Known Issues / Pre-launch actions
- **Google Fonts blocked in China** — self-host Fraunces + Manrope woff2 (audience constraint).
- **Missing assets** (user-supplied, not fabricated): 4 certificate thumbnails, contact portrait,
  WeChat QR, CV PDF. Placeholders shown; supply files at the referenced paths.
- **Canonical + OG image** use `github.io`; switch to the live GitLab Pages URL + add a
  1200×630 social preview.
- Mobile menu has no focus trap (AA does not require one; Escape + focus-return implemented).

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
