# LIVE_FACT_COMPARISON.md

> **Phase 8 & 9 Deliverable**: Post-Deployment Verification comparing Live Website against Canonical Data.

---

## Post-Deployment Fact Comparison Matrix

| Recruiter Fact Category | Deployed Live Web Fact (`index.html`) | Canonical Governed Fact (`career-data/facts/`) | Audit Trace ID | Final Verification Status |
| :--- | :--- | :--- | :--- | :---: |
| **Years Experience** | `11+ years` | `11+ years` (`EMP-2000` start `2014-01`) | `FACT-C-001` | **MATCH** |
| **Physical Countries** | `India and China` | `India and China` (`physical_country`) | `FACT-C-002` | **MATCH** |
| **Primary Teaching Degrees** | `PGCE (University of Cumbria)`, `B.Ed` | `QUAL-3002`, `QUAL-3003` | `FACT-QUAL-3002` | **MATCH** |
| **Primary School Settings** | `4 school settings` | `ORG-1000`, `ORG-1001`, `ORG-1004`, `ORG-1005` | `FACT-MET-002` | **MATCH** |
| **Professional Certifications**| `TESOL & TEFL` | `E-2004`, `E-2005` | `FACT-C-005` | **MATCH** |
| **Target Availability** | `August 2027` | `August 2027` (`claims/public.yml`) | `FACT-C-023` | **MATCH** |
| **Harris University Safeguard** | Restricted from Premium Packs | `confidence: V1`, `premium_schools: false` | `FACT-QUAL-3001` | **MATCH** |

---

## Live Verification Verdict

```text
Live Website (https://mdshezkhn.github.io/mo-portfolio-v2/)
       ↓
Generated Assets (compiled_assets/CV_Master.md, Portfolio_Copy.md)
       ↓
Canonical Claims (career-data/facts/claims/public.yml)
       ↓
Evidence Manifest (evidence/manifest.yml)

VERDICT: 100% FACTUALLY IDENTICAL & SYNCHRONIZED
```
