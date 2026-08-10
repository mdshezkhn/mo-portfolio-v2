import subprocess
import sys
from pathlib import Path
import yaml
import shutil
import os

BASE_DIR = Path(__file__).parent.parent.parent
EDGES_PATH = BASE_DIR / "career-data" / "relationships" / "edges.yml"
BACKUP_PATH = BASE_DIR / "career-data" / "relationships" / "edges_backup.yml"

def run_build(expect_fail=False):
    result = subprocess.run([sys.executable, str(BASE_DIR / 'scripts' / 'builders' / 'build_domain_model.py')], capture_output=True, text=True)
    if expect_fail:
        if result.returncode == 0:
            print("FAIL: Expected build to fail, but it succeeded.")
            print(result.stdout)
            sys.exit(1)
    else:
        if result.returncode != 0:
            print("FAIL: Expected build to succeed, but it failed.")
            print(result.stderr)
            sys.exit(1)
    return result

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
        
def save_yaml(p, data):
    with open(p, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False)

def test_mutations():
    print("Running Provenance Mutation Tests...")
    shutil.copy(EDGES_PATH, BACKUP_PATH)
    
    try:
        # 1. Clean build
        print("Testing: Clean graph")
        run_build(expect_fail=False)
        
        # 2. Orphaned claim edge (nonexistent evidence)
        print("Testing: Active edge -> nonexistent evidence")
        edges_doc = load_yaml(EDGES_PATH)
        edges_doc['edges'].append({'from': 'CLAIM-1003', 'to': 'E-9999', 'type': 'SUPPORTED_BY'})
        save_yaml(EDGES_PATH, edges_doc)
        run_build(expect_fail=True)
        
        # 3. Contradictory edge (E-3005 on EMP-2001)
        print("Testing: Active edge -> wrong employment assertions")
        edges_doc = load_yaml(BACKUP_PATH)
        edges_doc['edges'].append({'from': 'EMP-2001', 'to': 'E-3005', 'type': 'SUPPORTED_BY'})
        save_yaml(EDGES_PATH, edges_doc)
        run_build(expect_fail=True)
        
        # Restore for remaining logic tests
        shutil.copy(BACKUP_PATH, EDGES_PATH)
        
        # Check VM outcomes
        run_build(expect_fail=False)
        vm_path = BASE_DIR / 'artifacts' / 'cv_view_models' / 'master.json'
        with open(vm_path, 'r', encoding='utf-8') as f:
            import json
            vm = json.load(f)
            
        # 4. EMP-2003 empty bullets
        emp2003_exp = [e for e in vm.get('experience', []) if '2018-07 - 2020-08' in e.get('date', '')]
        if not emp2003_exp or len(emp2003_exp[0]['bullets']) > 0:
            print("FAIL: EMP-2003 did not render with 0 bullets.")
            sys.exit(1)
            
        # 5. EMP-2006 excluded because it has no evidence
        emp2006_exp = [e for e in vm.get('experience', []) if '2024-02 - 2026-07' in e.get('date', '')]
        if emp2006_exp:
            print("FAIL: EMP-2006 should be excluded because it has no evidence edges.")
            sys.exit(1)
            
        print("PASS: Provenance Mutations.")
        
    finally:
        shutil.copy(BACKUP_PATH, EDGES_PATH)
        os.remove(BACKUP_PATH)

if __name__ == "__main__":
    test_mutations()
