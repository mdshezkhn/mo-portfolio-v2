# Renderer Consumer Contracts

## Overview
This document formally defines the data requirements for every renderer in the pipeline. These contracts establish exactly what data each consumer requires from the View Model layer. 

Any schema serving these consumers MUST satisfy these contracts completely, without forcing the renderer to open raw YAML facts or manual JSON overrides.

---

## Consumer 1: HTML CV Generator (`build.py`)

### Input Requirement: `CVViewModel`
**Constraints:**
- Dates must be pre-formatted concatenated strings (e.g., "Feb 2024 – Present"), not objects.
- Summaries must be a single string paragraph.
- Requires explicit presentation layout markers (e.g., subtitles, asset names).

**Required Fields:**
```json
{
  "profile": {
    "title": "string (e.g., Master)",
    "asset_name": "string (e.g., CV_Master_v3.0)",
    "subtitle": "string",
    "summary": "string"
  },
  "competencies": ["string"],
  "claims": ["string (IDs)"],
  "experience": [
    {
      "company": "string",
      "date": "string (formatted)",
      "title": "string",
      "bullets": ["string"]
    }
  ],
  "education": ["string (formatted block)"]
}
```

---

## Consumer 2: Markdown CV Generator (`render_markdown.py`)

### Input Requirement: `MarkdownViewModel`
**Constraints:**
- Agnostic to complex HTML layout properties.
- Expects raw highlight lists for bullet generation.

**Required Fields:**
```json
{
  "candidate": {
    "name": "string",
    "title": "string"
  },
  "executive_summary": ["string"],
  "key_claims": ["string"],
  "experience": [
    {
      "id": "string",
      "title": "string",
      "organization": "string",
      "start_date": "string (YYYY-MM)",
      "end_date": "string (YYYY-MM or Present)",
      "highlights": ["string"]
    }
  ],
  "education": [
    {
      "id": "string",
      "name": "string",
      "institution": "string",
      "year": "string or null"
    }
  ]
}
```

---

## Consumer 3: Web Portfolio Builder (`build_portfolio.py` - Target)

### Input Requirement: `PortfolioViewModel`
**Constraints:**
- Must include SEO metadata and theme configuration.
- Requires asset links (images, certificates).

**Required Fields:**
```json
{
  "seo": {
    "page_title": "string",
    "meta_description": "string",
    "canonical_url": "string"
  },
  "hero": {
    "greeting": "string",
    "headline": "string",
    "subheadline": "string"
  },
  "competencies": [
    {
      "category": "string",
      "skills": ["string"]
    }
  ],
  "experience_timeline": [
    {
      "organization": "string",
      "role": "string",
      "duration": "string",
      "description": "string",
      "logo_url": "string (optional)"
    }
  ],
  "certifications_gallery": [
    {
      "name": "string",
      "issuer": "string",
      "image_url": "string",
      "evidence_id": "string"
    }
  ]
}
```

---

## Consumer 4: Recruiter Pack Generator (`generate_recruiter_pack.py`)

### Input Requirement: `RecruiterViewModel`
**Constraints:**
- Must expose raw evidence IDs for ATS parsing.
- Must include operational region and physical country context.
- Must include internal confidence scores for vetting.

**Required Fields:**
```json
{
  "candidate_name": "string",
  "professional_title": "string",
  "employment_history": [
    {
      "organization": "string",
      "role": "string",
      "physical_country": "string",
      "operational_regions": ["string"],
      "verified_evidence_id": "string",
      "confidence_score": "string"
    }
  ],
  "verified_qualifications": [
    {
      "name": "string",
      "evidence_id": "string",
      "confidence_score": "string"
    }
  ]
}
```
