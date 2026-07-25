# EVIDENCE_INDEX.md

**Layer:** Evidence Management (Layer 2 of 6)
**Purpose:** The immutable index of every primary document that enters the evidence pipeline. Each artifact receives a stable Evidence ID (E-XXXX) that is referenced by the Evidence Register, the Claim Register, and the Compliance Report. This file is the bridge between physical documents in `/private/` and the governance system above it.

**Relationship to other layers:**
```
PRIMARY SOURCES in /private/
  (Employment Letters, Certificates, Contracts, Research Papers…)
          │
          ▼
EVIDENCE_LIBRARY/EVIDENCE_INDEX.md   ← YOU ARE HERE
  (Evidence ID · Metadata · Verification Status)
          │
          ▼
Evidence_Register.md  (lifecycle: Pending → Received → Reviewed → Verified → Archived)
          │
          ▼
MASTER_BRAND_SPECIFICATION.md  (governance, evidence levels, traceability matrix)
          │
          ▼
CLAIM_REGISTER.md  (canonical wording, Evidence IDs per claim, asset maps)
          │
          ▼
ASSET_COMPLIANCE_REPORT.md  (validates every public asset against approved claims)
          │
          ▼
PUBLIC ASSETS  (CV, LinkedIn, Portfolio, Cover Letters, Interview Prep)
```

**Immutability rule:** Once an Evidence ID is assigned, it is permanent. If a document is superseded (e.g. a corrected employment letter replaces an earlier one), the old entry is marked `Superseded` and the new document receives a new ID. Evidence IDs are never reused or deleted.

**Version:** ER-1.0
**Status:** Active — awaiting first primary document
**Owner:** Mohammed Shehzad Khan
**Last Reviewed:** 2026-07-25

---

## Evidence ID Schema

- Format: `E-XXXX` (four-digit, zero-padded, sequential from E-0001)
- Assignment: IDs are assigned in the order documents are received and indexed, not in order of importance
- Cross-reference: Each ID appears in the Claim Register under "Supported by Evidence IDs" for every claim it supports

---

## Metadata Schema (per entry)

| Field | Description |
|-------|-------------|
| **Evidence ID** | Stable unique identifier (E-XXXX) |
| **Document Type** | Employment Letter / Employment Contract / Degree Certificate / PGCE Certificate / TESOL Certificate / TEFL Certificate / Transcript / Research Paper / Curriculum Sample / Lesson Observation / Testimonial / Performance Review / Student Work / Photograph / Other |
| **Issuer / Source** | Name of the organisation or person who issued the document |
| **Subject / Role** | What role, qualification, or event the document relates to |
| **Date of Document** | Date on the document itself (not the date received) |
| **Date Received** | Date the document was added to this index |
| **File Path** | Relative path within `/private/` (e.g. `Contracts/GEDU_Employment_Letter_2022.pdf`) |
| **Verification Status** | `Pending Review` / `Reviewed` / `Verified` / `Superseded` |
| **Claims Supported** | Comma-separated list of Claim IDs this document evidences (e.g. `C-004, C-007`) |
| **Notes** | Any relevant context, caveats, or follow-up actions |

---

## Index

> **Status as of 2026-07-25: No primary documents have been received.**
> `/private/Contracts/` is empty. `/private/Original Certificates/` is empty.
> The index below is ready to receive entries. Add a new row each time a document arrives in `/private/`.

| Evidence ID | Document Type | Issuer / Source | Subject / Role | Date of Document | Date Received | File Path | Verification Status | Claims Supported | Notes |
|-------------|---------------|-----------------|----------------|-----------------|---------------|-----------|---------------------|-----------------|-------|
| — | — | — | — | — | — | — | — | — | No entries yet. First entry will be E-0001. |

---

## Priority Queue

*Documents in the Priority Queue are expected but not yet received. This is a forward-looking reference — it does not assign Evidence IDs (IDs are only assigned when a document is in hand).*

| Expected Document | Expected ID (provisional) | Unblocks | Priority | Status |
|-------------------|--------------------------|----------|----------|--------|
| Scholars Academy employment letter | E-0001 (provisional) | C-001 (years), C-024 | P0 | Not received |
| GEDU employment letter | E-0002 (provisional) | C-002 (countries), C-017, C-018 | P0 | Not received |
| Aoxin International School employment letter (2018–2020) | E-0003 (provisional) | C-009, C-013 | P0 | Not received |
| Aoxin International School employment letter (2024–present) | E-0004 (provisional) | C-009, C-023 | P0 | Not received |
| WhiteHat Jr (BYJU'S) employment letter | E-0005 (provisional) | C-014, C-015 or C-016 (scope resolution) | P0 | Not received |
| Eton House Kindergarten employment letter | E-0006 (provisional) | C-010, C-019 | P0 | Not received |
| Zhejiang University / Helen China TEFL Network employment letter | E-0007 (provisional) | C-009 | P0 | Not received |
| PGCE certificate / University of Cumbria transcript | E-0008 (provisional) | C-004, C-007 | P0 | Not received |
| B.Ed. degree certificate | E-0009 (provisional) | C-003 | P1 | Not received |
| B.Sc. Physics degree certificate | E-0010 (provisional) | C-008 | P1 | Not received |
| TESOL certificate | E-0011 (provisional) | C-005 | P1 | Not received |
| TEFL certificate | E-0012 (provisional) | C-006 | P1 | Not received |
| University of Cumbria research paper / submission | E-0013 (provisional) | C-007 | P1 | Not received |
| WhiteHat Jr manager confirmation (scope: 200 vs 1,000) | E-0014 (provisional) | C-015 or C-016 resolution | P0 | Not received |
| GEDU manager confirmation (trainer team size) | E-0015 (provisional) | C-018 | P0 | Not received |

> **Provisional IDs are illustrative only.** Actual IDs are assigned in order of receipt, not priority. E-0001 will be whichever document arrives first.

---

## How to Add a New Entry

When a primary document arrives in `/private/`:

1. Move or save the document to the appropriate `/private/` subfolder.
2. Add a new row to the Index table above with the next sequential Evidence ID.
3. Fill all metadata fields.
4. Set Verification Status to `Pending Review`.
5. Update the Evidence Register entry for the corresponding claim(s).
6. Update the Claim Register — add the new Evidence ID to the "Supported by Evidence IDs" field for each claim the document supports.
7. Follow the full Regeneration SOP in `Evidence_Acquisition_Plan.md`.

---

## Change Log

| Date | Version | Change | Notes |
|------|---------|--------|-------|
| 2026-07-25 | ER-1.0 | Initial index created | No primary documents yet received. Schema and priority queue established. |
