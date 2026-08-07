import os
import yaml
from pathlib import Path
from datetime import datetime

PREFIXES = {
    'identity': 'PERSON',
    'organisation': 'ORG',
    'employment': 'EMP',
    'qualification': 'QUAL',
    'education': 'QUAL',
    'certification': 'CERT',
    'competency': 'COMP',
    'evidence': 'EVID',
    'narrative': 'NARR',
    'role': 'ROLE',
    'institution': 'INST'
}

# Block starts
NEXT_IDS = {
    'PERSON': 1000,
    'ORG': 1000,
    'EMP': 2000,
    'QUAL': 3000,
    'CERT': 4000,
    'COMP': 5000,
    'NARR': 6000,
    'EVID': 7000,
    'ROLE': 8000,
    'INST': 9000
}

def generate_id(entity_type):
    prefix = PREFIXES.get(entity_type.lower())
    if not prefix:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
    id_num = NEXT_IDS[prefix]
    NEXT_IDS[prefix] += 1
    return f"{prefix}-{id_num}"

def bootstrap(base_dir="career-data"):
    base_dir = Path(base_dir)
    data_dir = base_dir / "facts"
    
    registry = {
        'registry_version': '1.0',
        'entities': {}
    }
    
    operations = []
    
    id_mapping = {} # old_id -> new_id
    
    # Pass 1: Allocate new IDs and generate registry + operations
    for root, dirs, files in os.walk(data_dir):
        if 'metrics' in root:
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
                                    old_id = item['id']
                                    entity_type = item.get('entity_type')
                                    if not entity_type:
                                        entity_type = key.rstrip('s') if key != 'root' else path.stem.rstrip('s')
                                    if entity_type == 'unknown':
                                        print(f"Warning: Unknown type in {path} for key {key} item {item}")
                                        
                                    new_id = generate_id(entity_type)
                                    id_mapping[old_id] = new_id
                                    
                                    # Use old id as a base for the slug
                                    slug = old_id.lower().replace('-', '_')
                                    
                                    registry['entities'][new_id] = {
                                        'slug': slug,
                                        'state': 'PUBLISHED',
                                        'type': entity_type
                                    }
                                    
                                    operations.append({
                                        'allocate': {
                                            'id': new_id,
                                            'slug': slug,
                                            'state': 'PUBLISHED',
                                            'type': entity_type
                                        }
                                    })
                                    
    # Write registry
    Path(base_dir / "registry").mkdir(exist_ok=True, parents=True)
    with open(base_dir / "registry/ids.yml", 'w', encoding='utf-8') as f:
        yaml.dump(registry, f, sort_keys=False)
        
    # Write migration
    Path(base_dir / "migrations").mkdir(exist_ok=True, parents=True)
    migration = {
        'migration_id': '0001',
        'timestamp': datetime.now().isoformat() + "Z",
        'description': 'Initial ID allocation mapping old string IDs to block-reserved opaque IDs.',
        'operations': operations
    }
    with open(base_dir / "migrations/0001_initial_id_allocation.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(migration, f, sort_keys=False)
        
    print(f"Generated registry with {len(registry['entities'])} entities.")
    
    # Pass 2: Update all files with new IDs and references
    def update_refs(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and v in id_mapping:
                    node[k] = id_mapping[v]
                elif isinstance(v, list) and all(isinstance(x, str) for x in v):
                    node[k] = [id_mapping.get(x, x) for x in v]
                else:
                    update_refs(v)
        elif isinstance(node, list):
            for item in node:
                update_refs(item)

    # Rewrite facts
    for root, _, files in os.walk(data_dir):
        for f in files:
            if f.endswith('.yml') or f.endswith('.yaml'):
                path = Path(root) / f
                with open(path, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file)
                
                if data:
                    update_refs(data)
                    with open(path, 'w', encoding='utf-8') as out_file:
                        yaml.dump(data, out_file, sort_keys=False)

    # Rewrite relationships
    edges_path = base_dir / "relationships/edges.yml"
    if edges_path.exists():
        with open(edges_path, 'r', encoding='utf-8') as file:
            edges_data = yaml.safe_load(file)
        if edges_data:
            update_refs(edges_data)
            with open(edges_path, 'w', encoding='utf-8') as out_file:
                yaml.dump(edges_data, out_file, sort_keys=False)
                
    print("Rewrote all facts and relationships to use new IDs.")

if __name__ == "__main__":
    import sys
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    bootstrap(base_dir)
