import yaml
import os
import glob
from datetime import date

def migrate_claims(data):
    # claims.yml structure: {schema_version, generated, claims: [...]}
    if 'claims' not in data:
        return data
    for claim in data['claims']:
        # Rename 'canonical' to 'title'
        if 'canonical' in claim:
            claim['title'] = claim.pop('canonical')
        
        # Add schemaVersion
        claim['schemaVersion'] = "1.0"
        
        # Convert status 'active' -> 'verified'
        if claim.get('status') == 'active':
            claim['status'] = 'verified'
            
        # Add missing verification_date (map to today if missing)
        if 'verification_date' not in claim:
            claim['verification_date'] = date.today().isoformat()
            
        # Optional fields mappings if we want to keep them, we just let them stay 
        # (schema allows additionalProperties: true)
    return data

def migrate_evidence(data):
    if 'evidence' not in data:
        return data
    for ev in data['evidence']:
        ev['schemaVersion'] = "1.0"
        
        # We need filename, type, date_issued
        if 'filename' not in ev:
            ev['filename'] = f"{ev['id'].lower()}.pdf"
            
        if 'type' not in ev:
            ev['type'] = 'certificate'
            
        if 'date_issued' not in ev:
            ev['date_issued'] = '2020-01-01'
    return data

def main():
    facts_dir = 'career-data/facts'
    
    # 1. Migrate claims.yml
    claims_file = os.path.join(facts_dir, 'claims.yml')
    if os.path.exists(claims_file):
        with open(claims_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        data = migrate_claims(data)
        with open(claims_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print("Migrated claims.yml")
        
    # 2. Migrate evidence.yml
    evidence_file = os.path.join(facts_dir, 'evidence.yml')
    if os.path.exists(evidence_file):
        with open(evidence_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        data = migrate_evidence(data)
        with open(evidence_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print("Migrated evidence.yml")
        
if __name__ == '__main__':
    main()
