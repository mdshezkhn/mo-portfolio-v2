import os
import sys
from pathlib import Path

# Try to import graph query engine
try:
    from query_engine import load_graph
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from query_engine import load_graph

def select_claims(graph, market=None, min_confidence=None, limit=None):
    """
    Select claims from the graph based on market and confidence policies.
    Returns (selected_claims, decision_log)
    """
    all_claims = list(graph.claims())
    selected = []
    decision_log = []
    
    levels = {'unverified': 0, 'supported': 1, 'verified': 2}
    min_level = levels.get(min_confidence, 0) if min_confidence else 0
    
    for claim in all_claims:
        cid = claim['id']
        conf = claim.get('confidence', 'unverified')
        claim_level = levels.get(conf, 0)
        claim_markets = claim.get('markets', [])
        
        if market and market not in claim_markets:
            decision_log.append({
                'claim_id': cid,
                'status': 'Rejected',
                'reason': f"Not applicable to {market} market",
                'policy': 'market_rules',
                'confidence': conf,
                'evidence_count': sum(1 for edge in graph.edges if edge.get('from') == cid and edge.get('type') == 'SUPPORTED_BY')
            })
            continue
            
        if claim_level < min_level:
            decision_log.append({
                'claim_id': cid,
                'status': 'Rejected',
                'reason': f"Failed confidence threshold",
                'policy': f"min_confidence={min_confidence}",
                'confidence': conf,
                'evidence_count': sum(1 for edge in graph.edges if edge.get('from') == cid and edge.get('type') == 'SUPPORTED_BY')
            })
            continue
            
        claim_status = claim.get('status', 'draft')
        if claim_status != 'approved':
            decision_log.append({
                'claim_id': cid,
                'status': 'Rejected',
                'reason': f"Claim is not approved (status: {claim_status})",
                'policy': 'editorial_approval',
                'confidence': conf,
                'evidence_count': sum(1 for edge in graph.edges if edge.get('from') == cid and edge.get('type') == 'SUPPORTED_BY')
            })
            continue
            
        selected.append(claim)
        decision_log.append({
            'claim_id': cid,
            'status': 'Selected',
            'reason': 'Passed all policies',
            'policy': 'passed',
            'confidence': conf,
            'evidence_count': sum(1 for edge in graph.edges if edge.get('from') == cid and edge.get('type') == 'SUPPORTED_BY')
        })
        
    # Sort claims by priority if present, otherwise by ID
    def sort_key(claim):
        priority_map = {'high': 0, 'medium': 1, 'low': 2}
        priority = priority_map.get(claim.get('priority', 'low'), 2)
        return (priority, claim['id'])
        
    selected = sorted(selected, key=sort_key)
    
    if limit:
        selected = selected[:limit]
        
    return selected, decision_log

if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Claim Selection Engine")
    parser.add_argument("--data-dir", default="career-data")
    parser.add_argument("--market", default=None, help="Target market (e.g., british)")
    parser.add_argument("--min-confidence", default="supported", choices=["unverified", "supported", "verified"])
    args = parser.parse_args()
    
    graph = load_graph(args.data_dir)
    selected, decision_log = select_claims(graph, market=args.market, min_confidence=args.min_confidence)
    
    print(f"Selected {len(selected)} claims for market '{args.market or 'ALL'}' (min confidence: {args.min_confidence})")
    for claim in selected:
        print(f"[{claim['id']}] ({claim.get('confidence')}) - {claim.get('statement')}")
        
    print("\nDecision Log Summary:")
    for entry in decision_log:
        if entry['status'] == 'Rejected':
            print(f"[{entry['claim_id']}] {entry['status']} - {entry['reason']} (Policy: {entry['policy']})")
            
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    with open(artifacts_dir / "decision_log.json", "w", encoding="utf-8") as f:
        json.dump(decision_log, f, indent=2)
