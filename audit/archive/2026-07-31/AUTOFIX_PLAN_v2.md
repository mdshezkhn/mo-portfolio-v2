# AUTOFIX PLAN v2.0

**Generated:** 2026-07-31
**Source:** GLOBAL_AUDIT_REPORT.md v2.0
**Status:** PROPOSED — DO NOT APPLY WITHOUT OWNER REVIEW

> **RULE:** This plan proposes corrections. No file has been modified. Every recommendation cites evidence and the canonical value. Apply patches only after owner review.

---

## CRITICAL FIXES (Must Be Resolved Before Any Publication)

---

### FIX-001 — Unify Organisation ID Namespace
**Finding:** F-001
**Problem:** Three competing ID namespaces: `ORG-001` (CANONICAL_PROFILE), `ORG-1000` (organisations.yml), `ORG-0001` (ID_REGISTRY)
**Affected Files:**
- `CANONICAL_PROFILE.md`
- `career-data/facts/organisations.yml`
- `governance/ID_REGISTRY.yml`
**Canonical Value:** Adopt `ORG-1000` series (from organisations.yml) as the canonical namespace.
**Recommended Correction:**
1. Update `CANONICAL_PROFILE.md` to use `ORG-1000` through `ORG-1006`
2. Update `ID_REGISTRY.yml` to reference `ORG-1000` series only
3. Retire `ORG-001` and `ORG-0001` series
**Confidence:** High
**Reason:** `organisations.yml` is the Level 1 canonical source per `SOURCE_AUTHORITY.md`.

---

### FIX-002 — Unify Institution ID Namespace
**Finding:** F-002
**Problem:** Three competing namespaces: `INST-001` (CANONICAL_PROFILE), `INST-9000` (institutions.yml), `INST-0001` (ID_REGISTRY)
**Affected Files:**
- `CANONICAL_PROFILE.md`
- `career-data/facts/institutions.yml`
- `governance/ID_REGISTRY.yml`
**Canonical Value:** Adopt `INST-9000` series (from institutions.yml) as the canonical namespace.
**Recommended Correction:**
1. Update `CANONICAL_PROFILE.md` to use `INST-9000` through `INST-9003`
2. Update `ID_REGISTRY.yml` to reference `INST-9000` series only
**Confidence:** High
**Reason:** `institutions.yml` is the Level 1 canonical source.

---

### FIX-003 — Unify Employment ID Namespace
**Finding:** F-003
**Problem:** Three competing namespaces: `EMP-2000` (employment.yml), `EMP-0001` (ID_REGISTRY), `EMP-001` (manifest.yml)
**Affected Files:**
- `career-data/facts/employment.yml`
- `governance/ID_REGISTRY.yml`
- `evidence/manifest.yml`
**Canonical Value:** Adopt `EMP-2000` series (from employment.yml).
**Recommended Correction:**
1. Update `evidence/manifest.yml` linked_claims from `EMP-001`/`EMP-003` etc. to `EMP-2000`/`EMP-2003` etc.
2. Update `ID_REGISTRY.yml` to reference `EMP-2000` series
**Confidence:** High
**Reason:** `employment.yml` is the Level 1 canonical source.

---

### FIX-004 — Correct PGCE End Date to July 2026
**Finding:** F-004
**Problem:** Compiled assets say "Sep 2026" but canonical says "2026-07" (July 2026).
**Affected Files:**
- `compiled_assets/CV_Master.md` line 54
- `compiled_assets/CV_Primary_EAL.md` line 34
- `compiled_assets/CV_STEM_EAL.md` line 27
- `compiled_assets/LinkedIn_Profile.md` line 60
- `compiled_assets/Portfolio_Copy.md` line 63
- `compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md` line 75
- `MASTER_BRAND_SPECIFICATION.md` line 237
**Canonical Value:** `Sep 2025 – Jul 2026` (from education.yml QUAL-3002 and CLAIM_REGISTER C-007)
**Recommended Correction:** Change all instances of "Sep 2025 – Sep 2026" to "Sep 2025 – Jul 2026"
**Confidence:** High
**Reason:** education.yml date is `2026-07`. PGCE academic calendars run Sep–Jul.

---

### FIX-005 — Standardise Role Titles Across All Assets
**Finding:** F-005, F-006
**Problem:** Role titles vary across documents. Most critically, "Director of Educator Development" in CVs is an inflation of the canonical "Educator Development Lead."
**Affected Files:**
- `compiled_assets/CV_Master.md` line 29
- `compiled_assets/CV_EAL_Coordinator.md` line 26
- `compiled_assets/CV_Teacher_Development.md` line 20
- `compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md` lines 24, 32, 39, 45, 51, 57, 63
**Canonical Values (from roles.yml and CANONICAL_PROFILE.md):**

| Employer | Canonical Title |
|---|---|
| Scholars Academy | Primary Educator |
| Zhejiang/Helen China | ESL Educator |
| Eton House | Early Years EAL Teacher |
| Aoxin (1st) | Primary Educator & Curriculum Lead |
| WhiteHat Jr | Educator Development Lead |
| GEDU | Teacher Trainer & Quality Assurance |
| Aoxin (2nd) | Primary Educator & Curriculum Lead |

**Recommended Correction:** Replace all non-canonical titles with the canonical versions above. In particular:
- Replace "Director of Educator Development" → "Educator Development Lead" everywhere
- Replace "International Teacher Trainer & Quality Assurance" → "Teacher Trainer & Quality Assurance"
- Replace "English Language Teacher" → "ESL Educator"
**Confidence:** High
**Reason:** Title inflation is the most recruiter-damaging inconsistency. `roles.yml` is the canonical source.

---

## HIGH-PRIORITY FIXES

---

### FIX-006 — Resolve GEDU Location vs. Decision D-002
**Finding:** F-007
**Problem:** `employment.yml` says "UK/Dubai/Malta" but D-002 says GEDU was India-based.
**Affected Files:**
- `career-data/facts/employment.yml` line 59
- `CANONICAL_PROFILE.md` line 40
- `career-timeline.md` line 19
- `MASTER_BRAND_SPECIFICATION.md` line 296
**Canonical Value:** Per D-002: "India" or "India (International remit)"
**Recommended Correction:** OWNER DECISION REQUIRED — Either:
  a) Update employment.yml location to "India (International)" and all downstream
  b) OR reverse D-002 if the GEDU role truly was physically located abroad
**Confidence:** Medium — requires owner input
**Reason:** The canonical data contradicts the binding governance decision.

---

### FIX-007 — Add B.Ed. Dates to Canonical Data
**Finding:** F-008
**Problem:** B.Ed. dates are UNKNOWN in education.yml but "Oct 2021 – Mar 2024" in LinkedIn.
**Affected Files:**
- `career-data/facts/education.yml` QUAL-3003
- `compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md` line 80
**Canonical Value:** OWNER DECISION REQUIRED — Confirm or deny "Oct 2021 – Mar 2024"
**Recommended Correction:** If dates are correct, update education.yml. If not, remove from LinkedIn_Ready_To_Paste.md.
**Confidence:** Medium — requires owner confirmation
**Reason:** Dates in a public asset without canonical backing is a governance violation.

---

### FIX-008 — Propagate C-025 (M.A. English) to All Assets
**Finding:** F-009
**Problem:** M.A. English is in the claim register but missing from all compiled CVs, LinkedIn_Profile.md, and Portfolio_Copy.md.
**Affected Files:**
- `compiled_assets/CV_Master.md` (education section)
- `compiled_assets/CV_EAL_Coordinator.md` (education section)
- `compiled_assets/CV_Primary_EAL.md` (education section)
- `compiled_assets/LinkedIn_Profile.md` (education section)
- `compiled_assets/Portfolio_Copy.md` (education section)
**Canonical Value:** "M.A. English Language and Literature — Harris University (2007–2009)"
**Recommended Correction:** Add M.A. to education sections of all assets where the CLAIM_REGISTER CV map includes C-025.
**Confidence:** High
**Reason:** C-025 status is Approved; "Used In: CV · LinkedIn · Portfolio."

---

### FIX-009 — Fix Evidence ID Cross-References
**Finding:** F-010
**Problem:** E-2002 means "B.Ed. Degree Certificate" in CLAIM_REGISTER but "PGCE transcript" in manifest.yml. E-2003 means "MA Degree Certificate" in CLAIM_REGISTER but "PGCE letter of completion" in manifest.yml.
**Affected Files:**
- `CLAIM_REGISTER.md` C-003 (references E-2002)
- `CLAIM_REGISTER.md` C-025 (references E-2003)
- `evidence/manifest.yml` E-2002, E-2003
**Canonical Value:** The evidence manifest is the canonical evidence registry. CLAIM_REGISTER must reference the correct IDs.
**Recommended Correction:**
1. Determine correct evidence IDs for B.Ed. certificate (likely E-0009) and M.A. certificate (likely E-0008)
2. Update CLAIM_REGISTER C-003 to reference E-0009 instead of E-2002
3. Update CLAIM_REGISTER C-025 to reference E-0008 instead of E-2003
4. Add E-2006 entry to manifest for B.Sc. OR update CLAIM_REGISTER C-008 to reference E-0010
**Confidence:** High
**Reason:** Cross-reference integrity is essential for the traceability pipeline.

---

### FIX-010 — Fix Scholars Academy Confidence Level
**Finding:** F-011
**Problem:** employment.yml says "confidence: verified" but governance says Evidence Quality C / Low.
**Affected Files:**
- `career-data/facts/employment.yml` EMP-2000 line 10
**Canonical Value:** Per MASTER_BRAND_SPECIFICATION C-024: confidence should be `asserted` or `plausible` (not `verified`)
**Recommended Correction:** Change `confidence: verified` to `confidence: asserted` for EMP-2000
**Confidence:** High
**Reason:** MASTER_BRAND_SPECIFICATION is the authority on evidence levels.

---

### FIX-011 — Add Publication Block Warning to Compiled Assets
**Finding:** F-012
**Problem:** C-001 and C-002 are marked "Pending — do not publish" but all compiled assets publish them.
**Affected Files:** All compiled_assets/ files
**Canonical Value:** C-001 and C-002 should either (a) not appear until P0 evidence is filed, or (b) be formally approved for publication
**Recommended Correction:** OWNER DECISION REQUIRED — Either:
  a) Remove "11+" and "India and China" from all compiled assets until P0 evidence filed
  b) OR formally approve C-001 and C-002 for publication by updating their CLAIM_REGISTER status to "Approved"
**Confidence:** Medium — requires owner decision
**Reason:** Publishing pending claims violates the governance framework.

---

### FIX-012 — Add Hindi/Urdu to Portfolio
**Finding:** F-013
**Problem:** Portfolio_Copy.md only lists English; Hindi and Urdu are missing.
**Affected Files:**
- `compiled_assets/Portfolio_Copy.md` line 70–71
**Canonical Value:** C-020 (English), C-021 (Hindi), C-022 (Urdu)
**Recommended Correction:** Add Hindi (Native) and Urdu (Working proficiency) to Portfolio_Copy.md languages section
**Confidence:** High
**Reason:** Direct propagation failure.

---

### FIX-013 — Remove UK/Dubai/Malta from LinkedIn and Portfolio Narratives
**Finding:** F-014
**Problem:** LinkedIn and Portfolio About sections mention "UK, Dubai, and Malta" — violating D-002.
**Affected Files:**
- `compiled_assets/LinkedIn_Profile.md` line 47
- `compiled_assets/Portfolio_Copy.md` line 51
**Canonical Value:** Per D-002: Use "international markets" not specific country names
**Recommended Correction:** Replace "across UK, Dubai, and Malta" with "across international markets" or similar general wording
**Confidence:** High
**Reason:** D-002 is a binding governance decision.

---

### FIX-014 — Fix Evidence Manifest Claim Links
**Finding:** F-024
**Problem:** E-2001, E-2002, E-2003 all link to `C-002` (Countries) instead of `C-004` (PGCE).
**Affected Files:**
- `evidence/manifest.yml` lines 40, 49, 58
**Canonical Value:** PGCE documents should link to C-004
**Recommended Correction:** Change `linked_claims: ["C-002"]` to `linked_claims: ["C-004"]` for E-2001, E-2002, E-2003
**Confidence:** High
**Reason:** PGCE certificate cannot be evidence for a countries claim.

---

## MEDIUM-PRIORITY FIXES

---

### FIX-015 — Complete career-timeline.md with Missing Roles
**Finding:** F-019
**Affected Files:** `career-timeline.md`
**Correction:** Add Eton House (Aug 2017 – Jun 2018) and Zhejiang (Nov 2016 – Aug 2017) entries. Fix "7 listed roles" count.

### FIX-016 — Fix Duplicate Bullets in CV_Primary_EAL
**Finding:** F-020
**Affected Files:** `compiled_assets/CV_Primary_EAL.md` lines 18–20 vs 24–26
**Correction:** Differentiate the Aoxin 2024–Present bullets from the 2018–2020 bullets.

### FIX-017 — Replace Placeholder Content in CV_STEM_EAL
**Finding:** F-021
**Affected Files:** `compiled_assets/CV_STEM_EAL.md`
**Correction:** Replace raw claim text with professional CV bullet points.

### FIX-018 — Fix Chronological Order in CV_Teacher_Development
**Finding:** F-022
**Affected Files:** `compiled_assets/CV_Teacher_Development.md`
**Correction:** Reorder to reverse-chronological: Aoxin (2024–Present) first.

### FIX-019 — Reconcile EVIDENCE_INDEX.md with manifest.yml
**Finding:** F-023
**Affected Files:** `EVIDENCE_LIBRARY/EVIDENCE_INDEX.md`
**Correction:** Populate from evidence/manifest.yml entries or archive the file.

### FIX-020 — Archive BRAND_SPECIFICATION.md
**Finding:** F-025
**Affected Files:** `BRAND_SPECIFICATION.md`
**Correction:** Move to `archive/` and add "SUPERSEDED" header.

### FIX-021 — Fix Section Numbering in BRAND_SPECIFICATION.md
**Finding:** F-026
**Affected Files:** `BRAND_SPECIFICATION.md` line 124
**Correction:** Renumber duplicate section 9 to section 10.

### FIX-022 — Add Aoxin 2nd Stint to Evidence Manifest
**Finding:** F-027
**Affected Files:** `evidence/manifest.yml`
**Correction:** Add E-0006B entry for Aoxin (Feb 2024 – Present).

### FIX-023 — Fix Duplicate Context Line in Achievement Library
**Finding:** F-028
**Affected Files:** `Achievement_Library.md` line 71
**Correction:** Remove the duplicate "Context: Eton House Kindergarten" line.

### FIX-024 — Archive or Integrate Evidence_Register.md
**Finding:** F-029
**Affected Files:** `Evidence_Register.md`
**Correction:** Archive since evidence/manifest.yml is the active register.

### FIX-025 — Reorder CANONICAL_PROFILE Employment Records
**Finding:** F-030
**Affected Files:** `CANONICAL_PROFILE.md`
**Correction:** Reorder employment records chronologically (oldest to newest or newest to oldest — consistently).

### FIX-026 — Fix Schema Section 5 Duplicate
**Finding:** F-039
**Affected Files:** `SCHEMA.md` line 116
**Correction:** Renumber to "6. JSON Profile Schema"

### FIX-027 — Fix career-timeline.md File Reference
**Finding:** F-037
**Affected Files:** `career-timeline.md` line 37
**Correction:** Change `CLAIMS_REGISTER.md` to `CLAIM_REGISTER.md`

### FIX-028 — Resolve E-3005 ID Collision
**Finding:** F-040
**Affected Files:** `evidence/manifest.yml`, `CLAIM_REGISTER.md`
**Correction:** Assign a new evidence ID (e.g., E-3006) for the Aoxin endorsement letter, distinct from the Zhejiang employment verification.

---

## LOW-PRIORITY FIXES

---

### FIX-029 — Establish Single Canonical LinkedIn Headline
**Finding:** F-031
**Correction:** Choose one headline and enforce across all LinkedIn documents.

### FIX-030 — Add C-023 (Availability) to LinkedIn_Profile.md
**Finding:** F-008 (propagation)
**Correction:** Add "Available from August 2027" to LinkedIn_Profile.md.

### FIX-031 — Add Scholars Academy Entry to Achievement Library
**Finding:** F-034
**Correction:** Add VA-006 for Scholars Academy (Jan 2014 – Nov 2016).

### FIX-032 — Add E-2006 or Fix C-008 Reference
**Finding:** F-036
**Correction:** Either add E-2006 to manifest (B.Sc.) or update C-008 to reference E-0010.

### FIX-033 — Validate PGCE Grade 75/100 or Remove
**Finding:** F-017
**Correction:** If grade is real, add to education.yml. If not, remove from LinkedIn Master Profile.

---

## INFORMATION / IMPROVEMENT OPPORTUNITIES

---

### FIX-034 — Populate Evidence Directories
**Finding:** F-041
**Correction:** Add actual evidence files to `evidence/credentials/`, `evidence/employment/`, etc.

### FIX-035 — Remove or Document hash1.txt/hash2.txt
**Finding:** F-043
**Correction:** Delete or add README explaining purpose.

### FIX-036 — Clarify Authority Between MASTER_PORTFOLIO_SPECIFICATION and MASTER_BRAND_SPECIFICATION
**Finding:** F-044
**Correction:** Define scope boundaries (portfolio = visual/structural, brand = content/claims).

### FIX-037 — Create 08_Offer_and_Contract_Guide.md or Remove Reference
**Finding:** F-045
**Correction:** Create the file or mark as "Planned" in the index with no link.

---

## EXECUTION PRIORITY

```
PHASE 1 (Immediate — Before Any Publication):
  FIX-004 (PGCE dates)
  FIX-005 (Role titles — especially "Director" → "Lead")
  FIX-013 (Remove UK/Dubai/Malta from narratives)
  FIX-011 (Resolve C-001/C-002 publication status)

PHASE 2 (This Week):
  FIX-001, FIX-002, FIX-003 (ID namespace unification)
  FIX-009 (Evidence ID cross-references)
  FIX-010 (Scholars Academy confidence)
  FIX-014 (Manifest claim links)

PHASE 3 (Before First Application):
  FIX-006 (GEDU location — requires owner decision)
  FIX-007 (B.Ed. dates — requires owner confirmation)
  FIX-008 (M.A. propagation)
  FIX-012 (Portfolio languages)
  FIX-015 through FIX-028 (Medium-priority fixes)

PHASE 4 (Ongoing):
  FIX-029 through FIX-037 (Low and info fixes)
```

---

*This plan was generated as part of the GLOBAL_AUDIT_REPORT v2.0. No files have been modified. All corrections require owner review before application.*