import os
import shutil
import subprocess
import sys
import tempfile
import hashlib
import time
import json
from pathlib import Path

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def hash_directory(directory):
    """Returns a dict of relative_path -> sha256 for all files in a directory."""
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, directory).replace('\\', '/')
            
            sha256 = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            hashes[rel_path] = sha256.hexdigest()
    return hashes

def main():
    print("--- Starting Determinism Proof ---")
    
    # We will use a temporary directory to clone the current state safely
    # For CI and local testing, this avoids git clean -xfd which is destructive.
    with tempfile.TemporaryDirectory() as temp_dir:
        clone_dir = os.path.join(temp_dir, 'repo')
        
        print(f"Copying current repository to {clone_dir}...")
        # Ignore the target directory and node_modules/artifacts if they exist to prevent recursion/junk
        def ignore_func(dir_path, contents):
            return [c for c in contents if c in ['node_modules', '.git', 'artifacts', 'compiled_assets', 'mo-portfolio-v2']]
            
        shutil.copytree('.', clone_dir, ignore=ignore_func)
        
        # We must supply a stable SOURCE_DATE_EPOCH for determinism
        # We use a hardcoded fallback or try to get it from git, but here we just use the current time fixed for the whole run
        commit_ts = run_cmd("git log -1 --format=%ct") if os.path.exists('.git') else str(int(time.time()))
        env = os.environ.copy()
        env['SOURCE_DATE_EPOCH'] = commit_ts
        
        def build_and_hash(pass_name):
            print(f"\n--- Running Build Pass: {pass_name} ---")
            
            # Clean output directories if they exist
            for d in ['mo-portfolio-v2', 'compiled_assets', 'artifacts']:
                path = os.path.join(clone_dir, d)
                if os.path.exists(path):
                    shutil.rmtree(path)
                    
            print("Installing dependencies...")
            subprocess.run("npm ci", shell=True, cwd=clone_dir, env=env, check=True, stdout=subprocess.DEVNULL)
            subprocess.run("pip install -r requirements.txt", shell=True, cwd=clone_dir, env=env, check=True, stdout=subprocess.DEVNULL)
            
            print("Building...")
            subprocess.run("npm run build", shell=True, cwd=clone_dir, env=env, check=True, stdout=subprocess.DEVNULL)
            subprocess.run("python scripts/generate_manifest.py", shell=True, cwd=clone_dir, env=env, check=True, stdout=subprocess.DEVNULL)
            subprocess.run("python scripts/generate_provenance.py", shell=True, cwd=clone_dir, env=env, check=True, stdout=subprocess.DEVNULL)
            
            print("Hashing outputs...")
            manifest_hashes = hash_directory(os.path.join(clone_dir, 'artifacts'))
            html_hashes = hash_directory(os.path.join(clone_dir, 'mo-portfolio-v2'))
            
            return {
                'artifacts': manifest_hashes,
                'html': html_hashes
            }
            
        # Run first pass
        pass1 = build_and_hash("Pass 1")
        
        # Run second pass
        pass2 = build_and_hash("Pass 2")
        
        print("\n--- Comparing Passes ---")
        differences = 0
        
        report = {
            "run1": {
                "manifest_sha256": get_manifest_hash(pass1),
                "artifacts": pass1['artifacts'],
                "html": pass1['html']
            },
            "run2": {
                "manifest_sha256": get_manifest_hash(pass2),
                "artifacts": pass2['artifacts'],
                "html": pass2['html']
            },
            "comparison": {
                "manifest": get_manifest_hash(pass1) == get_manifest_hash(pass2) and get_manifest_hash(pass1) != 'missing',
                "artifacts": True,
                "html": True
            },
            "differences": []
        }
        
        for category in ['artifacts', 'html']:
            print(f"\nComparing {category}...")
            keys1 = set(pass1[category].keys())
            keys2 = set(pass2[category].keys())
            
            if keys1 != keys2:
                msg = f"File lists differ in {category}."
                print(f"[FAIL] {msg}")
                report["differences"].append(msg)
                differences += 1
                report["comparison"][category] = False
                
            for file in keys1.intersection(keys2):
                h1 = pass1[category][file]
                h2 = pass2[category][file]
                if h1 != h2:
                    msg = f"Hash mismatch for {category}/{file}: Run 1={h1}, Run 2={h2}"
                    print(f"[FAIL] {msg}")
                    report["differences"].append(msg)
                    differences += 1
                    report["comparison"][category] = False
                    
        report["overall_pass"] = (differences == 0)
        
        with open("artifacts/determinism-report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        if differences > 0:
            print(f"\n[FAIL] Determinism proof failed with {differences} differences.")
            sys.exit(1)
            
        print("\n[PASS] Determinism proof passed! Identical outputs across builds. Wrote determinism-report.json.")

def get_manifest_hash(pass_data):
    # Returns the hash of manifest.json from the pass data, if it exists
    return pass_data['artifacts'].get('manifest.json', 'missing')

if __name__ == '__main__':
    main()
