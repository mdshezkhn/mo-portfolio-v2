# LIVE_SITE_FACT_TABLE.md

> **Phase 3 Deliverable**: Line-by-line extraction of all recruiter-facing facts from `mo-portfolio-v2/index.html` and comparison against canonical YAML sources.

| Fact Category | Live HTML Assertion | Canonical Governed Value | Source YAML | Audit Status |
| :--- | :--- | :--- | :--- | :--- |
| **Years Experience** | `10+ years` | `11+ years` (2025/26) / `12+ years` (2027) | `employment.yml` (`EMP-2000`) | **NUMERIC DRIFT** |
| **Physical Countries** | `India and China` | `India and China` | `employment.yml` (`physical_country`) | **MATCH** |
| **Primary Degree** | `PGCE (University of Cumbria)` | `PGCE (University of Cumbria)` | `education.yml` (`QUAL-3002`) | **MATCH** |
| **School Settings** | `4 school settings` | `4 school settings` | `organisations.yml` (`ORG-1000`–`ORG-1005`) | **MATCH** |
| **Certifications** | `TESOL & TEFL` | `TESOL & TEFL` | `evidence/manifest.yml` (`E-2004`, `E-2005`) | **MATCH** |
| **Availability** | `August 2027` | `August 2027` | `claims/public.yml` (`C-023`) | **MATCH** |
| **Harris Safeguard** | `M.A. English — Harris University` | `Excluded from Premium Schools` | `education.yml` (`QUAL-3001`) | **MATCH** |