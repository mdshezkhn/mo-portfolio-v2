import json
import re
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.parent
PORTFOLIO_VM_PATH = BASE_DIR / "artifacts" / "cv_view_models" / "portfolio.json"
INDEX_HTML_PATH = BASE_DIR / "mo-portfolio-v2" / "index.html"

def audit_dom():
    if not PORTFOLIO_VM_PATH.exists():
        print("FAIL: Portfolio View Model not found.")
        sys.exit(1)
        
    with open(PORTFOLIO_VM_PATH, "r", encoding="utf-8") as f:
        vm = json.load(f)
        
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Check for forbidden unmanaged nodes globally
    # If there are any .tl-item blocks, they MUST be inside the governed markers.
    exp_pattern = r"<!-- PORTFOLIO_EXPERIENCE_START -->(.*?)<!-- PORTFOLIO_EXPERIENCE_END -->"
    exp_match = re.search(exp_pattern, html, flags=re.DOTALL)
    if not exp_match:
        print("FAIL: PORTFOLIO_EXPERIENCE_START/END markers missing in index.html.")
        sys.exit(1)
    
    cred_pattern = r"<!-- PORTFOLIO_CREDENTIALS_START -->(.*?)<!-- PORTFOLIO_CREDENTIALS_END -->"
    cred_match = re.search(cred_pattern, html, flags=re.DOTALL)
    if not cred_match:
        print("FAIL: PORTFOLIO_CREDENTIALS_START/END markers missing in index.html.")
        sys.exit(1)

    governed_exp_html = exp_match.group(1)
    governed_cred_html = cred_match.group(1)
    
    # Strip the governed blocks from the HTML and ensure no rogue nodes remain
    rest_of_html = html.replace(governed_exp_html, "").replace(governed_cred_html, "")
    
    if "class=\"tl-item\"" in rest_of_html:
        print("FAIL: Unmanaged .tl-item found outside governed experience block.")
        sys.exit(1)
        
    if "class=\"edu-card\"" in rest_of_html or "class=\"cert-card\"" in rest_of_html:
        print("FAIL: Unmanaged qualification card found outside governed credentials block.")
        sys.exit(1)
        
    # Check for legacy forbidden names outside governed content
    forbidden = ["Eton House", "Scholars Academy"]
    for f in forbidden:
        if f in rest_of_html:
            print(f"FAIL: Forbidden legacy string '{f}' found in unmanaged HTML.")
            sys.exit(1)

    # 2. Extract DOM IDs and content and ensure bijection with View Model
    dom_exps = re.findall(r'<div class="tl-item" data-id="([^"]+)">.*?<h3 class="tl-title">([^<]+)</h3>.*?<p class="tl-org">([^<]+)</p>', governed_exp_html, flags=re.DOTALL)
    vm_exps = {e['id']: e for e in vm.get('experience', [])}
    
    if len(dom_exps) != len(vm_exps):
        print(f"FAIL: DOM experience count ({len(dom_exps)}) != VM count ({len(vm_exps)})")
        sys.exit(1)
        
    for dom_id, role, company in dom_exps:
        if dom_id not in vm_exps:
            print(f"FAIL: DOM contains unmanaged experience ID: {dom_id}")
            sys.exit(1)
        vm_exp = vm_exps[dom_id]
        if vm_exp['role'].strip() != role.strip():
            print(f"FAIL: Content mismatch for {dom_id}. Expected role: {vm_exp['role']}, Got: {role}")
            sys.exit(1)
        if vm_exp['company'].strip() != company.strip():
            print(f"FAIL: Content mismatch for {dom_id}. Expected company: {vm_exp['company']}, Got: {company}")
            sys.exit(1)
            
    dom_quals = re.findall(r'<div class="edu-card" data-cert-id="([^"]+)".*?<h4 class="edu-title">([^<]+)</h4>.*?<p class="edu-sch">([^<]+)</p>', governed_cred_html, flags=re.DOTALL)
    dom_certs = re.findall(r'<div class="cert-card" data-cert-id="([^"]+)".*?<h4 class="cert-title">([^<]+)</h4>.*?<p class="cert-org">([^<]+)</p>', governed_cred_html, flags=re.DOTALL)
    
    # Map them into a single list
    all_dom_quals = []
    for d, title, inst in dom_quals + dom_certs:
        all_dom_quals.append((d.lower(), title, inst))
        
    vm_quals = {q['id'].lower(): q for q in vm.get('qualifications', []) if q.get('entity_type') != 'professional_development'}
    
    if len(all_dom_quals) != len(vm_quals):
        print(f"FAIL: DOM qualification count ({len(all_dom_quals)}) != VM count ({len(vm_quals)})")
        sys.exit(1)
        
    for dom_id, degree, institution in all_dom_quals:
        if dom_id not in vm_quals:
            print(f"FAIL: DOM contains unmanaged qualification ID: {dom_id}")
            sys.exit(1)
        vm_qual = vm_quals[dom_id]
        if vm_qual['degree'].strip() != degree.strip():
            print(f"FAIL: Content mismatch for {dom_id}. Expected degree: {vm_qual['degree']}, Got: {degree}")
            sys.exit(1)
        if vm_qual['institution'].strip() != institution.strip():
            print(f"FAIL: Content mismatch for {dom_id}. Expected institution: {vm_qual['institution']}, Got: {institution}")
            sys.exit(1)
            
    print("PASS: DOM Boundary Audit passed.")
    sys.exit(0)

if __name__ == "__main__":
    audit_dom()
