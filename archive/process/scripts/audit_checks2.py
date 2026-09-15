import re

# Targeted check: look for "current/ongoing/till date/to date" used as ACTUAL date separators
# i.e., in patterns like "Feb 2024 - Current" or "Dates: current"
live_files = [
    r'public_portfolio\assets\downloads\CV_Master.html',
    r'public_portfolio\assets\downloads\CV_Primary_EAL.html',
    r'public_portfolio\assets\downloads\CV_EAL_Coordinator.html',
    r'public_portfolio\assets\downloads\CV_STEM_EAL.html',
    r'public_portfolio\assets\downloads\CV_Teacher_Development.html',
    r'compiled_assets\CV_Master.html',
    r'compiled_assets\CV_Primary_EAL.html',
    r'compiled_assets\linkedin\LinkedIn_Ready_To_Paste.md',
    r'templates\cv\profiles\master.json',
    r'templates\cv\profiles\eal.json',
    r'templates\cv\profiles\td.json',
    r'templates\cv\profiles\stem.json',
    r'templates\cv\profiles\coordinator.json',
]

# Only flag if the word appears as a DATE ENDPOINT, not in prose
date_endpoint_pattern = re.compile(
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+20\d\d\s*[–-]\s*(?:current|ongoing|till date|to date)',
    re.IGNORECASE
)

print('=== TARGETED CHECK: Bad Present variants as date endpoints ===')
found_any = False
for filepath in live_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = date_endpoint_pattern.findall(content)
        if matches:
            print(f'  FAIL: {filepath}')
            for m in matches:
                print(f'    {m}')
            found_any = True
        else:
            print(f'  PASS: {filepath}')
    except FileNotFoundError:
        print(f'  NOT FOUND: {filepath}')

print()
if not found_any:
    print('ALL PASS: No bad Present variants used as date endpoints.')
    print('NOTE: The word "Currently" in master.json/CV_Master is prose in the')
    print('PGCE education description - this is correct English and should stay.')
