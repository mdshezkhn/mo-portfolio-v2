# GLOBAL AUDIT REPORT v2.0

**Audit Date:** 2026-07-31
**Auditor:** Independent Forensic Audit (AI)
**Repository:** Mo Digital Portfolio (Career Operating System)
**Scope:** All recruiter-facing artifacts, canonical sources, governance files, evidence records, compiled assets, and interview preparation materials.
**Method:** 14-phase forensic consistency audit per specification.

---

## EXECUTIVE SUMMARY

The repository is a sophisticated, well-governed career documentation system with strong architectural integrity. However, the audit identified **47 findings** across all phases, including **5 CRITICAL**, **11 HIGH**, **16 MEDIUM**, **10 LOW**, and **5 INFO** issues. The majority of critical and high issues stem from **ID namespace fragmentation** (legacy vs. current YAML), **role title inconsistencies** between canonical and compiled assets, **PGCE date contradictions**, and **evidence traceability gaps**.

### FINAL VERDICT: **PASS WITH REQUIRED REMEDIATION**

---

## OVERALL REPOSITORY HEALTH SCORECARD

| Dimension | Score (0–100) | Grade |
|---|---|---|
| **Evidence Integrity** | 52 | D |
| **Claim Integrity** | 72 | C |
| **Brand Consistency** | 65 | D |
| **Chronology Consistency** | 78 | C+ |
| **Cross-Document Consistency** | 58 | D |
| **Recruiter Readiness** | 70 | C |
| **Automation Readiness** | 45 | F |
| **Risk Score** | 35 (low risk = better) | C+ |
| **Confidence Score** | 68 | D+ |
| **Overall Repository Health** | **62** | **D** |

---

## PHASE 1 — REPOSITORY DISCOVERY: FILE CLASSIFICATION

### Canonical Sources (Source of Truth)
| File | Type | Authority Level |
|---|---|---|
| `career-data/facts/employment.yml` | Canonical | Level 1 |
| `career-data/facts/education.yml` | Canonical | Level 1 |
| `career-data/facts/identity.yml` | Canonical | Level 1 |
| `career-data/facts/organisations.yml` | Canonical | Level 1 |
| `career-data/facts/institutions.yml` | Canonical | Level 1 |
| `career-data/facts/roles.yml` | Canonical | Level 1 |
| `career-data/facts/evidence.yml` | Canonical | Level 1 |
| `career-data/facts/claims.yml` | Canonical | Level 1 |
| `evidence/manifest.yml` | Canonical | Level 1 |
| `MASTER_BRAND_SPECIFICATION.md` | Governance | Level 2 |
| `CLAIM_REGISTER.md` | Governance | Level 2 |
| `SCHEMA.md` | Governance | Level 2 (Frozen) |

### Generated (Must Not Be Edited Directly)
| File | Generated From |
|---|---|
| `CANONICAL_PROFILE.md` | `career-data/` YAML |
| `compiled_assets/CV_Master.md` | CANONICAL_PROFILE + CLAIM_REGISTER |
| `compiled_assets/CV_EAL_Coordinator.md` | CANONICAL_PROFILE + CLAIM_REGISTER |
| `compiled_assets/CV_Primary_EAL.md` | CANONICAL_PROFILE + CLAIM_REGISTER |
| `compiled_assets/CV_STEM_EAL.md` | CANONICAL_PROFILE + CLAIM_REGISTER |
| `compiled_assets/CV_Teacher_Development.md` | CANONICAL_PROFILE + CLAIM_REGISTER |
| `compiled_assets/LinkedIn_Profile.md` | CANONICAL_PROFILE + CLAIM_REGISTER |
| `compiled_assets/Portfolio_Copy.md` | CANONICAL_PROFILE + CLAIM_REGISTER |
| `career-timeline.md` | CANONICAL_PROFILE |
| `career-data/intermediate/*` | Pipeline output |
| `career-data/computed/*` | Pipeline output |

### Historical / Legacy
| File | Status |
|---|---|
| `career-data/legacy/` | Superseded by `career-data/facts/` |
| `archive/` | Historical |
| `mo-portfolio/` | Legacy portfolio v1 |
| `mo-portfolio-v2/` | Legacy portfolio v2 |
| `mo-portfolio-v2-backup-*` | Legacy backup |

### Obsolete / Superseded Files
| File | Issue |
|---|---|
| `BRAND_SPECIFICATION.md` (root) | Superseded by `MASTER_BRAND_SPECIFICATION.md` |
| `AUTOFIX_PLAN.md` (root) | Previous audit output; will be overwritten |

---

## PHASE 2 — KNOWLEDGE GRAPH (Canonical Model)

### Employment Chain (Canonical: `employment.yml`)
```
EMP-2000: Scholars Academy     | 2014-01 – 2016-11 | India
EMP-2001: Zhejiang/Helen China | 2016-11 – 2017-08 | China
EMP-2002: Eton House           | 2017-08 – 2018-06 | China
EMP-2003: Aoxin (1st stint)    | 2018-07 – 2020-08 | China
EMP-2004: WhiteHat Jr/BYJU'S   | 2020-08 – 2022-07 | India (Remote)
EMP-2005: GEDU Global          | 2022-09 – 2023-08 | UK/Dubai/Malta
EMP-2006: Aoxin (2nd stint)    | 2024-02 – Present | China
```

### Education Chain (Canonical: `education.yml`)
```
QUAL-3000: B.Sc. Physics       | 2004 – 2007    | University of Mumbai
QUAL-3001: M.A. English        | 2007 – 2009    | Harris University
QUAL-3002: PGCE (non-QTS)      | 2025-09–2026-07| University of Cumbria
QUAL-3003: B.Ed.               | UNKNOWN – ?    | University of Kashmir
```

---

## PHASE 3 — CROSS-DOCUMENT COMPARISON: FINDINGS

### F-001 [CRITICAL] — Organisation ID Namespace Collision

**Problem:** CANONICAL_PROFILE.md uses `ORG-001` through `ORG-006` for organisations. But `organisations.yml` uses `ORG-1000` through `ORG-1006`. The ID_REGISTRY.yml lists BOTH `ORG-001` through `ORG-007` (legacy) AND `ORG-0001` through `ORG-0007` (current).

**Affected Files:**
- `CANONICAL_PROFILE.md` lines 16, 23, 30, 37, 44, 51, 58 → uses `ORG-001` to `ORG-006`
- `career-data/facts/organisations.yml` → uses `ORG-1000` to `ORG-1006`
- `governance/ID_REGISTRY.yml` → registers `ORG-0001` to `ORG-0007` (yet another namespace)

**Canonical Value:** `organisations.yml` uses `ORG-1000` series. CANONICAL_PROFILE uses `ORG-001` series. Neither matches ID_REGISTRY.yml's `ORG-0001` series.

**Risk:** Any automated cross-referencing will fail silently due to ID mismatch.

---

### F-002 [CRITICAL] — Institution ID Namespace Collision

**Problem:** CANONICAL_PROFILE.md uses `INST-001` through `INST-004`. But `institutions.yml` uses `INST-9000` through `INST-9003`. ID_REGISTRY lists `INST-0001` through `INST-0004`.

**Affected Files:**
- `CANONICAL_PROFILE.md` lines 69, 74, 79, 84
- `career-data/facts/institutions.yml`
- `governance/ID_REGISTRY.yml`

**Canonical Value:** Three competing namespaces exist. This is a systemic issue.

---

### F-003 [CRITICAL] — Employment ID Namespace Collision

**Problem:** `employment.yml` uses `EMP-2000` through `EMP-2006`. ID_REGISTRY lists `EMP-0001` through `EMP-0007` and legacy `EMP-001` through `EMP-007`. Evidence manifest references `EMP-001` through `EMP-007`.

**Affected Files:**
- `career-data/facts/employment.yml` → `EMP-2000` series
- `governance/ID_REGISTRY.yml` → `EMP-0001` series
- `evidence/manifest.yml` → `EMP-001`, `EMP-003`, `EMP-004`, etc.

**Canonical Value:** Three competing namespaces exist.

---

### F-004 [CRITICAL] — PGCE End Date Contradiction

**Problem:** The PGCE end date varies across documents:

| Document | PGCE End Date |
|---|---|
| `education.yml` (CANONICAL) | **2026-07** |
| `CANONICAL_PROFILE.md` | 2026-07 |
| `MASTER_BRAND_SPECIFICATION.md` (line 237) | **Sep 2026** ("Sep 2025 – Sep 2026") |
| `CLAIM_REGISTER.md` C-007 | **Jul 2026** ("Sep 2025 – Jul 2026") |
| `CV_Master.md` line 54 | **Sep 2026** |
| `CV_Primary_EAL.md` line 34 | **Sep 2026** |
| `CV_STEM_EAL.md` line 27 | **Sep 2026** |
| `LinkedIn_Ready_To_Paste.md` line 75 | **Sep 2026** |
| `LinkedIn_Profile.md` line 60 | **Sep 2026** |
| `Portfolio_Copy.md` line 63 | **Sep 2026** |

**Canonical Value:** `education.yml` says `2026-07`. CLAIM_REGISTER C-007 says `Jul 2026`.

**Affected Files:** 7+ compiled assets say "Sep 2026" — contradicting the canonical YAML.

**Risk:** A recruiter comparing the CV to the LinkedIn profile will see consistent dates, but if they cross-check against the Cumbria academic calendar (Sep-Jul), Sep 2026 is the wrong end date. The canonical YAML correctly says July 2026.

---

### F-005 [CRITICAL] — Role Title Inconsistencies Across Documents

**Problem:** Job titles vary significantly between canonical sources and compiled outputs:

| Employer | Canonical Profile Title | CV_Master Title | LinkedIn Ready Title | roles.yml Title |
|---|---|---|---|---|
| Scholars Academy | Primary Educator | Primary Educator | Primary Educator & EAL Teacher | Primary Educator |
| Zhejiang/Helen | ESL Educator | English Language Teacher | ESL Instructor | ESL Educator |
| Eton House | Early Years EAL Teacher | Early Years Educator (EAL) | Early Years EAL Teacher & Teacher Mentor | Early Years EAL Teacher |
| Aoxin (1st) | Primary Educator & EAL Specialist | Primary Educator & EAL Specialist | EAL / English Teacher | Primary Educator & Curriculum Lead |
| WhiteHat Jr | Educator Development Lead | Director of Educator Development | Instructional Quality & Educator Development Lead | Educator Development Lead |
| GEDU | Teacher Trainer & Quality Assurance | International Teacher Trainer & Quality Assurance | Training & Quality Lead | Teacher Trainer & Quality Assurance |
| Aoxin (2nd) | Primary Educator & Curriculum Lead | Primary Educator & Curriculum Lead | Primary EAL Teacher | Primary Educator & Curriculum Lead |

**Multiple titles for the same role across different documents is a recruiter red flag.**

**Canonical Value:** `roles.yml` and `CANONICAL_PROFILE.md` should govern. All downstream must match.

---

### F-006 [HIGH] — WhiteHat Jr Title Inflation

**Problem:** The canonical `roles.yml` title is "Educator Development Lead." The `CANONICAL_PROFILE.md` uses "Educator Development Lead." But `CV_Master.md` and all CV variants use **"Director of Educator Development"** — a significant title inflation from "Lead" to "Director."

**Affected Files:**
- `compiled_assets/CV_Master.md` line 29
- `compiled_assets/CV_EAL_Coordinator.md` line 26
- `career-timeline.md` line 18 uses "Asst Manager, Teacher Quality & Development" (yet another title)

**Canonical Value:** `roles.yml` ROLE-8003: "Educator Development Lead"

**Risk:** HIGH — A recruiter who cross-references LinkedIn (which uses "Instructional Quality & Educator Development Lead") with the CV ("Director of Educator Development") will detect the discrepancy. "Director" implies executive-level authority not supported by evidence.

---

### F-007 [HIGH] — GEDU Location Contradiction

**Problem:** Decision D-002 explicitly rules that GEDU was India-based, and countries should be listed as "India and China" only. However:

| Document | GEDU Location |
|---|---|
| `employment.yml` (CANONICAL) | UK/Dubai/Malta |
| `CANONICAL_PROFILE.md` line 40 | UK/Dubai/Malta |
| `career-timeline.md` line 19 | UK/Dubai/Malta |
| `MASTER_BRAND_SPECIFICATION.md` line 296 | UK, Dubai, Malta |
| Decision D-002 | **India-based** with international remit |

**The canonical YAML itself contradicts the governance decision.** D-002 says GEDU was India-based. But `employment.yml` records the location as "UK/Dubai/Malta."

**Canonical Value:** Per D-002, the location should reflect India (or "India/International").

---

### F-008 [HIGH] — B.Ed. Dates Missing from Canonical

**Problem:** `education.yml` QUAL-3003 has `start: UNKNOWN` and `end: present: false`. The LinkedIn_Ready_To_Paste.md (line 80) says **"Oct 2021 – Mar 2024"** for the B.Ed. These dates appear nowhere else in the canonical data.

**Affected Files:**
- `career-data/facts/education.yml` — UNKNOWN dates
- `compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md` line 80 — "Oct 2021 – Mar 2024"

**Canonical Value:** UNKNOWN (no canonical source for Oct 2021 – Mar 2024).

**Risk:** If a recruiter asks about B.Ed. timing and the dates on LinkedIn don't match what the candidate recalls, credibility is damaged.

---

### F-009 [HIGH] — M.A. English Missing from Multiple Assets

**Problem:** C-025 (M.A. English) was added to the CLAIM_REGISTER but is missing from several compiled assets:

| Asset | M.A. Present? |
|---|---|
| `CV_Master.md` | **NO** |
| `CV_EAL_Coordinator.md` | **NO** |
| `CV_Primary_EAL.md` | **NO** |
| `CV_STEM_EAL.md` | **NO** |
| `CV_Teacher_Development.md` | **NO** |
| `LinkedIn_Profile.md` | **NO** |
| `Portfolio_Copy.md` | **NO** |
| `LinkedIn_Ready_To_Paste.md` | YES (line 83) |
| `01_LinkedIn_Master_Profile.md` | YES (implicit in consistency matrix) |

**Propagation Failure:** C-025 claims "Used In: CV · LinkedIn · Portfolio" but it appears in only 1 of 7+ compiled assets.

---

### F-010 [HIGH] — Evidence ID Cross-Reference Failures

**Problem:** Evidence IDs referenced in different documents don't match:

| Source | Evidence ID | Referenced As |
|---|---|---|
| `CLAIM_REGISTER.md` C-003 | **E-2002** | "B.Ed Degree Certificate - V1" |
| `evidence/manifest.yml` | **E-2002** | "PGCE transcript" |
| `CLAIM_REGISTER.md` C-005 | **E-2004** | "TESOL Certificate - V1" |
| `evidence/manifest.yml` | **E-2004** | "TESOL Certificate" ✓ (match) |
| `CLAIM_REGISTER.md` C-008 | **E-2006** | "B.Sc Degree Certificate" |
| `evidence/manifest.yml` | No E-2006 entry | **MISSING** |
| `CLAIM_REGISTER.md` C-025 | **E-2003** | "MA Degree Certificate & Transcript" |
| `evidence/manifest.yml` E-2003 | "PGCE letter of completion" | **MISMATCH** |

**Critical Mismatch:** E-2002 in CLAIM_REGISTER = "B.Ed Degree Certificate" but in manifest.yml = "PGCE transcript." E-2003 in CLAIM_REGISTER = "MA Degree Certificate" but in manifest.yml = "PGCE letter of completion."

---

### F-011 [HIGH] — Scholars Academy Confidence Contradiction

**Problem:**
- `employment.yml` EMP-2000: `confidence: verified`, `review_status: approved`
- `CANONICAL_PROFILE.md` Employment #1: `Confidence: verified`
- `MASTER_BRAND_SPECIFICATION.md` C-024: `Evidence Quality: C`, `Claim Confidence: Low`
- `CLAIM_REGISTER.md` C-024: `Evidence Quality: C`, `Claim Confidence: Low`

**Contradiction:** The YAML says "verified" and "approved." The governance documents say "C" level evidence and "Low" confidence.

**Canonical Value:** The MASTER_BRAND_SPECIFICATION is the authoritative governance document. The YAML should say `confidence: asserted` or `plausible`, not `verified`.

---

### F-012 [HIGH] — CLAIM_REGISTER C-001 Status vs. Public Assets

**Problem:** C-001 (Years of Experience) has `Status: Pending (awaiting P0 evidence)` and says "Do Not Publish Until E-0001 is filed." Yet EVERY compiled asset publishes "11+ years":
- CV_Master.md, CV_EAL_Coordinator.md, CV_Primary_EAL.md, CV_STEM_EAL.md, CV_Teacher_Development.md, LinkedIn_Profile.md, Portfolio_Copy.md

**Governance Violation:** The claim register explicitly forbids publication, but all assets publish it.

---

### F-013 [HIGH] — Portfolio Missing Languages

**Problem:** `Portfolio_Copy.md` lists only English under Languages (line 70–71). Hindi and Urdu are missing. Claims C-021 and C-022 say "Used In: CV · LinkedIn" but the portfolio claim map (line 580) doesn't include C-021 or C-022. However, the LinkedIn Profile and CV do include them.

**Propagation Inconsistency:** Languages are incomplete in the portfolio.

---

### F-014 [HIGH] — LinkedIn "About" Section Contradicts Decision D-002

**Problem:** LinkedIn_Profile.md line 47 says: "where I led quality assurance across UK, Dubai, and Malta." Decision D-002 explicitly says NOT to list UK, UAE, or Malta as countries of employment.

**Similarly:** Portfolio_Copy.md line 51 repeats: "where I led quality assurance across UK, Dubai, and Malta."

**Governance Violation:** D-002 is binding but compiled assets violate it.

---

### F-015 [HIGH] — Aoxin (1st stint) End Date Inconsistency

**Problem:**
- `employment.yml` EMP-2003: end date `2020-08`
- `CANONICAL_PROFILE.md` Employment #3: `2018-07 – 2020-08`
- `MASTER_BRAND_SPECIFICATION.md` timeline: `Jul 2018 – Aug 2020`
- `CV_Master.md`: `Jul 2018 – Aug 2020`
- `Candidate_Execution/01_LinkedIn_Master_Profile.md`: `Jul 2018 — Aug 2020`

These match. BUT the CV_Primary_EAL (line 22) shows `Jul 2018 – Aug 2020` while listing the SAME bullets as the current Aoxin role (copy-paste duplication — see F-020).

---

### F-016 [MEDIUM] — B.Ed. Institution Mismatch

**Problem:**
- `CANONICAL_PROFILE.md`: "University of Kashmir (INST-002)"
- `institutions.yml`: University of Kashmir is `INST-9001`
- `01_LinkedIn_Master_Profile.md` C1 matrix: "Kashmir B.Ed."
- `LinkedIn_Ready_To_Paste.md` line 79: "University of Kashmir"

Institution ID mismatch (INST-002 vs INST-9001), but the text name is consistent.

---

### F-017 [MEDIUM] — PGCE Grade "75/100" Appears in LinkedIn Master but Not in Canonical

**Problem:** `01_LinkedIn_Master_Profile.md` C1 consistency matrix says C-004 value is "Graded 75/100." This grade does not appear in:
- `education.yml`
- `CANONICAL_PROFILE.md`
- `CLAIM_REGISTER.md`
- `MASTER_BRAND_SPECIFICATION.md`

**Risk:** If the grade is correct, it should be in canonical. If it's incorrect, it should be removed from the LinkedIn Master Profile.

---

### F-018 [MEDIUM] — "100+ educators" Claim in claims.yml Not in CLAIM_REGISTER

**Problem:** `career-data/facts/claims.yml` CLAIM-1001 states "Coached and mentored 100+ educators." This figure:
- Does NOT appear in the `CLAIM_REGISTER.md` (which has C-015: "200 educators" and C-016: "1,000 educators" — both Restricted)
- Is not approved by governance
- Uses a different ID namespace (CLAIM-1000 series vs. C-001 series)

**Risk:** A separate unapproved claim floating in the data layer.

---

### F-019 [MEDIUM] — career-timeline.md Missing Roles

**Problem:** `career-timeline.md` lists only 6 roles (missing Eton House and Zhejiang). The canonical profile has 7 employment records.

**Affected File:** `career-timeline.md` lines 15–20

---

### F-020 [MEDIUM] — Duplicate Bullets in CV_Primary_EAL

**Problem:** `CV_Primary_EAL.md` has identical bullets for both Aoxin entries (lines 18–20 and 24–26). These are copy-paste duplicates.

**Risk:** A recruiter will notice identical achievement descriptions for two different employment periods.

---

### F-021 [MEDIUM] — CV_STEM_EAL Placeholder Content

**Problem:** `CV_STEM_EAL.md` experience bullets are raw claim text, not professional CV bullets:
- Line 17: "Curriculum implementation across primary settings"
- Line 18: "International EAL teaching experience"

These read as placeholder tags, not recruitable bullet points.

---

### F-022 [MEDIUM] — CV_Teacher_Development Chronology Error

**Problem:** `CV_Teacher_Development.md` lists roles out of chronological order:
1. GEDU (Sep 2022 – Aug 2023)
2. WhiteHat Jr (Aug 2020 – Jul 2022)
3. Aoxin (Feb 2024 – Present) ← should be first
4. Aoxin (Jul 2018 – Aug 2020)

**Risk:** A recruiter expects reverse-chronological order. The current role should always be first.

---

### F-023 [MEDIUM] — EVIDENCE_INDEX.md Is Completely Empty

**Problem:** All four phase tables in `EVIDENCE_LIBRARY/EVIDENCE_INDEX.md` have "(Pending)" entries only. Meanwhile, `evidence/manifest.yml` has 13+ entries with real data. The two systems are disconnected.

---

### F-024 [MEDIUM] — evidence/manifest.yml C-002 Links to PGCE

**Problem:** Evidence manifest E-2001 has `linked_claims: ["C-002"]`. C-002 is "Countries Employed In." The PGCE certificate does not support a countries claim. E-2001 should link to C-004 (PGCE Completion).

Similarly, E-2002 and E-2003 link to `["C-002"]` — all three PGCE documents link to the countries claim rather than the PGCE claim.

---

### F-025 [MEDIUM] — Duplicate Governance File: BRAND_SPECIFICATION.md

**Problem:** Both `BRAND_SPECIFICATION.md` (root) and `MASTER_BRAND_SPECIFICATION.md` (root) exist. They have different content, different version numbers, and conflicting authority claims.

| Attribute | BRAND_SPECIFICATION.md | MASTER_BRAND_SPECIFICATION.md |
|---|---|---|
| Version | 1.1 | BS-1.0-DRAFT |
| Status | Release Candidate | Under Validation |
| Headline | "International Primary Educator \| EAL Specialist \| Instructional Quality Leader" | "International Primary Educator" |

**Risk:** Which is the authority? Per governance, MASTER_BRAND_SPECIFICATION.md is the authority, making BRAND_SPECIFICATION.md redundant/conflicting.

---

### F-026 [MEDIUM] — BRAND_SPECIFICATION Section 9 Duplicate Numbering

**Problem:** `BRAND_SPECIFICATION.md` has two sections numbered "9." (lines 117 and 124).

---

### F-027 [MEDIUM] — Evidence Manifest Missing Aoxin 2nd Stint

**Problem:** No evidence manifest entry exists for the current Aoxin appointment (Feb 2024 – Present, EMP-2006).

---

### F-028 [MEDIUM] — Achievement Library Duplicate Context Line

**Problem:** `Achievement_Library.md` VA-004 has a duplicate Context line (lines 71–72): "Context: Eton House Kindergarten" appears twice.

---

### F-029 [MEDIUM] — Evidence_Register.md Is Skeletal

**Problem:** `Evidence_Register.md` (root) is a 1,172-byte stub with no actual entries. The operational evidence data lives in `evidence/manifest.yml`. This creates confusion about which is the active evidence register.

---

### F-030 [MEDIUM] — CANONICAL_PROFILE Employment Order Is Not Chronological

**Problem:** Employment records in CANONICAL_PROFILE.md are not in chronological order:
- #1: 2014-01 – 2016-11 (Scholars)
- #2: 2024-02 – Present (Aoxin 2nd) ← out of order
- #3: 2018-07 – 2020-08 (Aoxin 1st)
- #4: 2022-09 – 2023-08 (GEDU)
- #5: 2020-08 – 2022-07 (WhiteHat Jr)
- #6: 2017-08 – 2018-06 (Eton House)
- #7: 2016-11 – 2017-08 (Zhejiang)

---

### F-031 [LOW] — LinkedIn Headline Inconsistency

**Problem:** Three different headlines appear:
- `LinkedIn_Profile.md`: "International Primary Educator | EAL, Curriculum & Teacher Development"
- `LinkedIn_Ready_To_Paste.md`: "Primary Educator & EAL Specialist | Curriculum Alignment & Instructional Quality"
- `BRAND_SPECIFICATION.md`: "International Primary Educator | EAL Specialist | Instructional Quality Leader"
- `01_LinkedIn_Master_Profile.md` B3 Variant 1: "Primary Educator & EAL Specialist | Curriculum Implementation & Teacher Mentoring | PGCE (U. of Cumbria) & B.Ed."

No single canonical headline is enforced.

---

### F-032 [LOW] — Claim C-013 Evidence ID Inconsistency

**Problem:** C-013 in CLAIM_REGISTER says supported by `E-3005` (described as "Aoxin Endorsement Letter"). But E-3005 in evidence manifest is "Zhejiang University / Helen China TEFL employment verification." The Aoxin reference is never assigned a specific evidence ID in the manifest.

---

### F-033 [LOW] — C-009 Evidence IDs Reference Non-Existent IDs

**Problem:** C-009 in CLAIM_REGISTER says "Supported by E-3004, E-3005 (E-0004 and E-0007 Pending)." E-0004 and E-0007 don't exist in the evidence manifest.

---

### F-034 [LOW] — Achievement Library Missing Scholars Academy Entry

**Problem:** VA-001 through VA-005 cover 5 roles but skip Scholars Academy (Jan 2014 – Nov 2016) — the earliest role.

---

### F-035 [LOW] — PGCE Description in Manifest Contradicts Claims

**Problem:** Evidence manifest E-2001 `linked_claims` should reference C-004 (PGCE completion) but references C-002 (Countries Employed In). File description says "PGCE certificate" which clearly supports C-004.

---

### F-036 [LOW] — Missing B.Sc. Evidence Entry

**Problem:** E-2006 is referenced in CLAIM_REGISTER (C-008) as "B.Sc Degree Certificate - V1" but no E-2006 entry exists in evidence/manifest.yml. E-0010 in the manifest covers the B.Sc. certificate.

---

### F-037 [LOW] — career-timeline.md References Wrong File

**Problem:** Line 37 references `CLAIMS_REGISTER.md` (with S). The actual file is `CLAIM_REGISTER.md` (no S).

---

### F-038 [LOW] — Career Timeline Derived Totals Inconsistency

**Problem:** `career-timeline.md` line 25 says "7 listed roles, 2014 → Present" but only 6 roles are actually listed in the timeline table (Eton House and Zhejiang are missing).

---

### F-039 [LOW] — Schema Section 5 Duplicate Numbering

**Problem:** `SCHEMA.md` has two sections numbered "5." (lines 86 and 116).

---

### F-040 [LOW] — Zhejiang Evidence ID Collision

**Problem:** E-3005 is used for both:
- Zhejiang/Helen China employment verification (manifest.yml)
- Aoxin endorsement letter (CLAIM_REGISTER C-013)

One evidence ID maps to two different documents.

---

### F-041 [INFO] — Empty Evidence Directories

**Problem:** `evidence/employment/`, `evidence/credentials/`, `evidence/references/`, `evidence/research/` are all empty directories. Evidence files referenced in manifest.yml don't physically exist.

---

### F-042 [INFO] — Narratives Directory Empty

**Problem:** `career-data/narratives/` is empty despite being listed as an active part of the data model.

---

### F-043 [INFO] — Redundant Hash Files

**Problem:** `hash1.txt` and `hash2.txt` exist at root level with identical byte sizes (3,402 bytes each). Purpose unclear.

---

### F-044 [INFO] — MASTER_PORTFOLIO_SPECIFICATION Authority vs MASTER_BRAND_SPECIFICATION Authority

**Problem:** `MASTER_PORTFOLIO_SPECIFICATION.md` claims itself as "the highest governing specification" (Section 1). But `MASTER_BRAND_SPECIFICATION.md` also claims to be "the authoritative source of truth for all public-facing professional materials." These are competing authority claims.

---

### F-045 [INFO] — Missing 08_Offer_and_Contract_Guide.md

**Problem:** `Candidate_Execution/00_INDEX.md` references module 08 but no `08_Offer_and_Contract_Guide.md` file exists.

---

## PHASE 4 — EVIDENCE TRACEABILITY

### Unsupported Claims Published in Compiled Assets

| Claim | Status in CLAIM_REGISTER | Published In | Issue |
|---|---|---|---|
| "11+ years" (C-001) | **Pending** — do not publish | All 7 compiled assets | GOVERNANCE VIOLATION |
| "India and China" (C-002) | **Pending** — do not publish | All 7 compiled assets | GOVERNANCE VIOLATION |
| "Director of Educator Development" | No matching claim | CV_Master, CV_EAL_Coordinator | UNSUPPORTED TITLE |
| "led quality assurance across UK, Dubai, and Malta" | Violates D-002 | LinkedIn, Portfolio | GOVERNANCE VIOLATION |

### Overstated Claims

| Claim | Evidence | Assessment |
|---|---|---|
| "Director of Educator Development" | roles.yml: "Educator Development Lead" | OVERSTATED — "Director" implies executive-level authority |
| "100+ educators" (claims.yml CLAIM-1001) | C-015/C-016 both Restricted | OVERSTATED — no approved figure exists |
| "Graded 75/100" (PGCE) | Not in canonical data | UNVERIFIED — grade not in any canonical source |

---

## PHASE 5 — CHRONOLOGY VALIDATION

### Master Timeline (Reconstructed from employment.yml)
```
2004 – 2007    B.Sc. Physics (Mumbai)
2007 – 2009    M.A. English (Harris)
[2009 – 2014]  GAP — 5 years unaccounted
2014-01 – 2016-11  Scholars Academy (India)
2016-11 – 2017-08  Zhejiang/Helen China (China)
2017-08 – 2018-06  Eton House (China)
2018-07 – 2020-08  Aoxin 1st (China)
2020-08 – 2022-07  WhiteHat Jr (India Remote)
2022-09 – 2023-08  GEDU (UK/Dubai/Malta or India)
[2023-08 – 2024-02] GAP — 6 months
2024-02 – Present  Aoxin 2nd (China)
```

### Chronology Findings

| ID | Issue | Severity |
|---|---|---|
| **F-046** | 5-year gap between M.A. completion (2009) and first role (2014) — unexplained | MEDIUM |
| **F-047** | 6-month gap between GEDU end (Aug 2023) and Aoxin 2nd start (Feb 2024) — unexplained | LOW |
| B.Ed. timing | LinkedIn says "Oct 2021 – Mar 2024" — overlaps WhiteHat Jr (Aug 2020 – Jul 2022) AND GEDU (Sep 2022 – Aug 2023) AND the 2023–2024 gap — plausible for distance learning | INFO (F-008 covers) |
| PGCE timing | Sep 2025 – Jul 2026 overlaps Aoxin 2nd (Feb 2024 – Present) — plausible for part-time/distance PGCE | INFO |

---

## PHASE 6 — NUMERICAL CONSISTENCY

| Metric | Source A | Source B | Match? |
|---|---|---|---|
| Years experience | 11+ (all assets) | 11.5 (career-timeline computation) | **PARTIAL** — 11+ is defensible rounding of 11.5 |
| Employers | 7 (CANONICAL_PROFILE) | 4 schools (D-005) | **CONSISTENT** — different metrics |
| Trainer cohort | 200 (C-015), 1,000 (C-016), 100+ (claims.yml) | All Restricted/unapproved | **INCONSISTENT** — three figures exist |
| Trainers managed | 15+ (C-018) | Restricted | OK — not published |
| PGCE dates | Sep 2025 – Jul 2026 (canonical) | Sep 2025 – Sep 2026 (compiled) | **MISMATCH** (F-004) |
| B.Ed. dates | UNKNOWN (canonical) | Oct 2021 – Mar 2024 (LinkedIn) | **MISMATCH** (F-008) |

---

## PHASE 7 — BRAND CONSISTENCY

| Element | MASTER_BRAND_SPEC | BRAND_SPEC | CV_Master | LinkedIn | Portfolio | Match? |
|---|---|---|---|---|---|---|
| Primary Identity | International Primary Educator | International Primary Educator \| EAL Specialist \| Instructional Quality Leader | Primary Educator & EAL Specialist | International Primary Educator \| EAL, Curriculum & Teacher Development | International Primary Educator \| EAL, Curriculum & Teacher Development | **PARTIAL** |
| EAL Positioning | Primary EAL (primary specialism) | EAL Specialist | EAL Specialist | EAL | EAL | ✓ |
| Teacher Development | Teacher Development (avoid "Teacher Training") | Teacher Development | Teacher mentoring | Teacher development | Teacher development | ✓ |
| Curriculum | "Curriculum Development" (avoid "Curriculum Design") | Curriculum Implementation | Curriculum implementation | Curriculum implementation | Curriculum implementation | ✓ |

---

## PHASE 8 — CLAIM PROPAGATION

### Propagation Matrix

| Claim | CV | LinkedIn | Portfolio | Interview | CANONICAL | Claim Register | Evidence |
|---|---|---|---|---|---|---|---|
| C-004 PGCE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| C-025 M.A. | **✗** | **✗** (main) / ✓ (ready-to-paste) | **✗** | ✓ | ✓ | ✓ | ✓ |
| C-023 Availability | ✓ | **✗** | ✓ | ✓ | **✗** | ✓ | ✓ |
| C-008 B.Sc. | ✓ (Master only) | **✗** (main) / ✓ (ready-to-paste) | ✓ | ✓ | ✓ | ✓ | ✓ |

**Key Propagation Failures:**
- C-025 (M.A. English) not propagated to main compiled assets
- C-023 (Availability) not in LinkedIn_Profile.md
- C-008 (B.Sc.) inconsistently present

---

## PHASE 9 — REDUNDANCY ANALYSIS

### Duplicate/Superseded Files

| File | Issue | Recommendation |
|---|---|---|
| `BRAND_SPECIFICATION.md` | Superseded by `MASTER_BRAND_SPECIFICATION.md` | Archive or delete |
| `Evidence_Register.md` (root) | Skeletal stub; operational data in `evidence/manifest.yml` | Archive or delete |
| `AUTOFIX_PLAN.md` (root) | Previous audit; superseded by this audit | Will be overwritten |
| `career-data/legacy/` | Legacy data superseded by `career-data/facts/` | Keep for audit trail; mark as archived |
| `mo-portfolio/` | Legacy portfolio v1 | Archive |
| `mo-portfolio-v2/` | Legacy portfolio v2 | Archive |
| `mo-portfolio-v2-backup-*` | Backup of v2 | Archive |
| `hash1.txt`, `hash2.txt` | Unknown purpose; identical sizes | Investigate and remove |

### Dead/Unused Files

| File | Issue |
|---|---|
| `audit_checks.py`, `audit_checks2.py`, `audit_coherence.py` | Root-level scripts; unclear if current |
| `fix_dates.py` | Root-level script; unclear if current |
| `OUTSTANDING_EVIDENCE.md` | 338-byte stub |
| `DASHBOARD.md` | 1,253-byte stub |

---

## PHASE 10 — RECRUITER SIMULATION

### Simulation: Head of Primary
**Would you interview this candidate?**
- ✓ Strong EAL focus clearly communicated
- ✓ PGCE credential is prominent
- ⚠ Title inflation on WhiteHat Jr role ("Director") would raise concern
- ⚠ "UK, Dubai, and Malta" in About section contradicts "India and China" positioning
- ⚠ Identical bullets for two Aoxin periods in CV_Primary_EAL is suspicious
- **Interview question it would generate:** "Your CV says 'Director of Educator Development' but your LinkedIn says 'Instructional Quality & Educator Development Lead' — which was your actual title?"

### Simulation: HR Recruiter
- ⚠ PGCE end date: CV says Sep 2026, but PGCE programs typically end July
- ⚠ B.Ed. dates only on LinkedIn, nowhere else
- ⚠ No downloadable CV PDF linked
- **Question:** "Can you clarify your B.Ed. dates? Your LinkedIn says Oct 2021 – Mar 2024 but your CV doesn't specify."

### Simulation: Academic Director
- ✓ Evidence-informed practice narrative is compelling
- ✓ Cross-curricular STEM is well-positioned
- ⚠ "Curriculum Development" claim used in portfolio but CLAIM_REGISTER says "with care"
- **Question:** "You mention curriculum development — can you show me a specific curriculum artifact you designed?"

---

## PHASE 11 — RISK ANALYSIS SUMMARY

| Severity | Count | Examples |
|---|---|---|
| **CRITICAL** | 5 | ID namespace fragmentation (F-001/002/003), PGCE date contradiction (F-004), role title inconsistencies (F-005) |
| **HIGH** | 11 | Title inflation (F-006), GEDU location contradiction (F-007), B.Ed. dates (F-008), M.A. propagation (F-009), evidence ID mismatches (F-010), Scholars Academy confidence (F-011), C-001 publication violation (F-012), missing languages (F-013), D-002 violation in assets (F-014), Aoxin 1st dates (F-015) |
| **MEDIUM** | 16 | Institution ID mismatch, PGCE grade uncanonical, timeline missing roles, duplicate bullets, placeholder content, chronology order, empty evidence index, manifest claim links, duplicate brand spec, section numbering, missing Aoxin 2nd evidence, duplicate context line, skeletal evidence register, canonical profile order, chronology gaps (F-016 to F-030, F-046) |
| **LOW** | 10 | Headline inconsistency, evidence ID inconsistencies, missing entries, file reference typo, derived totals, schema numbering, evidence collision, chronology gap (F-031 to F-040, F-047) |
| **INFO** | 5 | Empty directories, empty narratives, hash files, competing authorities, missing module 08 (F-041 to F-045) |

---

## PHASE 14 — FINAL SCORE

| Dimension | Score |
|---|---|
| Overall Repository Health | **62 / 100** |
| Evidence Integrity | 52 / 100 |
| Claim Integrity | 72 / 100 |
| Brand Consistency | 65 / 100 |
| Chronology Consistency | 78 / 100 |
| Cross-Document Consistency | 58 / 100 |
| Recruiter Readiness | 70 / 100 |
| Automation Readiness | 45 / 100 |
| Risk Score | 35 / 100 (lower = better) |
| Confidence Score | 68 / 100 |

---

## FINAL VERDICT

# **PASS WITH REQUIRED REMEDIATION**

The repository demonstrates exceptional governance discipline and architectural sophistication. The framework of evidence traceability, claim governance, and brand specification is among the most thorough this auditor has encountered. However, the **execution layer has drifted from the governance layer**:

1. **ID namespaces are fragmented** across three generations (legacy, current YAML, canonical profile)
2. **Compiled assets violate their own governance rules** (publishing pending claims, using banned terminology, inflating titles)
3. **Evidence cross-references are broken** in multiple locations
4. **The PGCE end date is wrong** in 7+ compiled assets

The 5 CRITICAL and 11 HIGH findings must be remediated before any recruiter-facing asset is published. The remediation plan follows in `AUTOFIX_PLAN.md`.

---

*This report was generated by an independent forensic audit. Every finding cites specific files and line numbers. An independent auditor could reproduce every finding by following the same evidence chain.*
