# Monorepo Migration Plan

**Date:** 2026-08-07  
**Phase:** 3 — Migration Plan (PRE-EXECUTION)  
**Repository:** `mdshezkhn/mo-portfolio-v2`  
**Branch:** `release/2027.1`

---

## Phase 2: Classification

### Nested Repository Classifications

| # | Path | Category | Rationale | Action |
|---|------|----------|-----------|--------|
| 1 | `mo-portfolio-v2/` | **ACTIVE PRODUCT** | The live portfolio website (292 files, 47 commits). Currently the most developed version with credentials section, evidence-driven design. Has its own Git history with remote `mdshezkhn/mo-portfolio-v2.git`. | **TRACK NORMALLY** — Remove `.git`, track as regular directory. This is the website component of the Career OS. |
| 2 | `mo-portfolio/` | **OBSOLETE** | Contains only a single `README.md`. No `.git` directory. Empty shell from an earlier iteration. No functional content. | **REMOVE** — Delete the gitlink entry and the empty directory. |
| 3 | `mo-portfolio-v2-backup-20260717-2014/` | **OBSOLETE** | Empty directory (0 files). No `.git` directory. Was a backup point that was never populated or has been cleaned. | **REMOVE** — Delete the gitlink entry and the empty directory. |
| 4 | `archive/portfolio-before-audit-20260718-2123/` | **BACKUP** | Point-in-time snapshot (48 files) of the portfolio from before a major audit on 2026-07-18. HEAD at commit `cacc017`. Same remote as main portfolio. Contains 3 commits — all deployment/remediation related. | **ARCHIVE** — Remove `.git`, track as regular archived files. Valuable as pre-audit reference. |
| 5 | `archive/portfolio-v1/` | **LEGACY** | The original v1 portfolio (135 files, many commits). Has both `main` and `master` branches. Contains the full evolutionary history of v1 including remediations through v1.2.2. | **ARCHIVE** — Remove `.git`, track as regular archived files. Contains the v1 portfolio design and content. |
| 6 | `archive/portfolio-v2-backup-20260717/` | **BACKUP** | Near-duplicate of `portfolio-before-audit` (49 files, same commit messages). HEAD at `9093e07`. Remote points to a separate backup repo. 1 extra file vs before-audit. | **ARCHIVE** — Remove `.git`, track as regular archived files. Redundant with #4 but preserving to avoid data loss. |

### Already-Tracked Archive Content (No Issues)

| Path | Status | Notes |
|------|--------|-------|
| `archive/portfolio-v1-backup-20260717/` | ✅ Normal tracked | 33 files, no `.git`, clean |
| `archive/portfolio-v3-draft/` | ✅ Normal tracked | 42 files, no `.git`, clean |
| `archive/project-meridian/` | ✅ Normal tracked | 19 files, no `.git`, clean |
| `archive/public-portfolio-draft/` | ✅ Normal tracked | 6 files, no `.git`, clean |

### Deleted-On-Disk Files Still Tracked

| Path | Tracked files | On disk? | Action |
|------|--------------|----------|--------|
| `mo-portfolio-backup-20260717-1827/` | 43 files | ❌ No | **REMOVE FROM INDEX** — Formally commit the deletion |
| `portfolio-v3/` | 1 file | ❌ No | **REMOVE FROM INDEX** — Formally commit the deletion |
| `.playwright-mcp/` (9 files) | 9 files | ❌ No | **REMOVE FROM INDEX** — These are ephemeral; already gitignored pattern |

---

## Phase 3: Migration Plan

### Pre-Flight

> [!CAUTION]
> Before any modifications, create a backup stash and a safety branch.

```powershell
# 1. Create safety branch at current HEAD
git branch pre-monorepo-migration

# 2. Verify we're on the right branch
git branch --show-current
# Expected: release/2027.1
```

### Rollback Strategy

If anything goes wrong at any stage:

```powershell
# Option A: Reset to safety branch
git checkout pre-monorepo-migration
git checkout -B release/2027.1

# Option B: Hard reset to pre-migration commit
git reset --hard dd575ed
```

---

### Stage 1: Remove Stale Gitlink Entries (160000)

Remove all 6 submodule gitlinks from the index **without deleting files on disk**.

```powershell
# Remove gitlink entries from index only (--cached = index only, no disk deletion)
git rm --cached archive/portfolio-before-audit-20260718-2123
git rm --cached archive/portfolio-v1
git rm --cached archive/portfolio-v2-backup-20260717
git rm --cached mo-portfolio
git rm --cached mo-portfolio-v2
git rm --cached mo-portfolio-v2-backup-20260717-2014
```

**Verification:**
```powershell
git ls-files --stage | findstr "160000"
# Expected: NO OUTPUT
```

**Failure point:** If `git rm --cached` fails on any entry, the index may be corrupted. Use `git update-index --force-remove <path>` as fallback.

---

### Stage 2: Remove Nested `.git` Directories

Remove the independent Git repositories inside subdirectories so they become normal directories.

```powershell
# Remove nested .git directories (these are full repos, not worktree pointers)
Remove-Item -Recurse -Force "archive\portfolio-before-audit-20260718-2123\.git"
Remove-Item -Recurse -Force "archive\portfolio-v1\.git"
Remove-Item -Recurse -Force "archive\portfolio-v2-backup-20260717\.git"
Remove-Item -Recurse -Force "mo-portfolio-v2\.git"
```

**Verification:**
```powershell
Get-ChildItem -Path . -Recurse -Force -Filter ".git" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.claude\\' -and $_.FullName -eq (Resolve-Path ".\.git").Path -or $_.FullName -notmatch [regex]::Escape((Resolve-Path ".\.git").Path) }
# Expected: Only the root .git directory and the .claude worktree .git file
```

**Failure point:** Windows file locks on `.git` contents. Close all editors/terminals that may have handles open in those directories first.

---

### Stage 3: Add Directories as Normal Tracked Content

```powershell
# Add the active website as normal tracked files
git add mo-portfolio-v2/

# Add archive directories as normal tracked files
git add archive/portfolio-before-audit-20260718-2123/
git add archive/portfolio-v1/
git add archive/portfolio-v2-backup-20260717/
```

**Verification:**
```powershell
git ls-files --stage -- mo-portfolio-v2/ | Select-Object -First 5
# Expected: mode 100644 entries (normal files), NOT 160000
```

---

### Stage 4: Clean Up Obsolete Entries

```powershell
# Remove the empty/obsolete directories
Remove-Item -Recurse -Force "mo-portfolio" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "mo-portfolio-v2-backup-20260717-2014" -ErrorAction SilentlyContinue

# Remove deleted-on-disk files from the index
git rm --cached -r mo-portfolio-backup-20260717-1827 2>$null
git rm --cached -r portfolio-v3 2>$null

# Remove deleted .playwright-mcp files
git rm --cached -r .playwright-mcp 2>$null
```

---

### Stage 5: Prune Orphaned Worktree (Optional)

```powershell
# Check if the Claude agent worktree is still needed
git worktree list
# If the agent worktree is no longer active:
# git worktree remove .claude/worktrees/agent-a415229218a57a1e8 --force
# git branch -D worktree-agent-a415229218a57a1e8
```

> [!NOTE]
> The Claude worktree is inside `.claude/` which is gitignored. It poses no risk to the monorepo. Pruning is optional.

---

### Stage 6: Commit the Migration

```powershell
git add -A
git status
# Review carefully — should show:
# - Renamed/new files from former submodule directories
# - Deleted files from mo-portfolio-backup-20260717-1827/ and portfolio-v3/
# - No 160000 entries

git commit -m "refactor: convert repository to clean monorepo

- Remove 6 stale submodule gitlink entries (160000 mode)
- Remove 4 nested .git directories
- Track mo-portfolio-v2/ as normal directory (active website)
- Track archive/* as normal directories (historical snapshots)
- Remove obsolete empty directories (mo-portfolio, mo-portfolio-v2-backup-20260717-2014)
- Remove deleted-on-disk tracked files (mo-portfolio-backup-20260717-1827/, portfolio-v3/)
- Clean up stale .playwright-mcp entries

No .gitmodules file or submodule configuration remains.
Repository is now a proper single monorepo."
```

---

### Expected Final Structure

```
Mo Digital Portfolio/
├── .git/                        (root repository)
├── .github/                     (CI workflows)
├── .gitignore
├── archive/                     (historical snapshots — normal tracked)
│   ├── portfolio-before-audit-20260718-2123/
│   ├── portfolio-v1/
│   ├── portfolio-v1-backup-20260717/
│   ├── portfolio-v2-backup-20260717/
│   ├── portfolio-v3-draft/
│   ├── project-meridian/
│   └── public-portfolio-draft/
├── career-data/                 (canonical YAML data)
├── compiled_assets/             (generated CVs, profiles)
├── docs/
├── evidence/
├── governance/
├── mo-portfolio-v2/             (active website — normal tracked)
├── recruiter_packs/
├── releases/
├── schemas/
├── scripts/
├── templates/
├── tests/
├── build.py
├── package.json
└── README.md
```

---

### Verification Plan

After committing, run the following checks:

```powershell
# V1: No 160000 entries remain
git ls-files --stage | findstr "160000"
# Expected: NO OUTPUT

# V2: Submodule status works cleanly
git submodule status
# Expected: no output (no submodules configured) — NOT a fatal error

# V3: No nested .git directories (excluding .claude)
Get-ChildItem -Recurse -Force -Filter ".git" | Where-Object { $_.FullName -notmatch '\\\.claude\\' -and $_.FullName -ne (Resolve-Path ".\.git").Path }
# Expected: NO OUTPUT

# V4: No .gitmodules file
Test-Path .gitmodules
# Expected: False

# V5: Git status is clean
git status
# Expected: "nothing to commit, working tree clean" (or only intentional changes)

# V6: Git fsck passes
git fsck --no-dangling
# Expected: No errors

# V7: Total tracked file count increased (submodule content now tracked)
(git ls-files | Measure-Object -Line).Lines
# Expected: ~500+ (up from 345, since submodule contents are now tracked)

# V8: Fresh clone test
# (Manual verification — clone to a temp directory and verify all files present)
```
