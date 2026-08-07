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

CONTRACT_DEFINITIONS = {
    "contracts/resolved_graph": {
        "title": "Resolver Output Contract",
        "version": "1.0.0",
        "properties": {
            "version": {"type": "string", "const": "1.0.0"},
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "entity_type": {"type": "string"},
                        "data": {"type": "object"}
                    },
                    "required": ["id", "entity_type", "data"]
                }
            },
            "edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "target": {"type": "string"},
                        "relationship": {"type": "string"}
                    },
                    "required": ["source", "target", "relationship"]
                }
            },
            "indexes": {"type": "object"},
            "metadata": {
                "type": "object",
                "properties": {
                    "canonical_schema_version": {"type": "string"}
                },
                "required": ["canonical_schema_version"]
            },
            "statistics": {"type": "object", "description": "Optional"},
            "diagnostics": {"type": "object", "description": "Optional"},
            "orphan_nodes": {"type": "array", "deprecated": True, "description": "remove in v2"}
        },
        "required": ["version", "entities", "edges", "indexes", "metadata"],
        "additionalProperties": False,
        "patternProperties": {
            "^raw_yaml$": {"not": {}}
        }
    },
    "contracts/relationship_vocabulary": {
        "title": "Relationship Vocabulary Contract",
        "version": "1.0.0",
        "properties": {
            "version": {"type": "string", "const": "1.0.0"},
            "relationships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "enum": ["WORKED_AT", "HAS_ROLE", "SUPPORTED_BY", "STUDIED_AT"]},
                        "source_type": {"type": "string"},
                        "target_type": {"type": "string"},
                        "cardinality": {"type": "string", "enum": ["1:1", "1:N", "N:1", "N:M"]}
                    },
                    "required": ["name", "source_type", "target_type", "cardinality"]
                }
            }
        },
        "required": ["version", "relationships"],
        "additionalProperties": False
    },
    "contracts/intermediate": {
        "title": "Intermediate Compiler Schema",
        "version": "1.0.0",
        "properties": {
            "version": {"type": "string", "const": "1.0.0"},
            "facts": {"type": "object"},
            "metrics": {"type": "object"},
            "provenance": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "statement_id": {"type": "string"},
                        "source_ids": {"type": "array", "items": {"type": "string"}},
                        "relationship_ids": {"type": "array", "items": {"type": "string"}},
                        "metric_ids": {"type": "array", "items": {"type": "string"}},
                        "policy_ids": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["statement_id"]
                }
            },
            "build_manifest": {
                "type": "object",
                "properties": {
                    "resolver_version": {"type": "string"},
                    "schema_version": {"type": "string"},
                    "policy_version": {"type": "string"},
                    "generator_versions": {"type": "object"},
                    "input_hashes": {"type": "object"},
                    "output_hashes": {"type": "object"},
                    "warnings": {"type": "array"},
                    "performance": {"type": "object"}
                },
                "required": ["resolver_version", "schema_version", "policy_version", "generator_versions", "input_hashes", "output_hashes"]
            }
        },
        "required": ["version", "facts", "metrics", "provenance", "build_manifest"],
        "additionalProperties": False
    },
    "contracts/policy_api": {
        "title": "Policy API Schema",
        "version": "1.0.0",
        "properties": {
            "version": {"type": "string", "const": "1.0.0"},
            "input": {
                "type": "object",
                "properties": {
                    "intermediate_representation": {"$ref": "intermediate.schema.json"},
                    "rules": {"type": "object"}
                },
                "required": ["intermediate_representation", "rules"]
            },
            "output": {
                "type": "object",
                "properties": {
                    "filtered_intermediate": {"type": "object"},
                    "applied_policies": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["filtered_intermediate", "applied_policies"]
            }
        },
        "required": ["version", "input", "output"],
        "additionalProperties": False
    },
    "contracts/view_models": {
        "title": "View Models Schema",
        "version": "1.0.0",
        "properties": {
            "version": {"type": "string", "const": "1.0.0"},
            "type": {"type": "string", "enum": ["portfolio", "cv", "linkedin", "recruiter_pack"]},
            "market": {"type": "string"},
            "content": {"type": "object"},
            "metadata": {
                "type": "object",
                "properties": {
                    "build_id": {"type": "string"},
                    "provenance": {"type": "array"}
                },
                "required": ["build_id", "provenance"]
            }
        },
        "required": ["version", "type", "content", "metadata"],
        "additionalProperties": False
    }
}

def generate_contracts(output_dir):
    out_path = Path(output_dir)
    # Ensure directories exist
    (out_path / "contracts").mkdir(parents=True, exist_ok=True)

    for schema_name, specific_schema in CONTRACT_DEFINITIONS.items():
        # Merge BASE_TEMPLATE with specific_schema
        merged = {
            "$schema": BASE_TEMPLATE["$schema"],
            "title": specific_schema.get("title", ""),
            "description": f"Version {specific_schema.get('version', '1.0.0')}",
            "type": BASE_TEMPLATE["type"],
            "properties": specific_schema.get("properties", {}),
            "required": specific_schema.get("required", [])
        }
        
        if "additionalProperties" in specific_schema:
            merged["additionalProperties"] = specific_schema["additionalProperties"]
        if "patternProperties" in specific_schema:
            merged["patternProperties"] = specific_schema["patternProperties"]
            
        file_path = out_path / f"{schema_name}.schema.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
            
        print(f"Generated {file_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Interface Contracts (JSON Schemas) for Phase A")
    parser.add_argument("--output-dir", default="schemas", help="Directory to output generated schemas")
    args = parser.parse_args()
    
    generate_contracts(args.output_dir)
