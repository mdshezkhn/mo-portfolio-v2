# DECISION_LOG.md

**Version:** 2.0 (Career OS v4.0)
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-25
**Updated:** 2026-07-30

**Purpose:** A historical record of all significant branding, credential, editorial, and architectural decisions. This document prevents revisiting settled debates, provides audit trail for recruiters or compliance checks, and ensures future automation can trace why any specific professional convention was chosen.

**Governance Rule:** Every decision recorded here is considered binding until explicitly superseded by a new entry. No downstream document may contradict a decision without first creating a superseding entry below.

---

## Decision Format

Each entry records:
- **ID** — Sequential identifier (D-###)
- **Date** — Date of decision
- **Topic** — What was decided
- **Decision** — The exact ruling
- **Alternatives Rejected** — What was considered and why it was not chosen
- **Rationale** — Why this decision was made
- **Evidence Reference** — Supporting evidence ID (if applicable)
- **Recruiter Risk** — Impact if this decision is questioned
- **Owner** — Who authorised this decision
- **Supersedes** — Previous decision this replaces (if any)

---

## D-001
**Date:** 2026-07-25
**Topic:** Years of Experience
**Decision:** Use **11+** years (e.g., "11+ years of international teaching experience")
**Alternatives Rejected:**
- "10+ years" — mathematically incorrect; career started January 2014
- "Over a decade" — imprecise; does not communicate proximity to 12 years
- "12 years" — not yet accurate; rounds up prematurely
**Rationale:** Professional teaching began January 2014 at Scholars Academy. Employment was continuous to present. The calculation yields 11+ years as of 2026. The "+" qualifier is honest and standard professional convention.
**Evidence Reference:** E-3003 (Scholars Academy employment verification)
**Recruiter Risk:** Low — mathematically defensible; verified start date
**Owner:** Mohammed Shehzad Khan
**Supersedes:** Draft wording in BRAND_SPECIFICATION.md v1.0 (which wavered between 10+ and 11+)

---

## D-002
**Date:** 2026-07-25
**Topic:** Countries of Employment
**Decision:** List **India and China** as countries of employment. Do not list UK, UAE, or Malta as countries of employment.
**Alternatives Rejected:**
- "India, China, UK, UAE, Malta" — GEDU was India-registered; UK/UAE/Malta were client/market locations, not employment jurisdictions
- "Multiple countries" — vague; does not communicate the Asian international school context
**Rationale:** Counting countries based on client or market location rather than physical employment jurisdiction is not a defensible professional convention. GEDU Global Education is India-based with international remit. Employment contracts were Indian-jurisdiction. The correct canonical record is India and China.
**Evidence Reference:** E-3001 (GEDU employment verification)
**Recruiter Risk:** Low — accurately represents jurisdictional employment; international remit noted in role description
**Owner:** Mohammed Shehzad Khan
**Supersedes:** Draft wording in BRAND_SPECIFICATION.md v1.0

---

## D-003
**Date:** 2026-07-30
**Topic:** Harris University — Public CV Listing Policy
**Decision:** List the degree factually in public CVs with no qualifier appended. Apply per-document publication flags in education.yml. Internal records carry `institution_recognition_status: REQUIRES_EXTERNAL_VERIFICATION`.
**Alternatives Rejected:**
- "Verification pending" appended to CV entry — recruiter interpretation problem: reads as doubt about degree existence, not institution recognition status. These are entirely different messages.
- Hold entirely from all public assets — premature; degree existence confirmed by owner; omission introduces a different risk (unexplained study gap)
- "Attended Harris University" — misleading; degree was awarded
**Rationale:** The existence of the degree and the recognition status of the institution are recorded separately. The public CV lists what is factually true (degree awarded). The institution's recognition status is an internal governance matter tracked in Credential_Verification_Register.md. A separate explicit decision (D-003a if needed) will address any publication restriction once external verification is obtained.
**Evidence Reference:** E-0008 (pending — Harris University records)
**Recruiter Risk:** Medium — institution recognition is unverified; HIGH for premium school contexts (publication flag: `premium_schools: false`)
**Owner:** Mohammed Shehzad Khan
**Supersedes:** v2.0 plan wording "Verification pending"

---

## D-004
**Date:** 2026-07-30
**Topic:** PGCE Qualification Descriptor
**Decision:** Describe as **"Postgraduate Certificate in Education (PGCE, non-QTS)"** in all professional documents. Non-QTS status is stated explicitly.
**Alternatives Rejected:**
- "PGCE" alone — omits a material fact that recruiters in England and some international markets require
- "PGCE (International)" — inaccurate; University of Cumbria does not brand it this way
- Omitting non-QTS status — creates recruiter trust damage when discovered at interview; transparency is the safer position
**Rationale:** International recruiters generally accept PGCE without QTS. UK domestic recruiters may flag it. Stating it proactively demonstrates professional integrity and avoids the far worse scenario of a recruiter discovering the fact during due diligence.
**Evidence Reference:** E-2001 (PGCE certificate — University of Cumbria)
**Recruiter Risk:** Low — disclosed proactively; mitigated by interview preparation entry in INTERVIEW_DEFENSIBILITY_REGISTER.md
**Owner:** Mohammed Shehzad Khan

---

## D-005
**Date:** 2026-07-30
**Topic:** School Count vs. Role Count for Recruiter-Facing Metric
**Decision:** Use **"4 schools"** as the primary institutional count metric, not "7 roles."
**Alternatives Rejected:**
- "7 roles" — correct internally but misleading to a Head of Primary who equates roles with schools
- "7 positions" — same problem
- "5 employers" — includes WhiteHat Jr which is online-only; conflates classroom and EdTech contexts
**Rationale:** Recruiters hiring for international school positions evaluate credibility in terms of institutional affiliations, not role count. "4 schools" is more immediately legible. Internal records retain all 7 role entries.
**Evidence Reference:** employment.yml (all entries)
**Recruiter Risk:** Low
**Owner:** Mohammed Shehzad Khan

---

## D-006
**Date:** 2026-07-30
**Topic:** Portfolio Display Title
**Decision:** Use **"International Primary Educator"** as the portfolio display title.
**Alternatives Rejected:**
- "EAL Teacher" — too narrow; does not represent the full cross-curricular and leadership scope
- "Primary Teacher" — understates international and specialist context
- "Teacher Trainer" — accurate for one phase but not the dominant profile
**Rationale:** "International Primary Educator" is broad enough to cover all 7 roles, signals the international context, and does not over-claim in any single specialty. Supported by the full career chronology.
**Evidence Reference:** identity.yml
**Recruiter Risk:** Low
**Owner:** Mohammed Shehzad Khan

---

## D-007
**Date:** 2026-07-30
**Topic:** Canonical Branch for GitHub Pages Deployment
**Decision:** Canonical production branch is **`main`**. `deploy.yml` updated to listen on `main`.
**Alternatives Rejected:**
- Rename `main` to `master` — unnecessary disruption to current working branch
- Leave `master` as trigger — CI/CD has never fired due to this mismatch; must be corrected
**Rationale:** Current working branch is `main`. GitHub Actions `deploy.yml` was set to trigger on `master`, creating a mismatch that prevented all automated deployments. Correcting the trigger is the least disruptive fix.
**Evidence Reference:** N/A
**Recruiter Risk:** N/A (internal infrastructure decision)
**Owner:** Mohammed Shehzad Khan

---

## D-008
**Date:** 2026-07-30
**Topic:** Harris University — Publication Flags (Confirmed)
**Decision:** `public_cv: true`, `linkedin: true`, `premium_schools: false (configurable)`, `verification_status: requires_external_review`.
**Rationale:** Release manager confirmed: list the degree factually. No accreditation claims. No disclaimers. No editorial comments on public documents. Internal records carry `requires_external_review`. Premium school contexts excluded until G-006 is resolved, as that flag is configurable without touching the underlying fact.
**Alternatives Rejected:**
- Remove from public CV — premature; credential exists and is owner-confirmed
- Add "verification pending" qualifier — rejected in D-003; reiterated here
**Evidence Reference:** E-0008 (pending)
**Recruiter Risk:** Medium (general); High (premium contexts — mitigated by `premium_schools: false` flag)
**Owner:** Mohammed Shehzad Khan (release manager approval)
**Supersedes:** Partial treatment in D-003

---

## D-009
**Date:** 2026-07-30
**Topic:** B.Ed. Publication Policy
**Decision:** B.Ed. publication status is `EVIDENCE_COLLECTION_REQUIRED`, not `BLOCKED_FROM_PUBLICATION`. Publication is ALLOWED.
**Rationale:** There is a material distinction between *evidence not yet collected into the repository* and *a qualification that should not appear publicly*. The B.Ed. exists and is owner-confirmed. The repository simply does not yet contain the physical document. The correct action is evidence collection, not publication suppression. `BLOCKED_FROM_PUBLICATION` is reserved for qualifications where existence itself is in doubt or where a positive decision has been made to exclude.
**Alternatives Rejected:**
- `BLOCKED_FROM_PUBLICATION` — incorrect status; implies the qualification is in question, which it is not
**Evidence Reference:** E-0009 (Evidence Collection Required)
**Recruiter Risk:** Low — qualification is real; evidence collection is an internal process
**Owner:** Mohammed Shehzad Khan (release manager approval)

---

## D-010
**Date:** 2026-07-30
**Topic:** Career OS profile_version Starting Number
**Decision:** Career OS `profile_version` initialises at **`1.0.0`**.
**Rationale:** This is version 1 of the Career OS — a new product. Prior portfolio versions (v1, v2, v3) are separate products that have been archived. The Career OS does not inherit their version history. Starting at 1.0.0 correctly reflects that this is a new governed publishing system, not a continuation of an old portfolio project.
**Alternatives Rejected:**
- `2.0.0` — implies the Career OS continues from a prior version, which is architecturally incorrect
**Evidence Reference:** N/A
**Recruiter Risk:** N/A (internal versioning decision)
**Owner:** Mohammed Shehzad Khan (release manager approval)

---

## D-011
**Date:** 2026-07-30
**Topic:** Repository Freeze Policy Scope
**Decision:** The Repository Freeze Policy (active from end of Week 1) blocks **unapproved public-facing content changes**, not all changes.
**Rationale:** During Week 2 (data population), factual corrections will be discovered — incorrect employment dates, inconsistent school names, missing evidence IDs, broken timelines. These are corrections, not branding changes. Freezing them would be counterproductive. The policy must distinguish between:
- **Permitted during freeze:** Factual corrections to YAML data, evidence ID additions, confidence level adjustments, schema corrections, internal governance updates
- **Requires approval during freeze:** New public-facing claims, branding changes, narrative rewording, metric changes, new credentials added to public outputs
**Evidence Reference:** N/A
**Recruiter Risk:** N/A (internal governance decision)
**Owner:** Mohammed Shehzad Khan (release manager approval)

---

## D-012
**Date:** 2026-07-30
**Topic:** B.Ed. Publication Flags — Explicit Confirmation
**Decision:** B.Ed. (University of Kashmir) publication flags: `public_cv: true`, `linkedin: true`. Evidence manifest entry E-0009 set to `confidence: supported` and `publication_status: EVIDENCE_COLLECTION_REQUIRED`.
**Rationale:** Final architecture review confirmed: the qualification is genuine and owner-confirmed. Adding explicit publication flags (`public_cv: true`, `linkedin: true`) removes any ambiguity about publication intent. The `confidence` level is raised from `plausible` to `supported` because the owner has confirmed the qualification exists. `EVIDENCE_COLLECTION_REQUIRED` remains the operational status until the physical document is added to `evidence/credentials/`.
**Policy Trigger:** If at any point the owner cannot produce documentary evidence, this decision must be revisited and a new entry (D-012a) must record the changed policy.
**Evidence Reference:** E-0009
**Recruiter Risk:** Low — qualification is real; evidence collection is an internal process
**Owner:** Mohammed Shehzad Khan (final architecture review)
**Supersedes:** D-009 (strengthens rather than reverses)

---

## D-013
**Date:** 2026-07-30
**Topic:** Application Strategy Default
**Decision:** **No default application strategy.** Every application requires an explicit strategy selection (`--strategy A|B|C`) at generation time.
**Rationale:** An implicit default removes the deliberate thought required to match strategy to context. Each application to an international school should be a considered decision about which evidence to lead with, not an automated output. If a default must be set for testing purposes only, Strategy B (Mid-Tier) is acceptable, but this must never reach production as a silent default.
**Alternatives Rejected:**
- Strategy B as default — convenient but reduces intentionality; application quality depends on conscious strategy selection
**Evidence Reference:** N/A
**Recruiter Risk:** N/A (internal tooling decision)
**Owner:** Mohammed Shehzad Khan (final architecture review)

---

## D-014
**Date:** 2026-07-30
**Topic:** First Recruiter Evidence Pack Context
**Decision:** `BRITISH_CURRICULUM` is the first context pack to be built in Week 3.
**Rationale:** British curriculum international schools represent the largest segment of the target market across China, the Middle East, Southeast Asia, and Brunei. A British-curriculum baseline provides the greatest reuse and can be adapted for other contexts more easily than the reverse. Assumption A-002 tracks whether this proves correct.
**Evidence Reference:** N/A
**Recruiter Risk:** N/A (internal build sequence decision)
**Owner:** Mohammed Shehzad Khan (final architecture review)

---

## D-015
**Date:** 2026-07-30
**Topic:** Python Environment Verification Policy
**Decision:** Python environment (version and required packages) must be verified before any script is executed. Never assume package availability.
**Required packages:** `pyyaml`, `jsonschema`, `pytest`, `pathlib` (stdlib)
**Verification command:** `python --version && pip show pyyaml jsonschema pytest`
**Rationale:** Missing packages cause silent failures or misleading errors. A 30-second environment check prevents hours of debugging caused by missing dependencies.
**Evidence Reference:** N/A
**Recruiter Risk:** N/A (internal tooling decision)
**Owner:** Claude Code

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-25 | Initial — D-001, D-002 |
| 2.0 | 2026-07-30 | Career OS v4.0 — D-003 through D-007; expanded format |
| 3.0 | 2026-07-30 | Week 1 amendments — D-008 through D-011 |
| 4.0 | 2026-07-30 | Final architecture review — D-012 through D-015; architecture APPROVED |
