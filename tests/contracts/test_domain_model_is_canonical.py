import json
from pathlib import Path

# Words/Phrases that suggest presentation layer leakage
PRESENTATION_KEYWORDS = [
    "html", "markdown", "css", "class", "style", "icon", "seo", 
    "color", "font", "layout", "column", "break", "margin", "padding"
]

def test_domain_model_is_purely_semantic():
    """
    Asserts that the Domain Model contains NO presentation metadata.
    """
    domain_path = Path("artifacts/profile_domain_model.json")
    assert domain_path.exists(), "Domain Model not found"
    
    with open(domain_path, 'r', encoding='utf-8') as f:
        content = f.read().lower()
        
    for kw in PRESENTATION_KEYWORDS:
        # Check if the exact keyword exists as a key or distinct word in the JSON payload
        # Doing a basic string match might catch "classes" in a semantic context ("I took classes"),
        # but here we are checking the actual structure keys mostly. Let's do a strict parse check.
        pass

    with open(domain_path, 'r', encoding='utf-8') as f:
        domain = json.load(f)
        
    def check_dict(d, path=""):
        for k, v in d.items():
            k_lower = k.lower()
            for kw in PRESENTATION_KEYWORDS:
                assert kw not in k_lower, f"Presentation leak detected in key: '{k}' at {path}"
            
            if isinstance(v, dict):
                check_dict(v, f"{path}.{k}")
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        check_dict(item, f"{path}.{k}[{i}]")

    check_dict(domain, "$")
