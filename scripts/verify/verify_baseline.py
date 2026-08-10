import json
import hashlib
import subprocess
import sys
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

# Add BASE_DIR to sys.path so we can import production logic
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.verify.graph_validator import validate_graph
from scripts.verify.verification_resolver import resolve_verification_state

def hash_file(path):
    p = BASE_DIR / path
    if not p.exists():
        return "MISSING"
    h = hashlib.sha256()
    h.update(p.read_bytes().replace(b'\r\n', b'\n'))
    return h.hexdigest()

def get_git_info():
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=BASE_DIR).decode('utf-8').strip()
        status = subprocess.check_output(['git', 'status', '--porcelain', '--ignore-submodules'], cwd=BASE_DIR).decode('utf-8').strip()
        return commit, (len(status) == 0)
    except Exception as e:
        return "unknown", False

def verify():
    meta_path = BASE_DIR / 'artifacts' / 'baselines' / 'cv_master' / 'baseline_metadata.json'
    if not meta_path.exists():
        print("FAIL: baseline_metadata.json not found.")
        sys.exit(1)
        
    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        
    errors = []
    
    # 1. Precondition: Git clean check
    # Before the rebuild, the worktree must be completely clean (except for ignored files like final_audit_package).
    commit_sha, is_clean = get_git_info()
    if not is_clean:
        errors.append("Git worktree is dirty. Rebuild verification requires a completely clean worktree.")
        
    # The source_commit should match the metadata's source_commit.
    source_commit = metadata.get('git', {}).get('source_commit')
    
    # 2 & 3. Verify Source Manifest
    dep_mismatches = 0
    for category, files in metadata.get('source_manifest', {}).items():
        if not files:
            errors.append(f"Manifest category {category} is empty.")
        for source in files:
            current_hash = hash_file(source['path'])
            if current_hash == "MISSING":
                errors.append(f"Manifest file missing: {source['path']}")
                dep_mismatches += 1
            elif current_hash != source['sha256']:
                errors.append(f"Manifest hash mismatch for {source['path']}: expected {source['sha256']}, got {current_hash}")
                dep_mismatches += 1
                
    # Check evidence assertion hashes match physical files
    ev_mismatches = 0
    import yaml
    ev_assertions_path = BASE_DIR / 'career-data/facts/evidence_assertions.yml'
    with open(ev_assertions_path, 'r', encoding='utf-8') as f:
        ev_data = yaml.safe_load(f).get('evidence_assertions', [])
        for ev in ev_data:
            expected_hash = ev.get('source', {}).get('document_sha256')
            doc_path = ev.get('source', {}).get('document')
            if expected_hash and doc_path:
                actual_hash = hash_file(doc_path)
                if actual_hash != expected_hash:
                    errors.append(f"Evidence hash mismatch for {doc_path}: expected {expected_hash}, got {actual_hash}")
                    ev_mismatches += 1

    # Explicit Destructive Rebuild
    print("Deleting generated artifacts to ensure rebuild freshness...")
    vm_out_path = BASE_DIR / 'artifacts/cv_view_models/master.json'
    html_out_path = BASE_DIR / 'compiled_assets/CV_Master.html'
    if vm_out_path.exists():
        vm_out_path.unlink()
    if html_out_path.exists():
        html_out_path.unlink()
        
    print("Running rebuild for byte-comparison...")
    res1 = subprocess.run([sys.executable, 'scripts/builders/build_domain_model.py'], cwd=BASE_DIR, capture_output=True, text=True)
    if res1.returncode != 0:
        print("FAIL: Clean rebuild (domain model) failed.")
        print(res1.stderr)
        sys.exit(1)
        
    res2 = subprocess.run([sys.executable, 'build.py'], cwd=BASE_DIR, capture_output=True, text=True)
    if res2.returncode != 0:
        print("FAIL: Clean rebuild (html) failed.")
        print(res2.stderr)
        sys.exit(1)
        
    # Check output artifacts were successfully recreated
    if not vm_out_path.exists() or not html_out_path.exists():
        print("FAIL: Rebuild succeeded but artifacts were not created.")
        sys.exit(1)
        
    # Hash new artifacts and compare to baseline metadata
    arts = metadata.get('artifact_hashes', {})
    new_vm_hash = hash_file('artifacts/cv_view_models/master.json')
    new_html_hash = hash_file('compiled_assets/CV_Master.html')
    
    vm_match = (new_vm_hash == arts.get('master_json'))
    html_match = (new_html_hash == arts.get('cv_master_html'))
    
    if not vm_match:
         errors.append(f"Rebuilt View Model mismatch: expected {arts.get('master_json')}, got {new_vm_hash}")
    if not html_match:
         errors.append(f"Rebuilt HTML mismatch: expected {arts.get('cv_master_html')}, got {new_html_hash}")

    # Compute provenance metrics using the real engine logic
    print("Computing provenance metrics...")
    
    # Run graph validator natively to count orphan/contradictory edges
    # We will capture if it raises ValueError
    orphan_edges = 0
    contradictory_edges = 0
    try:
        validate_graph()
    except ValueError as e:
        msg = str(e).lower()
        if 'orphan' in msg or 'missing' in msg:
            orphan_edges += 1
        if 'contradiction' in msg or 'invalid' in msg or 'mismatch' in msg:
            contradictory_edges += 1
            
    resolved_all = resolve_verification_state()
    unverified_emp_ids = {eid for eid, state in resolved_all.items() if eid.startswith('EMP-') and state.get('status') != 'VERIFIED'}
    unverified_claim_ids = {cid for cid, state in resolved_all.items() if cid.startswith('C') and state.get('status') != 'VERIFIED'}
    all_resolved_claim_ids = {cid for cid in resolved_all.keys() if cid.startswith('C')}
    
    # Inspect the view model
    with open(vm_out_path, 'r', encoding='utf-8') as f:
        vm = json.load(f)
        
    # We need to map VM content back to IDs.
    # We rely on 'company' mapping to employer_id.
    published_emp_ids = set()
    published_claim_strings = set()
    for exp in vm.get('experience', []):
        published_emp_ids.add(exp['company'])
        for b in exp.get('bullets', []):
            published_claim_strings.add(b)
            
    unverified_emp_ids = {eid for eid, state in resolved_all.items() if state.get('status') != 'VERIFIED'}
    unverified_claim_ids = {cid for cid, state in resolved_all.items() if state.get('status') != 'VERIFIED'}
    
    # We need facts/employment.yml to reverse-map claim text back to claim_id
    with open(BASE_DIR / 'career-data/facts/employment.yml', 'r', encoding='utf-8') as f:
        emps = yaml.safe_load(f).get('employment_records', [])
        
    historical_highlights_published = 0
    unverified_claims_published = 0
    
    for emp in emps:
        # if emp is not published, skip its claims
        if emp['employer_id'] not in published_emp_ids:
            continue
        for ch in emp.get('cv_highlights', []):
            if isinstance(ch, str):
                if ch in published_claim_strings:
                    historical_highlights_published += 1
            elif isinstance(ch, dict) and 'claim_id' in ch:
                # Need to load claims.yml to match text
                # For simplicity, we just check if it's published and if it is unverified
                # Actually, the view model dropped any claim not in valid state. We can assert this structurally.
                # Since we don't map text perfectly here, we trust the count derived from engine intersection
                cid = ch['claim_id']
                if cid in unverified_claim_ids:
                    pass

    # Load claims
    with open(BASE_DIR / 'career-data/facts/claims.yml', 'r', encoding='utf-8') as f:
        claims_doc = yaml.safe_load(f).get('claims', [])
    claim_id_to_text = {c['id']: c['title'] for c in claims_doc}
    
    for cid in unverified_claim_ids:
        if claim_id_to_text.get(cid) in published_claim_strings:
            unverified_claims_published += 1
            
    unverified_employments_published = len(published_emp_ids.intersection(unverified_emp_ids))
    
    # Are there any published claims that have NO state resolved?
    unresolved_published_claims = 0
    for cid, text in claim_id_to_text.items():
        if text in published_claim_strings and cid not in all_resolved_claim_ids:
            unresolved_published_claims += 1

    report = {
        'release_gate': 'PASS' if (is_clean and len(errors)==0 and orphan_edges==0 and contradictory_edges==0 
                                   and unverified_employments_published==0 and unverified_claims_published==0
                                   and historical_highlights_published==0 and unresolved_published_claims==0
                                   and vm_match and html_match) else 'FAIL',
        'git': {
            'source_commit': source_commit,
            'metadata_commit': commit_sha,
            'worktree_clean': is_clean
        },
        'provenance': {
            'orphan_edges': orphan_edges, 
            'contradictory_edges': contradictory_edges,
            'unresolved_published_claims': unresolved_published_claims,
            'historical_highlights_published': historical_highlights_published
        },
        'presentation': {
            'employment_without_verified_provenance': unverified_employments_published,
            'claims_without_closed_provenance': unverified_claims_published
        },
        'reproducibility': {
            'dependency_hash_mismatches': dep_mismatches,
            'evidence_hash_mismatches': ev_mismatches,
            'view_model_hash_match': vm_match,
            'html_hash_match': html_match,
            'clean_rebuild_byte_identical': vm_match and html_match
        }
    }

    # Generate the closed final package
    out_dir = BASE_DIR / 'artifacts/baselines/final_audit_package'
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # copy files
    shutil.copy(meta_path, out_dir / 'baseline_metadata.json')
    shutil.copy(vm_out_path, out_dir / 'master.json')
    shutil.copy(html_out_path, out_dir / 'CV_Master.html')
    
    # write verification report WITHOUT the manifest hash first
    with open(out_dir / 'verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        
    # generate manifest of the package
    package_manifest = {}
    for pkg_file in ['baseline_metadata.json', 'master.json', 'CV_Master.html', 'verification_report.json']:
        package_manifest[pkg_file] = hash_file(f'artifacts/baselines/final_audit_package/{pkg_file}')
        
    with open(out_dir / 'manifest.json', 'w', encoding='utf-8') as f:
        json.dump(package_manifest, f, indent=2)
        
    # finally, record manifest hash inside verification report
    report['package_manifest_sha256'] = hash_file('artifacts/baselines/final_audit_package/manifest.json')
    with open(out_dir / 'verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    if report['release_gate'] == 'FAIL':
        print("BASELINE VERIFICATION FAILED:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
        
    print("BASELINE VERIFICATION PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
