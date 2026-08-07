import os
import re
import json

METADATA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".pdf", ".docx", ".pptx"}

def scan_metadata(inventory, base_dir):
    print("==================================================")
    print(" Phase 3: Executing Document & Asset Metadata Audit")
    print("==================================================")
    
    findings = []
    
    for item in inventory["files"]:
        rel_path = item["rel_path"]
        ext = item["extension"]
        
        if ext in METADATA_EXTENSIONS:
            abs_path = os.path.join(base_dir, rel_path)
            
            # 1. Quick binary inspection for author/software/GPS tags
            try:
                with open(abs_path, "rb") as f:
                    content_bytes = f.read(50000) # Check first 50KB for headers
                    
                # Look for common author/creator strings in headers
                matches = []
                if b"Exif" in content_bytes:
                    matches.append("EXIF Metadata Header Present")
                if b"GPS" in content_bytes or b"gps" in content_bytes:
                    matches.append("GPS Coordinate Metadata Tag")
                if b"Creator" in content_bytes or b"Producer" in content_bytes or b"Author" in content_bytes:
                    matches.append("Embedded Document Author/Creator Property")
                    
                if matches:
                    findings.append({
                        "category": "document_metadata",
                        "severity": "Medium",
                        "file": rel_path,
                        "detail": f"Detected metadata in {ext.upper()} asset: {', '.join(matches)}",
                        "remediation": "Strip EXIF and author document properties using asset sanitization tool."
                    })
            except Exception:
                pass
                
    print(f"-> Metadata Audit completed. Found {len(findings)} media/document items with metadata.")
    return findings
