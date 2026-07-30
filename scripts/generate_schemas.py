import json
import os
from pathlib import Path

# Base schema that all generated schemas must extend
BASE_TEMPLATE = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "schema_version": {"type": "number", "const": 1.0}
    },
    "required": [
        "schema_version"
    ]
}

# ISO-8601 structured dates
DATE_SCHEMA = {
    "type": "object",
    "properties": {
        "start": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "pattern": "^([0-9]{4}(-[0-9]{2})?|UNKNOWN)$"}
            },
            "required": ["date"]
        },
        "end": {
            "type": "object",
            "properties": {
                "date": {"type": ["string", "null"], "pattern": "^([0-9]{4}(-[0-9]{2})?|UNKNOWN)$"},
                "present": {"type": "boolean"}
            }
        }
    },
    "required": ["start"]
}

# Orthogonal confidence and review status
CONFIDENCE_ENUM = ["verified", "supported", "asserted", "unknown"]
REVIEW_STATUS_ENUM = ["active", "pending", "deprecated", "conflict"]

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
                        "dates": DATE_SCHEMA,
                        "confidence": {"type": "string", "enum": CONFIDENCE_ENUM},
                        "review_status": {"type": "string", "enum": REVIEW_STATUS_ENUM},
                        "primary_evidence_id": {"type": "string", "pattern": "^(E-[0-9]{4}|N/A)$"},
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
                    "required": ["id", "degree", "institution_id", "institution", "dates", "confidence", "review_status", "primary_evidence_id", "publication"]
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
                        "role_id": {"type": "string", "pattern": "^ROLE-[0-9]{3}$"},
                        "employer": {"type": "string"},
                        "dates": DATE_SCHEMA,
                        "location": {"type": "string"},
                        "confidence": {"type": "string", "enum": CONFIDENCE_ENUM},
                        "review_status": {"type": "string", "enum": REVIEW_STATUS_ENUM},
                        "primary_evidence_id": {"type": "string", "pattern": "^(E-[0-9]{4}|N/A)$"}
                    },
                    "required": ["id", "employer_id", "role_id", "employer", "dates", "location", "confidence", "review_status", "primary_evidence_id"]
                }
            }
        },
        "required": ["employment_records"]
    },
    "facts/roles": {
        "properties": {
            "roles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "pattern": "^ROLE-[0-9]{3}$"},
                        "title": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["id", "title"]
                }
            }
        },
        "required": ["roles"]
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
    "facts/evidence_links": {
        "properties": {
            "evidence_links": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "fact_id": {"type": "string", "pattern": "^(EMP|EDU|CERT|ORG|INST)-[0-9]{3}$"},
                        "evidence_ids": {
                            "type": "array",
                            "items": {"type": "string", "pattern": "^E-[0-9]{4}$"}
                        }
                    },
                    "required": ["fact_id", "evidence_ids"]
                }
            }
        },
        "required": ["evidence_links"]
    },
    "narratives/teaching_philosophy": {
        "properties": {
            "teaching_philosophy": {
                "type": "object",
                "properties": {
                    "confidence": {"type": "string", "enum": CONFIDENCE_ENUM},
                    "review_status": {"type": "string", "enum": REVIEW_STATUS_ENUM},
                    "authored_by": {"type": "string", "const": "Mohammed Shehzad Khan"},
                    "content": {"type": "string"}
                },
                "required": ["confidence", "review_status", "authored_by", "content"]
            }
        },
        "required": ["teaching_philosophy"]
    },
    "narratives/voice": {
        "properties": {
            "voice": {
                "type": "object",
                "properties": {
                    "tone": {"type": "array", "items": {"type": "string"}},
                    "vocabulary_preferences": {"type": "array", "items": {"type": "string"}},
                    "prohibited_terms": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["tone"]
            }
        },
        "required": ["voice"]
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
