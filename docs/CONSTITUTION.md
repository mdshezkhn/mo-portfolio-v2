# Portfolio Content Compilation Pipeline Roadmap (The Constitution)

**Architecture Status:** Compiler Core Version 1.0 (Frozen)

This document serves as the project's constitution, transitioning the portfolio from an evolving collection of scripts into a robust **content compilation pipeline**—a canonical knowledge base that emits highly reliable, versioned, recruiter-facing artifacts.

## Strategic Philosophy

Every new feature must answer one question:
> **Will this measurably improve recruiter-facing artifacts, or does it primarily make the compiler more elaborate?**

If it does not improve reliability, traceability, or the quality of generated outputs, it is complexity that will be deferred. The highest-value work is proving that the pipeline consistently produces recruiter-facing outputs that are accurate, traceable, and persuasive.

## Glossary

| Term | Definition |
| :--- | :--- |
| **Canonical Fact** | Human-authored immutable data (e.g., "Employment began 2018-07"). |
| **Relationship** | Typed edge between canonical entities. |
| **Resolver** | Builds the canonical graph. |
| **Intermediate** | Generator-independent compiled representation. |
| **Policy** | Rule set determining visibility and filtering, driven by configuration. |
| **View Model** | Presentation-specific semantic projection (e.g. Professional Profile). |
| **Renderer** | Pure logic-less function turning a View Model into a rendered document (e.g. Markdown). |

## Core Architectural Invariants (Enforced via Architecture Tests)

> **Governance Rule:** The architecture is frozen at Version 1.0. No architectural invariant defined in this constitution may be violated without an approved Architecture Decision Record (ADR) demonstrating clear recruiter benefit.

**1. The Fundamental Pipeline**
> **Every downstream layer depends only on the layer immediately preceding it. Reverse dependencies are prohibited.**
> `Facts → Relationships → Resolver → Claims → Metrics → Selection → Policy → View Models → Generators`

**2. Component Rules**
* `Resolver:` The Resolver is the exclusive ingestion boundary for canonical data. It enforces the explicit **Canonical Schema Version** (e.g., `Canonical Schema v1.0`) and refuses to process incompatible schemas.
* `Claims Register:` First-class entities representing recruiter messaging. Confidence is computed based on evidence count and verification level, never hardcoded.
* `Metrics Engine:` Metrics operate exclusively on the resolved graph and claim space.
* `Selection Engine:` Given a target market, recruiter persona, and policy priorities, selects the optimal subset of claims. Generators must never choose content.
* `Policy Engine:` The Policy Engine is configuration-driven. It evaluates external policy definitions (`market_rules.yml`, etc.) and **must not contain hard-coded domain rules**. It is pure (no file I/O outside loading config) and never reads the Resolver.
* `View Models:` View Models are immutable presentation projections with no business logic. Every View Model must satisfy its schema completely before reaching any Generator.
* `Generators:` Generators are pure functions from View Model → Artifact.

**3. Generator Dependency Isolation**
```
Generator input:
    View Model

Generator output:
    Artifact

Generator may not read:
    YAML
    Resolver
    Intermediate
    Metrics
```

Generators must guarantee:
* No mutation
* No side effects
* No hidden state
* No randomness
* Stable ordering (e.g., dictionary key sorting) to preserve determinism.

**4. Reproducibility Definition:**
Given the same repository commit, same canonical data, same configuration, and same generator version, all generated artifact payloads must be **byte-identical** (excluding build metadata like `generated_at`).

## 1. Pipelines & Testing

### 1.1 CI/CD Build & Validation Pipeline

Every commit will automatically execute the following pipeline. If any structural stage fails with a non-zero exit code (`exit 1`), the merge will be blocked. Failures must be actionable, emitting: `Severity`, `Component`, `Entity`, `Location`, and `Suggested Fix`.

1. `build_id_registry`
2. `validate_yaml`
3. `resolve_graph`
4. `validate_semantics`
5. `metrics_engine`
6. `compile_intermediate`
7. `policy_engine`
8. `build_view_models`
9. `generator_smoke_tests`
10. `regression_tests`

### 1.2 Test Pyramid
Architecture must distinguish tests strictly into:
`Unit → Component → Integration → Generator → Regression`

### 1.3 Release Pipeline
Release is distinct from the CI/CD build pipeline to enable staged releases. The flow is:
`Developer Commit → Build Pipeline → Validation Pipeline → Artifact Generation → Regression Verification → Release Candidate → Human Approval → Release Pipeline → Deployment`

## 2. Failure Classification

Pipeline validations are strictly categorized to keep the pipeline rigorous without being brittle.

**Structural Failures (Build MUST Fail):**
* Invalid YAML
* Duplicate IDs
* Broken graph references
* Schema violations
* Cyclic dependencies (where prohibited)

**Semantic Warnings (May pass depending on policy):**
* Missing evidence
* Pending verification
* Optional narratives
* Recruiter-pack completeness below target

## 3. Data Lineage & Traceability

Every generated recruiter-facing statement must be strictly traceable down to the specific entity IDs.

**Lineage Granularity:** Every sentence appearing in a generated artifact must explicitly trace back to:
* Canonical Facts (e.g. `Fact E-3002`)
* Canonical Narratives
* Specific Relationships (e.g. `Relationship R-52`)
* Computed Metrics (e.g. `Metric M-18`)
* Policy Evaluation (e.g. `Policy P-4`)

Nothing should be generated from undocumented assumptions.

## 4. Classifications & Vocabularies

### Relationship Governance
All relationship types are centrally registered in a controlled taxonomy. New relationship types require schema review and semantic validation before use.

### Metrics Classification
Metrics are strictly classified to avoid mixing objective facts with opinionated scoring:
* **Derived:** Computations (e.g., "11.4 years experience")
* **Aggregate:** Summaries (e.g., "Number of leadership roles")
* **Analytical:** Trends or statistical measurements
* **Compatibility:** Alignment against external standards
* **Quality:** Completeness or strength of the profile

### Policy Precedence
When policies conflict, the following strict precedence hierarchy determines the outcome:
`Global → Market → Employer → Generator`

### Evidence Status
Evidence availability is not binary. It must be distinguished as:
`Available`, `Verified`, `Pending`, `Missing`, `Expired`, or `Superseded`.

## 5. Artifact Versioning & Manifests

### Artifact Approval Lifecycle
Artifacts do not automatically become "Golden" simply by being generated. They must pass through strict lifecycle states:
`Generated → Reviewed → Approved → Golden`

Only explicitly Approved artifacts are stored in `golden/` to serve as the benchmark for future regression testing.

Every generated artifact will embed traceability metadata to ensure debugging is straightforward. 
Build metadata must be cleanly separated from the artifact payload to preserve reproducibility testing.

**Build Manifest (`build_manifest.json`)**
The pipeline will emit a central build manifest containing:
* Resolver Version
* Schema Version
* Policy Version
* Generator Versions
* Input Hashes
* Output Hashes
* Warnings
* Performance Execution times

## 6. Interface Contracts & Evolution

### Contract Versioning
Rather than freezing files, the following **contracts and interfaces** will be strictly frozen.
* **Resolver output contract:** The canonical graph.
* **Relationship vocabulary:** Governed taxonomy.
* **Intermediate JSON schema:** Intermediate representations are immutable products of compilation and may never be edited manually.
* **View Model schema:** Immutable projections.
* **Policy API:** Evaluator schema.

Version numbers for these contracts will change according to strict semantic rules:
| Change | Version |
| :--- | :--- |
| Bug fix, no contract change | Patch (1.0.1) |
| Backward-compatible interface addition | Minor (1.1.0) |
| Breaking interface change | Major (2.0.0) |

**Compatibility Guarantees:**
For each contract, semantic versioning must be backed by explicit compatibility guarantees defining:
* Required fields
* Optional fields
* Deprecated fields (with removal policy, e.g., "remove in v2")
* Forbidden properties (e.g., "no direct YAML payloads")

### Evolution Policy
When introducing new entity types, the expansion must follow this exact path:
`New entity type` → `Schema` → `Reference taxonomy` → `Migration` → `Resolver` → `Semantic validation` → `Metrics` → `Intermediate` → `View model` → `Generator` → `Regression test` → `Documentation`

### ADR Process
Foundational architectural decisions will be recorded as Architecture Decision Records (e.g., `ADR-001 Resolver Architecture`). Routine implementation choices remain in a standard decision log.

## 7. Implementation Stages

### Stage 1: Foundation & Early Integration
* Stand up CI/CD pipeline structure and ADR process
* Define Interface contracts and Quality Targets
* Migrate `Employment`, `Education`, and `Certification`
* **Integration Milestone:** Generate `BRITISH_CURRICULUM` recruiter pack.
  * *Critical Review Phase:* Stop feature work. Evaluate output as a Head of School (Would I interview? Supported claims? Missing info? Narrative coherence?). If compelling, shift focus to content quality over infrastructure.

### Stage 2: Graph Expansion & Competencies
* Migrate `Competencies`, `Claims`, and `Governance Registers`

### Stage 3: Evidence & Narratives
* Ensure `Evidence Availability`
* `Narrative authoring` (Consuming the mature graph)

## 8. Risk Register

| ID | Risk | Probability | Impact | Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| **R-007** | **Over-normalization** | Medium | Medium | No entity exists unless consumed by at least one downstream generator. |
| **R-008** | **Policy creep** | Medium | High | Business logic prohibited outside Policy Engine; Engine merely evaluates external YML rules. |
| **R-009** | **Canonical Drift** | Medium | High | "Canonical wins." Disagreements are resolved by correcting the canonical source. |
| **R-010** | **Schema Explosion** | High | Medium | An entity type is only permitted if it is strictly consumed downstream. |
| **R-011** | **Generator Divergence** | High | High | Generators are strictly prohibited from holding business logic; shared View Models only. |

## 9. Project Success Criteria

The system's success is defined by strict regression tests proving single-source-of-truth reliability.

**Acceptance Tests for Success:**
* One canonical employment correction automatically and accurately updates the Portfolio, CV, Recruiter Pack, and LinkedIn without manual edits.
* Every recruiter-facing artifact is fully generated from canonical data (0% manual assembly).
* Recruiter artifacts remain internally consistent across rendering targets.
* A single fact change automatically propagates correctly to all downstream outputs.
* Two independent builds from identical inputs produce byte-identical artifacts.

## User Review Required

> [!IMPORTANT]
> The final 15 v1.0 requirements have been strictly integrated (Canonical versioning, vocabulary governance, metrics classification, policy precedence, granular provenance, build manifest, test pyramid, error philosophy, and tightened linguistic invariants). Please review this ultimate constitution.

---

## 10. v1.0 Operational Doctrine

The architecture is formally frozen at v1.0. The operational focus shifts entirely to populating evidence, generating real-world artifacts, validating externally, and launching application campaigns.

### 10.1 Product Change Governance
Every change to the system post-v1.0 must record:
* **Problem:** What real-world issue prompted it?
* **Evidence:** Recruiter feedback, audit finding, application outcome, etc.
* **Change:** The exact layer modified (Canonical data, policy, claim, renderer).
* **Expected outcome:** The measurable improvement.
* **Verification:** How the improvement will be measured.
*(Note: v1.0 is stable, but not immune to evidence. If operational data proves an interface or policy is hurting outcomes, an ADR will be used to deliberately evolve the architecture.)*

### 10.2 Feedback Separation
Feedback must be strictly categorized:
* **Objective Defects:** Inconsistent dates, missing qualifications, unsupported claims. (Actionable compiler changes).
* **Subjective Preferences:** Style preferences, length tweaks, visual hierarchy. (Treated as market signals, rarely driving immediate architecture changes).

### 10.3 Stable Benchmarks
A fixed Golden benchmark artifact must be maintained to objectively compare new versions against baseline metrics (Readability, Evidence coverage, Recruiter scores, Consistency).

### 10.4 Outcome-Driven Metrics
Internal engineering metrics are replaced by operational outcome metrics:
* Recruiter response rate (Primary)
* Interview invitation rate
* Time to generate a tailored application
* Manual edits after generation (Target: Near zero)
* Defects per validation cycle

### 10.5 Core Principles for Season 1
1. **Evidence First:** The compiler should only become more persuasive because the underlying evidence becomes stronger, not because the wording becomes more aggressive. Prefer adding one new verified piece of evidence over rewriting ten existing claims.
2. **Outcome Before Optimization:** No optimization should be accepted without demonstrating an improvement in an external metric. (e.g., A new selection policy is only accepted if it increases interview rates or reviewer scores).
3. **The Right to Falsify:** The maintainers commit to accepting evidence that contradicts the project's assumptions, even when that evidence suggests the compiler should be simplified or specific features should be removed.

### 10.6 Future Architectural Enhancements (v1.1)
* **Evidence Confidence Model:** A future enhancement to distinguish evidence quality (e.g., E1: Official Document to E5: Aspirational). This will only be implemented if operational data proves that granular confidence scoring actively improves claim selection and recruiter outcomes.

## 11. Release Governance & Promotion Criteria

To ensure pipeline stability and integrity, promotion of any Release Candidate (e.g., `v2.0.0-rc1`) to a stable release (e.g., `v2.0.0`) must meet explicit, measurable criteria. Subjective or ambiguous criteria (such as "evaluation periods") are not permitted.

### Required (Blockers)
Promotion is strictly blocked unless the following objective criteria are met:
* Clean checkout build passes.
* GitHub Actions pipeline passes in a target-independent environment (pinned OS and tooling).
* All contract, schema, semantic, and structural regression tests pass.
* No release-blocking issues remain.
* Release notes completed.

### Additional Confidence (Advisory)
The following criteria provide additional confidence or verify quality outside the core automation:
* Multiple successful CI runs after the release candidate (e.g., 10 consecutive passes if code changes continue).
* Manual visual verification on Chrome.
* Manual visual verification on Firefox.
