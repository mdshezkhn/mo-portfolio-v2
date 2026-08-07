import json
import yaml
import glob
import sys
import os
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_yaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    schemas_dir = 'schemas'
    facts_dir = 'career-data/facts'
    
    # Map fact file -> schema file
    # Format: facts/X.yml -> schemas/X.schema.json
    fact_files = glob.glob(os.path.join(facts_dir, '*.yml'))
    
    errors = 0
    for fact_file in fact_files:
        basename = os.path.basename(fact_file)
        name_without_ext = os.path.splitext(basename)[0]
        schema_path = os.path.join(schemas_dir, f"{name_without_ext}.schema.json")
        
        if not os.path.exists(schema_path):
            print(f"Skipping {basename}: no schema found at {schema_path}")
            continue
            
        print(f"Validating {basename} against {name_without_ext}.schema.json...")
        schema = load_schema(schema_path)
        data = load_yaml(fact_file)
        
        try:
            # Extract the actual list of facts from the wrapper object
            items_to_validate = data
            if isinstance(data, dict):
                # The facts are usually under a key named after the file (e.g. 'claims')
                key_guess = name_without_ext
                if key_guess in data and isinstance(data[key_guess], list):
                    items_to_validate = data[key_guess]
                else:
                    # Fallback to the first list value found
                    for v in data.values():
                        if isinstance(v, list):
                            items_to_validate = v
                            break

            if isinstance(items_to_validate, list):
                for i, item in enumerate(items_to_validate):
                    try:
                        validate(instance=item, schema=schema)
                    except ValidationError as e:
                        print(f"[FAIL] Validation failed for {basename} at index {i}:")
                        print(f"  Path: {' -> '.join([str(p) for p in e.path])}")
                        print(f"  Error: {e.message}")
                        errors += 1
                if errors == 0:
                    print(f"[PASS] {basename} is valid ({len(items_to_validate)} items).")
            else:
                validate(instance=items_to_validate, schema=schema)
                print(f"[PASS] {basename} is valid.")
        except ValidationError as e:
            print(f"[FAIL] Validation failed for {basename}:")
            print(f"  Path: {' -> '.join([str(p) for p in e.path])}")
            print(f"  Error: {e.message}")
            errors += 1
            
    if errors > 0:
        print(f"\n{errors} schema validation error(s) found.")
        sys.exit(1)
    else:
        print("\nAll files passed schema validation.")

if __name__ == '__main__':
    main()
