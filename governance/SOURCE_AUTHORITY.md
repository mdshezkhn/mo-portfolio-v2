# SOURCE_AUTHORITY.md

**Version:** 1.0 (Career OS v4.0)
**Status:** FROZEN
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-31

**Purpose:** Defines the authority boundaries for all data entering the Canonical Career Model (`career-data/`). This prevents derived insights or subjective commentary in governance documents from "leaking" back into fact records.

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

*Example violation to avoid:* The Decision Log states "Candidate has extensive leadership experience." This must NOT be copied into `facts/skills.yml`. 

### Level 3 — Narrative Sources (Populate Narratives Only)
These documents represent subjective professional statements. They may only populate `career-data/narratives/`. They must never create facts.

1. Teaching Philosophy
2. Leadership Philosophy
3. Instructional Beliefs
4. Career Objective
5. LinkedIn About section
6. Recruiter Summary

*Rule:* Narrative statements hold a confidence level of `human_assertion`. They are valuable, but they are not facts.
