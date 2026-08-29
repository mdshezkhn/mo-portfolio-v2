import json
import yaml
from pathlib import Path

edges_path = Path('career-data/relationships/edges.yml')
claims_path = Path('career-data/facts/claims.yml')
emp_path = Path('career-data/facts/employment.yml')
ev_assert_path = Path('career-data/facts/evidence_assertions.yml')

with open(edges_path, 'r', encoding='utf-8') as f:
    edges = yaml.safe_load(f).get('edges', [])
with open(claims_path, 'r', encoding='utf-8') as f:
    claims = {c['id']: c for c in yaml.safe_load(f).get('claims', [])}
with open(emp_path, 'r', encoding='utf-8') as f:
    emps = {e['id']: e for e in yaml.safe_load(f).get('employment_records', [])}
with open(ev_assert_path, 'r', encoding='utf-8') as f:
    ev_asserts = {e['evidence_id']: e for e in yaml.safe_load(f).get('evidence_assertions', [])}

for emp_id in ['EMP-2001', 'EMP-2002', 'EMP-2003']:
    print(f'=== {emp_id} ===')
    supporting_claims = [e['from'] for e in edges if e['to'] == emp_id and e['type'] == 'SUPPORTED_BY']
    print(f'Supporting claims: {supporting_claims}')
    
    direct_evidence = [e['to'] for e in edges if e['from'] == emp_id and e['type'] == 'SUPPORTED_BY' and e['to'].startswith('E-')]
    print(f'Direct evidence: {direct_evidence}')
    
    with open('artifacts/cv_view_models/portfolio.json', 'r', encoding='utf-8') as f:
        portfolio = json.load(f)
    
    emp_vm = next((x for x in portfolio['experience'] if x['id'] == emp_id), None)
    if emp_vm:
        print(f'Rendered bullets: {len(emp_vm.get("bullets", []))}')
        for b in emp_vm.get('bullets', []):
            print(f'  - {b}')
    else:
        print('Not found in portfolio.json')
    print()
