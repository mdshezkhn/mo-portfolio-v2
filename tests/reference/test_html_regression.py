import re
from pathlib import Path
from bs4 import BeautifulSoup

def extract_text_from_html(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    return "\n".join(text for text in soup.stripped_strings)

def get_structure(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    structure = []
    
    # Extract sections
    sections = soup.find_all("section")
    for sec in sections:
        h2 = sec.find("h2")
        if h2:
            sec_name = h2.get_text(strip=True)
            structure.append(f"SECTION: {sec_name}")
                
    return structure

def test_html_regression():
    root = Path(__file__).parent.parent.parent
    legacy_path = root / "reference/baselines/v1.3.0/CV_Master.html"
    v2_path = root / "artifacts/generated/cv_v2.html"
    
    assert legacy_path.exists(), f"Reference HTML baseline not found: {legacy_path}"
    assert v2_path.exists(), f"V2 HTML not found: {v2_path}"
    
    with open(legacy_path, "r", encoding="utf-8") as f:
        legacy_html = f.read()
        
    with open(v2_path, "r", encoding="utf-8") as f:
        v2_html = f.read()
        
    struct_legacy = get_structure(legacy_html)
    struct_v2 = get_structure(v2_html)
    
    assert struct_legacy == struct_v2, f"HTML Structural Regression failed!\nLegacy: {struct_legacy}\nV2: {struct_v2}"
