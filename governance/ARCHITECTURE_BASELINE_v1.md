# Career OS v4.0 — Architecture Baseline v1.0
*Status: FROZEN*
*Date: 2026-07-30*

This document serves as the canonical record of the architecture freeze for Career OS v4.0. No further structural changes are permitted to the data model or processing pipeline without a formal Decision Log entry.

## 1. The Pipeline
The system enforces a strict, unidirectional data flow that guarantees reproducibility and separation of concerns.

**Canonical Facts (YAML)**
↓
**Relationship Graph (`edges.yml`)**
↓
**Resolver (`scripts/resolve_graph.py`)** -> *Outputs `resolved_graph.json`*
↓
**Semantic Validator (`scripts/validate_semantics.py`)**
↓
**Metrics Engine (`scripts/metrics_engine.py`)**
↓
**Intermediate Compiler (`scripts/compile_intermediate.py`)** -> *Outputs `facts.json`, `timeline.json`, etc.*
↓
**Policy Engine (`scripts/policy_engine.py`)**
↓
**View Model Builder (`scripts/build_view_models.py`)** -> *Outputs `recruiter_view.json`, etc.*
↓
**Generators (`scripts/generate_recruiter_pack.py`)**
↓
**Final Outputs (`RECRUITER_PACK.md`, etc.)**

## 2. Core Architectural Rules

1. **Immutable IDs:** All entities are identified by a 4-digit ID prefix (e.g., `EMP-0001`). No UUIDs are used to prevent dual-identity issues.
2. **Canonical Intermediate Graph:** The output of the Resolver (`resolved_graph.json`) is an **immutable contract** and the *only* supported interface consumed by downstream engines. Downstream systems must never read raw YAML files.
3. **Generated Registry:** The `id_registry.yml` is an auto-generated build artifact (`governance/id_registry.yml`), not a manually maintained file. The only authoritative IDs exist inside the YAML entities.
4. **Data Provenance:** Every generated JSON artifact includes expanded versioning metadata, and every build emits a `build_manifest.json` containing the build ID, commit, versions, timestamps, and hashes. Outputs (JSONs, markdown, recruiter packs) are **never frozen** and regenerate every build. Only schemas, graph contracts, and resolver outputs are frozen.
5. **Orthogonal Governance:** `confidence` (`[verified, supported, plausible, asserted]`) is strictly decoupled from `review_status` (`[approved, pending, conflict, obsolete]`).
6. **Declarative Metrics Engine:** Metrics are modeled as first-class entities with immutable IDs, derived declaratively. The Metrics engine **must never read raw facts**; it exclusively consumes `resolved_graph.json`.
7. **Semantic Claims:** Claims (`CLAIM-XXXX`) are purely semantic objects that depend only on metrics, competencies, and relationships, never directly on raw facts.
8. **View Model Purity:** View models contain **zero business logic**. They only rename, flatten, sort, format, and combine data. Policy (hiding sensitive info, selecting target audiences) belongs exclusively to the Policy Engine.

## Risk Register

| Risk ID | Title | Probability | Impact | Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| **R-007** | **Over-normalization** | Medium | Medium | No entity exists unless consumed by at least one downstream generator. Do not turn intrinsic event properties (like degree names) into relationships. |
| **R-008** | **Policy creep** | Medium | High | Business logic prohibited outside Policy Engine. Generators and View Models must remain "dumb" presenters of the data they are fed. |

## 3. Governance
From this point forward, Phase 3.1+ (Data Population) proceeds sequentially.
**MIGRATION RULE:** Every entity class (Organisation, Role, Employment, Education, etc.) must be migrated, validated, committed, and regression-tested **one at a time**.
Any required modifications to the schemas, enumerations, or pipeline stages documented above must be proposed, reviewed, and recorded as a formal `D-XXX` entry in `governance/DECISION_LOG.md`.
