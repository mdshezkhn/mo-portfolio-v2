"""
Chronological Coherence Audit
Extracts employer name, job title, dates from every CV profile JSON
and flags any discrepancies across variants.
"""
import json, os, re

profile_dir = r"templates\cv\profiles"
profiles = {}

for fname in os.listdir(profile_dir):
    if fname.endswith(".json"):
        with open(os.path.join(profile_dir, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        profiles[fname] = data

# Ground truth from LinkedIn export
GROUND_TRUTH = {
    "aoxin_current": {
        "employer": "Aoxin International School",
        "title_keywords": ["EAL", "Primary", "Educator", "Curriculum"],
        "dates": ["Feb 2024", "Present"],
    },
    "gedu": {
        "employer": "GEDU Global Education",
        "title_keywords": ["Training", "Quality", "Lead"],
        "dates": ["Sep 2022", "Aug 2023"],
    },
    "whitehat": {
        "employer": ["WhiteHat Jr", "BYJU"],
        "title_keywords": ["Teacher Quality", "Development", "Manager"],
        "dates": ["Aug 2020", "Jul 2022"],
    },
    "aoxin_first": {
        "employer": "Aoxin International School",
        "dates": ["Jul 2018", "Aug 2020"],
    },
    "eton": {
        "employer": "Eton House",
        "dates": ["Aug 2017", "Jun 2018"],
    },
    "zhejiang": {
        "employer": ["Zhejiang", "Helen", "TEFL"],
        "dates": ["Nov 2016", "Aug 2017"],
    },
    "scholars": {
        "employer": "Scholars Academy",
        "dates": ["Jan 2014", "Nov 2016"],
    },
}

print("=" * 60)
print("CHRONOLOGICAL COHERENCE AUDIT")
print("=" * 60)
print()

all_entries = {}  # company -> set of dates across profiles

for profile_name, data in sorted(profiles.items()):
    print(f"--- {profile_name} ---")
    experience = data.get("experience", [])
    for entry in experience:
        company = entry.get("company", "MISSING")
        date = entry.get("date", "MISSING")
        title = entry.get("title", data.get("subtitle", "N/A"))
        
        print(f"  Company: {company}")
        print(f"  Date:    {date}")
        print(f"  Title:   {title}")
        
        if company not in all_entries:
            all_entries[company] = {}
        if date not in all_entries[company]:
            all_entries[company][date] = []
        all_entries[company][date].append(profile_name)
        print()
    print()

print("=" * 60)
print("CROSS-PROFILE DATE CONSISTENCY")
print("=" * 60)
print()

issues_found = False
for company, date_map in sorted(all_entries.items()):
    if len(date_map) > 1:
        print(f"  INCONSISTENCY: '{company}' has different dates across profiles:")
        for date, profiles_using in date_map.items():
            print(f"    '{date}' in: {profiles_using}")
        issues_found = True
    else:
        date = list(date_map.keys())[0]
        print(f"  CONSISTENT: '{company}' -> '{date}' in all profiles that include it.")

print()
if not issues_found:
    print("No date inconsistencies found across profiles.")
else:
    print("Issues found above require attention.")

print()
print("=" * 60)
print("EMPLOYER NAME VARIANTS")
print("=" * 60)
print()
for company in sorted(all_entries.keys()):
    print(f"  '{company}'")
