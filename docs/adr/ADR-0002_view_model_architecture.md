# ADR 0002: View Model Architecture for Downstream Rendering

## Status
Proposed

## Context
The repository currently maintains canonical facts (`career-data/facts/`) which are transformed into a single `artifacts/professional_profile_vm.json`. This monolithic View Model (VM) was intended to serve as the universal data source for all renderers (Markdown CV, HTML CV, Web Portfolio, Recruiter Pack). 

Phase 2 coverage analysis revealed that this universal VM approach is fundamentally flawed. Different renderers require drastically different data structures and contextual metadata:
* **HTML/Markdown CVs** require layout parameters, page breaks, string-concatenated dates, and specific bullet ordering.
* **Web Portfolios** require SEO metadata, theme configurations, gallery references, and interactive URLs.
* **Recruiter Packs** require ATS metadata, internal confidence scores, and raw evidence links.

Forcing all of this disparate metadata into a single Universal VM creates an oversized, unstable, and highly coupled schema. Changes to the web portfolio's SEO requirements shouldn't break the recruiter pack generation.

## Options Considered

### Option A: The Universal View Model (Monolith)
* **Architecture:** Canonical Facts → Resolved Graph → `professional_profile_vm.json` → All Renderers.
* **Pros:** Single file to inspect, mathematically simple graph.
* **Cons:** The schema becomes heavily polluted with presentation-specific concerns. Renderers must ignore 80% of the payload to find the 20% they need. High risk of breaking changes when one renderer needs a structural update.

### Option B: Renderer-Specific VMs derived from a Profile Domain Model
* **Architecture:** Canonical Facts → Resolved Graph → `profile_domain_model.json` (Intermediate) → [ `cv_vm.json`, `portfolio_vm.json`, `recruiter_vm.json` ] → Specific Renderers.
* **Pros:** The Domain Model remains strictly focused on sanitized, graph-resolved semantic data. The presentation VMs act as "projections" optimized entirely for their respective consumers. Strong isolation between rendering concerns.
* **Cons:** Marginally more complex build graph with more intermediate JSON artifacts.

## Decision
We will adopt **Option B: Renderer-Specific VMs**. 

We will introduce `Phase 2.5: Schema Definition` to formally define JSON Schemas for both the intermediate Domain Model and the specialized VMs. No generator refactoring will occur until these contracts are frozen.

## Consequences
* **Positive:** Complete decoupling of presentation logic from semantic data validation. Renderers become dumb consumers of perfectly tailored JSON.
* **Positive:** Strict schema contracts mean we can catch build failures at the JSON validation stage rather than waiting for a renderer to crash.
* **Negative:** Requires writing and maintaining multiple JSON schemas.

## Next Steps
1. Define the Consumer Contracts for each renderer.
2. Draft the JSON Schema for the `ProfileDomainModel`.
3. Draft the JSON Schemas for the downstream projections (`CVViewModel`, `PortfolioViewModel`).
