import re
from pathlib import Path

def get_md_structure(md_str):
    structure = []
    lines = md_str.splitlines()
    
    in_manifest = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if "ASSET MANIFEST" in line:
            in_manifest = True
            continue
        if in_manifest and "Compliance: PASS" in line:
            in_manifest = False
            continue
        if in_manifest:
            continue
            
        if line.startswith("## "):
            structure.append(f"SECTION: {line[3:].strip()}")
                
    return structure

def test_markdown_regression():
    root = Path(__file__).parent.parent.parent
    legacy_path = root / "reference/baselines/v1.3.0/CV_Master.md"
    v2_path = root / "artifacts/generated/cv_v2.md"
    
    assert legacy_path.exists(), f"Reference MD baseline not found: {legacy_path}"
    assert v2_path.exists(), f"V2 MD not found: {v2_path}"
    
    with open(legacy_path, "r", encoding="utf-8") as f:
        legacy_md = f.read()
        
    with open(v2_path, "r", encoding="utf-8") as f:
        v2_md = f.read()
        
    struct_legacy = get_md_structure(legacy_md)
    struct_v2 = get_md_structure(v2_md)
    
    assert struct_legacy == struct_v2, f"Markdown Structural Regression failed!\nLegacy: {struct_legacy}\nV2: {struct_v2}"
