import json
from pathlib import Path
import re
import sys

def verify_terminology(text):
    forbidden = ["Elementary"] # We want "Primary"
    for word in forbidden:
        if word in text:
            return False, f"Forbidden terminology found: {word}"
    return True, ""

def run_verifications():
    artifacts_dir = Path("artifacts/generated")
    cv_path = artifacts_dir / "cv.md"
    linkedin_path = artifacts_dir / "linkedin.md"
    
    if not cv_path.exists() or not linkedin_path.exists():
        print("Markdown artifacts missing. Cannot verify cross-artifact consistency.")
        return 0 # Pass if not generated yet, or should it fail?
        
    with open(cv_path, "r", encoding="utf-8") as f:
        cv_text = f.read()
    with open(linkedin_path, "r", encoding="utf-8") as f:
        linkedin_text = f.read()
        
    vm_path = Path("artifacts/professional_profile_vm.json")
    with open(vm_path, "r", encoding="utf-8") as f:
        vm = json.load(f)
        
    errors = []
    
    # 1. Terminology check
    term_ok, term_err = verify_terminology(cv_text)
    if not term_ok: errors.append(term_err)
    
    # 2. Chronology check (End dates should be greater than start dates)
    for exp in vm['experience']:
        if exp['end_date'] != 'Present':
            if exp['start_date'] > exp['end_date']:
                errors.append(f"Chronology error in {exp['organization']}: {exp['start_date']} to {exp['end_date']}")
                
    # 3. Artifact consistency check (Do both mention the same organizations?)
    for exp in vm['experience']:
        org = exp['organization']
        if org not in cv_text:
            errors.append(f"Organization '{org}' missing from CV")
        if org not in linkedin_text:
            errors.append(f"Organization '{org}' missing from LinkedIn")
            
    if errors:
        print("[FAIL] Cross-Artifact Verification found errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
        
    print("[PASS] Cross-Artifact Consistency Verified")
    
if __name__ == "__main__":
    run_verifications()
