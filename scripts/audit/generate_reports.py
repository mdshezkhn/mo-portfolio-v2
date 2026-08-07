import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.audit.inventory import generate_inventory
from scripts.audit.security import scan_security
from scripts.audit.pii import scan_pii
from scripts.audit.metadata import scan_metadata
from scripts.audit.git_history import audit_git_history
from scripts.audit.release_readiness import scan_release_readiness
from scripts.audit.attack_surface import scan_attack_surface

SCHEMA_VERSION = "1.0.0"
AUDIT_DIR = os.path.join(BASE_DIR, "audit")

def get_git_sha(base_dir):
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=base_dir)
        return res.stdout.strip() if res.returncode == 0 else "unknown"
    except Exception:
        return "unknown"

def get_git_branch(base_dir):
    try:
        res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, cwd=base_dir)
        return res.stdout.strip() if res.returncode == 0 else "unknown"
    except Exception:
        return "unknown"

def run_full_audit():
    start_time = datetime.now()
    
    # 1. Phase 0 Inventory
    inventory = generate_inventory()
    inventory_hash = hashlib.sha256(json.dumps(inventory).encode("utf-8")).hexdigest()
    
    # 2. Phase 1 Security
    security_findings = scan_security(inventory, BASE_DIR)
    
    # 3. Phase 2 PII
    pii_findings = scan_pii(inventory, BASE_DIR)
    
    # 4. Phase 3 Metadata
    metadata_findings = scan_metadata(inventory, BASE_DIR)
    
    # 5. Phase 4 Git History
    git_results = audit_git_history(BASE_DIR)
    
    # 6. Phase 5 Release Readiness
    readiness_findings = scan_release_readiness(inventory, BASE_DIR)
    
    # 7. Phase 6 Attack Surface
    attack_surface_results = scan_attack_surface(inventory, BASE_DIR)
    
    # Aggregate counts by severity
    all_findings = security_findings + pii_findings + metadata_findings + git_results.get("findings", []) + readiness_findings
    
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0}
    for f in all_findings:
        sev = f.get("severity", "Medium")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
    provenance = {
        "timestamp": start_time.isoformat(),
        "git_commit_sha": get_git_sha(BASE_DIR),
        "git_branch": get_git_branch(BASE_DIR),
        "policy_version": "1.0.0",
        "inventory_sha256": inventory_hash,
        "tool_version": "v2.0.0"
    }
    
    canonical_results = {
        "schema_version": SCHEMA_VERSION,
        "provenance": provenance,
        "summary": {
            "total_findings": len(all_findings),
            "severity_counts": severity_counts
        },
        "findings": {
            "security": security_findings,
            "pii": pii_findings,
            "metadata": metadata_findings,
            "git_history": git_results,
            "release_readiness": readiness_findings,
            "attack_surface": attack_surface_results
        }
    }
    
    # Write canonical JSON
    results_json_path = os.path.join(AUDIT_DIR, "audit_results.json")
    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(canonical_results, f, indent=2)
    print(f"-> Canonical source of truth saved to: {results_json_path}")
    
    # Generate Markdown reports
    render_markdown_reports(canonical_results)
    
    # Write audit manifest
    duration_s = (datetime.now() - start_time).total_seconds()
    write_manifest(provenance, duration_s, canonical_results)

def render_markdown_reports(data):
    prov = data["provenance"]
    prov_hdr = f"> **Audit Provenance**: Timestamp: `{prov['timestamp']}` | Git SHA: `{prov['git_commit_sha']}` | Branch: `{prov['git_branch']}` | Tool: `{prov['tool_version']}`\n\n"
    
    # 1. SECURITY_AUDIT.md
    sec_path = os.path.join(AUDIT_DIR, "SECURITY_AUDIT.md")
    sec_findings = data["findings"]["security"]
    with open(sec_path, "w", encoding="utf-8") as f:
        f.write("# Repository Security Audit Report\n\n" + prov_hdr)
        f.write("## Executive Summary\n")
        f.write(f"Total Security Findings: **{len(sec_findings)}**\n\n")
        f.write("| Severity | Category | File | Finding Detail | Remediation |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        if not sec_findings:
            f.write("| PASS | None | - | Zero security risks or secrets detected | None required |\n")
        else:
            for s in sec_findings:
                f.write(f"| **{s['severity']}** | {s['category']} | `{s['file']}` | {s['detail']} | {s['remediation']} |\n")
    print(f"-> Generated {sec_path}")

    # 2. PII_AND_METADATA_AUDIT.md
    pii_path = os.path.join(AUDIT_DIR, "PII_AND_METADATA_AUDIT.md")
    pii_findings = data["findings"]["pii"]
    meta_findings = data["findings"]["metadata"]
    with open(pii_path, "w", encoding="utf-8") as f:
        f.write("# PII & Document Metadata Audit Report\n\n" + prov_hdr)
        f.write("## PII Findings\n")
        f.write("| Severity | File | Finding Detail | Remediation |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        if not pii_findings:
            f.write("| PASS | - | Zero unapproved PII leaks detected | None |\n")
        else:
            for p in pii_findings:
                f.write(f"| **{p['severity']}** | `{p['file']}` | {p['detail']} | {p['remediation']} |\n")
                
        f.write("\n## Document & Asset Metadata Findings\n")
        f.write("| Severity | File | Finding Detail | Remediation |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        if not meta_findings:
            f.write("| PASS | - | Zero sensitive document metadata headers detected | None |\n")
        else:
            for m in meta_findings:
                f.write(f"| **{m['severity']}** | `{m['file']}` | {m['detail']} | {m['remediation']} |\n")
    print(f"-> Generated {pii_path}")

    # 3. RELEASE_READINESS.md
    rr_path = os.path.join(AUDIT_DIR, "RELEASE_READINESS.md")
    rr_findings = data["findings"]["release_readiness"]
    with open(rr_path, "w", encoding="utf-8") as f:
        f.write("# Release Readiness & Supply Chain Audit Report\n\n" + prov_hdr)
        f.write("| Severity | Category | File | Finding Detail | Remediation |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        if not rr_findings:
            f.write("| PASS | Readiness | - | Repository meets all release readiness & supply chain criteria | None |\n")
        else:
            for r in rr_findings:
                f.write(f"| **{r['severity']}** | {r['category']} | `{r['file']}` | {r['detail']} | {r['remediation']} |\n")
    print(f"-> Generated {rr_path}")

    # 4. PUBLIC_ATTACK_SURFACE.md
    pas_path = os.path.join(AUDIT_DIR, "PUBLIC_ATTACK_SURFACE.md")
    pas_data = data["findings"]["attack_surface"]
    with open(pas_path, "w", encoding="utf-8") as f:
        f.write("# Public Attack Surface & OSINT Assessment Report\n\n" + prov_hdr)
        f.write(f"### Impersonation Risk Level: **{pas_data['impersonation_risk']}**\n\n")
        f.write(f"### Summary\n{pas_data['evaluation_summary']}\n\n")
        f.write("### Exposed Portfolio Attributes\n")
        for k, v in pas_data["exposed_attributes"].items():
            f.write(f"- **{k.replace('_', ' ').title()}**: {v}\n")
        f.write("\n### Governance Recommendations\n")
        for rec in pas_data["recommendations"]:
            f.write(f"- {rec}\n")
    print(f"-> Generated {pas_path}")

def write_manifest(prov, duration_s, data):
    manifest_path = os.path.join(AUDIT_DIR, "audit_manifest.json")
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "provenance": prov,
        "execution_summary": {
            "duration_seconds": round(duration_s, 2),
            "executed_phases": ["Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6"],
            "skipped_phases": [],
            "exit_code": 0
        },
        "findings_summary": data["summary"]
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"-> Audit Manifest written to: {manifest_path}\n")

if __name__ == "__main__":
    run_full_audit()
