import yaml
import jsonschema
import json
from pathlib import Path
import sys

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_against_schema(yaml_data, schema_path):
    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance=yaml_data, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, e.message

def build_registries(data_dir):
    registry = {
        'institutions': set(),
        'organisations': set(),
        'roles': set(),
        'aliases': set(),
        'used_roles': set(),
        'evidence_ids': set()
    }
    
    inst_file = data_dir / "facts" / "institutions.yml"
    if inst_file.exists():
        data = load_yaml(inst_file)
        for inst in data.get("institutions", []):
            registry['institutions'].add(inst['id'])
            for alias in inst.get('aliases', []):
                alias_lower = alias.strip().lower()
                if alias_lower in registry['aliases']:
                    print(f"Warning: Duplicate alias found: {alias}")
                registry['aliases'].add(alias_lower)
            
    org_file = data_dir / "facts" / "organisations.yml"
    if org_file.exists():
        data = load_yaml(org_file)
        for org in data.get("organisations", []):
            registry['organisations'].add(org['id'])
            for alias in org.get('aliases', []):
                alias_lower = alias.strip().lower()
                if alias_lower in registry['aliases']:
                    print(f"Warning: Duplicate alias found: {alias}")
                registry['aliases'].add(alias_lower)
                
    roles_file = data_dir / "facts" / "roles.yml"
    if roles_file.exists():
        data = load_yaml(roles_file)
        for role in data.get("roles", []):
            registry['roles'].add(role['id'])
            
    evidence_file = data_dir / "facts" / "evidence_links.yml"
    if evidence_file.exists():
        data = load_yaml(evidence_file)
        for link in data.get("evidence_links", []):
            for eid in link.get("evidence_ids", []):
                registry['evidence_ids'].add(eid)
                
    return registry

def check_referential_integrity(yaml_data, file_type, registry):
    errors = []
    
    if file_type == "facts/education":
        for record in yaml_data.get("education_records", []):
            inst_id = record.get("institution_id")
            if inst_id and inst_id not in registry['institutions']:
                errors.append(f"Record {record.get('id')} references unknown institution_id: {inst_id}")
            # Note: We aren't doing strict evidence checks against manifest.yml here yet,
            # but we could check primary_evidence_id
                
    elif file_type == "facts/employment":
        for record in yaml_data.get("employment_records", []):
            org_id = record.get("employer_id")
            role_id = record.get("role_id")
            
            if org_id and org_id not in registry['organisations']:
                errors.append(f"Record {record.get('id')} references unknown employer_id: {org_id}")
            if role_id and role_id not in registry['roles']:
                errors.append(f"Record {record.get('id')} references unknown role_id: {role_id}")
            if role_id:
                registry['used_roles'].add(role_id)
                
    return len(errors) == 0, errors

def main():
    root_dir = Path(__file__).parent.parent
    data_dir = root_dir / "career-data"
    schema_dir = root_dir / "schemas"
    
    if not data_dir.exists() or not schema_dir.exists():
        print("Error: Required directories (career-data, schemas) not found.")
        sys.exit(1)
        
    registry = build_registries(data_dir)
    has_errors = False
    
    for yaml_path in data_dir.rglob("*.yml"):
        rel_path = yaml_path.relative_to(data_dir)
        file_type = str(rel_path.with_suffix('')).replace('\\', '/')
        schema_path = schema_dir / f"{file_type}.schema.json"
        
        if not schema_path.exists():
            continue
            
        try:
            yaml_data = load_yaml(yaml_path)
        except Exception as e:
            print(f"[{file_type}] FAIL: Invalid YAML syntax - {e}")
            has_errors = True
            continue
            
        is_valid, error_msg = validate_against_schema(yaml_data, schema_path)
        if not is_valid:
            print(f"[{file_type}] FAIL Schema Validation: {error_msg}")
            has_errors = True
            continue
            
        is_ref_valid, ref_errors = check_referential_integrity(yaml_data, file_type, registry)
        if not is_ref_valid:
            print(f"[{file_type}] FAIL Referential Integrity:")
            for err in ref_errors:
                print(f"  - {err}")
            has_errors = True
            continue
            
        print(f"[{file_type}] PASS")
        
    # Check for orphan roles
    orphan_roles = registry['roles'] - registry['used_roles']
    if orphan_roles:
        print(f"\nWarning: Orphan roles detected (no employment record uses these): {orphan_roles}")
        
    # Add simple check against evidence manifest if it exists
    manifest_file = root_dir / "evidence" / "manifest.yml"
    if manifest_file.exists():
        manifest_data = load_yaml(manifest_file)
        # Assuming manifest contains entries with ID
        manifest_ids = {item.get('id') for item in manifest_data.get('evidence', [])}
        unused_evidence = manifest_ids - registry['evidence_ids']
        if unused_evidence:
            print(f"\nWarning: Unused evidence in manifest: {unused_evidence}")
        missing_evidence = registry['evidence_ids'] - manifest_ids
        if missing_evidence:
            print(f"\nError: Evidence IDs linked in facts but missing in manifest: {missing_evidence}")
            has_errors = True
        
    if has_errors:
        print("\nValidation FAILED.")
        sys.exit(1)
    else:
        print("\nValidation PASSED. Data model is consistent.")
        sys.exit(0)

if __name__ == "__main__":
    main()
