# SCHEMA.md

**Purpose:** This document freezes the structural conventions of the Professional Brand Governance Framework. To ensure long-term auditability and prevent fragmentation, these schemas must not be altered once evidence and claims have been indexed against them.

**Status:** FROZEN
**Version:** SCHEMA-1.0
**Owner:** Mohammed Shehzad Khan
**Last Reviewed:** 2026-07-25

---

## 1. Identifier Formats

### Evidence IDs
- **Format:** `E-XXXX` (four-digit, zero-padded)
- **Example:** `E-0012`
- **Rule:** Assigned sequentially upon receipt in `/private/`. Never reused or deleted. If a document is updated, mark the old ID as `Superseded` and issue a new ID.

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

## 4. Folder and Naming Conventions

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
