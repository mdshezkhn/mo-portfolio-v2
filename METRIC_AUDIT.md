# METRIC_AUDIT.md

> **Phase 5 Audit Deliverable**: Forensic verification of all computed recruiter metrics directly from governed YAML entities (`employment.yml`, `education.yml`, `organisations.yml`, `institutions.yml`, `evidence/manifest.yml`).

---

## 1. Metric Audit vs. Governed Entity Baseline

| Recruiter Metric | Mathematical Definition / Formula | Canonical Governed Value | Published Value (CV / LinkedIn / Portfolio) | Metric Verification Status | Discrepancy Analysis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Years of Professional Experience** | `Current_Year (2026/2027) - Start_Year (2014-01)` | **11+ Years** (2025/26) / **12+ Years** (2027) | `11+ years` / `12+ years` | **MATCH** | Dynamically computed from `EMP-2000` start date `2014-01`. |
| **School-Based Teaching Institutions** | `COUNT(DISTINCT org_id WHERE role == school_teaching)` | **4** (Scholars, Eton House, Aoxin, Zhejiang Univ.) | `4 teaching roles` / `4 school settings` | **MATCH** | Accurately excludes corporate L&D / EdTech employers (`ORG-1002`, `ORG-1003`). |
| **Total Employing Organisations** | `COUNT(DISTINCT organisation_id)` | **7** Legal Entities | `7 organisations` | **MATCH** | Matches `organisations.yml` (`ORG-1000` to `ORG-1006`). |
| **Physical In-Person Teaching Countries** | `COUNT(DISTINCT physical_country WHERE role == school_teaching)` | **2** (India, China) | `India and China` | **MATCH** | Directly extracted from `employment.yml` `physical_country` fields. |
| **International Operations Reach** | `COUNT(DISTINCT operational_regions)` | **3** (UK, Dubai, Malta) | `across UK, Dubai, and Malta` | **MATCH** | Properly attributed to `EMP-2005` (GEDU Global Education quality operations). |
| **Academic Degrees** | `COUNT(education_records)` | **4** (B.Sc., M.A., PGCE, B.Ed.) | `4 Degrees` | **MATCH** | Matches `education.yml` (`QUAL-3000` to `QUAL-3003`). |
| **Professional Certifications** | `COUNT(certifications)` | **2** (TESOL, TEFL) | `TESOL & TEFL` | **MATCH** | Matches `evidence/manifest.yml` (`E-2004`, `E-2005`). |
| **Canonical Active Prose Claims** | `COUNT(claims WHERE scope == public AND status == active)` | **15 Active Claims** | `15 Active Claims` | **MATCH** | Qualifications (`QUAL-3000`–`QUAL-3003`) separated as Entities. |

---

## 2. Publication Ratios & Evidence Coverage

* **Total Evidence Manifest Records (`evidence/manifest.yml`)**: 14 entries
* **Referenced by Active Claims / Entities**: 12 entries (`85.7%` evidence utilization)
* **Evidence Confidence Breakdown**:
  - `V5` (Primary Document Verified): 9 entries (`64.3%`)
  - `V4` (Corroborated Secondary): 1 entry (`7.1%`)
  - `V3` / `V1` (Plausible / Asserted): 4 entries (`28.6%`)

---

## 3. Metric Verification Decision

**Status:** **PASS**  
All computed recruiter metrics published in active presentation assets match the governed entity models with 0 mathematical or classification discrepancies.
