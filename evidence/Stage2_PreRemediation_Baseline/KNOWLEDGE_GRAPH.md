# Knowledge Graph - PGCE7002 Practitioner Research

This document illustrates the structural relationships between the raw evidence, the canonical research library, and the public assets generated for the portfolio.

## 1. Evidence Hierarchy

```mermaid
graph TD
    A[Absolute Truth] --> B[Canonical Markdown]
    B --> C[Machine Readable JSON]
    B --> D[Derived Snippets]
    D --> E[Public Assets]

    A1(PGCE Essay.pdf) --> A
    A2(Research Data.xlsx) --> A
    A3(Phase 1-12 Reports) --> A

    B1(findings.md) --> B
    B2(competencies.md) --> B
    B3(quantitative_results.md) --> B

    C1(research.json) --> C

    D1(cv_snippets.md) --> D
    D2(linkedin_snippets.md) --> D
    D3(interview_snippets.md) --> D
```

## 2. Research Findings to Competencies

```mermaid
graph LR
    F1[Finding 1: Belief-Practice Gap] --> C3[Pedagogical Evaluation]
    F2[Finding 2: Participation Filter] --> C7[Student-Centred Practice]
    F3[Finding 3: BICS-CALP Conflict] --> C4[Evidence-Informed Teaching]
    F4[Finding 4: Framework Absence] --> C1[Professional Inquiry]
    F5[Finding 5: Practice Change] --> C2[Reflective Practice]
    F7[Finding 7: Methodological Rigour] --> C5[Data Analysis]
```

## 3. Public Asset Generation

```mermaid
graph TD
    S1[CV Snippets] --> P1[World-Class CV]
    S2[LinkedIn Snippets] --> P2[Optimized LinkedIn Profile]
    S3[Portfolio Snippets] --> P3[Digital Portfolio Website]
    S4[Interview Snippets] --> P4[STAR Interview Bank]

    F(Verified Findings) --> S1
    F --> S2
    F --> S3
    F --> S4
```
