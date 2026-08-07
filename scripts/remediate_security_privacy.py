import os
import sys
import json
import shutil
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIT_RESULTS_FILE = os.path.join(BASE_DIR, "audit", "audit_results.json")
QUARANTINE_DIR = os.path.join(BASE_DIR, "quarantine")
REMEDIATION_PLAN_FILE = os.path.join(BASE_DIR, "audit", "REMEDIATION_PLAN.md")

def generate_remediation():
    print("==================================================")
    print(" Non-Destructive Remediation & Quarantine Planner ")
    print("==================================================")
    
    if not os.path.exists(AUDIT_RESULTS_FILE):
        print(f"Error: Audit results file `{AUDIT_RESULTS_FILE}` not found. Run generate_reports.py first.")
        return
        
    with open(AUDIT_RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    confirm = "--confirm" in sys.argv
    quarantine_targets = []
    
    # Collect items that should be quarantined (browser profiles, env files, temporary dumps)
    sec_findings = data["findings"].get("security", [])
    for item in sec_findings:
        if item.get("category") in ["browser_artifact", "browser_profile_directory", "environment_file", "sensitive_extension"]:
            quarantine_targets.append(item["file"])
            
    # Remove duplicates
    quarantine_targets = list(set(quarantine_targets))
    
    # Write Remediation Plan Markdown
    with open(REMEDIATION_PLAN_FILE, "w", encoding="utf-8") as f:
        f.write("# Non-Destructive Remediation Plan\n\n")
        f.write(f"Generated: `{datetime.now().isoformat()}`\n\n")
        f.write("## Targeted Items for Quarantine\n\n")
        if not quarantine_targets:
            f.write("No sensitive files or browser artifacts marked for quarantine.\n")
        else:
            for t in quarantine_targets:
                f.write(f"- `{t}` -> `quarantine/{t}`\n")
        f.write("\n## Execution Status\n")
        if confirm:
            f.write("State: **EXECUTED (--confirm mode enabled)**\n")
        else:
            f.write("State: **DRY RUN / PLAN GENERATED ONLY** (Run with `--confirm` to execute quarantine)\n")
            
    print(f"-> Remediation plan written to: {REMEDIATION_PLAN_FILE}")
    
    if quarantine_targets and confirm:
        if not os.path.exists(QUARANTINE_DIR):
            os.makedirs(QUARANTINE_DIR)
            
        print("\nExecuting quarantine transfer...")
        for rel_p in quarantine_targets:
            src = os.path.join(BASE_DIR, rel_p)
            if os.path.exists(src):
                dst = os.path.join(QUARANTINE_DIR, rel_p)
                dst_dir = os.path.dirname(dst)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                try:
                    shutil.move(src, dst)
                    print(f"  [QUARANTINED] {rel_p} -> quarantine/{rel_p}")
                except Exception as e:
                    print(f"  [ERROR] Could not move {rel_p}: {e}")
        print("\nQuarantine execution complete.")
    elif quarantine_targets:
        print(f"\nFound {len(quarantine_targets)} items to quarantine. Run `python scripts/remediate_security_privacy.py --confirm` to execute transfer.")
    else:
        print("\nZero items marked for quarantine.")

if __name__ == "__main__":
    generate_remediation()
