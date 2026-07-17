# Release Plan — Mohammed Shehzad Khan Portfolio

**Purpose:** Defines what "done" means at each release milestone.
Prevents scope creep. Keeps the project moving forward.

**Not public.** Not deployed.

---

## Release Overview

| Release | Name | Status | Goal |
|---|---|---|---|
| 0.9 | Foundation | ✅ **Complete** | Architecture, CI/CD, Git, deployment-ready |
| 1.0 | Recruiter Ready | 🟡 In Progress | First public version — live URL |
| 1.1 | Evidence | ⬜ Planned | Gallery, video, certificates, research |
| 2.0 | Professional Brand | ⬜ Planned | Blog, interactive timeline, portfolio PDF |

---

## Release 0.9 — Foundation ✅ Complete

**Completed:** 2026-07-17

### What was delivered
- [x] Scalable folder structure (`assets/css/`, `assets/js/`, `assets/images/`, `assets/documents/`, `assets/downloads/`)
- [x] Modular CSS architecture (8 focused files, `@import` chain, zero duplication)
- [x] Modular JavaScript (6 ES modules: navigation, animations + 4 stubs)
- [x] Complete HTML (`index.html`) with all sections written
- [x] SEO metadata (OG, Twitter Card, JSON-LD, canonical, sitemap, robots.txt)
- [x] Git repository with clean history
- [x] GitHub Actions deploy workflow (`.github/workflows/deploy.yml`)
- [x] GitLab CI/CD pipeline (`.gitlab-ci.yml`)
- [x] `private/` folder outside repo for sensitive documents
- [x] `ASSET_INVENTORY.md` — file tracking
- [x] `docs/CONTENT_MAP.md` — section-to-asset mapping
- [x] `docs/CONTENT_INVENTORY.md` — section completeness tracking
- [x] Naming convention: `YYYY-Category-Description.ext`
- [x] Placeholder READMEs in `downloads/`, `documents/`, `images/`, `videos/`

---

## Release 1.0 — Recruiter Ready 🟡 In Progress

**Target:** Before first job application of the 2027 hiring cycle

### Exit criteria (ALL must be met)

#### Content
- [ ] Professional headshot (WebP, ≤200KB, 460×575px)
- [ ] CV (PDF, final version, date-stamped filename)
- [ ] Teaching Philosophy (1–2 pages, PDF)
- [ ] Certificate thumbnail images × 4 (PGCE, TESOL, TEFL, British Council)
- [ ] Employment timeline is accurate and complete
- [ ] Contact details verified (email, phone, LinkedIn, WeChat)

#### Code
- [ ] Hero photo `src` → new headshot
- [ ] CV download `href` → final PDF
- [ ] Certificate image `src` → new thumbnail filenames
- [ ] Canonical URL → actual deployed GitHub Pages URL
- [ ] OG image URL → actual deployed URL

#### Deployment
- [ ] GitHub repository live
- [ ] GitHub Pages enabled and verified
- [ ] All assets load (no 404s)
- [ ] All links work (CV, LinkedIn, email, phone)
- [ ] Mobile layout verified on a real device
- [ ] Console error-free

#### Quality
- [ ] All images have descriptive `alt` text
- [ ] No images over 300KB
- [ ] Lighthouse Performance ≥ 90
- [ ] Lighthouse Accessibility ≥ 95
- [ ] Lighthouse SEO ≥ 95

---

## Release 1.1 — Evidence ⬜ Planned

**Target:** 4–6 weeks after Release 1.0

### Planned additions
- [ ] Classroom gallery section (`<section id="gallery">`)
- [ ] Classroom photos (minimum 3, safeguarding verified)
- [ ] Demo lesson video (YouTube embed or self-hosted)
- [ ] Certificate download links (PGCE, TESOL, TEFL PDFs)
- [ ] Leadership / training photos
- [ ] GitLab Pages verified
- [ ] Gitee Pages verified (China access from Zhengzhou)

---

## Release 2.0 — Professional Brand ⬜ Planned

**Target:** After securing next position (long-term)

### Planned additions
- [ ] Blog / professional articles section
- [ ] Interactive timeline (JavaScript expansion of current timeline)
- [ ] Project case studies (curriculum design, STEM projects)
- [ ] Downloadable portfolio PDF (single document for recruiters)
- [ ] Dark mode toggle (`theme.js` module activated)
- [ ] Self-hosted fonts (remove Google Fonts dependency — China compatibility)

---

## Operating Rules

1. **No new features during a release.** If an idea comes up mid-release, add it to the next release's planned section.
2. **Test before commit.** Open Live Server and verify visually before `git commit`.
3. **One section at a time.** Don't start wiring the gallery until the hero photo is working.
4. **Update the Content Inventory** after every session. The checklist is the source of truth.
5. **Never upload to `private/`.** That folder is outside the repo. Sensitive documents stay there.
