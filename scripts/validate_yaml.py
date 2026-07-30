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

def build_id_registry(data_dir):
    """
    Builds a registry of all valid IDs from the reference files
    to enable referential integrity checking.
    """
    registry = {
        'institutions': set(),
        'organisations': set()
    }
    
    inst_file = data_dir / "facts" / "institutions.yml"
    if inst_file.exists():
        data = load_yaml(inst_file)
        for inst in data.get("institutions", []):
            registry['institutions'].add(inst['id'])
            
    org_file = data_dir / "facts" / "organisations.yml"
    if org_file.exists():
        data = load_yaml(org_file)
        for org in data.get("organisations", []):
            registry['organisations'].add(org['id'])
            
    return registry

def check_referential_integrity(yaml_data, file_type, registry):
    """
    Checks that foreign keys (like institution_id) point to valid records.
    """
    errors = []
    
    if file_type == "facts/education":
        for record in yaml_data.get("education_records", []):
            inst_id = record.get("institution_id")
            if inst_id and inst_id not in registry['institutions']:
                errors.append(f"Record {record.get('id')} references unknown institution_id: {inst_id}")
                
    elif file_type == "facts/employment":
        for record in yaml_data.get("employment_records", []):
            org_id = record.get("employer_id")
            if org_id and org_id not in registry['organisations']:
                errors.append(f"Record {record.get('id')} references unknown employer_id: {org_id}")
                
    return len(errors) == 0, errors

def main():
    root_dir = Path(__file__).parent.parent
    data_dir = root_dir / "career-data"
    schema_dir = root_dir / "schemas"
    
    if not data_dir.exists() or not schema_dir.exists():
        print("Error: Required directories (career-data, schemas) not found.")
        sys.exit(1)
        
    registry = build_id_registry(data_dir)
    has_errors = False
    
    # Iterate through all yaml files in career-data
    for yaml_path in data_dir.rglob("*.yml"):
        rel_path = yaml_path.relative_to(data_dir)
        # Construct schema path (e.g. career-data/facts/education.yml -> schemas/facts/education.schema.json)
        file_type = str(rel_path.with_suffix('')).replace('\\', '/')
        schema_path = schema_dir / f"{file_type}.schema.json"
        
        if not schema_path.exists():
            print(f"[{file_type}] SKIP: No schema found at {schema_path}")
            continue
            
        try:
            yaml_data = load_yaml(yaml_path)
        except Exception as e:
            print(f"[{file_type}] FAIL: Invalid YAML syntax - {e}")
            has_errors = True
            continue
            
        # 1. Schema Validation
        is_valid, error_msg = validate_against_schema(yaml_data, schema_path)
        if not is_valid:
            print(f"[{file_type}] FAIL Schema Validation: {error_msg}")
            has_errors = True
            continue
            
        # 2. Referential Integrity
        is_ref_valid, ref_errors = check_referential_integrity(yaml_data, file_type, registry)
        if not is_ref_valid:
            print(f"[{file_type}] FAIL Referential Integrity:")
            for err in ref_errors:
                print(f"  - {err}")
            has_errors = True
            continue
            
        print(f"[{file_type}] PASS")
        
    if has_errors:
        print("\nValidation FAILED.")
        sys.exit(1)
    else:
        print("\nValidation PASSED. Data model is consistent.")
        sys.exit(0)

if __name__ == "__main__":
    main()
