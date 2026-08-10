import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import sys

BASE_DIR = Path(__file__).parent.parent.parent

def get_git_info():
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=BASE_DIR).decode('utf-8').strip()
        status = subprocess.check_output(['git', 'status', '--porcelain', '--ignore-submodules'], cwd=BASE_DIR).decode('utf-8').strip()
        return commit, (len(status) == 0)
    except Exception as e:
        return "unknown", False

def hash_file(path):
    p = BASE_DIR / path
    if not p.exists():
        return "MISSING"
    h = hashlib.sha256()
    h.update(p.read_bytes().replace(b'\r\n', b'\n'))
    return h.hexdigest()

def generate():
    manifest_categories = {
        'canonical_data': [
            'career-data/facts/employment.yml',
            'career-data/facts/claims.yml'
        ],
        'governance': [
            'governance/cv_policies.yml'
        ],
        'provenance_engine': [
            'career-data/relationships/edges.yml',
            'career-data/facts/evidence_assertions.yml'
        ],
        'verification_logic': [
            'scripts/verify/graph_validator.py',
            'scripts/verify/verification_resolver.py'
        ],
        'build_orchestration': [
            'scripts/builders/build_domain_model.py',
            'build.py'
        ],
        'templates': [
            'templates/cv/base.html',
            'templates/cv/partials/experience.html'
        ]
    }
    
    commit_sha, is_clean = get_git_info()
    
    source_manifest = {}
    for category, files in manifest_categories.items():
        source_manifest[category] = []
        for path in files:
            source_manifest[category].append({
                'path': path,
                'sha256': hash_file(path)
            })
            
    metadata = {
        'baseline': {
            'artifact': 'CV_Master.html'
        },
        'git': {
            'source_commit': commit_sha,
            'metadata_commit': 'pending_commit',
            'worktree_clean': is_clean
        },
        'source_manifest': source_manifest,
        'artifact_hashes': {
            'master_json': hash_file('artifacts/cv_view_models/master.json'),
            'cv_master_html': hash_file('compiled_assets/CV_Master.html')
        },
        'environment': {
            'viewport': '1920x1080',
            'browser': 'Chromium',
            'created_at': datetime.now(timezone.utc).isoformat()
        }
    }
    
    out_dir = BASE_DIR / 'artifacts' / 'baselines' / 'cv_master'
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'baseline_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
        
    print("Baseline metadata generated successfully.")

if __name__ == "__main__":
    generate()
