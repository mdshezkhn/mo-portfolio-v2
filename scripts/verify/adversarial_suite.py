import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

def run_cmd(cmd, cwd=BASE_DIR, fail_ok=False):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if not fail_ok and res.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{res.stderr}")
    return res

def is_clean():
    res = run_cmd(['git', 'status', '--porcelain', '--ignore-submodules'])
    return len(res.stdout.strip()) == 0

def restore_repo():
    run_cmd(['git', 'checkout', '--', '.'])
    run_cmd(['git', 'clean', '-fd'])
    # also restore baseline_metadata.json if it was mutated
    run_cmd(['git', 'checkout', 'HEAD', '--', 'artifacts/baselines/cv_master/baseline_metadata.json'], fail_ok=True)

class AdversarialSuite:
    def __init__(self):
        self.results = []
        
    def execute_test(self, name, mutation_fn, expected_fail=True):
        print(f"\n--- Running Attack: {name} ---")
        if not is_clean():
            print("FATAL: Repo not clean before test.")
            sys.exit(1)
            
        # 1. Apply mutation
        mutation_fn()
        mutation_applied = True
        print("Mutation applied.")
        
        # 2. Run verifier
        print("Running verify_baseline.py...")
        res = run_cmd([sys.executable, 'scripts/verify/verify_baseline.py'], fail_ok=True)
        
        mutation_detected = (res.returncode != 0) if expected_fail else (res.returncode == 0)
        if expected_fail:
            print(f"Verifier exit code: {res.returncode}")
        
        # 3. Restore
        restore_repo()
        working_tree_restored = is_clean()
        
        passed = mutation_applied and mutation_detected and working_tree_restored
        
        self.results.append({
            'attack': name,
            'mutation_applied': mutation_applied,
            'mutation_detected': mutation_detected,
            'exit_code': res.returncode,
            'working_tree_restored': working_tree_restored,
            'passed': passed
        })
        
        if passed:
            print("✅ TEST PASSED (Attack correctly caught & repo restored).")
        else:
            print("❌ TEST FAILED.")
            print(res.stdout)
            print(res.stderr)

def mutate_file(path, search, replace):
    p = BASE_DIR / path
    content = p.read_text(encoding='utf-8')
    if search not in content:
        raise ValueError(f"Search string not found in {path}")
    p.write_text(content.replace(search, replace), encoding='utf-8')

def append_to_file(path, text):
    p = BASE_DIR / path
    with open(p, 'a', encoding='utf-8') as f:
        f.write(text)

def main():
    if not is_clean():
        print("Repo must be clean before starting.")
        sys.exit(1)
        
    suite = AdversarialSuite()
    
    # 1. Wrong EMP->E edge
    suite.execute_test('Wrong EMP->E edge', 
        lambda: append_to_file('career-data/relationships/edges.yml', '\n  - {from: EMP-2001, to: E-3005, type: SUPPORTED_BY}\n'))
        
    # 2. Missing evidence
    suite.execute_test('Missing evidence (CLAIM-1003 -> E-3006)',
        lambda: append_to_file('career-data/relationships/edges.yml', '\n  - {from: CLAIM-1003, to: E-3006, type: SUPPORTED_BY}\n'))
        
    # 3. Nonexistent node
    suite.execute_test('Nonexistent node (E-9999)',
        lambda: append_to_file('career-data/relationships/edges.yml', '\n  - {from: EMP-2003, to: E-9999, type: SUPPORTED_BY}\n'))
        
    # 4. Altered assertion
    suite.execute_test('Altered assertion date',
        lambda: mutate_file('career-data/facts/evidence_assertions.yml', 'date: "2018-09-01"', 'date: "2018-09-02"'))
        
    # 5. Unauthorized VM claim (Policy bypass)
    # The builder checks `if ch['claim_id'] in approved_claims:`
    # We mutate it to bypass verification check
    suite.execute_test('Policy bypass (Unauthorized VM claim)',
        lambda: mutate_file('scripts/builders/build_domain_model.py', 
            "if ch['claim_id'] in approved_claims:",
            "if True: # Bypass!"))
            
    # 6. Historical highlight in VM
    suite.execute_test('Historical highlight in VM',
        lambda: mutate_file('scripts/builders/build_domain_model.py',
            "if isinstance(ch, str):\n                continue",
            "if isinstance(ch, str):\n                bullets.append(ch)\n                continue"))
            
    # 7. HTML tampering (baseline source template)
    suite.execute_test('HTML tampering (template)',
        lambda: append_to_file('templates/cv/base.html', '<!-- tampered -->'))
        
    # 8. Source drift (dependency file)
    suite.execute_test('Source drift (employment.yml)',
        lambda: append_to_file('career-data/facts/employment.yml', '\n# drifted\n'))
        
    # 9. Metadata tampering
    suite.execute_test('Metadata tampering',
        lambda: mutate_file('artifacts/baselines/cv_master/baseline_metadata.json', 
            '"cv_master_html":', '"cv_master_html": "invalid_hash", "old":'))

    print("\n=== ADVERSARIAL SUITE RESULTS ===")
    all_passed = True
    for r in suite.results:
        status = "✅" if r['passed'] else "❌"
        print(f"{status} {r['attack']}")
        if not r['passed']:
            all_passed = False
            print(f"    mutation_applied: {r['mutation_applied']}")
            print(f"    mutation_detected: {r['mutation_detected']} (exit {r['exit_code']})")
            print(f"    working_tree_restored: {r['working_tree_restored']}")
            
    if not all_passed:
        sys.exit(1)
    print("ALL ATTACKS DETECTED SUCCESSFULLY.")
    
if __name__ == "__main__":
    main()
