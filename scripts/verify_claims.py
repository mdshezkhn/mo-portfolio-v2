#!/usr/bin/env python3
"""Validator for CLAIM_REGISTER.md in the portfolio repository.
Ensures every claim has a valid Recruiter Value and Recruitment Priority.
"""
import re
import sys
import pathlib

ALLOWED_RECRUITER_VALUES = {"High", "Medium", "Low"}
ALLOWED_RECRUITMENT_PRIORITIES = {"Immediate", "High", "Medium", "Low"}

def validate_claims(content: str):
    errors = []
    
    # Split content by claim headers or rows to parse
    # Actually, the simplest way is to find all instances of Recruiter Value and Priority
    
    # Check all Recruiter Value rows
    rv_matches = re.finditer(r"\|\s*\*\*Recruiter Value\*\*\s*\|\s*(.*?)\s*\|", content)
    for i, match in enumerate(rv_matches, 1):
        val = match.group(1).strip()
        if val not in ALLOWED_RECRUITER_VALUES:
            errors.append(f"Claim #{i} has invalid Recruiter Value: '{val}'. Allowed: {ALLOWED_RECRUITER_VALUES}")

    rp_matches = re.finditer(r"\|\s*\*\*Recruitment Priority\*\*\s*\|\s*(.*?)\s*\|", content)
    for i, match in enumerate(rp_matches, 1):
        val = match.group(1).strip()
        if val not in ALLOWED_RECRUITMENT_PRIORITIES:
            errors.append(f"Claim #{i} has invalid Recruitment Priority: '{val}'. Allowed: {ALLOWED_RECRUITMENT_PRIORITIES}")
            
    return errors

def main():
    claim_path = pathlib.Path(__file__).resolve().parent.parent / "CLAIM_REGISTER.md"
    if not claim_path.is_file():
        print(f"ERROR: {claim_path} not found")
        sys.exit(1)
        
    content = claim_path.read_text(encoding="utf-8")
    errors = validate_claims(content)
    
    if errors:
        print(f"FAILED: CLAIM_REGISTER.md validation found {len(errors)} errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("PASS: CLAIM_REGISTER.md is valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
