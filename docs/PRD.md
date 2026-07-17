# Product Requirements Document (PRD)

## Project: Mohammed Shehzad Khan – Digital Teaching Portfolio

**Version:** 1.2 (Approved)

## 1. Vision
A world-class digital portfolio positioning Mo as a highly credible international educator and emerging educational leader. Story-driven, evidence-first. Not a resume converted into a webpage.

## 2. Objectives
- Increase interview invitations
- Establish professional credibility
- Differentiate from generic ESL teachers
- Showcase evidence rather than claims
- Serve as a long-term professional brand
- Be easy to maintain and expand

## 3. Portfolio Pillars (narrative backbone)
Every section reinforces at least one pillar:
1. **Educator** – who he is in the classroom
2. **Leader** – supporting teachers, quality, school improvement
3. **Researcher** – PGCE work, reflective, evidence-informed practice
4. **Lifelong Learner** – PD, certifications, continual growth
5. **Global Professional** – international experience, cross-cultural competence

## 4. Success Metrics
A recruiter, without scrolling past the first two screens, can answer: Who is this? What impact has he made? Can he teach and lead? Is there evidence? How do I contact him / get his CV?

**Technical acceptance (Lighthouse, mobile, throttled):** Performance >=90 at launch (>=95 post-optimization), Accessibility 100, Best Practices 100, SEO 100. FCP <1.5s.

## 5. Recruiter Journey (Section 22)
- 0–5s: understand who Mo is (Hero)
- 5–15s: see value proposition (Hero + Impact Highlights)
- 15–30s: view evidence of impact (Teaching Impact)
- 30–45s: explore journey and philosophy
- 45–60s: download CV or make contact (persistent nav CTA)

Every section must serve one of these moments or justify its position.

## 6. Target Audience
Primary: international school principals, academic directors, heads of school, HR managers, school owners. Often mobile, sometimes low-bandwidth. Secondary: universities, recruiters, parents, educators, professional network.

## 7. Key Decisions (locked)
- **Single-page architecture** for v1, anchor navigation, descriptive slugs
- **GitLab Pages default URL** for v1; custom domain post-launch
- **Rebuild from scratch**; no code inherited from previous versions
- **Google Fonts + Font Awesome retained for v1** (self-hosting/SVG icons = post-launch optimization backlog)
- **Verified statistics only**; unverifiable stats are omitted, never faked
- **Photos:** authentic; safeguarding-first (see Section 10)

## 8. Navigation
Sticky. Desktop: Logo | My Story | Impact | Philosophy | Leadership | Journey | Research | Moments | Credentials | Contact | [Download CV] (CTA). Mobile: drawer (focus trap, Esc close, scroll lock, aria-expanded). Skip-to-content link first.

## 9. Information Architecture (approved order — six-act narrative, Doc 1C §15)
Single page, anchor navigation, ordered as a cinematic arc (impression → journey →
evidence → classroom → future → invitation):

**Act I – First Impression:** Hero
**Act II – The Journey:** Story → Journey
**Act III – The Evidence:** Impact (Skills & Proficiencies) → Credentials
**Act IV – The Classroom:** Philosophy → Moments (Gallery) → Research
**Act V – The Future:** Leadership & Direction
**Act VI – The Invitation:** Contact → Footer

Testimonials placeholder hidden until real content exists.

## 10. Safeguarding Policy (mandatory)
No identifiable students without documented consent. Prefer environments, materials, adult workshops, or wide shots without identifiable faces. Follow school policies. Every image: consent status logged in ASSETS.md before entering the repo. A safeguarding & ethics statement appears in Credentials.

## 11. Accessibility
WCAG 2.1 AA minimum, Lighthouse 100. Skip link, semantic landmarks, single h1, keyboard support, visible focus, reduced-motion fallbacks for all animation, 44px touch targets, alt text on every image, color never sole indicator. **Accessibility is per-sprint definition of done, not a final audit.**

## 12. Performance & SEO
Lazy-loaded gallery, responsive srcset images, explicit image dimensions (CLS ~0), single minified CSS + JS. JSON-LD Person schema, Open Graph + Twitter cards, canonical URL, sitemap.xml, robots.txt, OG image (1200x630).

## 13. Technology
GitLab Pages, HTML5, CSS3 (custom properties), vanilla JS, Google Fonts (Fraunces + Manrope), Font Awesome (max 8 icons, one style). No frameworks, no build tools.

## 14. Content Principles (hard gate)
Every statement supported by experience, evidence, credentials, or measurable outcomes. Never: invented achievements, inflated numbers, guessed responsibilities, generic motivational phrases. AI must never fabricate: achievements, dates, outcomes, awards, findings, certifications, testimonials, biography, statistics. Placeholder format: `[NEEDS INPUT: description]` — never shippable.

## 15. Roadmap
- **Sprint 0** – Content extraction (see docs/SPRINT0.md)
- **Sprint 1** – Repo/Pages setup, design tokens, layout, nav, hero, footer
- **Sprint 2** – My Story, Philosophy, Journey, Contact
- **Sprint 3** – Teaching Impact, Leadership, Research, Credentials
- **Sprint 4** – Classroom Moments, downloads, Impact Highlights (if verified), testimonials placeholder
- **Sprint 5** – Verification: a11y, SEO, responsive QA, cross-browser (latest 2 Chrome/Safari/Firefox/Edge + mobile), 404 page, deployment

**Definition of done, every sprint:** Lighthouse a11y 100, keyboard pass, no unsourced content, reduced-motion verified.

## 16. Operating Rules
- **Rule A – One Improvement Rule:** each review fixes the single biggest quality improvement first.
- **Rule B – Version Freeze:** approved sprints are frozen; changes go through future sprints.
