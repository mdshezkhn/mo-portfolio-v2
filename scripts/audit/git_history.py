import os
import subprocess
import json
from datetime import datetime

def run_cmd(cmd_list, cwd):
    try:
        res = subprocess.run(cmd_list, capture_output=True, text=True, cwd=cwd, encoding="utf-8", errors="ignore")
        return res.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def audit_git_history(base_dir):
    print("==================================================")
    print(" Phase 4: Deep Git History & Commit Graph Audit   ")
    print("==================================================")
    
    findings = []
    git_dir = os.path.join(base_dir, ".git")
    if not os.path.exists(git_dir):
        print("-> Notice: Not a git repository directory. Skipping git history audit.")
        return {
            "summary": "Not a git repository",
            "findings": []
        }
        
    # 1. Timeline & Commits
    first_commit = run_cmd(["git", "log", "--reverse", "--format=%h %ad %s", "-n", "1"], base_dir)
    last_commit = run_cmd(["git", "log", "--format=%h %ad %s", "-n", "1"], base_dir)
    commit_count = run_cmd(["git", "rev-list", "--count", "HEAD"], base_dir)
    branches = run_cmd(["git", "branch", "-a"], base_dir)
    
    # 2. Check for historically committed sensitive filenames/directories
    sensitive_targets = ["_qa_shots", "backups", ".playwright-mcp", ".claude", ".env", "Cookies", "Login Data", ".pem"]
    for target in sensitive_targets:
        log_check = run_cmd(["git", "log", "--all", "--full-history", "--", f"*{target}*"], base_dir)
        if log_check:
            first_line = log_check.split("\n")[0] if log_check else ""
            findings.append({
                "category": "historical_git_leak",
                "severity": "High",
                "target": target,
                "detail": f"Target '{target}' appears in historical Git commit logs: {first_line}",
                "remediation": "Rewrite Git history using git-filter-repo if sensitive data was committed."
            })
            
    # 3. Check for dangling blobs / orphaned commits
    fsck_out = run_cmd(["git", "fsck", "--lost-found"], base_dir)
    dangling_count = fsck_out.count("dangling") if fsck_out else 0
    
    summary_data = {
        "first_commit": first_commit,
        "last_commit": last_commit,
        "total_commits": commit_count,
        "branches": branches.split("\n") if branches else [],
        "dangling_objects_count": dangling_count
    }
    
    print(f"-> Git History Audit completed. Commits: {commit_count}. Historical findings: {len(findings)}.")
    return {
        "summary": summary_data,
        "findings": findings
    }
