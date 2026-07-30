import json
import os
from pathlib import Path

# Base schema that all generated schemas must extend
# Enforces the 6th Recommendation: Per-file metadata
BASE_TEMPLATE = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "schema_version": {"type": "number", "const": 1.0},
        "profile_version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
        "last_reviewed": {"type": "string", "format": "date"},
        "owner": {"type": "string", "const": "Mohammed Shehzad Khan"},
        "status": {"type": "string", "const": "canonical"}
    },
    "required": [
        "schema_version",
        "profile_version",
        "last_reviewed",
        "owner",
        "status"
    ]
}

# Add a standard provenance block that most schemas will use for their items
PROVENANCE_SCHEMA = {
    "type": "object",
    "properties": {
        "authority": {"type": "string", "enum": ["evidence", "human_assertion"]},
        "source_id": {"type": "string"},
        "extracted_from": {"type": "string"},
        "decision": {"type": "string"}
    },
    "required": ["authority"]
}

# The definitions of specific schemas
SCHEMA_DEFINITIONS = {
    "facts/identity": {
        "properties": {
            "name": {"type": "string"},
            "title": {"type": "string"}
        },
        "required": ["name"]
    },
    "facts/education": {
        "properties": {
            "education_records": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "pattern": "^EDU-[0-9]{3}$"},
                        "degree": {"type": "string"},
                        "institution_id": {"type": "string", "pattern": "^INST-[0-9]{3}$"},
                        "institution": {"type": "string"},
                        "years": {"type": "string"},
                        "confidence": {"type": "string", "enum": ["verified", "supported", "plausible", "human_assertion", "needs_review"]},
                        "source": PROVENANCE_SCHEMA,
                        "evidence_id": {"type": "string", "pattern": "^(E-[0-9]{4}|N/A)$"},
                        "institution_recognition_status": {"type": "string"},
                        "publication": {
                            "type": "object",
                            "properties": {
                                "public_cv": {"type": "boolean"},
                                "linkedin": {"type": "boolean"},
                                "recruiter_pack": {"type": "string"},
                                "premium_schools": {"type": "boolean"},
                                "notes": {"type": "string"}
                            },
                            "required": ["public_cv", "linkedin"]
                        }
                    },
                    "required": ["id", "degree", "institution_id", "institution", "years", "confidence", "source", "evidence_id", "publication"]
                }
            }
        },
        "required": ["education_records"]
    },
    "facts/employment": {
        "properties": {
            "employment_records": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "pattern": "^EMP-[0-9]{3}$"},
                        "employer_id": {"type": "string", "pattern": "^ORG-[0-9]{3}$"},
                        "employer": {"type": "string"},
                        "portfolio_display_title": {"type": "string"},
                        "date": {"type": "string"},
                        "location": {"type": "string"},
                        "confidence": {"type": "string", "enum": ["verified", "supported", "plausible", "needs_review"]},
                        "source": PROVENANCE_SCHEMA,
                        "evidence_id": {"type": "string", "pattern": "^(E-[0-9]{4}|N/A)$"}
                    },
                    "required": ["id", "employer_id", "employer", "portfolio_display_title", "date", "location", "confidence", "source", "evidence_id"]
                }
            }
        },
        "required": ["employment_records"]
    },
    "facts/institutions": {
        "properties": {
            "institutions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "pattern": "^INST-[0-9]{3}$"},
                        "canonical_name": {"type": "string"},
                        "aliases": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["id", "canonical_name"]
                }
            }
        },
        "required": ["institutions"]
    },
    "facts/organisations": {
        "properties": {
            "organisations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "pattern": "^ORG-[0-9]{3}$"},
                        "canonical_name": {"type": "string"},
                        "aliases": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["id", "canonical_name"]
                }
            }
        },
        "required": ["organisations"]
    },
    "narratives/teaching_philosophy": {
        "properties": {
            "teaching_philosophy": {
                "type": "object",
                "properties": {
                    "confidence": {"type": "string", "const": "human_assertion"},
                    "evidence_id": {"type": "string", "const": "N/A"},
                    "authored_by": {"type": "string", "const": "Mohammed Shehzad Khan"},
                    "content": {"type": "string"}
                },
                "required": ["confidence", "evidence_id", "authored_by", "content"]
            }
        },
        "required": ["teaching_philosophy"]
    }
}

def generate_schemas(output_dir):
    out_path = Path(output_dir)
    # Ensure directories exist
    (out_path / "facts").mkdir(parents=True, exist_ok=True)
    (out_path / "narratives").mkdir(parents=True, exist_ok=True)

    for schema_name, specific_schema in SCHEMA_DEFINITIONS.items():
        # Merge BASE_TEMPLATE with specific_schema
        merged = {
            "$schema": BASE_TEMPLATE["$schema"],
            "type": BASE_TEMPLATE["type"],
            "properties": {**BASE_TEMPLATE["properties"], **specific_schema.get("properties", {})},
            "required": BASE_TEMPLATE["required"] + specific_schema.get("required", [])
        }
        
        file_path = out_path / f"{schema_name}.schema.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
            
        print(f"Generated {file_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate JSON Schemas for the Career OS")
    parser.add_argument("--output-dir", default="schemas", help="Directory to output generated schemas")
    args = parser.parse_args()
    
    generate_schemas(args.output_dir)
