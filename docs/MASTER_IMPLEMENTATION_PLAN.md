# PROJECT MERIDIAN V2 — MASTER IMPLEMENTATION PLAN

**Status:** Stage 3 deliverable (Audit → Plan). Not yet approved.
**Governing documents:** 1A `Agent.md` · 1B Engineering Constitution · 1C AI Decision Framework (incl. §16 Stage Gate) · **2A Creative Brief & Recruiter Psychology** (Creative Constitution) · 2 Creative Brief · `VISUAL_IDENTITY.md` · `INFORMATION_ARCHITECTURE.md` · `PRD.md` · `CONTENT_BLUEPRINT.md`.
**Authority order:** 1A > 1B > 1C > 2A/2 > component specs. Where 2A and an older spec conflict, **2A wins** (it is the current Creative Constitution).
**Hard rule:** No site code changes until this plan is self-reviewed and approved.

---

## 0. EXECUTIVE SUMMARY

The `mo-portfolio-v2` build is **structurally complete and already aligned with 2A's most important directive** — *technology must quietly reinforce credibility and disappear* (§18 Trust Equation omits animation; §19 avoid-list). There is no GSAP, no Three.js, no scroll library; only 9 CSS reveals + a restrained hero entrance, fully gated behind `prefers-reduced-motion`. The six-act arc, semantics, and accessibility scaffolding are solid.

The gaps are **not animation or architecture — they are (a) a design-system divergence, (b) missing content/sections required by the approved specs, and (c) absent user assets.** The single largest brief gap is the **§9 "Gallery → Authenticity" beat**, which is currently only a video placeholder with zero classroom photos.

**Top 5 actions (priority order):**
1. **Reconcile `VISUAL_IDENTITY.md` to the live light/navy theme** (the approved spec describes a dark violet theme the build does not use; 2A's "natural light / open spaces / campus" mood supports light). *Governance truth.*
2. **Build the Classroom Moments gallery** (real grid + lightbox with graceful fallbacks) — closes §9.
3. **Close spec-mandated compliance gaps**: safeguarding & ethics statement (PRD §10), Research "how this changed my classroom" (CONTENT_BLUEPRINT Must), languages list (CONTENT_BLUEPRINT Must), CV-download 404.
4. **Expand under-developed sections** to spec depth: Philosophy (6 topics), Leadership (cards + principles), Credentials (languages + safeguarding).
5. **Wire the asset pipeline** (align `ASSET_INVENTORY.md` paths/names with actual HTML; verify supplied assets).

---

## 1. CURRENT ARCHITECTURE ANALYSIS

- **Stack:** HTML5 + modular CSS (8 files + fonts.css) + vanilla ES-module JS. **No build step, no frameworks** — satisfies 1A/1B/1C stack constraints and GitLab Pages deploy.
- **Structure:** Single page, 10 `<section>` acts in correct six-act order (`index.html:124-572`), each with `aria-labelledby`, wrapped in `<main tabindex="-1">` with a skip link. Nav deep-links resolve.
- **CSS modules** (`assets/css/`): `variables → reset → typography → layout → components → sections → animations → responsive → fonts`. Loaded in cascade order (parallel, non-blocking — the old `@import` chain was removed). Components.css uses a clean "shared token + unique-property-only" discipline (§2–§11).
- **JS modules** (`assets/js/`): `main.js` (entry, imports + inits), `navigation.js` (focus-trapped mobile menu, Escape, outside-click, `aria-current` scroll-spy), `animations.js` (header shadow + IntersectionObserver reveals, reduced-motion aware), `utilities.js` (`initImageFallbacks`), plus **three stub modules** (`gallery.js`, `theme.js`, `timeline.js` — see §6).
- **No active external requests.** Only a commented-out YouTube embed, plus LinkedIn/canonical/schema URLs that are not network fetches. Fully self-contained → China-friendly.
- **Deploy:** `mo-portfolio-v2` is its own git repo with `.gitlab-ci.yml`. Working dir "Mo Digital Portfolio" is not versioned; the sub-repo is.

**Verdict:** Architecture is sound and on-constitution. No rewrite needed; this is refinement, not rebuild.

---

## 2. CONTENT AUDIT

| Section | State | Notes |
|---|---|---|
| Hero | Strong | Real portrait exists (`profile.jpeg`). Value prop ≈14 words (2A §6). CTAs present. |
| Story | Good | ~310 words (spec ≤250 — slightly over, acceptable). First-person, on-voice. |
| Journey | Strong data, weak *evidence* | Timeline is real & sourced, but bullets describe **responsibilities, not measured outcomes** — soft on 2A §7/§8 "evidence of impact". |
| Impact | Adequate | Stats (10+ yrs, 2 countries, 4 schools, MA/PGCE/B.Ed/B.Sc) + skill chips. **No dedicated "Tier 1 evidence cards"** the blueprint calls "Teaching Impact" (Must). |
| Credentials | Partial | Education + certs + "Professional Development Roadmap" present. **Missing: languages list (Must), safeguarding statement (PRD §10 Mandatory), "Currently Learning" label.** |
| Philosophy | Under-developed | 1 quote + 2 pillars vs spec's 450–700 words / six topics. |
| Moments | **Empty** | Video placeholder only. No image gallery. §9 Authenticity beat absent. |
| Research | Partial | Real title/grade/marker. **Missing: "how this changed my classroom" (Must) + publications slot (Nice).** |
| Leadership | Under-developed | 2 pillars vs spec's 2–4 LEADER cards + 3–4 principles. |
| Contact | Good | Email/phone/LinkedIn present. Footer is copyright-only (spec wants quiet nav repeat). |

**Content-accuracy flag (Doc 1A "never invent"):** "Harris University" MA (2007–2009) and the 2009–2014 employment gap are unverified. Not asserted as false; **require user confirmation before deploy.** Also verify "Schools: 4" against the 7 organisations in the Journey timeline.

---

## 3. UI/UX AUDIT

**Strengths:** Clear hierarchy; generous whitespace (112px section padding = 2A §12 "design should breathe"); editorial Fraunces/Manrope; working mobile drawer with focus trap; restrained, purposeful motion; hero portrait loads first on mobile (`order:-1`).
**Gaps:**
- **§9 Gallery/Authenticity beat missing** (see §2/§12).
- **Footer** is copyright-only; spec wants a quiet nav repeat + social links (2A §14 hierarchy).
- **Nav label "Gallery"** points to `#moments` (a video placeholder) — promises a gallery that doesn't exist. Mislabel.
- **Emoji icons** (↓ ✔ 📍) deviate from the "Font Awesome, max 8" spec and read slightly less premium than 2A's elegant/editorial personality (§11/§15). Recommend inline SVG.
- **No journey wayfinding** (2A §16 "know where you've been / are / going"). A subtle scroll-progress indicator could reinforce the metaphor without being flashy — optional.

---

## 4. ACCESSIBILITY AUDIT (WCAG 2.1 AA target)

**Strengths:** Skip link; semantic landmarks; single `<h1>`; `aria-labelledby` per section; focus-trapped mobile menu; `aria-expanded`/`aria-current`; visible `:focus-visible` (3px accent); full `prefers-reduced-motion` support; `alt` on all present images; image fallbacks carry `role="img"`+`aria-label`.
**Gaps (minor):**
- `video-placeholder` uses `role="img"` with text children — acceptable (aria-label wins) but semantically loose.
- Mobile nav link tap targets ≈40px (spec wants ≥44px).
- `contact-portrait.jpg` and cert/QR `<img>`s: ensure `loading="lazy"` where below fold (certs have it; contact-portrait does not).

**Verdict:** Strong baseline; no blocking a11y defects. Final AA pass is Stage 9.

---

## 5. PERFORMANCE AUDIT

**Strengths:** Self-hosted woff2 + `font-display:swap` (China-safe, no FOIT); no external requests; tiny JS (modules, `defer`); hero `loading="eager"` + `fetchpriority="high"` for LCP; modular CSS parallel-loaded; explicit `width/height` on most imgs (CLS guarded).
**Opportunities (Stage 8/10):**
- **Lighthouse not yet run** (needs Chrome locally) — Stage 10 gate.
- Optional: bundle the 8 CSS files or inline critical CSS to cut requests.
- Verify/compress `profile.jpeg` (target ≤300KB per `ASSET_INVENTORY.md`).
- Add `loading="lazy"` to `contact-portrait.jpg`.
- **Estimate:** likely Lighthouse Perf ≥90 / A11y 100 given the minimal footprint — but unverified.

---

## 6. TECHNICAL DEBT ANALYSIS

1. **Three stub JS modules imported and invoked but inert:** `gallery.js`, `theme.js`, `timeline.js` (Sprint 4/5/6 placeholders). `initGallery()` (no-op) means the Moments gallery has no behaviour; `initTheme()` implies dark mode that does not exist; `initTimeline()` implies interactivity that doesn't exist. → **Implement gallery.js (lightbox); remove theme.js (dark mode not in 2A scope) and timeline.js (timeline needs no JS) — or document as intentional.** Per 1C §8 "Remove It Test", dead code should go.
2. **Redundant `.reveal` class** hardcoded in HTML *and* added by `animations.js`. Harmless; can simplify by letting JS own it.
3. **CV download 404** — `assets/documents/Mohammed_Shehzad_Khan_CV.pdf` absent; the link has no graceful fallback (only `<img>`s get fallbacks). Needs a "available on request" state or the real file.
4. **Asset-path drift** — HTML references `certificates/*.jpg`, `wechat-qr.jpg` (root), `contact-portrait.jpg` (root), `profile.jpeg`; `ASSET_INVENTORY.md` expects dated `*.webp` in subfolders. The pipeline is misaligned (see §10/§11).

---

## 7. ANIMATION OPPORTUNITIES (constrained by 2A §18/§19)

Current motion is **appropriate and on-brief** — do not expand it.
- **Tighten reveal distance** 20px → 8–12px (matches `VISUAL_IDENTITY.md §15`; even quieter).
- **Gallery tile hover** — already patterned (cards/chips lift); apply to gallery tiles.
- **Optional scroll-progress indicator** — subtle, reinforces the "journey" metaphor (2A §16). Nice-to-have only.
- **Explicitly NOT recommended:** count-up stats, parallax, scroll-jacking, particle/background drift — these would "impress with technology" and violate the Creative Director's Critique.

---

## 8. 3D OPPORTUNITIES

**None.** 2A §19 forbids excessive 3D; there is no narrative need and no Three.js is loaded. Deliberately zero 3D. (Recorded so it isn't re-litigated.)

---

## 9. COMPONENT INVENTORY

| Component | File | State |
|---|---|---|
| Site header / sticky nav / hamburger | `components.css`, `navigation.js` | Complete, a11y-strong |
| Logo | `components.css` | Complete |
| Buttons (primary/secondary) + group | `components.css` | Complete |
| Stat card | `components.css` | Complete |
| Skill cluster + chips | `components.css` | Complete |
| Edu card | `components.css` | Complete |
| Cert card + thumb | `components.css` | Complete (img fallback) |
| PD card (dashed) | `components.css` | Complete |
| WeChat card + QR | `components.css` | Complete (img fallback) |
| Timeline + node + card | `sections.css` | Complete (no JS needed) |
| Research card | `components.css` | Complete |
| About grid / quote / pillar | `sections.css` | Complete |
| Video wrap / placeholder | `sections.css` | Placeholder only |
| Contact layout / link / image | `sections.css` | Complete (img fallback) |
| Image fallback | `components.css`, `utilities.js` | Complete |
| Badge / eyebrow / subsection-title | `typography.css` | Complete |
| **Gallery / lightbox** | *(missing)* | **Not built — stub only** |
| **Footer nav repeat** | *(missing)* | **Not built** |
| **Safeguarding statement** | *(missing)* | **Not built (mandatory)** |

---

## 10. FOLDER STRUCTURE REVIEW

```
mo-portfolio-v2/
├── index.html                  ✓ semantic, 6 acts
├── assets/
│   ├── css/  (9 files)         ✓ clean modular
│   ├── js/   (7 files)         ⚠ 3 stubs (§6)
│   ├── fonts/ (Fraunces/Manrope woff2) ✓ self-hosted
│   ├── images/ profile/✓  certificates/✗  classroom/✗  gallery/✗
│   │          leadership/✗  logos/✗  social/✗  timeline/✗  (most empty)
│   ├── documents/  cv/✗  certs/✗  degrees/✗  (drop targets, empty)
│   └── videos/  (empty; YouTube placeholder in HTML)
└── docs/  spec + this plan
```
**Issue:** Many `images/` subfolders are empty; HTML points at paths those folders don't populate (e.g. `certificates/pgce-cert.jpg`, `wechat-qr.jpg` at root). Reconcile paths in Stage 4/11 (see §11, §13-R3).

---

## 11. ASSET INVENTORY

**Present:** `profile.jpeg` (hero), `icon-192.svg`, fonts (3 woff2).
**Missing (user-supplied — graceful fallbacks live):**
- 4 certificate thumbnails (`certificates/*.jpg`)
- WeChat QR (`wechat-qr.jpg`)
- Contact portrait (`contact-portrait.jpg`)
- CV PDF (`documents/Mohammed_Shehzad_Khan_CV.pdf`) → currently 404
- **Classroom photos (0 of 8–20 target)** → §9 beat empty
- Teaching demo video ID (placeholder by design; note: YouTube is blocked in China — prefer self-hosted mp4 or accept China inaccessibility)

`ASSET_INVENTORY.md` lists dated `*.webp` targets that **do not match** the HTML `src` paths. **Decision needed (Stage 4):** adopt the inventory's `YYYY-Category-Desc.webp` convention and update HTML `src`s, or update the inventory to match the implementation. Recommended: adopt the convention (versionable, optimised) and rewire HTML.

---

## 12. MISSING CONTENT

1. Classroom Moments gallery (images + captions + lightbox) — **§9, highest brief impact**.
2. Safeguarding & ethics statement (Credentials) — **PRD §10 Mandatory**.
3. Research "how this changed my classroom" + publications slot — **CONTENT_BLUEPRINT Must/Nice**.
4. Languages list (Credentials) — **CONTENT_BLUEPRINT Must**.
5. Philosophy depth (6 topics, 450–700 words) — **CONTENT_BLUEPRINT Must**.
6. Leadership cards (2–4, LEADER tag) + principles (3–4) — **CONTENT_BLUEPRINT**.
7. "Currently Learning" labelling vs "Professional Development Roadmap".
8. Footer nav repeat + social links.
9. Verified measurable outcomes for Impact/Journey (only if genuinely evidenced — never invent).
10. Confirm: Harris University MA + 2009–2014 gap.

---

## 13. DESIGN INCONSISTENCIES (the critical fork)

**🔴 DARK vs LIGHT THEME DIVERGENCE.** `VISUAL_IDENTITY.md v1.1` specifies a **dark violet** system (`--bg:#0B0B0D`, `--accent:#7C5CFC`, grain, violet underglows, violet timeline nodes). The **live build is light navy** (`--bg:#F8FAFC`, `--accent:#1E3A5F`, neutral shadows, navy nodes) and contains **none** of the dark-spec treatments.

This is not a bug — it is a **spec-vs-build fork**. Resolution (recommendation, subject to your approval at Stage 3 exit):
- **Adopt the light/navy build as truth and revise `VISUAL_IDENTITY.md` to match.** Rationale: (a) 2A §12 explicitly describes "natural light, open spaces, a beautifully designed international school campus, premium materials" — a *light* mood; (b) the build is already shipped in light; (c) reverting to dark would contradict the Creative Constitution. The dark spec predates 2A.
- The alternative (revert build to dark violet) is rejected as it fights 2A.

**Other inconsistencies:**
- **Icons:** spec says Font Awesome (max 8); build uses emoji + inline SVG. Beneficial (no external dep, China-safe) but off-spec → formalise as "inline SVG / unicode, no icon font."
- **Typography:** spec said Google Fonts; build self-hosts. Beneficial deviation — keep.
- **Nav order:** `PRD §8` lists an order the build doesn't follow, but the build matches the newer `INFORMATION_ARCHITECTURE.md` six-act order — build is correct; `PRD §8` is stale.
- **Motion distance/duration:** build uses 20px / 0.6–0.9s; spec says 8–12px / 150–500ms. Tighten build toward spec (§7).
- **Timeline:** build is left-aligned navy (clean); spec said alternating violet. Build preferred; note in VI.
- **Spacing:** no spacing-scale tokens (magic numbers throughout). Extract `--space-*` tokens in Stage 4.

---

## 14. RECOMMENDED IMPROVEMENTS (consolidated)

1. **Reconcile `VISUAL_IDENTITY.md` → light/navy**; document icon strategy; add spacing tokens. (Stage 4)
2. **Implement Classroom Moments gallery** + lightbox (`gallery.js`), graceful fallbacks, safeguarding gate. (Stage 5/6)
3. **Add mandated content:** safeguarding statement, Research classroom-change + publications, languages, Philosophy depth, Leadership cards+principles, footer nav. (Stage 6)
4. **Fix CV 404** → graceful "available on request" until PDF supplied. (Stage 6)
5. **Remove dead stubs** (`theme.js`, `timeline.js`); let `gallery.js` do real work. (Stage 6)
6. **Replace emoji with inline SVG** for premium consistency. (Stage 6)
7. **Align asset paths** between HTML and `ASSET_INVENTORY.md`; verify supplied assets. (Stage 4/11)
8. **Tighten reveal** to 8–12px; optional scroll-progress indicator. (Stage 6/7)
9. **Run Lighthouse** when Chrome available; bundle CSS / inline critical if needed. (Stage 10)
10. **Confirm Harris University / 2009–2014** before deploy. (compliance)

---

## 15. SECTION-BY-SECTION IMPLEMENTATION ROADMAP

| Act | Section | Action | Gate |
|---|---|---|---|
| I | Hero | Keep. Replace emoji→SVG; wire CV fallback; verify portrait is genuine (not stock/AI, 2A §6). | Should |
| II | Story | Keep (~310w ok). | — |
| II | Journey | Add 1 *sourced* measurable achievement per major role (never invent). Verify "4 schools". | Should |
| III | Impact | Optionally add 2–3 Tier-1 evidence cards *if* real outcomes exist. Otherwise keep. | Should (content-gated) |
| III | Credentials | **Add languages list + safeguarding & ethics statement (Mandatory).** Rename PD→"Currently Learning". Wire cert thumbs. | **Must** |
| IV | Philosophy | Expand to 4–6 topic pillars (450–700w) with real examples. | Should |
| IV | Moments | **Build real gallery** (grid + filter + lightbox + captions + safeguarding gate). Fix nav label "Gallery". | **Must** (§9) |
| IV | Research | **Add "how this changed my classroom" + publications slot.** | **Must/Should** |
| V | Leadership | Add 2–4 LEADER cards + 3–4 principles (user-authored). | Should |
| VI | Contact | Verify contact-portrait + WeChat QR; add footer nav repeat + social. | Should |
| — | Design sys | Reconcile VI to light/navy; spacing tokens; icon strategy; asset paths. | **Must** |
| — | Tech debt | Remove stubs; CV fallback; reveal tuning. | Should |

---

## 16. RISK ASSESSMENT

| # | Risk | Prob. | Impact | Mitigation |
|---|---|---|---|---|
| R1 | User assets missing (certs/QR/CV/photos) | Certain | Med | Graceful fallbacks already live; clear drop-in paths; request once, non-blocking |
| R2 | Content accuracy (Harris Univ / 2009–14 gap) | Med | High (trust) | Confirm with user; never assert false; flag in UI if unconfirmed |
| R3 | Dark/light spec fork unresolved | High | Med (governance) | Align VI to light/navy per 2A (recommended); decide at approval |
| R4 | Safeguarding — identifiable students in photos | Med | High (legal/ethical) | Consent gate (PRD §10); prefer environments/wide shots; log in ASSETS.md |
| R5 | Over-animation temptation | Low | Med | 2A §18/§19 + critique lens; motion stays minimal |
| R6 | Scope creep / premature feature work | Low | Med | 1C §16 Stage Gate — plan-first, no code pre-approval |
| R7 | China audience — YouTube embed blocked | High (if used) | Med | Prefer self-hosted mp4 or accept China inaccessibility; no external CDNs |
| R8 | Lighthouse unrun (no Chrome) | High | Low | Note; run at Stage 10 when environment available |

---

## 17. ESTIMATED DEVELOPMENT PHASES (mapped to 1C §16 Stage Gate)

- **Phase A — Stages 1–3 (this document):** Backup ✓ · Audit ✓ · Plan (pending approval).
- **Phase B — Stage 4 Design System:** Reconcile `VISUAL_IDENTITY.md`→light/navy; spacing tokens; icon strategy; asset-path convention; dark-mode decision (drop).
- **Phase C — Stage 5 Component Library:** Formalise components; build gallery/lightbox; footer nav; safeguarding-statement block.
- **Phase D — Stage 6 Build:** Implement gallery, Philosophy/Leadership/Research/Credentials content, footer; wire assets; remove stubs; emoji→SVG; CV fallback.
- **Phase E — Stages 7–8 Test & Optimize:** Cross-browser (latest 2 of Chrome/Safari/Firefox/Edge + mobile); interaction/keyboard; image optimisation; CSS bundling; reveal tuning.
- **Phase F — Stages 9–10 A11y & Performance:** WCAG AA verification; Lighthouse (when Chrome available); perf budgets (LCP/INP/CLS).
- **Phase G — Stages 11–13 QA, Docs, Delivery:** Holistic pass against 2A §17 Recruiter Test + §18 Trust Equation; update `CHANGELOG.md`/`ASSET_INVENTORY.md`; deploy to GitLab Pages.

---

## 18. PRIORITY MATRIX

| Item | Priority | Recruiter impact | Stage |
|---|---|---|---|
| Reconcile VI → light/navy (governance truth) | **Must** | High | 4 |
| Classroom Moments gallery (§9 Authenticity) | **Must** | High | 5–6 |
| Safeguarding & ethics statement (PRD §10) | **Must** | High (compliance) | 6 |
| Research "changed my classroom" (blueprint Must) | **Must** | Med | 6 |
| CV download 404 → graceful | **Must** | High (action) | 6 |
| Languages list (blueprint Must) | **Must** | Med | 6 |
| Verify Harris Univ / 2009–14 gap | **Must** | High (trust) | pre-deploy |
| Cert / QR / contact-portrait assets | Should | Med (fallbacks OK) | 11 |
| Expand Philosophy (6 topics) | Should | Med | 6 |
| Expand Leadership (cards + principles) | Should | Med | 6 |
| Footer nav repeat + social | Should | Low–Med | 6 |
| Emoji → inline SVG | Should | Low (premium) | 6 |
| Spacing tokens | Should | Low (consistency) | 4 |
| Reveal 20px→8–12px | Should | Low | 6 |
| Scroll-progress indicator | Nice | Low | 7 |
| Lighthouse run + CSS bundle | Should | Med (perf) | 10 |
| Dark mode (theme.js) | Drop/Nice | — | — |

---

## 19. SELF-REVIEW CHECKLIST (against 1A/1B/1C/2A)

- [x] Single decisive narrative (six acts) preserved — 2A §10.
- [x] Motion outside Trust Equation, minimal, reduced-motion safe — 2A §18/§19.
- [x] No framework/build; vanilla; China-safe fonts — 1A/1B/1C.
- [x] Never-invent content rule flagged (Harris/2009–14) — 1A.
- [x] §9 Authenticity gap identified as top build item.
- [x] Stage Gate (1C §16) honoured: no code until approved.
- [x] Design-system fork surfaced with recommendation, not silently chosen.
- [ ] **Awaiting user approval of this plan before any Stage 4+ work.**
