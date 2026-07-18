# Changelog

This changelog documents the specific edits made during Phase 4 (Recruiter Trust & Conversion Optimization) to maximize recruiter trust while preserving complete factual accuracy. No structural code refactoring or visual redesigns were introduced during this phase.

## [2026-07-18] - Phase 4 Conversion Edits

### Modified Files

#### `index.html`
- **Change:** Audited and corrected all references to the teaching qualification. Changed instances of "PGCE" and "PGCE — Education" to the strict terminology: `"Postgraduate Certificate in Education (PGCE), University of Cumbria"`.
- **Reason:** To prevent any ambiguity regarding the qualification, its origin, and its status. Prevents the qualification from being confused with unverified "iPGCE" or "QTS" claims.
- **Expected Recruiter Impact:** Increases compliance trust. The recruiter knows exactly what the qualification is and where it is from, mitigating HR/visa risk.
- **Risk Assessment:** Low. Purely a text replacement.

- **Change:** Revised leadership claims in the "About Me", "Career Journey", and "Leadership Value" sections. Replaced phrases like "managed instructional quality" and "architecting quality-assurance frameworks" with strictly evidence-based alternatives like "contributed to quality assurance" and "demonstrated the ability to improve instructional quality beyond the classroom."
- **Reason:** To align the copy strictly with the evidence presented in the CV, ensuring the candidate does not imply they held formal Head of Department or SLT titles when they did not.
- **Expected Recruiter Impact:** Builds trust through verifiable honesty. Recruiters are highly sensitive to exaggerated claims; precise language proves reliability.
- **Risk Assessment:** Low. Preserves the candidate's achievements without risking perceived inflation.

### New Documentation Created

#### `docs/RECRUITER_OBJECTION_MAP.md`
- **Change:** Created a matrix mapping 15 common recruiter objections against the portfolio's existing evidence.
- **Reason:** To identify where the candidate's claims are strong, and where the candidate needs to inject specific evidence (e.g., CV updates, video) to close trust gaps.
- **Expected Recruiter Impact:** N/A (Internal document). Ensures the final asset uploads explicitly target recruiter objections.

#### `docs/GALLERY_CURATION_GUIDE.md`
- **Change:** Created a framework defining the pedagogical purpose of 8-10 recommended gallery images.
- **Reason:** To prevent the gallery from becoming a useless "photo album." 
- **Expected Recruiter Impact:** N/A (Internal document). Ensures the Principal sees active learning, STEM integration, and behavior management rather than posed smiles.

#### `recruiter_journey.md` (Artifact Update)
- **Change:** Inserted "Trust & Professional Credibility" and "Cultural & Community Fit" checkpoints into the recruiter journey map.
- **Reason:** To formalize the psychological gates a Principal must pass through before feeling comfortable offering an interview.

---

### Final Validation
- Verification confirmed no structural HTML changes were made.
- `grep_search` confirmed `iPGCE` and `QTS` do not exist in the codebase.
- Factually accurate qualifications consistently applied.
