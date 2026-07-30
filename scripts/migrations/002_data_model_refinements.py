import yaml
from pathlib import Path
import re

def remove_metadata_headers(data):
    for key in ['schema_version', 'profile_version', 'last_reviewed', 'owner', 'status']:
        data.pop(key, None)

def restructure_confidence(data):
    if 'confidence' in data:
        conf = data['confidence']
        # Map old confidence/status to new orthogonal model
        if conf == 'verified':
            data['confidence'] = 'verified'
            data['review_status'] = 'active'
        elif conf == 'supported':
            data['confidence'] = 'supported'
            data['review_status'] = 'active'
        elif conf == 'plausible':
            data['confidence'] = 'asserted'
            data['review_status'] = 'active'
        elif conf == 'needs_review':
            data['confidence'] = 'unknown'
            data['review_status'] = 'pending'
        elif conf == 'human_assertion':
            data['confidence'] = 'asserted'
            data['review_status'] = 'active'
            
def parse_date_string(date_str):
    # Very basic date string to ISO converter for the known data
    mapping = {
        'Jan 2014': '2014-01',
        'Nov 2016': '2016-11',
        'Feb 2024': '2024-02',
        'Jul 2018': '2018-07',
        'Aug 2020': '2020-08',
        'Sep 2022': '2022-09',
        'Aug 2023': '2023-08',
        'Aug 2020': '2020-08',
        'Jul 2022': '2022-07',
        'Aug 2017': '2017-08',
        'Jun 2018': '2018-06',
        'Nov 2016': '2016-11',
        'Aug 2017': '2017-08',
        '15 Sep 2025': '2025-09',
        '9 Jul 2026': '2026-07',
        '2007': '2007',
        '2009': '2009',
        '2004': '2004',
        'UNKNOWN — evidence required': 'UNKNOWN'
    }
    return mapping.get(date_str.strip(), date_str.strip())

def restructure_dates(data):
    date_field = 'years' if 'years' in data else 'date' if 'date' in data else None
    if not date_field: return
    
    val = data.pop(date_field)
    if '–' in val or '-' in val:
        parts = [p.strip() for p in re.split(r'–|-', val)]
        start = parse_date_string(parts[0])
        end = parse_date_string(parts[1])
        
        dates = {'start': {}}
        if start != 'UNKNOWN':
            dates['start']['date'] = start
            
        dates['end'] = {}
        if end.lower() == 'present':
            dates['end']['present'] = True
        elif end != 'UNKNOWN':
            dates['end']['date'] = end
            
        data['dates'] = dates
    else:
        # Fallback
        data['dates'] = {'start': {'date': parse_date_string(val)}, 'end': {'present': False}}

def extract_evidence(data, evidence_map):
    # Extracts evidence_id to a separate list, replaces source with primary_evidence_id
    ev_id = data.pop('evidence_id', None)
    source = data.pop('source', None)
    
    # Store primary evidence
    if ev_id and ev_id != 'N/A':
        data['primary_evidence_id'] = ev_id
        
        # Populate many-to-many links
        if data['id'] not in evidence_map:
            evidence_map[data['id']] = []
        evidence_map[data['id']].append(ev_id)
    else:
        data['primary_evidence_id'] = 'N/A'
        
def process_file(filepath, evidence_map, roles_map):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
        
    remove_metadata_headers(content)
    content['schema_version'] = 1.0
    
    # Process arrays of records
    for list_key in ['education_records', 'employment_records']:
        if list_key in content:
            for item in content[list_key]:
                restructure_confidence(item)
                restructure_dates(item)
                extract_evidence(item, evidence_map)
                
                # Role extraction for employment
                if list_key == 'employment_records':
                    title = item.pop('portfolio_display_title', 'Unknown Role')
                    # Find or create role
                    role_id = None
                    for rid, rtitle in roles_map.items():
                        if rtitle == title:
                            role_id = rid
                            break
                    if not role_id:
                        role_id = f"ROLE-{len(roles_map)+1:03d}"
                        roles_map[role_id] = title
                    item['role_id'] = role_id
                    
    # Process single objects
    if 'teaching_philosophy' in content:
        tp = content['teaching_philosophy']
        restructure_confidence(tp)
        tp.pop('source', None)
        tp.pop('evidence_id', None)

    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(content, f, sort_keys=False)

def main():
    root = Path(__file__).parent.parent.parent
    data_dir = root / 'career-data'
    facts_dir = data_dir / 'facts'
    narratives_dir = data_dir / 'narratives'
    
    evidence_map = {}
    roles_map = {}
    
    for yml in facts_dir.glob('*.yml'):
        if yml.name in ['evidence_links.yml', 'roles.yml']: continue
        print(f"Migrating {yml.name}")
        process_file(yml, evidence_map, roles_map)
        
    for yml in narratives_dir.glob('*.yml'):
        print(f"Migrating {yml.name}")
        process_file(yml, evidence_map, roles_map)
        
    # Write roles.yml
    if roles_map:
        roles_data = {'schema_version': 1.0, 'roles': []}
        for rid, title in roles_map.items():
            roles_data['roles'].append({'id': rid, 'title': title, 'description': ''})
        with open(facts_dir / 'roles.yml', 'w', encoding='utf-8') as f:
            yaml.dump(roles_data, f, sort_keys=False)
            
    # Write evidence_links.yml
    if evidence_map:
        links_data = {'schema_version': 1.0, 'evidence_links': []}
        for fid, eids in evidence_map.items():
            links_data['evidence_links'].append({'fact_id': fid, 'evidence_ids': eids})
        with open(facts_dir / 'evidence_links.yml', 'w', encoding='utf-8') as f:
            yaml.dump(links_data, f, sort_keys=False)
            
    print("Migration 002 complete.")

if __name__ == "__main__":
    main()
