import yaml
import json
from pathlib import Path

BASE_DIR = Path('c:/Users/Mohammed Shehzad/Documents/Mo Digital Portfolio')

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

edges = load_yaml(BASE_DIR / 'career-data/relationships/edges.yml').get('edges', [])
emps = load_yaml(BASE_DIR / 'career-data/facts/employment.yml').get('employment_records', [])

print("EMP | Org Evidence | Dates Evidence | Claims | Claim Evidence")
for emp in emps:
    if emp.get('review_status') == 'approved':
        emp_id = emp['id']
        org = emp.get('employer_id')
        dates = emp.get('dates')
        
        # What evidence supports this EMP directly?
        emp_ev = [e['to'] for e in edges if e['from'] == emp_id and e['type'] == 'SUPPORTED_BY']
        
        # What claims support this EMP directly?
        claims = [e['from'] for e in edges if e['to'] == emp_id and e['type'] == 'SUPPORTED_BY']
        
        print(f"{emp_id} | org:{org} -> ev:{emp_ev} | dates:{dates} -> ev:{emp_ev} | claims:{claims}")
