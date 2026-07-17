# Content Map — Mohammed Shehzad Khan Portfolio

**Purpose:** Internal reference. Maps every section of `index.html` to its source assets.
Use this when updating the site. It prevents hunting through folders six months later.

**Not public.** Not deployed.

---

## Hero

**What recruiter sees:** Name, title, location, availability, profile photo, two CTAs.

| Slot | Asset | Path | Status |
|---|---|---|---|
| Profile photo | `2026-Profile-Headshot.webp` | `assets/images/profile/` | ⬜ Needed |
| CV download | `2026-CV-Mohammed-Shehzad-Khan.pdf` | `assets/downloads/` | ⬜ Needed |
| Availability line | Text in HTML | `index.html` (hero section) | ✅ Written |
| Location | Text in HTML | `index.html` (hero section) | ✅ Written |

**HTML element:** `<section id="hero">`

---

## About / Teaching Philosophy

**What recruiter sees:** A mission statement, three teaching pillars, evidence of reflection.

| Slot | Asset | Path | Status |
|---|---|---|---|
| Teaching Philosophy (PDF) | `2026-Teaching-Philosophy.pdf` | `assets/downloads/` | ⬜ Needed |
| Mission statement | Text in HTML | `index.html` (about section) | ✅ Written |
| Teaching pillars | Text in HTML | `index.html` (about section) | ✅ Written |

**HTML element:** `<section id="about">`

---

## Teaching Impact (Stats)

**What recruiter sees:** Four headline statistics proving scale and reach.

| Slot | Content | Status |
|---|---|---|
| Years of experience | "10+ Years" | ✅ Written |
| Students taught | "1,000+ Students" | ✅ Written |
| Countries | "2 Countries" | ✅ Written |
| Schools | "5+ Schools" | ✅ Written |

**HTML element:** `<section id="impact">`

**Note:** Update numbers when a new role begins.

---

## Journey (Employment Timeline)

**What recruiter sees:** Chronological career history with institutions, dates, responsibilities.

| Slot | Asset | Path | Status |
|---|---|---|---|
| Timeline content | Text in HTML | `index.html` (journey section) | ✅ Written |
| Timeline photo (optional) | `YYYY-Timeline-[Role].webp` | `assets/images/timeline/` | ⬜ Optional |

**HTML element:** `<section id="journey">`

---

## Research / Practitioner Inquiry

**What recruiter sees:** PGCE research paper summary — evidence of reflective practice.

| Slot | Asset | Path | Status |
|---|---|---|---|
| Research summary | Text in HTML | `index.html` (research section) | ✅ Written |
| Paper PDF | `2026-Research-Questioning-Strategies-PGCE.pdf` | `assets/documents/publications/` | ⬜ Needed |
| Paper PDF (download) | Same PDF | `assets/downloads/` | ⬜ Optional |

**HTML element:** `<section id="research">`

---

## Classroom Moments (Gallery)

**What recruiter sees:** Photos of teaching in action. Currently a stub.

| Slot | Asset | Path | Status |
|---|---|---|---|
| Photo 1 | `2025-Classroom-EAL-Lesson.webp` | `assets/images/classroom/` | ⬜ Needed |
| Photo 2 | `2025-Classroom-STEM-Activity.webp` | `assets/images/classroom/` | ⬜ Needed |
| Photo 3 | `2023-Classroom-Guided-Reading.webp` | `assets/images/classroom/` | ⬜ Needed |

**HTML element:** `<section id="gallery">` *(section not yet implemented — Release 1.1)*

> ⚠️ Safeguarding: No identifiable students without documented parental consent.

---

## Qualifications / Credentials

**What recruiter sees:** Degree cards, certificate thumbnails, professional development roadmap.

| Slot | Asset | Path | Status |
|---|---|---|---|
| PGCE thumbnail | `2026-Certificate-PGCE-University-of-Cumbria.webp` | `assets/images/certificates/` | ⬜ Needed |
| TESOL thumbnail | `2026-Certificate-TESOL-Global-College.webp` | `assets/images/certificates/` | ⬜ Needed |
| TEFL thumbnail | `2026-Certificate-TEFL-Teacher-Record.webp` | `assets/images/certificates/` | ⬜ Needed |
| British Council thumbnail | `2026-Certificate-British-Council-PD.webp` | `assets/images/certificates/` | ⬜ Needed |
| Credentials text | Text in HTML | `index.html` (credentials section) | ✅ Written |

**HTML element:** `<section id="credentials">`

---

## Contact

**What recruiter sees:** Email, phone, LinkedIn, WeChat QR code, portrait photo.

| Slot | Asset | Path | Status |
|---|---|---|---|
| Contact portrait | `2026-Profile-Headshot.webp` | `assets/images/profile/` | ⬜ Same as hero photo |
| WeChat QR code | `wechat-qr.jpg` | `assets/images/` | ⬜ Check exists |
| Email | `mdshezkhn@hotmail.com` | `index.html` | ✅ Written |
| Phone | `+86-131 3771 9002` | `index.html` | ✅ Written |
| LinkedIn | `linkedin.com/in/mdshezkhn` | `index.html` | ✅ Written |

**HTML element:** `<section id="contact">`

---

## Navigation / Header

| Slot | Content | Status |
|---|---|---|
| Logo text | "Mohammed Shehzad Khan" | ✅ |
| Nav links | Hero, About, Journey, Research, Credentials, Contact | ✅ |
| CTA button | Links to `#contact` | ✅ |

---

## How to Update a Section

1. Open `index.html` and find the relevant `<section id="...">`.
2. Update the HTML content directly — no build step required.
3. If adding a new asset (photo, PDF), add it to the correct `assets/` subfolder using the `YYYY-Category-Description.ext` naming convention.
4. Update `ASSET_INVENTORY.md` — mark the "Added to Website?" column.
5. Save, reload Live Server, verify visually.
6. `git add -A && git commit -m "content: update [section name]"`.
7. Push to deploy.
