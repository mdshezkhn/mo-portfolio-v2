# CONSISTENCY_POLICY.md (v1.0)

**Version:** 1.0
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Purpose:** The central compilation policy dictating what properties must match identically across the repository and what properties are permitted to vary.
**Severity Reference:** See `SEVERITY_POLICY.md`

## Repository Lifecycle States

All documents and data records must traverse the following deterministic lifecycle:
1. **DRAFT**: Work in progress. Fails all pipeline certifications.
2. **REVIEW**: Ready for audit. Validation engines evaluate against this policy.
3. **APPROVED**: Certified compliant. May be compiled into recruiter-facing outputs.
4. **LOCKED**: Frozen snapshot for active recruitment cycles. Requires formal un-locking protocol to edit.
5. **ARCHIVED**: Retained for historical record. Excluded from compilation pipelines.

---

## Object Validation Policies

Validation engines must assess the repository at the object level, verifying complete knowledge units rather than isolated fields.

### 1. Employment Record
Canonical Source: `career-data/facts/employment.yml`

| Property | Rule | Variation Allowed | Severity on Failure |
|---|---|---|---|
| **Employer Name** | Must exactly match canonical | No | CRITICAL |
| **Dates (Start/End)** | Must exactly match canonical | No | CRITICAL |
| **Role Title** | Must match `roles.yml` | Approved aliases only | CRITICAL |
| **Country/Location** | Must follow D-002 policy | No | HIGH |
| **Achievement Bullets**| Must derive from `claims.yml`| Yes (Tailoring allowed) | ALLOWED |
| **Metrics/Stats** | Must exactly match `CLAIM_REGISTER`| No | CRITICAL |

### 2. Qualification Record
Canonical Source: `career-data/facts/education.yml`

| Property | Rule | Variation Allowed | Severity on Failure |
|---|---|---|---|
| **Institution Name** | Must exactly match `institutions.yml` | No | CRITICAL |
| **Award/Degree Name**| Must exactly match canonical | No | CRITICAL |
| **Graduation Date** | Must exactly match canonical | No | CRITICAL |
| **Grades/Marks** | Must match canonical (if published)| No | MEDIUM |
| **Non-QTS Status** | Must be disclosed for PGCE | No | HIGH |

### 3. Claim Object
Canonical Source: `CLAIM_REGISTER.md`

| Property | Rule | Variation Allowed | Severity on Failure |
|---|---|---|---|
| **Claim Status** | Must be `APPROVED` for publication | No | CRITICAL |
| **Evidence Link** | Must reference valid `manifest.yml` ID| No | HIGH |
| **Confidence Level** | Must match canonical assessment | No | HIGH |
| **Wording** | Must retain semantic meaning | Yes (Contextual) | LOW |

### 4. Brand / Identity Object
Canonical Source: `MASTER_BRAND_SPECIFICATION.md`

| Property | Rule | Variation Allowed | Severity on Failure |
|---|---|---|---|
| **Headline** | Must reflect core brand identity | Yes (SEO/Recruiter) | LOW |
| **Summary** | Must hit core competencies | Yes (Specializations) | ALLOWED |
| **Languages** | Must list all approved languages | No (Completeness) | MEDIUM |

---

## Validation Engine Directives
All modular certifications (`01` through `05`) must import and enforce this policy document. Certifications must never interpret facts directly; they must interpret facts *through* this policy.
