# ASSUMPTION_REGISTER.md

**Version:** 1.0 (Career OS v4.0)
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-30

**Purpose:** Tracks engineering and professional assumptions that underpin decisions made in the Career OS. Distinct from:
- `RISK_REGISTER.md` — risks that require active monitoring and mitigation
- `DECISION_LOG.md` — decisions that have been made with known rationale
- `EVIDENCE_GAP_REGISTER.md` — missing professional documents

Assumptions are propositions treated as true for planning purposes but **not yet validated by evidence or outcomes**. Left untracked, assumptions become invisible "facts" over time. This register forces periodic validation so that the Career OS remains grounded in reality as application data accumulates.

**Governance Rule:** Every assumption must be assigned a validation method and a review date. When validated, the entry is marked `VALIDATED` with the supporting evidence. When disproved, the entry is marked `DISPROVED` and any decisions or strategies built on it must be reviewed.

---

## Status Key

| Status | Meaning |
|---|---|
| `OPEN` | Assumption is active and untested |
| `VALIDATED` | Assumption confirmed by evidence or outcomes |
| `DISPROVED` | Assumption shown to be incorrect; dependent decisions must be reviewed |
| `SUPERSEDED` | Assumption no longer relevant; context has changed |

---

## Assumption Register

### A-001
**Status:** OPEN
**Category:** Recruiter Behaviour
**Assumption:** Recruiters in the international school market value a portfolio-based evidence presentation (structured CV + supporting documents) over a single CV document.
**Basis for assumption:** Anecdotal — international school hiring processes in Asia and the Middle East increasingly request portfolios alongside CVs; premium schools often request teaching videos.
**Impact if wrong:** The Recruiter Evidence Pack Generator (seven contexts) represents significant build effort. If recruiters ignore evidence packs and only read the CV, that effort is misallocated.
**Validation Method:** Track application outcomes — specifically, whether evidence packs are acknowledged, requested at interview, or ignored. Gather feedback from at least 5 applications per strategy.
**Owner:** Mohammed Shehzad Khan
**Review Date:** 2027-03-01 (after first application cohort)

---

### A-002
**Status:** OPEN
**Category:** Market Strategy
**Assumption:** The `BRITISH_CURRICULUM` recruiter pack will have the widest applicability across target markets (China, Middle East, Southeast Asia, Brunei).
**Basis for assumption:** British curriculum international schools represent the largest single segment of the international school market in Asia and the Gulf. A British-curriculum baseline pack can be adapted for other contexts more easily than the reverse.
**Impact if wrong:** If `CHINESE_BILINGUAL` or `IB_PYP` contexts prove more relevant to the actual job market in 2027, the BRITISH_CURRICULUM pack will be underused and a different context should be built first.
**Validation Method:** Track which context packs are sent per application. After 10 applications, review which context was most frequently used and whether BRITISH_CURRICULUM was the correct starting point.
**Owner:** Mohammed Shehzad Khan
**Review Date:** 2027-03-01 (after first application cohort)

---

### A-003
**Status:** OPEN
**Category:** Credential Strategy
**Assumption:** Omitting Harris University from premium-school recruiter packs (via `premium_schools: false` flag) improves application success rates compared to including it with full disclosure.
**Basis for assumption:** Hypothesis only. Premium schools may be more credential-scrutinous. Harris University's recognition status is unverified. Omission is the conservative choice.
**Impact if wrong:** If Harris University is in fact recognised and premium schools would view an MA positively, the omission flag is actively harming premium-school applications.
**Validation Method:** If G-006 (Harris University external verification) is obtained, reassess the `premium_schools` flag and set to `true`. Until then, assumption remains OPEN. Could also be tested via A/B comparison of packs with and without the credential, if sample size permits.
**Owner:** Mohammed Shehzad Khan
**Review Date:** 2026-12-01 (tied to G-006 target date)

---

### A-004
**Status:** OPEN
**Category:** Technical Architecture
**Assumption:** YAML is a sufficient and maintainable format for the Canonical Career Model. It will remain readable and editable by non-technical users (the owner) without assistance.
**Basis for assumption:** YAML is human-readable, widely supported, and appropriate for the data complexity involved. It is simpler than JSON for nested structures.
**Impact if wrong:** If YAML proves error-prone for the owner to maintain (e.g., indentation errors break builds, field names drift), a different format (TOML, structured Markdown, or a simple web form) may be needed.
**Validation Method:** Review the owner's experience editing YAML during Week 2. If errors are frequent or corrections require Claude Code assistance more than twice, reconsider the format.
**Owner:** Mohammed Shehzad Khan / Claude Code
**Review Date:** Week 2 complete

---

### A-005
**Status:** OPEN
**Category:** Application Strategy
**Assumption:** Strategy B (Mid-Tier International Schools) represents the highest-probability market for the 2027 job search, and is therefore the correct emphasis for the first full build cycle.
**Basis for assumption:** Mid-tier international schools represent the largest volume of advertised international positions in China and the Gulf. Strategy A (Premium) has lower probability given Harris University verification gap. Strategy C (Trainer) has lower volume.
**Impact if wrong:** If the job market shifts, or if the owner's PGCE and practitioner research make Strategy A more competitive than assumed, the CV variant and pack emphasis should be reweighted.
**Validation Method:** After 10 applications per strategy, compare interview invitation rates. Update strategy prioritisation accordingly.
**Owner:** Mohammed Shehzad Khan
**Review Date:** 2027-03-01 (after first application cohort)

---

### A-006
**Status:** OPEN
**Category:** Technical Architecture
**Assumption:** The Career OS will remain maintainable by a single person (the owner) using Claude Code assistance, without dedicated DevOps or a software development team.
**Basis for assumption:** The system is deliberately designed to be simple — static files, Python scripts, no database, no server infrastructure. Complexity is bounded.
**Impact if wrong:** If the system grows beyond maintainable complexity (e.g., 200+ YAML fields, 15+ scripts, complex interdependencies), the governance overhead may exceed the time savings.
**Validation Method:** After v1.0.0 release, assess monthly maintenance time. If governance tasks exceed 2 hours per month for routine updates, simplification is needed.
**Owner:** Mohammed Shehzad Khan
**Review Date:** 2027-01-01 (3 months post-release)

---

## Validated Assumptions

*(None yet — will be populated as assumptions are confirmed by outcomes)*

---

## Disproved Assumptions

*(None yet — will be populated if assumptions are shown to be incorrect)*

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-30 | Initial — A-001 through A-006 pre-populated |
