# Mohammed Shehzad Khan — Digital Portfolio v2

Professional portfolio website for Mohammed Shehzad Khan, an international primary educator and teacher developer with 12 years of experience across India and China.

**Live URL (GitHub Pages):** `https://mdshezkhn.github.io/mo-portfolio-v2/`

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
mo-portfolio-v2/
│
├── index.html               ← Single-page portfolio (full content)
├── README.md                ← This file
├── CHANGELOG.md             ← Version history
├── LICENSE                  ← MIT
├── robots.txt               ← Search engine directives
├── sitemap.xml              ← SEO sitemap
├── manifest.webmanifest     ← PWA/home screen metadata
├── assets/
│   ├── css/
│   │   ├── variables.css    ← Design tokens
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
│   │   ├── utilities.js     ← Image fallbacks
│   │   ├── credentials-registry.js ← Credential data & rendering
│   │   ├── credentials-modal.js  ← Modal display logic
│   │   └── contact-reveal.js     ← Contact channel modals
│   │
│   ├── images/
│   │   ├── profile/         ← Profile photos
│   │   ├── certificates/    ← Certificate thumbnail images
│   │   ├── social/          ← Social sharing images
│   │   └── icons/           ← Favicons and app icons
│   │
│   ├── documents/
│   │   ├── cv/              ← Current CV (internal reference)
│   │   └── artefacts/       ← Teaching artefacts (Q1–Q4 placeholders)
│   │
│   ├── downloads/           ← Public-facing recruiter downloads
│   └── videos/              ← Demo lesson recordings (placeholder)
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
| Fonts      | Self-hosted: Fraunces + Manrope (Google Fonts blocked in China) |
| Deployment | GitHub Pages                                |
| CI/CD      | GitHub Actions                              |
| Version    | Git                                         |

---

## Running Locally

No build step required.

1. Open the `mo-portfolio-v2/` folder in VS Code.
2. Install the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension.
3. Right-click `index.html` → **Open with Live Server**.
4. Visit `http://127.0.0.1:5500/`.

> **Note:** The site uses ES modules (`type="module"` on the script tag). Modules require a server — opening `index.html` directly via `file://` will not load JavaScript. Always use Live Server.

---

## Deployment

### GitHub Pages (Automatic via GitHub Actions)

The site deploys automatically on every push to `main` via GitHub Actions.

1. Push to `main` branch of `mdshezkhn/mo-portfolio-v2`
2. The [deploy.yml](.github/workflows/deploy.yml) workflow builds and deploys the site
3. Your site will be live at `https://mdshezkhn.github.io/mo-portfolio-v2/`

> The canonical URL in `index.html` and sitemap.xml is already set correctly.

---

## How to Update the CV

1. Replace `assets/documents/cv/Mohammed_Shehzad_Khan_CV.pdf` with the new version.
2. If you rename the file, also update the `href` in the two Download CV buttons in `index.html`.
3. Commit and push — the site will redeploy automatically.

---

## How to Update Profile Photo

1. Replace `assets/images/profile/profile.webp` with the new photo.
2. Maintain the same filename to avoid updating HTML.
3. Recommended: 460×575px, WEBP, under 200KB.

---

## How to Update Certificates

Certificate thumbnails are managed automatically via `credentials-registry.js`. To add a new certificate:

1. Add the thumbnail and full document to `assets/images/certificates/`
2. Add an entry to `credentials-registry.js` in the `CREDENTIALS_REGISTRY` array
3. Set `public: true` to surface it on the site
4. Commit and push — the site will redeploy automatically

---

## Core Principles

1. **Evidence over claims** — every statement traceable to a source. All numbers, dates, and achievements are verifiable through documentation.
2. **Nothing AI-invented** — no fabricated achievements, dates, statistics, or testimonials. Content is based on real experience and evidence.
3. **Safeguarding first** — no identifiable students without documented consent. Classroom artefacts avoid student-identifiable material.
4. **Design for longevity** — timeless over trendy. Focus on substance and clarity rather than fleeting design trends.
5. **Accessibility (WCAG 2.1 AA)** — maintained in every update, not just at launch. Semantic HTML, ARIA labels, proper heading hierarchy, and colour contrast ratios.

---

## Credits & Acknowledgements

- Site built and maintained by Mohammed Shehzad Khan
- Icons: Custom SVGs based on Fraunces typeface
- Fonts: Self-hosted Fraunces and Manrope for reliability in China
- Deployment: GitHub Actions for zero-configuration CI/CD
