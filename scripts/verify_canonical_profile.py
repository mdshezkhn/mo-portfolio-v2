#!/usr/bin/env python3
"""Validator for employment title fields in the portfolio repository.
Ensures each employment record in CANONICAL_PROFILE.md contains the required
fields, correct capitalization, ordering, date format, verification status,
no duplicate records, no overlapping dates for the same employer, and no unknown fields.
"""
import re
import sys
import pathlib
from collections import defaultdict
from difflib import get_close_matches

# Configuration constants
REQUIRED_FIELDS = [
    "Contract Title",
    "Official Title",
    "Portfolio Display Title",
    "Date"
]

ALLOWED_STATUSES = {
    "Pending verification",
    "Verified",
    "Partially verified",
    "Not independently verified",
}

PLACEHOLDERS = ["TBD", "TBA", "[", "]"]

def load_profile(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")

def extract_records(content: str):
    # Employment records are under "## 2. Immutable Employment Records"
    pattern = r"### Employment #\d+.*?(?=\n### Employment #|\n---|\Z)"
    return re.findall(pattern, content, flags=re.DOTALL)

def parse_date(date_str):
    """Parse 'Mmm YYYY' to an integer YYYYMM. Returns None if unparseable. Present is 999999."""
    if date_str.lower() == "present":
        return 999999
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    m = re.match(r"([A-Z][a-z]{2})\s+(\d{4})", date_val := date_str.strip())
    if m:
        month, year = m.groups()
        if month in months:
            return int(year) * 100 + months.index(month) + 1
    # Check just year
    m = re.match(r"^(\d{4})$", date_str.strip())
    if m:
        return int(m.group(1)) * 100 + 1
    return None

def check_record(record: str, record_id: str, all_records: list):
    errors = []
    lines = [line.strip() for line in record.splitlines() if line.strip()]
    
    present_fields = []
    field_lines = {}
    employer = None
    
    for i, line in enumerate(lines, 1):
        clean_line = line.strip()
        if clean_line.startswith('- '):
            clean_line = clean_line[2:]
        clean_line = clean_line.replace('**', '')
        
        m = re.match(r"^([^:]+):\s*(.*)", clean_line)
        if m:
            field_name = m.group(1).strip()
            field_val = m.group(2).strip()
            
            if field_name == "Employer":
                employer = field_val
                continue
                
            if field_name in ["Location", "Evidence ID", "Evidence Type", "Evidence Status", "Verification Status", "Dates"]:
                # Ignore metadata fields, except let's check for "Dates" vs "Date"
                if field_name == "Dates" and "Date" not in present_fields:
                    errors.append(f"Line {i}: Unknown field: '{field_name}'. Did you mean: 'Date'?")
                continue

            if field_name in REQUIRED_FIELDS:
                if field_name in present_fields:
                    errors.append(f"Line {i}: Duplicate field '{field_name}' in the same record.")
                else:
                    present_fields.append(field_name)
                    field_lines[field_name] = (i, field_val)
            else:
                matches = get_close_matches(field_name, REQUIRED_FIELDS, n=1, cutoff=0.5)
                suggestion = f" Did you mean '{matches[0]}'?" if matches else ""
                errors.append(f"Line {i}: Unknown field: '{field_name}'.{suggestion}")
            
            # Check for placeholders
            if not field_val:
                errors.append(f"Line {i}: Field '{field_name}' has an empty value.")
            elif any(p in field_val.upper() for p in ["TBD", "TBA", "[", "]"]):
                errors.append(f"Line {i}: Placeholder violation found in '{field_name}': '{field_val}'.")

    # Missing fields
    missing = [f for f in REQUIRED_FIELDS if f not in present_fields]
    if missing:
        errors.append(f"Missing required fields: {missing}")

    # Ordering
    expected_order = [f for f in REQUIRED_FIELDS if f in present_fields]
    if present_fields != expected_order:
        errors.append(f"Fields out of order. Expected sequence: {expected_order}, Found: {present_fields}")

    date_bounds = None
    # Date format and overlapping
    if "Date" in field_lines:
        ln, date_val = field_lines["Date"]
        if "Pending" not in date_val:
            m = re.fullmatch(r"([A-Z][a-z]{2} \d{4}|\d{4})\s[–-]\s([A-Z][a-z]{2} \d{4}|\d{4}|Present)", date_val)
            if not m:
                errors.append(f"Line {ln}: Invalid Date format '{date_val}'")
            else:
                start_val, end_val = m.groups()
                start_int = parse_date(start_val)
                end_int = parse_date(end_val)
                if start_int and end_int:
                    date_bounds = (start_int, end_int)

    # Verification status fields
    for field in ["Contract Title", "Official Title"]:
        if field in field_lines:
            ln, val = field_lines[field]
            if val and val not in ALLOWED_STATUSES:
                 errors.append(f"Line {ln}: Invalid verification status '{val}' for {field}. Allowed: {ALLOWED_STATUSES}")

    record_summary = {
        "employer": employer,
        "date_bounds": date_bounds,
        "portfolio_title": field_lines.get("Portfolio Display Title", (0, ""))[1],
        "date_str": field_lines.get("Date", (0, ""))[1],
    }
    all_records.append(record_summary)
    
    return errors

def main():
    profile_path = pathlib.Path(__file__).resolve().parent.parent / "CANONICAL_PROFILE.md"
    if not profile_path.is_file():
        print(f"ERROR: {profile_path} not found")
        sys.exit(1)
        
    content = load_profile(profile_path)
    records = extract_records(content)
    total = len(records)
    
    if total == 0:
        print("ERROR: No employment records found to validate.")
        sys.exit(1)

    passed = 0
    failed = 0
    all_parsed = []
    
    for i, rec in enumerate(records, 1):
        errs = check_record(rec, f"Employment #{i}", all_parsed)
        if errs:
            failed += 1
            print(f"File: CANONICAL_PROFILE.md | Record: Employment #{i} FAILED")
            for e in errs:
                print(f"  - {e}")
        else:
            passed += 1

    # Check duplicates and overlapping globally
    global_errors = []
    seen = set()
    employer_ranges = defaultdict(list)
    
    for idx, rp in enumerate(all_parsed, 1):
        # Duplicates
        identity = (rp["employer"], rp["date_str"], rp["portfolio_title"])
        if identity in seen:
            global_errors.append(f"Global FAILED: Duplicate employment record found for {identity}")
        seen.add(identity)
        
        # Overlapping for same employer
        if rp["employer"] and rp["date_bounds"]:
            st, en = rp["date_bounds"]
            for (ost, oen, oidx) in employer_ranges[rp["employer"]]:
                if max(st, ost) <= min(en, oen):
                    global_errors.append(f"Global FAILED: Overlapping dates for employer '{rp['employer']}' between Employment #{oidx} and Employment #{idx}.")
            employer_ranges[rp["employer"]].append((st, en, idx))

    if global_errors:
        for ge in global_errors:
            print(ge)
            failed += 1 # just count as another failure

    print(f"\nRecords checked: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    exit_code = 0 if failed == 0 else 1
    print(f"Exit code: {exit_code}")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
