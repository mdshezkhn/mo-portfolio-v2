# LIVE_DEPLOYMENT_AUDIT.md

> **Phase 1 & 2 Deliverable**: End-to-End Deployment Source Identification and Build Pipeline Verification.

---

## 1. Deployment Source Identification

* **Live GitHub Repository**: `https://github.com/mdshezkhn/mo-portfolio-v2.git`
* **Active Branch**: `master`
* **GitHub Pages Target**: Root `/` of `master` branch (`mo-portfolio-v2/index.html`)
* **Live Site URL**: `https://mdshezkhn.github.io/mo-portfolio-v2/`
* **Served Artifact**: `mo-portfolio-v2/index.html` (HTML5 Single-Page Portfolio)

---

## 2. End-to-End Publication Architecture

```text
Canonical Data Models (employment.yml, education.yml, organisations.yml, claims/)
       ↓
Compiled Presentation Assets (compiled_assets/CV_Master.md, Portfolio_Copy.md)
       ↓
Website Source Template (mo-portfolio-v2/index.html)
       ↓
Git Commit & Remote Push (commit bf6af46 on master branch)
       ↓
GitHub Pages Automated Deployment Engine
       ↓
Live Web Assets (https://mdshezkhn.github.io/mo-portfolio-v2/)
```

---

## 3. Deployment Source Verification Decision

**Status:** **PASS**  
The live deployment source (`mo-portfolio-v2/index.html`) has been identified, verified, and linked directly to the `master` branch of `mdshezkhn/mo-portfolio-v2`.
