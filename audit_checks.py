import os, re, sys

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

print('=== CHECK 1: HYPHENS AS DATE SEPARATORS ===')
hyphen_issues = []
for filepath in live_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Look for Mon YYYY - (hyphen, not en-dash) in date context
        matches = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+20\d\d\s+-\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Present)', content)
        if matches:
            hyphen_issues.append((filepath, matches))
    except FileNotFoundError:
        pass

if hyphen_issues:
    for f, m in hyphen_issues:
        print(f'  FAIL: {f}')
        for match in m:
            print(f'    Hyphen found: {match}')
else:
    print('  PASS: No hyphens as date separators found.')

print()
print('=== CHECK 2: PRESENT VARIANTS ===')
bad_variants = ['current', 'ongoing', 'till date', 'to date']
present_issues = []
for filepath in live_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        found = []
        for variant in bad_variants:
            for m in re.finditer(re.escape(variant), content, re.IGNORECASE):
                context = content[max(0, m.start()-40):m.end()+40]
                if re.search(r'20\d\d', context):
                    found.append(variant + ' :: ' + context.strip()[:80])
        if found:
            present_issues.append((filepath, found))
    except FileNotFoundError:
        pass

if present_issues:
    for f, issues in present_issues:
        print(f'  FAIL: {f}')
        for issue in issues:
            print(f'    {issue}')
else:
    print('  PASS: No bad Present variants near dates.')

print()
print('=== CHECK 3: PRESENT USED IN ACTIVE ROLE ===')
for filepath in live_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'Present' in content:
            print(f'  PASS: {filepath}')
        elif 'Aoxin' in content:
            print(f'  WARN (Aoxin but no Present): {filepath}')
        else:
            print(f'  SKIP (no Aoxin): {filepath}')
    except FileNotFoundError:
        print(f'  NOT FOUND: {filepath}')
