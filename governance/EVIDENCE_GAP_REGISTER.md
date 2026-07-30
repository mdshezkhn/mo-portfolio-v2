# EVIDENCE_GAP_REGISTER.md

**Version:** 1.0 (Career OS v4.0)
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-30

**Purpose:** A one-year acquisition roadmap identifying documents that, if obtained, would meaningfully strengthen the professional record. Distinct from Technical Debt (engineering issues) and the Claim Register (provenance).

This register answers: *"What evidence would most improve the defensibility and credibility of this application, and by when must it be obtained?"*

**Rule:** When a gap is filled, the corresponding evidence entry is added to `evidence/manifest.yml`, the relevant YAML field is updated, the confidence level is raised, and the gap is marked CLOSED with a resolution date.

---

## Impact Key

| Impact | Meaning |
|---|---|
| **CRITICAL** | Blocks publication of a credential or claim entirely (`BLOCKED_FROM_PUBLICATION`) |
| **HIGH** | Significantly improves recruiter credibility or unlocks a major claim |
| **MEDIUM** | Strengthens specific claim categories; useful for premium-context packs |
| **LOW** | Marginal improvement; desirable but not urgent |

---

## Gap Register

| Gap ID | Document / Evidence | Impact | Priority | Action Required | Evidence ID When Closed | Target Date | Status |
|---|---|---|---|---|---|---|---|
| G-001 | Classroom observation report (current Aoxin role) | HIGH | High | Request from line manager or Head of Department at Aoxin | TBD | 2026-09-01 | OPEN |
| G-002 | Reference letter from GEDU Global Education | HIGH | High | Contact GEDU HR or former line manager; request on headed paper | TBD | 2026-09-15 | OPEN |
| G-003 | Teacher training session attendance records or certificates | MEDIUM | Medium | Consolidate from email confirmations, event records, or LMS data at WhiteHat Jr / GEDU | TBD | 2026-08-01 | OPEN |
| G-004 | Teaching demonstration video (current academic year) | HIGH | High | Record a 15–20 minute lesson with appropriate consent; upload to private evidence folder | TBD | 2026-10-01 | OPEN |
| G-005 | Student work samples with written parental consent | MEDIUM | Medium | Collect with signed parental permission forms; photographs acceptable | TBD | 2026-11-01 | OPEN |
| G-006 | Harris University degree verification or institutional recognition confirmation | HIGH | High | Contact Harris University registrar directly, or submit recognition query to British Council or AIU | E-0008 | 2026-12-01 | OPEN |
| G-007 | B.Ed. certificate or official transcript (University of Kashmir) | CRITICAL | High | Search personal records; contact university registrar if document not found; required before credential can be published | E-0009 | 2026-08-01 | OPEN |
| G-008 | Aoxin employment verification letter (first appointment: Jul 2018 – Aug 2020) | MEDIUM | Medium | Request HR confirmation letter on school headed paper; email or original acceptable | E-0006A | 2026-09-01 | OPEN |

---

## Impact on Application Strategy

### Gaps Affecting Strategy A (Premium International Schools)

- G-001 (observation report) — essential for premium hiring contexts that require peer or leadership endorsement
- G-004 (teaching video) — increasingly required by premium schools as part of shortlisting
- G-006 (Harris University) — `premium_schools: false` flag will remain until resolved

### Gaps Affecting Strategy B (Mid-Tier International Schools)

- G-002 (GEDU reference) — supports teacher training credibility across all contexts
- G-003 (training records) — required to publish the "1,000+ educators trained" metric at full confidence

### Gaps Affecting Credential Publication

- G-007 — B.Ed. is currently `BLOCKED_FROM_PUBLICATION`. This gap must be resolved before the credential can appear in any public document.

---

## Closed Gaps

*(None yet — will be populated as gaps are resolved)*

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-30 | Initial — G-001 through G-008 pre-populated |
