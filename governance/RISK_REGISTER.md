# RISK_REGISTER.md

**Version:** 1.0 (Career OS v4.0)
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Created:** 2026-07-30

**Purpose:** Tracks active risks to the Career OS, the professional record, and the 2027 job search. Distinct from:
- `TECHNICAL_DEBT.md` — engineering shortcomings in the system
- `DECISION_LOG.md` — why decisions were made
- `EVIDENCE_GAP_REGISTER.md` — missing professional documents

Risks require **active monitoring**, not just documentation. Each risk has a probability, impact, and mitigation strategy. Unlike Technical Debt, risks are not always resolvable — they require ongoing management.

---

## Risk Matrix

| Probability | Impact | Rating |
|---|---|---|
| High × High | — | **CRITICAL** |
| High × Medium | — | **HIGH** |
| Medium × High | — | **HIGH** |
| Medium × Medium | — | **MEDIUM** |
| Low × High | — | **MEDIUM** |
| Low × Medium | — | **LOW** |
| Any × Low | — | **LOW** |

---

## Status Key

| Status | Meaning |
|---|---|
| `OPEN` | Risk is active; mitigation in progress or not yet started |
| `MITIGATED` | Mitigation measures are in place; risk reduced but not eliminated |
| `CLOSED` | Risk no longer applies; record retained for audit |
| `ACCEPTED` | Risk acknowledged; no mitigation planned; owner has accepted exposure |

---

## Risk Register

### R-001
**Rating:** HIGH
**Status:** MITIGATED
**Category:** Professional Credibility
**Risk:** A recruiter or employer questions the recognition status of Harris University and perceives the MA credential as fraudulent or unverifiable.
**Probability:** Medium
**Impact:** High — could result in an application being discarded or an offer being withdrawn
**Mitigation:**
- Degree listed factually with no embellishment or accreditation claims (Decision D-008)
- Internal flag `verification_status: requires_external_review` ensures it is never marketed as from an accredited institution
- `premium_schools: false` prevents inclusion in premium-context packs where credential scrutiny is highest
- G-006 in Evidence Gap Register targets external verification by 2026-12-01
- INTERVIEW_DEFENSIBILITY_REGISTER.md includes talking points if the question arises at interview
**Residual Risk:** Medium — institution recognition cannot be controlled; factual presentation is the only available mitigation
**Owner:** Mohammed Shehzad Khan
**Review Date:** 2026-12-01 (after G-006 target date)

---

### R-002
**Rating:** MEDIUM
**Status:** MITIGATED
**Category:** Data Consistency
**Risk:** Inconsistent school terminology across CVs, LinkedIn, portfolio, and recruiter packs causes recruiter confusion or creates the appearance of dishonesty (e.g., different names for the same employer appearing in different documents).
**Probability:** Low
**Impact:** Medium — creates recruiter doubt; may prompt additional verification questions
**Mitigation:**
- `governance/Career_Taxonomy.md` defines canonical terms; no synonym drift permitted
- All generated documents must use `career-data/facts/` as their sole data source — preventing inconsistency at generation time
- Regression test `test_employment.py::test_aoxin_appears_twice()` verifies key entries match across outputs
- QA check in `qa_check.py` validates employer name consistency pre-release
**Residual Risk:** Low — systematic controls in place once Week 3 automation is live
**Owner:** Claude Code (automation) / Mohammed Shehzad Khan (data)
**Review Date:** Week 3 complete

---

### R-003
**Rating:** HIGH**
**Status:** OPEN
**Category:** Application Readiness
**Risk:** Applications begin before key reference letters are obtained (G-002: GEDU reference), leaving major claims unsupported at shortlisting or interview stage.
**Probability:** Medium
**Impact:** High — applications to training and leadership roles without a GEDU reference are significantly weaker
**Mitigation:**
- G-002 in Evidence Gap Register with target date 2026-09-15
- Application Strategy C (Trainer) notes GEDU reference as highest priority for that strategy
- Do not apply to teacher training or CPD roles before G-002 is obtained
**Residual Risk:** Medium until G-002 is obtained; drops to Low after
**Owner:** Mohammed Shehzad Khan
**Review Date:** 2026-09-15

---

### R-004
**Rating:** MEDIUM
**Status:** MITIGATED
**Category:** Data Integrity
**Risk:** Evidence files are lost, corrupted, or accidentally deleted — making verified claims unable to be substantiated.
**Probability:** Low
**Impact:** High — loss of primary evidence degrades credential confidence levels permanently
**Mitigation:**
- Evidence files stored in `evidence/` directory under version control (git)
- Git history preserves all previous versions of all tracked files
- SHA-256 checksums (computed at Week 2 freeze) will detect any post-freeze tampering or corruption
- Owner maintains physical copies of primary documents separately
**Residual Risk:** Low — multiple independent backups via git history and physical copies
**Owner:** Mohammed Shehzad Khan
**Review Date:** Week 2 freeze date

---

### R-005
**Rating:** HIGH
**Status:** OPEN
**Category:** Employment Gap
**Risk:** A recruiter identifies the 2020–2024 period as a gap and suspects it conceals a serious issue (dismissal, disciplinary action, or unauthorised absence) rather than the documented WhiteHat Jr / GEDU appointments.
**Probability:** Medium
**Impact:** High — gap questions are standard in international school hiring; a poor answer at interview can be disqualifying
**Mitigation:**
- `employment.yml` will include `gap_explanation` field for the 2020–2024 period (Week 2 task)
- WhiteHat Jr (Aug 2020 – Jul 2022) and GEDU (Sep 2022 – Aug 2023) cover the period with documented roles
- The Aoxin re-engagement (Feb 2024) documents continuity into current role
- INTERVIEW_DEFENSIBILITY_REGISTER.md will include a prepared answer for "What happened between 2020 and 2024?"
- RECRUITER_QA.md (Week 4) will include this as a mandatory scenario
**Residual Risk:** Medium — risk is mitigated by documentation but cannot be fully eliminated; depends on interview preparation
**Owner:** Mohammed Shehzad Khan
**Review Date:** Week 2 complete (gap_explanation field populated)

---

### R-006
**Rating:** MEDIUM
**Status:** OPEN
**Category:** Technical Governance
**Risk:** Automation built in Weeks 3–4 produces incorrect outputs silently — incorrect dates, missing claims, wrong evidence IDs — due to bugs in generators or data entry errors in YAML, without detection before deployment.
**Probability:** Low
**Impact:** High — incorrect professional data reaches recruiters; damage is hard to undo once a document is submitted
**Mitigation:**
- Regression test suite (`tests/`) catches known invariants (Aoxin count, school count, timeline entries)
- `qa_check.py` validates schema compliance before every build
- Human Approval Gate in `release.py` requires explicit sign-off before deployment
- `validate_evidence.py` verifies evidence integrity post-freeze
- Post-deploy link check verifies live URLs
**Residual Risk:** Low — defence-in-depth reduces probability of silent failures reaching deployment
**Owner:** Claude Code (automation) / Mohammed Shehzad Khan (final approval)
**Review Date:** Week 3 complete (after first full generation run)

---

## Risk Summary Dashboard

| ID | Risk | Rating | Status | Review Date |
|---|---|---|---|---|
| R-001 | Harris University recognition questioned | HIGH | MITIGATED | 2026-12-01 |
| R-002 | Inconsistent school terminology | MEDIUM | MITIGATED | Week 3 |
| R-003 | Applications before GEDU reference obtained | HIGH | OPEN | 2026-09-15 |
| R-004 | Evidence files lost or corrupted | MEDIUM | MITIGATED | Week 2 freeze |
| R-005 | 2020–2024 gap misinterpreted by recruiter | HIGH | OPEN | Week 2 |
| R-006 | Automation produces incorrect outputs silently | MEDIUM | OPEN | Week 3 |

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-30 | Initial — R-001 through R-006 pre-populated |
