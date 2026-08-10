# Validation Cycle 1: Blind Persona Reviews & Defect Log

## Persona Feedback Summaries

### 1. Head of Primary
"The curriculum design claim is strong, but there is zero classroom impact or safeguarding mentioned. I see 'ESL Educator' and 'Primary Educator' with no highlights or achievements under them. Why is there a 2-year gap with no details under Scholars Academy? The PGCE is great, but I need to see classroom practice details."

### 2. Principal
"Strong leadership metrics (100+ educators) and QA initiatives show good strategic potential. However, the 'Educational Leader' title is too broad. The career history lacks clear progression because many early roles have no highlights. I would interview for a middle-leadership role, but the gaps in early career achievements give me pause."

### 3. HR Recruiter
"Clean chronology. The 'Unknown Year' for B.Ed was removed which is good, but missing a graduation year can trigger a compliance question during screening. I also notice the Executive Summary repeats exactly word-for-word the highlight under Zhejiang University, which looks like a typo or copy-paste error. Eligibility-wise, the PGCE is noted as non-QTS, which is clear and helpful."

### 4. Curriculum Director
"The curriculum design claim is exactly what I'm looking for, but there's no evidence presented for *what* the EAL integration actually achieved. Did student outcomes improve? I like the mentoring stat (100+ educators), but I need more substance on the actual pedagogical frameworks used."

---

## Defect & Opportunity Classification (Root Cause)

| ID | Layer | Category | Severity | Description | Fix Action |
|---|---|---|---|---|---|
| DEF-001 | B (Claim) | Presentation | Medium | The Executive Summary claim (CLAIM-1000) is repeating verbatim as a role highlight under Zhejiang University, indicating it is incorrectly linked via `SUPPORTED_BY` to `EMP-2001` without being a specific achievement. | Relink CLAIM-1000 to a global profile node rather than a specific employment, or remove it from the specific employment edge. |
| DEF-002 | A (Canonical) | Data Gap | High | Scholars Academy (2014-2016), Eton House (2017-2018), and Aoxin (2024-Present) have zero claims or highlights. | Add verified claims for these roles (if evidence exists) or log as an Evidence Opportunity. |
| DEF-003 | A (Canonical) | Data Gap | Medium | B.Ed. from University of Kashmir lacks a completion year, which triggers HR compliance flags. | Add the verified year to `education.yml` if known. |
| DEF-004 | B (Claim) | Claim Quality | Low | Curriculum design claim lacks quantified student outcomes (Curriculum Director feedback). | Needs stronger evidence or phrasing in `claims.yml`. |

## Evidence Opportunity Log

| Evidence | Status |
|---|---|
| E-3003 (Scholars Academy reference letter) | Not surfaced. No claims generated for this evidence yet. |
| E-3004 (Eton House Certificate) | Not surfaced. No claims generated for this role yet. |
| E-2001 (PGCE Transcripts) | Only appears in Education block; no pedagogical claims leverage this recent study. |
