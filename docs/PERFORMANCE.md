# Performance Budgets & Lighthouse Prep

**Project:** Mohammed Shehzad Khan Portfolio (Project Meridian V2)
**Last updated:** 2026-07-17 (Stage 10)
**Status:** Budgets defined; Lighthouse must be run by a human (no headless Chrome in the
build environment).

---

## 1. Budgets (from PRD §4 + ASSET_INVENTORY)

| Metric | Target | Notes |
|---|---|---|
| Lighthouse Performance (mobile, throttled) | ≥ 90 launch / ≥ 95 post-optimization | |
| Lighthouse Accessibility | 100 | Verified by structure audit (Stage 9) |
| Lighthouse Best Practices | 100 | |
| Lighthouse SEO | 100 | JSON-LD, OG/Twitter, canonical, sitemap all present |
| First Contentful Paint (FCP) | < 1.5 s | Hero image is the LCP element |
| Total CSS | 1 file, < 35 KB | Bundled in Stage 8 |
| Total JS | 1 module + imports, < 10 KB | Deferred (`type="module"`) |
| Images | ≤ 300 KB each | Per ASSET_INVENTORY |
| PDFs | ≤ 5 MB each | Per ASSET_INVENTORY |
| Render-blocking requests | CSS ×1, JS ×1, fonts ×1 | No `@import` chain (removed in Stage 8) |

---

## 2. Optimizations applied (Stage 8)

- **CSS bundled** — 8 modular stylesheets concatenated into a single `assets/css/style.css`.
  Eliminated 8 render-blocking `@import` requests → 1. The single file is the source of truth
  now (edit it directly; the old modules were removed and remain recoverable via git history).
- **Hero image optimized** — `assets/images/profile/profile.jpeg` resized 1600×2400 → 880×1320
  and recompressed (quality 82, progressive) → **680 KB → 88 KB (87% smaller)**. It is the LCP
  element and uses `loading="eager"` + `fetchpriority="high"`.
- **Scroll-reveal gated behind `.js`** — `.reveal` hidden state now applies only with JS active,
  so no-JS users and crawlers always see fully visible content (fixes a hidden-content bug and the
  old flash-of-visible-then-hidden regression).

---

## 3. How to run Lighthouse

No headless Chrome is available in the build environment, so a human must run it:

**Option A — Chrome DevTools**
1. `npm i -g serve` then `serve .` (or open `index.html` via a local static server — *not* `file://`).
2. Open DevTools → Lighthouse → Mobile → check Performance / Accessibility / Best Practices / SEO → Analyze.

**Option B — CLI**
```
npx lighthouse https://<your-gitlab-pages-url> --preset=Mobile --view
npx lighthouse https://<your-gitlab-pages-url> --preset=Desktop --view
```

Run against the **deployed** URL (or a local server) — not the raw `index.html` file — so fonts,
CSS, and the service context resolve correctly.

---

## 4. Known performance risks (pre-launch)

1. **Google Fonts blocked in mainland China.** The site links Google Fonts (Fraunces + Manrope)
   with `preconnect` but no self-hosted fallback. China-based recruiters (a core audience) may see
   a flash or a fallback system font. **Action:** self-host the woff2 files and add
   `font-display: swap` (stack constraint §"Audience"). This is the single biggest remaining
   perf/availability item.
2. **Missing images.** Certificate, portrait, and WeChat-QR images are not yet in the repo
   (see ASSET_INVENTORY). Placeholders are shown until supplied. When added, keep each ≤ 300 KB
   and prefer WebP.
3. **Missing CV PDF.** `assets/documents/Mohammed_Shehzad_Khan_CV.pdf` is not yet supplied; the
   "Download CV" links 404 until added.
4. **Canonical / social OG image** points at `github.io`; update to the live GitLab Pages URL
   (and add a 1200×630 social preview image) before launch.
