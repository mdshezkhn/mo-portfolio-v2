import os
import sys
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
    'institution': 'INST',
    'claim': 'CLAIM'
}

def allocate_id(entity_type, slug, base_dir="."):
    base_dir = Path(base_dir)
    registry_path = base_dir / "registry" / "ids.yml"
    
    if not registry_path.exists():
        print(f"CRITICAL ERROR: Registry not found at {registry_path}")
        sys.exit(1)
        
    with open(registry_path, 'r', encoding='utf-8') as file:
        registry = yaml.safe_load(file)
        
    prefix = PREFIXES.get(entity_type.lower())
    if not prefix:
        print(f"CRITICAL ERROR: Unknown entity type: {entity_type}")
        sys.exit(1)
        
    # Find highest ID for this prefix
    max_num = 0
    for entity_id in registry.get('entities', {}).keys():
        if entity_id.startswith(f"{prefix}-"):
            try:
                num = int(entity_id.split('-')[1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
                
    if max_num == 0:
        # Starter block depending on prefix (if missing, we just start at 1000)
        max_num = 999
        
    new_id = f"{prefix}-{max_num + 1}"
    
    # Check if slug exists
    for e_id, details in registry.get('entities', {}).items():
        if details.get('slug') == slug:
            print(f"WARNING: Slug '{slug}' already exists in {e_id}")
            
    registry['entities'][new_id] = {
        'slug': slug,
        'state': 'ALLOCATED',
        'type': entity_type
    }
    
    with open(registry_path, 'w', encoding='utf-8') as file:
        yaml.dump(registry, file, sort_keys=False)
        
    # Create migration op
    migrations_dir = base_dir / "migrations"
    migrations_dir.mkdir(exist_ok=True)
    
    migration_num = len(list(migrations_dir.glob('*.yaml'))) + 1
    migration_filename = f"{migration_num:04d}_allocate_{slug}.yaml"
    
    migration = {
        'migration_id': f"{migration_num:04d}",
        'timestamp': datetime.now().isoformat() + "Z",
        'description': f'Allocate ID for {slug}',
        'operations': [
            {
                'allocate': {
                    'id': new_id,
                    'slug': slug,
                    'state': 'ALLOCATED',
                    'type': entity_type
                }
            }
        ]
    }
    
    with open(migrations_dir / migration_filename, 'w', encoding='utf-8') as f:
        yaml.dump(migration, f, sort_keys=False)
        
    print(f"SUCCESS: Allocated {new_id} for '{slug}'")
    print(f"Created migration: {migration_filename}")
    return new_id

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, help="Entity type (e.g., employment, organisation)")
    parser.add_argument("--slug", required=True, help="Human readable slug")
    parser.add_argument("--base-dir", default=".")
    args = parser.parse_args()
    
    allocate_id(args.type, args.slug, args.base_dir)
