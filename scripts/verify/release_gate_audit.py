import yaml
import json
from pathlib import Path
from bs4 import BeautifulSoup
import sys

BASE_DIR = Path('c:/Users/Mohammed Shehzad/Documents/Mo Digital Portfolio')

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

edges_data = load_yaml(BASE_DIR / 'career-data/relationships/edges.yml')
edges = edges_data.get('edges', [])
emps = load_yaml(BASE_DIR / 'career-data/facts/employment.yml').get('employment_records', [])
claims_data = load_yaml(BASE_DIR / 'career-data/facts/claims.yml').get('claims', [])
golden_claims_data = load_yaml(BASE_DIR / 'career-data/golden/E-001/source/facts/claims.yml').get('claims', []) if (BASE_DIR / 'career-data/golden/E-001/source/facts/claims.yml').exists() else []
all_claims = {c['id']: c for c in claims_data + golden_claims_data}

# Helper to find edges
def get_edges(from_id=None, to_id=None, edge_type=None):
    res = []
    for e in edges:
        if from_id and e['from'] != from_id: continue
        if to_id and e['to'] != to_id: continue
        if edge_type and e['type'] != edge_type: continue
        res.append(e)
    return res

# Load View Model
vm_path = BASE_DIR / 'artifacts' / 'cv_view_models' / 'master.json'
vm = {}
if vm_path.exists():
    with open(vm_path, 'r', encoding='utf-8') as f:
        vm = json.load(f)

# Load DOM
html_path = BASE_DIR / 'artifacts' / 'baselines' / 'cv_master' / 'CV_Master.html'
dom_html = ""
if html_path.exists():
    with open(html_path, 'r', encoding='utf-8') as f:
        dom_html = f.read()
soup = BeautifulSoup(dom_html, 'html.parser')

print("| EMP ID | Org Ev | Dates Ev | Claims Linked | Claim Ev | Policy Decision | View-Model Status | Rendered DOM |")
print("|---|---|---|---|---|---|---|---|")

for emp in emps:
    emp_id = emp['id']
    review_status = emp.get('review_status', 'pending')
    
    # Direct evidence supporting the EMP record
    emp_ev_list = [e['to'] for e in get_edges(from_id=emp_id, edge_type='SUPPORTED_BY')]
    emp_ev_str = ",".join(emp_ev_list) if emp_ev_list else "NONE"
    
    # Claims supporting the EMP record
    claim_edges = get_edges(to_id=emp_id, edge_type='SUPPORTED_BY')
    claims_linked = []
    claim_evs = []
    
    for ce in claim_edges:
        cid = ce['from']
        claims_linked.append(cid)
        # Find what supports the claim
        cev = [e['to'] for e in get_edges(from_id=cid, edge_type='SUPPORTED_BY')]
        # Also check claims.yml for embedded evidence
        c_data = all_claims.get(cid, {})
        if c_data.get('evidence'):
            for ev in c_data.get('evidence'):
                if ev not in cev: cev.append(ev)
        if not cev: cev = ["NONE"]
        claim_evs.extend(cev)
        
    claims_str = ",".join(claims_linked) if claims_linked else "NONE"
    claim_ev_str = ",".join(set(claim_evs)) if claim_evs else "NONE"
    
    policy_dec = "INCLUDED" if review_status == "approved" else "EXCLUDED"
    
    # Check VM
    vm_status = "NOT_FOUND"
    for exp in vm.get('experience', []):
        if str(emp.get('dates', {}).get('start', ''))[:4] in exp.get('date', ''):
            vm_status = "FOUND"
            break
            
    # Check DOM
    dom_status = "NOT_FOUND"
    for entry in soup.select('.entry'):
        date_el = entry.select_one('.entry-date')
        if date_el and str(emp.get('dates', {}).get('start', ''))[:4] in date_el.text:
            dom_status = "FOUND"
            break
            
    print(f"| {emp_id} | {emp_ev_str} | {emp_ev_str} | {claims_str} | {claim_ev_str} | {policy_dec} | {vm_status} | {dom_status} |")
