# Repository-Wide Claim Audit Engine

This plan outlines the creation of an automated script to safeguard the repository against narrative drift and unverified claims. Based on user feedback, the architecture is **claim-centric, deterministic, and strictly governed.**

## Goal
To implement a "self-policing" governance step by building an automated, repository-wide claim validation script. The script will detect high-risk triggers across all presentation assets and deterministically validate them against a structured claim register using approved variants.

## Proposed Changes

### 1. Single Source of Truth
`claims.yml` will become the sole authoritative source for all claims. `CLAIM_REGISTER.md` will be deprecated as an editable file and converted into a compiled presentation asset (generated from `claims.yml`).

### 2. Expanded Claim Schema
`career-data/facts/claims.yml` will use an expanded schema to support rich governance:
* `id`
* `status`, `version`, `introduced`, `deprecated`, `superseded_by`
* `risk`
* `owner`
* `type` (e.g., leadership, identity, metrics)
* `canonical`
* `subject` & `modifier`
* `evidence`
* `allowed_variants`
* `presentation_assets`

### 3. Governance Data
#### [NEW] `governance/risk_triggers.yml`
A dictionary of high-risk triggers categorized by type (`identity`, `causality`, `performance`, `leadership`, `experience`) to identify which sentences require inspection.

### 4. The Engine (Deterministic Validation)
#### [NEW] `scripts/audit_claims.py`
A intentionally "dumb" and deterministic validator.
**Pipeline:**
1. **Trigger Detection:** Scan presentation assets for risk triggers.
2. **Normalization:** Normalize the flagged sentence (strip punctuation, whitespace).
3. **Variant Matching:** Compare the normalized sentence against the `allowed_variants` in `claims.yml`.
4. **Outcome:** PASS or Review Required.

**Reporting Output:**
1. **Explicit Unknown Claim Reporting:** Outputs the File, Sentence, Nearest Canonical Claim, Distance, and Recommendation for immediate remediation.
2. **Claim Coverage Report:** Tracks Canonical claims, Claims actually used, and Unused canonical claims (portfolio optimization opportunities).
3. **Orphan Claim Report:** Tracks Presentation claims, Canonical matches, and Orphan claims.
4. **Severity by Category:** Errors grouped by `IDENTITY`, `Leadership`, `Evidence`, etc., alongside standard Risk Levels (CRITICAL, HIGH, MEDIUM, LOW).
5. **Repository Health Metrics Dashboard.**

### 5. CI/CD Integration
#### [MODIFY] `career.bat` / `career.ps1`
Integrate the validator to run **before** any build compilation. Compilation will fail if governance fails.

## Verification Plan
* Run `scripts/audit_claims.py` against the repository to establish baseline compliance.
* Verify `CLAIM_REGISTER.md` is successfully generated from `claims.yml`.
* Ensure CI/CD scripts properly halt execution on governance failures.
