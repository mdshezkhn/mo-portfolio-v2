import sys
import subprocess
import os

def run_script(script_name):
    print(f"--- Running {script_name} ---")
    result = subprocess.run([sys.executable, f"scripts/{script_name}"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"[FAIL] {script_name} failed.")
        if result.stderr:
            print(result.stderr)
        return False
    print(f"[PASS] {script_name} passed.")
    return True

def main():
    audits = [
        "audit_claims.py",
        "audit_evidence.py"
    ]
    
    failures = 0
    for audit in audits:
        if not run_script(audit):
            failures += 1
            
    if failures > 0:
        print(f"\n{failures} audit(s) failed.")
        sys.exit(1)
        
    print("\nAll audits passed successfully.")

if __name__ == '__main__':
    main()
