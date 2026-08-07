import yaml
import hashlib
from pathlib import Path
import sys

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_evidence(evidence_dir, manifest_path, hashes_path):
    manifest = load_yaml(manifest_path)
    hash_registry = load_yaml(hashes_path).get("hashes", [])
    
    # Build hash lookup
    expected_hashes = {h["evidence_id"]: h["checksum"] for h in hash_registry if h.get("checksum")}
    
    errors = []
    
    for eid, entry in manifest.get("entries", {}).items():
        if entry.get("verified"):
            file_rel_path = entry.get("file")
            full_path = evidence_dir / file_rel_path
            
            if not full_path.exists():
                errors.append(f"Missing file for {eid}: {file_rel_path}")
                continue
                
            expected = expected_hashes.get(eid)
            if expected:
                actual = compute_sha256(full_path)
                if expected != actual:
                    errors.append(f"Hash mismatch for {eid} ({file_rel_path}). Expected: {expected}, Actual: {actual}")
            else:
                print(f"Warning: No checksum registered for {eid} yet.")

    if errors:
        print("Evidence Validation Failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("Evidence Validation Passed (or warnings logged for pending checksums).")
        sys.exit(0)

if __name__ == "__main__":
    root = Path(__file__).parent.parent
    evidence_dir = root / "evidence"
    manifest = evidence_dir / "manifest.yml"
    hashes = evidence_dir / "hashes.yml"
    
    validate_evidence(evidence_dir, manifest, hashes)
