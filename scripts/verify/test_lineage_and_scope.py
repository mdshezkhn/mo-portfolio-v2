import json
import yaml
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.parent

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def test_lineage_and_scope():
    print("Running Lineage & Scope Tests...")
    
    # 1. Load Canonical Data
    emp_path = BASE_DIR / 'career-data' / 'facts' / 'employment.yml'
    canonical_emp = load_yaml(emp_path).get('employment_records', [])
    
    # In Master scope (exhaustive), every verified EMP must appear
    verified_emps = [e for e in canonical_emp if e.get('review_status') == 'approved']
    
    # 2. Load View Model
    vm_path = BASE_DIR / 'artifacts' / 'cv_view_models' / 'master.json'
    if not vm_path.exists():
        print("FAIL: master.json view model not found.")
        sys.exit(1)
        
    with open(vm_path, 'r', encoding='utf-8') as f:
        vm = json.load(f)
        
    # --- Test 1: Employment Lineage Invariant ---
    print("Test 1: Employment Lineage Coverage")
    # For exhaustive Master scope, all verified employers must have a traceable representation
    # Since the current view model doesn't embed canonical IDs, we test entity/claim coverage by counting and matching
    
    canonical_employer_count = len(set([e['employer_id'] for e in verified_emps]))
    vm_employers = [e['company'] for e in vm.get('experience', [])]
    
    # Actually, the user asked for "Every employment fact within Master presentation scope must have exactly one traceable representation"
    # To test this perfectly, we need IDs in the view model. But currently they aren't there.
    # We can at least check if the number of distinct employment facts equals the coverage.
    
    # If the architecture says 7 facts, we must see 7 facts represented.
    # We will look for missing canonical facts by checking if their dates or unique highlights appear in the VM.
    
    missing_facts = []
    for emp in verified_emps:
        # check if this emp is represented in the view model by finding one of its highlights
        highlights = emp.get('cv_highlights', [])
        found = False
        for exp in vm.get('experience', []):
            vm_bullets = exp.get('bullets', [])
            # See if any of the canonical highlights from this emp are in the VM
            if any(h in b for h in highlights for b in vm_bullets):
                found = True
                break
        if not found:
            missing_facts.append(emp['id'])
            
    if missing_facts:
        print(f"FAIL: Canonical employment facts {missing_facts} have NO traceable representation in the view model.")
        sys.exit(1)
    else:
        print("PASS: Employment Lineage Coverage")

    # --- Test 2: Bullet / Claim Lineage Invariant ---
    print("Test 2: Bullet Lineage Coverage (Master Scope)")
    canonical_highlights = []
    for emp in verified_emps:
        canonical_highlights.extend(emp.get('cv_highlights', []))
        
    vm_bullets = []
    for exp in vm.get('experience', []):
        vm_bullets.extend(exp.get('bullets', []))
        
    # In exhaustive scope, all canonical highlights must appear
    missing_bullets = []
    for ch in canonical_highlights:
        if not any(ch in vb or vb in ch for vb in vm_bullets):
            missing_bullets.append(ch)
            
    if missing_bullets:
        print(f"FAIL: {len(missing_bullets)} canonical claims in Master scope are missing from the view model.")
        sys.exit(1)
    else:
        print("PASS: Bullet Lineage Coverage")
        
    # --- Test 3: Date Provenance ---
    print("Test 3: Date Provenance Validation")
    # All dates in the view model should trace back to canonical dates
    canonical_start_dates = [e['dates'].get('start') for e in verified_emps if 'start' in e['dates']]
    canonical_end_dates = [e['dates'].get('end') for e in verified_emps if 'end' in e['dates']]
    canonical_date_years = set()
    for d in canonical_start_dates + canonical_end_dates:
        if str(d) != 'Present':
            canonical_date_years.add(str(d)[:4])
            
    vm_dates = [e['date'] for e in vm.get('experience', [])]
    for vd in vm_dates:
        # Simple extraction of years
        years_in_vd = [word for word in vd.replace('-', ' ').replace('–', ' ').split() if word.isdigit() and len(word)==4]
        for y in years_in_vd:
            if y not in canonical_date_years:
                print(f"FAIL: View model date '{vd}' contains year '{y}' not found in canonical dates.")
                sys.exit(1)
    print("PASS: Date Provenance")
    
    print("All Lineage & Scope tests passed.")

if __name__ == '__main__':
    test_lineage_and_scope()
