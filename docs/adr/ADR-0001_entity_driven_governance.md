# ADR-0001: Entity-Driven Governance Architecture

* **Status**: Accepted (Designated in Production Baseline v2.0)
* **Date**: 2026-08-01
* **Context**: Initially, presentation assets (CVs, LinkedIn text) contained duplicated claims and restated entity facts (e.g. degrees restated as prose claims), leading to narrative drift and unverified outcome assertions.

## Decisions

1. **Entity-Driven Architecture**: Entities (`organisations`, `institutions`, `qualifications`, `locations`) are the single source of truth. Metrics are computed directly from entities, not derived from prose claims.
2. **Qualifications $\ne$ Claims**: Qualification degrees and certificates (`QUAL-3000` to `QUAL-3003`) are entities, not prose claims. They are removed from the claim registry and rendered directly from `education.yml` + publication policy rules.
3. **Evidence-First Root of Trust**: Evidence manifest (`evidence/manifest.yml`) is the root of trust with machine-safe confidence enums (`V1` to `V5`).
4. **Dynamic Time-Aware Computation**: Experience is computed dynamically (`calculate_years_experience("2014-01")`) rather than hardcoded in prose text.

## Consequences

* **Positive**: Eliminates duplicated truth, eliminates manual yearly experience edits, prevents unverified claim drift, and enables automated impact analysis (`scripts/impact_analysis.py`).
* **Negative**: Requires strict initial normalization of legacy content.

## Production Guarantees (v2.0)

* Deterministic builds
* Reproducible recruiter assets
* Traceable evidence
* Continuous policy enforcement
* Backward-compatible v2.x evolution
