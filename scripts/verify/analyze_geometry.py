import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

def load_data(file_name):
    return json.loads((BASE_DIR / file_name).read_text(encoding='utf-8'))

def analyze():
    man = load_data('manual_geometry.json')
    gen = load_data('gen_geometry.json')
    
    report = ["# Forensic CSS/DOM Geometry Comparison", ""]
    
    # 1. Total Height
    man_body = next((e for e in man if e['tag'] == 'body'), None)
    gen_body = next((e for e in gen if e['tag'] == 'body'), None)
    
    report.append(f"## 1. Overall Body Height")
    report.append(f"- Manual: {man_body['rect']['height']}px")
    report.append(f"- Generated: {gen_body['rect']['height']}px")
    report.append(f"- Difference: {gen_body['rect']['height'] - man_body['rect']['height']}px")
    report.append("")
    
    # Let's extract total margins/paddings from all elements
    def sum_spacing(data, prop):
        total = 0
        for e in data:
            val = e['style'][prop]
            if val.endswith('px'):
                total += float(val.replace('px', ''))
        return total
    
    report.append(f"## 2. Cumulative Spacing Analysis")
    report.append("| Property | Manual Total | Generated Total | Diff |")
    report.append("| --- | --- | --- | --- |")
    
    for prop in ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom']:
        m_val = sum_spacing(man, prop)
        g_val = sum_spacing(gen, prop)
        report.append(f"| {prop} | {m_val:.1f}px | {g_val:.1f}px | {g_val - m_val:.1f}px |")
        
    report.append("")
    
    # Compare sections
    report.append("## 3. Section Analysis")
    man_sections = [e for e in man if e['tag'] == 'section']
    gen_sections = [e for e in gen if e['tag'] == 'section']
    
    report.append(f"- Manual CV has {len(man_sections)} `<section>` elements.")
    report.append(f"- Generated CV has {len(gen_sections)} `<section>` elements.")
    
    report.append("")
    report.append("### Major Block Divergences")
    
    man_entries = [e for e in man if e['className'] and ('role' in e['className'] or 'education' in e['className'])]
    gen_entries = [e for e in gen if e['className'] and ('entry' in e['className'])]
    
    report.append(f"- Manual CV `.role` / `.education` blocks count: {len(man_entries)}")
    report.append(f"- Generated CV `.entry` blocks count: {len(gen_entries)}")
    
    report.append("\n**Average Margins for manual `.role` vs generated `.entry`:**")
    if man_entries and gen_entries:
        m_mt = sum(float(e['style']['marginTop'].replace('px', '')) for e in man_entries) / len(man_entries)
        m_mb = sum(float(e['style']['marginBottom'].replace('px', '')) for e in man_entries) / len(man_entries)
        g_mt = sum(float(e['style']['marginTop'].replace('px', '')) for e in gen_entries) / len(gen_entries)
        g_mb = sum(float(e['style']['marginBottom'].replace('px', '')) for e in gen_entries) / len(gen_entries)
        report.append(f"- Manual Margin: Top {m_mt:.1f}px, Bottom {m_mb:.1f}px")
        report.append(f"- Generated Margin: Top {g_mt:.1f}px, Bottom {g_mb:.1f}px")
        
    report.append("")
    report.append("## 4. Specific CSS Rules Missing")
    # find missing fonts or line heights
    m_lh = sum(float(e['style']['lineHeight'].replace('px', '')) for e in man if e['style']['lineHeight'].endswith('px')) / max(1, len([e for e in man if e['style']['lineHeight'].endswith('px')]))
    g_lh = sum(float(e['style']['lineHeight'].replace('px', '')) for e in gen if e['style']['lineHeight'].endswith('px')) / max(1, len([e for e in gen if e['style']['lineHeight'].endswith('px')]))
    
    report.append(f"- Manual Avg Line Height: {m_lh:.1f}px")
    report.append(f"- Generated Avg Line Height: {g_lh:.1f}px")
    
    return "\n".join(report)

(BASE_DIR / 'diagnostic_report.md').write_text(analyze(), encoding='utf-8')
print("Diagnostic report generated.")
