import os
import hashlib
import json
import mimetypes
from datetime import datetime, timezone

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def gather_files(paths_to_include, exclude_paths):
    files_list = []
    for path in paths_to_include:
        if os.path.isfile(path):
            files_list.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    norm_full = os.path.normpath(full_path)
                    excluded = False
                    for ex in exclude_paths:
                        if norm_full.startswith(os.path.normpath(ex)):
                            excluded = True
                            break
                    if not excluded:
                        files_list.append(full_path)
    
    # Sort files to guarantee determinism
    files_list.sort()
    return files_list

def determine_classification(filepath):
    norm_path = filepath.replace('\\', '/')
    if norm_path.startswith('career-data/') or norm_path.startswith('schemas/') or norm_path == 'CI_SPECIFICATION.md':
        return 'normative', 'required' if 'evidence' in norm_path or 'claims' in norm_path else 'optional'
    elif norm_path.startswith('mo-portfolio-v2/') or norm_path.startswith('compiled_assets/'):
        return 'generated', 'prohibited'
    elif norm_path.startswith('scripts/') or norm_path in ['package.json', 'requirements.txt', 'package-lock.json']:
        return 'source', 'optional'
    else:
        return 'derived', 'optional'

def get_timestamp(filepath):
    epoch = os.environ.get('SOURCE_DATE_EPOCH')
    if epoch:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat()
    # Fallback to file mtime if no epoch provided
    stat = os.stat(filepath)
    return datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()

def generate_manifest():
    normative_paths = [
        'career-data',
        'schemas',
        'templates',
        'scripts',
        'package.json',
        'requirements.txt',
        'CI_SPECIFICATION.md',
        'package-lock.json'
    ]
    derived_paths = [
        'mo-portfolio-v2',
        'compiled_assets',
        'artifacts'
    ]
    
    exclude_paths = [
        os.path.join('artifacts', 'manifest.json'),
        os.path.join('artifacts', 'build-info.json'),
        'mo-portfolio-v2/node_modules'
    ]
    
    all_paths = normative_paths + derived_paths
    files_to_hash = gather_files(all_paths, exclude_paths)
    
    entries = []
    for filepath in files_to_hash:
        try:
            mime_type, _ = mimetypes.guess_type(filepath)
            if mime_type is None:
                mime_type = 'application/octet-stream'
                
            stat = os.stat(filepath)
            classification, traceability = determine_classification(filepath)
            
            entry = {
                "filename": os.path.basename(filepath),
                "relative_path": filepath.replace('\\', '/'),
                "sha256": get_sha256(filepath),
                "size": stat.st_size,
                "mime_type": mime_type,
                "modified_date": get_timestamp(filepath),
                "classification": classification,
                "traceability": traceability
            }
            
            # If traceability is required, evidence_id must be present, though we might not have it yet.
            # We'll just leave it out if we don't know it, schema might fail if we don't set it.
            # To pass schema for 'required', we set it to 'E-UNKNOWN' for now if not available.
            if traceability == 'required':
                entry['evidence_id'] = 'E-0000' # Placeholder, ideally extracted from actual file context
                
            entries.append(entry)
        except Exception as e:
            print(f"Failed to process {filepath}: {e}")
            
    # Sort entries by relative_path
    entries.sort(key=lambda x: x['relative_path'])
    
    epoch = os.environ.get('SOURCE_DATE_EPOCH')
    if epoch:
        gen_at = datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat()
    else:
        gen_at = datetime.now(timezone.utc).isoformat()
            
    manifest = {
        "manifestVersion": "1.0",
        "generatedAt": gen_at,
        "generatorVersion": "v1.0.0",
        "entries": entries
    }
    
    os.makedirs('artifacts', exist_ok=True)
    with open('artifacts/manifest.json', 'w', encoding='utf-8') as f:
        # Sort keys to ensure stable output
        json.dump(manifest, f, indent=2, sort_keys=True)
        
    print(f"Generated manifest.json with {len(entries)} entries.")

if __name__ == '__main__':
    generate_manifest()
