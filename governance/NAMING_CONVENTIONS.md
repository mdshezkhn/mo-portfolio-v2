# NAMING_CONVENTIONS.md

**Version:** 1.0 (Career OS v4.0)
**Status:** FROZEN
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-31

**Purpose:** Freezes the exact spelling and formatting of canonical names used throughout the Career OS. A canonical name must exist exactly once in `career-data/`. Any variations or abbreviations belong in the `aliases` metadata field, never in the primary display field.

## Organisations & Institutions

| Canonical Name | Aliases / Incorrect Forms to Avoid |
|---|---|
| WhiteHat Jr | WhiteHat Jr., White Hat Junior, BYJU'S Future School |
| GEDU Global Education | GEDU, Global Education |
| Aoxin International School | Aoxin, Aoxin School |
| Eton House Kindergarten | EtonHouse, Eton House |
| Scholars Academy | Scholars' Academy, Scholar Academy |
| Zhejiang University | ZJU |
| Helen China TEFL Network | Helen China, Helen TEFL |
| University of Cumbria | Cumbria University |
| University of Kashmir | Kashmir University |
| Harris University | Harris |
| University of Mumbai | Mumbai University |

## Qualifications & Certifications

| Canonical Name | Aliases / Incorrect Forms to Avoid |
|---|---|
| Postgraduate Certificate in Education | PGCE |
| Bachelor of Education | B.Ed., BEd |
| Bachelor of Science, Physics | B.Sc., BSc |
| Master of Arts, English Language and Literature | M.A., MA |

## Identifiers (Stable IDs)

All IDs in the system follow a strictly typed, monotonically increasing format. **Once assigned, an ID is never renumbered.** If an item is deleted, its ID is retired and never reused.

*   **PERSON-XXX**: Individuals (e.g., references, self)
*   **EMP-XXX**: Employment records
*   **EDU-XXX**: Educational qualifications
*   **CERT-XXX**: Certifications
*   **INST-XXX**: Academic institutions
*   **ORG-XXX**: Employers / Companies
*   **ROLE-XXX**: Job titles / Roles
*   **CLAIM-XXX**: Verified public claims

*Example:* `EMP-001`, `EMP-002`. If `EMP-002` is removed, the next employment is `EMP-003`.

## File Metadata

Every YAML file in `career-data/` and `schemas/` must begin with standard metadata:

```yaml
schema_version: 1.0
profile_version: 1.0.0
last_reviewed: 2026-07-31
owner: Mohammed Shehzad Khan
status: canonical
```
