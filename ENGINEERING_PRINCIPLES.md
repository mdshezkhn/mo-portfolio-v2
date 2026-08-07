# Repository Engineering & Governance Principles

This document outlines the foundational engineering principles governing the structure, build pipelines, release gates, and security infrastructure of this repository.

---

## 1. Inventory-First Architecture
All repository audits, security checks, and build operations consume a single, versioned repository inventory (`REPOSITORY_INVENTORY.json`) created at Phase 0. No scanner or build step relies on ad-hoc directory traversals.

## 2. Canonical Single Source of Truth
Machine-readable JSON data models (`audit_results.json`, `resolved_graph.json`, `build_manifest.json`) serve as the authoritative single source of truth. All human-readable Markdown reports and HTML views are rendered deterministically from these canonical data structures.

## 3. Evidence Before Presentation
No claim, qualification, or achievement is presented in public portfolio artifacts without traceable, verified backing evidence (`career-data/facts/`, `EVIDENCE_LIBRARY/`).

## 4. Deterministic & Reproducible Builds
Build outputs are strictly deterministic. The build system purges local machine paths (`C:\Users\...`), environment artifacts, and timestamps to guarantee byte-for-byte build reproducibility across environments.

## 5. Policy-Driven Classification
Security, PII, and privacy rules are defined declaratively in version-controlled configuration files (`governance/privacy_policy.yaml`, `governance/privacy_allowlist.yaml`, `governance/security_baseline.json`) rather than hardcoded in scanner scripts.

## 6. Governance Integrity & Self-Protection
Governance rules themselves are protected against silent dilution. **RC-10 (Governance Integrity Gate)** hashes policy configuration files (`governance_manifest.json`) and fails the build if a policy is altered without explicit manifest sign-off.

## 7. Decoupled Gate vs. Deep Audit Tooling
Release gates (RC-1 through RC-10) are lightweight, deterministic, and execute in seconds to provide fast CI feedback. Deep analysis (Git history commit graph audits, full repository scans) runs on-demand or pre-release.

## 8. Non-Destructive Remediation
Remediation tooling never silently deletes files. It generates a human-readable remediation plan (`REMEDIATION_PLAN.md`), moves flagged assets into an isolated quarantine area (`quarantine/`), and requires explicit confirmation (`--confirm`) before any permanent action.

## 9. Fail-Closed Security Posture
Any unhandled active secret, private key, browser profile database, or unapproved PII entity defaults to an immediate release build failure.

## 10. Dual-Purpose Architecture
The repository maintains strict engineering governance for technical reviewers (CI/CD, regression fixtures, release gates, provenance tracking) while delivering a clean, presentation for recruiters and non-technical stakeholders.

---

## Architecture Lifecycle Status

> [!NOTE]
> **Architecture Status: Feature Frozen (v1.x)**
> New architectural components require a demonstrated deficiency in the current framework or a formally approved design change. Current maintenance focuses on fixing defects, expanding security test fixtures (`tests/security_fixtures/`), and keeping dependencies current.
