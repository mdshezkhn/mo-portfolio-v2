# ASSET_COMPLIANCE_REPORT.md

**Layer:** Compliance (Layer 5 of 6)
**Purpose:** Validates every public asset against the approved claims in `CLAIM_REGISTER.md` and the governance rules in `MASTER_BRAND_SPECIFICATION.md`. A public asset may only be published if it passes this report. This document is updated each time a public asset is created, modified, or when the Claim Register changes.

**Compliance Reports are not evidence.** They validate; they do not generate evidence or claims.

**Version:** COMP-1.0
**Status:** Template — no public assets yet approved for publication
**Owner:** Mohammed Shehzad Khan
**Last Reviewed:** 2026-07-25

---

## Document Version Tracker

*Track the current approved version of every layer in the governance stack. When a compliance audit is run, record the versions audited against.*

| Layer | Document | Current Version | Last Updated |
|-------|----------|-----------------|--------------|
| Layer 2 — Evidence Management | EVIDENCE_LIBRARY/EVIDENCE_INDEX.md | ER-1.0 | 2026-07-25 |
| Layer 2 — Evidence Lifecycle | Evidence_Register.md | ER-1.0 | 2026-07-25 |
| Layer 2 — Evidence Acquisition | Evidence_Acquisition_Plan.md | EAP-1.0 | 2026-07-25 |
| Layer 3 — Governance | MASTER_BRAND_SPECIFICATION.md | BS-1.0-DRAFT | 2026-07-25 |
| Layer 4 — Claims | CLAIM_REGISTER.md | CR-1.0-DRAFT | 2026-07-25 |
| Layer 6 — CV | (not yet published) | — | — |
| Layer 6 — LinkedIn | (not yet published) | — | — |
| Layer 6 — Portfolio | portfolio-v3/index.html | PORT-3.x | — |
| Layer 6 — Cover Letters | (templates pending) | — | — |
| Layer 6 — Interview Prep | (pending) | — | — |

---

## Pre-Publication Gate

> **No public asset may be published until ALL of the following are true:**
> 1. `MASTER_BRAND_SPECIFICATION.md` status is `Version 1.0 APPROVED` (not DRAFT)
> 2. Open Human Decisions (Decision 1 — years; Decision 2 — countries) are resolved
> 3. Every claim used in the asset has Status: **Approved** in `CLAIM_REGISTER.md`
> 4. Every claim used in the asset appears in the asset's Claim Map in `CLAIM_REGISTER.md`
> 5. The asset passes the Recruiter Read Test (5 stages) in `MASTER_BRAND_SPECIFICATION.md`

**Current gate status:** ❌ BLOCKED — `MASTER_BRAND_SPECIFICATION.md` is Version 1.0-DRAFT. Open Human Decisions unresolved.

---

## Compliance Audit Template

*Copy this template for each audit. Fill in the asset version, the specification versions audited against, and the results.*

```
AUDIT DATE: ____-__-__
AUDITOR: Mohammed Shehzad Khan
ASSET: [CV / LinkedIn / Portfolio / Cover Letter / Interview Prep]
ASSET VERSION: [e.g. CV-1.0]

BUILT FROM (Asset Version Lock):
  BS-____ (Brand Specification)
  CR-____ (Claim Register)
  ER-____ (Evidence Index)

CLAIMS USED IN THIS ASSET:
  [ ] C-001  [ ] C-002  [ ] C-003  [ ] C-004  [ ] C-005
  [ ] C-006  [ ] C-007  [ ] C-008  [ ] C-009  [ ] C-010
  [ ] C-011  [ ] C-012  [ ] C-013  [ ] C-014  [ ] C-017
  [ ] C-019  [ ] C-020  [ ] C-021  [ ] C-022  [ ] C-023

CLAIM STATUS CHECK:
  All used claims have Status: Approved in CLAIM_REGISTER.md?  [ ] Yes  [ ] No
  All used claims appear in this asset's Claim Map?             [ ] Yes  [ ] No
  Any Restricted claims (C/Low) used?                           [ ] No   [ ] Yes → FAIL

METRICS CHECK:
  All numerical values appear in Approved Metrics Register?     [ ] Yes  [ ] No
  Any metric with status HOLD used?                             [ ] No   [ ] Yes → FAIL

TERMINOLOGY CHECK:
  All terms follow Canonical Terminology table?                 [ ] Yes  [ ] No

RECRUITER READ TEST:
  10-second scan: identity and specialism clear?                [ ] Pass [ ] Fail
  30-second skim: no contradictions or inflation?               [ ] Pass [ ] Fail
  2-minute review: specific, consistent, evidence-matched?      [ ] Pass [ ] Fail
  ATS parsing: key terms appear naturally?                      [ ] Pass [ ] Fail
  Interview consistency: every claim answerable without docs?   [ ] Pass [ ] Fail

RESULT:
  [ ] PASS — asset approved for publication
  [ ] FAIL — asset must be revised (list issues below)

ISSUES (if FAIL):
  1.
  2.
  3.

SIGN-OFF: ______________________  DATE: ____-__-__
```

---

## Audit Log

### CV

| Audit Date | Asset Version | Spec Version | CR Version | Result | Issues |
|------------|---------------|-------------|------------|--------|--------|
| — | — | — | — | Not yet audited | CV not yet drafted — awaiting P0 evidence and resolution of Decisions 1 & 2 |

### LinkedIn Profile

| Audit Date | Asset Version | Spec Version | CR Version | Result | Issues |
|------------|---------------|-------------|------------|--------|--------|
| — | — | — | — | Not yet audited | LinkedIn not yet updated against specification |

### Portfolio (portfolio-v3)

| Audit Date | Asset Version | Spec Version | CR Version | Result | Issues |
|------------|---------------|-------------|------------|--------|--------|
| — | — | — | — | Not yet audited | Portfolio not yet audited against specification |

### Cover Letters

| Audit Date | Asset Version | Spec Version | CR Version | Result | Issues |
|------------|---------------|-------------|------------|--------|--------|
| — | — | — | — | Not yet audited | Cover letter templates not yet created |

### Interview Preparation Materials

| Audit Date | Asset Version | Spec Version | CR Version | Result | Issues |
|------------|---------------|-------------|------------|--------|--------|
| — | — | — | — | Not yet audited | Interview prep not yet created against specification |

---

## Known Non-Compliance (Current)

> This section documents known gaps between existing public assets and the specification. It is not a failure log — it is an honest record of work to be done. All items below are pre-existing issues that existed before this governance system was established.

| Asset | Non-Compliance | Claim Affected | Action Required | Priority |
|-------|---------------|----------------|-----------------|----------|
| Portfolio (portfolio-v3) | Professional headline may not match Canonical Identity from BS | C-009 | Audit and align | P1 |
| Portfolio (portfolio-v3) | CV download link returns 404 | — | Replace with intentional placeholder per EAP guidance | P0 |
| LinkedIn | Not yet audited against specification | All | Full audit required | P1 |
| All assets | C-001 (years) uses unresolved figure | C-001 | Freeze until Decision 1 resolved | P0 |
| All assets | C-002 (countries) uses unresolved definition | C-002 | Freeze until Decision 2 resolved | P0 |

---

## Dependency Rules

*These rules govern which layers may reference which others. Violations create circular dependencies and undermine auditability.*

| Layer | May Reference | Must Not Reference |
|-------|---------------|--------------------|
| Primary Sources (Layer 1) | Nothing | Anything above Layer 1 |
| Evidence Index (Layer 2) | Primary Sources only | Layers 3–6 |
| Evidence Register (Layer 2) | Evidence IDs only | Layers 3–6 |
| Brand Specification (Layer 3) | Evidence Levels, Claim IDs | Raw document names, Asset content |
| Claim Register (Layer 4) | Evidence IDs, Asset IDs | Raw document names |
| Compliance Report (Layer 5) | All layers | May reference but never becomes evidence |
| Public Assets (Layer 6) | Approved Claim IDs only | Evidence IDs, raw documents, unregistered claims |

---

## Change Log

| Date | Version | Change | Notes |
|------|---------|--------|-------|
| 2026-07-25 | COMP-1.0 | Initial compliance report created | No public assets yet audited. Pre-publication gate is currently BLOCKED pending BS-1.0 APPROVED status. Known non-compliance items documented. |
