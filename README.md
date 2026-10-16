# Mohammed Shehzad Khan — Talking-Video Portfolio

A quiet, premium, single-page portfolio: white, black and grays only, one
talking intro video, and every word traceable to the résumé.

**Live:** `https://mdshezkhn.github.io/mo-portfolio-v2/`

---

## Run it

```bash
npm install
npm run dev        # http://localhost:3000/mo-portfolio-v2
npm run build      # static export → out/
npm run preview    # serve the export locally
```

## Sections

| # | Section | Component | Signature interaction |
|---|---------|-----------|----------------------|
| 00 | Hero | `hero/Hero.tsx` | Talking video, seamless loop, multiply blend, ▶/❚❚ sound toggle |
| 01 | About | `sections/About.tsx` | Hanging lanyard ID card — pendulum swing, flip |
| 02 | Skills | `sections/Skills.tsx` | Periodic table of the practice + sticky inspector |
| 03 | Work | `sections/Work.tsx` | Expanding accordion gallery + illustrative mini-UIs |
| 04 | Certifications | `sections/Certifications.tsx` | Ink-flood index |
| 05 | Experience | `sections/Experience.tsx` | Timeline that draws as you scroll |
| 06 | Achievements | `sections/Achievements.tsx` | Pinned horizontal gallery, count-up numbers |
| 07 | Contact | `sections/Contact.tsx` | Letter-hop heading, copy-email chip, spinning badge |

All content lives in **`src/lib/data.ts`** — components only read from it.
The résumé (`public/resume/Mohammed_Shehzad_Khan_CV.pdf`) is the single
source of truth; nothing on the page exists outside it. Per the repo's
publication policy, only verifiable counts appear in Achievements.

## Rebuilding the hero video

1. Generate your intro clip (Google Flow or similar): standing centred,
   plain white background, 8–15 s, landscape.
2. Then:

```bash
# auto-detects the person, whitens the backdrop, cross-fades the loop
python scripts/build-hero-assets.py path/to/intro.mp4

# manual crop instead of auto-detection
python scripts/build-hero-assets.py intro.mp4 --crop 800:1000:560:80

# before the real video exists: silent breathing-zoom placeholder
python scripts/build-hero-assets.py --placeholder portfolio-src/profile.jpeg
```

Outputs `public/hero/hero.webm` + `hero.mp4` (webm is listed first),
plus `public/portrait-bust.webp` when `--portrait` is given.
Requires `ffmpeg` on PATH; audio cross-fade needs `numpy`.

## Fonts

Self-hosted in `src/fonts` via `next/font/local` (no runtime CDN):

- **Inter Tight** (variable) — display + body
- **Instrument Serif** (400 + italic) — one accent word per heading
- **JetBrains Mono** (variable) — labels, indices, numbers

Sources: `@fontsource/*` packages (SIL OFL 1.1).

## Brand logos & licences

`public/logos/` holds official brand SVGs (Google, Microsoft, Moodle,
Canvas, Zoom, OBS) extracted from **simple-icons** (CC0) by
`node scripts/make-logos.mjs`. Brand artwork remains the trademark of
its owner and appears only to identify the technology. Concept-skill
line icons are original to this repo (MIT, see `LICENSE`).

## Tech

Next.js 15 (App Router, static export) · React 19 · TypeScript ·
Tailwind CSS 4 · Lenis (only animation dependency) · CSS animations,
IntersectionObserver and small rAF loops — no three.js, no GSAP.

## Previous version

The original static HTML/CSS/JS portfolio is preserved under `legacy/`
(and in git history). The deployed workflow now builds this Next.js app
and uploads `out/`.
