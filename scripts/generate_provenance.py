import os
import json
import subprocess
import platform
import sys
from datetime import datetime, timezone
import hashlib

def get_git_sha():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
    except Exception:
        return 'unknown'

def get_node_version():
    try:
        return subprocess.check_output(['node', '-v']).decode('utf-8').strip()
    except Exception:
        return 'unknown'

def get_manifest_hash():
    manifest_path = 'artifacts/manifest.json'
    if not os.path.exists(manifest_path):
        return 'missing'
    sha256_hash = hashlib.sha256()
    with open(manifest_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_repository_version():
    try:
        with open('package.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('version', 'unknown')
    except Exception:
        return 'unknown'

def main():
    epoch = os.environ.get('SOURCE_DATE_EPOCH')
    if epoch:
        gen_at = datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat()
    else:
        gen_at = datetime.now(timezone.utc).isoformat()
        
    provenance = {
        "generatorVersion": "v1.0.0",
        "manifestHash": get_manifest_hash(),
        "gitSha": get_git_sha(),
        "repositoryVersion": get_repository_version(),
        "workflowRunId": os.environ.get('GITHUB_RUN_ID', 'local'),
        "pythonVersion": sys.version.split()[0],
        "nodeVersion": get_node_version(),
        "os": platform.platform(),
        "utc": gen_at,
        "schemaVersion": "1.0"
    }
    
    os.makedirs('artifacts', exist_ok=True)
    with open('artifacts/build-info.json', 'w', encoding='utf-8') as f:
        json.dump(provenance, f, indent=2)
        
    print("Generated build-info.json successfully.")

if __name__ == '__main__':
    main()
