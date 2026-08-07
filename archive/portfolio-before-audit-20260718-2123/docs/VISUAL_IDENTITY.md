# Visual Identity & Design Language Guide

**Version:** 2.0 (Reconciled to live build — 2026-07-17)
**Authority:** Design-system layer of Project Meridian. Subordinate to Document 1 (1A/1B/1C) and the Creative Constitution (2A). Where this guide and 2A conflict, 2A wins.

> **Reconciliation note.** v1.1 of this guide specified a *dark violet* system
> (`--bg:#0B0B0D`, `--accent:#7C5CFC`, grain, violet underglows). The implemented
> build is a *light navy editorial* system and uses none of those treatments. Document
> 2A §12 explicitly describes a light mood — "natural light, open spaces, a beautifully
> designed international school campus, premium materials" — so per the authority order
> (2A > older specs) this guide is reconciled to the **live light/navy build**. All
> v1.1 divergences are corrected inline below.

---

## 1. Governing Principles
1. **Design for longevity** — credible for 5+ years; timeless over trendy.
2. **Calm authority** — composed, precise, warm; nothing shouts.
3. **Evidence has visual priority** — strongest emphasis reserved for evidence, not decoration.
4. **One accent (navy), used with discipline** — navy means "this matters or is interactive."
5. **Pillars shape emphasis** — every section visually reinforces at least one pillar.

---

## 2. Mood
Light, editorial, not promotional. A beautifully typeset journal profile of an educator.
Soft near-white backdrop, generous space, natural light. Feeling: serious, accomplished,
human. **Backgrounds must never compete with content** — if noticeable while reading, too strong.

---

## 3. Color Tokens (live values, 2A-aligned)

| Token | Value | Role |
|---|---|---|
| `--bg` | `#F8FAFC` | Page background (near-white) |
| `--text` | `#111827` | Headings, primary (~16:1 on bg) |
| `--text-secondary` | `#374151` | Body (~10:1 on bg) |
| `--text-muted` | `#4B5563` | Captions, metadata (~7:1 on bg) |
| `--accent` | `#1E3A5F` | Buttons, borders, markers, links (navy) |
| `--accent-soft` | `rgba(30,58,95,.08)` | Tints, washes, tags |
| `--border` | `#E5E7EB` | Hairlines |
| `--border-strong` | `#64748B` | Emphasized dividers (≥3:1 on white) |

No `--bg-elevated` / `--surface` tokens — this is a **flat light theme**; cards are white
sitting on the near-white background, separated by 1px borders + subtle neutral shadows.
No grain, no violet radial washes (both removed vs v1.1).

**Shadows (neutral, not violet):**
`--shadow-card: 0 4px 12px rgba(0,0,0,.03)` · `--shadow-card-hover: 0 12px 24px rgba(0,0,0,.06)` · `--shadow-subtle: 0 4px 6px -1px rgba(0,0,0,.05)`.

---

## 4. Typography (Fraunces + Manrope, self-hosted)
- **Headings:** Fraunces (serif, warm, academic, timeless).
- **Body:** Manrope (readable, distinctive).
- **Self-hosted woff2** with `font-display: swap` — replaces Google Fonts (blocked in
  mainland China, was render-blocking). No external font requests.
- Max 4 weights (400/500/600/700). Never Inter, Roboto, or Arial.
- Display `clamp(3rem,6vw,4.8rem)` serif · H2 `clamp(2.3rem,4vw,3.2rem)` serif · H3 `1.5rem` ·
  Body `1rem–1.2rem`, line-height `1.65`, max `62ch` · Labels `.875rem` uppercase letter-spaced accent.
- Italics for quotations only; uppercase label style = section eyebrows.

---

## 5. Spacing (tokenised, 8px base)
```
--space-1: 0.5rem;   /* 8px  */
--space-2: 1rem;     /* 16px */
--space-3: 1.5rem;   /* 24px */
--space-4: 2rem;     /* 32px */
--space-5: 3rem;     /* 48px */
--space-6: 4rem;     /* 64px */
--space-7: 6rem;     /* 96px */
--space-8: 8rem;     /* 128px */
--section-py:       112px;   /* desktop section padding */
--section-py-mobile: 80px;   /* ≤900px section padding */
```
Whitespace is the primary hierarchy tool. Generous vertical rhythm between sections.

---

## 6. Grid & Width Rhythm
Max `1120px` (`--container`), side padding `24px`. Breakpoints `480 / 900`.
Hero `55fr / 45fr` split → reading sections single/two-column → evidence/gallery `1120` →
contact two-column. Asymmetric editorial splits permitted.

---

## 7. Radii
Buttons/tags `8px` (`--radius-sm`) · cards/images `8px` · large panels/hero `16px` (`--radius-lg`).
No circular images except the optional small footer avatar.

---

## 8. Elevation
Depth via **subtle neutral shadows + 1px borders**, not coloured glows.
Flat (`--bg`) → Card (white + `--border`) → Hover (`--shadow-card-hover` + `--accent-soft` border).
No violet underglow (removed vs v1.1).

---

## 9. Borders
1px hairlines, neutral. Navy accent borders reserved for: focus ring, active timeline node, primary CTA hover.

---

## 10. Card Hierarchy
- **Tier 1 Evidence** (Impact / Leadership): tag, headline, detail, source line.
- **Tier 2 Timeline**: accent spine, navy nodes, otherwise quiet.
- **Tier 3 Lists** (Credentials): compact, metadata-styled.
Tier 1 must be distinguishable from Tier 3 at a squint.

---

## 11. Buttons
- **Primary** (Download CV): `--accent` fill, white `600`, hover lift `-2px` + shadow.
- **Secondary**: transparent, `--border-strong`, hover `--accent-soft` wash.
- **Rule:** only one visually dominant action per viewport.

---

## 12. Iconography
**Inline SVG** (20–24px, `currentColor`) or unicode glyphs. **No icon font** (Font Awesome
dropped — avoids an external dependency, China-safe, smaller payload). Max ~6 distinct icons
site-wide. Icons support labels, never replace them; `aria-hidden` when decorative.
> Note: the current build uses 2–3 emoji (↓ ✔ 📍) in the hero/contact. These are to be
> replaced with inline SVG in Stage 6 for a more premium, consistent treatment.

---

## 13. Photography
Authentic, warm natural colour, no filters/duotone/violet tinting. 8–16px radius, subtle
border frame. Caption + alt text on every image. **Portraits show approachability and
confidence rather than authority — warmth over executive polish.** Safeguarding rules apply.

---

## 14. Graphics
No decorative illustration. Functional only: clean typographic stats, simple country treatment.

---

## 15. Motion (outside the Trust Equation — 2A §18/§19)
Durations `300ms` UI · `650ms` reveals. Entrances: ease-out, **fade + ~20px rise**
(target: tighten to 8–12px in Stage 6/7), `100–400ms` stagger, fire once at ~15% intersection.
`prefers-reduced-motion`: everything instant and fully visible. JS failure: content visible by
default. **No loops, no background drift, no scroll-jacking, no parallax.** Animation supports
trust; it does not create it. The build uses only CSS reveals + a restrained hero entrance —
no GSAP, no Three.js.

---

## 16. Pillar Expression
Pillars are expressed via section eyebrows + the navy accent (no per-pillar colours). An
optional uppercase navy-soft pill may mark pillar tags on Tier 1 cards.

---

## 17. Longevity Guardrails (avoided)
Bento overuse, neon meshes, glass beyond the nav, cursor effects, scroll-jacking, marquee,
AI-art imagery, rainbow pillar coding, cleverness-for-its-own-sake, **excessive 3D** (2A §19 —
deliberately zero Three.js).

---

## 18. Content Voice & Tone
Reflective, precise, evidence-based, human, concise. First person, active voice, claims
followed by evidence. Avoid: corporate jargon, inspirational clichés, AI-sounding prose,
unsupported adjectives ("passionate", "dynamic", "results-driven"). Mixed short/medium
sentences, paragraphs 2–4 sentences, headings clear over clever.

---

## 19. Component Behavior
- **Nav:** sticky `72px`; blur + hairline; scroll-spy accent (`aria-current="page"`);
  focus-trapped drawer (Esc, outside-click, focus return); smooth anchors with header offset
  (`scroll-margin-top: 72px`).
- **Timeline:** vertical spine, navy nodes, **left-aligned** (intentional — cleaner than
  alternating); reveal once; **no JS required** (timeline.js stub removed).
- **Gallery:** filter pills, lazy grid, minimal lightbox (Esc, arrows, focus return); no
  autoplay/carousel. *(To be built — Stage 5/6.)*
- **Accordion:** native `details/summary` if needed.
- **Section transitions:** spacing + background only, no dividers.
