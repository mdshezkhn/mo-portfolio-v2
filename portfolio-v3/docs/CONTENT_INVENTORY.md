# Content Inventory — Mohammed Shehzad Khan Portfolio

**Purpose:** Tracks the completeness of each website section toward a publishable state.
Update the % and status after each work session.

**Not public.** Not deployed.

---

## How to read this

| Status | Meaning |
|---|---|
| ✅ Done | Section is complete and recruiter-ready |
| 🟡 In Progress | Partially written or needs asset |
| ⬜ Not Started | Section exists in HTML but is a placeholder |
| 🔒 Gated | Blocked on a specific missing asset |

---

## Section Status

| Section | Completeness | Status | Blocking Asset | Target Release |
|---|---|---|---|---|
| **Hero** | 85% | 🔒 Gated | CV PDF | 1.0 |
| **About / Philosophy** | 60% | 🟡 In Progress | Teaching Philosophy PDF | 1.0 |
| **Teaching Impact** | 90% | 🟡 In Progress | Verify stat accuracy | 1.0 |
| **Journey / Timeline** | 80% | 🟡 In Progress | Optional: timeline photos | 1.0 |
| **Research** | 70% | 🟡 In Progress | Research paper PDF | 1.1 |
| **Gallery** | 0% | ⬜ Not Started | Classroom photos (safeguarding check) | 1.1 |
| **Qualifications** | 50% | 🔒 Gated | Certificate thumbnail images | 1.0 |
| **Contact** | 90% | 🟡 In Progress | WeChat QR confirm, contact portrait | 1.0 |
| **Footer** | 100% | ✅ Done | — | 0.9 |
| **Navigation** | 100% | ✅ Done | — | 0.9 |
| **Mobile Responsive** | 100% | ✅ Done | — | 0.9 |
| **SEO / Meta** | 95% | 🟡 In Progress | Update canonical URL after deploy | 1.0 |

---

## Release 1.0 Checklist (Recruiter Ready)

The following must be complete before the site goes live at a public URL.

### Assets
- [x] Professional headshot compressed and added (`assets/images/profile/2026-Profile-Headshot.webp`)
- [ ] CV finalised and added (`assets/downloads/2026-CV-Mohammed-Shehzad-Khan.pdf`)
- [ ] Teaching Philosophy PDF added (`assets/downloads/2026-Teaching-Philosophy.pdf`)
- [ ] Certificate thumbnails created and added (4 images, `assets/images/certificates/`)
- [ ] WeChat QR code confirmed in correct path (`assets/images/wechat-qr.jpg`)

### HTML
- [x] Hero photo `src` updated to new headshot path
- [ ] Hero "Download CV" button `href` updated to `assets/downloads/2026-CV-Mohammed-Shehzad-Khan.pdf`
- [ ] Certificate `src` attributes updated to new thumbnail filenames
- [ ] Canonical URL updated in `<head>` to actual GitHub Pages URL
- [ ] `og:image` URL updated to actual deployed URL

### Deployment
- [ ] GitHub repository created
- [ ] `git push -u origin main` completed
- [ ] GitHub Pages enabled (Settings → Pages → GitHub Actions)
- [ ] Verified live at `https://[username].github.io/mo-portfolio/`
- [ ] All images load (no broken image icons)
- [ ] All links work (CV download, LinkedIn, email, phone)
- [ ] Mobile layout verified on a real phone
- [ ] Console has no JavaScript errors

---

## Release 1.1 Checklist (Evidence)

- [ ] Classroom gallery section implemented
- [ ] Gallery photos added (safeguarding checked for each)
- [ ] Demo lesson video linked (YouTube unlisted or `assets/videos/`)
- [ ] Research paper linked
- [ ] Certificate download links added
- [ ] Awards section (if applicable)
- [ ] GitLab Pages verified
- [ ] Gitee Pages verified (China access)

---

## Content Quality Standards

Every section must meet these before Release 1.0:

| Standard | Pass Criteria |
|---|---|
| **Accuracy** | All dates, institutions, stats are verifiable |
| **Tone** | Professional, reflective, not promotional |
| **Evidence** | Every claim supported by a document or data point |
| **Safeguarding** | No identifiable students without documented consent |
| **Accessibility** | All images have descriptive `alt` text |
| **Performance** | No image over 300KB in `assets/images/` (except profile: max 200KB) |

---

*Last updated: 2026-07-17*
