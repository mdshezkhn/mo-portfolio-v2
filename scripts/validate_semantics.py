import json
import sys
from pathlib import Path

def validate_employment(graph):
    errors = []
    
    # Check coverage for each employment record
    for eid, entity in graph['entities'].items():
        if entity.get('entity_type') == 'employment':
            
            # 1. Relationship coverage
            edges_out = graph['indexes']['by_source'].get(eid, [])
            worked_at = [e for e in edges_out if e['type'] == 'WORKED_AT']
            has_role = [e for e in edges_out if e['type'] == 'HAS_ROLE']
            
            if len(worked_at) != 1:
                errors.append(f"{eid} has {len(worked_at)} WORKED_AT edges (must have exactly 1)")
            else:
                org_id = worked_at[0]['to']
                if org_id not in graph['entities']:
                    errors.append(f"{eid} references non-existent organisation {org_id}")
                    
            if len(has_role) < 1:
                errors.append(f"{eid} has {len(has_role)} HAS_ROLE edges (must have at least 1)")
            else:
                for edge in has_role:
                    role_id = edge['to']
                    if role_id not in graph['entities']:
                        errors.append(f"{eid} references non-existent role {role_id}")
                        
            # 2. Date Constraints
            dates = entity.get('dates', {})
            start_date_str = dates.get('start', {}).get('date')
            end_date_str = dates.get('end', {}).get('date')
            is_present = dates.get('end', {}).get('present', False)
            
            if is_present and end_date_str:
                errors.append(f"{eid} is marked as present but has an end date {end_date_str}")
                
            if start_date_str and end_date_str and start_date_str != 'UNKNOWN' and end_date_str != 'UNKNOWN':
                # Basic string comparison works for ISO dates 'YYYY-MM'
                if end_date_str < start_date_str:
                    errors.append(f"{eid} has end date ({end_date_str}) before start date ({start_date_str})")
                    
    return errors

def validate_semantics(intermediate_dir):
    graph_path = intermediate_dir / 'resolved_graph.json'
    if not graph_path.exists():
        print(f"Error: {graph_path} not found.")
        sys.exit(1)
        
    with open(graph_path, 'r', encoding='utf-8') as f:
        graph = json.load(f)
        
    errors = []
    
    # 1. Check Identity Node
    identities = [k for k, v in graph['entities'].items() if v.get('entity_type') == 'identity' or v.get('entity_type') == 'entity']
    if len(identities) == 0:
        errors.append("No canonical identity node found.")
    elif len(identities) > 1:
        errors.append("Multiple canonical identity nodes found.")
        
    # 2. Check Employment
    emp_errors = validate_employment(graph)
    errors.extend(emp_errors)
        
    if errors:
        print("Semantic Validation FAILED:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
        
    print("Semantic Validation Passed on resolved_graph.json.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--intermediate-dir", default="career-data/intermediate")
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent
    intermediate_dir = root / args.intermediate_dir
    validate_semantics(intermediate_dir)
