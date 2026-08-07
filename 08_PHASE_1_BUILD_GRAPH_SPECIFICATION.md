# Phase 1: Repository Build Graph Specification

## 1. Objective
This specification formally defines the repository's build graph. It explicitly details the nodes (assets) and edges (transformations) currently observed in the repository, making the provenance chains machine-readable and exposing the missing transformations.

---

## 2. Nodes (Assets & Artifacts)

### [NODE-001] Canonical Facts
* **ID:** `career-data/facts`
* **Inputs:** None (Root Node)
* **Outputs:** `NODE-002`, `NODE-003`, `NODE-007`
* **Producer:** None (Human-authored)
* **Consumers:** `ci_pipeline.py`, `resolve_graph.py`, `compile_intermediate.py`
* **Deterministic:** N/A (Source)
* **Incremental:** No
* **Cacheable:** Yes
* **Rebuild Command:** N/A
* **Evidence Reference:** `ci_pipeline.py`

### [NODE-002] Intermediate Facts Compilation
* **ID:** `career-data/intermediate/facts.json`
* **Inputs:** `NODE-001`
* **Outputs:** Downstream validators
* **Producer:** `scripts/compile_intermediate.py`
* **Consumers:** `validate_semantics.py`
* **Deterministic:** Yes
* **Incremental:** No
* **Cacheable:** Yes
* **Rebuild Command:** `python scripts/compile_intermediate.py`
* **Evidence Reference:** `compile_intermediate.py:62`

### [NODE-003] Resolved Graph
* **ID:** `career-data/intermediate/resolved_graph.json`
* **Inputs:** `NODE-001`
* **Outputs:** `NODE-004`
* **Producer:** `scripts/resolve_graph.py`
* **Consumers:** `scripts/build_view_models.py`
* **Deterministic:** Yes
* **Incremental:** No
* **Cacheable:** Yes
* **Rebuild Command:** `python scripts/resolve_graph.py`
* **Evidence Reference:** `resolve_graph.py:213`

### [NODE-004] Professional Profile View Model
* **ID:** `artifacts/professional_profile_vm.json`
* **Inputs:** `NODE-003`
* **Outputs:** `NODE-005`
* **Producer:** `scripts/build_view_models.py`
* **Consumers:** `scripts/render_markdown.py`
* **Deterministic:** Yes
* **Incremental:** No
* **Cacheable:** Yes
* **Rebuild Command:** `python scripts/build_view_models.py`
* **Evidence Reference:** `build_view_models.py:132`

### [NODE-005] Generated Markdown CV
* **ID:** `artifacts/generated/cv.md`
* **Inputs:** `NODE-004`
* **Outputs:** None (Terminal Node)
* **Producer:** `scripts/render_markdown.py`
* **Consumers:** None deployed
* **Deterministic:** Yes
* **Incremental:** No
* **Cacheable:** Yes
* **Rebuild Command:** `python scripts/render_markdown.py`
* **Evidence Reference:** `render_markdown.py:65`

### [NODE-006] JSON Profiles (Legacy)
* **ID:** `templates/cv/profiles/*.json`
* **Inputs:** Unknown
* **Outputs:** `NODE-008`
* **Producer:** Unknown (No in-repository producer)
* **Consumers:** `build.py`
* **Deterministic:** N/A (Manual input)
* **Incremental:** N/A
* **Cacheable:** N/A
* **Rebuild Command:** N/A
* **Evidence Reference:** `build.py:46`

### [NODE-007] Rendered Certificates
* **ID:** `mo-portfolio-v2/assets/images/certificates/`
* **Inputs:** `NODE-001`
* **Outputs:** `NODE-009` (via HTML inclusion)
* **Producer:** `process_authentic_certificates.py`, `generate_documentary_certificates.py`
* **Consumers:** `mo-portfolio-v2/index.html`
* **Deterministic:** Yes
* **Incremental:** No
* **Cacheable:** Yes
* **Rebuild Command:** `python scripts/generate_documentary_certificates.py`
* **Evidence Reference:** `generate_documentary_certificates.py:6`

### [NODE-008] Compiled HTML Assets
* **ID:** `compiled_assets/`
* **Inputs:** `NODE-006`
* **Outputs:** None (Terminal Node)
* **Producer:** `build.py`
* **Consumers:** Recruiter distribution (Manual)
* **Deterministic:** Yes
* **Incremental:** No
* **Cacheable:** Yes
* **Rebuild Command:** `python career.py build`
* **Evidence Reference:** `build.py:35`

### [NODE-009] Web Portfolio Payload
* **ID:** `mo-portfolio-v2/index.html`
* **Inputs:** None found (Should be `NODE-004`)
* **Outputs:** GitLab Pages Deployment
* **Producer:** Unknown (No in-repository producer)
* **Consumers:** `.gitlab-ci.yml`
* **Deterministic:** N/A (Manual input)
* **Incremental:** N/A
* **Cacheable:** N/A
* **Rebuild Command:** N/A
* **Evidence Reference:** `.gitlab-ci.yml:18`

---

## 3. Edges (Transformations)

| Edge ID | Source (Input) | Destination (Output) | Transformation Script | Verified? | CI Stage |
|---|---|---|---|---|---|
| **E-001** | `NODE-001` (Facts) | `NODE-002` (Intermediate) | `compile_intermediate.py` | Yes | Gate 2 |
| **E-002** | `NODE-001` (Facts) | `NODE-003` (Graph) | `resolve_graph.py` | Yes | Gate 2 |
| **E-003** | `NODE-003` (Graph) | `NODE-004` (VM) | `build_view_models.py` | Yes | Gate 2 |
| **E-004** | `NODE-004` (VM) | `NODE-005` (CV.md) | `render_markdown.py` | Yes | Gate 2 |
| **E-005** | `NODE-001` (Facts) | `NODE-007` (Certificates) | `generate_documentary_certificates.py`| Yes | None (Manual) |
| **E-006** | `NODE-006` (Profiles) | `NODE-008` (Compiled HTML) | `build.py` | Yes | None (Manual) |
| **E-007** | `NODE-001` (Facts) | `NODE-009` (Portfolio) | **MISSING** | No | N/A |
| **E-008** | `NODE-009` (Portfolio) | GitLab Pages | `.gitlab-ci.yml` (copy) | Yes | Deploy |

---

## 4. Visualizing the Graph

```text
       ┌──────────► NODE-002 (Intermediate Facts)
       │
NODE-001 (Canonical Facts)
       │
       ├──────────► NODE-007 (Certificates) ─────┐
       │                                         │ (Manual inclusion)
       └──────────► NODE-003 (Graph)             ▼
                       │                      NODE-009 (Portfolio HTML)
                       ▼                         │
                    NODE-004 (VM)                │
                       │                         │
                       ▼                         ▼
                    NODE-005 (CV.md)          GitLab Pages (Production)


NODE-006 (Manual Profiles)
       │
       └──────────► NODE-008 (Compiled HTML Assets)
```

## 5. Phase 1 Conclusions
The Build Graph Specification mathematically proves the core disconnect: **Edge E-007 is missing**. 
There is no automated transformation mapping the Canonical Facts (or View Models) into the final Web Portfolio Payload. Furthermore, the Compiled HTML Assets pipeline (`NODE-006` to `NODE-008`) is entirely severed from the Canonical Facts.
