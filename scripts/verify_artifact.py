import os
import json
import sys
import hashlib
import zipfile
import tempfile
import shutil

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_artifact():
    manifest_path = 'artifacts/manifest.json'
    if not os.path.exists(manifest_path):
        print("[FAIL] manifest.json missing.")
        sys.exit(1)
        
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    entries = manifest.get('entries', [])
    
    # 1. Create Release Artifact
    zip_path = 'release-artifact.zip'
    print(f"Creating {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for entry in entries:
            file_path = entry['relative_path']
            # On windows, we might need to normalize for exists
            local_path = os.path.normpath(file_path)
            if os.path.exists(local_path):
                zf.write(local_path, file_path)
            else:
                print(f"Warning: Could not find {local_path} to add to zip")
        # Always include manifest itself
        zf.write(manifest_path, manifest_path)
        if os.path.exists('artifacts/build-info.json'):
            zf.write('artifacts/build-info.json', 'artifacts/build-info.json')
            
    # 2. Extract Artifact to secure location
    with tempfile.TemporaryDirectory() as extract_dir:
        print(f"Extracting to {extract_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)
            
        # 3. Verify Manifest
        manifest_path = os.path.join(extract_dir, 'artifacts', 'manifest.json')
        if not os.path.exists(manifest_path):
            print("[FAIL] manifest.json missing from artifact.")
            sys.exit(1)
            
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            
        entries = manifest.get('entries', [])
        
        print("Verifying Hashes...")
        differences = 0
        for entry in entries:
            rel_path = entry['relative_path']
            expected_hash = entry['sha256']
            extracted_path = os.path.join(extract_dir, rel_path)
            
            if not os.path.exists(extracted_path):
                print(f"[FAIL] Missing file referenced in manifest: {rel_path}")
                differences += 1
                continue
                
            actual_hash = get_sha256(extracted_path)
            if actual_hash != expected_hash:
                print(f"[FAIL] Hash mismatch for {rel_path}: expected {expected_hash}, got {actual_hash}")
                differences += 1
                
        print("Verifying No Undeclared Files Exist...")
        manifest_paths = set(entry['relative_path'] for entry in entries)
        # Manifest itself and build-info are allowed natively in the artifact
        manifest_paths.add('artifacts/manifest.json')
        manifest_paths.add('artifacts/build-info.json')
        
        for root, _, files in os.walk(extract_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, extract_dir).replace('\\', '/')
                if rel_path not in manifest_paths:
                    print(f"[FAIL] Undeclared file found in artifact: {rel_path}")
                    differences += 1
                
        if differences > 0:
            print(f"[FAIL] Artifact verification failed with {differences} errors.")
            sys.exit(1)
            
        print("[PASS] Artifact Verification PASS. All hashes match.")

if __name__ == '__main__':
    verify_artifact()
