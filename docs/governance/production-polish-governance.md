# Production Design System & Professional Consistency Audit Plan

**Governance Version:** v1.0
**Status:** Approved
**Effective Date:** 2026-07-19
**Owner:** Mohammed Shehzad Khan
**Supersedes:** All previous Production Polish governance documents

Project Meridian has transitioned from the "build" phase to the "production polish" phase. The objective is to minimize risk while maximizing consistency, ensuring every public touchpoint tells exactly the same professional story, and the UI feels like a single coherent system.

## Definition of Done

The project is considered Production Ready only when all of the following are true:
- Portfolio, CV and LinkedIn contain no factual inconsistencies.
- All production assets resolve successfully (no unintended 404s).
- Recruiter Scan Test passes at 5 seconds, 30 seconds and 2 minutes.
- No design drift remains against the Project Meridian design language.
- Lighthouse ≥95 Performance, Accessibility, Best Practices and SEO.
- WCAG AA compliance maintained.
- No HTML validation errors.
- No console errors.
- No layout shifts or overflow on desktop, tablet or mobile.
- No further structural or visual changes are required.

## Critical Constraints

> [!CAUTION]
> **Source of Truth Hierarchy**
> Resolve conflicts using this priority: 1) User's explicit instruction here, 2) Latest approved CV, 3) Portfolio, 4) LinkedIn, 5) Older archive files. Do not decide independently.

> [!CAUTION]
> **No Hallucination & No Silent Changes Rule**
> Never infer metrics, scope, promotions, years, or responsibilities. If evidence does not exist: flag it, do not invent it.
> Every modified file must appear in the final report. No hidden edits. No opportunistic cleanup. No formatting-only changes unless approved.

> [!CAUTION]
> **Structural Redesigns Prohibited**
> Structural redesigns are prohibited. Existing layouts, section order, and information architecture must remain unchanged. Presentation refinements (spacing, typography, alignment, responsive adjustments, and visual consistency) are permitted when they do not alter functionality or information hierarchy.

> [!WARNING]
> **Preserve Intent Rule**
> Equivalent wording that materially changes professional positioning, emphasis, or recruiter perception must not replace approved wording unless explicitly approved by the user. Grammar, punctuation, typography, spelling, and British English corrections that do not materially alter meaning may be applied without being classified as narrative changes. Preserve approved terminology including:
> - International Primary Educator
> - EAL / Multilingual Learning
> - STEM-through-English
> - Teacher Trainer
> - Research-informed Practice
> - Instructional Quality

> [!WARNING]
> **Frozen Systems (HTML, CSS, Design, Copy, Metadata, Scope)**
> - **Approved Narrative**: Do not rewrite approved narrative sections. Do not paraphrase. Do not shorten. Only modify wording when a factual error exists or explicitly requested. *If wording changes are proposed, quote: old text, new text, reason, supporting evidence.*
> - **Metadata Freeze**: Metadata may be updated only when correcting factual errors or improving technical compliance (canonical URLs, structured data validation, deployment fixes).
> - **Repository Scope**: Only modify files necessary for the approved fix. Do not edit `archive/`, `docs/`, `scratch/`, or historical versions.
> - **Project Meridian Design Language**: Section order, component architecture, design tokens, and interaction models are frozen. Refinement of implementation is allowed so long as it adheres to the established design language.
> - **HTML/CSS Architecture**: Do not rename IDs/variables or merge/split CSS files. Do not move/add/remove semantic sections (harmless presentation wrappers `<div>` for responsive alignment are permitted).

> [!IMPORTANT]
> **No Scope Expansion**
> While implementing an approved objective, newly discovered issues must be documented but not corrected unless they fall within the current approved objective or receive separate approval.

> [!IMPORTANT]
> **Evidence & Severity Rule**
> Every recommendation must contain: `Issue` -> `Evidence` -> `Proposed Fix` -> `Expected Benefit`.
> Severity Actions:
> - **Critical** (Technical, Professional, Accessibility) → Blocks all further execution.
> - **High** (Must fix before application season) → Must be resolved before production release.
> - **Medium** (Should fix) → May be deferred with user approval.
> - **Low** (Optional polish) → Optional polish. Never blocks release.

> [!IMPORTANT]
> **Git Safety & Visual Regression Rule**
> Before any production modification, create a checkpoint commit. Apply one logical change at a time and validate.
> - **Visual Regression**: Every approved CSS change must demonstrate before/after desktop/tablet/mobile. No unrelated visual differences are acceptable.
> - **Rollback**: If validation or visual regression fails, revert the last logical change, document the failure in the Rollback Log (Date, Commit hash, Files affected, Reason, Validation failure, Resolution), and stop execution.

## Execution Authority

> [!CAUTION]
> No execution may begin until all of the following are true:
> - The requested objective has been explicitly approved by the user.
> - The objective falls within the current execution budget.
> - No blocking condition is active.
> - The Release Gate requirements have been satisfied.
> The AI must never interpret silence, implied intent, or previous discussions as approval to execute changes.

## Execution Sequence

### Blocking Condition

> [!CAUTION]
> If the Professional Truth Audit identifies any factual inconsistency across public materials, or specifically regarding:
> - **WhiteHat Jr title**: Assistant Manager – Teacher Quality & Development
> - **Teaching progression**: Mumbai → Shenzhen (high school) → Huzhou (middle school then kindergarten) → Zhengzhou (primary)
> - **Current positioning**: International Primary Educator, EAL/Multilingual Specialist, STEM-through-English Practitioner, Teacher Trainer, Research-Informed Educator
> - **Education chronology**: B.Ed. (2022–2024)
> 
> **STOP immediately.** Do not proceed to any visual or CSS work. Produce the inconsistency report and wait for approval.

---

### Phase 1: Pre-Execution Audits & Reports (Reports Only)

**Report Completion Criteria:**
A report is considered complete only when:
- All required sections have been reviewed.
- Every finding has a severity classification.
- Evidence is cited for every finding.
- No assumptions remain unresolved.

**1A. Professional Truth Audit (Report A: Hard Facts)**
Verify across Portfolio, CV, LinkedIn, GitHub, PGCE, and Teaching Portfolio: Full name, Headline, Job titles, Employers, Dates, Locations, Teaching phases, Subjects, Qualifications, Certification names, Institutions, Graduation dates, Contact info, and URLs (LinkedIn, GitHub, Portfolio, CV download). Output every inconsistency in a table.

**1B. Professional Truth Audit (Report B: Professional Narrative)**
Verify professional positioning is identical across all metadata, profiles, and copy. Ensure positioning strictly aligns with the blocking condition parameters.

**2. Evidence Hierarchy Audit**
Classify claims: L1 (Documentary), L2 (Quantifiable), L3 (Demonstrated Practice), L4 (Personal Philosophy), L5 (Aspirational positioning e.g. "Passionate educator"). Aspirational positioning should appear sparingly and never outweigh documentary evidence. No section should rely primarily on L4/L5 when L1-3 evidence exists elsewhere. Recommend moving evidence closer to claims.

**3. Recruiter Psychology & Conversion Audit**
Assume the reviewer is a Head of School, Principal, HR Recruiter, and Academic Director. Utilize the **Recruiter Scorecard** (require: `score`, `rationale`, `supporting evidence`, `risk if unchanged`): `Trust`, `Authority`, `Leadership`, `Evidence`, `Readability`, `Professionalism`, `Visual Quality`, `Recruiter Conversion`.

**4. Content Quality & Professional Writing Audit**
Verify consistent tense, first-person voice, terminology, abbreviations, punctuation style, capitalization, date formats, and strict adherence to **British English**.

**5. Design Drift & CSS Cleanup Report**
Identify where the portfolio violates its own design language (radii, weights, containers). Identify dead CSS, unused utilities, and duplicated selectors without removing anything. Identification of unused CSS does not imply approval for removal.

---

### Release Gate

> [!IMPORTANT]
> Phase 2 may begin only if:
> - Professional Truth Audit complete
> - No unresolved Critical findings
> - User approval recorded
> - Checkpoint commit created
> - Working tree contains no unrelated or uncommitted changes except the approved execution objective
> - Validation passed

---

### Phase 2: Execution

> [!CAUTION]
> **Execution Budget**
> Each execution cycle is limited to ONE approved objective (e.g., Professional Truth corrections only, CSS spacing only). Do not combine multiple objectives into one execution cycle unless explicitly approved.
> After completing one objective: 1) Validate, 2) Commit, 3) Report, 4) Wait for approval.

**6. Approve Fixes**
Only fixes explicitly approved by you will move to execution.

**7. Apply Approved Refinements & Documentation**
Apply the fixes incrementally, utilizing the Git Safety & Visual Regression Rules.
Maintain a `decision_log.md` recording every user-approved decision (Date, Decision, Reason, Approved by User, Files affected, Status). Future execution must follow the Decision Log.
Maintain a **Design Exception Register**: Whenever someone intentionally overrides governance, record (Exception ID, Date, Reason, Approved by, Scope, Files affected, Temporary/Permanent).

**8. Final QA**
Execute the massive pre-flight checklist:
- `[ ]` Core Web Vitals: CLS < 0.1, LCP < 2.5 s, INP < 200 ms
- `[ ]` Lighthouse ≥95, HTML validation, Accessibility, Keyboard navigation, Console clean, No 404s, Broken image scan, Font loading verification, Cross-browser testing (Chrome, Edge, Safari, Firefox)
- `[ ]` Internal anchors & External links, PDF downloads, Contact links, WeChat QR, LinkedIn, GitHub, Download CV
- `[ ]` Mobile, Tablet, Desktop, Print stylesheet
- `[ ]` GitHub Pages deployment
- `[ ]` Canonical URL, robots.txt, sitemap.xml, Structured data, OpenGraph, Twitter cards, Manifest, Favicon

**9. Production Release Summary**
Output the final summary: `Version`, `Commit hash`, `Date`, `Files changed`, `Rollback availability`, `Remaining known issues`, `Production readiness score`, Critical/High/Medium findings resolved.

---

## Governance Freeze

> [!IMPORTANT]
> Once this document is approved, it becomes the governing specification for the Production Polish phase. Do not modify this governance document during execution unless a critical omission is discovered or the user explicitly requests a governance change. All further work must follow this document exactly.

## User Review Required

**Awaiting approval. No reports will be generated and no files will be modified until approval is explicitly given.**
