import re
import yaml
import os
import json
from datetime import datetime

def parse_markdown_table(text_block):
    data = {}
    lines = text_block.strip().split('\n')
    in_table = False
    for line in lines:
        if line.startswith('| Field |') or line.startswith('|-------|'):
            in_table = True
            continue
        if in_table and line.startswith('|'):
            parts = line.split('|')
            if len(parts) >= 3:
                key = parts[1].strip().replace('**', '')
                value = parts[2].strip().replace('`', '')
                data[key] = value
    return data

def migrate_claims():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    register_path = os.path.join(base_dir, 'CLAIM_REGISTER.md')
    out_path = os.path.join(base_dir, 'claims.yml')
    
    if not os.path.exists(register_path):
        print(f"File not found: {register_path}")
        return
        
    with open(register_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all claim blocks
    pattern = re.compile(r'### (C-\d+) — ([^\n]+)\n+(.*?)(?=\n### C-\d+ |$)', re.DOTALL)
    matches = pattern.findall(content)
    
    claims_list = []
    
    for match in matches:
        claim_id = match[0]
        # title is part of canonical wording usually, but we have a title in the heading
        title = match[1]
        table_content = match[2]
        
        data = parse_markdown_table(table_content)
        
        # Extract evidence IDs (E-1234)
        evidence_str = data.get('Supported by Evidence IDs', '')
        evidence_ids = re.findall(r'E-\d+', evidence_str)
        
        status_str = data.get('Status', 'Pending').lower()
        if 'approved' in status_str:
            status = 'verified'
        elif 'pending' in status_str:
            status = 'pending'
        else:
            status = 'archived'
            
        # construct the v1.0 schema object
        claim_obj = {
            "id": claim_id,
            "schemaVersion": "1.0",
            "title": data.get('Canonical Wording', title),
            "status": status,
            "evidence": evidence_ids,
            "verification_date": data.get('Last Reviewed', datetime.now().strftime("%Y-%m-%d"))
        }
        claims_list.append(claim_obj)
        
    print(f"Migrating {len(claims_list)} claims...")
    
    # We will output as JSON or YAML. The spec says claims.yml
    with open(out_path, 'w', encoding='utf-8') as f:
        yaml.dump(claims_list, f, sort_keys=False, default_flow_style=False)
        
    print(f"Successfully migrated claims to {out_path}")

if __name__ == '__main__':
    migrate_claims()
