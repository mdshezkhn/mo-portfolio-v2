# Information Architecture & Wireframe Specification

**Version:** 1.1 (Approved) · Single page, anchor navigation

## 1. Recruiter Journey Mapping
| Time | Question | Section(s) | Outcome |
|---|---|---|---|
| 0–5s | Who is this? | Hero | Name, role, setting understood without scrolling |
| 5–15s | What's his value? | Hero value line + Impact Highlights | One differentiator absorbed |
| 15–30s | Where's the evidence? | Teaching Impact | One concrete sourced example seen |
| 30–45s | How does he think/grow? | Philosophy, Leadership, Journey | Depth confirmed |
| 45–60s | How do I act? | Persistent nav CTA + Contact | CV downloaded or contact made |

## 2. Page Order (approved)
1. **Hero** (1120) – all pillars
2. **Impact Highlights** (1120) – ships hidden unless >=3 verified stats
3. **My Story** (720)
4. **Teaching Impact** (1120)
5. **Teaching Philosophy** (720)
6. **Leadership & Teacher Development** (1120)
7. **Professional Journey** (1120)
8. **Research & Innovation** (720)
9. **Classroom Moments** (1120)
10. **Credentials** (1120)
11. **Contact** (720)
Footer.

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
