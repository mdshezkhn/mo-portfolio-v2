# Mohammed Shehzad Khan — Digital Portfolio

Professional portfolio website for Mohammed Shehzad Khan, an international primary educator with 10+ years of experience across India and China.

**Live URL (GitHub Pages):** `https://mdshezkhn.github.io/mo-portfolio/`

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Technology Stack](#technology-stack)
4. [Running Locally](#running-locally)
5. [Deployment](#deployment)
6. [How to Update the CV](#how-to-update-the-cv)
7. [How to Update Profile Photo](#how-to-update-profile-photo)
8. [How to Update Certificates](#how-to-update-certificates)
9. [Core Principles](#core-principles)

---

## Project Overview

A recruiter-focused professional platform designed to be credible, maintainable, and accessible. It is built with zero dependencies — pure HTML, CSS, and vanilla JavaScript.

**Target audience:** International school recruiters, principals, academic directors, and HR managers.

---

## Folder Structure

```
mo-portfolio/
│
├── index.html               ← Single-page portfolio (full content)
├── README.md                ← This file
├── CHANGELOG.md             ← Version history
├── LICENSE                  ← MIT
├── robots.txt               ← Search engine directives
├── sitemap.xml              ← SEO sitemap
├── manifest.webmanifest     ← PWA/home screen metadata
├── favicon.ico              ← Browser tab icon
│
├── assets/
│   ├── css/
│   │   ├── style.css        ← Master @import entry point
│   │   ├── variables.css    ← All design tokens
│   │   ├── reset.css        ← Browser normalisation + accessibility
│   │   ├── typography.css   ← Heading scale, badges, eyebrow
│   │   ├── layout.css       ← Container and section spacing
│   │   ├── components.css   ← Nav, buttons, cards
│   │   ├── sections.css     ← Section-specific layouts
│   │   ├── animations.css   ← Scroll-reveal and hero keyframes
│   │   └── responsive.css   ← Breakpoint overrides
│   │
│   ├── js/
│   │   ├── main.js          ← Entry point (imports all modules)
│   │   ├── navigation.js    ← Mobile menu + active section
│   │   ├── animations.js    ← Header shadow + scroll-reveal
│   │   ├── timeline.js      ← Stub (Sprint 4)
│   │   ├── gallery.js       ← Stub (Sprint 5)
│   │   └── theme.js         ← Stub (Sprint 6)
│   │
│   ├── images/
│   │   ├── profile/         ← profile.jpeg (hero portrait)
│   │   ├── certificates/    ← Certificate thumbnail images
│   │   ├── hero/            ← Hero background images
│   │   ├── classroom/       ← Classroom photography
│   │   ├── leadership/      ← Leadership and PD photos
│   │   ├── gallery/         ← Gallery images
│   │   └── logos/           ← School/organisation logos
│   │
│   ├── documents/
│   │   ├── cv/              ← Current CV (internal reference)
│   │   ├── certificates/    ← Scanned certificates
│   │   ├── pgce/            ← PGCE-related documents
│   │   └── publications/    ← Research papers
│   │
│   ├── downloads/           ← Public-facing recruiter downloads
│   ├── icons/               ← Favicons, apple-touch-icon, manifest icons
│   └── videos/              ← Demo lesson recordings
│
├── docs/                    ← PRD, visual identity, architecture docs
├── archive/                 ← Previous CSS versions (not served)
└── .github/
    └── workflows/
        └── deploy.yml       ← GitHub Actions auto-deploy
```

---

## Technology Stack

| Layer      | Technology                                  |
|------------|---------------------------------------------|
| Markup     | HTML5 (semantic, ARIA-labelled)             |
| Styling    | Vanilla CSS (modular, no framework)         |
| Script     | Vanilla JavaScript ES Modules (no build)    |
| Fonts      | Google Fonts: Fraunces + Manrope            |
| Deployment | GitHub Pages · GitLab Pages · Gitee Pages   |
| CI/CD      | GitHub Actions · GitLab CI/CD               |
| Version    | Git                                         |

---

## Running Locally

No build step required.

1. Open the `mo-portfolio/` folder in VS Code.
2. Install the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension.
3. Right-click `index.html` → **Open with Live Server**.
4. Visit `http://127.0.0.1:5500/`.

> **Note:** The site uses ES modules (`type="module"` on the script tag). Modules require a server — opening `index.html` directly via `file://` will not load JavaScript. Always use Live Server.

---

## Deployment

### GitHub Pages

1. Create a repository at `github.com` (e.g. `mdshezkhn/mo-portfolio`).
2. Add the remote: `git remote add origin https://github.com/mdshezkhn/mo-portfolio.git`
3. Push: `git push -u origin main`
4. In GitHub repo → **Settings** → **Pages** → Source: **GitHub Actions**.
5. The [deploy.yml](.github/workflows/deploy.yml) workflow will auto-deploy on every push to `main`.
6. Your site will be live at `https://mdshezkhn.github.io/mo-portfolio/`.

> Update the `canonical` URL in `index.html` and the Sitemap/robots.txt with your actual URL.

---

### GitLab Pages

1. Create a project at `gitlab.com` (e.g. `mdshezkhn/mo-portfolio`).
2. Add the remote: `git remote add gitlab https://gitlab.com/mdshezkhn/mo-portfolio.git`
3. Push: `git push gitlab main`
4. The [.gitlab-ci.yml](.gitlab-ci.yml) pipeline will auto-deploy on every push.
5. In GitLab project → **Deploy** → **Pages** to see your Pages URL.

---

### Gitee Pages

1. Create a repository at `gitee.com` (e.g. `mdshezkhn/mo-portfolio`).
2. Add the remote: `git remote add gitee https://gitee.com/mdshezkhn/mo-portfolio.git`
3. Push: `git push gitee main`
4. In Gitee repo → **Services** → **Gitee Pages** → select `main` branch → **Deploy**.

> Gitee Pages may require email/phone verification. The site uses only relative asset paths so it works on all three platforms without changes.

---

## How to Update the CV

1. Replace `assets/documents/cv/Mohammed_Shehzad_Khan_CV.pdf` with the new version.
2. If you rename the file, also update the `href` in the two Download CV buttons in `index.html`.
3. Commit and push — the site will redeploy automatically.

---

## How to Update Profile Photo

1. Replace `assets/images/profile/profile.jpeg` with the new photo.
2. Maintain the same filename to avoid updating HTML.
3. Recommended: 460×575px, JPEG, under 200KB.

---

## How to Update Certificates

1. Add new certificate thumbnail images to `assets/images/certificates/`.
2. Add a new `.cert-card` block to the Certifications section of `index.html`.
3. Follow the existing pattern (`cert-thumb`, `cert-name`, `cert-issuer`, `cert-desc`).

---

## Core Principles

1. **Evidence over claims** — every statement traceable to a source.
2. **Nothing AI-invented** — no fabricated achievements, dates, statistics, or testimonials.
3. **Safeguarding first** — no identifiable students without documented consent.
4. **Design for longevity** — timeless over trendy.
5. **Accessibility (WCAG 2.1 AA)** — maintained in every update, not just at launch.
