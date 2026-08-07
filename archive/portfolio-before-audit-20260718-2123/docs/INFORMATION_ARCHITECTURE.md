# Information Architecture & Wireframe Specification

**Version:** 1.2 (Approved) · Single page, anchor navigation · Cinematic six-act narrative (Doc 1C §15)

## 0. Cinematic Narrative Framework (Six Acts)

The portfolio is a single-page cinematic narrative, not a collection of unrelated
sections. Every section is grouped under one of six acts so the recruiter moves
impression → journey → evidence → classroom → future → invitation without
backtracking (Doc 1C §15, PRD §5). The section order below is the approved act order.

1. **Act I – The First Impression** (Hero & identity) → `Hero`
2. **Act II – The Journey** (Story & experience) → `Story`, `Journey`
3. **Act III – The Evidence** (Achievements & impact) → `Impact`, `Credentials`
4. **Act IV – The Classroom** (Teaching philosophy, gallery, research) → `Philosophy`, `Moments`, `Research`
5. **Act V – The Future** (Vision, leadership, innovation) → `Leadership`
6. **Act VI – The Invitation** (Contact & call to action) → `Contact`

## 1. Recruiter Journey Mapping
| Time | Question | Section(s) | Outcome |
|---|---|---|---|
| 0–5s | Who is this? | Hero | Name, role, setting understood without scrolling |
| 5–15s | What's his value? | Hero value line + Impact Highlights | One differentiator absorbed |
| 15–30s | Where's the evidence? | Teaching Impact | One concrete sourced example seen |
| 30–45s | How does he think/grow? | Philosophy, Leadership, Journey | Depth confirmed |
| 45–60s | How do I act? | Persistent nav CTA + Contact | CV downloaded or contact made |

## 2. Page Order (approved — six-act arc)

Grouped by act (§0); section widths preserved from v1.1.

**Act I – The First Impression**
1. **Hero** (1120) – all pillars

**Act II – The Journey**
2. **Story** (720) – About Me
3. **Journey** (1120) – Professional Journey timeline

**Act III – The Evidence**
4. **Impact** (1120) – Skills & Proficiencies
5. **Credentials** (1120) – Education & Certifications

**Act IV – The Classroom**
6. **Philosophy** (720) – Teaching philosophy
7. **Moments** (1120) – Classroom Moments / gallery
8. **Research** (720) – PGCE practitioner research

**Act V – The Future**
9. **Leadership** (1120) – Leadership & Direction

**Act VI – The Invitation**
10. **Contact** (720) – Contact & CTA
Footer.

> Note: "Impact Highlights" and a standalone "Teaching Impact" section from the
> v1.1 blueprint were consolidated into the live `Impact` (Skills & Proficiencies)
> section. If distinct evidence cards are later authored, reintroduce them inside
> Act III. Testimonials remain hidden until real content exists.

## 3. Section Specifications
**Hero** (<=100vh, min 640px): eyebrow (INTERNATIONAL EDUCATOR · [LOCATION]) · name (serif display) · value proposition (<=14 words) · **location + availability line** · Download CV (primary) + Get in touch (secondary) · portrait (5-col, 12px radius) · one static-capable violet wash · subtle scroll cue. Desktop 7/5 split; mobile stacked, full-width CTAs.

**Impact Highlights:** 3–4 verified stats, serif display number + uppercase label + one-line source context. **Every stat answers Scale, Reach, Improvement, or Leadership. No vanity metrics.** Mobile 2x2.

**My Story:** 2–3 paragraphs (<=250 words), magazine-profile tone, values row (3, text only), optional candid photo.

**Teaching Impact:** eyebrow + H2 + framing paragraph, then 4–6 Tier 1 evidence cards, 2-col desktop / 1-col mobile. Card: pillar tag, headline, 2–3 sentence detail, source line.

**Teaching Philosophy:** lead statement in large serif + six topics (differentiation, student-centred learning, assessment, inclusion, growth mindset, evidence-informed teaching). **450–600 words, hard cap 700.** Accordions only if topics exceed ~80 words.

**Leadership:** Tier 1 cards (2–4, LEADER tag) + **Leadership Principles** block (3–4 short user-authored principles).

**Professional Journey:** vertical timeline, newest first, alternating desktop / left mobile. **Major roles expanded (2–3 responsibilities + 1 achievement), minor roles condensed (title + one line).**

**Research:** <=300 words: PGCE focus, inquiry approach, and required closing: **"How this research changed my classroom."** Future publications link slot.

**Classroom Moments:** filter pills → responsive grid (3/2/1–2 cols), captions on all images, lightbox. Safeguarding gate on every asset.

**Credentials:** two-column Tier 3 lists (education + certifications | languages + skills) + **Currently Learning** block + safeguarding & ethics note.

**Contact:** centered closing serif line, obfuscated email, **"Connect on LinkedIn"** labeled link, Download CV (dominant action of this viewport). Footer: name, copyright, quiet nav repeat.

## 4. Responsive
<=768px: single column, drawer nav, 80px padding, stats 2x2, timeline left. 768–1024: 2-col cards, hero may stack. >=1024: full layouts. Touch targets >=44px; no hover-dependent information.

## 5. Scroll & State
Scroll-spy nav underline · descriptive slugs (#teaching-impact) · hash updates for shareable deep links · reveals fire once per session · fully readable with JS disabled.
