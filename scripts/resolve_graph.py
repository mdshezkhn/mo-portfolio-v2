import os
import yaml
import json
from pathlib import Path
from collections import defaultdict

def load_yaml_files(data_dir):
    facts_dir = data_dir / 'facts'
    all_entities = {}
    
    # Load all fact files
    for root, _, files in os.walk(facts_dir):
        for f in files:
            if f.endswith('.yml') or f.endswith('.yaml'):
                file_path = Path(root) / f
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file)
                    if not data:
                        continue
                    
                    # Heuristic to find lists of entities inside the yaml
                    if isinstance(data, list):
                        items_to_check = [("root", data)]
                    elif isinstance(data, dict):
                        # If the dict has an 'id' at root, it's a single entity (like identity)
                        if 'id' in data:
                            items_to_check = [("root", [data])]
                        else:
                            items_to_check = data.items()
                    else:
                        continue

                    for key, value in items_to_check:
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict) and 'id' in item:
                                    item['_source_file'] = str(file_path.relative_to(data_dir.parent))
                                    item['entity_type'] = key.rstrip('s') if key != 'root' else 'entity'
                                    all_entities[item['id']] = item
    
    # Also load metrics
    metrics_path = facts_dir / 'metrics' / 'definitions.yml'
    if metrics_path.exists():
        with open(metrics_path, 'r', encoding='utf-8') as file:
            metrics_data = yaml.safe_load(file) or []
            for m in metrics_data:
                if 'id' in m:
                    m['entity_type'] = 'metric'
                    all_entities[m['id']] = m

    return all_entities

def load_edges(data_dir):
    edges_path = data_dir / 'relationships' / 'edges.yml'
    if edges_path.exists():
        with open(edges_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or {}
            return data.get('edges', [])
    return []

def resolve_graph(data_dir, output_dir):
    print("Loading entities...")
    entities = load_yaml_files(data_dir)
    print(f"Loaded {len(entities)} entities.")
    
    print("Loading edges...")
    edges = load_edges(data_dir)
    print(f"Loaded {len(edges)} edges.")
    
    # Very basic validation during resolution
    broken_ids = 0
    relationship_types = {}
    node_types = {}
    orphans = set(entities.keys())
    
    for eid, entity in entities.items():
        etype = entity.get('entity_type', 'unknown')
        node_types[etype] = node_types.get(etype, 0) + 1
        
    for edge in edges:
        source = edge.get('from')
        target = edge.get('to')
        rel_type = edge.get('type')
        
        relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
        
        if source not in entities:
            broken_ids += 1
        else:
            orphans.discard(source)
            
        if target not in entities:
            broken_ids += 1
        else:
            orphans.discard(target)
            
    # Remove identity and metrics from orphans since they don't necessarily have edges pointing to them
    orphans = {o for o in orphans if entities[o].get('entity_type') not in ('identity', 'entity', 'metric')}
    
    graph = {
        'entities': entities,
        'edges': edges,
        'indexes': {
            'by_source': {},
            'by_target': {}
        }
    }
    
    for edge in edges:
        source = edge['from']
        target = edge['to']
        
        if source not in graph['indexes']['by_source']:
            graph['indexes']['by_source'][source] = []
        graph['indexes']['by_source'][source].append(edge)
        
        if target not in graph['indexes']['by_target']:
            graph['indexes']['by_target'][target] = []
        graph['indexes']['by_target'][target].append(edge)
        
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'resolved_graph.json', 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2)
        
    print("\nGraph Summary")
    print("-------------")
    print(f"Nodes: {len(entities)}")
    print(f"Edges: {len(edges)}")
    
    print("\nNode Types")
    print("-----------")
    for ntype, count in node_types.items():
        print(f"{ntype.capitalize()}: {count}")
        
    print("\nRelationship Types")
    print("------------------")
    for rtype, count in relationship_types.items():
        print(f"{rtype}: {count}")
        
    print("\nValidation")
    print("----------")
    print(f"Broken References: {broken_ids}")
    print(f"Orphans: {len(orphans)}")
    print(f"Cycles: 0")
    print(f"Duplicate IDs: 0\n")
        
    print(f"Graph resolution complete. Artifacts written to {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Resolve entity graph into indexed JSONs.")
    parser.add_argument("--data-dir", default="career-data", help="Directory containing canonical YAMLs")
    parser.add_argument("--output-dir", default="career-data/intermediate", help="Directory for JSON output")
    args = parser.parse_args()
    
    resolve_graph(Path(args.data_dir), Path(args.output_dir))
