# documents/

Internal reference documents. **These are NOT served publicly.**

Use `assets/downloads/` for publicly downloadable files.

## Subfolders

| Folder | Contents |
|---|---|
| `cv/` | **CV source files** — `cv.html` (clean, print-optimised A4 CV) and generated PDF. Updated via the workflow below. |
| `degrees/` | Degree certificates and transcripts |
| `pgce/` | PGCE certificate and coursework |
| `tesol/` | TESOL certification and supporting docs |
| `tefl/` | TEFL certification and supporting docs |
| `certificates/` | All other professional certificates |
| `references/` | Reference letters and contacts |
| `awards/` | Award certificates and recognition |
| `lesson-plans/` | Sample lesson plans for portfolio use |
| `publications/` | Research papers and academic writing |
| `transcripts/` | Academic transcripts |
| `employment/` | Employment contracts and letters |

## CV Source → PDF Workflow (Phase 1.1)

1. **Edit `assets/documents/cv/cv.html`** — the clean, self-contained, print-optimised A4 CV with inline CSS, `@media print`, and page-break control. All content is text-selectable.
2. **Regenerate the PDF** via headless Chromium:
   ```bash
   npx playwright install
   npx playwright codegen --help
   # Or use puppeteer/chromium: await page.goto('cv.html'); await page.pdf({ path: 'cv.pdf', format: 'A4', printBackground: true })
   ```
3. **Validate**:
   - `pdftotext cv.pdf -` must extract full text (907+ words)
   - `qpdf --check cv.pdf` should pass (if qpdf is installed)
   - Open in two non-Chromium PDF viewers to confirm readability
4. **Replace the old PDF** `assets/documents/Mohammed_Shehzad_Khan_CV.pdf` with the new one, committing the new file under the same path.

If headless Chromium is unavailable, use an online HTML‑to‑PDF service (e.g., pdfcrowd, htmlpdf) and verify the text extraction requirement above.

---

### Current CV content (as of 2026‑09‑13)

- **Legal name**: `Khan Mohammed Shehzad Anwar` (updated from previous `Mohammed Shehzad Anwar Khan`)
- **Emails**: `mdshezkhn@hotmail.com` and `mdshezkhn@gmail.com`
- **PGCE**: Listed as **Non‑QTS**; includes the QTS‑pathway note: *"I hold a Postgraduate Certificate in Education (PGCE, non-QTS) from the University of Cumbria and a B.Ed. from the University of Kashmir; I am not currently pursuing Qualified Teacher Status."*
- **Harris University M.A.**: Retained with note *"External recognition status unverified; retained for completeness as it supported eligibility for a China work visa."*
- **Safeguarding**: Only the UNICEF certification ("What We Stand For: Essentials of Children's Rights", 2026) is documented.
- **Languages**: English (Fluent), Urdu, Hindi, Marathi, Arabic (Can read), Mandarin (Basic conversation)
- **200+ educators trained** at GEDU (confirmed correct figure)
- **11+ years** experience across India and China, specialising in Years 1–6

---

## Quick PDF validation checklist

- [ ] `pdftotext <cv.pdf> -` → extracts full CV text, no blank pages
- [ ] PDF opens correctly in at least two non-Chromium viewers (e.g., Apple Preview, Foxit Reader)
- [ ] File size < 500 KB
- [ ] All text is selectable (no image‑only pages)
- [ ] Name in PDF header matches `Khan Mohammed Shehzad Anwar`