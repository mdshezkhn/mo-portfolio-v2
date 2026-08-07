# CHANGE_PROTOCOL.md (v1.0)

**Version:** 1.0
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Purpose:** Defines the deterministic workflow for processing any change to the repository to ensure published artifacts always reflect the canonical truth.

## The Change Lifecycle

Whenever new evidence is acquired or a claim is altered, the system must traverse these exact steps in order. A certification must never interpret the raw repository directly; it must evaluate the output of the compilation pipeline against the policy layer.

### Step 1: Evidence Acquisition
- Physical document added to `evidence/` directories.
- Entry added/updated in `evidence/manifest.yml` with assigned E-### ID.

### Step 2: Canonical Model Update
- Relevant canonical data (`employment.yml`, `education.yml`, etc.) is updated to match the evidence.
- Status moves from `DRAFT` to `REVIEW`.

### Step 3: Claim Recomputation
- `CLAIM_REGISTER.md` is updated.
- Claim links to the new/updated Evidence ID.
- Claim status is updated to `APPROVED` if supported.

### Step 4: Consistency & Propagation Validation
- `CONSISTENCY_POLICY.md` validates object integrity.
- `PROPAGATION_RULES.md` validates object presence in targets.

### Step 5: Build Compilation
- Generator scripts compile the target artifacts (`CV_*`, `LinkedIn_*`, `Portfolio_Copy.md`).
- Outputs are strictly derived from the canonical model and approved claims.

### Step 6: Certification Run
- The five modular certifications are executed against the compiled outputs:
  - `01_DATA_INTEGRITY.md`
  - `02_BRAND_CONSISTENCY.md`
  - `03_RECRUITER_READINESS.md`
  - `04_PIPELINE_HEALTH.md`
  - `05_EVIDENCE_SUFFICIENCY.md`

### Step 7: Release
- If all certifications PASS (no CRITICAL or HIGH issues), the repository state moves to `LOCKED`.

### Step 8: Version Tag
- The release is tagged with the new semantic version (e.g., v4.1).
