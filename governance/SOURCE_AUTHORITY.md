# SOURCE_AUTHORITY.md (v2.0)

**Version:** 2.0 (Career OS v4.0)
**Status:** FROZEN
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-31

**Purpose:** Defines the authority boundaries for all data entering the Canonical Career Model and provides an explicit **Source Authority Matrix** to resolve any conflicts between documents deterministically.

## Source Authority Hierarchy

### Level 1 — Canonical Sources (May Create Facts)
Only these documents are authorised to create or modify objective facts in `career-data/facts/` (e.g., creating a new employment record, a new qualification, dates, or quantitative metrics).

1. `CANONICAL_PROFILE.md` (The human-curated master record)
2. `evidence/manifest.yml`
3. Credential Verification Register
4. Evidence Register
5. Primary evidence documents (certificates, transcripts, contracts, reference letters in `/private/`)

### Level 2 — Derived Sources (May Enrich, Not Create)
These documents track governance, provenance, and risk. They may add *metadata* (like confidence levels or publication flags) to existing facts, but they **must never** introduce a new employment record, qualification, date, or objective metric.

1. Claim Register
2. Decision Log
3. Risk Register
4. Evidence Gap Register
5. Technical Debt
6. Assumption Register

### Level 3 — Narrative Sources (Populate Narratives Only)
These documents represent subjective professional statements. They may only populate `career-data/narratives/`. They must never create facts.

1. Teaching Philosophy
2. Leadership Philosophy
3. Instructional Beliefs
4. Career Objective
5. LinkedIn About section
6. Recruiter Summary

---

## Source Authority Matrix

This matrix answers: *"Which source wins in the event of a contradiction?"* The validation engine must always defer to the higher-ranking document.

### Fact Precedence
`evidence/manifest.yml` → `career-data/facts/*.yml` → `CANONICAL_PROFILE.md` → Compiled Artifacts

### Governance Precedence
`MASTER_BRAND_SPECIFICATION.md` → `CONSISTENCY_POLICY.md` → `DECISION_LOG.md` → Output Assets

### Dispute Resolution Scenarios

| Dispute | Winning Source | Loser | Action |
|---|---|---|---|
| **Employment Dates** vary | `employment.yml` | `CV_Master.md` | Overwrite CV with YAML data |
| **Role Title** varies | `roles.yml` | `LinkedIn_Profile.md`| Overwrite LinkedIn with YAML data |
| **Qualification Name** varies | `education.yml` | `Portfolio_Copy.md` | Overwrite Portfolio with YAML data |
| **Claim Text** differs | `CLAIM_REGISTER.md` | `Achievement_Library.md`| Overwrite Achievement with Claim Register |
| **Publishing Pending Claim**| `CLAIM_REGISTER.md` | ANY Artifact | Block Build (CRITICAL) |
| **Headlines** differ | Allowed to vary | N/A | Pass (SEO/Recruiter variants allowed) |
