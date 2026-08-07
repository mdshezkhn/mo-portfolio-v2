import os
import sys
import re
from pathlib import Path

try:
    from query_engine import load_graph
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from query_engine import load_graph

def score_quality(graph):
    """
    Score the content quality of the claims in the graph.
    Produces a continuous improvement report (0-100 scores).
    """
    claims = list(graph.claims())
    if not claims:
        print("No claims to score.")
        return
        
    scores = {}
    
    # 1. Evidence Coverage (Ratio of claims with supporting canonical evidence)
    supported_claims = list(graph.claims().supported())
    scores['Evidence Coverage'] = (len(supported_claims) / len(claims)) * 100 if claims else 0
    
    # 2. Quantification (Number of claims with measurable outcomes - simple digits heuristic)
    quantified = 0
    for c in claims:
        stmt = c.get('statement', '')
        if re.search(r'\d+', stmt) or '%' in stmt:
            quantified += 1
    scores['Quantification'] = (quantified / len(claims)) * 100 if claims else 0
    
    # 3. Market Alignment (Claims mapped to a market vs general)
    aligned = sum(1 for c in claims if c.get('markets'))
    scores['Market Alignment'] = (aligned / len(claims)) * 100 if claims else 0
    
    # 4. Leadership Signals (Mentoring, Curriculum, QA, Training)
    leadership_keywords = ['mentor', 'lead', 'curriculum', 'training', 'quality', 'guide', 'head', 'coordinator']
    leadership_count = 0
    for c in claims:
        stmt = c.get('statement', '').lower()
        if any(kw in stmt for kw in leadership_keywords):
            leadership_count += 1
    # Assuming we expect at least 20% leadership claims for a perfect 100
    leadership_ratio = (leadership_count / len(claims)) if claims else 0
    scores['Leadership Signals'] = min(100, (leadership_ratio / 0.20) * 100) if claims else 0
    
    # 5. Readability / Grammar (Sentence length, active voice)
    # Simple heuristic: penalize sentences > 30 words, reward shorter active sentences
    readability_pts = 0
    weak_verbs = ['helped', 'assisted', 'was', 'were', 'been']
    for c in claims:
        stmt = c.get('statement', '')
        words = stmt.split()
        if len(words) < 30 and not any(wv in stmt.lower() for wv in weak_verbs):
            readability_pts += 1
    scores['Readability'] = (readability_pts / len(claims)) * 100 if claims else 0
    
    # 6. Redundancy (Deduplication of core ideas)
    # Very naive check: unique words
    scores['Redundancy'] = 100 # Placeholder for advanced NLP deduplication
    
    # Unused Evidence Check
    all_evidence = [e['id'] for e in graph.evidence()]
    used_evidence = set()
    for edge in graph.edges:
        if edge.get('type') == 'SUPPORTED_BY' and edge.get('to') in all_evidence:
            used_evidence.add(edge.get('to'))
            
    unused_evidence = [eid for eid in all_evidence if eid not in used_evidence]
    scores['Evidence Utilization'] = ((len(all_evidence) - len(unused_evidence)) / len(all_evidence) * 100) if all_evidence else 100
    
    # Compute Overall
    overall = sum(scores.values()) / len(scores)
    
    print("\n================ CONTENT QUALITY ================")
    print(f"Overall                 {int(overall)}")
    print("-------------------------------------------------")
    for dim, score in scores.items():
        print(f"{dim:<23} {int(score)}")
    print("=================================================")
    
    # Claim Coverage metric
    unsupported = [c['id'] for c in claims if c not in supported_claims]
    if unsupported:
        print("\n[WARNING] Claims lacking evidence:")
        for cid in unsupported:
            print(f"  - {cid}")
            
    if unused_evidence:
        print("\n[WARNING] Unused Evidence (Missed Opportunities):")
        for eid in unused_evidence:
            print(f"  - {eid}")
            
    print("\n")
    return scores, overall

def write_history(scores, overall):
    import json
    import csv
    import datetime
    
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "overall": int(overall)
    }
    for k, v in scores.items():
        entry[k] = int(v)
        
    # JSON History
    history_json = artifacts_dir / "metrics_history.json"
    history = []
    if history_json.exists():
        with open(history_json, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                pass
    history.append(entry)
    with open(history_json, "w") as f:
        json.dump(history, f, indent=2)
        
    # CSV History
    history_csv = artifacts_dir / "metrics_history.csv"
    headers = list(entry.keys())
    write_header = not history_csv.exists()
    
    with open(history_csv, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if write_header:
            writer.writeheader()
        writer.writerow(entry)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Content Quality Engine")
    parser.add_argument("--data-dir", default="career-data")
    args = parser.parse_args()
    
    graph = load_graph(args.data_dir)
    scores, overall = score_quality(graph)
    write_history(scores, overall)
