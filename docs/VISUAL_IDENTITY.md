# Visual Identity & Design Language Guide

**Version:** 1.1 (Approved)

## 1. Governing Principles
1. **Design for longevity** – credible for 5+ years; timeless over trendy; any "current-year trend" pattern rejected by default
2. **Calm authority** – composed, precise, warm; nothing shouts
3. **Evidence has visual priority** – strongest emphasis reserved for evidence, not decoration
4. **One accent, used with discipline** – violet means "this matters or is interactive"
5. **Pillars shape emphasis** – every section visually reinforces at least one pillar

## 2. Mood
Editorial, not promotional. A beautifully typeset journal profile of an educator. Dark quiet backdrop, generous space. Feeling: serious, accomplished, human. **Backgrounds must never compete with content** – if noticeable while reading, too strong.

## 3. Color Tokens
| Token | Value | Role |
|---|---|---|
| --bg | #0B0B0D | Page background |
| --bg-elevated | #121216 | Section alternation |
| --surface | #17171C | Cards |
| --surface-raised | #1E1E24 | Hover, nested cards |
| --text | #F5F5F7 | Headings, primary (~17:1) |
| --text-secondary | #B9B9C3 | Body (~10:1) |
| --text-muted | #8A8A96 | Captions, metadata (~5:1) |
| --accent | #7C5CFC | Buttons, borders, markers, glows (non-text UI) |
| --accent-text | #A78BFA | Link text, highlights (~7:1) |
| --accent-soft | rgba(124,92,252,0.12) | Tints, washes, tags |
| --border | rgba(255,255,255,0.08) | Hairlines |
| --border-strong | rgba(255,255,255,0.14) | Emphasized dividers |

Contrast re-verified in Sprint 1; hexes nudged if any pair falls below AA. Grain <=3% opacity on --bg only. Gradients: violet radial washes <=10% opacity, max one per viewport height.

## 4. Typography (official: Fraunces + Manrope)
- **Headings:** Fraunces (serif, warm, academic, timeless)
- **Body:** Manrope (readable, distinctive, not tech-startup default)
- Never use Inter, Roboto, or Arial. Max 4 weights total, Google Fonts for v1.
- Display 44–76px serif 600 · H2 32–48px serif · H3 20–24px sans 600 · Body 17–18px, line-height 1.7, max 68ch · Labels 13–14px uppercase letter-spaced muted
- No weights below 400 for body; italics for quotations only; uppercase label style = pillar tags and section eyebrows

## 5. Spacing
8px base: 4/8/12/16/24/32/48/64/96/128/160. Sections 128px desktop / 80px mobile. Heading-to-content 48px. Card padding 32px. Whitespace is the primary hierarchy tool.

## 6. Grid & Width Rhythm
12-column, 24px gutters, max 1120px, side padding 24/48px. Breakpoints 480/768/1024/1280. **Rhythm:** Hero 1120 → reading sections 720 → evidence/gallery 1120 → contact 720. Asymmetric editorial splits permitted.

## 7. Radii
Buttons/tags 8px · cards/images 12px · large panels 16px · pills only for pillar tags · no circular images except optional small footer avatar.

## 8. Elevation
Depth via surface lightness, not drop shadows. Flat (--bg) → Card (--surface + --border) → Raised (--surface-raised + --border-strong + single soft violet underglow 0 8px 32px rgba(124,92,252,0.10)). Glass only on sticky nav.

## 9. Borders
1px hairlines. Violet borders reserved for: focus, active timeline node, primary CTA.

## 10. Card Hierarchy
- **Tier 1 Evidence** (Impact/Leadership): pillar tag, headline, detail, on-card source line; only tier with accent-tinted icons
- **Tier 2 Timeline**: accent spine, violet nodes, otherwise quiet
- **Tier 3 Lists** (Credentials): compact, metadata-styled
Tier 1 must be distinguishable from Tier 3 at a squint.

## 11. Buttons
- **Primary** (Download CV): --accent fill, white 600/>=16px text, hover lighten 8% + lift 2px, 2px offset focus ring
- **Secondary**: transparent, --border-strong, hover --accent-soft wash
- **Tertiary**: --accent-text link, underline on hover
**Rule: only one visually dominant action per viewport.**

## 12. Iconography
Font Awesome, one style (regular/light), **max 8 distinct icons site-wide**, 20–24px, --text-muted default, accent only in Tier 1 cards. Icons support labels, never replace them. Decorative icons aria-hidden.

## 13. Photography
Authentic, warm natural color, no filters/duotone/violet tinting. 12px radius, subtle border frame. Caption + alt text on every image. **Portraits show approachability and confidence rather than authority – warmth over executive polish.** Safeguarding rules apply without exception.

## 14. Graphics
No decorative illustration. Functional only: simple country treatment for Global Professional, clean typographic stats.

## 15. Motion
Durations 150/300/500ms. Entrances: confident ease-out cubic-bezier(0.16,1,0.3,1); fade + **8–12px rise** (12 large panels, 8 small), 60ms stagger, fire once at ~20% intersection. prefers-reduced-motion: everything instant and fully visible. JS failure: content visible by default. No loops except <=3% background drift.

## 16. Pillar Expression
One consistent uppercase violet-soft pill for all five pillars (no per-pillar colors). Appears on Tier 1 cards, timeline milestones, section eyebrows.

## 17. Longevity Guardrails (avoided)
Indiscriminate bento layouts (bento only where it improves hierarchy: Impact, Skills), neon meshes, glass beyond nav, cursor effects, scroll-jacking, marquee, AI-art imagery, rainbow pillar coding, cleverness-for-its-own-sake.

## 18. Content Voice & Tone
Reflective, precise, evidence-based, human, concise. First person, active voice, claims followed by evidence. Avoid: corporate jargon, inspirational cliches, AI-sounding prose, unsupported adjectives ("passionate", "dynamic", "results-driven"). Mixed short/medium sentences, paragraphs 2–4 sentences, headings clear over clever.

## 19. Component Behavior
- **Nav:** sticky 72/64px; transparent over hero, blur + hairline after 40px scroll; scroll-spy accent underline; smooth anchors with header offset
- **Timeline:** vertical spine, nodes fill violet on viewport entry, alternating desktop / left mobile, reveal once
- **Gallery:** filter pills, lazy grid, minimal lightbox (Esc, arrows, focus return); no autoplay/carousel
- **Accordion:** native details/summary, chevron 300ms
- **Tooltips:** none in v1
- **Section transitions:** no dividers; --bg/--bg-elevated alternation + spacing
