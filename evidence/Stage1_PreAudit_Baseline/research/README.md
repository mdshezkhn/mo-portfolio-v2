# PGCE Practitioner Research Evidence System

## Overview

This directory contains the normalized, production-quality evidence system for the PGCE7002 practitioner research project. All content is derived from the original 12-phase evidence reports, with duplication eliminated and cross-referencing implemented.

## Architecture

```
evidence/
├── AUDIT_REPORT.md              # Phase 1: Audit of original files
├── research/                    # Phase 2: Master evidence model
│   ├── README.md                # This file
│   ├── research_metadata.md     # Research metadata (canonical source)
│   ├── findings.md              # All findings (canonical source)
│   ├── evidence_register.md     # Evidence register
│   ├── quantitative_results.md  # Quantitative data (canonical source)
│   ├── qualitative_results.md   # Qualitative data (canonical source)
│   ├── competencies.md          # Professional competencies (canonical source)
│   ├── impact_register.md       # Impact assessment (canonical source)
│   ├── recruiter_translation.md # Multi-audience translations
│   ├── interview_bank.md        # STAR stories for interviews
│   ├── portfolio_case_study.md  # Portfolio-ready case study
│   ├── linkedin_assets.md       # LinkedIn content
│   ├── cv_assets.md             # CV-ready content
│   └── overclaim_register.md    # Overclaim warnings
├── CANONICAL_RESEARCH_SPECIFICATION.md  # Master specification
├── TRACEABILITY_MATRIX.md       # Claim-to-source traceability
├── KNOWLEDGE_GRAPH.md           # Mermaid diagrams
├── research.json                # Machine-readable data
├── snippets/                    # Reusable modular snippets
├── QA_REPORT.md                 # Quality assurance report
└── RESEARCH_GOVERNANCE.md       # Governance framework
```

## Design Principles

1. **DRY (Don't Repeat Yourself)**: Each fact stored once, referenced everywhere
2. **Single Source of Truth**: Canonical files hold authoritative content
3. **Cross-Referencing**: Derived works link back to canonical sources
4. **Machine-Readable**: JSON format enables programmatic access
5. **Traceability**: Every claim links to its verification source
6. **Modularity**: Snippets enable reuse across contexts

## Canonical Sources

The following files are canonical sources — all other content derives from them:

- `research/research_metadata.md` — Research metadata
- `research/findings.md` — All findings
- `research/quantitative_results.md` — Quantitative data
- `research/qualitative_results.md` — Qualitative data
- `research/competencies.md` — Professional competencies
- `research/impact_register.md` — Impact assessment

## Derived Outputs

These files reference canonical sources rather than duplicating content:

- `research/recruiter_translation.md`
- `research/interview_bank.md`
- `research/portfolio_case_study.md`
- `research/linkedin_assets.md`
- `research/cv_assets.md`

## Usage

To generate a CV bullet, LinkedIn post, or interview answer:
1. Query `research.json` for relevant evidence
2. Reference the canonical source file for full context
3. Apply the appropriate translation from `recruiter_translation.md`

## Versioning

All files use semantic versioning. See `RESEARCH_GOVERNANCE.md` for update process.