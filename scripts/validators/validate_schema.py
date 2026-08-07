import json
import sys
import jsonschema
from pathlib import Path

def validate_schema(data_path, schema_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
        
    try:
        jsonschema.validate(instance=data, schema=schema)
        print("Schema validation PASS")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Schema validation FAIL: {e.message}")
        print(f"Path: {e.json_path}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="artifacts/profile_domain_model.json")
    parser.add_argument("--schema", default="schemas/profile_domain_model.schema.json")
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent.parent
    data_path = root / args.data
    schema_path = root / args.schema
    
    if not validate_schema(data_path, schema_path):
        sys.exit(1)
