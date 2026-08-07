# PROPAGATION_RULES.md (v1.0)

**Version:** 1.0
**Status:** ACTIVE
**Owner:** Mohammed Shehzad Khan
**Purpose:** Defines explicitly where specific information objects must appear across the repository to prevent propagation failures.

## Propagation Matrix

This policy answers: *"Where must this information appear?"*

### 1. Qualifications
| Object | Target Destinations | Severity if Missing |
|---|---|---|
| **PGCE (C-004)** | `CV_*`, `LinkedIn`, `Portfolio`, `Interview_Stories`, `Teaching_Philosophy` | CRITICAL |
| **B.Ed. (C-003)** | `CV_*`, `LinkedIn`, `Portfolio` | HIGH |
| **M.A. English (C-025)** | `CV_*`, `LinkedIn`, `Portfolio`, `Interview_Stories` | HIGH |
| **B.Sc. Physics (C-008)** | `CV_Master`, `CV_STEM`, `Portfolio` | MEDIUM |

### 2. Core Career Claims
| Object | Target Destinations | Severity if Missing |
|---|---|---|
| **Availability (C-023)** | `CV_*`, `LinkedIn`, `Portfolio`, `Recruiter_Playbook` | HIGH |
| **Years Experience (C-001)** | `CV_*`, `LinkedIn`, `Portfolio` | HIGH |
| **Languages (C-020, 21, 22)**| `CV_*`, `LinkedIn`, `Portfolio` | MEDIUM |

### 3. Employment History
| Object | Target Destinations | Severity if Missing |
|---|---|---|
| **Aoxin 2nd Stint (Current)** | `CV_*`, `LinkedIn`, `Portfolio`, `career-timeline.md` | CRITICAL |
| **GEDU Global** | `CV_*`, `LinkedIn`, `Portfolio`, `career-timeline.md` | CRITICAL |
| **WhiteHat Jr** | `CV_*`, `LinkedIn`, `Portfolio`, `career-timeline.md` | CRITICAL |
| **Aoxin 1st Stint** | `CV_*`, `LinkedIn`, `Portfolio`, `career-timeline.md` | CRITICAL |
| **Eton House** | `CV_Master`, `LinkedIn`, `career-timeline.md` | HIGH |
| **Zhejiang/Helen** | `CV_Master`, `LinkedIn`, `career-timeline.md` | HIGH |
| **Scholars Academy** | `CV_Master`, `LinkedIn`, `career-timeline.md` | HIGH |

## Propagation Validation
Certification `03_RECRUITER_READINESS.md` and `04_PIPELINE_HEALTH.md` must enforce these targets. If a target artifact lacks the required object, the pipeline flags a `PROPAGATION FAILURE`.
