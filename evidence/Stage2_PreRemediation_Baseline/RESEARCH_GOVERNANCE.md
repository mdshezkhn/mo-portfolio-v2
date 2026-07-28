# Research Governance

This document establishes the immutable laws of the PGCE Practitioner Research Evidence System.

## The Prime Directive

> **No derived artifact may introduce a fact that is absent from the canonical research library.**

This means:
1. No CV inflation.
2. No LinkedIn embellishment.
3. No Interview inconsistencies.
4. No Recruiter-specific wording that invents evidence.

## Evidence Hierarchy
1. **Absolute Truth**: `PGCE Essay.pdf`, `Research Data.xlsx`, and `Phase1-12.md` reports.
2. **Canonical Markdown**: `evidence/research/*.md` (Frozen and verified against Absolute Truth).
3. **Machine Readable**: `evidence/research.json` (Direct 1:1 map of Canonical Markdown).
4. **Derived Snippets**: `evidence/snippets/*.md` (Strict subsets of Canonical Markdown).
5. **Public Outputs**: Portfolio, CV, LinkedIn (Assembled exclusively from Snippets).

## QA Execution Gates
Every downstream layer must faithfully reflect the upstream layer. If a file is generated, it must be verified immediately for:
- Missing Evidence IDs
- Broken Links
- Duplicate Content
- Unsupported Claims

Fail fast. Correct immediately. Do not propagate errors.

## Evidence Precedence Hierarchy
If two sources conflict, the higher-precedence source governs the canonical repository unless explicitly stated otherwise:
1. **Raw research dataset** (Questionnaire Data / Interview Data worksheets)
2. **Original PGCE essay**
3. **Canonical research files** (`research/*.md`)
4. **Derived assets** (CV, LinkedIn, portfolio, snippets)

## Baseline Preservation Rule
The pre-remediation repository shall be retained as a read-only baseline (e.g., `Stage1_PreAudit_Baseline` or `Stage2_PreRemediation_Baseline`) to enable future forensic comparison.
