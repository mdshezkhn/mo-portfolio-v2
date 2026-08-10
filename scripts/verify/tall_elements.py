import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

man = json.loads((BASE_DIR / 'manual_geometry.json').read_text(encoding='utf-8'))
gen = json.loads((BASE_DIR / 'gen_geometry.json').read_text(encoding='utf-8'))

print("=== TALL ELEMENTS IN MANUAL ===")
for e in man:
    if e['rect']['height'] > 50 and e['tag'] not in ['section', 'body']:
        print(f"Manual: {e['tag']}.{e['className']} - H:{e['rect']['height']} - MT:{e['style']['marginTop']} - MB:{e['style']['marginBottom']} - Text: {e['text'][:20]}")

print("\n=== TALL ELEMENTS IN GEN ===")
for e in gen:
    if e['rect']['height'] > 50 and e['tag'] not in ['section', 'body']:
        print(f"Gen: {e['tag']}.{e['className']} - H:{e['rect']['height']} - MT:{e['style']['marginTop']} - MB:{e['style']['marginBottom']} - Text: {e['text'][:20]}")
