# TECHNICAL_DEBT.md

**Version:** 1.0 (Career OS v4.0)
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-30

**Purpose:** Tracks all known engineering, data integrity, and governance issues that exist but have not yet been resolved. Distinct from Evidence Gap Register (which covers missing professional evidence) and Claim Register (which covers provenance). This document covers *system* and *data model* shortcomings.

**Rule:** Every item in this register must have an owner and a target milestone. Items are marked RESOLVED when closed, never deleted.

---

## Priority Key

| Priority | Meaning |
|---|---|
| **CRITICAL** | Blocks publication; must be resolved before any release |
| **HIGH** | Should be resolved before Week 2 completion |
| **MEDIUM** | Should be resolved before v1.0.0 release |
| **LOW** | Desirable; can be deferred to post-launch maintenance |

---

## Open Items

### TD-001
**Priority:** CRITICAL → RESOLVED in Week 2
**Category:** Data Architecture
**Issue:** `build.py` reads from a flat JSON structure, not from `career-data/facts/` YAML. Any generation run produces outputs that are not governed by the Career Model.
**Impact:** All currently generated CVs and portfolio HTML are NOT evidence-traceable. They are manually authored documents.
**Resolution Plan:** Week 3 — upgrade `build.py` to read exclusively from `career-data/facts/` and `career-data/narratives/`
**Target Milestone:** Week 3
**Owner:** Claude Code

---

### TD-002
**Priority:** HIGH
**Category:** Repository Governance
**Issue:** The workspace root (`Mo Digital Portfolio/`) is a mixed-purpose directory containing private governance, public portfolio, and legacy/archive material with no clear separation.
**Impact:** Risk of inadvertently committing private governance files to the public repository.
**Resolution Plan:** Week 1 — complete directory restructure; Week 2 — add `.gitignore` rules ensuring `governance/`, `evidence/`, `private/`, and `career-data/` are excluded from `mo-portfolio-v2` remote
**Target Milestone:** Week 1
**Owner:** Claude Code

---

### TD-003
**Priority:** HIGH
**Category:** Data Integrity
**Issue:** Harris University institution recognition status is unverified. `education.yml` will carry `confidence: needs_review` and `institution_recognition_status: REQUIRES_EXTERNAL_VERIFICATION`.
**Impact:** Medium-high recruiter risk in premium school contexts. Mitigated by `premium_schools: false` publication flag.
**Resolution Plan:** Contact Harris University directly or via British Council recognition check. Update manifest entry E-0008 when evidence obtained.
**Target Milestone:** See G-006 in EVIDENCE_GAP_REGISTER.md (target: 2026-12-01)
**Owner:** Mohammed Shehzad Khan

---

### TD-004
**Priority:** HIGH
**Category:** Data Integrity
**Issue:** B.Ed. study period unknown. No physical evidence document has been added to `evidence/credentials/` yet.
**Correction (Week 1 Amendment):** Previous status of `BLOCKED_FROM_PUBLICATION` was incorrect. The qualification exists and is owner-confirmed. The correct status is `EVIDENCE_COLLECTION_REQUIRED`. Publication is ALLOWED. There is a critical distinction between *evidence not yet collected into the repository* and *a qualification that should not appear publicly*.
**Impact:** Credential cannot carry `confidence: verified` until document is added. Appears in public CV with `confidence: plausible` until resolved.
**Resolution Plan:** Owner to locate physical B.Ed. certificate or transcript and add to `evidence/credentials/`. Update manifest entry E-0009 on receipt.
**Target Milestone:** See G-007 in EVIDENCE_GAP_REGISTER.md (target: 2026-08-01)
**Owner:** Mohammed Shehzad Khan

---

### TD-005
**Priority:** HIGH
**Category:** Data Integrity
**Issue:** All 7 employment contract titles marked "Pending verification." Contract title field in `employment.yml` will carry `confidence: needs_review` for all roles.
**Impact:** Cannot generate fully-verified employment record. Portfolio Display Titles used as fallback.
**Resolution Plan:** Request HR confirmation letters or obtain contract copies for each employer. Update per-entry as evidence arrives.
**Target Milestone:** Ongoing — see Evidence Gap Register (G-001, G-008)
**Owner:** Mohammed Shehzad Khan

---

### TD-006
**Priority:** MEDIUM
**Category:** Data Integrity
**Issue:** Aoxin gap (Aug 2020 – Feb 2024: approximately 3.5 years) has no canonical explanation in the career record. WhiteHat Jr / BYJU'S and GEDU cover part of this period; full timeline continuity not verified.
**Impact:** Recruiter question risk — "What happened between 2020 and 2024?" flagged as mandatory RECRUITER_QA entry.
**Resolution Plan:** Week 2 — add `gap_explanation` field to `employment.yml` for the 2020–2024 period; cross-reference with WhiteHat Jr and GEDU dates.
**Target Milestone:** Week 2
**Owner:** Mohammed Shehzad Khan

---

### TD-007 — RESOLVED (Week 1)
**Priority:** ~~MEDIUM~~ RESOLVED
**Category:** CI/CD
**Issue:** GitHub Actions `deploy.yml` in `mo-portfolio-v2` listened on `master` branch; canonical working branch is `main`.
**Resolution:** Updated `deploy.yml` branch trigger to `main` in Week 1 commit (Decision D-007).
**Resolved Date:** 2026-07-30
**Resolved By:** Claude Code

---

### TD-008
**Priority:** MEDIUM
**Category:** Evidence Governance
**Issue:** SHA-256 checksums deferred until repository structure is frozen (end of Week 2). Until then, `validate_evidence.py` can only verify ID existence, not file integrity.
**Impact:** Evidence integrity cannot be fully guaranteed during Week 1–2 restructuring. Acceptable trade-off; see manifest checksum deferral policy.
**Resolution Plan:** End of Week 2 — compute and record all checksums; activate integrity validation.
**Target Milestone:** Week 2 end
**Owner:** Claude Code

---

### TD-009
**Priority:** LOW
**Category:** Application Engine
**Issue:** Recruiter Evidence Pack Generator (`generate_recruiter_pack.py`) will only produce BRITISH_CURRICULUM context pack during Week 3. Remaining 6 contexts deferred to Week 4.
**Impact:** Application engine operational but not at full capacity for v1.0.0 release.
**Resolution Plan:** Week 4 — generate remaining 6 context packs.
**Target Milestone:** Week 4
**Owner:** Claude Code

---

## Resolved Items

*(None yet — will be populated as items are closed)*

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-30 | Initial — TD-001 through TD-009 pre-populated |
