import yaml
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.parent
CAREER_DATA = BASE_DIR / "career-data"

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_graph():
    print("Running Graph Validation...")
    
    # Load all nodes
    edges_data = load_yaml(CAREER_DATA / "relationships" / "edges.yml").get("edges", [])
    emps_data = load_yaml(CAREER_DATA / "facts" / "employment.yml").get("employment_records", [])
    
    claims_path = CAREER_DATA / "facts" / "claims.yml"
    claims_data = load_yaml(claims_path).get("claims", []) if claims_path.exists() else []
    
    golden_claims_path = CAREER_DATA / "golden" / "E-001" / "source" / "facts" / "claims.yml"
    golden_claims_data = load_yaml(golden_claims_path).get("claims", []) if golden_claims_path.exists() else []
    
    all_claims = {c['id']: c for c in claims_data + golden_claims_data}
    all_emps = {e['id']: e for e in emps_data}
    
    ev_assertions_path = CAREER_DATA / "facts" / "evidence_assertions.yml"
    ev_assertions = load_yaml(ev_assertions_path).get("evidence_assertions", []) if ev_assertions_path.exists() else []
    all_ev = {ev['evidence_id']: ev for ev in ev_assertions}
    
    errors = []
    
    # 1. Orphan Checks
    for edge in edges_data:
        from_id = edge['from']
        to_id = edge['to']
        
        # We only strictly validate EMP, CLAIM, and E-* IDs for now
        if from_id.startswith("CLAIM-") and from_id not in all_claims:
            errors.append(f"ORPHANED EDGE: 'from' {from_id} does not exist.")
        if from_id.startswith("EMP-") and from_id not in all_emps:
            errors.append(f"ORPHANED EDGE: 'from' {from_id} does not exist.")
            
        if (from_id.startswith("EMP-") or from_id.startswith("CLAIM-")) and to_id.startswith("E-"):
            if to_id not in all_ev:
                errors.append(f"ORPHANED EDGE: 'to' {to_id} does not exist in evidence_assertions.")
        
    # 2. Contradiction Checks
    # For every EMP -> E-* edge, the assertions must match
    for edge in edges_data:
        if edge['from'].startswith("EMP-") and edge['to'].startswith("E-"):
            emp = all_emps.get(edge['from'])
            ev = all_ev.get(edge['to'])
            if emp and ev:
                ev_emp_assertions = ev.get('assertions', {}).get('employment', {})
                # Check org
                if emp.get('employer_id') != ev_emp_assertions.get('employer_id'):
                    errors.append(f"CONTRADICTION: {edge['from']} employer_id {emp.get('employer_id')} != {edge['to']} {ev_emp_assertions.get('employer_id')}")
                
                # Check dates
                emp_start = emp.get('dates', {}).get('start')
                emp_end = emp.get('dates', {}).get('end')
                ev_start = ev_emp_assertions.get('dates', {}).get('start')
                ev_end = ev_emp_assertions.get('dates', {}).get('end')
                
                if emp_start != ev_start or emp_end != ev_end:
                    errors.append(f"CONTRADICTION: {edge['from']} dates {emp_start}-{emp_end} != {edge['to']} {ev_start}-{ev_end}")

    if errors:
        print("GRAPH VALIDATION FAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
        
    print("GRAPH VALIDATION PASSED.")

if __name__ == "__main__":
    validate_graph()
