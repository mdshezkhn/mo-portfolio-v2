from pathlib import Path

def find_cert_assets():
    root = Path(__file__).resolve().parent.parent
    
    extensions = ['.png', '.jpg', '.jpeg', '.webp', '.pdf', '.svg']
    
    found = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in extensions:
            rel = str(p.relative_to(root)).replace("\\", "/")
            if any(part in rel for part in ['.git', '.playwright-mcp', 'brain', '.claude']):
                continue
            found.append(rel)
            
    print(f"Found {len(found)} image/document files:")
    for f in sorted(found):
        if "cert" in f.lower() or "edu" in f.lower() or "pgce" in f.lower() or "tesol" in f.lower() or "tefl" in f.lower() or "assets/images" in f.lower():
            print(f" - {f}")

if __name__ == "__main__":
    find_cert_assets()
