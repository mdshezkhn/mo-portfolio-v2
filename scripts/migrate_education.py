import yaml
from pathlib import Path

def pad_id(prefix, raw_id):
    if raw_id.startswith(prefix + '-') and len(raw_id) == len(prefix) + 4:
        return prefix + '-0' + raw_id[len(prefix)+1:]
    return raw_id

legacy_path = Path('career-data/legacy/facts/education.yml')
facts_path = Path('career-data/facts/education.yml')
edges_path = Path('career-data/relationships/edges.yml')

with open(legacy_path, 'r', encoding='utf-8') as f:
    legacy_data = yaml.safe_load(f)

new_records = []
new_edges = []

for edu in legacy_data.get('education_records', []):
    edu_id = pad_id('EDU', edu['id'])
    
    # Extract edge info
    inst_id = pad_id('INST', edu.get('institution_id', ''))
    ev_id = edu.get('primary_evidence_id', '')
    
    if inst_id:
        new_edges.append({
            "from": edu_id,
            "to": inst_id,
            "type": "STUDIED_AT"
        })
        
    if ev_id and ev_id != 'N/A':
        new_edges.append({
            "from": edu_id,
            "to": ev_id,
            "type": "SUPPORTED_BY"
        })
        
    # Clean the education record itself
    new_record = {
        "id": edu_id,
        "entity_type": "education",
        "degree": edu["degree"],
        "dates": edu["dates"],
        "confidence": edu["confidence"],
        "review_status": edu["review_status"],
        "publication": edu["publication"]
    }
    
    # Preserve institution recognition status if present
    if 'institution_recognition_status' in edu:
        # User specified formalizing Harris University case
        new_record["institution_recognition_status"] = edu["institution_recognition_status"].lower()
    
    # Normalize review/confidence status values to match updated schemas
    if new_record['confidence'] == 'unknown':
        new_record['confidence'] = 'asserted'  # Fallback to a valid enum
    if new_record['review_status'] == 'active':
        new_record['review_status'] = 'approved' # Fallback to a valid enum
        
    new_records.append(new_record)

# Sort chronologically by start date
# UNKNOWN sorts after numbers usually, but let's handle it gracefully
def get_start_date(r):
    date_str = r['dates']['start']['date']
    return date_str if date_str != 'UNKNOWN' else '9999'

new_records.sort(key=get_start_date)

with open(facts_path, 'w', encoding='utf-8') as f:
    yaml.dump({"education_records": new_records}, f, default_flow_style=False, sort_keys=False)

# Append to edges.yml
with open(edges_path, 'r', encoding='utf-8') as f:
    edges_data = yaml.safe_load(f)
    
if not edges_data or 'edges' not in edges_data or not edges_data['edges']:
    edges_data = {"edges": []}
    
edges_data['edges'].extend(new_edges)

with open(edges_path, 'w', encoding='utf-8') as f:
    yaml.dump(edges_data, f, default_flow_style=False, sort_keys=False)

print(f"Migrated {len(new_records)} education records and added {len(new_edges)} new edges.")
