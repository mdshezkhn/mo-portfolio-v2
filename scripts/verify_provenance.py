import json
from pathlib import Path
import sys

def verify_provenance():
    artifacts_dir = Path("artifacts")
    vm_path = artifacts_dir / "professional_profile_vm.json"
    graph_path = artifacts_dir.parent / "career-data" / "intermediate" / "resolved_graph.json"
    
    if not vm_path.exists() or not graph_path.exists():
        print("Missing view model or resolved graph.")
        sys.exit(1)
        
    with open(vm_path, "r", encoding="utf-8") as f:
        vm = json.load(f)
        
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
        
    # Get all rendered claims
    rendered_claims = set()
    for stmt in vm.get('executive_summary', []):
        rendered_claims.add(stmt)
    for exp in vm.get('experience', []):
        for stmt in exp.get('highlights', []):
            rendered_claims.add(stmt)
            
    if not rendered_claims:
        print("[PASS] No claims rendered.")
        sys.exit(0)
        
    # Map statements to claim IDs
    statement_to_claim_id = {}
    for eid, entity in graph['entities'].items():
        if entity.get('entity_type') == 'claim':
            statement_to_claim_id[entity.get('statement')] = eid
            
    edges = graph['edges']
    errors = []
    
    for stmt in rendered_claims:
        cid = statement_to_claim_id.get(stmt)
        if not cid:
            errors.append(f"Rendered claim statement not found in canonical graph: '{stmt}'")
            continue
            
        # Check if this claim has at least one SUPPORTED_BY edge pointing to an EVIDENCE node
        has_evidence = False
        for edge in edges:
            if edge.get('from') == cid and edge.get('type') == 'SUPPORTED_BY':
                target_id = edge.get('to')
                target_entity = graph['entities'].get(target_id)
                if target_entity and target_entity.get('entity_type') == 'evidence':
                    has_evidence = True
                    break
                    
        if not has_evidence:
            errors.append(f"Claim [{cid}] is rendered but does NOT resolve to any verified evidence record!")
            
    if errors:
        print("[FAIL] Golden Provenance Criteria Failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
        
    print("[PASS] 100% of rendered claims resolve to verified evidence records.")
    
if __name__ == "__main__":
    verify_provenance()
