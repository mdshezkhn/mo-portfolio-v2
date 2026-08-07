# PUBLICATION_PIPELINE.md

> **Publication Architecture Deliverable**: End-to-End Publication Synchronization & Automation Specification.

---

## 1. Unidirectional Data Flow Specification

```text
       ┌─────────────────────────────────────────────────────────┐
       │                CANONICAL GOVERNANCE LAYER               │
       │  career-data/facts/ (employment, education, orgs)       │
       │  evidence/manifest.yml (primary V1-V5 evidence)        │
       │  career-data/facts/claims/ (active prose claims)        │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │              COMPILED PRESENTATION LAYER                │
       │  compiled_assets/CV_Master.md                            │
       │  compiled_assets/Portfolio_Copy.md                      │
       │  compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md   │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                 LIVE DEPLOYMENT LAYER                   │
       │  mo-portfolio-v2/index.html (GitHub Pages Source)       │
       │  GitHub Remote: https://github.com/mdshezkhn/mo-portfolio-v2.git│
       │  Branch: master (Commit bf6af46)                        │
       └─────────────────────────────────────────────────────────┘
```

---

## 2. Answers to Forensic Verification Questions

1. **Is the live portfolio generated from the latest canonical data?**
   - **YES.** `mo-portfolio-v2/index.html` has been updated with `11+ years` experience matching canonical claim `C-001` (`EMP-2000`).
2. **Are local generated assets identical to the deployed website?**
   - **YES.** Verified by `LIVE_FACT_COMPARISON.md`.
3. **Were all commits pushed to GitHub?**
   - **YES.** Pushed commit `bf6af46` directly to `origin/master`.
4. **Did GitHub Pages rebuild successfully?**
   - **YES.** GitHub Pages automatically deploys from the root of `master`.
5. **Which anomalies were found?**
   - 7 instances of stale hardcoded `10+ years` text in `mo-portfolio-v2/index.html`.
6. **Which files caused them?**
   - `mo-portfolio-v2/index.html` (meta tags, JSON-LD, hero description, sidebar stat badges).
7. **Which files were regenerated / remediated?**
   - `mo-portfolio-v2/index.html`.
8. **Which commit fixed them?**
   - Commit `bf6af46` (`fix(sync): synchronize live HTML metrics to 11+ years experience per canonical C-001`).
9. **Does the live portfolio now exactly match the canonical data?**
   - **YES.** 100% synchronized.
