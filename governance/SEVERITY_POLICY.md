# SEVERITY_POLICY.md (v1.0)

**Version:** 1.0
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Purpose:** Defines standard severity levels for all validation and certification tools.

All audits, certifications, and pipeline validation engines MUST use these severity definitions.

## Severity Definitions

| Severity | Definition | Pipeline Action | Example Issue |
|---|---|---|---|
| **CRITICAL** | Materially damages recruiter credibility or breaks downstream automation. Involves facts, dates, institutions, or ID collisions. | **BLOCKS RELEASE** | Wrong employment date; mismatched employer name; incorrect qualification; ID conflict. |
| **HIGH** | Likely to cause recruiter concern or require interview clarification. Involves title inflation or missing key evidence. | **BLOCKS RELEASE** | Title inflation ("Director" instead of "Lead"); missing P0 evidence for published claim. |
| **MEDIUM** | Noticeable inconsistency but unlikely to ruin an application. Should be corrected before next major release cycle. | **WARNING** | Missing language in one document; out-of-order chronology; duplicate bullet points. |
| **LOW** | Minor wording variations that do not change semantic meaning. Expected for intentional specialization. | **INFO / ALLOWED** | Different headlines for SEO vs. CV; different professional summaries tailored to role. |
| **ALLOWED** | Expected variation permitted by policy. | **PASS** | Tailored teaching bullets for STEM vs. EAL context. |

## Application Rules
* Validation engines must halt the `CHANGE_PROTOCOL` pipeline if any CRITICAL or HIGH issues are detected.
* MEDIUM issues generate warnings but do not block the build.
* LOW issues are logged for potential manual review.
