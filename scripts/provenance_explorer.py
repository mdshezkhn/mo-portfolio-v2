import os
import sys
from pathlib import Path

try:
    from query_engine import load_graph
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from query_engine import load_graph

def trace_provenance(graph, claim_id):
    """
    Output the lineage and justification of a given claim.
    """
    claim_query = graph.entity(claim_id)
    if not claim_query:
        print(f"Error: Claim {claim_id} not found.")
        return
        
    claim = list(claim_query)[0]
    
    print(f"\n================ PROVENANCE TRACE ================")
    print(f"Claim:        {claim['id']}")
    print(f"Statement:    \"{claim.get('statement', '').strip()}\"")
    print(f"Type:         {claim.get('claim_type')}")
    print(f"Confidence:   {claim.get('confidence').upper()}")
    print(f"Markets:      {', '.join(claim.get('markets', []))}")
    print(f"Priority:     {claim.get('priority')}")
    print(f"==================================================")
    
    print("\nWhy was it chosen? (Policy & Selection)")
    print(f"  -> Because it targets markets: {claim.get('markets')}")
    print(f"  -> Because it has priority: {claim.get('priority')}")
    print(f"  -> Because it reached confidence threshold: {claim.get('confidence')}")
    
    print("\nWhere did it come from? (Canonical Facts)")
    
    upstream = claim_query.get_downstream('SUPPORTED_BY')
    if not upstream:
        print("  -> No supporting canonical facts found. (UNVERIFIED)")
    else:
        for u in upstream:
            print(f"  -> [SUPPORTED_BY] {u['id']} ({u.get('entity_type')})")
            
            # Trace one level deeper for employments or qualifications
            deeper = graph.entity(u['id']).get_downstream()
            for d in deeper:
                if d['id'] != claim_id:
                    print(f"       -> [SUPPORTED_BY] {d['id']} ({d.get('entity_type')})")
                    
    print("==================================================\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Provenance Explorer")
    parser.add_argument("--claim-id", required=True, help="Claim ID to trace")
    parser.add_argument("--data-dir", default="career-data")
    args = parser.parse_args()
    
    graph = load_graph(args.data_dir)
    trace_provenance(graph, args.claim_id)
