# Monorepo Forensic Audit

**Date:** 2026-08-07  
**Auditor:** Automated Principal Engineer  
**Branch:** `release/2027.1` @ `dd575ed`  
**Repository:** `mdshezkhn/mo-portfolio-v2`

---

## Executive Summary

The repository is in an **invalid hybrid state**. Six (6) stale submodule entries exist in the Git index (mode `160000`), but no `.gitmodules` file exists to map them. This causes `git submodule status` to fail with a fatal error. Four (4) nested `.git` directories contain full independent repositories. The worktree system has one Claude agent worktree that is functional but orphaned from any active workflow.

**Severity: HIGH** — The repository cannot be cleanly cloned as a monorepo, and any submodule-related Git operation will fail.

---

## 1. Stale 160000 Git Index Entries

Six paths are registered as submodules (gitlinks) in both the index and the committed tree (`HEAD`):

| # | Path | SHA | Object in parent? | On disk? | Has `.git`? | File count |
|---|------|-----|-------------------|----------|-------------|------------|
| 1 | `archive/portfolio-before-audit-20260718-2123` | `cacc017` | ✅ Yes | ✅ Yes | ✅ Yes (dir) | 48 |
| 2 | `archive/portfolio-v1` | `5f3c9de` | ✅ Yes | ✅ Yes | ✅ Yes (dir) | 135 |
| 3 | `archive/portfolio-v2-backup-20260717` | `9093e07` | ❌ Missing | ✅ Yes | ✅ Yes (dir) | 49 |
| 4 | `mo-portfolio` | `20dae72` | ✅ Yes | ✅ Yes | ❌ No | 1 (README only) |
| 5 | `mo-portfolio-v2` | `f10be95` | ✅ Yes | ✅ Yes | ✅ Yes (dir) | 292 |
| 6 | `mo-portfolio-v2-backup-20260717-2014` | `9093e07` | ❌ Missing | ✅ Yes | ❌ No | 0 (empty) |

### Root Cause
These entries were introduced in commit `8ad48e3` ("Initial commit: Governance and Phase C Release Assets") and `b405cee` ("Career OS v4.0 — Week 1"). At that time, the directories contained independent Git repositories whose `.git` directories existed. Git automatically detected them as submodules and recorded gitlink entries. The `.gitmodules` file was either never created or was subsequently deleted, leaving the index in an inconsistent state.

### Object Integrity Note
SHA `9093e07` (used by entries #3 and #6) does **not** exist in the parent repository's object store. This is expected — gitlink SHAs point to commits inside the submodule's own object store, not the parent's. However, it means `git fsck` may report missing objects in certain modes.

---

## 2. Nested `.git` Directories

| # | Path | Type | Full repo? | Remote | Branch |
|---|------|------|-----------|--------|--------|
| 1 | `archive/portfolio-before-audit-20260718-2123/.git` | Directory | ✅ Yes | `mdshezkhn/mo-portfolio-v2.git` | `master` |
| 2 | `archive/portfolio-v1/.git` | Directory | ✅ Yes | `mdshezkhn/mo-portfolio-v2.git` | `main` |
| 3 | `archive/portfolio-v2-backup-20260717/.git` | Directory | ✅ Yes | `mdshezkhn/mo-portfolio-v2-backup-20260717-2014.git` | `master` |
| 4 | `mo-portfolio-v2/.git` | Directory | ✅ Yes | `mdshezkhn/mo-portfolio-v2.git` | `master` |

**All four are complete independent Git repositories** with their own objects, refs, logs, and remotes. They are historical snapshots frozen at different points in the project's evolution.

### `.git` File (Worktree)
| # | Path | Type | Purpose |
|---|------|------|---------|
| 5 | `.claude/worktrees/agent-a415229218a57a1e8/.git` | File | Valid Git worktree pointer (part of `.claude/` — gitignored) |

---

## 3. Git Configuration Analysis

- **`.git/config`**: Clean. No `[submodule]` sections exist.
- **`.git/modules/`**: Does **not** exist. (No cached submodule repos.)
- **`.gitmodules`**: Does **not** exist on disk or in tracked files.
- **Git worktrees**: One active worktree (`agent-a415229218a57a1e8`) on branch `worktree-agent-a415229218a57a1e8`.
- **Stash**: One stash entry (`Pre-repository-reconciliation backup`).
- **Tags**: `phase-3.1-reference-layer`, `v1.0`.
- **`git fsck --no-dangling`**: Clean. No corruption in the parent repo's object store.

---

## 4. Tracked Files Analysis

**345 total tracked files** in the index. Distribution:

| Category | Path prefix | Files | Status |
|----------|------------|-------|--------|
| Archive (properly tracked) | `archive/portfolio-v1-backup-20260717/` | 33 | Normal — tracked as regular files |
| Archive (properly tracked) | `archive/portfolio-v3-draft/` | 42 | Normal — tracked as regular files |
| Archive (properly tracked) | `archive/project-meridian/` | 19 | Normal — tracked as regular files |
| Archive (properly tracked) | `archive/public-portfolio-draft/` | 6 | Normal — tracked as regular files |
| Legacy backup (tracked) | `mo-portfolio-backup-20260717-1827/` | 43 | Normal files, but **dir doesn't exist on disk** (shows as `D` deleted) |
| Legacy backup (tracked) | `portfolio-v3/` | 1 | Normal file, but **dir doesn't exist on disk** (shows as `D` deleted) |
| **Stale gitlinks** | 6 paths | 6 | **Mode 160000 — MUST BE REMOVED** |
| Active product | `career-data/`, `schemas/`, etc. | ~80 | Normal — the monorepo content |

### Key Findings
- `mo-portfolio-backup-20260717-1827/` is tracked in Git but the directory has been deleted from disk. Git status shows 43 deleted files.
- `portfolio-v3/` has 1 tracked file but the directory is deleted from disk.
- These deletions are **unstaged** — they are not yet committed.

---

## 5. Worktree Assessment

| Worktree | Branch | Location | Status |
|----------|--------|----------|--------|
| Main | `release/2027.1` | Root | Active |
| Agent | `worktree-agent-a415229218a57a1e8` | `.claude/worktrees/...` | Functional but orphaned |

The agent worktree is inside `.claude/` which is gitignored. It's benign but should be pruned to avoid confusion.

---

## 6. Risk Analysis

| Risk | Severity | Impact |
|------|----------|--------|
| `git submodule status` fatal error | **CRITICAL** | Any CI or tool relying on submodule commands will fail |
| 160000 entries block normal tracking | **HIGH** | Files inside these directories cannot be tracked by the parent repo |
| Nested `.git` dirs cause confusion | **HIGH** | `git add` inside these dirs modifies the wrong repo |
| Missing `.gitmodules` with gitlinks present | **HIGH** | Invalid Git state; violates Git invariants |
| Deleted-on-disk files still tracked | **MEDIUM** | 44 files show as deleted; need to be committed or restored |
| Object SHA `9093e07` missing from parent | **LOW** | Expected for gitlinks; no corruption |
| Orphaned worktree | **LOW** | No impact; can be pruned |

---

## 7. Migration Recommendations

1. **Remove all 6 gitlink (160000) entries** from the Git index using `git rm --cached`
2. **Remove all 4 nested `.git` directories** so files can be tracked normally
3. **Stage the directory contents** as regular tracked files where appropriate
4. **Classify each nested repository** (Phase 2) to determine: archive, track, or remove
5. **Clean up deleted-on-disk files** — either restore them or formally remove from tracking
6. **Prune the orphaned worktree** 
7. **Commit all changes** as a single "monorepo migration" commit
8. **Validate** with `git ls-files --stage | findstr 160000` (expect zero results)