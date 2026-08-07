import yaml
from pathlib import Path

def pad_id(prefix, raw_id):
    if raw_id.startswith(prefix + '-') and len(raw_id) == len(prefix) + 4:
        return prefix + '-0' + raw_id[len(prefix)+1:]
    return raw_id

legacy_path = Path('career-data/legacy/facts/employment.yml')
facts_path = Path('career-data/facts/employment.yml')
edges_path = Path('career-data/relationships/edges.yml')

with open(legacy_path, 'r', encoding='utf-8') as f:
    legacy_data = yaml.safe_load(f)

new_records = []
new_edges = []

for emp in legacy_data.get('employment_records', []):
    emp_id = pad_id('EMP', emp['id'])
    
    # Extract edge info
    org_id = pad_id('ORG', emp.get('employer_id', ''))
    role_id = pad_id('ROLE', emp.get('role_id', ''))
    ev_id = emp.get('primary_evidence_id', '')
    
    if org_id:
        new_edges.append({
            "from": emp_id,
            "to": org_id,
            "type": "WORKED_AT"
        })
    
    if role_id:
        new_edges.append({
            "from": emp_id,
            "to": role_id,
            "type": "HAS_ROLE"
        })
        
    if ev_id and ev_id != 'N/A':
        new_edges.append({
            "from": emp_id,
            "to": ev_id,
            "type": "SUPPORTED_BY"
        })
        
    # Clean the employment record itself
    new_record = {
        "id": emp_id,
        "entity_type": "employment",
        "dates": emp["dates"],
        "location": emp["location"],
        "confidence": emp["confidence"],
        "review_status": emp["review_status"]
    }
    
    # Normalize review/confidence status values to match updated schemas
    if new_record['confidence'] == 'unknown':
        new_record['confidence'] = 'asserted'  # Fallback to a valid enum
    if new_record['review_status'] == 'active':
        new_record['review_status'] = 'approved' # Fallback to a valid enum
        
    new_records.append(new_record)

# Sort chronologically by start date
new_records.sort(key=lambda x: x['dates']['start']['date'])

with open(facts_path, 'w', encoding='utf-8') as f:
    yaml.dump({"employment_records": new_records}, f, default_flow_style=False, sort_keys=False)

# Append to edges.yml
with open(edges_path, 'r', encoding='utf-8') as f:
    edges_data = yaml.safe_load(f)
    
if not edges_data or 'edges' not in edges_data or not edges_data['edges']:
    edges_data = {"edges": []}
    
edges_data['edges'].extend(new_edges)

with open(edges_path, 'w', encoding='utf-8') as f:
    yaml.dump(edges_data, f, default_flow_style=False, sort_keys=False)

print(f"Migrated {len(new_records)} employment records and added {len(new_edges)} new edges.")
