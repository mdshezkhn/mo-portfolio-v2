import os
import sys
import yaml
from pathlib import Path

def validate_ids(data_dir="career-data", registry_path="registry/ids.yml"):
    data_dir = Path(data_dir)
    registry_path = Path(registry_path)
    
    if not registry_path.exists():
        print(f"CRITICAL ERROR: Registry not found at {registry_path}")
        sys.exit(1)
        
    with open(registry_path, 'r', encoding='utf-8') as file:
        registry_data = yaml.safe_load(file)
        
    registry_entities = registry_data.get('entities', {})
    
    facts_dir = data_dir / "facts"
    
    used_ids = set()
    duplicate_ids = set()
    unknown_ids = set()
    
    for root, dirs, files in os.walk(facts_dir):
        if 'metrics' in root or 'claims' in root:
            continue
        for f in files:
            if f.endswith('.yml') or f.endswith('.yaml'):
                path = Path(root) / f
                with open(path, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file)
                    if not data:
                        continue
                    
                    if isinstance(data, list):
                        items_to_check = [("root", data)]
                    elif isinstance(data, dict):
                        if 'id' in data:
                            items_to_check = [("root", [data])]
                        else:
                            items_to_check = data.items()
                    else:
                        continue
                        
                    for key, value in items_to_check:
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict) and 'id' in item:
                                    entity_id = item['id']
                                    
                                    if entity_id in used_ids:
                                        duplicate_ids.add(entity_id)
                                    used_ids.add(entity_id)
                                    
                                    if entity_id not in registry_entities:
                                        unknown_ids.add(entity_id)
                                        
    if duplicate_ids:
        print(f"CRITICAL ERROR: Duplicate IDs found in facts: {duplicate_ids}")
        sys.exit(1)
        
    if unknown_ids:
        print(f"CRITICAL ERROR: Unknown IDs found in facts (not in registry): {unknown_ids}")
        sys.exit(1)
        
    print(f"SUCCESS: Validated {len(used_ids)} fact IDs against the registry.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="career-data")
    parser.add_argument("--registry-path", default="registry/ids.yml")
    args = parser.parse_args()
    
    validate_ids(args.data_dir, args.registry_path)
