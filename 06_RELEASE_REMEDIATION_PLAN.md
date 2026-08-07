# Release Remediation & Target Architecture (Phase 6)

## 1. Goal Description

This engineering design document outlines the target architecture and migration strategy to resolve the systemic flaw identified in the reproducibility audit. 

**Current Flaw:** The repository has one governed source of truth (`career-data/facts/`) but two downstream assets (`compiled_assets/` and `mo-portfolio-v2/`) whose synchronization with that source is not demonstrated by in-repository automation. 

**Target State:** Establish a single, end-to-end reproducible pipeline where a clean checkout and a single build command deterministically produce both the compiled CV assets and the deployable web portfolio from the canonical facts. The build outputs will be strictly isolated from the deployment payload, and all unsupported directories will undergo dependency verification before deprecation.

> [!IMPORTANT]
> ## User Review Required
> This document has been revised based on your architectural feedback. It defers irreversible actions (like deletion) until dependency verification and reproducibility are demonstrated. Please review the updated 8-phase migration sequence.

---

## 2. Target Architecture

The target architecture introduces a dedicated `build/` directory to eliminate ambiguity between generated artifacts, the deployment payload, and canonical data. Every edge in the build graph will have exactly one producer.

```text
career-data/facts/ (Canonical Facts)
    ↓
scripts/ (Validation & Graph Resolution)
    ↓
build/intermediate/ (Intermediate Data)
    ↓
build/view_models/ (Canonical View Model - pending coverage analysis)
    ↓
Renderers
    ├── Markdown (artifacts/generated/cv.md)
    ├── Recruiter Pack
    ├── Portfolio 
    └── Release Manifest
    ↓
build/release/ (Release Assembler)
    ↓
deploy/portfolio/ (Deployment Payload - e.g., mo-portfolio-v2)
    ↓
GitLab Pages
```

---

## 3. Migration Sequence (8 Phases)

To ensure maximum safety and evidence-backed changes, the migration will follow this strict sequence.

### Phase 0: Dependency Verification
Before any code is changed, we will formally verify the producer and consumer of every directory.
* Map all dependencies for `compiled_assets`, `recruiter_packs`, `computed`, `golden`, and `view_models`.
* Categorize every directory with verified evidence. Nothing moves forward until this matrix is complete.

### Phase 1: Build Graph Documentation
* Formally document the exact dependency graph from `facts.yml` down to all expected outputs.
* Explicitly define the inputs and outputs for every step.

### Phase 2: Single Canonical View Model
* Perform a coverage analysis on `artifacts/professional_profile_vm.json`.
* Prove that this JSON contains everything required to generate the HTML portfolio, CV, LinkedIn, and certificates.
* If it lacks data, extend `build_view_models.py` until the single view model has 100% coverage of all downstream needs.

### Phase 3: Refactor Generators
* Refactor `build.py` (and any new portfolio generator) to consume the single canonical view model from Phase 2.
* Reroute all generator outputs into isolated subdirectories within the new `build/` directory (e.g., `build/rendered/`).
* Do **not** overwrite `mo-portfolio-v2/index.html` during this phase.

### Phase 4: Release Assembler
* Introduce a release assembler script that copies the fully rendered assets from `build/rendered/` into a pristine deployment directory (`deploy/portfolio/`).
* Compare the output of the release assembler against the legacy `mo-portfolio-v2/` directory to ensure identical rendering, Lighthouse scores, and accessibility.

### Phase 5: Determinism Proof
* Update `prove_determinism.py` to run the entire pipeline end-to-end.
* Prove mathematically (via hashing) that running the pipeline twice produces bit-for-bit identical deployment payloads in `deploy/portfolio/`.

### Phase 6: Deprecate Legacy Assets
* Once reproducibility is proven, formally deprecate `mo-portfolio-v2/`, `compiled_assets/`, and the manual `templates/cv/profiles/*.json`.
* Issue a final release snapshot of the legacy state.

### Phase 7: Delete Obsolete Assets
* Delete the deprecated directories (only after Phase 6 is complete and the new deployment payload is live).
* Remove any unsupported directories (`career-data/computed/`, `career-data/view_models/`, `recruiter_packs/`) that were proven obsolete in Phase 0.

---

## 4. Verification Plan

### Automated Tests
* The pipeline will be fully executed via `scripts/ci_pipeline.py`.
* `prove_determinism.py` must pass on the new `deploy/portfolio/` directory.

### Manual Verification
* The assembled `deploy/portfolio/index.html` will be audited against the legacy `mo-portfolio-v2/index.html` for visual parity, SEO parity, and Lighthouse performance parity before the legacy files are deleted.
