# SCHEMA.md

**Purpose:** This document freezes the structural conventions of the Professional Brand Governance Framework. To ensure long-term auditability and prevent fragmentation, these schemas must not be altered once evidence and claims have been indexed against them.

**Status:** FROZEN
**Version:** SCHEMA-1.0
**Owner:** Mohammed Shehzad Khan
**Last Reviewed:** 2026-07-25

---

## 1. Identifier Formats

### Evidence IDs
- **Format:** `E-XXXX` (four-digit, categorized by range)
- **Example:** `E-2001`
- **Rule:** Assigned based on the category of the evidence to avoid mixing types. Never reused or deleted. If a document is updated, mark the old ID as `Superseded` and issue a new ID within the same range.

**Category Ranges:**
| Range | Category |
|---|---|
| E-1000–1999 | Identity |
| E-2000–2999 | Qualifications |
| E-3000–3999 | Employment |
| E-4000–4999 | Research & Publications |
| E-5000–5999 | Professional Development |
| E-6000–6999 | Performance & Impact |
| E-7000–7999 | Awards & Recognition |
| E-8000–8999 | Supporting Evidence |

### Claim IDs
- **Format:** `C-XXX` (three-digit, zero-padded)
- **Example:** `C-014`
- **Rule:** Assigned sequentially when a claim is added to the Traceability Matrix. Never reused or deleted. If a claim is retired, mark status as `Retired`.

---

## 2. Version Numbering

Every governance layer uses strict version tracking.

| Layer | Prefix | Format | Example |
|-------|--------|--------|---------|
| Evidence Management | ER- | Major.Minor | ER-1.2 |
| Brand Specification | BS- | Major.Minor | BS-1.0 |
| Claim Register | CR- | Major.Minor | CR-1.0 |
| Compliance Report | COMP- | Major.Minor | COMP-1.0 |
| Schema | SCHEMA- | Major.Minor | SCHEMA-1.0 |

### Version Bump Rules
- **Major bump (1.0 → 2.0):** Structural change to the document or a major career transition.
- **Minor bump (1.0 → 1.1):** Addition of new evidence, resolution of a human decision, or a claim wording update.
- **-DRAFT suffix:** Document is under active revision and has not yet passed a compliance audit. (e.g., `BS-1.0-DRAFT`).

---

## 3. Claim Status Schema

Every claim in `CLAIM_REGISTER.md` must hold one of the following states:

| Status | Meaning | Usage |
|--------|---------|-------|
| **Draft** | Idea or unverified claim | Internal only; must not be published |
| **Pending** | Awaiting owner decision or evidence | Internal only; must not be published |
| **Approved** | Verified against A/B level evidence | Cleared for use in Public Assets |
| **Restricted** | Supported by C/Low evidence | Internal only; defensible but not for print |
| **Retired** | Claim no longer used or relevant | Kept for audit trail only |
| **Superseded**| Replaced by a newer version/wording | Kept for audit trail only |

---

## 4. Verification Levels

To distinguish between claims backed by original documents and those awaiting stronger evidence, every evidence item is assigned a Verification Level:

| Level | Meaning |
|-------|---------|
| **V1** | Original primary document (e.g., original certificate, signed contract) |
| **V2** | Official institutional record (e.g., transcript, HR system export) |
| **V3** | Employer-issued document (e.g., recommendation letter, performance review) |
| **V4** | Corroborated secondary evidence (e.g., news article, third-party publication) |
| **V5** | Self-reported only (e.g., unverified CV claim, personal statement) |

---

## 5. Folder and Naming Conventions

The repository structure is strictly defined to separate public assets from private evidence and governance logic.

### Folder Structure
```
/
├── /private/
│   ├── /Contracts/              (Employment letters, HR correspondence)
│   ├── /Original Certificates/  (Degree, PGCE, TESOL, TEFL)
│   └── /Working Docs/           (Personal statements, interview prep notes)
├── /EVIDENCE_LIBRARY/
│   └── EVIDENCE_INDEX.md
├── /portfolio-v3/               (Public portfolio asset)
```

### Governance File Naming
- `SCHEMA.md`
- `Evidence_Acquisition_Plan.md`
- `Evidence_Register.md`
- `MASTER_BRAND_SPECIFICATION.md`
- `CLAIM_REGISTER.md`
- `ASSET_COMPLIANCE_REPORT.md`

### Document Immutability
- Documents in `/private/` are **immutable**. Once filed, they are read-only.
- If an immutable document needs correction, the new version is filed alongside the old, and a new `E-XXXX` ID is assigned.

---

## 5. JSON Profile Schema (`templates/cv/profiles/*.json`)

The generated outputs in `compiled_assets/` rely on a strictly structured JSON profile. All CV variants must conform to this schema structure.

```json
{
  "title": "String (Short internal name)",
  "asset_name": "String (e.g. CV_Master_v3.0)",
  "subtitle": "String (e.g. Primary Educator)",
  "claims": ["Array of C-XXX strings"],
  "summary": "String",
  "competencies": ["Array of strings"],
  "experience": [
    {
      "company": "String (must match Employer in canonical)",
      "date": "String (e.g. Feb 2024 – Present)",
      "title": "String (must match Portfolio Display Title in canonical)",
      "bullets": ["Array of strings"]
    }
  ],
  "education": ["Array of strings"]
}
```

---

## 6. Evidence Ingestion Standard

For every uploaded document, four outputs must be produced before the Canonical Profile is modified:

1. **Evidence Record:** Metadata only. Must include the following fields:
   - **Evidence ID:** (e.g., E-2001)
   - **Document Title:**
   - **Verification Level:** (V1 - V5)
   - **Evidence Confidence:** (High / Medium / Low)
   - **Document Version:**
   - **Supersedes Evidence ID:** (if applicable)
2. **Fact Extraction:** A list of objective facts copied or faithfully paraphrased from the document (no interpretation).
3. **Claim Mapping:** Which atomic claims are supported and whether the support is complete or partial.
4. **Consistency Review:** Compare extracted facts against the Canonical Profile and categorize as Match, Conflict, Missing, or Not Applicable.

Only after all four are complete should any verification status change.

---

## 7. Conflict Policy

**Document Precedence Rule:** If documentary evidence conflicts with the Canonical Profile, the Canonical Profile is not updated automatically. The conflict must be logged, investigated, and resolved before any canonical data is changed. This prevents accidental corruption due to transcription mistakes or outdated documents.

---

## 8. Governance Freeze Rule

Changes to the governance model (schema, validation rules, evidence taxonomy, claim taxonomy, canonical structure, or verification workflow) require demonstrated need arising from real evidence ingestion. Governance must not be expanded solely in anticipation of hypothetical future requirements. 

---

## 9. RC-2 Goals & KPIs (Evidence Completion)

**Evidence Completion Targets:**
- Qualifications: 100%
- Employment: 100%
- Research: ≥90%
- Professional Development: ≥95%
- Awards: 100%
- Impact Metrics: ≥80%

**Repository Health KPIs:**
| KPI | Target |
|---|---|
| Claims Verified | 100% |
| Claims with Strong Evidence | >95% |
| Unsupported Claims | 0 |
| Conflicting Evidence | 0 unresolved |
| Placeholder Values | 0 |
| Broken Evidence Links | 0 |
| Generated Assets Current | 100% |

---

## 10. Definition of Done

A claim is only considered complete when all of the following are true:
1. Claim exists in the Claim Register.
2. Canonical source exists in the Canonical Profile.
3. Supporting evidence exists in the Evidence Library.
4. Evidence sufficiency is **Sufficient** or **Strong**.
5. Claim confidence is **High**.
6. No unresolved conflicts remain.
7. Public wording has been regenerated.
8. Validator passes.

---

## 11. Three-Layer Evidence Taxonomy

Every evidence record must define its `Evidence Purpose` as one of the following layers:

| Layer             | Proves                                 | Examples                                                                                                     |
| ----------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **L1 – Identity** | I held the position                    | Contract, appointment letter, experience letter, HR confirmation                                             |
| **L2 – Practice** | I performed these responsibilities     | Curriculum documents, timetables, moderation records, lesson observations, meeting minutes, training agendas |
| **L3 – Impact**   | My work produced demonstrable outcomes | Student achievement data, research findings, KPIs, commendations, performance reviews, programme outcomes    |

---

## 12. Evidence Gap Score

Every claim in the Claim Register receives a Gap Score:

*   **0**: Complete (Fully supported by required evidence layers)
*   **1**: Minor evidence missing
*   **2**: Needs supporting evidence (e.g., has L1 Identity, but needs L2/L3 for impact)
*   **3**: Weakly supported
*   **4**: Unsupported

---

## 13. Release Gate Checklist

Before publishing any public portfolio update (CV, LinkedIn, Website, etc.), the following checklist must be satisfied:

| Check | Required |
| --- | :---: |
| Validators pass | ✅ |
| No evidence conflicts | ✅ |
| No unsupported public claims | ✅ |
| Derived metrics regenerated | ✅ |
| Dashboard current | ✅ |
| Public assets regenerated | ✅ |
| LinkedIn synchronized | ✅ |
| Version number updated | ✅ |
| Release notes updated | ✅ |
| Portfolio build reproducible | ✅ |
