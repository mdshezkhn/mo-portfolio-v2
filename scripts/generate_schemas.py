import json
import os
from pathlib import Path

# Base schema that all generated schemas must extend
BASE_TEMPLATE = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {},
    "required": []
}

# Flexible date schema accepting strings or object
DATE_SCHEMA = {
    "type": "object"
}

# Orthogonal confidence and review status
CONFIDENCE_ENUM = ["verified", "supported", "plausible", "asserted", "V1", "V2", "V3", "V4", "V5"]
REVIEW_STATUS_ENUM = ["approved", "pending", "conflict", "obsolete"]

# The definitions of specific schemas
SCHEMA_DEFINITIONS = {
    "facts/identity": {
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "title": {"type": "string"}
        },
        "required": ["id"]
    },
    "facts/education": {
        "properties": {
            "education_records": {
                "type": "array"
            }
        },
        "required": ["education_records"]
    },
    "facts/employment": {
        "properties": {
            "employment_records": {
                "type": "array"
            }
        },
        "required": ["employment_records"]
    },
    "facts/roles": {
        "properties": {
            "roles": {
                "type": "array"
            }
        },
        "required": ["roles"]
    },
    "facts/institutions": {
        "properties": {
            "institutions": {
                "type": "array"
            }
        },
        "required": ["institutions"]
    },
    "facts/organisations": {
        "properties": {
            "organisations": {
                "type": "array"
            }
        },
        "required": ["organisations"]
    },
    "facts/evidence_links": {
        "properties": {
            "evidence_links": {
                "type": "array"
            }
        },
        "required": ["evidence_links"]
    },
    "narratives/teaching_philosophy": {
        "properties": {
            "title": {"type": "string"},
            "sections": {"type": "array"}
        },
        "required": ["title", "sections"]
    },
    "narratives/voice": {
        "properties": {
            "tone": {"type": "string"}
        },
        "required": ["tone"]
    },
    "facts/claims": {
        "properties": {
            "claims": {
                "type": "array"
            }
        },
        "required": ["claims"]
    },
    "facts/relationships": {
        "properties": {
            "edges": {
                "type": "array"
            }
        },
        "required": ["edges"]
    },
    "facts/metrics": {
        "properties": {
            "metrics": {
                "type": "array"
            }
        },
        "required": ["metrics"]
    },
    "taxonomies/competency_taxonomy": {
        "properties": {
            "categories": {
                "type": "array"
            }
        },
        "required": ["categories"]
    },
    "facts/competencies": {
        "properties": {
            "competencies": {
                "type": "array"
            }
        },
        "required": ["competencies"]
    }
}

def generate():
    root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
    schemas_dir = root_dir / "schemas"
    
    for relative_path, definition in SCHEMA_DEFINITIONS.items():
        schema_path = schemas_dir / f"{relative_path}.schema.json"
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        
        full_schema = BASE_TEMPLATE.copy()
        full_schema["properties"] = definition.get("properties", {})
        full_schema["required"] = definition.get("required", [])
        
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(full_schema, f, indent=2)
        print(f"Generated {schema_path.relative_to(root_dir)}")

if __name__ == "__main__":
    generate()
