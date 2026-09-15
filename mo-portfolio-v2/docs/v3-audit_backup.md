# Phase 0 Audit: v3 Rebuild Foundation

**Branch:** `v3/rebuild` (checked out from `main`)
**Tag:** `pre-v3` marking current state before changes
**Date:** 2026-09-08

---

## 0.1 Repository Snapshot (pre‑v3)

| Item | State |
|------|-------|
| **Live site** | `https://mdshezkhn.github.io/mo-portfolio-v2/` served from `index.html` |
| **Stack** | Vanilla HTML/CSS/JS ES modules; no build step; server required (`type="module"`); GitHub Pages deploy on push to `main` |
| **Assets** | `assets/css/` (9 files), `assets/js/` (7 files: main.js, navigation.js, animations.js, timeline.js, gallery.js, theme.js, utilities.js), `assets/images/` (profile, certificates, gallery, classroom, leadership, logos, social), `assets/documents/` (CV PDF, certificates, PGCE, publications), `assets/videos/` |
| **CV PDF** | `assets/documents/Mohammed_Shehzad_Khan_CV.pdf` – 93 KB; `pdftotext` extraction untested; known FlateDecode corruption risk (Phase 1 1.1) |
| **Current index.html** | Full single‑page with 10 sections (Hero, Story, Journey, Impact, Credentials, Philosophy, Moments, Research, Leadership, Contact). JSON‑LD structured data present. |
| **Design system fork** | `VISUAL_IDENTITY.md` specifies dark violet (`--bg:#0B0B0D`, `--accent:#7C5CFC`); live build is light navy (`--bg:#F8FAFC`, `--accent:#1E3A5F`). 2A §12 describes “natural light, open spaces” → **light/navy is the truth** (per master plan). |
| **Sprint 0 master plan** | `docs\SPRINT0.md` defines content‑extraction tasks (Hero, Story, Teaching Impact, Philosophy, Leadership, Research, Classroom Moments, Credentials). |
| **Recruiter Objection Map** | `docs\RECRUITER_OBJECTION_MAP.md` lists 11 recruiter objections + evidence gaps. |
| **Content Inventory** | `docs\CONTENT_INVENTORY.md` tracks section completeness; most sections 🟡 In Progress, gated on missing assets. |
| **Asset Register** | `ASSETS.md` lists pending user‑supplied assets: headshot, CV PDF, certificates, email, WeChat QR, classroom photos, teaching video, OG image, favicon set. |
| **Unverified / sensitive items** | Harris University M.A. (2007‑2009) unverified; 2009‑2014 employment gap flagged; “Zhejiang University — Helen China TEFL Network” affiliation present; three name renderings on certificates vs. site name. |
| **Dead code** | `timeline.js`, `theme.js`, `gallery.js` are stubs (imported but inert). |
| **Redundant / orphan files** | `_before.html`, `live_index.html`, `backups/`, `_qa_shots/` referenced in master plan → to be moved to `archive/` after confirmation. |

---

## 0.2 Audit Findings (aligned to Phase 0‑1.4 requirements)

### Claims / Evidence gaps (from Content Inventory & Recruiter Objection Map)

| Section | Gap | Priority (Must/Should/Nice) |
|---------|-----|-----------------------------|
| **Hero** | CV download 404 (`assets/documents/Mohammed_Shehzad_Khan_CV.pdf` currently broken) | **Must** |
| **Credentials** | Languages list missing (CONTENT_BLUEPRINT Must) | **Must** |
| **Credentials** | Safeguarding & ethics statement missing (PRD §10 Mandatory) | **Must** |
| **Credentials** | Harris University M.A. unverified → must confirm or remove (master plan §2.7) | **Must** |
| **Journey / Timeline** | Bullets describe duties, not measured outcomes (2A §7/§8) | **Should** |
| **Impact** | No dedicated Tier‑1 evidence cards (blueprint) | **Should** |
| **Philosophy** | Only 3 pillars vs. spec's 450‑700 w / six topics (CONTENT_BLUEPRINT Must) | **Must** |
| **Moments / Gallery** | Placeholder images + captions claiming “Authentic moments... student faces blurred” without actual photos (Phase 1 1.3) | **Must** (gallery removal) |
| **Research** | Missing “how this changed my classroom” (CONTENT_BLUEPRINT Must) | **Must** |
| **Leadership** | Only 2 pillars vs. spec's 2‑4 LEADER cards + 3‑4 principles | **Should** |
| **Contact** | Hotmail address possibly obsolete; WeChat/WhatsApp QR codes need confirmation for international recruiter experience (Phase 3 1) | **Should** |
| **Profile portrait** | Current portrait may have “white wash”; need neutral professional portrait (460×575, ≤200 KB) (Phase 3 3) | **Should** |
| **Timeline** | 7 roles present; bullets are duty‑language; need ACTION+CONTEXT+verified OUTCOME rewrite (Phase 2 6) | **Should** |
| **CV content** | Remove “Master's level (PGCE7002)” (PGCE is non‑QTS); standardize name to legal/passport name; remove “Zhejiang University — Helen China TEFL Network” unless confirmed | **Must** (Phase 1 1.1) |
| **Gallery captions** | Currently claim images exist; must remove immediately; Phase 2 replaces with “Classroom in Practice” pending real photos | **Must** (Phase 1 1.3) |
| **Name variants** | Certificates show three name renderings vs. “Mohammed Shehzad Khan”; need exact passport spelling for note (Phase 1 1.4) | **Must** |

### Technical defects (Phase 0 safety net)

| Defect | Status | Required fix |
|--------|--------|--------------|
| **PDF corruption** | PDF has malformed FlateDecode streams; may render blank in non‑Chromium viewers | **Must** – create `cv.html` → generate clean PDF; validate with `pdftotext` + `qpdf --check` |
| **Mobile scroll‑reveal bug** | On mobile, Journey & Impact sections get stuck at `opacity:0` | **Must** – invert mechanism: visible by default; JS‑added `js-reveal-ready` class may hide‑then-reveal; IntersectionObserver with `threshold:0`, generous rootMargin, 3‑sec fallback timer, `window.load` force‑reveal; `prefers-reduced-motion` support |
| **JS‑off readability** | Site must be fully readable without JavaScript | **Must** – already gated via `.no-js` → `.js` class; verify full page readable |
| **Contrast** | Audit every text/background pair ≥ 4.5:1 WCAG 2.1 AA (variables.css) | **Must** |
| **Mobile breakpoints** | Test at 320/375/390/768/1024/1440/1920 px; no horizontal scroll; CTAs visible; modals work | **Must** |
| **Zero broken links, relative paths** | All asset paths must remain relative (subpath `/mo-portfolio-v2/`) | **Must** |
| **Lighthouse scores** | Run before/after; report mobile scores | **Should** |

### Design‑system fork (Phase 3 4)

- **Dark violet vs. light navy** → adopt light/navy build as truth; revise `VISUAL_IDENTITY.md` to match (2A §12 “natural light, open spaces”). 
- **Icons**: spec says Font Awesome (max 8); build uses emoji + inline SVG → formalise as inline SVG/unicode, no icon font. 
- **Typography**: Google Fonts blocked in China → build self‑hosts (keep). 
- **Spacing**: no tokens → extract `--space-*` tokens in Stage 4. 
- **Motion distance**: tighten reveal from 20 px → 8‑12 px (VISUAL_IDENTITY.md §15). 

### Dead‑code / orphan cleanup (Phase 4)

- Move `_before.html`, `live_index.html`, `backups/`, `_qa_shots/` into `archive/` after confirming no references.
- Remove stub `theme.js` (dark mode not in 2A scope).
- Decide fate of `timeline.js` (timeline needs no JS) or keep as no‑op.

---

## 0.3 Consolidated Question List for the User

*All questions are grouped here; answer at your convenience. Responses will inform the V3 rebuild and are **not** on the live site.*

1. **Legal/passport name** (Phase 1 1.1, 1.4):
   - What is the exact passport spelling? The site currently shows "Mohammed Shehzad Khan". Certificates render three variants; confirm which is the canonical passport name and how to handle the others.

2. **Zhejiang University affiliation** (Phase 1 1.1):
   - Should the "Zhejiang University — Helen China TEFL Network" affiliation be removed from the CV, or do you confirm it?

3. **Harris University M.A. verification** (Phase 2.7, master plan §2.7):
   - Can you verify the Harris University M.A. (2007‑2009) accreditation? If not, it must be removed from the site and CV entirely.

4. **Safeguarding training details** (Phase 2.7):
   - Do you have current safeguarding/child‑protection training details to add under the Credentials heading? If not, a placeholder is acceptable.

5. **QTS pathway plan wording** (Phase 2.7):
   - What one‑sentence QTS pathway plan should appear? (e.g., "I am pursuing Qualified Teacher Status via…") – do not invent.

6. **Hotmail address replacement** (Phase 3 1):
   - What is your preferred replacement email address for the Hotmail (`mdshezkhn@hotmail.com`)? Update both site and `cv.html` together.

7. **Neutral professional portrait** (Phase 3 3):
   - Do you have a new neutral professional portrait (460×575 px, ≤200 KB, no white wash) to replace the current thumbs‑up portrait? If not, we can use the existing one with the white‑wash fixed via `onerror` fallback to a styled monogram.

8. **Teaching video** (Phase 2.5):
   - Do you have a teaching video (demo lesson)? If yes, provide year group, subject, and "what‑to‑watch‑for" notes (no autoplay; safeguarding first; keep clips short). If no, the "See Me Teach" CTA stays empty until you supply one.

9. **Gallery / Classroom photos** (Phase 1.3, 2.5):
   - Do you have real classroom photos with documented consent (faces blurred acceptable)? If yes, provide them (~1200 px, ≤150 KB, WebP + JPEG fallback, descriptive alt text). If no, the gallery must be removed now and replaced with a holding statement asking for photos.

10. **Research evidence for flagship case studies** (Phase 2.3):
    - **Case Study 1** ("Increasing Participation Through Teacher Questioning"): Do you have the PGCE practitioner research document/PDF? Any data/excerpts to visualise?
    - **Case Study 2** ("EAL + STEM"): Do you have a real lesson/project with classroom evidence (photos, materials, student work)? Verified outcomes only.
    - **Case Study 3** ("Developing Teachers, Not Just Lessons"): Do you have mentoring/training materials, anonymised feedback, or evaluation summaries?

11. **Impact metrics verification** (Phase 2.2, 2.6):
    - The CV states "more than 200 educators" trained at GEDU – confirm this figure is correct for use on the site.
    - Any other verified statistics (years, schools, students) you want highlighted?

12. **Availability phrasing** (Phase 2 hero):
    - The hero states "Available August 2027". Is this accurate, or should it be adjusted (e.g., "open to opportunities late 2026")?

13. **Languages list** (Phase 2.7):
    - What six languages should appear in the visual strip near the hero or under Credentials? Provide the languages and any proficiency labels you wish to surface.

14. **Footer nav repeat + social links** (Phase 3 2):
    - The spec wants a quiet nav repeat + social links in the footer. Do you want the current LinkedIn + email only, or add any other links (e.g., WeChat, GitHub)?

15. **Design tokens / spacing** (Phase 3 4):
    - Any preference on extracting `--space-*` tokens from the current CSS, or shall I proceed with the light/navy theme as‑is?

16. **Any other content or constraints**:
    - Is there any other content, claim, or design preference you want to surface before the rebuild proceeds?

---

## 0.4 Acceptance Criteria for Phase 0

- ✅ Branch `v3/rebuild` exists and is checked out.
- ✅ Tag `pre-v3` created at current HEAD.
- ✅ Audit notes written to `docs/v3-audit.md`.
- ✅ Consolidated question list documented above (user will answer).
- ✅ No code changes merged until user responses are received (or reasonable defaults applied as described in the master prompt).

---

*End of Phase 0 Audit.*