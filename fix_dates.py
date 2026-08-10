import os
import re

# Directory to search
repo_dir = r"c:\Users\Mohammed Shehzad\Documents\Mo Digital Portfolio"

# Exact replacements to make
replacements = {
    "2024–Present & 2018–2020": "Feb 2024 – Present & Jul 2018 – Aug 2020",
    "2022–2023": "Sep 2022 – Aug 2023",
    "2020–2022": "Aug 2020 – Jul 2022",
    "2018–2020": "Jul 2018 – Aug 2020",
    "2014–2016": "Jan 2014 – Nov 2016",
    # Education
    "(Expected 2026)": "(Sep 2025 – Sep 2026)",
    "Expected 2026": "Sep 2025 – Sep 2026",
    "(University of Cumbria, 2026)": "(University of Cumbria, Sep 2025 – Sep 2026)",
}

# The career direction replacement
old_direction_regex = re.compile(r"Seeking international or UK-aligned schools in the Gulf and Southeast Asia for an August 2027 start, growing into curriculum, pastoral, or STEM-integration leadership roles\.")
new_direction = "Targeting an August 2027 start at international or UK-aligned schools, with a strong geographic preference for China and Brunei, as well as key locations in the Gulf (Saudi Arabia, Bahrain, Oman, and Qatar)."

# Special contextual replacements
def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    
    # Apply exact replacements
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        # Handle cases with hyphen instead of en-dash
        new_content = new_content.replace(old.replace("–", "-"), new)

    # Handle Eton House 2016-2018 mistake specifically
    new_content = re.sub(r'Eton House Kindergarten([^"]*?)"2016[–-]2018"', r'Eton House Kindergarten\1"Aug 2017 – Jun 2018"', new_content)
    new_content = re.sub(r'Eton House Kindergarten\*\*.*?2016[–-]2018', r'Eton House Kindergarten**\n**Dates:** Aug 2017 – Jun 2018', new_content, flags=re.DOTALL)
    new_content = re.sub(r'Eton House Kindergarten.*?2017[–-]2018', r'Eton House Kindergarten\n- **Context:** Eton House Kindergarten, China, Aug 2017 – Jun 2018', new_content, flags=re.DOTALL)
    
    # Fix Achievement Library
    new_content = new_content.replace("Eton House Kindergarten, China, 2017–2018", "Eton House Kindergarten, China, Aug 2017 – Jun 2018")
    new_content = new_content.replace("Zhejiang University / Helen China TEFL Network, middle & high school, 2016–2017", "Zhejiang University / Helen China TEFL Network, middle & high school, Nov 2016 – Aug 2017")
    new_content = new_content.replace("Aoxin International School, primary team, 2018–2020", "Aoxin International School, primary team, Jul 2018 – Aug 2020")
    new_content = new_content.replace("Remote, high-scale EdTech environment (WhiteHat Jr / BYJU'S), 2020–2022", "Remote, high-scale EdTech environment (WhiteHat Jr / BYJU'S), Aug 2020 – Jul 2022")
    new_content = new_content.replace("Multi-campus organisation across UK, Dubai and Malta, 2022–2023", "Multi-campus organisation across UK, Dubai and Malta, Sep 2022 – Aug 2023")

    # Fix Career Direction
    new_content = old_direction_regex.sub(new_direction, new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

modified_files = []
for root, dirs, files in os.walk(repo_dir):
    if '.git' in root or 'node_modules' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith(('.md', '.html', '.json', '.txt')):
            filepath = os.path.join(root, file)
            try:
                if process_file(filepath):
                    modified_files.append(filepath)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

print("Modified files:")
for f in modified_files:
    print(f)
