import subprocess
import time
import sys

STAGES = [
    {"name": "Audit Claims", "cmd": ["python", "scripts/audit_claims.py"], "max_ms": 1000},
    {"name": "Validate ID Registry", "cmd": ["python", "scripts/validate_ids.py"], "max_ms": 500},
    {"name": "Validate Employment YAML", "cmd": ["python", "scripts/validate_yaml.py", "--file", "career-data/facts/employment.yml"], "max_ms": 1000},
    {"name": "Validate Education YAML", "cmd": ["python", "scripts/validate_yaml.py", "--file", "career-data/facts/education.yml"], "max_ms": 1000},
    {"name": "Resolve Graph", "cmd": ["python", "scripts/resolve_graph.py"], "max_ms": 1000},
    {"name": "Phase 3A: Build Domain Model", "cmd": ["python", "scripts/builders/build_domain_model.py"], "max_ms": 1000},
    {"name": "Phase 3A: Validate Domain Schema", "cmd": ["python", "scripts/validators/validate_schema.py"], "max_ms": 1000},
    {"name": "Phase 3A: Validate Domain Semantics", "cmd": ["python", "scripts/validators/validate_semantics.py"], "max_ms": 1000},
    {"name": "Phase 3B: Project CV VM", "cmd": ["python", "scripts/builders/project_cv_vm.py"], "max_ms": 1000},
    {"name": "Phase 3B: CV Contract Validation", "cmd": ["python", "-m", "pytest", "tests/contracts/test_cv_contract.py", "tests/contracts/test_domain_model_is_canonical.py", "-q"], "max_ms": 3000},
    {"name": "Validate Semantics", "cmd": ["python", "scripts/validate_semantics.py"], "max_ms": 500},
    {"name": "Metrics Engine", "cmd": ["python", "scripts/metrics_engine.py"], "max_ms": 500},
    {"name": "Content Quality Engine", "cmd": ["python", "scripts/content_quality_engine.py"], "max_ms": 1000},
    {"name": "Claim Selection Engine", "cmd": ["python", "scripts/selection_engine.py", "--market", "british"], "max_ms": 1000},
    {"name": "Compile Claim Register", "cmd": ["python", "scripts/compile_claim_register.py"], "max_ms": 500},
    {"name": "Compile Intermediate", "cmd": ["python", "scripts/compile_intermediate.py"], "max_ms": 500},
    {"name": "Policy Engine", "cmd": ["python", "scripts/policy_engine.py"], "max_ms": 500},
    {"name": "Phase 3C1: Render HTML CV", "cmd": ["python", "scripts/renderers/render_html_cv.py"], "max_ms": 1500},
    {"name": "Phase 3C1: HTML Reference Regression", "cmd": ["python", "-m", "pytest", "tests/reference/test_html_regression.py", "-q"], "max_ms": 3000},
    {"name": "Phase 3C2: Render MD CV", "cmd": ["python", "scripts/renderers/render_md_cv.py"], "max_ms": 1500},
    {"name": "Phase 3C2: Markdown Reference Regression", "cmd": ["python", "-m", "pytest", "tests/reference/test_markdown_regression.py", "-q"], "max_ms": 3000},
    {"name": "Cross-Artifact Verification", "cmd": ["python", "scripts/verify_cross_artifact.py"], "max_ms": 500},
    {"name": "Compiler Report", "cmd": ["python", "scripts/build_compiler_report.py"], "max_ms": 500},
    {"name": "RC-7 Privacy Gate", "cmd": ["python", "scripts/verify/privacy_gate.py"], "max_ms": 1500},
    {"name": "RC-8 Security Gate", "cmd": ["python", "scripts/verify/security_gate.py"], "max_ms": 1500},
    {"name": "RC-9 Hygiene Gate", "cmd": ["python", "scripts/verify/hygiene_gate.py"], "max_ms": 1500},
    {"name": "RC-10 Governance Integrity Gate", "cmd": ["python", "scripts/verify/governance_gate.py"], "max_ms": 500},
    {"name": "Security Fixture Regression Tests", "cmd": ["python", "-m", "pytest", "tests/test_security_governance_fixtures.py", "-q"], "max_ms": 3000},
    {"name": "Architecture Rules Test", "cmd": ["python", "-m", "pytest", "tests/test_architecture_rules.py", "-q"], "max_ms": 3000},
    {"name": "Snapshot Regression Tests", "cmd": ["python", "-m", "pytest", "tests/test_snapshot_regression.py", "-q"], "max_ms": 10000}
]

def run_pipeline():
    print("====================================")
    print(" Starting CI/CD Pipeline Validation ")
    print("====================================\n")
    
    total_start = time.time()
    
    for stage in STAGES:
        print(f"Running: {stage['name']}...")
        start_t = time.time()
        
        try:
            import os
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            result = subprocess.run(stage["cmd"], capture_output=True, text=True, encoding="utf-8", env=env)
            elapsed_ms = (time.time() - start_t) * 1000
            
            if result.returncode != 0:
                print(f"[FAIL] {stage['name']} failed in {elapsed_ms:.0f} ms (Exit Code {result.returncode})")
                print("--- STDOUT ---")
                print(result.stdout)
                print("--- STDERR ---")
                print(result.stderr)
                sys.exit(1)
                
            status = "PASS"
            if elapsed_ms > stage["max_ms"]:
                status = f"WARN (Exceeded {stage['max_ms']}ms gate)"
                
            print(f"[{status}] {stage['name']} completed in {elapsed_ms:.0f} ms\n")
            
        except Exception as e:
            print(f"[ERROR] Failed to run {stage['name']}: {e}")
            sys.exit(1)
            
    total_elapsed = time.time() - total_start
    print("====================================")
    print(f" CI/CD Pipeline PASSED in {total_elapsed:.2f} s ")
    print("====================================")
    
if __name__ == "__main__":
    run_pipeline()
