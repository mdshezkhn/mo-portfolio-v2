import json
import sys
import hashlib
from datetime import datetime
from pathlib import Path

def compute_hash(data):
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def compile_intermediate(intermediate_dir):
    graph_path = intermediate_dir / 'resolved_graph.json'
    if not graph_path.exists():
        print(f"Error: {graph_path} not found.")
        sys.exit(1)
        
    with open(graph_path, 'r', encoding='utf-8') as f:
        graph = json.load(f)
        
    graph_meta = graph.get('metadata', {})
    
    metadata = {
        "artifact_version": graph_meta.get("artifact_version", "1.0.0"),
        "schema_version": graph_meta.get("schema_version", "1.0.0"),
        "graph_version": graph_meta.get("graph_version", "1.0.0"),
        "resolver_version": graph_meta.get("resolver_version", "1.0.0"),
        "metrics_version": "1.0.0",
        "build_id": graph_meta.get("build_id", "BUILD-V1-001"),
        "generated_at": graph_meta.get("generated_at", datetime.now().isoformat() + "Z"),
        "source_commit": graph_meta.get("source_commit", "HEAD"),
        "input_hash": compute_hash(graph)
    }
    
    # In Vertical Slice, we only have identity, so we'll output the graph as facts.json with metadata
    facts_json = {
        "_metadata": metadata,
        "facts": graph['entities']
    }
    
    out_path = intermediate_dir / 'facts.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(facts_json, f, indent=2)
        
    # Stub timeline.json, relationships.json, metrics.json
    with open(intermediate_dir / 'timeline.json', 'w', encoding='utf-8') as f:
        json.dump({"_metadata": metadata, "timeline": []}, f, indent=2)
        
    with open(intermediate_dir / 'relationships.json', 'w', encoding='utf-8') as f:
        json.dump({"_metadata": metadata, "relationships": graph['edges']}, f, indent=2)
        
    with open(intermediate_dir / 'metrics.json', 'w', encoding='utf-8') as f:
        json.dump({"_metadata": metadata, "metrics": {}}, f, indent=2)
        
    with open(intermediate_dir / 'build_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Intermediate JSONs compiled into {intermediate_dir} with full version metadata and build_manifest.json.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--intermediate-dir", default="career-data/intermediate")
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent
    intermediate_dir = root / args.intermediate_dir
    compile_intermediate(intermediate_dir)
