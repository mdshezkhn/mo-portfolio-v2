import json
import sys
from pathlib import Path

def validate_semantics(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        domain = json.load(f)
        
    errors = []
    
    # 1. Unique IDs
    ids = set()
    for e in domain.get("employment", []):
        if e["id"] in ids:
            errors.append(f"Duplicate ID: {e['id']}")
        ids.add(e["id"])
        
    for q in domain.get("education", []):
        if q["id"] in ids:
            errors.append(f"Duplicate ID: {q['id']}")
        ids.add(q["id"])
        
    for c in domain.get("claims", []):
        if c["id"] in ids:
            errors.append(f"Duplicate ID: {c['id']}")
        ids.add(c["id"])
        
    # 2. Employment Dates Normalized and Non-Overlapping? (Currently skipping non-overlapping as they may overlap, but ensuring normalized format)
    import re
    date_regex = re.compile(r'^\d{4}-\d{2}(-\d{2})?$')
    for e in domain.get("employment", []):
        start = e.get("dates", {}).get("start_date")
        if start and not date_regex.match(start):
            errors.append(f"Invalid date format in employment {e['id']}: {start}")
            
    # 3. Valid Verification Levels
    valid_confidences = {"V1", "V2", "V3", "V4", "V5", "unverified", "supported", "verified"}
    for e in domain.get("employment", []):
        conf = e.get("metadata", {}).get("confidence")
        if conf and conf not in valid_confidences:
            errors.append(f"Invalid confidence {conf} in employment {e['id']}")
            
    # 4. Sorting (Newest First)
    employments = domain.get("employment", [])
    for i in range(len(employments) - 1):
        d1 = employments[i].get("dates", {}).get("start_date", "")
        d2 = employments[i+1].get("dates", {}).get("start_date", "")
        if d1 < d2:
            errors.append(f"Employment records not sorted newest-first: {employments[i]['id']} vs {employments[i+1]['id']}")
            
    if errors:
        print("Semantic validation FAIL:")
        for err in errors:
            print(f" - {err}")
        return False
        
    print("Semantic validation PASS")
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="artifacts/profile_domain_model.json")
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent.parent
    data_path = root / args.data
    
    if not validate_semantics(data_path):
        sys.exit(1)
