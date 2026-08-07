# Canonical Data Specification

## Core Invariant
> **Identity is immutable. Content is mutable.**
> 
> A canonical entity can change its title, description, evidence, and notes over time. It can never change its identity.

## 1. What is an entity?
Entities are divided strictly into two categories:

**Canonical Entities (Persistent):**
The fundamental building blocks of professional identity that persist over time. They are authored by humans and stored in the `career-data/facts/` directory. These are the *only* objects that receive permanent, registry-backed IDs.
- `PERSON`: Identity and biographical facts
- `ORG`: Organizations and institutions
- `EMP`: Employments and engagements
- `QUAL`: Academic qualifications
- `CERT`: Professional certifications
- `COMP`: Competencies and skills
- `EVID`: Verifiable evidence artifacts
- `NARR`: Authored narratives

**Derived Objects (Ephemeral):**
Outputs generated dynamically by the compiler pipeline (e.g., Metrics, View Models, final Artifacts). These do NOT receive permanent IDs in the registry. Their identity is transient and bound strictly to the build execution context.

## 2. How is identity assigned?
Identities are assigned explicitly via the **ID Registry** (`registry/ids.yml`). 
- IDs are opaque, block-reserved keys (e.g., `EMP-2101`).
- The registry maps the opaque ID to a human-readable **slug** (e.g., `aoxin_2018`), which serves as a stable anchor for human authors.
- Fact YAML files reference these IDs but cannot invent or define allocation policy.

## 3. How does an entity evolve?
An entity evolves through explicit lifecycle states defined in the registry:
- **DRAFT**: Entity is proposed but not fully resolved or verified.
- **ALLOCATED**: ID is formally assigned in the registry.
- **VERIFIED**: Entity facts are corroborated by evidence.
- **PUBLISHED**: Entity is approved for inclusion in downstream view models.
- **DEPRECATED**: Entity is superseded by a newer representation (must include `superseded_by`).
- **ARCHIVED**: Entity is retired from active view models but preserved for historical lineage.

## 4. When can an entity be removed?
**Never.** 
- Canonical entities are never physically deleted. 
- If an entity is no longer relevant, it is transitioned to the `DEPRECATED` or `ARCHIVED` state.
- **Rule:** Once retired, an ID may **never** be reassigned.

## 5. How is provenance preserved?
- All changes to identity (allocation, splitting, merging, slug renaming) are recorded as explicit, immutable operation blocks in `migrations/`.
- Downstream derived objects maintain structural references to their canonical source IDs, ensuring every sentence in a generated artifact can trace its lineage back to the immutable `registry/ids.yml`.
