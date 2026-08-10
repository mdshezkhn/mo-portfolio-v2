import json
import yaml
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path('c:/Users/Mohammed Shehzad/Documents/Mo Digital Portfolio')
CAREER_DATA = BASE_DIR / "career-data"

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

edges = load_yaml(CAREER_DATA / 'relationships' / 'edges.yml').get('edges', [])
emps = load_yaml(CAREER_DATA / 'facts' / 'employment.yml').get('employment_records', [])

vm_path = BASE_DIR / 'artifacts' / 'cv_view_models' / 'master.json'
with open(vm_path, 'r', encoding='utf-8') as f:
    vm = json.load(f)

html_path = BASE_DIR / 'artifacts' / 'baselines' / 'cv_master' / 'CV_Master.html'
with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("| Employment | Employment status | Claim status | VM | DOM |")
print("| ---------- | ----------------- | ------------ | -- | --- |")

for emp in emps:
    emp_id = emp['id']
    
    # Check emp status logic from resolver
    emp_ev_edges = [e for e in edges if e['from'] == emp_id and e['type'] == 'SUPPORTED_BY' and e['to'].startswith('E-')]
    emp_status = 'VERIFIED' if emp_ev_edges else 'UNVERIFIED'
    
    # Check claims status
    cv_highlights = emp.get('cv_highlights', [])
    claim_status = 'UNVERIFIED'
    if cv_highlights:
        # Are there any verified claims?
        for ch in cv_highlights:
            if isinstance(ch, dict) and 'claim_id' in ch:
                cid = ch['claim_id']
                ev_edges = [e for e in edges if e['from'] == cid and e['type'] == 'SUPPORTED_BY' and e['to'].startswith('E-')]
                if ev_edges and emp_status == 'VERIFIED':
                    claim_status = 'VERIFIED'
    
    # VM status
    company = emp.get('employer_id')
    vm_entry = None
    for exp in vm.get('experience', []):
        if exp.get('company') == company and str(emp.get('dates', {}).get('start', '')) in exp.get('date', ''):
            vm_entry = exp
            break
            
    if vm_entry:
        vm_str = f"included, {len(vm_entry['bullets'])} bullets"
    else:
        vm_str = "excluded"
        
    # DOM status
    dom_str = "absent"
    start_year = str(emp.get('dates', {}).get('start', ''))[:4]
    for entry in soup.select('.entry'):
        date_el = entry.select_one('.entry-date')
        if date_el and start_year in date_el.text:
            dom_str = "present"
            break
            
    print(f"| {emp_id} | {emp_status} | {claim_status} | {vm_str} | {dom_str} |")
