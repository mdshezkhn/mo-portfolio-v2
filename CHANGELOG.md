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
