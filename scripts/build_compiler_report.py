import json
from pathlib import Path
import datetime

def generate_report():
    artifacts_dir = Path("artifacts")
    
    report_lines = [
        "# Compiler Build Report",
        f"Generated at: {datetime.datetime.now().isoformat()}",
        ""
    ]
    
    # 1. Quality History
    metrics_path = artifacts_dir / "metrics_history.json"
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            history = json.load(f)
            if history:
                latest = history[-1]
                report_lines.append("## Content Quality")
                report_lines.append(f"- **Overall Score**: {latest.get('overall')}/100")
                for k, v in latest.items():
                    if k not in ['timestamp', 'overall']:
                        report_lines.append(f"  - {k}: {v}")
                report_lines.append("")
                
    # 2. Claim Utilization
    approved_claims = 0
    selected_claims = 0
    rendered_claims = 0
    
    graph_path = artifacts_dir.parent / "career-data" / "intermediate" / "resolved_graph.json"
    if graph_path.exists():
        with open(graph_path, "r", encoding="utf-8") as f:
            graph = json.load(f)
            approved_claims = sum(1 for e in graph['entities'].values() if e.get('entity_type') == 'claim' and e.get('status') == 'approved')
            
    decision_path = artifacts_dir / "decision_log.json"
    if decision_path.exists():
        with open(decision_path, "r", encoding="utf-8") as f:
            log = json.load(f)
            selected_claims = sum(1 for e in log if e['status'] == 'Selected')
            rejected_claims = sum(1 for e in log if e['status'] == 'Rejected')
            
            report_lines.append("## Claim Utilization")
            report_lines.append("| Metric | Value |")
            report_lines.append("|---|---|")
            report_lines.append(f"| Approved | {approved_claims} |")
            report_lines.append(f"| Selected | {selected_claims} |")
            
            vm_path = artifacts_dir / "professional_profile_vm.json"
            if vm_path.exists():
                with open(vm_path, "r", encoding="utf-8") as f:
                    vm = json.load(f)
                    rendered_statements = set()
                    for stmt in vm.get('executive_summary', []): rendered_statements.add(stmt)
                    for exp in vm.get('experience', []):
                        for stmt in exp.get('highlights', []): rendered_statements.add(stmt)
                    rendered_claims = len(rendered_statements)
            
            report_lines.append(f"| Rendered | {rendered_claims} |")
            report_lines.append("")
            
            report_lines.append("## Selection Engine Decisions")
            report_lines.append(f"- Claims Selected: {selected_claims}")
            report_lines.append(f"- Claims Rejected: {rejected_claims}")
            
            report_lines.append("\n### Rejections Summary")
            for entry in log:
                if entry['status'] == 'Rejected':
                    report_lines.append(f"- **{entry['claim_id']}**: {entry['reason']} (Policy: {entry['policy']})")
                    
    # Write report
    report_path = artifacts_dir / "compiler_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Generated Compiler Report at {report_path}")

if __name__ == "__main__":
    generate_report()
