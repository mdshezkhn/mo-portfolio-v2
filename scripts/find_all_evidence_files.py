from pathlib import Path

def find_all_files():
    root = Path(__file__).resolve().parent.parent
    for p in root.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(root)).replace("\\", "/")
            if any(part in rel for part in ['.git', '.playwright-mcp', 'brain', '.claude']):
                continue
            if "evidence" in rel.lower() or "cert" in rel.lower() or "qual" in rel.lower() or "assets/images" in rel.lower():
                print(rel)

if __name__ == "__main__":
    find_all_files()
