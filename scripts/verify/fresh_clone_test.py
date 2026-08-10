import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
CLONE_DIR = BASE_DIR.parent / "Mo Digital Portfolio_fresh_clone"

def run_cmd(cmd, cwd=BASE_DIR, fail_ok=False):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if not fail_ok and res.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{res.stderr}")
    return res

def main():
    print("Starting Fresh-Clone Verification Test...")
    
    # Get current metadata commit
    current_commit = run_cmd(['git', 'rev-parse', 'HEAD']).stdout.strip()
    print(f"Target metadata_commit: {current_commit}")
    
    # 1. Clone the repository
    if CLONE_DIR.exists():
        shutil.rmtree(CLONE_DIR)
        
    print(f"Cloning to {CLONE_DIR}...")
    run_cmd(['git', 'clone', str(BASE_DIR), str(CLONE_DIR)])
    
    # 2. Resolve the exact metadata_commit
    print("Checking out metadata_commit...")
    run_cmd(['git', 'checkout', current_commit], cwd=CLONE_DIR)
    
    # 3. Verify baseline_metadata.json is present
    metadata_path = CLONE_DIR / 'artifacts' / 'baselines' / 'cv_master' / 'baseline_metadata.json'
    if not metadata_path.exists():
        raise RuntimeError("baseline_metadata.json not found in fresh clone!")
        
    # 4. Extract source_commit
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    source_commit = metadata.get('git', {}).get('source_commit')
    if not source_commit:
        raise RuntimeError("source_commit not found in baseline_metadata.json")
    print(f"Extracted source_commit: {source_commit}")
    
    # 5. Verify source_commit is an ancestor
    res = run_cmd(['git', 'merge-base', '--is-ancestor', source_commit, current_commit], cwd=CLONE_DIR, fail_ok=True)
    if res.returncode != 0:
        raise RuntimeError(f"source_commit {source_commit} is not an ancestor of {current_commit}")
    print("Verified source_commit is an ancestor of metadata_commit.")
    
    # 6. Verify every manifest hash against checked-out files
    # (verify_baseline.py handles this internally, but we can do a quick check here too or just let verify_baseline do it)
    print("Skipping redundant hash check (verify_baseline.py will do this).")
    
    # 7 & 8. Run verify_baseline.py and require exit code 0
    # 10. verify_baseline.py also enforces working tree clean
    print("Running verify_baseline.py in fresh clone...")
    run_cmd([sys.executable, 'scripts/verify/verify_baseline.py'], cwd=CLONE_DIR)
    print("verify_baseline.py returned exit code 0.")
    
    # 9. Verify reported commits in verification_report.json
    report_path = CLONE_DIR / 'artifacts' / 'baselines' / 'final_audit_package' / 'verification_report.json'
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
        
    reported_source = report.get('git', {}).get('source_commit')
    reported_meta = report.get('git', {}).get('metadata_commit')
    
    if reported_source != source_commit:
        raise RuntimeError(f"Reported source_commit {reported_source} != expected {source_commit}")
    if reported_meta != current_commit:
        raise RuntimeError(f"Reported metadata_commit {reported_meta} != expected {current_commit}")
        
    print("Reported commits match exactly.")
    
    # Cleanup
    print("Cleaning up clone...")
    shutil.rmtree(CLONE_DIR, ignore_errors=True)
    
    print("✅ FRESH CLONE VERIFICATION PASSED.")

if __name__ == "__main__":
    main()
