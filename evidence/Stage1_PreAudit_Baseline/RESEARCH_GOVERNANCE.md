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
