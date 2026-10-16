# Changelog

All notable changes to this portfolio are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## Versioning Policy

- **v1.x** — Bug fixes, evidence additions, updated CV, new qualifications. No structural changes.
- **v2.0** — Structural redesign or major repositioning. Requires justification.
- **v3.0** — Significant career change (e.g., moving into leadership). Full rebuild warranted.

**Feature freeze:** No structural redesigns or messaging changes unless driven by recruiter feedback or significant new evidence (new qualification, published research, recommendation, award, teaching video).

**Allowed without justification:** Adding new evidence, updating dates, fixing bugs, correcting errors.

---

## [2.0.0] - 2026-10-17 — Talking-video rebuild

### Changed
- **Full rebuild as a Next.js 15 "talking-video" portfolio** (React 19, TypeScript, Tailwind CSS 4, Lenis — the only animation dependency). Static export deployed via the updated GitHub Pages workflow (build step added, uploads `out/`).
- New art direction: quiet premium paper/ink/gray system (`--paper #f4f2ee`), Inter Tight + Instrument Serif italic accent + JetBrains Mono, self-hosted via `next/font/local`.
- Sections: Hero (talking video, seamless loop, mix-blend multiply, sound toggle) → About (hanging lanyard TEACHER ID card, pendulum physics, flip) → Skills (periodic table + sticky inspector, official brand logos) → Work (expanding accordion gallery, grayscale illustrative mini-UIs) → Certifications (ink-flood index) → Experience (scroll-drawn timeline) → Achievements (pinned horizontal gallery, count-up numbers) → Contact (letter-hop heading, copy-email chip, spinning badge).
- All content moved to `src/lib/data.ts`, sourced exclusively from the résumé PDF; achievements use only verifiable counts (publication-policy compliant — no 200+/1,000+ claims).
- First-load JS ≈ 129 kB. `npm run build` passes clean.

### Added
- `scripts/build-hero-assets.py` — ffmpeg pipeline: person detection/auto-crop, background whitening, seamless video+audio cross-fade loop, hero.mp4 (H.264/AAC) + hero.webm (VP9/Opus), portrait-bust; `--placeholder` mode generated the current silent breathing-zoom hero from the portrait photo.
- `public/og.jpg` (1200×630), self-hosted fonts in `src/fonts`, brand logos in `public/logos` (simple-icons CC0 + hand-drawn Microsoft mark) with LICENSE.
- Résumé copied to `public/resume/` for the Résumé ↓ buttons.

### Preserved
- Previous static site fully retained under `legacy/` (and git history); repo docs unchanged.

---

## [1.0.0] - 2026-07-22

### Added
- Production CV as ATS-optimised HTML (`assets/documents/Mohammed_Shehzad_Khan_CV.html`)
- 6 role-specific cover letter variants (Primary English, EAL, Homeroom, Curriculum Coordinator, Head of English, Academic Coordinator)
- LinkedIn ready-to-paste rewrites (headline, about, 7 experience sections, skills)
- Evidence library structure with READMEs (`evidence/teaching/`, `evidence/research/`, `evidence/leadership/`, `evidence/professional/`, `evidence/qualifications/`)

### Fixed
- Portfolio canonical URL: `/portfolio/` → `/mo-portfolio-v2/`
- Open Graph and Twitter Card image URLs
- JSON-LD structured data (url, image, jobTitle, knowsAbout)
- `robots.txt` sitemap URL
- `sitemap.xml` canonical URL
- Meta description and keywords (added EAL, PGCE, Curriculum, Differentiated Instruction, Safeguarding)

### Changed
- Hero description: trimmed from dense paragraph to 4 clear sentences
- Stat card "15+ Years Professional Experience" → "7 Schools Across 2 Countries"
- "high school, middle school, kindergarten, and primary" → "kindergarten through secondary"
- "Contributed to quality assurance" → "Conducted quality assurance audits"
- "supported international professional development" → "designed and facilitated"
- "The science degree is not incidental" → "The physics degree directly supports"
- "Grow into curriculum or instructional leadership roles" → "contribute to curriculum development and instructional leadership"
- Cover letter: "contributed to instructional quality" → "drove instructional quality"

### Verified
- Employer names consistent across CV, LinkedIn rewrites, portfolio (Aoxin, GEDU, WhiteHat Jr, Eton House, Helen, Scholars Academy)
- Dates consistent across all assets
- Qualifications consistent (PGCE, B.Ed, M.A., B.Sc.)
- Heading hierarchy correct (h1 → h2 → h3 → h4 → h5)
- All images have alt text
- ARIA labels present (25+ attributes)
- Skip link present for accessibility

### Known Limitations
- CV PDF not yet generated from HTML (open HTML in browser, Print → Save as PDF)
- Evidence library folders are empty — need real documents populated
- Portfolio teaching demonstration video placeholder remains
- Portfolio CV download button links to HTML version (not PDF)
- Live site not yet validated against deployment
- LinkedIn not yet updated with rewrites
- No git tag created yet

---

## Pre-1.0 History

### Planning Phase
- Professional brand audit (CV, LinkedIn, portfolio)
- ATS keyword analysis
- Recruiter simulation
- Consistency matrix
- Improvement roadmap

### Building Phase
- Portfolio redesign and SEO optimisation
- CV creation and iteration
- LinkedIn rewrite drafts
- Cover letter generation
- Evidence library structure
