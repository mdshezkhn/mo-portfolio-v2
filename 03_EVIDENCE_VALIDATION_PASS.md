# Evidence Validation Pass (Phase 3)

## 1. Executive Summary
This document serves as a strict evidence audit of the claims made in `02_REPOSITORY_ARCHITECTURE_SPECIFICATION.md`. It evaluates every major architectural assertion against verifiable repository evidence (scripts, file contents, git history). Assertions lacking direct evidence have been downgraded to "Unsupported" or "Inferred" and flagged for correction.

### Validation Criteria
| Status | Definition |
|---|---|
| **Verified** | Directly observed in the repository via code, config, or explicit file structures. |
| **Derived** | Logically deduced from a combination of verified facts. |
| **Inferred** | Plausible based on naming conventions, but lacking programmatic proof. |
| **Unsupported** | No repository evidence exists, or evidence directly contradicts the claim. |

---

## 2. Audit of Critical Issues

### Issue 1: Script Provenance and Outputs
**Claim in Spec:** `scripts/build_view_models.py` generates `career-data/view_models/`. `scripts/render_markdown.py` generates `compiled_assets/`.
* **Validation:** **Unsupported / Contradicted**
* **Evidence:**
  - `build_view_models.py` (Lines 128-132) explicitly writes to `artifacts/professional_profile_vm.json`. It does *not* write to `career-data/view_models`.
  - `render_markdown.py` (Lines 60-70) reads from `artifacts/professional_profile_vm.json` and writes to `artifacts/generated/cv.md` and `artifacts/generated/linkedin.md`. It does *not* write to `compiled_assets/`.
* **Correction:** The provenance of `compiled_assets/` and `career-data/view_models/` is currently **Unknown/Unsupported**. No python scripts in `scripts/` automate their generation. They may be manual copies or artifacts of a deprecated build process.

### Issue 2: `career-data/golden/` Classification
**Claim in Spec:** `career-data/golden/` is "Canonical Source / Generated (Mixed)".
* **Validation:** **Verified (with correction)**
* **Evidence:** `artifacts/manifest.json` and `audit/REPOSITORY_INVENTORY.json` show that `career-data/golden/` contains versioned snapshot directories (e.g., `career-data/golden/E-001/`). Inside `E-001/`, there are `source/facts/` (canonical data), `artifacts/` (generated), and `intermediate/` (generated).
* **Correction:** `golden` is not a working directory; it is a **Release Snapshot Archive**. It intrinsically contains mixed states because it freezes a point-in-time snapshot of the entire data/build pipeline.

### Issue 3: Recommendation Creep
**Claim in Spec:** Recommends splitting the repositories into two.
* **Validation:** **Unsupported (Out of Scope)**
* **Correction:** Removed from the architectural specification. The specification must describe the current state (a nested `.git` directory inside the Career OS). Future architectural migrations are deferred to a separate proposal.

### Issue 4: Mixed Directories without Proof
**Claim in Spec:** `career-data` contains generated `view_models/`, `computed/`, `intermediate/`.
* **Validation:** **Partially Verified / Partially Unsupported**
* **Evidence:**
  - `intermediate/`: **Verified**. Scripts like `compile_intermediate.py` and `resolve_graph.py` explicitly write to `--output-dir career-data/intermediate`.
  - `computed/`: **Verified**. `REPOSITORY_ASSET_INDEX.md` and `manifest.json` list files like `career-data/computed/claims.json`.
  - `view_models/`: **Unsupported**. While `scripts/generate_recruiter_pack.py` reads from `--view-dir career-data/view_models`, no script was found that writes to it.
* **Correction:** The architectural risk stands for `intermediate` and `computed`, but the provenance of `view_models` requires further investigation.

---

## 3. Audited Dependency Graph (Directed & Verified)

The dependency graph has been corrected to reflect only **verified** inputs and outputs.

```text
[Verified Canonical Sources]
  career-data/facts/ *.yml
  registry/ids.yml
        │
        ▼
[Verified Validation Layer]
  scripts/validate_yaml.py
  scripts/validate_semantics.py
  scripts/validate_ids.py
        │
        ▼ (Output: Pass/Fail in CI)
        │
[Verified Intermediate Compilation]
  scripts/resolve_graph.py
  scripts/compile_intermediate.py
        │
        ▼
[Verified Intermediate Artifacts]
  career-data/intermediate/facts.json
  career-data/intermediate/resolved_graph.json
        │
        ▼
[Verified View Model Generation]
  scripts/build_view_models.py
        │
        ▼
[Verified JSON Artifact]
  artifacts/professional_profile_vm.json
        │
        ▼
[Verified Presentation Generation]
  scripts/render_markdown.py
        │
        ▼
[Verified Output]
  artifacts/generated/cv.md
  artifacts/generated/linkedin.md
```

*Note: The bridge between `artifacts/generated/*` and the deployment folder (`mo-portfolio-v2/`) or `compiled_assets/` is currently **Unsupported** by evidence. It is inferred to be a manual copy process.*

---

## 4. Evidence-Backed Provenance Matrix

Every generated directory must declare its provenance with verified evidence.

| Generated Directory | Produced By | Consumes | Rebuild Command | Deterministic? | Evidence Link |
|---|---|---|---|---|---|
| `career-data/intermediate/` | `resolve_graph.py`, `compile_intermediate.py` | `career-data/facts/` | `python scripts/ci_pipeline.py` | Yes | Verified in source code (argparse `--output-dir`). |
| `artifacts/generated/` | `render_markdown.py` | `artifacts/professional_profile_vm.json` | `python scripts/render_markdown.py` | Yes | Verified in source code (Lines 61-70). |
| `artifacts/professional_profile_vm.json` | `build_view_models.py` | `query_engine.load_graph` | `python scripts/build_view_models.py` | Yes | Verified in source code (Lines 128-132). |
| `compiled_assets/` | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Unknown | **Unsupported**. No generator script found in `scripts/`. |
| `career-data/computed/` | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Unknown | **Unsupported**. Exists in manifests but no python script orchestrates it. |

---

## 5. Repository Constitution (Strictly Current Invariants)

The constitution is now limited to **Verified Current Invariants**. Aspirational goals have been removed.

1. **Single Source of Truth:** `career-data/facts/` is the sole observed input for downstream CI validation and graph resolution.
2. **Deployment Boundary:** `mo-portfolio-v2/` acts as the physical deployment boundary, containing a nested `.git` environment entirely separated from the Career OS lifecycle.
3. **Evidence Registry:** The `evidence/manifest.yml` file acts as the primary registry mapping physical claims to their hashed binary equivalents.
4. **Deterministic Validation:** The `ci_pipeline.py` enforces sequential validation of YAML semantics, ID integrity, and graph resolution before allowing artifact generation.

*Aspirational goals (e.g., eliminating mixed directories, splitting the repo) belong in a Migration Strategy document, not this baseline specification.*
